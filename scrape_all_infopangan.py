"""
Script untuk mengambil SEMUA data dari InfoPangan API
Mengambil data dari semua pasar dan semua komoditas
Output: 1 CSV lengkap dengan data pasar, komoditas, dan harga
"""

import pandas as pd
from infopangan import InfoPangan
from datetime import datetime
import time

def scrape_all_data():
    """
    Scrape semua data dari InfoPangan API untuk semua pasar
    """
    print("="*80)
    print("SCRAPING ALL DATA FROM INFOPANGAN API")
    print("="*80)

    # Initialize client
    client = InfoPangan()

    # Step 1: Get all markets
    print("\n[1/3] Fetching all markets...")
    markets = client.get_markets()
    print(f"[OK] Found {len(markets)} markets")

    # Display market list
    print("\nMarket List:")
    for i, market in enumerate(markets, 1):
        mid = int(market['market_id'])
        print(f"  {i:2d}. [{mid:3d}] {market['market_name']} - {market['city_name']}")

    # Step 2: Get prices for all markets
    print(f"\n[2/3] Fetching prices for all {len(markets)} markets...")
    print("This may take a while due to rate limiting...")

    all_records = []
    total_markets = len(markets)

    for idx, market in enumerate(markets, 1):
        market_id = market['market_id']
        market_name = market['market_name']

        print(f"  [{idx}/{total_markets}] Processing {market_name} (ID: {market_id})...", end='')

        # Get prices for this market
        prices_data = client.get_prices(market_id)

        if prices_data and 'data' in prices_data:
            price_date = prices_data.get('selected_price_date')
            commodities = prices_data.get('data', [])

            print(f" {len(commodities)} commodities")

            # Add each commodity as a record
            for commodity in commodities:
                record = {
                    # Market Info
                    'market_id': market_id,
                    'market_name': market['market_name'],
                    'market_address': market['market_address'],
                    'city_id': market.get('city_id'),
                    'city_name': market.get('city_name'),
                    'province_id': market.get('province_id'),
                    'province_name': market.get('province_name'),
                    'latitude': market.get('market_latitude'),
                    'longitude': market.get('market_longitude'),

                    # Price Date
                    'price_date': price_date,

                    # Commodity Info
                    'commodity_id': commodity.get('commodity_id'),
                    'commodity_name': commodity.get('name'),
                    'unit': commodity.get('unit'),

                    # Price Info
                    'newest_price': commodity.get('newest_price'),
                    'prev_price': commodity.get('prev_price'),
                    'highest_price': commodity.get('highest_price'),
                    'lowest_price': commodity.get('lowest_price'),
                    'avg_price': commodity.get('avg_price'),

                    # Status
                    'status': commodity.get('status'),
                    'latest_update': commodity.get('latest_new_price_date')
                }

                all_records.append(record)
        else:
            print(" No data")

        # Rate limiting: 1 second delay between requests
        if idx < total_markets:
            time.sleep(1)

    # Step 3: Create DataFrame and save to CSV
    print(f"\n[3/3] Creating DataFrame...")
    df = pd.DataFrame(all_records)

    print(f"[OK] Created DataFrame with {len(df)} rows and {len(df.columns)} columns")
    print(f"\nDataFrame Info:")
    print(f"  Total records: {len(df):,}")
    print(f"  Unique markets: {df['market_id'].nunique()}")
    print(f"  Unique commodities: {df['commodity_id'].nunique()}")
    print(f"  Unique cities: {df['city_name'].nunique()}")

    # Save to CSV
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"infopangan_complete_data_{timestamp}.csv"

    print(f"\n[SAVING] Saving to {filename}...")
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f"[OK] Data saved successfully!")

    # Display sample data
    print("\n" + "="*80)
    print("SAMPLE DATA (First 10 rows)")
    print("="*80)
    print(df.head(10).to_string())

    # Summary statistics
    print("\n" + "="*80)
    print("SUMMARY STATISTICS")
    print("="*80)

    print("\nBy Market:")
    market_summary = df.groupby(['market_name', 'city_name']).agg({
        'commodity_id': 'count',
        'newest_price': 'mean'
    }).round(2)
    market_summary.columns = ['Total Commodities', 'Avg Price']
    print(market_summary)

    print("\nTop 10 Most Expensive Commodities:")
    expensive = df.nlargest(10, 'newest_price')[['commodity_name', 'unit', 'newest_price', 'market_name']]
    print(expensive.to_string(index=False))

    print("\nTop 10 Cheapest Commodities:")
    cheap = df[df['newest_price'] > 0].nsmallest(10, 'newest_price')[['commodity_name', 'unit', 'newest_price', 'market_name']]
    print(cheap.to_string(index=False))

    print("\n" + "="*80)
    print("SCRAPING COMPLETED!")
    print("="*80)
    print(f"Output file: {filename}")
    print(f"Total records: {len(df):,}")
    print("="*80)

    return df, filename


if __name__ == "__main__":
    # Run the scraper
    df, filename = scrape_all_data()
