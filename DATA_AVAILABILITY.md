# Data Availability

> **Last Updated:** November 28, 2025
> **Total Datasets:** 31 files | **Total Records:** ~937,000+ | **Coverage:** 2006 - 2025

## 📊 Quick Overview

| Data Category | Files | Key Metrics |
|---------------|-------|-------------|
| 🏦 **Economic Indicators** | 5 | National inflation, CPI, retail sales (5 years) |
| 🏙️ **Jakarta Open Data** | 4 | Regional inflation, CPI, population, poverty |
| 📈 **BPS Jakarta & Jabar** | 8 | Consumption patterns, **Production (Supply-Side)** |
| 🛒 **Food Prices (InfoPangan)** | 2 | **Historical (Jan 2024 - Nov 2025)** + Real-time snapshot |
| 💰 **Food Prices (BI PIHPS)** | 3 | **5 years data (2020-2025)**, 21 commodities, Jakarta + Jabar |
| 🌤️ **Weather Data** | 2 | **Historical (5 years)** + Market snapshot |
| 🏭 **Supply Chain Spatial** | 3 | **17,344 facilities**, Production to Retail mapping |
| 🗺️ **GeoJSON Maps** | 4 | **National to Village level** boundaries |

**Geographic Coverage:** National → Provincial → City → Kelurahan (267) → Market (55)
**Commodity Coverage:** 47 InfoPangan items + 21 PIHPS commodities

---

## 📑 Table of Contents
1. [Economic Indicators (Trading Economics)](#economic-indicators-trading-economics)
2. [Jakarta Open Data (Satu Data Jakarta)](#jakarta-open-data-satu-data-jakarta)
3. [BPS Jakarta & Jawa Barat Data](#bps-jakarta-data-badan-pusat-statistik)
4. [Food Prices (InfoPangan)](#food-prices-infopangan-jakarta)
5. [Food Prices (BI PIHPS)](#food-prices-bi-pihps)
6. [Weather Data (Open-Meteo)](#weather-data-open-meteo-api)
7. [Supply Chain Spatial Data (OpenStreetMap)](#supply-chain-spatial-data-openstreetmap)
8. [Tools](#tools)
9. [Data Summary](#data-summary)
10. [Potential Use Cases](#potential-use-cases)
11. [Data Quality Notes](#data-quality-notes)

---


## Economic Indicators (Trading Economics)
Data periode: Oktober 2020 - Oktober 2025 (5 tahun)

| File | Records | Description |
|------|---------|-------------|
| `indonesia_inflation_rate_mom.csv` | 61 | Inflasi bulanan (MoM %) |
| `indonesia_retail_sales.csv` | 61 | Penjualan ritel bulanan (MoM %) |
| `indonesia_consumer_price_index.csv` | 61 | Indeks Harga Konsumen |
| `indonesia_consumer_confidence.csv` | 61 | Indeks Kepercayaan Konsumen |
| `indonesia_food_inflation.csv` | 61 | Inflasi pangan (YoY %) |

## Jakarta Open Data (Satu Data Jakarta)

### Jakarta Inflation Rate
**File:** `jakarta_inflation_rate.csv`
**Records:** 21
**Period:** Jan 2024 - Sep 2025
**Columns:** date, year, month, inflation_yoy_pct, inflation_mom_pct, inflation_ytd_pct

### Jakarta Consumer Price Index
**File:** `jakarta_consumer_price_index.csv`
**Records:** 21
**Period:** Jan 2024 - Sep 2025
**Columns:** date, year, month, cpi_index

### Jakarta Population Density
**File:** `jakarta_population_density.csv`
**Records:** 267
**Period:** 2024
**Coverage:** 6 cities (Jakarta Pusat, Timur, Barat, Selatan, Utara, Kep. Seribu)
**Columns:** year, city, district, subdistrict, population, population_density_per_km2

### Jakarta Poverty Statistics
**File:** `jakarta_poverty_statistics.csv`
**Records:** 7
**Period:** 2006 - 2012
**Columns:** year, poor_population_count, poverty_percentage

## BPS Jakarta Data (Badan Pusat Statistik)
Dataset terstruktur dari publikasi BPS DKI Jakarta 2024

### 1. Pengeluaran Per Kapita Per Wilayah
**File:** `bps-jakarta-data/pengeluaran_per_kapita_wilayah.csv`
**Records:** 7
**Period:** 2023 - 2024
**Coverage:** 6 kabupaten/kota + rata-rata DKI Jakarta
**Columns:** kabupaten_kota, pengeluaran_2023_rp, pengeluaran_2024_rp
**Source:** Pola Konsumsi Penduduk Provinsi DKI Jakarta 2024 (Tabel 2.1)

**Summary:**
- Rata-rata pengeluaran DKI Jakarta 2024: Rp 2.794.485
- Tertinggi: Jakarta Selatan (Rp 3.274.714)
- Terendah: Kepulauan Seribu (Rp 1.415.690)

### 2. Proporsi Pengeluaran Makanan
**File:** `bps-jakarta-data/proporsi_pengeluaran_makanan.csv`
**Records:** 6
**Period:** 2024
**Coverage:** 5 golongan pengeluaran + rata-rata
**Columns:** golongan_pengeluaran_rp, makanan_persen, bukan_makanan_persen
**Source:** Pola Konsumsi Penduduk Provinsi DKI Jakarta 2024 (Gambar 2.4)

**Key Insights:**
- Rata-rata pengeluaran makanan: 39,66%
- Golongan rendah (300k-500k): 57,29% untuk makanan
- Golongan tinggi (>1,5jt): 36,82% untuk makanan

### 3. Konsumsi Komoditas Utama
**File:** `bps-jakarta-data/konsumsi_komoditas_utama.csv`
**Records:** 19
**Period:** 2024
**Coverage:** 19 komoditas makanan utama
**Columns:** komoditas, satuan, rata_rata_konsumsi, rata_rata_pengeluaran_rp
**Source:** Pola Konsumsi Penduduk Provinsi DKI Jakarta 2024 (Tabel 2.5)

**Commodities Covered:**
- Beras, Tepung Terigu, Singkong
- Ikan/Udang (segar & awetan)
- Daging Sapi, Daging Ayam, Telur
- Susu Kental Manis
- Sayuran: Bayam, Bawang Merah, Bawang Putih, Cabai Merah, Cabai Rawit
- Buah: Pisang
- Protein Nabati: Tahu, Tempe
- Minyak Goreng, Gula Pasir

**Top Expenditures:**
1. Beras: Rp 77.807
2. Ikan/Udang Segar: Rp 72.133
3. Daging Ayam: Rp 37.385

### 4. Pengeluaran Komoditas Per Wilayah
**File:** `bps-jakarta-data/pengeluaran_komoditas_per_wilayah.csv`
**Records:** 12
**Period:** 2024
**Coverage:** 11 kelompok komoditas × 6 wilayah
**Columns:** kelompok_komoditas, kepulauan_seribu, jakarta_selatan, jakarta_timur, jakarta_pusat, jakarta_barat, jakarta_utara
**Source:** Pola Konsumsi Penduduk Provinsi DKI Jakarta 2024 (Tabel 2.3)

**Commodity Groups:**
- Padi-padian, Umbi-umbian
- Ikan/Udang/Cumi/Kerang
- Daging, Telur dan Susu
- Sayur-sayuran, Kacang-kacangan, Buah-buahan
- Minyak dan Kelapa, Bumbu-bumbuan
- Makanan Jadi

**Regional Patterns:**
- Jakarta Selatan: Pengeluaran makanan tertinggi (Rp 1.273.855)
- Kepulauan Seribu: Pengeluaran makanan terendah (Rp 837.989)
- Makanan Jadi dominan di semua wilayah (30-50% total pengeluaran)

### 5. Sarana Ekonomi Kelurahan
**File:** `bps-jakarta-data/sarana_ekonomi_kelurahan.csv`
**Records:** 7
**Period:** 2024
**Coverage:** 6 kabupaten/kota + total DKI Jakarta
**Columns:** kabupaten_kota, kelompok_pertokoan, pasar_permanen, pasar_semi_permanen, toko_warung_kelontong
**Source:** Statistik Potensi Kelurahan Provinsi DKI Jakarta 2024 (Tabel 9.2)

**Infrastructure Summary:**
- Total kelurahan: 267
- Kelurahan dengan pertokoan: 218 (81,6%)
- Kelurahan dengan pasar permanen: 158 (59,2%)
- Kelurahan dengan pasar semi permanen: 104 (39,0%)
- Semua kelurahan memiliki toko/warung kelontong

**Best Coverage:**
- Jakarta Timur: 57 kelurahan dengan pertokoan, 43 pasar permanen
- Jakarta Selatan: 56 kelurahan dengan pertokoan, 36 pasar permanen

### 6. Penerima SKTM (Indikator Kemiskinan)
**File:** `bps-jakarta-data/penerima_sktm_kelurahan.csv`
**Records:** 7
**Period:** 2023
**Coverage:** 6 kabupaten/kota + total DKI Jakarta
**Columns:** kabupaten_kota, kelurahan_ada_penerima_sktm, kelurahan_tidak_ada_penerima_sktm, total_kelurahan
**Source:** Statistik Potensi Kelurahan Provinsi DKI Jakarta 2024 (Tabel 17.1)

**Poverty Indicators:**
- 243 kelurahan (91,0%) memiliki warga penerima SKTM
- 24 kelurahan (9,0%) tidak ada warga penerima SKTM

**Regional Distribution:**
- Jakarta Timur: 63/65 kelurahan (96,9%) ada penerima SKTM
- Jakarta Barat: 54/56 kelurahan (96,4%) ada penerima SKTM
- Jakarta Selatan: 56/65 kelurahan (86,2%) ada penerima SKTM

### 7. Profil Penghasilan Utama
**File:** `bps-jakarta-data/profil_penghasilan_utama.csv`
**Records:** 7
**Period:** 2024
**Coverage:** 6 kabupaten/kota + total kelurahan
**Columns:** kabupaten_kota, pertanian_perikanan, industri_pengolahan, perdagangan_reparasi, akomodasi_makan_minum
**Source:** Statistik Potensi Kelurahan Provinsi DKI Jakarta 2024 (Tabel 2.1)

**Economic Profile:**
- Perdagangan & Reparasi: Dominan (171 kelurahan, 64,0%)
- Akomodasi & Makan Minum: 25 kelurahan (9,4%)
- Industri Pengolahan: 17 kelurahan (6,4%)
- Pertanian/Perikanan: 6 kelurahan (2,2%) - hanya di Kepulauan Seribu

**Regional Specialization:**
- Jakarta Barat: Perdagangan terkuat (46 kelurahan)
- Jakarta Selatan: Akomodasi & Makan Minum terbanyak (17 kelurahan)
- Jakarta Barat: Industri Pengolahan terbanyak (8 kelurahan)

## BPS Jawa Barat Data (Provinsi Jawa Barat Dalam Angka 2025)
Data produksi pangan strategis (Supply-Side) untuk analisis ketersediaan pasokan ke Jakarta.

### 1. Produksi Pangan Strategis 2024
**File:** `bps-jakarta-data/jawa_barat_food_production_2024.csv`
**Records:** 27 (Kabupaten/Kota di Jawa Barat)
**Period:** 2024 (Angka Sementara)
**Columns:** nama_kabupaten_kota, produksi_bawang_merah_ton, produksi_cabai_besar_ton, produksi_cabai_rawit_ton, produksi_daging_ayam_ton, produksi_telur_ayam_ton, produksi_daging_sapi_ton, tahun_data

**Key Insights (Supply Centers):**
- **Bawang Merah:** Kab. Bandung (87.6rb ton), Kab. Garut (37rb ton), Kab. Cirebon (32rb ton).
- **Cabai Rawit:** Kab. Garut (53rb ton), Kab. Bandung (37.8rb ton), Kab. Cianjur (19.4rb ton).
- **Daging Ayam:** Kab. Ciamis (141rb ton), Kab. Subang (114rb ton).
- **Telur Ayam:** Kab. Bogor (242rb ton), Kab. Sukabumi (125rb ton).
- **Peran:** Mengidentifikasi sentra produksi utama yang menjadi sumber pasokan pasar Jakarta.

## Food Prices (InfoPangan Jakarta)

### 1. Historical Data (NEW!)
**File:** `infopangan_historical_20251127_202417.csv`
**Size:** ~115 MB
**Period:** **1 Januari 2024 - 27 November 2025** (Daily)
**Coverage:** 55 Markets × 47 Commodities
**Columns:** `date`, `market_id`, `market_name`, `commodity_id`, `commodity_name`, `price`, `unit` (estimated)

### 2. Real-time Snapshot
**File:** `infopangan_complete_data_20251127_144533.csv`
**Records:** 2,377
**Date:** 27 November 2025
**Columns:** market_id, market_name, market_address, city_id, city_name, province_id, province_name, latitude, longitude, price_date, commodity_id, commodity_name, unit, newest_price, prev_price, highest_price, lowest_price, avg_price, status, latest_update

**Market Coverage:**
- 48 pasar Jakarta (Jakarta Pusat, Timur, Barat, Selatan, Utara)
- 5 pasar Bogor
- 2 pasar Tangerang

## Food Prices (BI PIHPS)
**Source:** Bank Indonesia - Pusat Informasi Harga Pangan Strategis

### 1. Cleaned Combined Data
**File:** `cleaned_pihps_data/cleaned_combined.csv`
**Size:** 39 MB
**Records:** 373,430
**Period:** November 30, 2020 - November 28, 2025 (5 years)
**Coverage:** DKI Jakarta + Jawa Barat
**Columns:** date, commodity_id, commodity_name, province_id, province_name, location_type, location_name, price, retrieved_at

**Commodities (21 items):**
- Beras (6 kualitas: Bawah I/II, Medium I/II, Super I/II)
- Protein: Daging Ayam Ras, Daging Sapi Kualitas 1/2, Telur Ayam Ras
- Sayuran: Bawang Merah, Bawang Putih, Cabai Merah Besar, Cabai Merah Keriting, Cabai Rawit Hijau/Merah
- Minyak Goreng: Curah, Kemasan Bermerk 1/2
- Gula Pasir: Kualitas Premium, Lokal

**Location Types:**
- Agregat: 54,322 records
- Provinsi: 53,298 records
- Kabupaten/Kota: 265,810 records

### 2. DKI Jakarta
**File:** `cleaned_pihps_data/dki_jakarta.csv`
**Size:** 8.4 MB
**Records:** 80,333
**Locations:** 3 (Semua Provinsi, DKI Jakarta, Jakarta Pusat)
**Avg Price:** Rp 38,934 (min: 9,900 - max: 165,000)

### 3. Jawa Barat
**File:** `cleaned_pihps_data/jawa_barat.csv`
**Size:** 31 MB
**Records:** 293,097
**Locations:** 11 (Semua Provinsi, Jawa Barat + 9 kota/kabupaten: Bogor, Sukabumi, Depok, Bandung, Bekasi, Kab. Tasikmalaya, Tasikmalaya, Cirebon, Kab. Cirebon)
**Avg Price:** Rp 37,237 (min: 8,150 - max: 227,500)

## Weather Data (Open-Meteo API)

### 1. Historical Weather for PIHPS Locations (NEW!)
**File:** `weather_pihps_historical.csv`
**Records:** 21,900
**Period:** November 30, 2020 - November 28, 2025 (5 years)
**Coverage:** 12 locations (DKI Jakarta + Jawa Barat cities)
**Columns:** date, location_name, latitude, longitude, temperature_max_c, temperature_min_c, temperature_mean_c, precipitation_mm, rain_mm, precipitation_hours, windspeed_max_kmh, windgusts_max_kmh, retrieved_at

**Locations:**
- DKI Jakarta: DKI Jakarta, Jakarta Pusat
- Jawa Barat: Jawa Barat, Bandung, Bekasi, Bogor, Cirebon, Depok, Kab. Cirebon, Kab. Tasikmalaya, Sukabumi, Tasikmalaya

**Weather Summary:**
- Average temperature: 25.3°C
- Average precipitation: 7.3 mm/day
- Days with rain: 19,678 (89.9%)
- Complete daily weather data matching PIHPS date range

### 2. Market Snapshot Weather
**File:** `weather_data_20251127_150653.csv`
**Records:** 55
**Date:** November 27, 2025
**Coverage:** 55 markets (48 Jakarta, 5 Bogor, 2 Tangerang)
**Columns:** date, market_id, market_name, city_name, latitude, longitude, temperature_max_c, temperature_min_c, temperature_mean_c, precipitation_mm, rain_mm, precipitation_hours, windspeed_max_kmh, weather_code

**Summary:**
- Average temperature: 28.0°C (range: 25.2°C - 29.0°C)
- Average precipitation: 0.3mm
- Markets with rain: 39/55

## Supply Chain Spatial Data (OpenStreetMap)

### 1. Supply Chain Facilities (NEW!)
**File:** `supply_chain_spatial_fast/supply_chain_facilities_20251128_141527.csv`
**Records:** 17,344
**Date:** November 28, 2025
**Coverage:** 10 locations (Jakarta Pusat, Bandung, Depok, Bekasi, Bogor, Cirebon, Sukabumi, Kab. Cirebon, Kab. Tasikmalaya, Tasikmalaya)
**Search Radius:** 15 KM from city center
**Columns:** osm_id, osm_type, commodity, facility_type, facility_label, name, latitude, longitude, search_location, search_location_lat, search_location_lon, distance_to_location_km, tags, retrieved_at

**Facilities by Commodity:**
- Beras: 3,750 facilities (rice mills, farms, warehouses, markets, retail)
- Minyak Goreng: 3,609 facilities (oil mills, palm oil factories, warehouses, retail)
- Telur Ayam: 3,609 facilities (poultry farms, markets, retail)
- Gula Pasir: 3,609 facilities (sugar mills, sugarcane farms, warehouses, retail)
- Cabai: 803 facilities (chili farms, greenhouses, markets, retail)
- Bawang Merah: 530 facilities (onion farms, vegetable warehouses, markets)
- Bawang Putih: 530 facilities (garlic farms, vegetable warehouses, markets)
- Daging Ayam: 452 facilities (poultry farms, slaughterhouses, cold storage, butchers)
- Daging Sapi: 452 facilities (cattle farms, slaughterhouses, cold storage, butchers)

**Facilities by Type:**
- Retail: 12,913 facilities (convenience stores, supermarkets, greengrocers, butchers)
- Distribution: 4,013 facilities (wholesale markets, traditional markets)
- Production: 414 facilities (farms, mills, factories)
- Processing: 4 facilities (slaughterhouses)

**Facilities by Location:**
- Jakarta Pusat: 6,918 facilities
- Bandung: 3,631 facilities
- Depok: 2,819 facilities
- Bekasi: 1,438 facilities
- Bogor: 1,407 facilities
- Cirebon: 613 facilities
- Sukabumi: 334 facilities
- Kab. Cirebon: 81 facilities
- Kab. Tasikmalaya: 56 facilities
- Tasikmalaya: 47 facilities

### 2. Location-Facility Summary Matrix
**File:** `supply_chain_spatial_fast/location_facility_summary_20251128_141527.csv`
**Records:** 90 (10 locations × 9 commodities)
**Columns:** location, commodity, total_facilities, production_count, processing_count, storage_count, distribution_count, retail_count, nearest_facility_km

**Purpose:** Summary matrix showing facility counts by type for each location-commodity combination, plus distance to nearest facility.

### 3. Spatial Features for Price Analysis
**File:** `supply_chain_spatial_fast/spatial_features_20251128_141527.csv`
**Records:** 90 (10 locations × 9 commodities)
**Columns:** location, commodity, nearest_production_km, avg_production_distance_km, nearest_distribution_km, avg_distribution_distance_km, nearest_retail_km

**Purpose:** Distance-based features for analyzing spatial influence on commodity prices. Ready to merge with PIHPS price data.

**Key Insights:**
- Complete supply chain mapping from production to retail
- Geographic coordinates for all facilities (spatial analysis ready)
- Distance calculations from city centers
- Infrastructure gap identification capability
- Correlation analysis ready: distance vs price

## GeoJSON Data (Administrative Boundaries)
**Source:** Repository Local (`GeoJSON/`)
**Coverage:** National (Indonesia)

| File | Size | Level | Description |
|------|------|-------|-------------|
| `Indonesia_provinces.geojson` | 1.2 MB | Provinsi | Batas wilayah provinsi seluruh Indonesia |
| `Indonesia_cities.geojson` | 2.2 MB | Kota/Kabupaten | Batas wilayah kota/kabupaten |
| `Indonesia_subdistricts.geojson` | 8.0 MB | Kecamatan | Batas wilayah kecamatan (Sub-district) |
| `Indonesia_villages.geojson` | 64 MB | Kelurahan/Desa | Batas wilayah kelurahan/desa (Village) |

**Relevance:**
- Memungkinkan visualisasi peta choropleth (heatmap wilayah).
- Analisis spasial level Kelurahan untuk Jakarta (267 kelurahan).
- Overlay dengan data supply chain dan harga pasar.

## Tools
- `infopangan.py` - Python client untuk InfoPangan API
- `openmeteo.py` - Python client untuk Open-Meteo Weather API
- `scrape_all_infopangan.py` - Script scraper semua data pasar
- `scrape_historical_infopangan.py` - Script scraper data historis InfoPangan
- `scrape_weather_data.py` - Script scraper data cuaca untuk semua pasar
- `scrape_pihps_bi.py` - Script scraper PIHPS Bank Indonesia (parallel processing)
- `clean_pihps_data.py` - Script cleaning data PIHPS (wide to long format)
- `scrape_weather_pihps.py` - Script scraper historical weather untuk lokasi PIHPS (parallel processing)
- `supply_chain_explorer.py` - **Script scraper supply chain facilities dari OpenStreetMap (optimized batching + server rotation)**
- `normalize_jakarta_data.py` - Script normalisasi data Jakarta
- `enhance_jakarta_data.py` - Script enhancement data Jakarta

## Data Summary

### Total Dataset Coverage

| Category | Files | Records | Time Period |
|----------|-------|---------|-------------|
| **Economic Indicators (National)** | 5 | 305 | Oct 2020 - Oct 2025 |
| **Jakarta Open Data** | 4 | 316 | 2006 - 2025 |
| **BPS Jakarta & Jabar** | 8 | 92 | 2023 - 2024 |
| **Food Prices (InfoPangan Historical)** | 1 | **~500,000+** | **Jan 2024 - Nov 2025** |
| **Food Prices (InfoPangan Snapshot)** | 1 | 2,377 | Nov 27, 2025 |
| **Food Prices (BI PIHPS)** | 3 | **373,430** | **Nov 2020 - Nov 2025** |
| **Weather Data (Historical)** | 1 | **21,900** | **Nov 2020 - Nov 2025** |
| **Weather Data (Snapshot)** | 1 | 55 | Nov 27, 2025 |
| **Supply Chain Spatial Data** | 3 | **17,524** | **Nov 28, 2025** |
| **GeoJSON Maps** | 4 | **83,000+ (Villages)** | **2024** |
| **TOTAL** | **30** | **~1,000,000+** | **2006 - 2025** |

### Data Granularity

| Level | Datasets | Use Cases |
|-------|----------|-----------|
| **National** | Economic indicators (inflation, CPI, retail sales) | Macro trends, national context |
| **Provincial (DKI Jakarta)** | BPS consumption patterns, expenditure data | Regional analysis, policy insights |
| **City/District** | Population density, poverty stats, infrastructure | Spatial analysis, targeting |
| **Kelurahan (Subdistrict)** | SKTM recipients, economic facilities | Micro-level targeting, accessibility |
| **Market-level** | Food prices, weather conditions | Price monitoring, supply chain |
| **Commodity-level** | 47 food commodities, consumption patterns | Product-specific analysis |

### Key Variables Available

**Economic Indicators:**
- Inflation (national & Jakarta, MoM/YoY/YTD)
- Consumer Price Index (national & Jakarta)
- Consumer Confidence Index
- Retail Sales Growth
- Food Inflation

**Demographic & Social:**
- Population density (267 kelurahan)
- Poverty indicators (SKTM recipients)
- Income sources by area

**Consumption Patterns:**
- Household expenditure by region
- Food vs non-food spending by income group
- Consumption of 19 key commodities
- Expenditure on 11 commodity groups

**Infrastructure:**
- Market facilities (permanent, semi-permanent)
- Retail shops and grocery stores
- Geographic coverage (218 kelurahan with retail)

**Food Prices:**
- **Daily Historical Series (Jan '24 - Nov '25)**
- 47 commodities across 55 markets
- Price trends (current, previous, avg, min, max)
- Geographic coordinates for spatial analysis

**Weather:**
- **5 Years Historical Data (Nov 2020 - Nov 2025)** - matching PIHPS date range
- Temperature (min, max, mean) daily
- Precipitation and rain daily
- Wind speed and gusts
- 12 locations (DKI Jakarta + Jawa Barat)
- 21,900 daily observations

## Potential Use Cases

### 1. Food Price Prediction
**Datasets:** InfoPangan prices + Weather + Economic indicators + BPS consumption
**Features:**
- Historical prices, weather conditions
- Inflation rates, consumer confidence
- Seasonal patterns, consumption trends
- Market infrastructure accessibility

### 2. Demand Forecasting
**Datasets:** BPS consumption patterns + Population density + Economic indicators
**Features:**
- Consumption rates by commodity
- Population distribution
- Income levels (expenditure data)
- Economic trends

### 3. Market Accessibility Analysis
**Datasets:** BPS infrastructure + Population density + Food prices
**Features:**
- Market distribution by kelurahan
- Population density patterns
- Price variations by location
- Infrastructure gaps

### 4. Poverty & Food Security
**Datasets:** SKTM recipients + Food prices + Expenditure patterns
**Features:**
- Poverty distribution (243 kelurahan affected)
- Food expenditure share (39.66% avg)
- Price affordability by region
- Essential commodity costs

### 5. Regional Price Disparity
**Datasets:** Food prices + BPS expenditure by region + Infrastructure
**Features:**
- Price variations across 6 regions
- Expenditure patterns by area
- Market infrastructure differences
- Economic specialization

### 6. Weather Impact on Prices
**Datasets:** Weather data + Food prices (time series)
**Features:**
- Temperature effects on perishables
- Precipitation impact on supply
- Seasonal patterns
- Geographic price variations

### 7. Supply Chain Infrastructure Analysis (NEW!)
**Datasets:** Supply Chain Spatial + PIHPS Prices + BPS Infrastructure
**Features:**
- Distance to production facilities vs price correlation
- Infrastructure gap identification (high price + no nearby production)
- Supply chain completeness by location (production → distribution → retail)
- Facility density impact on price stability
- Optimization opportunities: where to build new facilities

**Key Questions:**
- Do locations closer to production facilities have lower prices?
- Which locations lack critical supply chain infrastructure?
- Is there correlation between retail density and price competition?
- Can we predict price based on distance to nearest production/distribution?

## Data Quality Notes

✅ **Strengths:**
- **Rich Historical Data:** Daily food prices from Nov 2020 to Nov 2025 (5 years from PIHPS)
- **Complete Weather Data:** 5 years of daily weather observations matching PIHPS period
- **Supply Chain Mapping:** 17,344 facilities mapped from production to retail (OpenStreetMap)
- **Spatial Analysis Ready:** Geographic coordinates for all facilities and markets
- Comprehensive coverage (national to market level)
- Multiple data sources (government, APIs, BPS, OpenStreetMap)
- Rich demographic and economic context
- Weather-price alignment for time series analysis
- Distance-based features for spatial price analysis

⚠️ **Limitations:**
- Poverty data outdated (2006-2012)
- BPS data limited to 2023-2024
- Some kelurahan-level data aggregated
- InfoPangan historical data only ~2 years (Jan 2024 - Nov 2025)

📊 **Recommended Next Steps:**
1. ✅ ~~Scrape historical weather data~~ - **COMPLETED** (5 years matching PIHPS)
2. ✅ ~~Map supply chain facilities~~ - **COMPLETED** (17,344 facilities from OpenStreetMap)
3. **Merge spatial features with PIHPS price data** for correlation analysis
4. **Analyze distance-to-facility impact on prices** (production, distribution, retail)
5. **Identify infrastructure gaps**: locations with high prices but no nearby facilities
6. Perform correlation analysis between weather anomalies and price spikes
7. Update poverty statistics with newer sources if available
8. Build spatial regression model: `price ~ distance_to_production + distance_to_distribution + weather + demographics`
