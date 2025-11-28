"""
Script untuk mengambil data historis InfoPangan dengan multiprocessing
Menggunakan semua CPU cores untuk scraping paralel
"""

import pandas as pd
from datetime import datetime
from infopangan import InfoPangan
from multiprocessing import Pool, cpu_count
from tqdm import tqdm
import itertools

def fetch_market_month_data(args):
    """
    Worker function to fetch data for one market-month combination
    Returns list of records
    """
    market, year_month = args
    market_id = int(market['market_id'])
    market_name = market['market_name']

    # Each worker creates its own client
    client = InfoPangan()
    records = []

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
                    records.append(record)

        return records

    except Exception as e:
        # Return empty list on error
        return []

def main():
    print("="*80)
    print("SCRAPING HISTORICAL INFOPANGAN DATA (MULTIPROCESSING)")
    print("="*80)

    # Initialize client to get markets (main thread)
    client = InfoPangan(timeout=30)

    # Get all markets - try API first, fallback to cache
    print("\n[1] Getting all markets...")
    markets = client.get_markets()

    if not markets:
        print("  [WARN] API failed, trying cache...")
        import json
        try:
            with open('markets_cache.json', 'r', encoding='utf-8') as f:
                markets = json.load(f)
            print(f"  [OK] Loaded {len(markets)} markets from cache")
        except Exception as e:
            print(f"  [ERROR] Could not load cache: {e}")
            return
    else:
        print(f"  [OK] Found {len(markets)} markets from API")

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

    # Create tasks (market, month) combinations
    tasks = list(itertools.product(markets, month_list))
    total_tasks = len(tasks)

    print(f"\n[3] Multiprocessing setup:")
    print(f"  Total tasks: {total_tasks}")
    print(f"  CPU cores: {cpu_count()}")
    print(f"  Using {cpu_count()} workers")

    # Run multiprocessing with progress bar
    print(f"\n[4] Fetching data with {cpu_count()} parallel workers...")
    print("  This will be much faster!\n")

    all_records = []

    with Pool(processes=cpu_count()) as pool:
        # Use imap_unordered for better performance with tqdm
        results = list(tqdm(
            pool.imap_unordered(fetch_market_month_data, tasks),
            total=total_tasks,
            desc="Fetching data",
            unit="task",
            ncols=80
        ))

        # Flatten results
        for result in results:
            all_records.extend(result)

    # Create DataFrame
    print("\n[5] Creating DataFrame...")
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
        print("\n[6] Summary:")
        print(f"  Total records: {len(df):,}")
        print(f"  Date range: {df['date'].min()} to {df['date'].max()}")
        print(f"  Markets: {df['market_id'].nunique()}")
        print(f"  Commodities: {df['commodity_id'].nunique()}")
        print(f"  Days with data: {df['date'].nunique()}")

        # Data completeness check
        print(f"\n[7] Data completeness:")
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

    print("\n" + "="*80)
    print("HISTORICAL DATA SCRAPING COMPLETED!")
    print("="*80)

if __name__ == '__main__':
    main()
