"""
STANDALONE SCRIPT: Run FIXED SDM Analysis
All-in-one script that doesn't require running Fase 1 separately

FIXES:
1. TRUE PANEL STRUCTURE (monthly panel, not time-averaged)
2. FACILITY NETWORK WEIGHTS (economic weights from supply chain)
3. TEMPORAL LAG STRUCTURE (for early warning system)
"""

import os
import warnings
import numpy as np
import pandas as pd
from scipy.spatial.distance import pdist, squareform
from scipy import stats
from scipy.linalg import inv
import libpysal
from libpysal.weights import W, KNN
import spreg
from spreg import GM_Lag, ML_Lag

warnings.filterwarnings('ignore')

# Create directories
os.makedirs('sdm_results_fixed/fase1', exist_ok=True)
os.makedirs('sdm_results_fixed/fase2', exist_ok=True)
os.makedirs('sdm_results_fixed/fase4', exist_ok=True)

print("="*80)
print("FIXED SDM ANALYSIS - Panel + Facility Weights + Temporal Lags")
print("="*80)

# ============================================================================
# STEP 1: LOAD AND MERGE DATA
# ============================================================================

print("\n[1/5] Loading and merging datasets...")

# Load PIHPS
df_pihps = pd.read_csv('cleaned_pihps_data/cleaned_combined.csv', parse_dates=['date'])
print(f"  PIHPS data: {df_pihps.shape}")

# Filter rice commodities only
rice_commodities = ['com_1', 'com_2', 'com_3', 'com_4', 'com_5', 'com_6']
df = df_pihps[df_pihps['commodity_id'].isin(rice_commodities)].copy()
print(f"  Rice commodities only: {df.shape}")

# Merge weather
df_weather = pd.read_csv('weather_pihps_historical.csv', parse_dates=['date'])
df = df.merge(
    df_weather[['date', 'location_name', 'temperature_mean_c', 'precipitation_mm']],
    on=['date', 'location_name'],
    how='left'
)
print(f"  After weather merge: {df.shape}")

# Merge BBM
df_bbm = pd.read_csv('indonesia_gasoline_prices_5y.csv', parse_dates=['Date'])
df_bbm['year_month'] = df_bbm['Date'].dt.to_period('M')
df['year_month'] = pd.to_datetime(df['date']).dt.to_period('M')
df = df.merge(
    df_bbm[['year_month', 'Price_IDR_per_Liter']].rename(columns={'Price_IDR_per_Liter': 'bbm_price_idr'}),
    on='year_month',
    how='left'
)
df = df.sort_values(['location_name', 'commodity_id', 'date'])
df['bbm_price_idr'] = df.groupby(['location_name', 'commodity_id'])['bbm_price_idr'].ffill()
print(f"  After BBM merge: {df.shape}")

# Merge Luas Panen
df_panen = pd.read_csv('bps-jakarta-data/jawa_barat_rice_production_2020_2024.csv')
df['year'] = pd.to_datetime(df['date']).dt.year

location_mapping = {
    'Bandung': 'Bandung', 'Bekasi': 'Bekasi', 'Bogor': 'Bogor',
    'Cianjur': 'Cianjur', 'Cirebon': 'Cirebon', 'Garut': 'Garut',
    'Indramayu': 'Indramayu', 'Karawang': 'Karawang', 'Kuningan': 'Kuningan',
    'Majalengka': 'Majalengka', 'Purwakarta': 'Purwakarta', 'Subang': 'Subang',
    'Sukabumi': 'Sukabumi', 'Sumedang': 'Sumedang', 'Tasikmalaya': 'Tasikmalaya',
    'DKI Jakarta': None
}
df['kabupaten_kota'] = df['location_name'].map(location_mapping)
df = df.merge(
    df_panen[['year', 'kabupaten_kota', 'luas_panen_ha']],
    on=['year', 'kabupaten_kota'],
    how='left'
)
df['luas_panen_ha'].fillna(0, inplace=True)
print(f"  After luas panen merge: {df.shape}")

# Add distance
df_facility = pd.read_csv('supply_chain_spatial_fast/supply_chain_facilities_20251128_141527.csv')
avg_distance = df_facility.groupby('search_location')['distance_to_location_km'].mean()
df['avg_distance_km'] = df['location_name'].map(avg_distance)
df['avg_distance_km'].fillna(avg_distance.median(), inplace=True)

# Clean
df_clean = df.dropna(subset=['price', 'precipitation_mm', 'bbm_price_idr'])
print(f"  Final cleaned: {df_clean.shape}")

# ============================================================================
# STEP 2: BUILD FACILITY NETWORK WEIGHTS (FIX #2)
# ============================================================================

print("\n[2/5] Constructing facility network weights...")

coords_df = df_weather[['location_name', 'latitude', 'longitude']].drop_duplicates()
locations = sorted(coords_df['location_name'].unique())
n_locations = len(locations)
coords = coords_df.set_index('location_name').loc[locations][['longitude', 'latitude']].values

print(f"  Locations: {n_locations}")

# Count distribution facilities per location
facility_counts = df_facility[df_facility['facility_type'] == 'distribution'].groupby('search_location').size()

# Distance matrix
dist_matrix = squareform(pdist(coords, metric='euclidean')) * 111  # to km

# Economic weight matrix: W[i,j] = sqrt(fac_i * fac_j) / distance_ij
facility_vector = np.array([facility_counts.get(loc, 1) for loc in locations])

w_econ_array = np.zeros((n_locations, n_locations))
for i in range(n_locations):
    for j in range(n_locations):
        if i != j:
            fac_interaction = np.sqrt(facility_vector[i] * facility_vector[j])
            w_econ_array[i, j] = fac_interaction / (dist_matrix[i, j] + 0.1)

# Row-standardize
w_econ_array = w_econ_array / w_econ_array.sum(axis=1, keepdims=True)

# Geographic weights (KNN k=3)
w_knn = KNN.from_array(coords, k=3)
w_knn.transform = 'r'
w_knn_array = w_knn.full()[0]

# Combined weights (alpha=0.5)
alpha = 0.5
w_combined_array = alpha * w_knn_array + (1 - alpha) * w_econ_array
w_combined_array = w_combined_array / w_combined_array.sum(axis=1, keepdims=True)

# Create W object
neighbors = {}
weights = {}
for i in range(n_locations):
    neighbors[i] = [j for j in range(n_locations) if i != j]
    weights[i] = w_combined_array[i, neighbors[i]].tolist()

w_combined = W(neighbors, weights)
print(f"  Combined weights: {w_combined.n} units, {w_combined.s0:.2f} total weights")

# Save
pd.DataFrame(w_econ_array, index=locations, columns=locations).to_csv(
    'sdm_results_fixed/fase2/economic_weights_matrix.csv'
)

# ============================================================================
# STEP 3: CREATE PANEL DATA WITH LAGS (FIX #1 & #3)
# ============================================================================

print("\n[3/5] Creating panel data with temporal lags...")

commodity = 'com_1'  # Focus on Beras Kualitas Bawah I
df_commodity = df_clean[df_clean['commodity_id'] == commodity].copy()

# Aggregate to monthly panel
df_commodity['year_month'] = pd.to_datetime(df_commodity['date']).dt.to_period('M')
df_panel = df_commodity.groupby(['location_name', 'year_month']).agg({
    'price': 'mean',
    'precipitation_mm': 'sum',
    'temperature_mean_c': 'mean',
    'bbm_price_idr': 'mean',
    'luas_panen_ha': 'first',
    'avg_distance_km': 'first'
}).reset_index()

df_panel['date'] = df_panel['year_month'].dt.to_timestamp()
df_panel = df_panel.sort_values(['location_name', 'date'])

print(f"  Panel: {df_panel['location_name'].nunique()} locations x {df_panel['year_month'].nunique()} months = {len(df_panel)} obs")

# Create lagged variables
df_panel['price_lag1'] = df_panel.groupby('location_name')['price'].shift(1)
df_panel['bbm_lag1'] = df_panel.groupby('location_name')['bbm_price_idr'].shift(1)
df_panel['rain_lag1'] = df_panel.groupby('location_name')['precipitation_mm'].shift(1)
df_panel['rain_lag2'] = df_panel.groupby('location_name')['precipitation_mm'].shift(2)
df_panel['rain_lag3'] = df_panel.groupby('location_name')['precipitation_mm'].shift(3)
df_panel['temp_lag1'] = df_panel.groupby('location_name')['temperature_mean_c'].shift(1)

# Drop missing lags
df_panel_clean = df_panel.dropna(subset=['price_lag1', 'bbm_lag1', 'rain_lag3'])
print(f"  After lags: {len(df_panel_clean)} obs")

# Time fixed effects (month dummies)
df_panel_clean['month'] = df_panel_clean['date'].dt.month
month_dummies = pd.get_dummies(df_panel_clean['month'], prefix='month', drop_first=True, dtype=np.int32)
df_panel_clean = pd.concat([df_panel_clean, month_dummies], axis=1)

# Save
df_panel_clean.to_csv('sdm_results_fixed/fase1/panel_data_with_lags.csv', index=False)

# ============================================================================
# STEP 4: ESTIMATE PANEL SDM (FIX #1, #2, #3 COMBINED)
# ============================================================================

print("\n[4/5] Estimating Panel Spatial Durbin Model...")

# Filter to locations in weights matrix
df_panel_clean = df_panel_clean[df_panel_clean['location_name'].isin(locations)]

# Sort by location index
location_to_idx = {loc: i for i, loc in enumerate(locations)}
df_panel_clean['loc_idx'] = df_panel_clean['location_name'].map(location_to_idx)
df_panel_clean = df_panel_clean.sort_values(['loc_idx', 'date'])

# Prepare y and X
y = df_panel_clean['price'].values.reshape(-1, 1)

X_vars = [
    'price_lag1',
    'precipitation_mm', 'rain_lag1', 'rain_lag2', 'rain_lag3',
    'temperature_mean_c', 'temp_lag1',
    'bbm_price_idr', 'bbm_lag1',
    'luas_panen_ha',
    'avg_distance_km'
]

month_cols = [col for col in df_panel_clean.columns if col.startswith('month_')]
X_vars_all = X_vars + month_cols
X = df_panel_clean[X_vars_all].values

print(f"  y: {y.shape}, X: {X.shape}")
print(f"  Variables: {len(X_vars_all)} ({len(X_vars)} + {len(month_cols)} month dummies)")

# CRITICAL FIX: For panel data, W must be expanded using Kronecker product
# W_panel = I_T ⊗ W_N where I_T is TxT identity matrix
n_time_periods = df_panel_clean.groupby('loc_idx').size().iloc[0]
print(f"  Time periods: {n_time_periods}")
print(f"  Expanding W from {w_combined.n}x{w_combined.n} to {y.shape[0]}x{y.shape[0]}")

# Create panel W using Kronecker product
from scipy.linalg import kron
I_T = np.eye(n_time_periods)
W_N = w_combined.full()[0]
W_panel_array = kron(I_T, W_N)

# Create W object for panel
neighbors_panel = {}
weights_panel = {}
n_panel = W_panel_array.shape[0]

for i in range(n_panel):
    neighbors_panel[i] = [j for j in range(n_panel) if W_panel_array[i, j] > 0]
    weights_panel[i] = W_panel_array[i, neighbors_panel[i]].tolist()

w_panel = W(neighbors_panel, weights_panel)
print(f"  Panel W created: {w_panel.n} units, {w_panel.s0:.2f} total weights")

# Estimate SDM with panel W
print("\n  Estimating with GM_Lag...")

try:
    sdm = GM_Lag(
        y, X, w=w_panel,
        slx_lags=1,
        name_y='price',
        name_x=X_vars_all,
        name_w='panel_combined',
        name_ds='Panel Rice Price - FIXED',
        spat_impacts=['simple', 'full']
    )
    print("  [OK] GM estimation successful")

except Exception as e:
    print(f"  [WARN] GM failed: {str(e)[:100]}")
    print("  Trying ML_Lag...")

    sdm = ML_Lag(
        y, X, w=w_panel,
        slx_lags=1,
        name_y='price',
        name_x=X_vars_all,
        name_w='panel_combined',
        name_ds='Panel Rice Price - FIXED',
        spat_impacts=['simple', 'full'],
        spat_diag=True
    )
    print("  [OK] ML estimation successful")

# Save summary
with open('sdm_results_fixed/fase4/panel_sdm_summary.txt', 'w', encoding='utf-8') as f:
    f.write(str(sdm.summary))

# Extract coefficients
coef_names = ['Constant'] + X_vars_all + [f'W_{x}' for x in X_vars_all] + ['rho']
n_coefs = len(sdm.betas)

coef_df = pd.DataFrame({
    'Variable': coef_names[:n_coefs],
    'Coefficient': sdm.betas.flatten()
})

if hasattr(sdm, 'vm'):
    coef_df['Std_Error'] = np.sqrt(np.diag(sdm.vm))

if hasattr(sdm, 'z_stat'):
    z_stat_array = np.array(sdm.z_stat).flatten() if isinstance(sdm.z_stat, list) else sdm.z_stat.flatten()
    # Ensure length matches
    if len(z_stat_array) >= len(coef_df):
        coef_df['Z_stat'] = z_stat_array[:len(coef_df)]
        coef_df['P_value'] = [2 * (1 - stats.norm.cdf(abs(z))) for z in z_stat_array[:len(coef_df)]]
        coef_df['Sig'] = coef_df['P_value'].apply(
            lambda p: '***' if p < 0.001 else ('**' if p < 0.01 else ('*' if p < 0.05 else ''))
        )
    else:
        print(f"  [WARN] z_stat length mismatch: {len(z_stat_array)} vs {len(coef_df)}")

coef_df.to_csv('sdm_results_fixed/fase4/panel_coefficients.csv', index=False)

print("\n  Model fit statistics:")
if hasattr(sdm, 'pr2'):
    print(f"    Pseudo R2: {sdm.pr2:.4f}")
if hasattr(sdm, 'logll'):
    print(f"    Log-likelihood: {sdm.logll:.2f}")
if hasattr(sdm, 'aic'):
    print(f"    AIC: {sdm.aic:.2f}")

# ============================================================================
# STEP 5: INTERPRET LAG STRUCTURE (EARLY WARNING)
# ============================================================================

print("\n[5/5] Interpreting temporal lag structure...")

print("\n  RAINFALL LAG EFFECTS (Early Warning Window):")
rain_vars = ['precipitation_mm', 'rain_lag1', 'rain_lag2', 'rain_lag3']
for var in rain_vars:
    row = coef_df[coef_df['Variable'] == var]
    if len(row) > 0:
        coef = row['Coefficient'].values[0]
        sig = row.get('Sig', pd.Series([''])).values[0]

        if 'lag1' in var:
            window = "1 month (30 days)"
        elif 'lag2' in var:
            window = "2 months (60 days)"
        elif 'lag3' in var:
            window = "3 months (90 days)"
        else:
            window = "Current month"

        print(f"    {var:20s} ({window:20s}): {coef:+.4f}{sig}")

print("\n  BBM LAG EFFECT (Transport Cost Delay):")
for var in ['bbm_price_idr', 'bbm_lag1']:
    row = coef_df[coef_df['Variable'] == var]
    if len(row) > 0:
        coef = row['Coefficient'].values[0]
        sig = row.get('Sig', pd.Series([''])).values[0]
        window = "Current month" if 'lag' not in var else "1 month delay"
        print(f"    {var:20s} ({window:20s}): {coef:+.4f}{sig}")

print("\n  AUTOREGRESSIVE TERM (Price Persistence):")
row = coef_df[coef_df['Variable'] == 'price_lag1']
if len(row) > 0:
    coef = row['Coefficient'].values[0]
    sig = row.get('Sig', pd.Series([''])).values[0]
    print(f"    price_lag1          (1 month lag)       : {coef:+.4f}{sig}")
    if abs(coef) > 0.5:
        print("    --> High persistence: price shocks last multiple months")
    else:
        print("    --> Moderate persistence: prices adjust relatively quickly")

# Save interpretation
with open('sdm_results_fixed/fase4/early_warning_interpretation.txt', 'w', encoding='utf-8') as f:
    f.write("EARLY WARNING SYSTEM - TEMPORAL LAG INTERPRETATION\n")
    f.write("="*60 + "\n\n")
    f.write("Rainfall Lag Effects:\n")
    for var in rain_vars:
        row = coef_df[coef_df['Variable'] == var]
        if len(row) > 0:
            f.write(f"{row.to_string(index=False)}\n")
    f.write("\nBBM Lag Effects:\n")
    for var in ['bbm_price_idr', 'bbm_lag1']:
        row = coef_df[coef_df['Variable'] == var]
        if len(row) > 0:
            f.write(f"{row.to_string(index=False)}\n")

print("\n" + "="*80)
print("FIXED SDM ANALYSIS COMPLETED!")
print("="*80)
print("\nKey Improvements:")
print("  [OK] True panel structure (monthly, not time-averaged)")
print("  [OK] Facility network weights (economic + geographic combined)")
print("  [OK] Temporal lags (rainfall lag1-3, BBM lag1, price AR1)")
print("\nResults saved in: sdm_results_fixed/")
print("  - fase1/panel_data_with_lags.csv")
print("  - fase2/economic_weights_matrix.csv")
print("  - fase4/panel_sdm_summary.txt")
print("  - fase4/panel_coefficients.csv")
print("  - fase4/early_warning_interpretation.txt")
