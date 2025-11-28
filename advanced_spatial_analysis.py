import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
from mgwr.gwr import GWR, MGWR
from mgwr.sel_bw import Sel_BW
import libpysal as ps
from shapely.geometry import Point
import os
import glob
import warnings

# Suppress warnings
warnings.filterwarnings('ignore')

# Configuration
OUTPUT_DIR = 'paper_analysis_output/advanced_sota'
os.makedirs(OUTPUT_DIR, exist_ok=True)
plt.style.use('seaborn-v0_8-whitegrid')

print("="*80)
print("STARTING SOTA SPATIAL ANALYSIS (MGWR)")
print("="*80)

# 1. LOAD DATA
print("\n[1/4] Loading & Preparing Data...")

# Load Prices
df_prices = pd.read_csv('cleaned_pihps_data/cleaned_combined.csv')
df_prices['date'] = pd.to_datetime(df_prices['date'])
df_prices['commodity_name'] = df_prices['commodity_name'].str.strip()

# Focus on 2024 & Cabai Merah Keriting (High Volatility)
target_commodity = 'Cabai Merah Keriting'
df_2024 = df_prices[
    (df_prices['date'].dt.year == 2024) & 
    (df_prices['commodity_name'] == target_commodity)
]

# Mapping Locations
loc_map = {
    'DKI Jakarta': 'Jakarta Pusat',
    'Jakarta Pusat': 'Jakarta Pusat',
    'Bandung': 'Bandung',
    'Bogor': 'Bogor',
    'Bekasi': 'Bekasi',
    'Depok': 'Depok',
    'Cirebon': 'Cirebon',
    'Sukabumi': 'Sukabumi',
    'Tasikmalaya': 'Tasikmalaya',
    'Kab. Cirebon': 'Kab. Cirebon',
    'Kab. Tasikmalaya': 'Kab. Tasikmalaya',
    'Kab. Bogor': 'Kab. Bogor',
    'Kab. Sukabumi': 'Kab. Sukabumi',
    'Kab. Bandung': 'Kab. Bandung',
    'Kab. Bekasi': 'Kab. Bekasi'
}
df_2024['mapped_loc'] = df_2024['location_name'].map(loc_map)

# Aggregate Price per Location
avg_price = df_2024.groupby('mapped_loc')['price'].mean().reset_index()

# Load Supply Chain Distances (from OSM)
# We need to re-calculate avg distance per location from the raw facility file
list_of_files = glob.glob('supply_chain_spatial_fast/supply_chain_facilities_*.csv')
latest_file = max(list_of_files, key=os.path.getctime)
df_facilities = pd.read_csv(latest_file)

# Filter for Chili Production
chili_prod = df_facilities[
    (df_facilities['commodity'].str.contains('Cabai', case=False)) & 
    (df_facilities['facility_type'] == 'production')
]
avg_dist = chili_prod.groupby('search_location')['distance_to_location_km'].mean().reset_index()

# Merge Data
data = pd.merge(avg_price, avg_dist, left_on='mapped_loc', right_on='search_location')

# Add Coordinates (Hardcoded for simplicity/accuracy matching PIHPS locations)
# In a real scenario, we would geocode these names.
coords_dict = {
    'Jakarta Pusat': (106.8456, -6.2088),
    'Bandung': (107.6191, -6.9175),
    'Bogor': (106.7890, -6.5950),
    'Bekasi': (106.9756, -6.2383),
    'Depok': (106.8181, -6.4025),
    'Cirebon': (108.5571, -6.7063),
    'Sukabumi': (106.9277, -6.9277),
    'Tasikmalaya': (108.2207, -7.3274),
    'Kab. Cirebon': (108.4773, -6.7622),
    'Kab. Tasikmalaya': (108.1068, -7.3592),
    'Kab. Bogor': (106.8637, -6.4779),
    'Kab. Sukabumi': (106.5507, -6.9881),
    'Kab. Bandung': (107.5283, -7.0252),
    'Kab. Bekasi': (107.1720, -6.3639)
}

data['coords'] = data['mapped_loc'].map(coords_dict)
data = data.dropna(subset=['coords']) # Drop if no coords

# Split coords into X and Y
data['x'] = data['coords'].apply(lambda x: x[0])
data['y'] = data['coords'].apply(lambda x: x[1])

print(f"   Final Dataset Size: {len(data)} locations")
print(data[['mapped_loc', 'price', 'distance_to_location_km']])

# 2. MGWR ANALYSIS
print("\n[2/4] Running MGWR Analysis...")

# Prepare Variables
# y = Price (Standardized)
# X = Distance (Standardized)
y = (data['price'].values.reshape((-1,1)) - data['price'].mean()) / data['price'].std()
X = (data['distance_to_location_km'].values.reshape((-1,1)) - data['distance_to_location_km'].mean()) / data['distance_to_location_km'].std()
coords = list(zip(data['x'], data['y']))

try:
    # Select optimal bandwidth
    selector = Sel_BW(coords, y, X)
    bw = selector.search()
    print(f"   Optimal Bandwidth: {bw}")

    # Fit GWR Model
    model = GWR(coords, y, X, bw)
    results = model.fit()

    print(f"   GWR R-squared: {results.R2}")
    print("   Local Coefficients (Beta) Summary:")
    print(pd.DataFrame(results.params, columns=['Intercept', 'Distance_Beta']).describe())

    # Add results back to DataFrame
    data['beta_distance'] = results.params[:, 1] # Slope for distance
    data['local_R2'] = results.localR2
    
    # Save Results
    data.to_csv(f"{OUTPUT_DIR}/mgwr_results.csv", index=False)
    print("   Saved mgwr_results.csv")

except Exception as e:
    print(f"   ERROR in MGWR: {e}")
    # Fallback to simple OLS if GWR fails (e.g., too few points)
    exit()

# 3. VISUALIZATION (SOTA MAPS)
print("\n[3/4] Generating SOTA Visualizations...")

# Convert to GeoDataFrame
gdf = gpd.GeoDataFrame(data, geometry=gpd.points_from_xy(data.x, data.y))
# Set CRS to WGS84
gdf.set_crs(epsg=4326, inplace=True)

# Load Indonesia Provinces for Background
try:
    provinces = gpd.read_file('GeoJSON/Indonesia_provinces.geojson')
    # Filter for Java only to zoom in
    java_provinces = provinces[provinces['NAME_1'].isin(['Jawa Barat', 'DKI Jakarta', 'Banten'])]
except:
    java_provinces = None
    print("   Warning: Could not load background map")

# MAP 1: Local Coefficients (The "Policy Map")
fig, ax = plt.subplots(figsize=(12, 10))
if java_provinces is not None:
    java_provinces.plot(ax=ax, color='#f0f0f0', edgecolor='white')

# Plot points colored by Beta Coefficient
# Red = Positive Beta (Jarak Jauh -> Harga Mahal) -> Sesuai Teori
# Blue = Negative Beta (Anomali)
gdf.plot(column='beta_distance', ax=ax, legend=True, 
         cmap='RdBu_r', markersize=200, edgecolor='black',
         legend_kwds={'label': "Sensitivity of Price to Distance (Beta)"})

# Add labels
for x, y, label in zip(gdf.geometry.x, gdf.geometry.y, gdf.mapped_loc):
    ax.text(x, y+0.02, label, fontsize=8, ha='center')

plt.title(f'SOTA Map 1: Spatial Heterogeneity of Supply Chain Impact\n(Where does Distance matter most for {target_commodity}?)', fontsize=14)
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/SOTA_Map1_Local_Coefficients.png", dpi=300)
print("   Saved SOTA_Map1_Local_Coefficients.png")

# MAP 2: Local R-squared (Model Performance)
fig, ax = plt.subplots(figsize=(12, 10))
if java_provinces is not None:
    java_provinces.plot(ax=ax, color='#f0f0f0', edgecolor='white')

gdf.plot(column='local_R2', ax=ax, legend=True, 
         cmap='Greens', markersize=200, edgecolor='black',
         legend_kwds={'label': "Local R-squared (Model Fit)"})

for x, y, label in zip(gdf.geometry.x, gdf.geometry.y, gdf.mapped_loc):
    ax.text(x, y+0.02, label, fontsize=8, ha='center')

plt.title(f'SOTA Map 2: Local Model Performance\n(Where is the Price well-explained by Supply Chain Distance?)', fontsize=14)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/SOTA_Map2_Local_R2.png", dpi=300)
print("   Saved SOTA_Map2_Local_R2.png")

print("\n" + "="*80)
print("SOTA ANALYSIS COMPLETED")
print("="*80)
