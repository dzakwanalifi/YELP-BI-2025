"""
Script untuk enhance data Jakarta yang sudah dinormalisasi
- Tambahkan kolom tanggal yang lebih readable
- Reorder kolom untuk better readability
- Filter hanya kolom yang bermanfaat
"""

import pandas as pd
from datetime import datetime

print("="*80)
print("ENHANCING JAKARTA DATA")
print("="*80)

# 1. Jakarta Inflation Rate
print("\n[1] Processing jakarta_inflation_rate.csv...")
df = pd.read_csv("jakarta_inflation_rate.csv")

# Convert periode_data (YYYYMM) to readable date
df['year'] = df['periode_data'] // 100
df['month'] = df['periode_data'] % 100
df['date'] = pd.to_datetime(df[['year', 'month']].assign(day=1))

# Rename columns for clarity
df = df.rename(columns={
    'nilai_yoy': 'inflation_yoy_pct',
    'nilai_mtm': 'inflation_mom_pct',
    'nilai_ytd': 'inflation_ytd_pct'
})

# Select and reorder columns
df = df[['date', 'year', 'month', 'inflation_yoy_pct', 'inflation_mom_pct', 'inflation_ytd_pct']]
df = df.sort_values('date')

df.to_csv("jakarta_inflation_rate.csv", index=False, encoding='utf-8-sig')
print(f"  [OK] Enhanced. Rows: {len(df)}, Columns: {len(df.columns)}")
print(f"  Date range: {df['date'].min()} to {df['date'].max()}")

# 2. Jakarta CPI
print("\n[2] Processing jakarta_consumer_price_index.csv...")
df = pd.read_csv("jakarta_consumer_price_index.csv")

# Convert periode_data (YYYYMM) to readable date
df['year'] = df['periode_data'] // 100
df['month'] = df['periode_data'] % 100
df['date'] = pd.to_datetime(df[['year', 'month']].assign(day=1))

# Rename columns
df = df.rename(columns={'nilai_indeks': 'cpi_index'})

# Select and reorder columns
df = df[['date', 'year', 'month', 'cpi_index']]
df = df.sort_values('date')

df.to_csv("jakarta_consumer_price_index.csv", index=False, encoding='utf-8-sig')
print(f"  [OK] Enhanced. Rows: {len(df)}, Columns: {len(df.columns)}")
print(f"  Date range: {df['date'].min()} to {df['date'].max()}")

# 3. Jakarta Population Density
print("\n[3] Processing jakarta_population_density.csv...")
df = pd.read_csv("jakarta_population_density.csv")

# Rename columns for clarity
df = df.rename(columns={
    'periode_data': 'year',
    'wilayah': 'city',
    'kecamatan': 'district',
    'kelurahan': 'subdistrict',
    'jumlah_penduduk': 'population',
    'jumlah_kepadatan': 'population_density_per_km2'
})

# Clean city names
df['city'] = df['city'].str.replace('KOTA ADM. ', '').str.title()

# Select useful columns
df = df[['year', 'city', 'district', 'subdistrict', 'population', 'population_density_per_km2']]
df = df.sort_values(['year', 'city', 'district', 'subdistrict'])

df.to_csv("jakarta_population_density.csv", index=False, encoding='utf-8-sig')
print(f"  [OK] Enhanced. Rows: {len(df)}, Columns: {len(df.columns)}")
print(f"  Cities: {df['city'].unique().tolist()}")

# 4. Jakarta Poverty Statistics
print("\n[4] Processing jakarta_poverty_statistics.csv...")
df = pd.read_csv("jakarta_poverty_statistics.csv")

# Rename columns
df = df.rename(columns={
    'periode_data': 'year',
    'indikator_kemiskinan': 'poverty_indicator',
    'nilai': 'value',
    'satuan': 'unit'
})

# Translate indicator to English
indicator_map = {
    'Jumlah Penduduk Miskin': 'poor_population_count',
    'Persentase Penduduk Miskin': 'poverty_percentage'
}

# Pivot untuk format yang lebih clean
df_pivot = df.pivot(index='year', columns='poverty_indicator', values='value').reset_index()
df_pivot.columns.name = None
df_pivot = df_pivot.rename(columns=indicator_map)

df_pivot = df_pivot.sort_values('year')

df_pivot.to_csv("jakarta_poverty_statistics.csv", index=False, encoding='utf-8-sig')
print(f"  [OK] Enhanced. Rows: {len(df_pivot)}, Columns: {len(df_pivot.columns)}")
print(f"  Year range: {df_pivot['year'].min()} to {df_pivot['year'].max()}")

print("\n" + "="*80)
print("ENHANCEMENT COMPLETED!")
print("="*80)
print("\nAll files have been enhanced with:")
print("  - Readable date columns")
print("  - Standardized column names (English)")
print("  - Sorted by date/time")
print("  - Only useful columns kept")
