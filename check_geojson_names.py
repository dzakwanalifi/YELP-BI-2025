
import geopandas as gpd

print("Loading GeoJSON...")
gdf = gpd.read_file('GeoJSON/Indonesia_cities.geojson')

targets = ['Jakarta', 'Bandung', 'Cirebon', 'Indramayu', 'Bekasi', 'Karawang', 'Tasikmalaya', 'Bogor', 'Sukabumi', 'Surabaya']

print("\n--- MATCHING NAMES ---")
for target in targets:
    matches = gdf[gdf['NAME_2'].str.contains(target, case=False, na=False)]['NAME_2'].unique()
    print(f"{target}: {matches}")
