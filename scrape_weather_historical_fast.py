"""
Script untuk mengambil data cuaca historis dengan multiprocessing
Berdasarkan tanggal dari data InfoPangan historis
"""

import pandas as pd
from datetime import datetime
import requests
from multiprocessing import Pool, cpu_count
from tqdm import tqdm
import itertools
import time

def fetch_weather_for_date_market(args):
    """
    Worker function to fetch weather for one date-market combination
    Returns weather record or None
    """
    date_str, market = args

    lat = market['latitude']
    lon = market['longitude']
    market_id = market['market_id']
    market_name = market['market_name']
    city_name = market['city_name']

    # Skip if coordinates are missing
    if pd.isna(lat) or pd.isna(lon):
        return None

    # Open-Meteo API endpoint
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        'latitude': lat,
        'longitude': lon,
        'daily': [
            'temperature_2m_max',
            'temperature_2m_min',
            'temperature_2m_mean',
            'precipitation_sum',
            'rain_sum',
            'precipitation_hours',
            'windspeed_10m_max',
            'weathercode'
        ],
        'timezone': 'Asia/Jakarta',
        'start_date': date_str,
        'end_date': date_str
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if 'daily' in data and data['daily']:
            daily = data['daily']

            record = {
                'date': date_str,
                'market_id': market_id,
                'market_name': market_name,
                'city_name': city_name,
                'latitude': lat,
                'longitude': lon,
                'temperature_max_c': daily['temperature_2m_max'][0] if daily.get('temperature_2m_max') else None,
                'temperature_min_c': daily['temperature_2m_min'][0] if daily.get('temperature_2m_min') else None,
                'temperature_mean_c': daily['temperature_2m_mean'][0] if daily.get('temperature_2m_mean') else None,
                'precipitation_mm': daily['precipitation_sum'][0] if daily.get('precipitation_sum') else None,
                'rain_mm': daily['rain_sum'][0] if daily.get('rain_sum') else None,
                'precipitation_hours': daily['precipitation_hours'][0] if daily.get('precipitation_hours') else None,
                'windspeed_max_kmh': daily['windspeed_10m_max'][0] if daily.get('windspeed_10m_max') else None,
                'weather_code': daily['weathercode'][0] if daily.get('weathercode') else None
            }

            return record
        else:
            return None

    except Exception as e:
        # Return None on error
        return None

def main():
    print("="*80)
    print("SCRAPING HISTORICAL WEATHER DATA (MULTIPROCESSING)")
    print("="*80)

    # Read InfoPangan historical data
    print("\n[1] Reading InfoPangan historical data...")
    df_infopangan = pd.read_csv("infopangan_historical_20251127_202417.csv")

    # Get unique dates
    unique_dates = sorted(df_infopangan['date'].unique())
    print(f"  [OK] Found {len(unique_dates)} unique dates")
    print(f"  Date range: {unique_dates[0]} to {unique_dates[-1]}")

    # Get unique markets
    markets = df_infopangan[['market_id', 'market_name', 'city_name', 'latitude', 'longitude']].drop_duplicates()
    markets = markets.dropna(subset=['latitude', 'longitude'])
    print(f"  [OK] Found {len(markets)} markets with coordinates")

    # Create tasks (date, market) combinations
    tasks = list(itertools.product(unique_dates, markets.to_dict('records')))
    total_tasks = len(tasks)

    print(f"\n[2] Multiprocessing setup:")
    print(f"  Total tasks: {total_tasks:,}")
    print(f"  CPU cores: {cpu_count()}")
    print(f"  Using {cpu_count()} workers")
    print(f"  Estimated time: ~{(total_tasks * 0.05) / 60:.1f} minutes")

    # Run multiprocessing with progress bar
    print(f"\n[3] Fetching weather data with {cpu_count()} parallel workers...")
    print("  This will take a few minutes...\n")

    all_records = []

    with Pool(processes=cpu_count()) as pool:
        # Use imap_unordered for better performance with tqdm
        results = list(tqdm(
            pool.imap_unordered(fetch_weather_for_date_market, tasks),
            total=total_tasks,
            desc="Fetching weather",
            unit="task",
            ncols=80
        ))

        # Filter out None results
        all_records = [r for r in results if r is not None]

    # Create DataFrame
    print(f"\n[4] Creating DataFrame...")
    df = pd.DataFrame(all_records)

    if len(df) > 0:
        # Sort by date and market
        df = df.sort_values(['date', 'market_id'])

        print(f"  [OK] Total records: {len(df):,}")
        print(f"  Date range: {df['date'].min()} to {df['date'].max()}")
        print(f"  Unique dates: {df['date'].nunique()}")
        print(f"  Unique markets: {df['market_id'].nunique()}")
        print(f"  Success rate: {len(df) / total_tasks * 100:.1f}%")

        # Save to CSV
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f"weather_historical_{timestamp}.csv"

        df.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"\n  [OK] Saved to {output_file}")

        # Summary statistics
        print(f"\n[5] Summary:")
        print(f"  Total records: {len(df):,}")
        print(f"  Date range: {df['date'].min()} to {df['date'].max()}")
        print(f"  Markets: {df['market_id'].nunique()}")
        print(f"  Days with data: {df['date'].nunique()}")

        # Weather statistics
        print(f"\n[6] Weather statistics:")
        print(f"  Temperature (mean): {df['temperature_mean_c'].mean():.1f}°C")
        print(f"    Min: {df['temperature_mean_c'].min():.1f}°C")
        print(f"    Max: {df['temperature_mean_c'].max():.1f}°C")
        print(f"  Precipitation (average): {df['precipitation_mm'].mean():.1f}mm")
        print(f"  Days with rain: {(df['precipitation_mm'] > 0).sum():,}/{len(df):,} ({(df['precipitation_mm'] > 0).sum() / len(df) * 100:.1f}%)")

    else:
        print("  [WARN] No weather data collected!")

    print("\n" + "="*80)
    print("HISTORICAL WEATHER DATA SCRAPING COMPLETED!")
    print("="*80)

if __name__ == '__main__':
    main()
