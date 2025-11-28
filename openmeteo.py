"""
Open-Meteo Weather API Client
==============================
Modular Python library untuk mengakses data cuaca dari Open-Meteo API.

Features:
    - Historical weather: Get weather data for specific dates and locations
    - Multiple locations: Fetch data for multiple coordinates in one call
    - DataFrame export: Convert data to pandas DataFrame for analysis
    - Flexible date ranges: Get weather data for any date range

Usage:
    from openmeteo import OpenMeteo

    # Initialize client
    client = OpenMeteo()

    # Get weather data for single location
    weather = client.get_weather(
        latitude=-6.2088,
        longitude=106.8456,
        start_date="2024-01-01",
        end_date="2024-01-31"
    )

    # Get weather for multiple locations
    locations = [
        {"lat": -6.2088, "lon": 106.8456, "name": "Jakarta"},
        {"lat": -6.9175, "lon": 107.6191, "name": "Bandung"}
    ]
    df = client.get_weather_multiple(locations, "2024-01-01", "2024-01-31")

Author: Weather Data Scraper
Version: 1.0.0
"""

import requests
from typing import List, Dict, Optional, Union
from datetime import datetime, timedelta
import pandas as pd
import time


class OpenMeteo:
    """
    Client untuk mengakses Open-Meteo Weather API
    """

    BASE_URL = "https://archive-api.open-meteo.com/v1/archive"

    # Default weather variables to fetch
    DEFAULT_VARIABLES = [
        "temperature_2m_max",
        "temperature_2m_min",
        "temperature_2m_mean",
        "precipitation_sum",
        "rain_sum",
        "precipitation_hours",
        "wind_speed_10m_max",
        "wind_gusts_10m_max"
    ]

    def __init__(self, timeout: int = 30):
        """
        Initialize Open-Meteo client

        Args:
            timeout (int): Request timeout dalam detik (default: 30)
        """
        self.timeout = timeout
        self.session = requests.Session()

    def get_weather(
        self,
        latitude: float,
        longitude: float,
        start_date: str,
        end_date: Optional[str] = None,
        variables: Optional[List[str]] = None
    ) -> Dict:
        """
        Ambil data cuaca untuk satu lokasi

        Args:
            latitude (float): Latitude lokasi
            longitude (float): Longitude lokasi
            start_date (str): Tanggal mulai (YYYY-MM-DD)
            end_date (str, optional): Tanggal akhir (YYYY-MM-DD). Jika None, sama dengan start_date
            variables (List[str], optional): Variabel cuaca yang diambil. Jika None, gunakan default

        Returns:
            Dict: Data cuaca dengan metadata

        Example:
            >>> client = OpenMeteo()
            >>> weather = client.get_weather(-6.2088, 106.8456, "2024-01-01", "2024-01-31")
            >>> print(weather['daily']['time'])
        """
        if end_date is None:
            end_date = start_date

        if variables is None:
            variables = self.DEFAULT_VARIABLES

        params = {
            'latitude': latitude,
            'longitude': longitude,
            'start_date': start_date,
            'end_date': end_date,
            'daily': ','.join(variables),
            'timezone': 'Asia/Jakarta'
        }

        try:
            response = self.session.get(self.BASE_URL, params=params, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
            return data
        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather for {latitude},{longitude}: {e}")
            return {}

    def get_weather_multiple(
        self,
        locations: List[Dict],
        start_date: str,
        end_date: Optional[str] = None,
        variables: Optional[List[str]] = None,
        delay: float = 0.5
    ) -> pd.DataFrame:
        """
        Ambil data cuaca untuk beberapa lokasi sekaligus

        Args:
            locations (List[Dict]): List of locations dengan format:
                [{"lat": -6.2088, "lon": 106.8456, "name": "Jakarta"}, ...]
            start_date (str): Tanggal mulai (YYYY-MM-DD)
            end_date (str, optional): Tanggal akhir (YYYY-MM-DD)
            variables (List[str], optional): Variabel cuaca yang diambil
            delay (float): Delay antar request dalam detik (default: 0.5)

        Returns:
            pd.DataFrame: DataFrame dengan data cuaca semua lokasi

        Example:
            >>> client = OpenMeteo()
            >>> locations = [
            ...     {"lat": -6.2088, "lon": 106.8456, "name": "Jakarta"},
            ...     {"lat": -6.9175, "lon": 107.6191, "name": "Bandung"}
            ... ]
            >>> df = client.get_weather_multiple(locations, "2024-01-01", "2024-01-31")
            >>> df.to_csv('weather_data.csv', index=False)
        """
        records = []

        for idx, location in enumerate(locations):
            lat = location.get('lat')
            lon = location.get('lon')
            name = location.get('name', f"{lat},{lon}")

            weather = self.get_weather(lat, lon, start_date, end_date, variables)

            if weather and 'daily' in weather:
                daily = weather['daily']
                dates = daily.get('time', [])

                for date_idx, date in enumerate(dates):
                    record = {
                        'date': date,
                        'location_name': name,
                        'latitude': lat,
                        'longitude': lon
                    }

                    # Add all weather variables
                    for var in (variables or self.DEFAULT_VARIABLES):
                        if var in daily:
                            record[var] = daily[var][date_idx]

                    records.append(record)

            # Rate limiting
            if idx < len(locations) - 1:
                time.sleep(delay)

        return pd.DataFrame(records)

    def to_dataframe(
        self,
        latitude: float,
        longitude: float,
        start_date: str,
        end_date: Optional[str] = None,
        variables: Optional[List[str]] = None,
        location_name: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Convert data cuaca ke pandas DataFrame untuk satu lokasi

        Args:
            latitude (float): Latitude lokasi
            longitude (float): Longitude lokasi
            start_date (str): Tanggal mulai (YYYY-MM-DD)
            end_date (str, optional): Tanggal akhir (YYYY-MM-DD)
            variables (List[str], optional): Variabel cuaca yang diambil
            location_name (str, optional): Nama lokasi untuk kolom

        Returns:
            pd.DataFrame: Data dalam format tabel

        Example:
            >>> client = OpenMeteo()
            >>> df = client.to_dataframe(-6.2088, 106.8456, "2024-01-01", "2024-01-31", location_name="Jakarta")
            >>> df.to_excel('jakarta_weather.xlsx', index=False)
        """
        weather = self.get_weather(latitude, longitude, start_date, end_date, variables)

        if not weather or 'daily' not in weather:
            return pd.DataFrame()

        daily = weather['daily']
        dates = daily.get('time', [])

        records = []
        for date_idx, date in enumerate(dates):
            record = {
                'date': date,
                'location_name': location_name or f"{latitude},{longitude}",
                'latitude': latitude,
                'longitude': longitude
            }

            # Add all weather variables
            for var in (variables or self.DEFAULT_VARIABLES):
                if var in daily:
                    record[var] = daily[var][date_idx]

            records.append(record)

        return pd.DataFrame(records)


# Convenience functions untuk quick access
def get_weather(latitude: float, longitude: float, start_date: str, end_date: Optional[str] = None) -> Dict:
    """Quick function to get weather data"""
    client = OpenMeteo()
    return client.get_weather(latitude, longitude, start_date, end_date)


def get_weather_df(latitude: float, longitude: float, start_date: str, end_date: Optional[str] = None) -> pd.DataFrame:
    """Quick function to get weather data as DataFrame"""
    client = OpenMeteo()
    return client.to_dataframe(latitude, longitude, start_date, end_date)


# Example usage
if __name__ == "__main__":
    print("="*70)
    print("Open-Meteo Weather API Client - Example Usage")
    print("="*70)

    # Initialize client
    client = OpenMeteo()

    # Example 1: Get weather for single location
    print("\n[1] Getting weather for Jakarta...")
    weather = client.get_weather(
        latitude=-6.2088,
        longitude=106.8456,
        start_date="2024-01-01",
        end_date="2024-01-07"
    )

    if weather and 'daily' in weather:
        print(f"Date range: {weather['daily']['time'][0]} to {weather['daily']['time'][-1]}")
        print(f"Total days: {len(weather['daily']['time'])}")
        print(f"Variables: {', '.join(weather['daily'].keys())}")

    # Example 2: Convert to DataFrame for single location
    print("\n[2] Converting to DataFrame for Jakarta...")
    df = client.to_dataframe(
        latitude=-6.2088,
        longitude=106.8456,
        start_date="2024-01-01",
        end_date="2024-01-31",
        location_name="Jakarta"
    )

    if not df.empty:
        print(f"DataFrame shape: {df.shape}")
        print(f"Columns: {', '.join(df.columns)}")
        print("\nFirst 3 rows:")
        print(df.head(3))

    # Example 3: Get weather for multiple locations
    print("\n[3] Getting weather for multiple locations...")
    locations = [
        {"lat": -6.2088, "lon": 106.8456, "name": "Jakarta"},
        {"lat": -6.9175, "lon": 107.6191, "name": "Bandung"},
        {"lat": -7.7956, "lon": 110.3695, "name": "Yogyakarta"}
    ]

    df_multi = client.get_weather_multiple(
        locations=locations,
        start_date="2024-01-01",
        end_date="2024-01-07"
    )

    if not df_multi.empty:
        print(f"DataFrame shape: {df_multi.shape}")
        print(f"Locations: {df_multi['location_name'].unique().tolist()}")
        print(f"Date range: {df_multi['date'].min()} to {df_multi['date'].max()}")

        # Save to CSV
        output_file = f"weather_data_{datetime.now().strftime('%Y%m%d')}.csv"
        df_multi.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"\nData saved to: {output_file}")

    # Example 4: Weather summary by location
    print("\n[4] Weather summary by location...")
    if not df_multi.empty:
        summary = df_multi.groupby('location_name').agg({
            'temperature_2m_mean': 'mean',
            'precipitation_sum': 'sum',
            'rain_sum': 'sum'
        }).round(2)

        print(summary)

    print("\n" + "="*70)
    print("Done!")
    print("="*70)
