import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
from shapely.geometry import Point
import os
import glob
import warnings

# Suppress warnings
warnings.filterwarnings('ignore')

# Configuration
OUTPUT_DIR = 'paper_analysis_output/spatial_maps'
os.makedirs(OUTPUT_DIR, exist_ok=True)
plt.style.use('seaborn-v0_8-whitegrid')

print("="*80)
print("STARTING SPATIAL VISUALIZATION (OVERLAY)")
print("="*80)

# 1. LOAD DATA
print("\n[1/3] Loading Data...")

# Load Prices
df_prices = pd.read_csv('cleaned_pihps_data/cleaned_combined.csv')
df_prices['date'] = pd.to_datetime(df_prices['date'])
df_prices['commodity_name'] = df_prices['commodity_name'].str.strip()

# Focus on Cabai (All types) to get max coverage
target_commodities = ['Cabai Merah Keriting', 'Cabai Rawit Merah', 'Cabai Merah Besar']
df_subset = df_prices[
    (df_prices['date'].dt.year >= 2023) & 
    (df_prices['commodity_name'].isin(target_commodities))
]

# Mapping Locations (Standardizing)
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
df_subset['mapped_loc'] = df_subset['location_name'].map(loc_map)

# Aggregate Price per Location
avg_price = df_subset.groupby('mapped_loc')['price'].mean().reset_index()

# Load Supply Chain Distances
list_of_files = glob.glob('supply_chain_spatial_fast/supply_chain_facilities_*.csv')
latest_file = max(list_of_files, key=os.path.getctime)
df_facilities = pd.read_csv(latest_file)

# Filter for Production
prod_facilities = df_facilities[df_facilities['facility_type'] == 'production']
avg_dist = prod_facilities.groupby('search_location')['distance_to_location_km'].mean().reset_index()

# Merge
data = pd.merge(avg_price, avg_dist, left_on='mapped_loc', right_on='search_location', how='outer')

# Coordinates Dictionary (Manual Geocoding for West Java & Jakarta)
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
    'Kab. Bekasi': (107.1720, -6.3639),
    'Cimahi': (107.5421, -6.8722),
    'Banjar': (108.5310, -7.3746),
    'Kab. Karawang': (107.3073, -6.3012),
    'Kab. Purwakarta': (107.4450, -6.5561),
    'Kab. Subang': (107.7625, -6.5716),
    'Kab. Indramayu': (108.3223, -6.3275),
    'Kab. Majalengka': (108.2262, -6.8365),
    'Kab. Sumedang': (107.9206, -6.8586),
    'Kab. Kuningan': (108.4800, -6.9760),
    'Kab. Ciamis': (108.3537, -7.3263),
    'Kab. Garut': (107.9006, -7.2020),
    'Kab. Pangandaran': (108.4763, -7.7056),
    'Kab. Cianjur': (107.1422, -6.8206)
}

data['coords'] = data['mapped_loc'].map(coords_dict)
data = data.dropna(subset=['coords'])
data['x'] = data['coords'].apply(lambda x: x[0])
data['y'] = data['coords'].apply(lambda x: x[1])

# Create GeoDataFrame
gdf = gpd.GeoDataFrame(data, geometry=gpd.points_from_xy(data.x, data.y))
gdf.set_crs(epsg=4326, inplace=True)

print(f"   Mapped {len(gdf)} locations successfully.")

# 2. VISUALIZATION
print("\n[2/3] Generating Maps...")

# Load Background Map
try:
    provinces = gpd.read_file('GeoJSON/Indonesia_provinces.geojson')
    background = provinces[provinces['NAME_1'].isin(['Jawa Barat', 'DKI Jakarta', 'Banten'])]
except:
    background = None
    print("   Warning: Could not load background map")

# MAP 1: Price Heatmap (Interpolated)
fig, ax = plt.subplots(figsize=(12, 10))
if background is not None:
    background.plot(ax=ax, color='#f0f0f0', edgecolor='white')

# Plot Price Bubbles
# Size = Price
# Color = Price
gdf.plot(column='price', ax=ax, legend=True, 
         cmap='Reds', markersize=gdf['price']/100, alpha=0.7, edgecolor='black',
         legend_kwds={'label': "Average Chili Price (Rp)"})

for x, y, label in zip(gdf.geometry.x, gdf.geometry.y, gdf.mapped_loc):
    ax.text(x, y+0.03, label, fontsize=8, ha='center')

plt.title('Map 1: Spatial Price Disparity of Chili in West Java & Jakarta', fontsize=14)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/Map1_Price_Disparity.png", dpi=300)
print("   Saved Map1_Price_Disparity.png")

# MAP 2: Supply Chain Gap (Distance)
fig, ax = plt.subplots(figsize=(12, 10))
if background is not None:
    background.plot(ax=ax, color='#f0f0f0', edgecolor='white')

# Plot Distance Bubbles
# Size = Distance
# Color = Distance (Darker = Further)
gdf.plot(column='distance_to_location_km', ax=ax, legend=True, 
         cmap='Blues', markersize=gdf['distance_to_location_km']*20, alpha=0.7, edgecolor='black',
         legend_kwds={'label': "Avg Distance to Production (km)"})

for x, y, label in zip(gdf.geometry.x, gdf.geometry.y, gdf.mapped_loc):
    ax.text(x, y+0.03, label, fontsize=8, ha='center')

plt.title('Map 2: Supply Chain Infrastructure Gaps\n(Larger/Darker Circles = Further from Production)', fontsize=14)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/Map2_Supply_Chain_Gaps.png", dpi=300)
print("   Saved Map2_Supply_Chain_Gaps.png")

# MAP 3: Bivariate Map (Price vs Distance) - The "Insight Map"
# High Price + High Distance = Structural Problem (Red)
# High Price + Low Distance = Inefficiency/Hoarding (Orange)
# Low Price + Low Distance = Efficient (Green)

# Simple categorization
median_price = gdf['price'].median()
median_dist = gdf['distance_to_location_km'].median()

def categorize(row):
    if pd.isna(row['price']) or pd.isna(row['distance_to_location_km']):
        return 'Unknown'
    if row['price'] > median_price and row['distance_to_location_km'] > median_dist:
        return 'High Price - Structural Gap (Priority)'
    elif row['price'] > median_price and row['distance_to_location_km'] <= median_dist:
        return 'High Price - Inefficiency'
    elif row['price'] <= median_price and row['distance_to_location_km'] > median_dist:
        return 'Low Price - Good Logistics'
    else:
        return 'Low Price - Efficient'

gdf['category'] = gdf.apply(categorize, axis=1)

fig, ax = plt.subplots(figsize=(12, 10))
if background is not None:
    background.plot(ax=ax, color='#f0f0f0', edgecolor='white')

# Define colors
category_colors = {
    'High Price - Structural Gap (Priority)': 'red',
    'High Price - Inefficiency': 'orange',
    'Low Price - Good Logistics': 'blue',
    'Low Price - Efficient': 'green',
    'Unknown': 'gray'
}

for cat, color in category_colors.items():
    subset = gdf[gdf['category'] == cat]
    if not subset.empty:
        subset.plot(ax=ax, color=color, markersize=300, edgecolor='black', label=cat)

plt.legend(title='Cluster Analysis')
plt.title('Map 3: Strategic Intervention Clusters (Policy Map)', fontsize=14)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/Map3_Policy_Clusters.png", dpi=300)
print("   Saved Map3_Policy_Clusters.png")

print("\n" + "="*80)
print("SPATIAL VISUALIZATION COMPLETED")
print("="*80)
