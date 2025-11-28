"""
Script untuk mengambil data cuaca berdasarkan koordinat dari InfoPangan CSV
Menggunakan Open-Meteo API (free, no auth required)
"""

import pandas as pd
import requests
import time
from datetime import datetime

print("="*80)
print("FETCHING WEATHER DATA FOR INFOPANGAN MARKETS")
print("="*80)

# Read InfoPangan data
print("\n[1] Reading InfoPangan data...")
df = pd.read_csv("infopangan_complete_data_20251127_144533.csv")

# Get unique markets with coordinates
markets = df[['market_id', 'market_name', 'city_name', 'latitude', 'longitude']].drop_duplicates()
print(f"  [OK] Found {len(markets)} unique markets")

# Get unique dates
dates = df['price_date'].unique()
print(f"  [OK] Found {len(dates)} unique date(s): {dates}")

# Prepare weather data collection
weather_records = []

print("\n[2] Fetching weather data from Open-Meteo API...")
print(f"  Total requests: {len(markets)} markets x {len(dates)} dates = {len(markets) * len(dates)}")

for idx, (_, market) in enumerate(markets.iterrows(), 1):
    market_id = int(market['market_id'])
    market_name = market['market_name']
    lat = market['latitude']
    lon = market['longitude']
    city = market['city_name']

    # Skip if coordinates are missing
    if pd.isna(lat) or pd.isna(lon):
        print(f"  {idx:2d}. [SKIP] [{market_id:3d}] {market_name} - Missing coordinates")
        continue

    for date_str in dates:
        # Convert date string to datetime
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        date_formatted = date_obj.strftime('%Y-%m-%d')

        # Open-Meteo API endpoint for historical weather
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
            'start_date': date_formatted,
            'end_date': date_formatted
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if 'daily' in data and data['daily']:
                daily = data['daily']

                record = {
                    'date': date_formatted,
                    'market_id': market_id,
                    'market_name': market_name,
                    'city_name': city,
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

                weather_records.append(record)
                print(f"  {idx:2d}. [OK] [{market_id:3d}] {market_name[:40]:<40} | Temp: {record['temperature_mean_c']:.1f}C | Rain: {record['precipitation_mm']}mm")
            else:
                print(f"  {idx:2d}. [FAIL] [{market_id:3d}] {market_name} - No weather data in response")

        except requests.exceptions.RequestException as e:
            print(f"  {idx:2d}. [ERROR] [{market_id:3d}] {market_name} - {str(e)[:50]}")

        # Rate limiting - be nice to free API
        time.sleep(0.5)

# Create DataFrame and save to CSV
print("\n[3] Saving weather data to CSV...")
df_weather = pd.DataFrame(weather_records)

if len(df_weather) > 0:
    # Sort by date and market_id
    df_weather = df_weather.sort_values(['date', 'market_id'])

    # Generate filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = f"weather_data_{timestamp}.csv"

    df_weather.to_csv(output_file, index=False, encoding='utf-8-sig')

    print(f"  [OK] Saved to {output_file}")
    print(f"  Total records: {len(df_weather)}")
    print(f"\nSummary statistics:")
    print(f"  Temperature (mean): {df_weather['temperature_mean_c'].mean():.1f}C (min: {df_weather['temperature_mean_c'].min():.1f}C, max: {df_weather['temperature_mean_c'].max():.1f}C)")
    print(f"  Precipitation: {df_weather['precipitation_mm'].mean():.1f}mm average")
    print(f"  Records with rain: {(df_weather['precipitation_mm'] > 0).sum()}/{len(df_weather)}")
else:
    print("  [WARN] No weather data collected!")

print("\n" + "="*80)
print("WEATHER DATA COLLECTION COMPLETED!")
print("="*80)

# Weather code reference
print("\nWeather Code Reference:")
print("  0: Clear sky")
print("  1-3: Mainly clear, partly cloudy, overcast")
print("  45-48: Fog")
print("  51-57: Drizzle")
print("  61-67: Rain")
print("  71-77: Snow")
print("  80-82: Rain showers")
print("  95-99: Thunderstorm")
