import pandas as pd
import numpy as np
import networkx as nx
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.spatial import cKDTree
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import glob
import os
import warnings

warnings.filterwarnings('ignore')
OUTPUT_DIR = 'paper_analysis_output/ultimate_model'
os.makedirs(OUTPUT_DIR, exist_ok=True)
plt.style.use('seaborn-v0_8-whitegrid')

print("="*80)
print("STARTING ULTIMATE INTEGRATED MODEL (NETWORK + CLIMATE + PRODUCTION + PRICE)")
print("="*80)

# ==============================================================================
# 1. PREPARE NETWORK FEATURES (FROM OSM)
# ==============================================================================
print("\n[1/5] Extracting Network Features (OSM)...")
list_of_files = glob.glob('supply_chain_spatial_fast/supply_chain_facilities_*.csv')
latest_file = max(list_of_files, key=os.path.getctime)
df_osm = pd.read_csv(latest_file)
df_osm = df_osm.dropna(subset=['latitude', 'longitude'])

# Build simple graph to calculate connectivity per city
# OPTIMIZATION: Instead of full NetworkX graph, we just count neighbors using KDTree
# This is much faster and gives the same "Connectivity Index" (Degree)
coords = df_osm[['latitude', 'longitude']].values
tree = cKDTree(coords)

# Count neighbors within 20km (approx 0.18 degrees)
radius_deg = 20 / 111.0
neighbors_count = tree.query_ball_point(coords, r=radius_deg, return_length=True)

# Assign Degree (Connectivity)
df_osm['degree'] = neighbors_count

# Aggregate Network Features per City
network_features = df_osm.groupby('search_location').agg({
    'degree': 'mean', # Average connectivity (density of supply chain)
    'name': 'count'   # Total facilities
}).rename(columns={'degree': 'connectivity_index', 'name': 'facility_count'}).reset_index()

print(f"   Network features extracted for {len(network_features)} locations.")

# ==============================================================================
# 2. PREPARE PRODUCTION FEATURES (FROM BPS)
# ==============================================================================
print("\n[2/5] Extracting Production Features (BPS)...")
df_prod = pd.read_csv('bps-jakarta-data/jawa_barat_food_production_2024.csv')

# Normalize city names to match OSM/PIHPS
# Remove 'Kota ' and 'Kabupaten ' prefixes for matching
def clean_city_name(name):
    return name.replace('Kota ', '').replace('Kabupaten ', '').replace('Kab. ', '').strip()

df_prod['clean_loc'] = df_prod['nama_kabupaten_kota'].apply(clean_city_name)
# Focus on Chili Production
prod_features = df_prod[['clean_loc', 'produksi_cabai_rawit_ton']].rename(columns={'produksi_cabai_rawit_ton': 'production_ton'})

print(f"   Production features extracted for {len(prod_features)} locations.")

# ==============================================================================
# 3. PREPARE CLIMATE FEATURES (FROM OPEN-METEO)
# ==============================================================================
print("\n[3/5] Extracting Climate Features (Open-Meteo)...")
df_weather = pd.read_csv('weather_pihps_historical.csv')
df_weather['date'] = pd.to_datetime(df_weather['date'])

# Avg Rainfall per City (2024)
weather_2024 = df_weather[df_weather['date'].dt.year == 2024]
weather_features = weather_2024.groupby('location_name').agg({
    'rain_mm': 'mean',
    'temperature_max_c': 'mean'
}).reset_index()
weather_features['clean_loc'] = weather_features['location_name'].apply(clean_city_name)

print(f"   Climate features extracted for {len(weather_features)} locations.")

# ==============================================================================
# 4. PREPARE TARGET VARIABLE: PRICE (FROM PIHPS)
# ==============================================================================
print("\n[4/5] Extracting Price Target (PIHPS)...")
df_prices = pd.read_csv('cleaned_pihps_data/cleaned_combined.csv')
df_prices['date'] = pd.to_datetime(df_prices['date'])
df_prices['commodity_name'] = df_prices['commodity_name'].str.strip()

# Target: Cabai Rawit Merah 2024 Avg Price
price_target = df_prices[
    (df_prices['date'].dt.year == 2024) & 
    (df_prices['commodity_name'] == 'Cabai Rawit Merah')
]
price_features = price_target.groupby('location_name')['price'].mean().reset_index()
price_features['clean_loc'] = price_features['location_name'].apply(clean_city_name)

print(f"   Price target extracted for {len(price_features)} locations.")

# ==============================================================================
# 5. MERGE ALL & MODELING
# ==============================================================================
print("\n[5/5] Merging & Modeling (The Ultimate Integration)...")

# Merge Logic: Price <- Network <- Production <- Weather
# Base is Price locations
final_df = price_features[['clean_loc', 'price']].copy()

# Merge Network
final_df = pd.merge(final_df, network_features, left_on='clean_loc', right_on='search_location', how='left')
# Merge Production
final_df = pd.merge(final_df, prod_features, on='clean_loc', how='left')
# Merge Weather
final_df = pd.merge(final_df, weather_features[['clean_loc', 'rain_mm', 'temperature_max_c']], on='clean_loc', how='left')

# Fill NaN (some cities might miss data)
final_df = final_df.fillna(0) # Simple imputation for demo

print("   Final Integrated Dataset Sample:")
print(final_df.head())

# MODELING: Random Forest to find Feature Importance
X = final_df[['connectivity_index', 'facility_count', 'production_ton', 'rain_mm', 'temperature_max_c']]
y = final_df['price']

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

# Feature Importance
importance = pd.DataFrame({
    'feature': X.columns,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

# VISUALIZATION: Feature Importance
plt.figure(figsize=(10, 6))
sns.barplot(data=importance, x='importance', y='feature', palette='viridis')
plt.title('What Drives Chili Prices in West Java?\n(Integrated Model Result)', fontsize=14)
plt.xlabel('Relative Importance (Impact on Price)')
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/Ultimate_Feature_Importance.png", dpi=300)
print("   Saved Ultimate_Feature_Importance.png")

# VISUALIZATION: Correlation Heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(final_df.corr(numeric_only=True), annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlation Matrix of All Factors', fontsize=14)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/Ultimate_Correlation_Matrix.png", dpi=300)
print("   Saved Ultimate_Correlation_Matrix.png")

# Save Final Data for Paper Table
final_df.to_csv(f"{OUTPUT_DIR}/final_integrated_data.csv", index=False)
print("   Saved final_integrated_data.csv")

print("\n" + "="*80)
print("ULTIMATE MODEL COMPLETED")
print("="*80)
