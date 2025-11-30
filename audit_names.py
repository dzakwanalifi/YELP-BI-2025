
import pandas as pd
import geopandas as gpd

print("--- AUDIT DATA NAMES ---")

# 1. Cek Nama di CSV
try:
    df = pd.read_csv('sdm_results_fixed/fase1/panel_data_with_lags.csv')
    csv_locs = sorted(df['location_name'].unique().astype(str))
    print(f"\n[CSV] Location Names ({len(csv_locs)}):")
    for loc in csv_locs:
        print(f"  - {loc}")
except Exception as e:
    print(f"Error reading CSV: {e}")

# 2. Cek Nama di GeoJSON (Target)
try:
    gdf = gpd.read_file('GeoJSON/Indonesia_cities.geojson')
    # Filter hanya yang mirip dengan lokasi kita untuk memperpendek list
    keywords = ['Jakarta', 'Bandung', 'Cirebon', 'Indramayu', 'Bekasi', 'Karawang', 'Tasik', 'Bogor', 'Sukabumi', 'Surabaya']
    
    print(f"\n[GeoJSON] Potential Matches in NAME_2:")
    found_names = []
    for idx, row in gdf.iterrows():
        name = str(row['NAME_2'])
        if any(k.lower() in name.lower() for k in keywords):
            found_names.append(name)
    
    for name in sorted(list(set(found_names))):
        print(f"  - {name}")
        
except Exception as e:
    print(f"Error reading GeoJSON: {e}")
