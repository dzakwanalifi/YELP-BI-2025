# InfoPangan Statistics API Guide

Quick guide untuk menggunakan statistics endpoint yang baru ditambahkan.

## Overview

Statistics endpoint menyediakan data **bulanan** dengan time series harian untuk:
- Pasar tertentu (filter by market)
- Kota tertentu (filter by city)
- Komoditas tertentu (filter by commodity)

## Quick Start

```python
from infopangan import InfoPangan

client = InfoPangan()

# Get statistics untuk Pasar Senen di November 2025
stats = client.get_statistics_by_market(3, "2025-11")

# Print summary
for commodity in stats['data']:
    print(f"{commodity['commodity_name']}")
    print(f"  Avg: Rp {commodity['avg_value']:,}")
    print(f"  Max: Rp {commodity['max_value']:,}")
    print(f"  Min: Rp {commodity['min_value']:,}")
```

## Response Structure

```json
{
  "data": [
    {
      "commodity_id": 1,
      "commodity_name": "Beras IR. I (IR 64)",
      "avg_value": 15882,
      "max_value": 16000,
      "min_value": 15000,
      "recaps": [
        {"value": 16000, "time": "2025-11-02"},
        {"value": 16000, "time": "2025-11-03"}
      ]
    }
  ]
}
```

## Methods Available

### 1. `get_statistics(filter_by, entity_id, year_month)`

Main method untuk mengambil statistik.

**Parameters:**
- `filter_by`: "market", "city", or "commodity"
- `entity_id`: ID dari entitas (market_id, city_id, atau commodity_id)
- `year_month`: Format "YYYY-MM" (contoh: "2025-11")

```python
# By market
stats = client.get_statistics("market", 3, "2025-11")

# By city
stats = client.get_statistics("city", 31, "2025-11")

# By commodity
stats = client.get_statistics("commodity", 1, "2025-11")
```

### 2. `get_statistics_by_market(market_id, year_month)`

Shortcut untuk statistik pasar.

```python
stats = client.get_statistics_by_market(3, "2025-11")
```

### 3. `get_statistics_by_city(city_id, year_month)`

Shortcut untuk statistik kota.

```python
stats = client.get_statistics_by_city(31, "2025-11")
```

### 4. `get_statistics_by_commodity(commodity_id, year_month)`

Shortcut untuk statistik komoditas.

```python
stats = client.get_statistics_by_commodity(1, "2025-11")
```

### 5. `get_statistics_range(filter_by, entity_id, start_month, end_month=None, months=None)`

Ambil statistik untuk beberapa bulan.

```python
# Get 3 bulan terakhir
stats = client.get_statistics_range(
    filter_by="market",
    entity_id=3,
    start_month="2025-09",
    months=3
)

# Get range spesifik
stats = client.get_statistics_range(
    filter_by="market",
    entity_id=3,
    start_month="2025-01",
    end_month="2025-11"
)
```

### 6. `statistics_to_dataframe(filter_by, entity_id, year_month, include_daily=False)`

Convert statistik ke pandas DataFrame.

**Parameters:**
- `include_daily`:
  - `False` = Summary only (avg, max, min per commodity)
  - `True` = Include daily time series data

```python
# Summary DataFrame
df = client.statistics_to_dataframe("market", 3, "2025-11")
# Columns: filter_by, entity_id, year_month, commodity_id, commodity_name,
#          avg_value, max_value, min_value, data_points

# Daily time series DataFrame
df_daily = client.statistics_to_dataframe("market", 3, "2025-11", include_daily=True)
# Columns: filter_by, entity_id, year_month, date, commodity_id, commodity_name,
#          price, avg_monthly, max_monthly, min_monthly
```

## Common Use Cases

### 1. Get Monthly Summary for a Market

```python
from infopangan import InfoPangan

client = InfoPangan()
df = client.statistics_to_dataframe("market", 3, "2025-11")

# Top 10 most expensive (by average)
top10 = df.nlargest(10, 'avg_value')[['commodity_name', 'avg_value']]
print(top10)

# Export to CSV
df.to_csv('monthly_summary.csv', index=False)
```

### 2. Get Daily Price Trends

```python
client = InfoPangan()
df = client.statistics_to_dataframe("market", 3, "2025-11", include_daily=True)

# Filter specific commodity
beras = df[df['commodity_name'].str.contains('Beras', case=False)]

# Plot trend (if matplotlib available)
import matplotlib.pyplot as plt
plt.plot(beras['date'], beras['price'])
plt.title('Beras Price Trend - November 2025')
plt.xticks(rotation=45)
plt.show()

# Export to CSV
beras.to_csv('beras_daily.csv', index=False)
```

### 3. Compare Multiple Markets

```python
client = InfoPangan()

markets = [3, 10, 21, 12]  # Senen, Mayestik, Tanah Abang, Kramat Jati
dfs = []

for market_id in markets:
    df = client.statistics_to_dataframe("market", market_id, "2025-11")
    dfs.append(df)

# Combine all
all_data = pd.concat(dfs, ignore_index=True)

# Compare average prices by market
market_names = {3: 'Senen', 10: 'Mayestik', 21: 'Tanah Abang', 12: 'Kramat Jati'}
all_data['market_name'] = all_data['entity_id'].map(market_names)

pivot = all_data.pivot_table(
    values='avg_value',
    index='commodity_name',
    columns='market_name',
    aggfunc='mean'
)

print(pivot)
```

### 4. Track Historical Trends (Multiple Months)

```python
client = InfoPangan()

# Get 6 months of data
stats_range = client.get_statistics_range(
    filter_by="market",
    entity_id=3,
    start_month="2025-06",
    months=6
)

# Extract specific commodity across months
beras_trend = []
for month_data in stats_range:
    for commodity in month_data['data']['data']:
        if 'Beras' in commodity['commodity_name']:
            beras_trend.append({
                'month': month_data['year_month'],
                'commodity': commodity['commodity_name'],
                'avg_price': commodity['avg_value']
            })

df_trend = pd.DataFrame(beras_trend)
print(df_trend)
```

### 5. Export to Excel with Multiple Sheets

```python
import pandas as pd
from datetime import datetime

client = InfoPangan()

# Get both summary and daily
df_summary = client.statistics_to_dataframe("market", 3, "2025-11")
df_daily = client.statistics_to_dataframe("market", 3, "2025-11", include_daily=True)

output = f"statistics_{datetime.now().strftime('%Y%m%d')}.xlsx"

with pd.ExcelWriter(output, engine='openpyxl') as writer:
    df_summary.to_excel(writer, sheet_name='Summary', index=False)
    df_daily.to_excel(writer, sheet_name='Daily Data', index=False)

    # Top 10
    top10 = df_summary.nlargest(10, 'avg_value')
    top10.to_excel(writer, sheet_name='Top 10', index=False)

print(f"Saved to {output}")
```

## Convenience Functions

Quick access tanpa class initialization:

```python
from infopangan import get_market_statistics, get_city_statistics, get_commodity_statistics

# Market statistics
stats = get_market_statistics(3, "2025-11")

# City statistics
stats = get_city_statistics(31, "2025-11")

# Commodity statistics
stats = get_commodity_statistics(1, "2025-11")
```

## Filter IDs Reference

### Market IDs
See [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for complete list. Common ones:
- 3: Pasar Senen
- 10: Pasar Mayestik
- 21: Pasar Tanah Abang
- 12: Pasar Kramat Jati

### City IDs
- 31: Jakarta Pusat
- 32: Jakarta Utara
- 73: Jakarta Barat
- 74: Jakarta Selatan
- 75: Jakarta Timur

### Commodity IDs
- 1: Beras IR. I (IR 64)
- 2: Beras IR. II (IR 64)
- ... (check API response for complete list)

## Notes

- Data tersedia per bulan (month granularity)
- Format `year_month`: "YYYY-MM"
- Response includes daily breakdown via `recaps` array
- Recommended delay antar request: 1-2 detik
- Data points vary by month (number of days data was recorded)

## Complete Examples

See `example_statistics.py` for comprehensive usage examples including:
- Market, city, and commodity filtering
- Multiple months retrieval
- DataFrame conversion and analysis
- Price trend analysis
- Excel export with multiple sheets

## API Endpoint

```
GET /api2/v1/public/report
Parameters:
  - filterBy: "market" | "city" | "commodity"
  - Id: entity_id (int)
  - yearMonth: "YYYY-MM"
```

For complete API documentation, see [API_DOCUMENTATION.md](API_DOCUMENTATION.md).
