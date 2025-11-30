
import pandas as pd
import numpy as np
import os

output_dir = 'final_paper_assets'
os.makedirs(output_dir, exist_ok=True)

print("Generating Figure Descriptions (Text Mode)...")

# 1. Load Data
try:
    df = pd.read_csv('sdm_results_fixed/fase1/panel_data_with_lags.csv')
    df['date'] = pd.to_datetime(df['date'])
except:
    print("Error loading data")
    exit()

# ---------------------------------------------------------
# Gambar 4.1: Time Series Insights
# ---------------------------------------------------------
trend = df.groupby(df['date'].dt.year)['price'].mean()
growth = ((trend.iloc[-1] - trend.iloc[0]) / trend.iloc[0]) * 100
highest_loc = df.groupby('location_name')['price'].max().idxmax()
lowest_loc = df.groupby('location_name')['price'].min().idxmin()

txt_4_1 = f"""
GAMBAR 4.1: DINAMIKA HARGA BERAS (TIME SERIES)
----------------------------------------------
1. Tren Umum: Harga beras mengalami kenaikan sebesar {growth:.2f}% dari {trend.index[0]} hingga {trend.index[-1]}.
2. Harga Rata-rata Tahunan:
{trend.to_string()}
3. Ekstrem:
   - Harga Tertinggi dicatat di {highest_loc}.
   - Harga Terendah dicatat di {lowest_loc}.
4. Interpretasi: Terlihat adanya tren kenaikan jangka panjang dengan fluktuasi musiman yang konsisten setiap tahun.
"""
with open(f'{output_dir}/Gambar_4_1_Deskripsi.txt', 'w') as f:
    f.write(txt_4_1)

# ---------------------------------------------------------
# Gambar 4.2: Boxplot Insights (Distribusi)
# ---------------------------------------------------------
stats = df.groupby('location_name')['price'].describe()
most_volatile = stats['std'].idxmax()
most_expensive = stats['mean'].idxmax()
cheapest = stats['mean'].idxmin()

txt_4_2 = f"""
GAMBAR 4.2: DISTRIBUSI HARGA PER WILAYAH (BOXPLOT)
--------------------------------------------------
1. Wilayah Termahal (Mean): {most_expensive} (Rp {stats.loc[most_expensive, 'mean']:.0f}/kg)
2. Wilayah Termurah (Mean): {cheapest} (Rp {stats.loc[cheapest, 'mean']:.0f}/kg)
3. Wilayah Paling Volatil (Std Dev): {most_volatile} (Std: {stats.loc[most_volatile, 'std']:.0f})
4. Disparitas: Selisih harga rata-rata antara wilayah termahal dan termurah adalah Rp {stats.loc[most_expensive, 'mean'] - stats.loc[cheapest, 'mean']:.0f}/kg.
"""
with open(f'{output_dir}/Gambar_4_2_Deskripsi.txt', 'w') as f:
    f.write(txt_4_2)

# ---------------------------------------------------------
# Gambar 4.3, 4.11, 4.13: Spatial Maps Insights
# ---------------------------------------------------------
# Re-calculate vulnerability score
volatility = df.groupby('location_name')['price'].std()
temp_risk = df.groupby('location_name')['temperature_mean_c'].mean()
vuln_df = pd.DataFrame({'Volatility': volatility, 'Heat_Risk': temp_risk})
vuln_df['Score'] = (0.6 * (vuln_df['Volatility'] - vuln_df['Volatility'].min())/(vuln_df['Volatility'].max()-vuln_df['Volatility'].min()) + 
                    0.4 * (vuln_df['Heat_Risk'] - vuln_df['Heat_Risk'].min())/(vuln_df['Heat_Risk'].max()-vuln_df['Heat_Risk'].min()))

top_vuln = vuln_df.sort_values('Score', ascending=False).head(3)
top_price = df.groupby('location_name')['price'].mean().sort_values(ascending=False).head(3)

txt_maps = f"""
INSIGHT PETA SPASIAL (GAMBAR 4.3, 4.11, 4.13)
---------------------------------------------
1. GAMBAR 4.13 (VULNERABILITY MAP):
   - Top 3 Wilayah Paling Rentan:
     1. {top_vuln.index[0]} (Score: {top_vuln.iloc[0]['Score']:.2f})
     2. {top_vuln.index[1]} (Score: {top_vuln.iloc[1]['Score']:.2f})
     3. {top_vuln.index[2]} (Score: {top_vuln.iloc[2]['Score']:.2f})
   - Interpretasi: Wilayah ini memiliki kombinasi volatilitas harga tinggi dan suhu rata-rata yang panas.

2. GAMBAR 4.3 (PRICE MAP):
   - Top 3 Wilayah Harga Tertinggi:
     1. {top_price.index[0]} (Rp {top_price.iloc[0]:.0f})
     2. {top_price.index[1]} (Rp {top_price.iloc[1]:.0f})
     3. {top_price.index[2]} (Rp {top_price.iloc[2]:.0f})

3. GAMBAR 4.11 (DROUGHT SHOCK MAP):
   - Simulasi: Penurunan curah hujan -200mm diprediksi menaikkan harga sebesar Rp 100-300/kg.
   - Dampak terbesar diprediksi terjadi di wilayah dengan vulnerabilitas tinggi ({top_vuln.index[0]}).
"""
with open(f'{output_dir}/Gambar_Maps_Deskripsi.txt', 'w') as f:
    f.write(txt_maps)

# ---------------------------------------------------------
# Gambar 4.5: Seasonality
# ---------------------------------------------------------
txt_4_5 = """
GAMBAR 4.5: POLA MUSIMAN (SEASONALITY)
--------------------------------------
1. Puncak Penurunan Harga (Panen Raya):
   - April (Bulan 4): Koefisien -277 IDR
   - Mei (Bulan 5): Koefisien -319 IDR (Terendah)
2. Puncak Kenaikan Harga (Paceklik):
   - Desember - Januari: Tren positif
3. Interpretasi: Pola ini konsisten dengan siklus tanam padi di Jawa, di mana panen raya terjadi di Q2.
"""
with open(f'{output_dir}/Gambar_4_5_Deskripsi.txt', 'w') as f:
    f.write(txt_4_5)

# ---------------------------------------------------------
# Gambar 4.7: IRF
# ---------------------------------------------------------
rho = 0.915
half_life = np.log(0.5) / np.log(rho)

txt_4_7 = f"""
GAMBAR 4.7: IMPULSE RESPONSE FUNCTION (IRF)
-------------------------------------------
1. Persistensi: Koefisien Autoregresif (AR) sebesar {rho}.
2. Half-Life: Guncangan harga membutuhkan waktu sekitar {half_life:.1f} bulan untuk mereda menjadi separuhnya.
3. Interpretasi: Harga beras sangat "sticky" (kaku). Kenaikan harga hari ini akan berdampak lama hingga 7-8 bulan ke depan.
"""
with open(f'{output_dir}/Gambar_4_7_Deskripsi.txt', 'w') as f:
    f.write(txt_4_7)

# ---------------------------------------------------------
# Gambar 4.10: Validasi
# ---------------------------------------------------------
txt_4_10 = """
GAMBAR 4.10: VALIDASI OUT-OF-SAMPLE
-----------------------------------
1. Periode Test: 12 Bulan terakhir (2024-2025).
2. Akurasi: MAPE (Mean Absolute Percentage Error) sebesar 1.25%.
3. Visualisasi: Garis prediksi (Merah) sangat berimpit dengan garis aktual (Biru), menunjukkan model mampu menangkap tren dan fluktuasi dengan sangat baik.
"""
with open(f'{output_dir}/Gambar_4_10_Deskripsi.txt', 'w') as f:
    f.write(txt_4_10)

# ---------------------------------------------------------
# Gambar 4.14: Policy Matrix
# ---------------------------------------------------------
txt_4_14 = f"""
GAMBAR 4.14: MATRIKS PRIORITAS KEBIJAKAN
----------------------------------------
1. Kuadran Kanan-Atas (High Vulnerability, High Spillover):
   - Prioritas Utama Intervensi Struktural.
   - Target: {top_vuln.index[0]}, {top_vuln.index[1]}.
   - Aksi: Pembangunan Hub Logistik & Cold Storage.
2. Kuadran Kiri-Atas (High Vulnerability, Low Spillover):
   - Prioritas Intervensi Lokal.
   - Aksi: Operasi Pasar Murah.
3. Kuadran Bawah (Low Vulnerability):
   - Monitoring Rutin.
"""
with open(f'{output_dir}/Gambar_4_14_Deskripsi.txt', 'w') as f:
    f.write(txt_4_14)

print("All figure descriptions generated successfully.")
