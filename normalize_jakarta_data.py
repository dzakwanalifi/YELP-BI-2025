"""
Script untuk normalisasi data dari folder satu-data-jakarta
- Baca semua file Excel
- Analisis struktur dan kolom
- Normalisasi nama file dan kolom
- Convert ke CSV dengan format standar
"""

import pandas as pd
import os
from pathlib import Path

# Directory path
data_dir = "satu-data-jakarta"

# File mapping (old name -> new name, description)
files = {
    "angka-inflasi-(1764230074032).xlsx": {
        "new_name": "jakarta_inflation_rate.csv",
        "description": "Angka Inflasi DKI Jakarta"
    },
    "data-kepadatan-penduduk-provinsi-dki-jakarta-(1764230058966).xlsx": {
        "new_name": "jakarta_population_density.csv",
        "description": "Kepadatan Penduduk DKI Jakarta"
    },
    "data-statistik-kemiskinan-dki-jakarta-(1764229928809).xlsx": {
        "new_name": "jakarta_poverty_statistics.csv",
        "description": "Statistik Kemiskinan DKI Jakarta"
    },
    "indeks-harga-konsumen-provinsi-dki-jakarta-(1764229804998).xlsx": {
        "new_name": "jakarta_consumer_price_index.csv",
        "description": "Indeks Harga Konsumen DKI Jakarta"
    }
}

print("="*80)
print("NORMALISASI DATA SATU DATA JAKARTA")
print("="*80)

for old_filename, info in files.items():
    filepath = os.path.join(data_dir, old_filename)
    new_filename = info["new_name"]
    description = info["description"]

    print(f"\n[Processing] {description}")
    print(f"  Source: {old_filename}")
    print(f"  Target: {new_filename}")

    try:
        # Read Excel file
        print("  Reading Excel file...")

        # Try to read all sheets first
        xl_file = pd.ExcelFile(filepath)
        print(f"  Sheets found: {xl_file.sheet_names}")

        # Read first sheet or the most relevant one
        df = pd.read_excel(filepath, sheet_name=0)

        print(f"  Original shape: {df.shape}")
        print(f"  Original columns: {list(df.columns)}")

        # Display first few rows
        print("\n  First 5 rows:")
        print(df.head().to_string())

        # Basic cleaning
        print("\n  Cleaning data...")

        # Remove completely empty rows and columns
        df = df.dropna(how='all', axis=0)
        df = df.dropna(how='all', axis=1)

        # Clean column names - lowercase, replace spaces with underscore
        df.columns = df.columns.str.strip()
        df.columns = df.columns.str.lower()
        df.columns = df.columns.str.replace(' ', '_')
        df.columns = df.columns.str.replace('[^a-z0-9_]', '', regex=True)

        print(f"  Cleaned shape: {df.shape}")
        print(f"  Cleaned columns: {list(df.columns)}")

        # Save to CSV
        output_path = new_filename
        df.to_csv(output_path, index=False, encoding='utf-8-sig')
        print(f"  [OK] Saved to {output_path}")

        # Summary stats
        print(f"\n  Summary:")
        print(f"    Total rows: {len(df)}")
        print(f"    Total columns: {len(df.columns)}")
        print(f"    Data types: {df.dtypes.value_counts().to_dict()}")

    except Exception as e:
        print(f"  [ERROR] Failed to process: {e}")

print("\n" + "="*80)
print("NORMALIZATION COMPLETED!")
print("="*80)
print("\nOutput files created:")
for info in files.values():
    if os.path.exists(info["new_name"]):
        size = os.path.getsize(info["new_name"])
        print(f"  - {info['new_name']} ({size:,} bytes)")
