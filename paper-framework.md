# Framework Paper YELP BI 2025

## 1. Ide & Konsep Dasar
**Fokus Utama:** **"Spatial Intelligence for Inflation Control"** - Menggunakan Big Data Geospasial (OSM), Harga Pangan (PIHPS), dan Iklim (Open-Meteo) untuk Optimalisasi Rantai Pasok & Stabilitas Harga Jakarta.

**Permasalahan (Why?):**
*   **Ketergantungan Pasokan:** Jakarta bukan produsen pangan, sangat rentan terhadap *supply shock*.
*   **Inefisiensi Distribusi:** Apakah harga tinggi di suatu wilayah disebabkan oleh jauhnya jarak ke distributor/pasar induk? Atau karena minimnya infrastruktur ritel?
*   **Ancaman Iklim (Climate Shock):** Bagaimana anomali cuaca (hujan ekstrem/kekeringan) di sentra produksi mempengaruhi harga di pasar Jakarta secara spesifik?
*   **Gap Informasi:** Kebijakan saat ini seringkali "pukul rata" (agregat), padahal setiap wilayah (Kelurahan/Kecamatan) memiliki karakteristik supply chain yang berbeda.

**Solusi & Pendekatan (How?):**
*   **Supply Chain Mapping (OSM):**
    *   Memetakan 17,000+ fasilitas (produsen, distributor, ritel) di Jakarta & daerah penyangga (Jabar).
    *   Menghitung "Jarak ke Sumber Pasokan" untuk setiap pasar.
*   **Spatial Regression Analysis:**
    *   Model: `Harga ~ Jarak_ke_Produsen + Jarak_ke_Distributor + Curah_Hujan + Demografi`.
    *   Membuktikan hipotesis: "Semakin dekat ke infrastruktur supply chain, harga semakin stabil/murah."
*   **Infrastructure Gap Detection:**
    *   Identifikasi "Food Deserts" atau wilayah dengan harga tinggi namun minim fasilitas supply chain.
    *   Rekomendasi lokasi optimal untuk pembangunan gudang/pasar baru (KAD - Kerjasama Antar Daerah).
*   **Strategic Alignment:**
    *   Mendukung mandat BI dalam stabilitas harga melalui intervensi sisi penawaran (supply-side) yang terukur.
    *   Mengintegrasikan program GNPIP, KAD, dan PSBI dalam satu ekosistem data spasial.

---

## 2. Rencana Judul
*Opsi Judul:*
1.  **"Spatial Intelligence for Price Stability: Integrasi Big Data Geospasial Rantai Pasok dan Iklim dalam Pengendalian Inflasi Pangan Jakarta"**
2.  **"Membedah Transmisi Harga Pangan Jakarta: Pendekatan Spatial Econometrics Berbasis OpenStreetMap dan PIHPS untuk Efisiensi GNPIP"**

---

## 3. Struktur Paper (Outline)

### I. Pendahuluan
*   **Latar Belakang:** Inflasi volatile food sebagai tantangan utama Jakarta. Pentingnya pemahaman *supply chain* yang granular, bukan sekadar agregat.
*   **Masalah:** Kenaikan harga seringkali asimetris antar wilayah. Apa penyebab strukturalnya? (Jarak? Infrastruktur? Cuaca?).
*   **Novelty:** Penggunaan data **OpenStreetMap (17k facilities)** digabungkan dengan **PIHPS (5 tahun)** dan **Open-Meteo (Weather)** untuk analisis spasial yang belum pernah dilakukan sebelumnya.

### II. Tinjauan Pustaka
*   **Teori Lokasi & Harga:** Von Thunen Model (Jarak vs Harga).
*   **Supply Chain Management:** Peran infrastruktur distribusi dalam efisiensi harga.
*   **Climate Economics:** Dampak cuaca terhadap volatilitas harga pertanian.
*   **Kebijakan GNPIP:** Fokus pada kelancaran distribusi dan ketersediaan pasokan.

### III. Metodologi
*   **Data:**
    1.  **Supply Chain Spatial (OSM):** 17,344 fasilitas (Production, Distribution, Retail).
    2.  **Harga Pangan (PIHPS):** Data harian 5 tahun (2020-2025) untuk 9 komoditas strategis.
    3.  **Iklim (Open-Meteo):** Data curah hujan & suhu harian (5 tahun) matching dengan lokasi PIHPS.
    4.  **Ekonomi & Demografi:** Data BPS (Pengeluaran, Penduduk) & Indikator Makro.
    5.  **Peta Digital (GeoJSON):** Batas administrasi Kelurahan/Kecamatan Jakarta untuk visualisasi & analisis spasial.
*   **Metode Analisis:**
    1.  **Geospatial Processing:** Menghitung *Euclidean/Haversine Distance* dari pasar ke fasilitas terdekat.
    2.  **Correlation Analysis:** Korelasi antara Jarak vs Harga, dan Cuaca vs Harga.
    3.  **Spatial Regression:** Mengukur seberapa besar pengaruh variabel spasial terhadap disparitas harga.

### IV. Hasil dan Diskusi

#### 1. Peta Ketahanan Pangan Jakarta (Spatial Mapping)
*   **Visualisasi (Gambar 1):** *"Jakarta Food Supply Chain Heatmap"* - Peta densitas fasilitas (titik merah = pasar, hijau = produsen/gudang) untuk mengidentifikasi *Food Deserts*.
*   **Tabel 1:** *"Statistik Infrastruktur Pangan per Wilayah"* - Menampilkan metrik `Facility Density` (fasilitas/km²) dan `Avg Distance to Supply` (km) untuk setiap Kota Administrasi.
*   **Visualisasi (Gambar 2):** *"Disparitas Akses Pangan"* - Bar chart membandingkan rata-rata jarak tempuh supply chain antar wilayah (misal: Jakpus vs Jaksel).

#### 2. Analisis Determinan Harga (Spatial Regression)
*   **Tabel 2:** *"Hasil Regresi Spasial (Spatial Error Model)"*
    *   **Variabel Dependen:** Harga Komoditas (Beras/Cabai).
    *   **Variabel Independen:** Jarak ke Produsen, Jarak ke Distributor, Curah Hujan, Dummy Wilayah.
    *   **Metrik Utama:** Koefisien (Beta) untuk melihat elastisitas jarak terhadap harga, P-value (Signifikansi), dan R-squared.
*   **Visualisasi (Gambar 3):** *"Scatter Plot Jarak vs Harga"* - Membuktikan hipotesis Von Thunen (semakin jauh dari sumber, harga semakin mahal).
*   **Visualisasi (Gambar 4):** *"Residual Map (Peta Anomali)"* - Menandai pasar-pasar yang memiliki harga "tidak wajar" (jauh di atas prediksi model) sebagai target prioritas Operasi Pasar.

#### 3. Dampak Anomali Cuaca (Climate Impact)
*   **Visualisasi (Gambar 5):** *"Time-Lag Analysis: Curah Hujan vs Harga Cabai"* - Line chart ganda (Dual Axis) untuk melihat seberapa cepat harga merespon kejadian hujan ekstrem di sentra produksi.
*   **Metrik:** `Price Volatility Index` (standar deviasi harga) pada periode El Nino vs Normal.

#### 4. Simulasi Kebijakan (Policy Simulation)
*   **Visualisasi (Gambar 6):** *"Skenario Optimasi Infrastruktur"* - Grafik estimasi penurunan harga jika dibangun 1 *Cold Storage* di titik strategis rekomendasi model.
*   **Metrik:** Potensi Penghematan Biaya Logistik (Rp Miliar/Tahun) dan Penurunan Inflasi Volatile Food (%).
#### 5. Implikasi Kebijakan Strategis (Peran Baru BI)
    *   **Transformasi Peran:** Mengubah pendekatan BI dari sekadar "Pemadam Kebakaran" (reaktif menaikkan suku bunga) menjadi **"Arsitek Ekonomi Daerah"** (preventif membenahi struktur pasar).
    *   **Stabilitas Moneter (Inflation Expectations):**
        *   Output *Nowcasting* digunakan untuk komunikasi kebijakan lebih awal.
        *   Meredam kepanikan pasar (*second-round effect*) sebelum inflasi pangan menjalar ke inflasi inti.
    *   **Optimalisasi GNPIP (Gerakan Nasional Pengendalian Inflasi Pangan):**
        *   **Operasi Pasar Presisi:** Intervensi difokuskan hanya pada pasar/wilayah dengan "Infrastructure Gap" atau anomali harga tertinggi (bukan "pukul rata" satu Jakarta).
        *   **Subsidi Ongkir Cerdas:** Alokasi anggaran subsidi difokuskan pada jalur distribusi yang teridentifikasi paling tidak efisien dalam peta supply chain.
    *   **Efisiensi Kerjasama Antar Daerah (KAD):**
        *   Rekomendasi mitra dagang berbasis data logistik riil (misal: Jakarta Timur pasokan bawangnya dialihkan ke sentra produksi yang lebih dekat/murah secara ongkos angkut).
    *   **Sinergi PSBI & Digitalisasi (QRIS):**
        *   **Program Sosial BI (PSBI):** Bantuan alat pertanian/gudang (Cold Storage) diberikan spesifik ke simpul distribusi yang teridentifikasi lemah dalam model.
        *   **Digitalisasi:** Perluasan QRIS pada pedagang rantai pasok yang terpetakan untuk efisiensi transaksi dan akurasi data harga.

### V. Kesimpulan dan Rekomendasi
*   Pentingnya dimensi spasial dalam pengendalian inflasi.
*   Rekomendasi pembangunan infrastruktur logistik (Cold Storage/Gudang) di titik-titik strategis hasil analisis.

---

## 4. Action Plan (Updated)

### Data Preparation (Ready!)
- [x] **Supply Chain Data:** Scraped 17,344 facilities (OSM).
- [x] **Price Data:** Scraped 5 years PIHPS data.
- [x] **Weather Data:** Scraped 5 years historical weather.
- [x] **GeoJSON Data:** Available (National to Village level).
- [x] **Production Data:** Available (BPS Jabar 2024 - Supply Side).
- [x] **Economic Data:** Available (Inflation, CPI).

### Analysis Phase
- [ ] **Data Merging:** Gabungkan `spatial_features.csv` dengan `cleaned_pihps_data`.
- [ ] **Correlation Matrix:** Hitung korelasi `Price` vs `Distance_to_Production`, `Distance_to_Distribution`.
- [ ] **Visualization:** Buat peta sebaran fasilitas dan harga (bisa pakai QGIS atau Python Folium/Geopandas).
- [ ] **Regression Modeling:** Jalankan model regresi sederhana dulu.

### Drafting Phase
- [ ] **Bab 1-3:** Sesuaikan narasi dengan fokus spasial & supply chain.
- [ ] **Bab 4:** Fokus pada *insight* dari data OSM yang baru didapat.
