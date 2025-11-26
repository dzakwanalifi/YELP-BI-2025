# InfoPangan Jakarta API Client

Python library untuk mengakses data harga pangan Jakarta dari InfoPangan API.

## 📦 Instalasi

```bash
pip install -r requirements.txt
```

## 🚀 Quick Start

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

# Get prices for a market
prices = client.get_prices(market_id=3)
print(f"Tanggal: {prices['selected_price_date']}")
print(f"Komoditas: {len(prices['data'])}")

# Get prices from multiple markets
results = client.get_prices_multiple([3, 10, 21])

# Convert to DataFrame
df = client.to_dataframe([3, 10, 21], include_market_info=True)
df.to_csv('prices.csv', index=False)
```

## 📖 Dokumentasi API

Lihat [API_DOCUMENTATION.md](API_DOCUMENTATION.md) untuk dokumentasi lengkap endpoint API.

## 🔧 Class Methods

### `InfoPangan(timeout=10)`

Main client class.

**Methods:**

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

#### `get_prices_range(market_ids, days=7, delay=1.0) -> pd.DataFrame`
Generate data range untuk beberapa hari.

```python
df = client.get_prices_range([3, 10, 21], days=7)
```

#### `to_dataframe(market_ids, include_market_info=True) -> pd.DataFrame`
Convert data ke pandas DataFrame.

```python
df = client.to_dataframe([3, 10, 21])
df.to_excel('prices.xlsx', index=False)
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

## 🌐 Convenience Functions

Untuk akses cepat tanpa inisialisasi class:

```python
from infopangan import get_all_markets, get_market_prices, search_market

# Get all markets
markets = get_all_markets()

# Get prices
prices = get_market_prices(market_id=3)

# Search
results = search_market("Senen")
```

## 📝 Notes

- API hanya menyediakan data **hari ini**
- Untuk data historis, jalankan script secara terjadwal (cron job)
- Default timeout: 10 detik
- Recommended delay antar request: 1-2 detik
- Semua koordinat GPS tersedia (latitude & longitude)

## 📂 File Structure

```
.
├── infopangan.py           # Main module
├── API_DOCUMENTATION.md    # API docs
├── requirements.txt        # Dependencies
└── README.md              # This file
```

## 🔗 Links

- Website: https://infopangan.jakarta.go.id
- API Base URL: https://infopangan.jakarta.go.id/api2

## 📄 License

MIT License - Free to use for research and commercial purposes.
