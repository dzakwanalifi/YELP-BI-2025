"""
Spatial Durbin Model (SDM) Estimation - Advanced Phases 4-7
YELP BI 2025 - Rice Price Prediction

This script continues from sdm_analysis_complete.py to implement:
4. Model Estimation (SDM with Fixed Effects)
5. Output & Interpretation (Effects Decomposition)
6. Validation & Robustness
7. Policy Simulation

Requirements:
    pip install pandas numpy scipy statsmodels pysal spreg libpysal esda splot geopandas
"""

import os
import pickle
import warnings
import numpy as np
import pandas as pd
from datetime import datetime
from scipy import stats
from scipy.linalg import inv
import libpysal
from libpysal.weights import W, KNN
import spreg
from spreg import Panel_FE_Lag, GM_Lag, ML_Lag
import matplotlib.pyplot as plt
import seaborn as sns

warnings.filterwarnings('ignore')


class SDMEstimation:
    """Spatial Durbin Model Estimation and Advanced Analysis"""

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

        # Load merged dataset
        df = pd.read_csv('sdm_results/fase1/1b_merged_dataset.csv', parse_dates=['date'])
        print(f"\nDataset loaded: {df.shape}")

        self.data['merged'] = df
        return df

    def reconstruct_spatial_weights(self):
        """Reconstruct spatial weights matrices"""
        print("\n--- Reconstructing spatial weights ---")

        df_weather = pd.read_csv(os.path.join(self.base_dir, 'weather_pihps_historical.csv'))
        coords_df = df_weather[['location_name', 'latitude', 'longitude']].drop_duplicates()
        coords = coords_df[['longitude', 'latitude']].values

        # Create KNN weights
        for k in [3, 5, 8]:
            w_knn = KNN.from_array(coords, k=k)
            w_knn.transform = 'r'
            self.weights[f'knn{k}'] = w_knn

        print(f"Spatial weights reconstructed: {list(self.weights.keys())}")
        return self.weights

    # =========================================================================
    # FASE 4: MODEL ESTIMATION
    # =========================================================================

    def fase4_estimate_sdm(self, commodity='com_1', w_type='knn3'):
        """FASE 4: Estimate Spatial Durbin Model with Fixed Effects"""
        print("\n" + "="*80)
        print("FASE 4: SPATIAL DURBIN MODEL ESTIMATION")
        print("="*80)

        df = self.data['merged']
        w = self.weights[w_type]

        # Filter for commodity
        df_commodity = df[df['commodity_id'] == commodity].copy()

        print(f"\nCommodity: {commodity}")
        print(f"Sample size: {len(df_commodity)}")
        print(f"Spatial weights: {w_type} ({w.n} units)")

        # Aggregate to location-year-month for panel structure
        # This creates a manageable panel
        df_commodity['year_month'] = pd.to_datetime(df_commodity['date']).dt.to_period('M')

        df_panel = df_commodity.groupby(['location_name', 'year_month']).agg({
            'price': 'mean',
            'precipitation_mm': 'sum',  # Total monthly precipitation
            'temperature_mean_c': 'mean',
            'bbm_price_idr': 'mean',
            'luas_panen_ha': 'first',
            'avg_distance_km': 'first',
            'year': 'first'
        }).reset_index()

        # Convert period to datetime for sorting
        df_panel['date'] = df_panel['year_month'].dt.to_timestamp()
        df_panel = df_panel.sort_values(['location_name', 'date'])

        print(f"\nPanel structure:")
        print(f"  Time periods: {df_panel['year_month'].nunique()}")
        print(f"  Locations: {df_panel['location_name'].nunique()}")
        print(f"  Total observations: {len(df_panel)}")

        # Prepare panel data matrices
        # spreg Panel_FE_Lag expects data in wide format (T×N) or long format
        # We'll use cross-sectional approach with time-averaged data first

        # Option 1: Time-averaged cross-section (for simplicity)
        print("\n--- Using Time-Averaged Cross-Sectional Data ---")

        df_cross = df_panel.groupby('location_name').agg({
            'price': 'mean',
            'precipitation_mm': 'mean',
            'temperature_mean_c': 'mean',
            'bbm_price_idr': 'mean',
            'luas_panen_ha': 'mean',
            'avg_distance_km': 'first'
        }).reset_index()

        # Get coordinates for proper ordering
        df_weather = pd.read_csv(os.path.join(self.base_dir, 'weather_pihps_historical.csv'))
        coords_df = df_weather[['location_name', 'latitude', 'longitude']].drop_duplicates()
        df_cross = df_cross.merge(coords_df, on='location_name', how='left')
        df_cross = df_cross.dropna()

        print(f"Cross-sectional observations: {len(df_cross)}")

        # Prepare y and X
        y = df_cross['price'].values.reshape(-1, 1)
        X_vars = ['precipitation_mm', 'temperature_mean_c', 'bbm_price_idr',
                 'luas_panen_ha', 'avg_distance_km']
        X = df_cross[X_vars].values

        print(f"\ny shape: {y.shape}")
        print(f"X shape: {X.shape}")

        # Estimate Spatial Durbin Model using GM_Lag (Generalized Method of Moments)
        print("\n--- ESTIMATING SPATIAL DURBIN MODEL (GM) ---")

        try:
            sdm = GM_Lag(
                y, X, w=w,
                slx_lags=1,  # This creates the Spatial Durbin specification
                name_y='price',
                name_x=X_vars,
                name_w=w_type,
                name_ds='Rice Price Analysis',
                spat_impacts=['simple', 'full']  # Calculate direct/indirect effects
            )

            print("\n" + "="*60)
            print("SDM ESTIMATION RESULTS")
            print("="*60)
            print(sdm.summary)

            # Store model
            self.models['sdm_gm'] = sdm

        except Exception as e:
            print(f"\n✗ GM estimation failed: {str(e)}")
            print("Trying ML estimation instead...")

            # Try Maximum Likelihood
            sdm = ML_Lag(
                y, X, w=w,
                slx_lags=1,
                name_y='price',
                name_x=X_vars,
                name_w=w_type,
                name_ds='Rice Price Analysis',
                spat_impacts=['simple', 'full'],
                spat_diag=True
            )

            print("\n" + "="*60)
            print("SDM ESTIMATION RESULTS (ML)")
            print("="*60)
            print(sdm.summary)

            self.models['sdm_ml'] = sdm

        # Save model summary
        with open('sdm_results/fase4/4_sdm_summary.txt', 'w') as f:
            f.write(str(sdm.summary))

        # Extract and save coefficients
        coef_names = ['Constant'] + X_vars + [f'W_{x}' for x in X_vars] + ['rho']
        n_coefs = len(sdm.betas)

        coef_df = pd.DataFrame({
            'Variable': coef_names[:n_coefs],
            'Coefficient': sdm.betas.flatten(),
            'Std_Error': np.sqrt(np.diag(sdm.vm)) if hasattr(sdm, 'vm') else [np.nan]*n_coefs,
        })

        if hasattr(sdm, 'z_stat'):
            coef_df['Z_stat'] = sdm.z_stat.flatten()
            coef_df['P_value'] = [2 * (1 - stats.norm.cdf(abs(z))) for z in sdm.z_stat.flatten()]

        print("\n--- COEFFICIENT ESTIMATES ---")
        print(coef_df)

        coef_df.to_csv('sdm_results/fase4/4_coefficients.csv', index=False)

        print("\n✓ FASE 4 completed.")
        return sdm

    # =========================================================================
    # FASE 5: OUTPUT & INTERPRETATION
    # =========================================================================

    def fase5a_model_fit_statistics(self):
        """FASE 5A: Calculate model fit statistics"""
        print("\n" + "="*80)
        print("FASE 5A: MODEL FIT STATISTICS")
        print("="*80)

        sdm = self.models.get('sdm_gm') or self.models.get('sdm_ml')

        if sdm is None:
            print("✗ No model found. Run fase4 first.")
            return

        # Extract fit statistics
        print("\n--- MODEL FIT STATISTICS ---")

        stats_dict = {
            'N_observations': sdm.n,
            'N_variables': sdm.k,
        }

        # R-squared
        if hasattr(sdm, 'pr2'):
            stats_dict['Pseudo_R2'] = sdm.pr2
            print(f"Pseudo R²: {sdm.pr2:.4f}")

        # Log-likelihood
        if hasattr(sdm, 'logll'):
            stats_dict['Log_Likelihood'] = sdm.logll
            print(f"Log-Likelihood: {sdm.logll:.2f}")

        # AIC
        if hasattr(sdm, 'aic'):
            stats_dict['AIC'] = sdm.aic
            print(f"AIC: {sdm.aic:.2f}")

        # BIC (calculate manually if not available)
        if hasattr(sdm, 'logll'):
            bic = -2 * sdm.logll + sdm.k * np.log(sdm.n)
            stats_dict['BIC'] = bic
            print(f"BIC: {bic:.2f}")

        # RMSE
        if hasattr(sdm, 'u'):
            rmse = np.sqrt(np.mean(sdm.u ** 2))
            stats_dict['RMSE'] = rmse
            print(f"RMSE: Rp {rmse:.2f}")

        # MAPE
        if hasattr(sdm, 'y') and hasattr(sdm, 'predy'):
            mape = np.mean(np.abs((sdm.y - sdm.predy) / sdm.y)) * 100
            stats_dict['MAPE'] = mape
            print(f"MAPE: {mape:.2f}%")

        # Spatial rho
        if hasattr(sdm, 'rho'):
            stats_dict['Rho'] = sdm.rho
            print(f"Spatial Rho (ρ): {sdm.rho:.4f}")

        # Save
        stats_df = pd.DataFrame([stats_dict])
        stats_df.to_csv('sdm_results/fase5/5a_model_fit.csv', index=False)

        self.results['fase5a'] = stats_df
        print("\n✓ FASE 5A completed.")
        return stats_df

    def fase5b_effects_decomposition(self):
        """FASE 5B: Decompose Direct, Indirect, and Total Effects"""
        print("\n" + "="*80)
        print("FASE 5B: EFFECTS DECOMPOSITION")
        print("="*80)

        sdm = self.models.get('sdm_gm') or self.models.get('sdm_ml')

        if sdm is None or not hasattr(sdm, 'direct'):
            print("✗ No spatial impacts available. Model may not support decomposition.")
            return

        # Extract direct, indirect, total effects
        print("\n--- DIRECT EFFECTS ---")
        print("(Average effect of X in location i on Y in location i)")
        print(sdm.direct)

        print("\n--- INDIRECT EFFECTS (Spillover) ---")
        print("(Average effect of X in location j on Y in location i)")
        print(sdm.indirect)

        print("\n--- TOTAL EFFECTS ---")
        print("(Direct + Indirect)")
        print(sdm.total)

        # Create summary table
        X_vars = ['precipitation_mm', 'temperature_mean_c', 'bbm_price_idr',
                 'luas_panen_ha', 'avg_distance_km']

        effects_data = []

        for i, var in enumerate(X_vars):
            effects_data.append({
                'Variable': var,
                'Direct_Effect': sdm.direct[i] if hasattr(sdm, 'direct') else np.nan,
                'Indirect_Effect': sdm.indirect[i] if hasattr(sdm, 'indirect') else np.nan,
                'Total_Effect': sdm.total[i] if hasattr(sdm, 'total') else np.nan,
            })

        effects_df = pd.DataFrame(effects_data)

        print("\n--- EFFECTS SUMMARY TABLE ---")
        print(effects_df)

        # Interpretation
        print("\n--- INTERPRETATION EXAMPLE ---")
        print("\nVariable: BBM (bbm_price_idr)")
        bbm_idx = X_vars.index('bbm_price_idr')
        if hasattr(sdm, 'direct'):
            direct_bbm = sdm.direct[bbm_idx]
            indirect_bbm = sdm.indirect[bbm_idx]
            total_bbm = sdm.total[bbm_idx]

            print(f"Direct: {direct_bbm:.4f}")
            print(f"  → BBM +Rp 1000/liter → local price +Rp {direct_bbm * 1000:.2f}/kg")

            print(f"Indirect: {indirect_bbm:.4f}")
            print(f"  → BBM +Rp 1000 in neighbor → local price +Rp {indirect_bbm * 1000:.2f}/kg")

            print(f"Total: {total_bbm:.4f}")
            print(f"  → Total system effect: +Rp {total_bbm * 1000:.2f}/kg")

        # Save
        effects_df.to_csv('sdm_results/fase5/5b_effects_decomposition.csv', index=False)

        self.results['fase5b'] = effects_df
        print("\n✓ FASE 5B completed.")
        return effects_df

    def fase5c_spatial_multiplier(self):
        """FASE 5C: Calculate spatial multiplier matrix"""
        print("\n" + "="*80)
        print("FASE 5C: SPATIAL MULTIPLIER ANALYSIS")
        print("="*80)

        sdm = self.models.get('sdm_gm') or self.models.get('sdm_ml')
        w = self.weights.get('knn3')

        if sdm is None or w is None:
            print("✗ Model or weights not available.")
            return

        # Extract rho
        rho = sdm.rho if hasattr(sdm, 'rho') else 0

        print(f"\nSpatial lag parameter (ρ): {rho:.4f}")

        # Spatial multiplier: (I - ρW)^(-1)
        n = w.n
        W_full = w.full()[0]  # Get full weight matrix

        I = np.eye(n)
        multiplier_matrix = inv(I - rho * W_full)

        print(f"\nMultiplier matrix shape: {multiplier_matrix.shape}")

        # Diagonal elements (own-location effects)
        diag_multipliers = np.diag(multiplier_matrix)
        print(f"Average own-location multiplier: {np.mean(diag_multipliers):.4f}")
        print(f"Range: {np.min(diag_multipliers):.4f} - {np.max(diag_multipliers):.4f}")

        # Get location names
        df_weather = pd.read_csv(os.path.join(self.base_dir, 'weather_pihps_historical.csv'))
        coords_df = df_weather[['location_name', 'latitude', 'longitude']].drop_duplicates()
        locations = coords_df['location_name'].values

        # Create multiplier dataframe
        multiplier_df = pd.DataFrame(
            multiplier_matrix,
            index=locations[:n],
            columns=locations[:n]
        )

        print("\n--- MULTIPLIER MATRIX (sample) ---")
        print(multiplier_df.iloc[:5, :5])

        # Interpretation
        print("\n--- INTERPRETATION ---")
        print("Shock of Rp 1 in location i → total effect on location j:")
        print(f"  Jakarta → Jakarta: Rp {multiplier_df.iloc[0, 0] if 'DKI Jakarta' in locations else 'N/A':.2f}")
        print(f"  Jakarta → Others: Rp {multiplier_df.iloc[0, 1:].mean():.2f} (average)")

        # Save
        multiplier_df.to_csv('sdm_results/fase5/5c_spatial_multiplier_matrix.csv')

        # Save summary statistics
        multiplier_summary = pd.DataFrame({
            'Location': locations[:n],
            'Own_Effect': diag_multipliers,
            'Spillover_to_Others': [multiplier_matrix[i, :].sum() - multiplier_matrix[i, i] for i in range(n)],
            'Total_Effect': multiplier_matrix.sum(axis=1)
        })

        multiplier_summary.to_csv('sdm_results/fase5/5c_multiplier_summary.csv', index=False)

        self.results['fase5c'] = {
            'multiplier_matrix': multiplier_df,
            'summary': multiplier_summary
        }

        print("\n✓ FASE 5C completed.")
        return multiplier_df

    # =========================================================================
    # FASE 6: VALIDATION & ROBUSTNESS
    # =========================================================================

    def fase6a_residual_diagnostics(self):
        """FASE 6A: Post-estimation residual diagnostics"""
        print("\n" + "="*80)
        print("FASE 6A: RESIDUAL DIAGNOSTICS")
        print("="*80)

        sdm = self.models.get('sdm_gm') or self.models.get('sdm_ml')
        w = self.weights.get('knn3')

        if sdm is None:
            print("✗ Model not available.")
            return

        # Extract residuals
        residuals = sdm.u.flatten()

        print(f"\nResiduals shape: {residuals.shape}")
        print(f"Mean: {np.mean(residuals):.6f}")
        print(f"Std: {np.std(residuals):.2f}")

        # Spatial autocorrelation of residuals (Moran's I)
        print("\n--- MORAN'S I OF RESIDUALS ---")
        from esda.moran import Moran

        moran_resid = Moran(residuals, w)

        print(f"Moran's I: {moran_resid.I:.4f}")
        print(f"Expected I: {moran_resid.EI:.4f}")
        print(f"P-value: {moran_resid.p_norm:.6f}")

        if abs(moran_resid.I) < 0.1 and moran_resid.p_norm > 0.05:
            print("✓ No spatial autocorrelation in residuals (good!)")
        else:
            print("⚠ Residual spatial autocorrelation detected")

        # Normality test (Jarque-Bera)
        print("\n--- NORMALITY TEST (Jarque-Bera) ---")
        from scipy.stats import jarque_bera

        jb_stat, jb_pvalue = jarque_bera(residuals)
        print(f"JB Statistic: {jb_stat:.4f}")
        print(f"P-value: {jb_pvalue:.6f}")

        if jb_pvalue > 0.05:
            print("✓ Residuals approximately normal")
        else:
            print("⚠ Residuals not normally distributed (common in large samples)")

        # Save diagnostics
        diag_df = pd.DataFrame([{
            'Moran_I_residuals': moran_resid.I,
            'Moran_p_value': moran_resid.p_norm,
            'JB_statistic': jb_stat,
            'JB_p_value': jb_pvalue,
            'Residual_mean': np.mean(residuals),
            'Residual_std': np.std(residuals)
        }])

        diag_df.to_csv('sdm_results/fase6/6a_residual_diagnostics.csv', index=False)

        self.results['fase6a'] = diag_df
        print("\n✓ FASE 6A completed.")
        return diag_df

    def fase6b_robustness_checks(self):
        """FASE 6B: Robustness checks with alternative specifications"""
        print("\n" + "="*80)
        print("FASE 6B: ROBUSTNESS CHECKS")
        print("="*80)

        print("\nTesting model robustness with alternative spatial weights...")

        df = self.data['merged']
        df_commodity = df[df['commodity_id'] == 'com_1'].copy()

        df_commodity['year_month'] = pd.to_datetime(df_commodity['date']).dt.to_period('M')
        df_panel = df_commodity.groupby(['location_name', 'year_month']).agg({
            'price': 'mean',
            'precipitation_mm': 'sum',
            'temperature_mean_c': 'mean',
            'bbm_price_idr': 'mean',
            'luas_panen_ha': 'first',
            'avg_distance_km': 'first',
        }).reset_index()

        df_panel['date'] = df_panel['year_month'].dt.to_timestamp()
        df_panel = df_panel.sort_values(['location_name', 'date'])

        df_cross = df_panel.groupby('location_name').agg({
            'price': 'mean',
            'precipitation_mm': 'mean',
            'temperature_mean_c': 'mean',
            'bbm_price_idr': 'mean',
            'luas_panen_ha': 'mean',
            'avg_distance_km': 'first'
        }).reset_index()

        df_weather = pd.read_csv(os.path.join(self.base_dir, 'weather_pihps_historical.csv'))
        coords_df = df_weather[['location_name', 'latitude', 'longitude']].drop_duplicates()
        df_cross = df_cross.merge(coords_df, on='location_name', how='left').dropna()

        y = df_cross['price'].values.reshape(-1, 1)
        X_vars = ['precipitation_mm', 'temperature_mean_c', 'bbm_price_idr',
                 'luas_panen_ha', 'avg_distance_km']
        X = df_cross[X_vars].values

        # Test with different W matrices
        robustness_results = []

        for w_name in ['knn3', 'knn5', 'knn8']:
            print(f"\n--- Testing with {w_name} ---")

            w = self.weights.get(w_name)
            if w is None:
                print(f"  Skipping {w_name} (not available)")
                continue

            try:
                sdm_temp = GM_Lag(
                    y, X, w=w,
                    slx_lags=1,
                    name_y='price',
                    name_x=X_vars,
                    name_w=w_name,
                    name_ds='Robustness'
                )

                # Extract key coefficients
                rho = sdm_temp.rho if hasattr(sdm_temp, 'rho') else np.nan
                bbm_coef = sdm_temp.betas[3, 0]  # Assuming BBM is 3rd variable (index 3 with constant)

                robustness_results.append({
                    'W_type': w_name,
                    'Rho': rho,
                    'BBM_coef': bbm_coef,
                    'Pseudo_R2': sdm_temp.pr2 if hasattr(sdm_temp, 'pr2') else np.nan,
                    'N': sdm_temp.n
                })

                print(f"  ρ = {rho:.4f}, BBM_coef = {bbm_coef:.4f}")

            except Exception as e:
                print(f"  Error: {str(e)}")

        # Create comparison table
        if len(robustness_results) > 0:
            robust_df = pd.DataFrame(robustness_results)

            print("\n--- ROBUSTNESS COMPARISON ---")
            print(robust_df)

            # Check coefficient stability
            print("\n--- COEFFICIENT STABILITY ---")
            print(f"Rho range: {robust_df['Rho'].min():.4f} - {robust_df['Rho'].max():.4f}")
            print(f"BBM coef range: {robust_df['BBM_coef'].min():.4f} - {robust_df['BBM_coef'].max():.4f}")

            rho_cv = robust_df['Rho'].std() / robust_df['Rho'].mean() * 100
            bbm_cv = robust_df['BBM_coef'].std() / abs(robust_df['BBM_coef'].mean()) * 100

            print(f"Rho CV: {rho_cv:.2f}%")
            print(f"BBM coef CV: {bbm_cv:.2f}%")

            if rho_cv < 10 and bbm_cv < 10:
                print("✓ Coefficients robust across specifications")
            else:
                print("⚠ Some coefficient instability detected")

            robust_df.to_csv('sdm_results/fase6/6b_robustness_checks.csv', index=False)

            self.results['fase6b'] = robust_df
        else:
            print("✗ No robustness tests completed.")

        print("\n✓ FASE 6B completed.")
        return robustness_results

    # =========================================================================
    # FASE 7: POLICY SIMULATION
    # =========================================================================

    def fase7_policy_simulations(self):
        """FASE 7: Policy counterfactual simulations"""
        print("\n" + "="*80)
        print("FASE 7: POLICY SIMULATIONS")
        print("="*80)

        sdm = self.models.get('sdm_gm') or self.models.get('sdm_ml')

        if sdm is None or not hasattr(sdm, 'betas'):
            print("✗ Model not available.")
            return

        # Extract coefficients
        # Assuming order: [Constant, precip, temp, bbm, luas_panen, distance, W_precip, W_temp, W_bbm, W_luas_panen, W_distance]
        betas = sdm.betas.flatten()
        rho = sdm.rho if hasattr(sdm, 'rho') else 0

        X_vars = ['precipitation_mm', 'temperature_mean_c', 'bbm_price_idr',
                 'luas_panen_ha', 'avg_distance_km']

        print(f"\nModel coefficients:")
        for i, var in enumerate(X_vars):
            print(f"  {var}: β={betas[i+1]:.4f}, θ={betas[i+6]:.4f}")

        print(f"\nSpatial lag (ρ): {rho:.4f}")

        # Simulation scenarios
        simulations = []

        # Scenario 1: BBM shock (+15%)
        print("\n--- SCENARIO 1: BBM PRICE SHOCK (+15%) ---")
        bbm_shock = 1500  # Rp increase
        bbm_idx = X_vars.index('bbm_price_idr')

        direct_effect = betas[bbm_idx + 1] * bbm_shock
        spatial_effect = betas[bbm_idx + 6] * bbm_shock  # W_bbm coefficient

        # Total effect with multiplier (simplified)
        multiplier = 1 / (1 - rho)  # Approximate total multiplier
        total_effect = (direct_effect + spatial_effect) * multiplier

        print(f"BBM increase: +Rp {bbm_shock:.0f}/liter")
        print(f"Direct effect: +Rp {direct_effect:.2f}/kg")
        print(f"Spatial spillover: +Rp {spatial_effect:.2f}/kg")
        print(f"Total effect (with multiplier): +Rp {total_effect:.2f}/kg")

        simulations.append({
            'Scenario': 'BBM +15% (Rp 1500)',
            'Variable': 'BBM',
            'Shock_Size': bbm_shock,
            'Direct_Effect_Rp': direct_effect,
            'Spatial_Effect_Rp': spatial_effect,
            'Total_Effect_Rp': total_effect
        })

        # Scenario 2: Luas Panen increase (+10,000 ha)
        print("\n--- SCENARIO 2: LUAS PANEN INCREASE (+10,000 ha) ---")
        panen_shock = 10000  # ha
        panen_idx = X_vars.index('luas_panen_ha')

        direct_effect = betas[panen_idx + 1] * panen_shock
        spatial_effect = betas[panen_idx + 6] * panen_shock

        total_effect = (direct_effect + spatial_effect) * multiplier

        print(f"Luas panen increase: +{panen_shock:,.0f} ha")
        print(f"Direct effect: Rp {direct_effect:.2f}/kg")
        print(f"Spatial spillover: Rp {spatial_effect:.2f}/kg")
        print(f"Total effect: Rp {total_effect:.2f}/kg")

        simulations.append({
            'Scenario': 'Luas Panen +10k ha',
            'Variable': 'Luas Panen',
            'Shock_Size': panen_shock,
            'Direct_Effect_Rp': direct_effect,
            'Spatial_Effect_Rp': spatial_effect,
            'Total_Effect_Rp': total_effect
        })

        # Scenario 3: Extreme weather (+50mm rainfall)
        print("\n--- SCENARIO 3: EXTREME WEATHER (+50mm rainfall) ---")
        rain_shock = 50  # mm
        rain_idx = X_vars.index('precipitation_mm')

        direct_effect = betas[rain_idx + 1] * rain_shock
        spatial_effect = betas[rain_idx + 6] * rain_shock

        total_effect = (direct_effect + spatial_effect) * multiplier

        print(f"Rainfall increase: +{rain_shock} mm")
        print(f"Direct effect: Rp {direct_effect:.2f}/kg")
        print(f"Spatial spillover: Rp {spatial_effect:.2f}/kg")
        print(f"Total effect: Rp {total_effect:.2f}/kg")

        simulations.append({
            'Scenario': 'Extreme Rain +50mm',
            'Variable': 'Precipitation',
            'Shock_Size': rain_shock,
            'Direct_Effect_Rp': direct_effect,
            'Spatial_Effect_Rp': spatial_effect,
            'Total_Effect_Rp': total_effect
        })

        # Save simulations
        sim_df = pd.DataFrame(simulations)
        sim_df.to_csv('sdm_results/fase7/7_policy_simulations.csv', index=False)

        print("\n--- SIMULATION SUMMARY ---")
        print(sim_df)

        self.results['fase7'] = sim_df

        print("\n✓ FASE 7 completed.")
        return sim_df

    # =========================================================================
    # RUN ALL ADVANCED PHASES
    # =========================================================================

    def run_all_advanced(self):
        """Run all advanced phases (4-7)"""
        print("\n" + "="*80)
        print("RUNNING ADVANCED SDM ANALYSIS (PHASES 4-7)")
        print("="*80)

        # Load data
        self.load_preprocessed_data()
        self.reconstruct_spatial_weights()

        # Phase 4
        self.fase4_estimate_sdm(commodity='com_1', w_type='knn3')

        # Phase 5
        self.fase5a_model_fit_statistics()
        self.fase5b_effects_decomposition()
        self.fase5c_spatial_multiplier()

        # Phase 6
        self.fase6a_residual_diagnostics()
        self.fase6b_robustness_checks()

        # Phase 7
        self.fase7_policy_simulations()

        print("\n" + "="*80)
        print("ALL ADVANCED PHASES COMPLETED!")
        print("="*80)


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("SDM Advanced Estimation - Phases 4-7")

    # Initialize
    sdm_est = SDMEstimation(base_dir='.')

    try:
        # Run all advanced phases
        sdm_est.run_all_advanced()

        print("\n" + "="*80)
        print("SUCCESS! ALL 7 PHASES COMPLETED")
        print("="*80)
        print("\nResults saved in: sdm_results/")
        print("\nKey outputs:")
        print("  - Fase 4: SDM model estimation")
        print("  - Fase 5: Effects decomposition & spatial multipliers")
        print("  - Fase 6: Residual diagnostics & robustness checks")
        print("  - Fase 7: Policy simulations")

    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()
