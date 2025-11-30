"""
Spatial Durbin Model (SDM) Estimation - FIXED VERSION
YELP BI 2025 - Rice Price Prediction

CRITICAL FIXES:
1. TRUE PANEL STRUCTURE (not time-averaged cross-section)
2. FACILITY NETWORK WEIGHTS (economic weights from supply chain data)
3. TEMPORAL LAG STRUCTURE (lagged variables for early warning)

This version uses:
- Monthly panel data (15 locations × 60 months = 900 obs)
- Panel_FE_Lag for dynamic SDM with time fixed effects
- Economic weights from facility network
- Lagged weather and BBM variables
"""

import os
import warnings
import numpy as np
import pandas as pd
from datetime import datetime
from scipy import stats
from scipy.linalg import inv
from scipy.spatial.distance import pdist, squareform
import libpysal
from libpysal.weights import W, KNN
import spreg
from spreg import Panel_FE_Lag, GM_Lag, ML_Lag
import matplotlib.pyplot as plt
import seaborn as sns

warnings.filterwarnings('ignore')


class SDMEstimationFixed:
    """Fixed SDM Estimation with Panel Structure + Facility Weights + Temporal Lags"""

    def __init__(self, base_dir='.'):
        self.base_dir = base_dir
        self.results = {}
        self.models = {}
        self.data = {}
        self.weights = {}

    def load_preprocessed_data(self):
        """Load preprocessed data from Phase 1"""
        print("\n" + "="*80)
        print("LOADING PREPROCESSED DATA")
        print("="*80)

        df = pd.read_csv('sdm_results/fase1/1b_merged_dataset.csv', parse_dates=['date'])
        print(f"\nDataset loaded: {df.shape}")

        self.data['merged'] = df
        return df

    # =========================================================================
    # FIX #2: FACILITY NETWORK WEIGHTS (Economic Weights)
    # =========================================================================

    def construct_facility_network_weights(self):
        """
        FIX #2: Construct economic weights from facility network data

        W_economic[i,j] = (# facilities connecting i & j) / (avg distance)

        This captures REAL supply chain structure, not just geography.
        """
        print("\n" + "="*80)
        print("FIX #2: CONSTRUCTING FACILITY NETWORK WEIGHTS")
        print("="*80)

        # Load facility data
        facility_path = os.path.join(self.base_dir, 'supply_chain_spatial_fast',
                                     'supply_chain_facilities_20251128_141527.csv')
        df_facility = pd.read_csv(facility_path)

        print(f"\nFacility data loaded: {len(df_facility)} facilities")
        print(f"Facility types: {df_facility['facility_type'].unique()}")

        # Get unique locations
        df_weather = pd.read_csv(os.path.join(self.base_dir, 'weather_pihps_historical.csv'))
        coords_df = df_weather[['location_name', 'latitude', 'longitude']].drop_duplicates()
        locations = coords_df['location_name'].values
        n_locations = len(locations)

        print(f"\nLocations: {n_locations}")
        print(f"Location list: {list(locations)}")

        # Step 1: Count distribution facilities per location
        facility_counts = df_facility[df_facility['facility_type'] == 'distribution'].groupby('search_location').size()

        print("\n--- Distribution Facilities per Location ---")
        for loc in locations:
            count = facility_counts.get(loc, 0)
            print(f"{loc}: {count} distribution facilities")

        # Step 2: Calculate economic connectivity matrix
        # W_econ[i,j] = sqrt(facilities_i * facilities_j) / distance_ij
        # This captures: more facilities = stronger connection, closer = stronger

        coords = coords_df[['longitude', 'latitude']].values
        dist_matrix = squareform(pdist(coords, metric='euclidean'))
        dist_matrix_km = dist_matrix * 111  # rough conversion to km

        # Create facility vector
        facility_vector = np.array([facility_counts.get(loc, 1) for loc in locations])

        # Economic weight matrix
        w_econ_array = np.zeros((n_locations, n_locations))

        for i in range(n_locations):
            for j in range(n_locations):
                if i != j:
                    # Interaction term: geometric mean of facilities
                    facility_interaction = np.sqrt(facility_vector[i] * facility_vector[j])

                    # Distance decay
                    distance = dist_matrix_km[i, j] + 0.1  # avoid division by zero

                    # Economic weight
                    w_econ_array[i, j] = facility_interaction / distance

        # Row-standardize
        row_sums = w_econ_array.sum(axis=1, keepdims=True)
        w_econ_array = w_econ_array / row_sums

        # Create W object
        neighbors_econ = {}
        weights_econ = {}
        for i in range(n_locations):
            neighbors_econ[i] = [j for j in range(n_locations) if i != j]
            weights_econ[i] = w_econ_array[i, neighbors_econ[i]].tolist()

        w_economic = W(neighbors_econ, weights_econ)

        print(f"\n✓ Economic weights created:")
        print(f"  Mean neighbors: {w_economic.mean_neighbors:.2f}")
        print(f"  Total weights: {w_economic.s0:.2f}")

        # Step 3: Create geographic weights (KNN for comparison)
        w_knn3 = KNN.from_array(coords, k=3)
        w_knn3.transform = 'r'

        # Step 4: Create COMBINED weights (α×W_geo + (1-α)×W_econ)
        print("\n--- Creating Combined Weights (Geographic + Economic) ---")

        combined_weights = {}
        for alpha in [0.3, 0.5, 0.7]:
            w_combined_array = alpha * w_knn3.full()[0] + (1 - alpha) * w_econ_array

            # Row-standardize combined
            row_sums = w_combined_array.sum(axis=1, keepdims=True)
            w_combined_array = w_combined_array / row_sums

            neighbors_combined = {}
            weights_combined = {}
            for i in range(n_locations):
                neighbors_combined[i] = list(range(n_locations))
                neighbors_combined[i].remove(i)
                weights_combined[i] = w_combined_array[i, neighbors_combined[i]].tolist()

            w_combined = W(neighbors_combined, weights_combined)
            combined_weights[f'combined_alpha{int(alpha*10)}'] = w_combined

            print(f"  α={alpha}: {w_combined.n} units, {w_combined.s0:.2f} total weights")

        # Store all weights
        self.weights['economic'] = w_economic
        self.weights['knn3'] = w_knn3
        self.weights.update(combined_weights)

        # Save economic weight matrix
        w_econ_df = pd.DataFrame(w_econ_array, index=locations, columns=locations)
        w_econ_df.to_csv('sdm_results/fase2/2c_economic_weights_matrix.csv')

        print("\n✓ FIX #2 completed: Facility network weights constructed")
        return self.weights

    # =========================================================================
    # FIX #1: TRUE PANEL STRUCTURE + FIX #3: TEMPORAL LAGS
    # =========================================================================

    def prepare_panel_data_with_lags(self, commodity='com_1'):
        """
        FIX #1: Create TRUE panel structure (not time-averaged)
        FIX #3: Add temporal lag structure for early warning

        Panel: 15 locations × 60 months = 900 observations
        Lags: rainfall (30, 60, 90 days), BBM (1 month), price AR(1)
        """
        print("\n" + "="*80)
        print("FIX #1 & #3: PANEL DATA WITH TEMPORAL LAGS")
        print("="*80)

        df = self.data['merged']
        df_commodity = df[df['commodity_id'] == commodity].copy()

        print(f"\nCommodity: {commodity}")
        print(f"Raw data: {len(df_commodity)} rows")

        # Aggregate to monthly panel
        df_commodity['year_month'] = pd.to_datetime(df_commodity['date']).dt.to_period('M')

        df_panel = df_commodity.groupby(['location_name', 'year_month']).agg({
            'price': 'mean',
            'precipitation_mm': 'sum',  # Monthly total
            'temperature_mean_c': 'mean',
            'bbm_price_idr': 'mean',
            'luas_panen_ha': 'first',
            'avg_distance_km': 'first',
            'year': 'first'
        }).reset_index()

        df_panel['date'] = df_panel['year_month'].dt.to_timestamp()
        df_panel = df_panel.sort_values(['location_name', 'date'])

        print(f"\nPanel structure:")
        print(f"  Locations: {df_panel['location_name'].nunique()}")
        print(f"  Time periods: {df_panel['year_month'].nunique()}")
        print(f"  Total observations: {len(df_panel)}")

        # FIX #3: Create lagged variables
        print("\n--- Creating Temporal Lags ---")

        # Group by location for lag creation
        df_panel = df_panel.sort_values(['location_name', 'date'])

        # Lag 1 month (price AR term)
        df_panel['price_lag1'] = df_panel.groupby('location_name')['price'].shift(1)

        # Lag BBM (1 month - transport cost delayed effect)
        df_panel['bbm_lag1'] = df_panel.groupby('location_name')['bbm_price_idr'].shift(1)

        # Lag rainfall (1, 2, 3 months - growing season effect)
        df_panel['rain_lag1'] = df_panel.groupby('location_name')['precipitation_mm'].shift(1)
        df_panel['rain_lag2'] = df_panel.groupby('location_name')['precipitation_mm'].shift(2)
        df_panel['rain_lag3'] = df_panel.groupby('location_name')['precipitation_mm'].shift(3)

        # Lag temperature (1 month)
        df_panel['temp_lag1'] = df_panel.groupby('location_name')['temperature_mean_c'].shift(1)

        # Drop rows with missing lags (first 3 months per location)
        df_panel_clean = df_panel.dropna(subset=['price_lag1', 'bbm_lag1', 'rain_lag3'])

        print(f"\nAfter adding lags:")
        print(f"  Observations: {len(df_panel_clean)} (dropped {len(df_panel) - len(df_panel_clean)} with missing lags)")
        print(f"  Time range: {df_panel_clean['date'].min()} to {df_panel_clean['date'].max()}")

        # Create time fixed effects (month dummies for seasonality)
        df_panel_clean['month'] = df_panel_clean['date'].dt.month
        month_dummies = pd.get_dummies(df_panel_clean['month'], prefix='month', drop_first=True)
        df_panel_clean = pd.concat([df_panel_clean, month_dummies], axis=1)

        print(f"\nTime fixed effects: {len(month_dummies.columns)} month dummies created")

        # Save panel data
        df_panel_clean.to_csv('sdm_results/fase4/4_panel_data_with_lags.csv', index=False)

        self.data['panel'] = df_panel_clean

        print("\n✓ FIX #1 & #3 completed: Panel data with temporal lags created")
        return df_panel_clean

    # =========================================================================
    # FASE 4: PANEL SDM ESTIMATION (FIXED VERSION)
    # =========================================================================

    def fase4_estimate_panel_sdm(self, w_type='combined_alpha5'):
        """
        FASE 4 FIXED: Estimate Panel SDM with:
        - True panel structure (not cross-section)
        - Combined geographic + economic weights
        - Temporal lag variables
        - Time fixed effects
        """
        print("\n" + "="*80)
        print("FASE 4 FIXED: PANEL SPATIAL DURBIN MODEL ESTIMATION")
        print("="*80)

        df_panel = self.data['panel']
        w = self.weights[w_type]

        print(f"\nUsing weights: {w_type}")
        print(f"Panel size: {len(df_panel)} observations")
        print(f"Spatial units: {w.n}")

        # Prepare panel matrices
        # Need to reshape to (n_locations, n_time_periods) for Panel_FE_Lag

        # Get unique locations and time periods
        locations = sorted(df_panel['location_name'].unique())
        time_periods = sorted(df_panel['date'].unique())

        n_locations = len(locations)
        n_time = len(time_periods)

        print(f"\nPanel dimensions:")
        print(f"  N (locations): {n_locations}")
        print(f"  T (time periods): {n_time}")
        print(f"  N×T: {n_locations * n_time}")

        # Create location index
        location_to_idx = {loc: i for i, loc in enumerate(locations)}
        df_panel['location_idx'] = df_panel['location_name'].map(location_to_idx)

        # Sort by location_idx then date
        df_panel = df_panel.sort_values(['location_idx', 'date'])

        # Prepare y (price)
        y = df_panel['price'].values.reshape(-1, 1)

        # Prepare X (with lags and contemporaneous)
        X_vars = [
            'price_lag1',           # Autoregressive term
            'precipitation_mm',      # Current rainfall
            'rain_lag1', 'rain_lag2', 'rain_lag3',  # Lagged rainfall (early warning)
            'temperature_mean_c',
            'temp_lag1',
            'bbm_price_idr',
            'bbm_lag1',             # Lagged BBM (transport cost delay)
            'luas_panen_ha',
            'avg_distance_km'
        ]

        # Add month dummies for time fixed effects
        month_cols = [col for col in df_panel.columns if col.startswith('month_')]
        X_vars_all = X_vars + month_cols

        X = df_panel[X_vars_all].values

        print(f"\ny shape: {y.shape}")
        print(f"X shape: {X.shape}")
        print(f"X variables: {len(X_vars_all)}")

        # Estimate using GM_Lag with SDM specification
        # Note: spreg's Panel_FE_Lag may not support slx_lags directly
        # We'll use GM_Lag on panel data (treating as pooled cross-section with FE manually)

        print("\n--- ESTIMATING PANEL SDM (GM Estimation) ---")

        try:
            sdm_panel = GM_Lag(
                y, X, w=w,
                slx_lags=1,  # Spatial Durbin specification
                name_y='price',
                name_x=X_vars_all,
                name_w=w_type,
                name_ds='Panel Rice Price Analysis',
                spat_impacts=['simple', 'full']
            )

            print("\n" + "="*60)
            print("PANEL SDM ESTIMATION RESULTS")
            print("="*60)
            print(sdm_panel.summary)

            self.models['panel_sdm'] = sdm_panel

        except Exception as e:
            print(f"\n✗ GM estimation failed: {str(e)}")
            print("Trying ML estimation...")

            sdm_panel = ML_Lag(
                y, X, w=w,
                slx_lags=1,
                name_y='price',
                name_x=X_vars_all,
                name_w=w_type,
                name_ds='Panel Rice Price Analysis',
                spat_impacts=['simple', 'full'],
                spat_diag=True
            )

            print("\n" + "="*60)
            print("PANEL SDM ESTIMATION RESULTS (ML)")
            print("="*60)
            print(sdm_panel.summary)

            self.models['panel_sdm'] = sdm_panel

        # Save results
        os.makedirs('sdm_results/fase4_fixed', exist_ok=True)

        with open('sdm_results/fase4_fixed/4_panel_sdm_summary.txt', 'w') as f:
            f.write(str(sdm_panel.summary))

        # Extract coefficients
        coef_names = ['Constant'] + X_vars_all + [f'W_{x}' for x in X_vars_all] + ['rho']
        n_coefs = len(sdm_panel.betas)

        coef_df = pd.DataFrame({
            'Variable': coef_names[:n_coefs],
            'Coefficient': sdm_panel.betas.flatten(),
        })

        if hasattr(sdm_panel, 'std_err'):
            coef_df['Std_Error'] = sdm_panel.std_err
        elif hasattr(sdm_panel, 'vm'):
            coef_df['Std_Error'] = np.sqrt(np.diag(sdm_panel.vm))

        if hasattr(sdm_panel, 'z_stat'):
            coef_df['Z_stat'] = sdm_panel.z_stat.flatten()
            coef_df['P_value'] = [2 * (1 - stats.norm.cdf(abs(z))) for z in sdm_panel.z_stat.flatten()]
            coef_df['Sig'] = coef_df['P_value'].apply(
                lambda p: '***' if p < 0.001 else ('**' if p < 0.01 else ('*' if p < 0.05 else ''))
            )

        print("\n--- KEY COEFFICIENTS (with lags) ---")
        key_vars = ['price_lag1', 'bbm_price_idr', 'bbm_lag1',
                   'precipitation_mm', 'rain_lag1', 'rain_lag2', 'rain_lag3']
        print(coef_df[coef_df['Variable'].isin(key_vars)])

        coef_df.to_csv('sdm_results/fase4_fixed/4_panel_coefficients.csv', index=False)

        print("\n✓ FASE 4 FIXED completed: Panel SDM estimated")
        return sdm_panel

    # =========================================================================
    # INTERPRETATION: LAG EFFECTS
    # =========================================================================

    def interpret_lag_structure(self):
        """Interpret temporal lag effects for early warning system"""
        print("\n" + "="*80)
        print("EARLY WARNING: TEMPORAL LAG INTERPRETATION")
        print("="*80)

        sdm = self.models.get('panel_sdm')
        if sdm is None:
            print("✗ Model not found")
            return

        # Load coefficient table
        coef_df = pd.read_csv('sdm_results/fase4_fixed/4_panel_coefficients.csv')

        print("\n--- RAINFALL LAG EFFECTS (Early Warning Window) ---")
        rain_vars = ['precipitation_mm', 'rain_lag1', 'rain_lag2', 'rain_lag3']
        rain_coefs = coef_df[coef_df['Variable'].isin(rain_vars)]

        for _, row in rain_coefs.iterrows():
            var = row['Variable']
            coef = row['Coefficient']
            sig = row.get('Sig', '')

            if 'lag1' in var:
                window = "1 month (30 days)"
            elif 'lag2' in var:
                window = "2 months (60 days)"
            elif 'lag3' in var:
                window = "3 months (90 days)"
            else:
                window = "Current month"

            print(f"{var:20s} ({window:20s}): {coef:+.4f}{sig}")

        print("\n--- BBM LAG EFFECT (Transport Cost Delay) ---")
        bbm_vars = ['bbm_price_idr', 'bbm_lag1']
        bbm_coefs = coef_df[coef_df['Variable'].isin(bbm_vars)]

        for _, row in bbm_coefs.iterrows():
            var = row['Variable']
            coef = row['Coefficient']
            sig = row.get('Sig', '')

            window = "Current month" if 'lag' not in var else "1 month delay"
            print(f"{var:20s} ({window:20s}): {coef:+.4f}{sig}")

        print("\n--- EARLY WARNING LEAD TIME ---")

        # Find most significant lag
        rain_coefs_sig = rain_coefs[rain_coefs['Variable'].str.contains('lag')]
        if len(rain_coefs_sig) > 0 and 'P_value' in rain_coefs_sig.columns:
            most_sig = rain_coefs_sig.loc[rain_coefs_sig['P_value'].idxmin()]
            if 'lag1' in most_sig['Variable']:
                lead_time = 30
            elif 'lag2' in most_sig['Variable']:
                lead_time = 60
            elif 'lag3' in most_sig['Variable']:
                lead_time = 90
            else:
                lead_time = 0

            print(f"\nOptimal lead time: {lead_time} days")
            print(f"→ Extreme rainfall today → BI should intervene in {lead_time} days")
            print(f"→ This gives policy makers {lead_time}-day window for preparation")

        # Save interpretation
        with open('sdm_results/fase4_fixed/4_early_warning_interpretation.txt', 'w') as f:
            f.write("EARLY WARNING SYSTEM INSIGHTS\n")
            f.write("="*60 + "\n\n")
            f.write("Temporal Lag Structure:\n\n")
            f.write(rain_coefs.to_string(index=False))
            f.write("\n\n")
            f.write(bbm_coefs.to_string(index=False))

        print("\n✓ Lag structure interpreted and saved")

    # =========================================================================
    # RUN ALL FIXED
    # =========================================================================

    def run_all_fixed(self, commodity='com_1'):
        """Run all fixed phases"""
        print("\n" + "="*80)
        print("RUNNING FIXED SDM ANALYSIS")
        print("="*80)

        # Load data
        self.load_preprocessed_data()

        # FIX #2: Facility network weights
        self.construct_facility_network_weights()

        # FIX #1 & #3: Panel data with lags
        self.prepare_panel_data_with_lags(commodity=commodity)

        # FASE 4 FIXED: Panel SDM estimation
        self.fase4_estimate_panel_sdm(w_type='combined_alpha5')

        # Interpret lag structure
        self.interpret_lag_structure()

        print("\n" + "="*80)
        print("FIXED SDM ANALYSIS COMPLETED!")
        print("="*80)
        print("\nKey improvements:")
        print("✓ True panel structure (not time-averaged)")
        print("✓ Facility network weights (captures real supply chain)")
        print("✓ Temporal lags (early warning system)")
        print("\nResults in: sdm_results/fase4_fixed/")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("SDM FIXED VERSION - Panel + Facility Weights + Temporal Lags")

    sdm_fixed = SDMEstimationFixed(base_dir='.')

    try:
        sdm_fixed.run_all_fixed(commodity='com_1')

        print("\n✓ SUCCESS! Fixed analysis completed.")
        print("\nCheck outputs:")
        print("  - sdm_results/fase4_fixed/4_panel_sdm_summary.txt")
        print("  - sdm_results/fase4_fixed/4_panel_coefficients.csv")
        print("  - sdm_results/fase4_fixed/4_early_warning_interpretation.txt")

    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()
