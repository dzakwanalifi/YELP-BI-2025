"""
Script untuk mengambil data historis InfoPangan secara efisien
Menggunakan API statistics yang punya data harian untuk tiap bulan
"""

import pandas as pd
from datetime import datetime
from infopangan import InfoPangan
import time

print("="*80)
print("SCRAPING HISTORICAL INFOPANGAN DATA (EFFICIENT METHOD)")
print("="*80)

# Initialize client
client = InfoPangan()

# Get all markets
print("\n[1] Getting all markets...")
markets = client.get_markets()
print(f"  [OK] Found {len(markets)} markets")

# Define month range (from 2024-01 to current month)
start_month = "2024-01"
end_month = datetime.now().strftime("%Y-%m")

print(f"\n[2] Month range: {start_month} to {end_month}")

# Generate month list
start_dt = datetime.strptime(start_month, "%Y-%m")
end_dt = datetime.strptime(end_month, "%Y-%m")

month_list = []
current = start_dt
while current <= end_dt:
    month_list.append(current.strftime("%Y-%m"))
    if current.month == 12:
        current = current.replace(year=current.year + 1, month=1)
    else:
        current = current.replace(month=current.month + 1)

print(f"  Total months: {len(month_list)}")
print(f"  Months: {', '.join(month_list)}")
print(f"  Total requests: {len(markets)} markets x {len(month_list)} months = {len(markets) * len(month_list)}")
print(f"  Estimated time: ~{(len(markets) * len(month_list) * 1) / 60:.1f} minutes (with 1s delay)")

# Confirm
print("\n[WARNING] This will make {0} API requests!".format(len(markets) * len(month_list)))
print("Press Ctrl+C within 5 seconds to cancel...")
time.sleep(5)

print("\n[3] Fetching historical data using statistics API...")

all_records = []
errors = []

# Iterate through each month
for month_idx, year_month in enumerate(month_list, 1):
    print(f"\n  Month {month_idx}/{len(month_list)}: {year_month}")

    # Fetch statistics for all markets in this month
    for market_idx, market in enumerate(markets, 1):
        market_id = int(market['market_id'])
        market_name = market['market_name']

        try:
            stats = client.get_statistics_by_market(market_id, year_month)

            if stats and 'data' in stats:
                commodities = stats.get('data', [])

                for commodity in commodities:
                    # Get daily data from recaps
                    recaps = commodity.get('recaps', [])

                    for recap in recaps:
                        record = {
                            'date': recap.get('time'),
                            'market_id': market_id,
                            'market_name': market_name,
                            'market_address': market.get('market_address'),
                            'city_name': market.get('city_name'),
                            'latitude': market.get('market_latitude'),
                            'longitude': market.get('market_longitude'),
                            'commodity_id': commodity.get('commodity_id'),
                            'commodity_name': commodity.get('commodity_name'),
                            'price': recap.get('value'),
                            'avg_monthly': commodity.get('avg_value'),
                            'max_monthly': commodity.get('max_value'),
                            'min_monthly': commodity.get('min_value')
                        }
                        all_records.append(record)

                if market_idx % 10 == 0:
                    print(f"    Progress: {market_idx}/{len(markets)} markets, {len(all_records):,} records")

            # Rate limiting
            time.sleep(1)

        except Exception as e:
            error_msg = f"Month: {year_month}, Market: {market_id} ({market_name}), Error: {str(e)}"
            errors.append(error_msg)
            print(f"    [ERROR] Market {market_id}: {str(e)[:50]}")

    print(f"    [OK] Completed {year_month}: {len(all_records):,} total records")

# Create DataFrame
print("\n[4] Creating DataFrame...")
df = pd.DataFrame(all_records)

if len(df) > 0:
    # Sort by date and market
    df = df.sort_values(['date', 'market_id', 'commodity_id'])

    print(f"  [OK] Total records: {len(df):,}")
    print(f"  Date range: {df['date'].min()} to {df['date'].max()}")
    print(f"  Unique dates: {df['date'].nunique()}")
    print(f"  Unique markets: {df['market_id'].nunique()}")
    print(f"  Unique commodities: {df['commodity_id'].nunique()}")

    # Save to CSV
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = f"infopangan_historical_{timestamp}.csv"

    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"\n  [OK] Saved to {output_file}")

    # Summary statistics
    print("\n[5] Summary:")
    print(f"  Total records: {len(df):,}")
    print(f"  Total errors: {len(errors)}")
    print(f"  Date range: {df['date'].min()} to {df['date'].max()}")
    print(f"  Markets: {df['market_id'].nunique()}")
    print(f"  Commodities: {df['commodity_id'].nunique()}")
    print(f"  Days with data: {df['date'].nunique()}")

    # Data completeness check
    print(f"\n[6] Data completeness:")
    records_per_date = df.groupby('date').size()
    print(f"  Average records per day: {records_per_date.mean():,.0f}")
    print(f"  Min records per day: {records_per_date.min():,}")
    print(f"  Max records per day: {records_per_date.max():,}")

    # Top commodities by average price
    avg_prices = df[df['price'] > 0].groupby('commodity_name')['price'].mean().sort_values(ascending=False)
    print(f"\n  Top 5 most expensive commodities (average):")
    for i, (commodity, price) in enumerate(avg_prices.head().items(), 1):
        print(f"    {i}. {commodity}: Rp {price:,.0f}")

else:
    print("  [WARN] No data collected!")

# Save errors if any
if errors:
    error_file = f"errors_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(error_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(errors))
    print(f"\n  Errors saved to {error_file}")

print("\n" + "="*80)
print("HISTORICAL DATA SCRAPING COMPLETED!")
print("="*80)
print(f"\nNext step: Run scrape_weather_data_historical.py to fetch weather for all dates")
