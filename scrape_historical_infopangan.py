"""
Script untuk mengambil data historis harga pangan InfoPangan
Data tersedia mulai 2024-01-01
"""

import pandas as pd
from datetime import datetime, timedelta
from infopangan import InfoPangan
import time

print("="*80)
print("SCRAPING HISTORICAL INFOPANGAN DATA")
print("="*80)

# Initialize client
client = InfoPangan()

# Get all markets
print("\n[1] Getting all markets...")
markets = client.get_markets()
print(f"  [OK] Found {len(markets)} markets")

# Extract market IDs
market_ids = [int(m['market_id']) for m in markets]

# Define date range (from earliest available to today)
start_date = "2024-01-01"  # API data starts here
end_date = datetime.now().strftime("%Y-%m-%d")

print(f"\n[2] Date range: {start_date} to {end_date}")

# Calculate total days
start_dt = datetime.strptime(start_date, "%Y-%m-%d")
end_dt = datetime.strptime(end_date, "%Y-%m-%d")
total_days = (end_dt - start_dt).days + 1

print(f"  Total days: {total_days}")
print(f"  Total requests: {len(market_ids)} markets x {total_days} days = {len(market_ids) * total_days}")
print(f"  Estimated time: ~{(len(market_ids) * total_days * 1) / 60:.1f} minutes (with 1s delay)")

# Confirm
print("\n[WARNING] This will make many API requests!")
print("Press Ctrl+C within 5 seconds to cancel...")
time.sleep(5)

print("\n[3] Fetching historical data...")
print("  This may take a while...")

all_records = []
errors = []

# Iterate through each day
current_date = start_dt
day_count = 0

while current_date <= end_dt:
    day_count += 1
    date_str = current_date.strftime("%Y-%m-%d")

    print(f"\n  Day {day_count}/{total_days}: {date_str}")

    # Fetch data for all markets on this date
    for idx, market_id in enumerate(market_ids, 1):
        try:
            prices = client.get_prices(market_id, date=date_str)

            if prices and 'data' in prices:
                market = next((m for m in markets if int(m['market_id']) == market_id), None)

                commodities = prices.get('data', [])

                for commodity in commodities:
                    record = {
                        'date': date_str,
                        'market_id': market_id,
                        'market_name': market.get('market_name') if market else None,
                        'market_address': market.get('market_address') if market else None,
                        'city_name': market.get('city_name') if market else None,
                        'latitude': market.get('market_latitude') if market else None,
                        'longitude': market.get('market_longitude') if market else None,
                        'commodity_id': commodity.get('commodity_id'),
                        'commodity_name': commodity.get('name'),
                        'unit': commodity.get('unit'),
                        'newest_price': commodity.get('newest_price'),
                        'prev_price': commodity.get('prev_price'),
                        'highest_price': commodity.get('highest_price'),
                        'lowest_price': commodity.get('lowest_price'),
                        'avg_price': commodity.get('avg_price'),
                        'status': commodity.get('status'),
                        'latest_update': commodity.get('latest_new_price_date')
                    }
                    all_records.append(record)

                if idx % 10 == 0:
                    print(f"    Progress: {idx}/{len(market_ids)} markets, {len(all_records)} records")

            # Rate limiting
            time.sleep(1)

        except Exception as e:
            error_msg = f"Date: {date_str}, Market: {market_id}, Error: {str(e)}"
            errors.append(error_msg)
            print(f"    [ERROR] Market {market_id}: {str(e)[:50]}")

    print(f"    [OK] Completed {date_str}: {len(all_records)} total records")

    # Move to next day
    current_date += timedelta(days=1)

# Create DataFrame
print("\n[4] Creating DataFrame...")
df = pd.DataFrame(all_records)

if len(df) > 0:
    print(f"  [OK] Total records: {len(df)}")
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

    # Price statistics
    avg_prices = df[df['newest_price'] > 0].groupby('commodity_name')['newest_price'].mean().sort_values(ascending=False)
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
