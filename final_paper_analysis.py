import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import json
import glob
from datetime import datetime
import statsmodels.api as sm
from scipy import stats
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

# ============================================================================
# CONFIGURATION & SETUP
# ============================================================================
OUTPUT_DIR = 'paper_analysis_output'
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Plotting Style for Academic Paper
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_context("paper", font_scale=1.4)
COLORS = sns.color_palette("viridis", 10)

# File Paths
PATH_PRICES = 'cleaned_pihps_data/cleaned_combined.csv'
PATH_SUPPLY_CHAIN = 'supply_chain_spatial_fast' # Directory
PATH_WEATHER = 'weather_pihps_historical.csv'
PATH_PRODUCTION = 'bps-jakarta-data/jawa_barat_food_production_2024.csv'
PATH_GEOJSON = 'GeoJSON/Indonesia_cities.geojson' # Using cities for simplicity in this script

print("="*80)
print("STARTING FINAL PAPER ANALYSIS")
print("="*80)

# ============================================================================
# 1. DATA LOADING & PREPROCESSING
# ============================================================================
print("\n[1/6] Loading Data...")

# A. Load Prices (PIHPS)
print("   - Loading Prices...")
df_prices = pd.read_csv(PATH_PRICES)
df_prices['date'] = pd.to_datetime(df_prices['date'])
# Filter for Jakarta & West Java cities only (Study Area)
study_cities = ['DKI Jakarta', 'Jakarta Pusat', 'Kota Bandung', 'Kota Bogor', 'Kota Bekasi', 
                'Kota Depok', 'Kota Sukabumi', 'Kota Tasikmalaya', 'Kota Cirebon',
                'Kab. Bogor', 'Kab. Sukabumi', 'Kab. Bandung', 'Kab. Bekasi', 'Kab. Cirebon']
# Note: PIHPS names might differ slightly, we'll standardize later if needed.
# For now, let's take 2024 data for cross-sectional analysis
df_prices_2024 = df_prices[df_prices['date'].dt.year == 2024]

# B. Load Supply Chain (OSM)
print("   - Loading Supply Chain Facilities...")
# Find the latest facility file
list_of_files = glob.glob(f'{PATH_SUPPLY_CHAIN}/supply_chain_facilities_*.csv')
latest_file = max(list_of_files, key=os.path.getctime)
df_facilities = pd.read_csv(latest_file)
print(f"     Loaded {len(df_facilities)} facilities from {latest_file}")

# C. Load Weather
print("   - Loading Weather...")
df_weather = pd.read_csv(PATH_WEATHER)
df_weather['date'] = pd.to_datetime(df_weather['date'])

# D. Load Production (BPS)
print("   - Loading Production Data...")
df_production = pd.read_csv(PATH_PRODUCTION)

# ============================================================================
# 2. SPATIAL ANALYSIS (INFRASTRUCTURE MAPPING)
# ============================================================================
print("\n[2/6] Generating Spatial Visualizations...")

# FIGURE 1: Facility Density by Location (Bar Chart Proxy for Heatmap if no GeoPandas)
# Aggregating facilities by location and type
facility_stats = df_facilities.groupby(['search_location', 'facility_type']).size().unstack(fill_value=0)
facility_stats['Total'] = facility_stats.sum(axis=1)
facility_stats = facility_stats.sort_values('Total', ascending=False)

plt.figure(figsize=(12, 8))
# Plotting
facility_stats[['retail', 'distribution', 'production']].plot(kind='bar', stacked=True, colormap='viridis', figsize=(12, 8))
plt.title('Figure 1: Supply Chain Infrastructure Density by Region', fontsize=16, pad=20)
plt.xlabel('Region', fontsize=12)
plt.ylabel('Number of Facilities', fontsize=12)
plt.legend(title='Facility Type')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/Fig1_Infrastructure_Density.png", dpi=300)
plt.close()
print("   - Saved Fig1_Infrastructure_Density.png")

# FIGURE 2: Access Disparity (Avg Distance to Production)
# We need to calculate avg distance to production for each location
# Filter for production facilities
prod_facilities = df_facilities[df_facilities['facility_type'] == 'production']
if not prod_facilities.empty:
    avg_dist_prod = prod_facilities.groupby('search_location')['distance_to_location_km'].mean().sort_values()
    
    plt.figure(figsize=(12, 6))
    sns.barplot(x=avg_dist_prod.index, y=avg_dist_prod.values, palette="rocket")
    plt.title('Figure 2: Disparity in Access to Production Centers', fontsize=16, pad=20)
    plt.ylabel('Avg Distance to Nearest Production (km)', fontsize=12)
    plt.xlabel('Region', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/Fig2_Access_Disparity.png", dpi=300)
    plt.close()
    print("   - Saved Fig2_Access_Disparity.png")
else:
    print("   ! No production facilities found to plot Fig 2")

# TABLE 1: Infrastructure Statistics
table1 = facility_stats.copy()
if not prod_facilities.empty:
    table1['Avg_Dist_Production_km'] = prod_facilities.groupby('search_location')['distance_to_location_km'].mean()
table1.to_csv(f"{OUTPUT_DIR}/Table1_Infrastructure_Stats.csv")
print("   - Saved Table1_Infrastructure_Stats.csv")


# ============================================================================
# 3. SPATIAL REGRESSION ANALYSIS (PRICE DETERMINANTS)
# ============================================================================
print("\n[3/6] Running Spatial Regression Analysis...")

# Prepare Data for Regression
# We want to see if Distance to Production affects Price
# 1. Get Avg Price per Location for 2024 (e.g., for 'Beras')
target_commodity = 'Beras'
price_subset = df_prices_2024[df_prices_2024['commodity_name'].str.contains(target_commodity, case=False)]

# Map PIHPS location names to OSM search_location names
# This is a simple mapping, might need refinement based on exact strings
loc_map = {
    'DKI Jakarta': 'Jakarta Pusat', # Proxy
    'Jakarta Pusat': 'Jakarta Pusat',
    'Kota Bandung': 'Bandung',
    'Kota Bogor': 'Bogor',
    'Kota Bekasi': 'Bekasi',
    'Kota Depok': 'Depok',
    'Kota Cirebon': 'Cirebon',
    'Kota Sukabumi': 'Sukabumi',
    'Kota Tasikmalaya': 'Tasikmalaya',
    'Kab. Cirebon': 'Kab. Cirebon',
    'Kab. Tasikmalaya': 'Kab. Tasikmalaya'
}

price_subset['mapped_loc'] = price_subset['location_name'].map(loc_map)
avg_price_loc = price_subset.groupby('mapped_loc')['price'].mean().reset_index()

# 2. Get Avg Distance to Production per Location (from OSM)
# Filter OSM for Rice related production
rice_prod = df_facilities[
    (df_facilities['commodity'] == 'Beras') & 
    (df_facilities['facility_type'] == 'production')
]
avg_dist_loc = rice_prod.groupby('search_location')['distance_to_location_km'].mean().reset_index()

# 3. Merge
reg_df = pd.merge(avg_price_loc, avg_dist_loc, left_on='mapped_loc', right_on='search_location')

if len(reg_df) > 2:
    # FIGURE 3: Scatter Plot (Distance vs Price)
    plt.figure(figsize=(10, 6))
    sns.regplot(data=reg_df, x='distance_to_location_km', y='price', color='teal', marker='o', scatter_kws={'s':100})
    
    # Label points
    for i, point in reg_df.iterrows():
        plt.text(point['distance_to_location_km']+0.2, point['price'], point['mapped_loc'], fontsize=9)

    plt.title(f'Figure 3: Impact of Supply Chain Distance on {target_commodity} Price', fontsize=16, pad=20)
    plt.xlabel('Avg Distance to Production Facilities (km)', fontsize=12)
    plt.ylabel('Average Price (Rp/kg)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/Fig3_Distance_Price_Correlation.png", dpi=300)
    plt.close()
    print("   - Saved Fig3_Distance_Price_Correlation.png")

    # TABLE 2: Regression Results
    X = sm.add_constant(reg_df['distance_to_location_km'])
    y = reg_df['price']
    model = sm.OLS(y, X).fit()
    
    with open(f"{OUTPUT_DIR}/Table2_Regression_Results.txt", "w") as f:
        f.write(model.summary().as_text())
    print("   - Saved Table2_Regression_Results.txt")
else:
    print("   ! Not enough data points for regression (need > 2 matching locations)")


# ============================================================================
# 4. CLIMATE IMPACT ANALYSIS
# ============================================================================
print("\n[4/6] Analyzing Climate Impact...")

# Focus on 'Cabai' (Chili) which is sensitive to weather
commodity_weather = 'Cabai Merah Keriting'
loc_weather = 'Kota Bandung' # Example location with good data

# Filter Price
price_ts = df_prices[
    (df_prices['location_name'] == loc_weather) & 
    (df_prices['commodity_name'] == commodity_weather)
].sort_values('date')

# Filter Weather (using 'Bandung' as proxy for Kota Bandung)
weather_ts = df_weather[df_weather['location_name'] == 'Bandung'].sort_values('date')

# Merge on Date
climate_df = pd.merge(price_ts, weather_ts, on='date', how='inner')

if not climate_df.empty:
    # Resample to Weekly to reduce noise
    climate_weekly = climate_df.set_index('date').resample('W').agg({
        'price': 'mean',
        'rain_mm': 'sum'
    }).reset_index()

    # FIGURE 5: Dual Axis Line Chart
    fig, ax1 = plt.subplots(figsize=(14, 7))

    color = 'tab:red'
    ax1.set_xlabel('Date', fontsize=12)
    ax1.set_ylabel(f'{commodity_weather} Price (Rp)', color=color, fontsize=12)
    ax1.plot(climate_weekly['date'], climate_weekly['price'], color=color, linewidth=2, label='Price')
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    color = 'tab:blue'
    ax2.set_ylabel('Weekly Rainfall (mm)', color=color, fontsize=12)  # we already handled the x-label with ax1
    ax2.bar(climate_weekly['date'], climate_weekly['rain_mm'], color=color, alpha=0.3, width=5, label='Rainfall')
    ax2.tick_params(axis='y', labelcolor=color)

    plt.title(f'Figure 5: Impact of Rainfall on {commodity_weather} Prices in {loc_weather}', fontsize=16, pad=20)
    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.savefig(f"{OUTPUT_DIR}/Fig5_Climate_Impact.png", dpi=300)
    plt.close()
    print("   - Saved Fig5_Climate_Impact.png")
else:
    print("   ! No matching data for Climate Analysis")


# ============================================================================
# 5. POLICY SIMULATION (SCENARIO)
# ============================================================================
print("\n[5/6] Running Policy Simulation...")

# Scenario: Building a Cold Storage reduces 'distance premium' by 30%
# Based on our regression beta (slope)
if 'model' in locals():
    slope = model.params['distance_to_location_km']
    current_avg_dist = reg_df['distance_to_location_km'].mean()
    current_avg_price = reg_df['price'].mean()
    
    # Simulation
    reduction_pct = 0.30 # 30% reduction in effective distance
    new_dist = current_avg_dist * (1 - reduction_pct)
    predicted_price_drop = slope * (current_avg_dist - new_dist)
    
    # FIGURE 6: Scenario Chart
    scenarios = ['Current State', 'With New Cold Storage']
    prices = [current_avg_price, current_avg_price - predicted_price_drop]
    
    plt.figure(figsize=(8, 6))
    bars = plt.bar(scenarios, prices, color=['#e74c3c', '#2ecc71'], width=0.5)
    
    # Add labels
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                 f'Rp {int(height):,}',
                 ha='center', va='bottom', fontsize=12, fontweight='bold')
        
    plt.title(f'Figure 6: Policy Simulation - Impact of Infrastructure Optimization\n(Estimated Price Reduction: Rp {int(predicted_price_drop):,}/kg)', fontsize=14, pad=20)
    plt.ylabel('Average Price (Rp/kg)')
    plt.ylim(0, max(prices)*1.2)
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/Fig6_Policy_Simulation.png", dpi=300)
    plt.close()
    print("   - Saved Fig6_Policy_Simulation.png")
else:
    print("   ! Skipping simulation (no regression model)")

# ============================================================================
# 6. PRODUCTION MAP (SUPPLY SIDE)
# ============================================================================
print("\n[6/6] Visualizing Supply Side (Production)...")

# Top 5 Producers of Chili (Cabai Rawit)
top_producers = df_production.sort_values('produksi_cabai_rawit_ton', ascending=False).head(10)

plt.figure(figsize=(12, 6))
sns.barplot(data=top_producers, x='produksi_cabai_rawit_ton', y='nama_kabupaten_kota', palette='Greens_r')
plt.title('Top 10 Chili (Cabai Rawit) Producers in West Java (2024)', fontsize=16, pad=20)
plt.xlabel('Production (Ton)', fontsize=12)
plt.ylabel('')
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/Fig_Supply_Production.png", dpi=300)
plt.close()
print("   - Saved Fig_Supply_Production.png")

print("\n" + "="*80)
print(f"ANALYSIS COMPLETED. CHECK '{OUTPUT_DIR}' FOLDER.")
print("="*80)
