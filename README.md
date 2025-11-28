# InfoPangan Jakarta API Client

Python library untuk mengakses data harga pangan Jakarta dari InfoPangan API.

## 📦 Instalasi

```bash
pip install -r requirements.txt
```

## 🚀 Quick Start

### Current Prices

```python
from infopangan import InfoPangan

# Initialize client
client = InfoPangan()

# Get all markets
markets = client.get_markets()
print(f"Total pasar: {len(markets)}")

# Search specific market
senen = client.get_markets(search="Senen")
print(senen[0]['market_name'])

# Get current prices
prices = client.get_prices(market_id=3)
print(f"Tanggal: {prices['selected_price_date']}")
print(f"Komoditas: {len(prices['data'])}")

# Get historical prices (available from 2024-01-01)
prices_aug = client.get_prices(market_id=3, date="2024-08-15")
print(f"Historical date: {prices_aug['selected_price_date']}")

# Get price range for multiple days
df = client.get_prices_range([3, 10], "2024-08-01", "2024-08-07")
df.to_csv('prices_range.csv', index=False)

# Convert to DataFrame
df = client.to_dataframe([3, 10, 21], include_market_info=True)
df.to_csv('prices.csv', index=False)
```

### Historical Statistics

```python
from infopangan import InfoPangan

client = InfoPangan()

# Get monthly statistics (available from 2024-08)
stats = client.get_statistics_by_market(3, "2024-10")
print(f"Commodities: {len(stats['data'])}")

# Convert to DataFrame with daily time series
df = client.statistics_to_dataframe("market", 3, "2024-10", include_daily=True)
df.to_csv('statistics_daily.csv', index=False)

# Get multiple months
stats_range = client.get_statistics_range("market", 3, "2024-08", months=3)
print(f"Months fetched: {len(stats_range)}")
```

## 📖 Dokumentasi API

Lihat [API_DOCUMENTATION.md](API_DOCUMENTATION.md) untuk dokumentasi lengkap endpoint API.

## 🔧 Class Methods

### `InfoPangan(timeout=10)`

Main client class.

**Methods:**

### Price Methods (Current Data)

#### `get_markets(search=None) -> List[Dict]`
Ambil daftar pasar (opsional: dengan pencarian).

```python
# All markets
markets = client.get_markets()

# Search
results = client.get_markets(search="Tanah Abang")
```

#### `get_market(market_id) -> Dict`
Ambil detail satu pasar berdasarkan ID.

```python
market = client.get_market(3)
print(market['market_name'])
print(market['market_address'])
print(market['market_latitude'], market['market_longitude'])
```

#### `get_prices(market_id=0, date=None) -> Dict`
Ambil harga komoditas untuk pasar tertentu.

```python
# Specific market
prices = client.get_prices(market_id=3)

# All markets
all_prices = client.get_prices(market_id=0)
```

#### `get_prices_multiple(market_ids, delay=1.0) -> Dict[int, Dict]`
Ambil harga dari beberapa pasar sekaligus.

```python
results = client.get_prices_multiple([3, 10, 21, 12], delay=1.5)
```

#### `to_dataframe(market_ids, include_market_info=True) -> pd.DataFrame`
Convert data ke pandas DataFrame.

```python
df = client.to_dataframe([3, 10, 21])
df.to_excel('prices.xlsx', index=False)
```

### Statistics Methods (Historical Monthly Data)

#### `get_statistics(filter_by, entity_id, year_month) -> Dict`
Ambil data statistik bulanan dengan time series harian.

```python
# By market
stats = client.get_statistics("market", 3, "2025-11")

# By city
stats = client.get_statistics("city", 31, "2025-11")

# By commodity
stats = client.get_statistics("commodity", 1, "2025-11")
```

#### `get_statistics_by_market(market_id, year_month) -> Dict`
Shortcut untuk statistik pasar.

```python
stats = client.get_statistics_by_market(3, "2025-11")
print(f"Total commodities: {len(stats['data'])}")
```

#### `get_statistics_by_city(city_id, year_month) -> Dict`
Shortcut untuk statistik kota.

```python
stats = client.get_statistics_by_city(31, "2025-11")
```

#### `get_statistics_by_commodity(commodity_id, year_month) -> Dict`
Shortcut untuk statistik komoditas.

```python
stats = client.get_statistics_by_commodity(1, "2025-11")
```

#### `get_statistics_range(filter_by, entity_id, start_month, end_month=None, months=None, delay=1.0) -> List[Dict]`
Ambil statistik untuk rentang beberapa bulan.

```python
# Get 3 months
stats = client.get_statistics_range("market", 3, "2025-09", months=3)

# Get specific range
stats = client.get_statistics_range("market", 3, "2025-01", "2025-11")
```

#### `statistics_to_dataframe(filter_by, entity_id, year_month, include_daily=False) -> pd.DataFrame`
Convert statistik ke pandas DataFrame.

```python
# Summary (avg, max, min)
df = client.statistics_to_dataframe("market", 3, "2025-11")

# Include daily time series
df_daily = client.statistics_to_dataframe("market", 3, "2025-11", include_daily=True)
df_daily.to_csv('daily_prices.csv', index=False)
```

## 🏪 Market IDs

| Market ID | Nama Pasar | Wilayah |
|-----------|------------|---------|
| 3 | Pasar Senen | Jakarta Pusat |
| 8 | Pasar Glodok | Jakarta Barat |
| 10 | Pasar Mayestik | Jakarta Selatan |
| 12 | Pasar Kramat Jati | Jakarta Timur |
| 21 | Pasar Tanah Abang | Jakarta Pusat |

Lihat `API_DOCUMENTATION.md` untuk daftar lengkap.

## 📊 Contoh Penggunaan

### Export ke CSV

```python
from infopangan import InfoPangan

client = InfoPangan()
df = client.to_dataframe([3, 10, 21, 12])
df.to_csv('harga_pangan.csv', index=False, encoding='utf-8-sig')
```

### Export ke Excel

```python
df = client.to_dataframe([3, 10, 21])
df.to_excel('harga_pangan.xlsx', index=False)
```

### Analisis Harga

```python
import pandas as pd
from infopangan import InfoPangan

client = InfoPangan()
df = client.to_dataframe([3, 10, 21, 12])

# Filter komoditas tertentu
beras = df[df['commodity_name'].str.contains('Beras', case=False)]

# Hitung rata-rata per pasar
avg_by_market = beras.groupby('market_name')['newest_price'].mean()
print(avg_by_market)

# Top 10 termahal
top10 = df.nlargest(10, 'newest_price')[['commodity_name', 'newest_price', 'market_name']]
print(top10)
```

### Monitoring Harga

```python
from infopangan import InfoPangan

client = InfoPangan()

# Monitor harga cabe di beberapa pasar
df = client.to_dataframe([3, 10, 21])
cabe = df[df['commodity_name'].str.contains('Cabe', case=False)]

# Cek yang naik
rising = cabe[cabe['status'] == 'rise']
print(f"Komoditas naik: {len(rising)}")
print(rising[['commodity_name', 'market_name', 'newest_price', 'prev_price']])
```

## 📈 Statistics Usage Examples

### Get Monthly Statistics

```python
from infopangan import InfoPangan

client = InfoPangan()

# Get statistics untuk Pasar Senen di November 2025
stats = client.get_statistics_by_market(3, "2025-11")

# Data includes: avg_value, max_value, min_value, recaps (daily data)
for commodity in stats['data']:
    print(f"{commodity['commodity_name']}")
    print(f"  Average: Rp {commodity['avg_value']:,}")
    print(f"  Max: Rp {commodity['max_value']:,}")
    print(f"  Min: Rp {commodity['min_value']:,}")
    print(f"  Daily data points: {len(commodity['recaps'])}")
```

### Get Daily Time Series

```python
# Convert statistics to DataFrame with daily data
df = client.statistics_to_dataframe("market", 3, "2025-11", include_daily=True)

# Columns: filter_by, entity_id, year_month, date, commodity_id, commodity_name, price, avg_monthly, max_monthly, min_monthly
print(df.head())

# Filter specific commodity
beras = df[df['commodity_name'].str.contains('Beras', case=False)]
print(beras[['date', 'commodity_name', 'price']])
```

### Get Multiple Months

```python
# Get 3 months of statistics
stats_range = client.get_statistics_range(
    filter_by="market",
    entity_id=3,
    start_month="2025-09",
    months=3
)

for month_data in stats_range:
    print(f"{month_data['year_month']}: {len(month_data['data']['data'])} commodities")
```

## 🌐 Convenience Functions

Untuk akses cepat tanpa inisialisasi class:

```python
from infopangan import get_all_markets, get_market_prices, search_market
from infopangan import get_market_statistics, get_city_statistics

# Get all markets
markets = get_all_markets()

# Get current prices
prices = get_market_prices(market_id=3)

# Get statistics
stats = get_market_statistics(market_id=3, year_month="2025-11")

# Search
results = search_market("Senen")
```

## 📝 Notes

### Current Prices (get_prices)
- ✅ **Data historis tersedia mulai 1 Januari 2024**
- Mendukung parameter `date` untuk query historical data
- Format date: `YYYY-MM-DD`
- Continuous data dari 2024-01-01 hingga sekarang

### Statistics (get_statistics)
- ✅ **Data historis tersedia mulai 14 Agustus 2024**
- API menyediakan data **bulanan** dengan time series harian
- Format: `year_month="YYYY-MM"` (contoh: "2025-11")
- Response includes: avg_value, max_value, min_value, recaps (daily data)
- 3 filter modes: "market", "city", "commodity"
- ⚠️ Beberapa bulan memiliki gaps (Jan 2025, May 2025, Jun 2025)

### Data Availability
- **Prices**: 2024-01-01 s/d sekarang (continuous)
- **Statistics**: 2024-08-14 s/d sekarang (with gaps)
- Lihat [DATA_AVAILABILITY.md](DATA_AVAILABILITY.md) untuk detail lengkap

### General
- Default timeout: 10 detik
- Recommended delay antar request: 1-2 detik
- Semua koordinat GPS tersedia (latitude & longitude)

## 📂 File Structure

```
.
├── infopangan.py           # Main module
├── example_usage.py        # Usage examples (current prices)
├── example_statistics.py   # Usage examples (statistics)
├── API_DOCUMENTATION.md    # API endpoint documentation
├── DATA_AVAILABILITY.md    # Historical data availability guide
├── STATISTICS_GUIDE.md     # Complete statistics usage guide
├── requirements.txt        # Dependencies
└── README.md              # This file
```

## 🔗 Links

- Website: https://infopangan.jakarta.go.id
- API Base URL: https://infopangan.jakarta.go.id/api2

## 📄 License

MIT License - Free to use for research and commercial purposes.
