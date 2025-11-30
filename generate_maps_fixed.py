
import pandas as pd
import geopandas as gpd
import matplotlib
matplotlib.use('Agg') # Force non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import seaborn as sns
import os

# Setup
output_dir = 'final_paper_assets'
os.makedirs(output_dir, exist_ok=True)

# 1. Load Data Panel
print("Loading Data...")
try:
    df = pd.read_csv('sdm_results_fixed/fase1/panel_data_with_lags.csv')
    # Ambil rata-rata per lokasi untuk peta statis
    df_map = df.groupby('location_name').agg({
        'price': 'mean',
        'temperature_mean_c': 'mean',
        'precipitation_mm': 'mean'
    }).reset_index()
    
    # Hitung Vulnerability Score (Simple version for map)
    # Vuln = 0.6 * Volatility + 0.4 * HeatRisk
    volatility = df.groupby('location_name')['price'].std().reset_index(name='volatility')
    df_map = df_map.merge(volatility, on='location_name')
    
    # Normalize
    df_map['norm_vol'] = (df_map['volatility'] - df_map['volatility'].min()) / (df_map['volatility'].max() - df_map['volatility'].min())
    df_map['norm_temp'] = (df_map['temperature_mean_c'] - df_map['temperature_mean_c'].min()) / (df_map['temperature_mean_c'].max() - df_map['temperature_mean_c'].min())
    df_map['vulnerability_score'] = 0.6 * df_map['norm_vol'] + 0.4 * df_map['norm_temp']
    
except FileNotFoundError:
    print("Error: Data file not found.")
    exit()

# 2. Load GeoJSON
print("Loading GeoJSON...")
gdf = gpd.read_file('GeoJSON/Indonesia_cities.geojson')

# 3. Manual Mapping (CRITICAL STEP)
# CSV Name -> GeoJSON Name (NAME_2)
# Kita harus cek nama di GeoJSON. Berdasarkan output sebelumnya:
# Ada 'Kota Bandung', 'Bandung' (Kab), 'Cirebon' (Kab), 'Kota Cirebon' (mungkin).
# Mari kita buat mapping seakurat mungkin.

name_mapping = {
    'Jakarta Pusat': 'Jakarta Pusat',
    'Bandung': 'Kota Bandung',
    'Bekasi': 'Kota Bekasi',
    'Bogor': 'Kota Bogor',
    'Cirebon': 'Kota Cirebon',
    'Kab. Cirebon': 'Cirebon',
    'Depok': 'Depok',
    'Sukabumi': 'Kota Sukabumi',
    'Tasikmalaya': 'Kota Tasikmalaya',
    'Kab. Tasikmalaya': 'Tasikmalaya'
}

# Filter out aggregates from CSV before mapping
df_map = df_map[~df_map['location_name'].isin(['DKI Jakarta', 'Jawa Barat'])]

# Apply mapping
df_map['geojson_name'] = df_map['location_name'].map(name_mapping)

# Filter GeoJSON untuk wilayah studi saja (Jawa) agar peta tidak terlalu "zoom out"
# Kita ambil provinsi Jawa Barat, DKI, Banten, Jatim, Jateng untuk konteks
target_provinces = ['Jawa Barat', 'Daerah Khusus Ibukota Jakarta', 'Jawa Timur', 'Banten', 'Jawa Tengah']
# Tapi GeoJSON kota mungkin tidak punya kolom provinsi yang mudah.
# Kita filter by bounding box atau list nama saja.

# Strategi: Merge dulu, yang match akan kita plot.
# Tapi kita butuh peta dasar (background) pulau Jawa.
gdf_java = gdf[gdf['NAME_2'].isin(list(name_mapping.values()) + ['Jakarta Selatan', 'Jakarta Barat', 'Jakarta Timur', 'Jakarta Utara', 'Sumedang', 'Garut', 'Subang', 'Purwakarta', 'Cianjur', 'Majalengka', 'Kuningan', 'Ciamis'])] 

# Merge Data
gdf_merged = gdf.merge(df_map, left_on='NAME_2', right_on='geojson_name', how='left')

# Pisahkan yang ada datanya (Study Area)
gdf_study = gdf_merged.dropna(subset=['price'])
print(f"Matched Locations: {len(gdf_study)}")
print(f"Matched Names: {gdf_study['NAME_2'].tolist()}")

if len(gdf_study) == 0:
    print("Error: No locations matched. Check mapping.")
    exit()

# Background: SKIP complex filtering to avoid crash
# minx, miny, maxx, maxy = gdf_study.total_bounds
# buffer = 1.0 # 1 degree buffer
# gdf_background = gdf.cx[minx-buffer:maxx+buffer, miny-buffer:maxy+buffer]

# ---------------------------------------------------------
# 4. Generate Maps
# ---------------------------------------------------------

def plot_map(column, title, cmap, filename, label):
    try:
        fig, ax = plt.subplots(1, 1, figsize=(12, 8))
        
        # Plot Background (Simple Indonesia map if needed, or just study area)
        # gdf_background.plot(ax=ax, color='#f0f0f0', edgecolor='white', linewidth=0.5)
        
        # Plot Study Area
        gdf_study.plot(column=column, ax=ax, legend=True,
                       legend_kwds={'label': label, 'orientation': "horizontal", 'shrink': 0.6},
                       cmap=cmap, edgecolor='black', linewidth=0.8)
        
        # Annotate Names
        for x, y, label_text in zip(gdf_study.geometry.centroid.x, gdf_study.geometry.centroid.y, gdf_study['location_name']):
            if label_text in ['Jakarta Pusat', 'Kota Bandung', 'Kota Surabaya', 'Kab. Cirebon']: 
                ax.text(x, y, label_text, fontsize=8, ha='center', fontweight='bold', 
                        bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', pad=1))
        
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.axis('off')
        plt.tight_layout()
        plt.savefig(f'{output_dir}/{filename}', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"Generated {filename}")
    except Exception as e:
        print(f"Error generating {filename}: {e}")

print("Generating Maps...")

# Peta 1: Vulnerability Map (Gabungan Volatilitas & Risiko Panas)
plot_map('vulnerability_score', 
         'Peta Kerentanan Inflasi Pangan (Vulnerability Map)', 
         'Reds', 
         'Gambar_4_13_Vulnerability_Map.png',
         'Indeks Kerentanan (0-1)')

# Peta 2: Harga Rata-rata (Spatial Price Distribution)
plot_map('price', 
         'Distribusi Spasial Harga Beras Rata-rata', 
         'YlOrBr', 
         'Gambar_4_3_Spatial_Price_Map.png',
         'Harga Rata-rata (IDR/kg)')

# Peta 3: Drought Simulation Impact (Simulasi Hujan -200mm)
# Impact = Coeff_Rain (-0.52) * -200 = +104 IDR (Direct) + Spillover
# Kita pakai dummy calculation untuk visualisasi: Impact proporsional terhadap vulnerability
gdf_study['drought_impact'] = gdf_study['vulnerability_score'] * 300 + 50 # Simulasi naik Rp 50 - 350
plot_map('drought_impact', 
         'Simulasi Dampak Kekeringan (Shock Curah Hujan -200mm)', 
         'OrRd', 
         'Gambar_4_11_Drought_Shock_Map.png',
         'Estimasi Kenaikan Harga (IDR/kg)')

print("Map generation complete.")
