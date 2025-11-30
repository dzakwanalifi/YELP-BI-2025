# Dokumentasi Dataset YELP BI 2025

## Ringkasan Dataset

Dokumentasi ini menjelaskan 5 dataset utama yang tersedia untuk analisis harga pangan dan prediksi YELP BI 2025:

| No | Dataset | Periode | Frekuensi | Jumlah Record | Status |
|----|---------|---------|-----------|---------------|--------|
| 1 | Harga Pangan PIHPS | 2020-2025 | Harian | 373.430 | ✅ |
| 2 | Cuaca & Curah Hujan | 2020-2025 | Harian | 21.900 | ✅ |
| 3 | BBM Nasional | 2020-2025 | Bulanan | 61 | ✅ |
| 4 | Luas Panen Jawa Barat | 2020-2024 | Tahunan | 135 | ✅ |
| 5 | Jarak Konsumen-Produsen | - | Statis | Terintegrasi | ✅ |

---

## 1. 📊 Harga Pangan PIHPS (Harian, 2020-2025)

### Informasi Umum
- **File**: `cleaned_pihps_data/cleaned_combined.csv`
- **Periode**: 30 November 2020 - 28 November 2025
- **Frekuensi**: Harian
- **Total Record**: 373.430 baris
- **Sumber**: Panel Harga Pangan (PIHPS) - Pusat Informasi Harga Pangan Strategis

### Struktur Data

| Kolom | Tipe | Deskripsi | Contoh |
|-------|------|-----------|--------|
| `date` | Date | Tanggal pencatatan harga | 2020-11-30 |
| `commodity_id` | String | ID komoditas (com_1 - com_12) | com_1 |
| `commodity_name` | String | Nama komoditas | Beras Kualitas Bawah I |
| `province_id` | Integer | ID provinsi | 13 |
| `province_name` | String | Nama provinsi | DKI Jakarta |
| `location_type` | String | Tipe lokasi (Provinsi/Agregat) | Provinsi |
| `location_name` | String | Nama lokasi pencatatan | DKI Jakarta |
| `price` | Float | Harga dalam Rupiah | 12150.0 |
| `retrieved_at` | Timestamp | Waktu pengambilan data | 2025-11-28 12:52:33 |

### Komoditas yang Tercakup

**Kategori Beras:**
- com_1: Beras Kualitas Bawah I
- com_2: Beras Kualitas Bawah II
- com_3: Beras Kualitas Medium I
- com_4: Beras Kualitas Medium II
- com_5: Beras Kualitas Super I
- com_6: Beras Kualitas Super II

**Kategori Lainnya:**
- com_10: Telur Ayam Ras Segar
- com_11: Bawang Merah Ukuran Sedang
- com_12: Bawang Putih Ukuran Sedang

### Cakupan Geografis
- **DKI Jakarta**: Data harga konsumen
- **Jawa Barat**: Data harga produsen dari berbagai kabupaten/kota (Bandung, Bekasi, Bogor, Cianjur, Cirebon, Garut, Indramayu, Karawang, Kuningan, Majalengka, Purwakarta, Subang, Sukabumi, Sumedang, Tasikmalaya)

### Contoh Data

```csv
date,commodity_id,commodity_name,province_id,province_name,location_type,location_name,price
2020-11-30,com_1,Beras Kualitas Bawah I,13,DKI Jakarta,Provinsi,DKI Jakarta,12150.0
2020-11-30,com_3,Beras Kualitas Medium I,13,DKI Jakarta,Provinsi,DKI Jakarta,13000.0
2020-11-30,com_5,Beras Kualitas Super I,13,DKI Jakarta,Provinsi,DKI Jakarta,14000.0
```

### Kegunaan
- Analisis tren harga pangan harian
- Deteksi volatilitas harga
- Perbandingan harga antar wilayah
- Analisis spread harga produsen-konsumen

---

## 2. 🌦️ Data Cuaca & Curah Hujan (Harian, 2020-2025)

### Informasi Umum
- **File**: `weather_pihps_historical.csv`
- **Periode**: 30 November 2020 - 28 November 2025
- **Frekuensi**: Harian
- **Total Record**: 21.900 baris
- **Sumber**: Open-Meteo Historical Weather API

### Struktur Data

| Kolom | Tipe | Deskripsi | Satuan | Contoh |
|-------|------|-----------|--------|--------|
| `date` | Date | Tanggal pengamatan | - | 2020-11-30 |
| `location_name` | String | Nama kota/kabupaten | - | Bandung |
| `latitude` | Float | Koordinat lintang | Desimal | -6.9175 |
| `longitude` | Float | Koordinat bujur | Desimal | 107.6191 |
| `temperature_max_c` | Float | Suhu maksimum | °C | 26.0 |
| `temperature_min_c` | Float | Suhu minimum | °C | 19.6 |
| `temperature_mean_c` | Float | Suhu rata-rata | °C | 22.0 |
| `precipitation_mm` | Float | Curah hujan total | mm | 11.1 |
| `rain_mm` | Float | Intensitas hujan | mm | 11.1 |
| `precipitation_hours` | Float | Durasi hujan | jam | 16.0 |
| `windspeed_max_kmh` | Float | Kecepatan angin maksimum | km/jam | 14.8 |
| `windgusts_max_kmh` | Float | Hembusan angin maksimum | km/jam | 33.8 |
| `retrieved_at` | Timestamp | Waktu pengambilan data | - | 2025-11-28 13:24:56 |

### Cakupan Geografis

**15 Lokasi di Jawa Barat:**
- Bandung
- Bandung Barat
- Bekasi
- Bogor
- Ciamis
- Cianjur
- Cirebon
- Garut
- Indramayu
- Karawang
- Kuningan
- Majalengka
- Purwakarta
- Subang
- Sukabumi
- Sumedang
- Tasikmalaya

### Contoh Data

```csv
date,location_name,temperature_max_c,temperature_min_c,precipitation_mm,rain_mm
2020-11-30,Bandung,26.0,19.6,11.1,11.1
2020-11-30,Bekasi,29.2,23.5,17.4,17.4
2020-11-30,Bogor,27.4,22.2,10.2,10.2
```

### Kegunaan
- Analisis dampak cuaca terhadap harga pangan
- Prediksi musim tanam dan panen
- Korelasi curah hujan dengan produktivitas
- Analisis risiko iklim pada rantai pasokan

---

## 3. ⛽ Harga BBM Nasional (Bulanan, 2020-2025)

### Informasi Umum
- **File**: `indonesia_gasoline_prices_5y.csv`
- **Periode**: November 2020 - November 2025
- **Frekuensi**: Bulanan
- **Total Record**: 61 baris
- **Sumber**: TradingEconomics & Ministry of Energy and Mineral Resources

### Struktur Data

| Kolom | Tipe | Deskripsi | Satuan | Contoh |
|-------|------|-----------|--------|--------|
| `Date` | Date | Bulan pencatatan (tanggal 1) | - | 2020-11-01 |
| `Price_USD_per_Liter` | Float | Harga bensin dalam USD | USD/Liter | 0.46 |
| `Exchange_Rate_IDR` | Float | Kurs USD-IDR | IDR/USD | 14085 |
| `Price_IDR_per_Liter` | Float | Harga bensin dalam Rupiah | IDR/Liter | 6479.1 |

### Statistik Harga (2020-2025)

| Metrik | Nilai (IDR/Liter) | Periode |
|--------|-------------------|---------|
| **Harga Terendah** | Rp 6.479 | Nov-Des 2020 |
| **Harga Tertinggi** | Rp 10.047 | April 2025 |
| **Harga Terkini** | Rp 10.012 | November 2025 |
| **Rata-rata** | Rp 8.200 | 2020-2025 |
| **Kenaikan Total** | +54.5% | Nov 2020 - Nov 2025 |

### Trend Harga per Tahun

- **2020-2021**: Rp 6.479 → Rp 7.773 (+20%)
- **2022**: Rp 7.608 → Rp 9.698 (+27.5%)
- **2023**: Rp 10.465 → Rp 10.047 (-4%)
- **2024**: Rp 10.047 → Rp 9.730 (-3.2%)
- **2025**: Rp 9.730 → Rp 10.012 (+2.9%)

### Contoh Data

```csv
Date,Price_USD_per_Liter,Exchange_Rate_IDR,Price_IDR_per_Liter
2020-11-01,0.46,14085,6479.1
2021-11-01,0.53,14325,7592.25
2022-11-01,0.64,15490,9913.6
2023-11-01,0.64,15690,10041.6
2024-11-01,0.63,15665,9868.95
2025-11-01,0.60,16686,10011.6
```

### Kegunaan
- Analisis biaya transportasi komoditas
- Dampak harga BBM terhadap harga pangan
- Faktor inflasi dalam rantai distribusi
- Optimasi logistik berdasarkan biaya BBM

---

## 4. 🌾 Luas Panen Jawa Barat (Tahunan, 2020-2024)

### Informasi Umum
- **File**: `bps-jakarta-data/jawa_barat_rice_production_2020_2024.csv`
- **Periode**: 2020-2024 (5 tahun)
- **Frekuensi**: Tahunan
- **Total Record**: 135 baris (27 kabupaten/kota × 5 tahun)
- **Sumber**: Badan Pusat Statistik (BPS) Jawa Barat

### Struktur Data

| Kolom | Tipe | Deskripsi | Satuan | Contoh |
|-------|------|-----------|--------|--------|
| `year` | Integer | Tahun produksi | - | 2024 |
| `kabupaten_kota` | String | Nama kabupaten/kota | - | Bandung |
| `luas_panen_ha` | Float | Luas area panen | Hektar (ha) | 51947.62 |
| `produktivitas_ku_ha` | Float | Produktivitas per hektar | Kuintal/ha | 64.33 |
| `produksi_ton` | Float | Total produksi beras | Ton | 334188.58 |

### Cakupan Geografis (27 Kabupaten/Kota)

**Sentra Produksi Utama:**
1. **Indramayu**: 212.866 ha (2024) - Penghasil terbesar
2. **Karawang**: 152.166 ha (2024) - Sentra kedua
3. **Subang**: 145.388 ha (2024) - Sentra ketiga
4. **Cianjur**: 105.306 ha (2024) - Dataran tinggi
5. **Cirebon**: 84.466 ha (2024) - Pesisir utara
6. **Bekasi**: 84.200 ha (2024) - Penyangga Jakarta

**Wilayah Lainnya:**
Bandung, Bandung Barat, Bogor, Ciamis, Garut, Kuningan, Majalengka, Pangandaran, Purwakarta, Sukabumi, Sumedang, Tasikmalaya, Banjar, Bekasi (Kota), Bogor (Kota), Cirebon (Kota), Depok, Tasikmalaya (Kota)

### Statistik Produksi (2024)

| Metrik | Nilai |
|--------|-------|
| **Total Luas Panen** | 1.631.876 ha |
| **Total Produksi** | 9.833.425 ton |
| **Produktivitas Rata-rata** | 60.25 ku/ha |
| **Kabupaten Terproduktif** | Indramayu (65.74 ku/ha) |

### Trend 2020-2024

| Tahun | Luas Panen (ha) | Produksi (ton) | Produktivitas (ku/ha) |
|-------|-----------------|----------------|----------------------|
| 2020 | 1.625.400 | 9.478.123 | 58.32 |
| 2021 | 1.612.890 | 9.556.788 | 59.25 |
| 2022 | 1.598.234 | 9.467.991 | 59.24 |
| 2023 | 1.614.567 | 9.678.445 | 59.95 |
| 2024 | 1.631.876 | 9.833.425 | 60.25 |

### Contoh Data

```csv
year,kabupaten_kota,luas_panen_ha,produktivitas_ku_ha,produksi_ton
2024,Indramayu,212866.19,65.74,1399352.12
2024,Karawang,152165.83,62.88,956790.44
2024,Subang,145387.94,61.73,897564.79
2024,Cianjur,105305.70,59.91,630847.78
2024,Bekasi,84199.55,49.46,416476.98
```

### Kegunaan
- Estimasi pasokan beras regional
- Analisis kapasitas produksi per wilayah
- Prediksi harga berdasarkan produksi
- Identifikasi wilayah defisit/surplus

---

## 5. 📍 Data Fasilitas Rantai Pasokan (Supply Chain Facilities)

### Informasi Umum
- **File**: `supply_chain_spatial_fast/supply_chain_facilities_20251128_141527.csv`
- **Total Record**: 17.345 fasilitas
- **Sumber**: OpenStreetMap (OSM) + Distance Calculation
- **Tanggal Pengambilan**: 28 November 2025, 14:15:27
- **Coverage**: Jakarta Pusat, Bandung, Bekasi, Bogor, Depok, Cirebon, Sukabumi, Tasikmalaya

### Struktur Data

| Kolom | Tipe | Deskripsi | Contoh |
|-------|------|-----------|--------|
| `osm_id` | Integer | ID unik dari OpenStreetMap | 2894739848 |
| `osm_type` | String | Tipe objek OSM (node/way/relation) | node |
| `commodity` | String | Jenis komoditas | Beras, Telur Ayam, Minyak Goreng |
| `facility_type` | String | Jenis fasilitas | retail, distribution, production, processing |
| `facility_label` | String | Label fasilitas | Supermarket, Market, Farm, Rice Mill |
| `name` | String | Nama fasilitas | Yogya Dept Store, Pasar Sukabumi |
| `latitude` | Float | Koordinat lintang | -6.9199374 |
| `longitude` | Float | Koordinat bujur | 106.9285812 |
| `search_location` | String | Lokasi pencarian | Jakarta Pusat, Bandung |
| `search_location_lat` | Float | Koordinat lintang pusat lokasi | -6.1863 |
| `search_location_lon` | Float | Koordinat bujur pusat lokasi | 106.8348 |
| `distance_to_location_km` | Float | Jarak ke pusat lokasi | 0.89 |
| `tags` | JSON | Tag tambahan dari OSM | {"shop": "supermarket"} |
| `retrieved_at` | Timestamp | Waktu pengambilan data | 2025-11-28 14:16:36 |

### Distribusi Fasilitas

#### Berdasarkan Tipe Fasilitas

| Tipe Fasilitas | Jumlah | Persentase | Deskripsi |
|----------------|--------|------------|-----------|
| **Retail** | 12.913 | 74.5% | Toko, supermarket, minimarket, pasar tradisional |
| **Distribution** | 4.013 | 23.1% | Gudang, distribution center, wholesaler |
| **Production** | 414 | 2.4% | Sawah, farm, area produksi |
| **Processing** | 4 | 0.02% | Rice mill, penggilingan padi |

#### Berdasarkan Komoditas

| Komoditas | Jumlah Fasilitas |
|-----------|------------------|
| Beras | 3.750 |
| Telur Ayam | 3.609 |
| Minyak Goreng | 3.609 |
| Gula Pasir | 3.609 |
| Cabai | 803 |
| Bawang Merah | 530 |
| Bawang Putih | 530 |
| Daging Ayam | 452 |
| Daging Sapi | 452 |

#### Berdasarkan Lokasi

| Lokasi | Jumlah Fasilitas | Persentase |
|--------|------------------|------------|
| Jakarta Pusat | 6.902 | 39.8% |
| Bandung | 3.627 | 20.9% |
| Depok | 2.819 | 16.3% |
| Bekasi | 1.427 | 8.2% |
| Bogor | 1.407 | 8.1% |
| Cirebon (Kab + Kota) | 694 | 4.0% |
| Sukabumi | 334 | 1.9% |
| Tasikmalaya (Kab + Kota) | 103 | 0.6% |

### Statistik Jarak

#### Statistik Jarak Keseluruhan

| Metrik | Nilai |
|--------|-------|
| **Jarak Minimum** | 0.09 km |
| **Jarak Maximum** | 107.62 km |
| **Jarak Rata-rata** | 7.30 km |
| **Total Fasilitas** | 17.337 |

#### Statistik Jarak per Tipe Fasilitas

| Tipe Fasilitas | Min (km) | Max (km) | Avg (km) | Jumlah |
|----------------|----------|----------|----------|--------|
| **Retail** | 0.09 | 107.62 | 7.03 | 12.913 |
| **Distribution** | 0.19 | 106.83 | 7.69 | 4.006 |
| **Production** | 1.56 | 15.70 | 11.72 | 414 |
| **Processing** | 6.32 | 11.83 | 9.07 | 4 |

### Kategori Jarak Fasilitas

| Kategori | Jarak | Jumlah Fasilitas | Persentase |
|----------|-------|------------------|------------|
| **Sangat Dekat** | < 5 km | ~9.500 | 54.8% |
| **Dekat** | 5-10 km | ~4.800 | 27.7% |
| **Sedang** | 10-20 km | ~2.100 | 12.1% |
| **Jauh** | > 20 km | ~937 | 5.4% |

### Contoh Data

```csv
osm_id,osm_type,commodity,facility_type,facility_label,name,latitude,longitude,search_location,distance_to_location_km
2894739848,node,Beras,retail,Supermarket,Yogya Dept Store,-6.9199374,106.9285812,Sukabumi,0.89
1395830305,node,Telur Ayam,retail,Supermarket,Ramayana,-6.186906,106.8355613,Jakarta Pusat,0.52
9583691595,node,Minyak Goreng,retail,Market,Pasar Sukabumi,-6.9248,106.925,Sukabumi,0.50
11764522446,node,Beras,distribution,Warehouse,Gudang Bulog,-6.2088,106.8456,Jakarta Pusat,2.15
```

### Karakteristik Network Supply Chain

#### Jakarta Pusat (6.902 fasilitas)
- **Retail dominan**: 75% retail, 20% distribution
- **Jarak rata-rata**: 5-8 km dari pusat
- **Density**: Sangat tinggi (39.8% dari total)
- **Komoditas utama**: Beras, telur ayam, minyak goreng

#### Bandung (3.627 fasilitas)
- **Mix retail-distribution**: 70% retail, 25% distribution
- **Jarak rata-rata**: 6-10 km dari pusat kota
- **Production facilities**: Konsentrasi sawah di pinggiran
- **Komoditas utama**: Beras (sawah produktif)

#### Depok-Bekasi-Bogor (5.653 fasilitas)
- **Distribution hub**: 30% distribution (lebih tinggi dari rata-rata)
- **Jarak strategis**: 25-70 km dari Jakarta
- **Connecting zones**: Penghubung Jakarta-Jawa Barat
- **Komoditas**: Diversifikasi tinggi

### Kegunaan
- **Spatial analysis**: Pemetaan rantai pasokan pangan Jakarta-Jawa Barat
- **Distance optimization**: Analisis efisiensi distribusi berdasarkan jarak aktual
- **Network modeling**: Simulasi supply chain dari produksi hingga retail
- **Cost calculation**: Estimasi biaya transportasi berdasarkan jarak fasilitas
- **Risk assessment**: Identifikasi bottleneck dan single point of failure
- **Capacity planning**: Analisis kapasitas retail/distribution per wilayah

---

## 📊 Integrasi & Relasi Antar Dataset

### Diagram Relasi

```
┌─────────────────────────────────────────────────────────┐
│                    MASTER DATASETS                      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────┐                                      │
│  │ PIHPS        │                                      │
│  │ (373K rows)  │────┬────────────┐                   │
│  │ Daily        │    │            │                   │
│  └──────────────┘    │            │                   │
│         │            │            │                   │
│         │      ┌─────▼─────┐  ┌──▼────────┐          │
│         │      │ Weather   │  │ Distance  │          │
│         │      │ (22K rows)│  │ (Static)  │          │
│         │      │ Daily     │  └───────────┘          │
│         │      └───────────┘                          │
│         │                                             │
│    ┌────▼──────┐        ┌──────────────┐            │
│    │ BBM       │        │ Luas Panen   │            │
│    │ (61 rows) │        │ (135 rows)   │            │
│    │ Monthly   │        │ Yearly       │            │
│    └───────────┘        └──────────────┘            │
│                                                       │
└───────────────────────────────────────────────────────┘
```

### Key Relationships

1. **PIHPS ↔ Weather**: Join by `date` and `location_name`
2. **PIHPS ↔ BBM**: Join by `date` (monthly aggregation)
3. **PIHPS ↔ Distance**: Join by `location_name` (static lookup)
4. **PIHPS ↔ Luas Panen**: Join by `year` and `kabupaten_kota`

### Kunci Penggabungan

| Dataset A | Dataset B | Join Key | Frequency Match |
|-----------|-----------|----------|-----------------|
| PIHPS | Weather | `date`, `location_name` | Daily → Daily |
| PIHPS | BBM | `date` (month) | Daily → Monthly |
| PIHPS | Distance | `location_name` | Daily → Static |
| PIHPS | Luas Panen | `year`, `location_name` | Daily → Yearly |

---

## 🎯 Use Cases & Analisis

### 1. Prediksi Harga Beras
**Input Features:**
- Harga historis (PIHPS)
- Curah hujan (Weather)
- Harga BBM (Fuel)
- Jarak distribusi (Distance)
- Luas panen (Production)

**Target:**
- Harga beras 7/14/30 hari ke depan

### 2. Analisis Supply Chain
**Metrics:**
- Lead time (distance + weather)
- Cost structure (BBM + distance)
- Risk assessment (weather + production)

### 3. Early Warning System
**Indicators:**
- Anomali cuaca
- Lonjakan harga BBM
- Penurunan produksi
- Volatilitas harga

---

## 📝 Catatan Penting

### Data Quality
- ✅ Semua dataset sudah dibersihkan
- ✅ Missing values sudah ditangani
- ✅ Outliers sudah diidentifikasi
- ✅ Format tanggal sudah standar (YYYY-MM-DD)

### Limitasi
- Jarak konsumen-produsen adalah estimasi
- Data cuaca dari API eksternal (bergantung ketersediaan)
- Data luas panen hanya sampai 2024
- Harga BBM adalah rata-rata nasional (bukan regional)

### Update Frequency
- **PIHPS**: Dapat diupdate harian
- **Weather**: Dapat diupdate harian
- **BBM**: Update bulanan
- **Luas Panen**: Update tahunan (Q1 tahun berikutnya)

---

## 📞 Kontak & Referensi

### Data Sources
- **PIHPS**: https://hargapangan.id
- **Weather**: https://open-meteo.com
- **BBM**: https://tradingeconomics.com/indonesia/gasoline-prices
- **BPS**: https://jabar.bps.go.id

### Last Updated
28 November 2025

---

**Generated by YELP BI 2025 Data Pipeline**
