"""
InfoPangan Jakarta API Client
==============================
Modular Python library untuk mengakses data harga pangan Jakarta.

Features:
    - Current prices: Get real-time commodity prices from markets
    - Statistics: Get monthly historical data with daily time series
    - DataFrame export: Convert data to pandas DataFrame for analysis
    - Multiple markets: Fetch data from multiple markets in one call

Usage - Current Prices:
    from infopangan import InfoPangan

    # Initialize client
    client = InfoPangan()

    # Get all markets
    markets = client.get_markets()

    # Get current commodity prices
    prices = client.get_prices(market_id=3)

    # Convert to DataFrame
    df = client.to_dataframe([3, 10, 21])

Usage - Statistics (Monthly Historical Data):
    from infopangan import InfoPangan

    client = InfoPangan()

    # Get monthly statistics for a market
    stats = client.get_statistics_by_market(3, "2025-11")

    # Get daily time series as DataFrame
    df = client.statistics_to_dataframe("market", 3, "2025-11", include_daily=True)

    # Get multiple months
    stats_range = client.get_statistics_range("market", 3, "2025-09", months=3)

Author: InfoPangan Scraper
Version: 2.0.0
"""

import requests
from typing import List, Dict, Optional, Union
from datetime import datetime, timedelta
import pandas as pd
import time


class InfoPangan:
    """
    Client untuk mengakses InfoPangan Jakarta API
    """

    BASE_URL = "https://infopangan.jakarta.go.id/api2"

    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json, text/plain, */*',
        'app-client-id': '6d608776a6b399ac767db6b0df8b864a18b1c1e9'
    }

    def __init__(self, timeout: int = 10):
        """
        Initialize InfoPangan client

        Args:
            timeout (int): Request timeout dalam detik (default: 10)
        """
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(self.HEADERS)

    def get_markets(self, search: Optional[str] = None) -> List[Dict]:
        """
        Ambil daftar pasar

        Args:
            search (str, optional): Keyword pencarian pasar

        Returns:
            List[Dict]: Daftar pasar dengan informasi lengkap

        Example:
            >>> client = InfoPangan()
            >>> markets = client.get_markets()
            >>> print(f"Total pasar: {len(markets)}")

            >>> # Search specific market
            >>> senen = client.get_markets(search="Senen")
            >>> print(senen[0]['market_name'])
        """
        url = f"{self.BASE_URL}/v1/master-data/market"
        params = {'search_text': search} if search else {}

        try:
            response = self.session.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
            return data.get('data', [])
        except requests.exceptions.RequestException as e:
            print(f"Error fetching markets: {e}")
            return []

    def get_market(self, market_id: int) -> Optional[Dict]:
        """
        Ambil detail satu pasar berdasarkan ID

        Args:
            market_id (int): ID pasar

        Returns:
            Dict: Detail pasar atau None jika tidak ditemukan

        Example:
            >>> client = InfoPangan()
            >>> market = client.get_market(3)
            >>> print(f"{market['market_name']} - {market['market_address']}")
        """
        markets = self.get_markets()
        for market in markets:
            if str(market.get('market_id')) == str(market_id):
                return market
        return None

    def get_prices(
        self,
        market_id: int = 0,
        date: Optional[str] = None
    ) -> Dict:
        """
        Ambil harga komoditas untuk pasar tertentu

        Args:
            market_id (int): ID pasar (0 untuk semua pasar, default: 0)
            date (str, optional): Tanggal dalam format YYYY-MM-DD
                                 Data tersedia mulai 2024-01-01
                                 Jika tidak diisi, akan return data hari ini

        Returns:
            Dict: Data harga komoditas dengan metadata

        Example:
            >>> client = InfoPangan()
            >>> # Get current prices
            >>> prices = client.get_prices(market_id=3)
            >>> print(f"Tanggal: {prices['selected_price_date']}")
            >>> print(f"Jumlah komoditas: {len(prices['data'])}")

            >>> # Get historical prices (available from 2024-01-01)
            >>> prices_aug = client.get_prices(market_id=3, date="2024-08-15")
            >>> print(f"Date: {prices_aug['selected_price_date']}")

            >>> # Get specific commodity
            >>> for commodity in prices['data']:
            ...     if 'Beras' in commodity['name']:
            ...         print(f"{commodity['name']}: Rp {commodity['newest_price']:,}")
        """
        url = f"{self.BASE_URL}/v2/public/master-data/commodity/markets/{market_id}"
        params = {'date': date} if date else {}

        try:
            response = self.session.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()

            if data.get('status') == 200:
                return data.get('data', {})
            else:
                print(f"API returned status: {data.get('status')}")
                return {}
        except requests.exceptions.RequestException as e:
            print(f"Error fetching prices for market {market_id}: {e}")
            return {}

    def get_prices_multiple(
        self,
        market_ids: List[int],
        delay: float = 1.0
    ) -> Dict[int, Dict]:
        """
        Ambil harga dari beberapa pasar sekaligus

        Args:
            market_ids (List[int]): Daftar ID pasar
            delay (float): Delay antar request dalam detik (default: 1.0)

        Returns:
            Dict[int, Dict]: Dictionary dengan market_id sebagai key

        Example:
            >>> client = InfoPangan()
            >>> results = client.get_prices_multiple([3, 10, 21])
            >>> for market_id, data in results.items():
            ...     print(f"Market {market_id}: {len(data['data'])} komoditas")
        """
        results = {}

        for idx, market_id in enumerate(market_ids):
            data = self.get_prices(market_id)
            if data:
                results[market_id] = data

            # Delay untuk rate limiting
            if idx < len(market_ids) - 1:
                time.sleep(delay)

        return results

    def get_prices_range(
        self,
        market_ids: List[int],
        start_date: str,
        end_date: Optional[str] = None,
        days: Optional[int] = None,
        delay: float = 1.0
    ) -> pd.DataFrame:
        """
        Ambil data harga historis untuk rentang tanggal

        Args:
            market_ids (List[int]): Daftar ID pasar
            start_date (str): Tanggal mulai YYYY-MM-DD (minimum: 2024-01-01)
            end_date (str, optional): Tanggal akhir YYYY-MM-DD
            days (int, optional): Jumlah hari dari start_date (alternatif end_date)
            delay (float): Delay antar request (default: 1.0)

        Returns:
            pd.DataFrame: DataFrame dengan data harga multiple hari

        Note:
            Data historis tersedia mulai 2024-01-01

        Example:
            >>> client = InfoPangan()
            >>> # Get range spesifik
            >>> df = client.get_prices_range([3, 10], "2024-08-01", "2024-08-07")

            >>> # Get 7 hari dari tanggal tertentu
            >>> df = client.get_prices_range([3, 10], "2024-08-15", days=7)

            >>> df.to_csv('prices.csv', index=False)
        """
        # Parse start date
        start = datetime.strptime(start_date, "%Y-%m-%d")

        # Determine end date
        if end_date:
            end = datetime.strptime(end_date, "%Y-%m-%d")
        elif days:
            end = start + timedelta(days=days - 1)
        else:
            end = start

        # Generate date list
        current = start
        date_list = []
        while current <= end:
            date_list.append(current.strftime("%Y-%m-%d"))
            current += timedelta(days=1)

        records = []

        # Fetch data for each date and market
        for idx, date_str in enumerate(date_list):
            for market_id in market_ids:
                prices = self.get_prices(market_id, date=date_str)

                if prices and 'data' in prices:
                    commodities = prices.get('data', [])

                    for commodity in commodities:
                        price = commodity.get('newest_price') or 0

                        records.append({
                            'date': date_str,
                            'market_id': market_id,
                            'commodity_id': commodity.get('commodity_id'),
                            'commodity_name': commodity.get('name'),
                            'unit': commodity.get('unit'),
                            'price': price,
                            'prev_price': commodity.get('prev_price'),
                            'status': commodity.get('status'),
                            'latest_update': commodity.get('latest_new_price_date')
                        })

            # Rate limiting after each date (not each market)
            if idx < len(date_list) - 1:
                time.sleep(delay)

        return pd.DataFrame(records)

    def to_dataframe(
        self,
        market_ids: Union[int, List[int]],
        include_market_info: bool = True
    ) -> pd.DataFrame:
        """
        Convert data harga ke pandas DataFrame

        Args:
            market_ids: Single market ID atau list of market IDs
            include_market_info: Include informasi pasar (default: True)

        Returns:
            pd.DataFrame: Data dalam format tabel

        Example:
            >>> client = InfoPangan()
            >>> df = client.to_dataframe([3, 10, 21])
            >>> print(df.columns)
            >>> df.to_excel('harga_pangan.xlsx', index=False)
        """
        if isinstance(market_ids, int):
            market_ids = [market_ids]

        # Get prices
        prices_data = self.get_prices_multiple(market_ids)

        records = []
        for market_id, data in prices_data.items():
            price_date = data.get('selected_price_date')
            commodities = data.get('data', [])

            for commodity in commodities:
                record = {
                    'market_id': market_id,
                    'price_date': price_date,
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

                # Add market info if requested
                if include_market_info:
                    market = self.get_market(market_id)
                    if market:
                        record.update({
                            'market_name': market.get('market_name'),
                            'market_address': market.get('market_address'),
                            'city_name': market.get('city_name'),
                            'latitude': market.get('market_latitude'),
                            'longitude': market.get('market_longitude')
                        })

                records.append(record)

        return pd.DataFrame(records)

    def get_statistics(
        self,
        filter_by: str,
        entity_id: int,
        year_month: str
    ) -> Dict:
        """
        Ambil data statistik bulanan untuk pasar, kota, atau komoditas

        Args:
            filter_by (str): Filter mode - "market", "city", atau "commodity"
            entity_id (int): ID entitas (market_id, city_id, atau commodity_id)
            year_month (str): Periode dalam format YYYY-MM (contoh: "2025-11")

        Returns:
            Dict: Data statistik dengan time series harian

        Example:
            >>> client = InfoPangan()
            >>> # Get statistics untuk Pasar Senen di November 2025
            >>> stats = client.get_statistics("market", 3, "2025-11")
            >>> print(f"Total commodities: {len(stats['data'])}")

            >>> # Get statistics untuk kota
            >>> stats = client.get_statistics("city", 31, "2025-11")

            >>> # Get statistics untuk komoditas tertentu
            >>> stats = client.get_statistics("commodity", 1, "2025-11")
        """
        if filter_by not in ["market", "city", "commodity"]:
            print(f"Invalid filter_by: {filter_by}. Must be 'market', 'city', or 'commodity'")
            return {}

        url = f"{self.BASE_URL}/v1/public/report"
        params = {
            'filterBy': filter_by,
            'Id': entity_id,
            'yearMonth': year_month
        }

        try:
            response = self.session.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()

            if data.get('status') == 200:
                return data.get('data', {})
            else:
                print(f"API returned status: {data.get('status')}")
                return {}
        except requests.exceptions.RequestException as e:
            print(f"Error fetching statistics: {e}")
            return {}

    def get_statistics_by_market(
        self,
        market_id: int,
        year_month: str
    ) -> Dict:
        """
        Ambil statistik bulanan untuk pasar tertentu

        Args:
            market_id (int): ID pasar
            year_month (str): Periode YYYY-MM

        Returns:
            Dict: Data statistik pasar

        Example:
            >>> client = InfoPangan()
            >>> stats = client.get_statistics_by_market(3, "2025-11")
        """
        return self.get_statistics("market", market_id, year_month)

    def get_statistics_by_city(
        self,
        city_id: int,
        year_month: str
    ) -> Dict:
        """
        Ambil statistik bulanan untuk kota tertentu

        Args:
            city_id (int): ID kota
            year_month (str): Periode YYYY-MM

        Returns:
            Dict: Data statistik kota

        Example:
            >>> client = InfoPangan()
            >>> stats = client.get_statistics_by_city(31, "2025-11")
        """
        return self.get_statistics("city", city_id, year_month)

    def get_statistics_by_commodity(
        self,
        commodity_id: int,
        year_month: str
    ) -> Dict:
        """
        Ambil statistik bulanan untuk komoditas tertentu

        Args:
            commodity_id (int): ID komoditas
            year_month (str): Periode YYYY-MM

        Returns:
            Dict: Data statistik komoditas

        Example:
            >>> client = InfoPangan()
            >>> stats = client.get_statistics_by_commodity(1, "2025-11")
        """
        return self.get_statistics("commodity", commodity_id, year_month)

    def get_statistics_range(
        self,
        filter_by: str,
        entity_id: int,
        start_month: str,
        end_month: Optional[str] = None,
        months: Optional[int] = None,
        delay: float = 1.0
    ) -> List[Dict]:
        """
        Ambil statistik untuk rentang beberapa bulan

        Args:
            filter_by (str): Filter mode - "market", "city", atau "commodity"
            entity_id (int): ID entitas
            start_month (str): Bulan awal YYYY-MM
            end_month (str, optional): Bulan akhir YYYY-MM
            months (int, optional): Jumlah bulan dari start_month (alternatif end_month)
            delay (float): Delay antar request dalam detik

        Returns:
            List[Dict]: List data statistik per bulan

        Example:
            >>> client = InfoPangan()
            >>> # Get 3 bulan terakhir
            >>> stats = client.get_statistics_range("market", 3, "2025-09", months=3)

            >>> # Get range spesifik
            >>> stats = client.get_statistics_range("market", 3, "2025-01", "2025-11")
        """
        # Parse start month
        start_date = datetime.strptime(start_month, "%Y-%m")

        # Determine end date
        if end_month:
            end_date = datetime.strptime(end_month, "%Y-%m")
        elif months:
            end_date = start_date + timedelta(days=30 * (months - 1))
        else:
            end_date = start_date

        # Generate month list
        current = start_date
        month_list = []
        while current <= end_date:
            month_list.append(current.strftime("%Y-%m"))
            # Move to next month
            if current.month == 12:
                current = current.replace(year=current.year + 1, month=1)
            else:
                current = current.replace(month=current.month + 1)

        # Fetch data for each month
        results = []
        for idx, month in enumerate(month_list):
            data = self.get_statistics(filter_by, entity_id, month)
            if data:
                results.append({
                    'year_month': month,
                    'filter_by': filter_by,
                    'entity_id': entity_id,
                    'data': data
                })

            # Rate limiting
            if idx < len(month_list) - 1:
                time.sleep(delay)

        return results

    def statistics_to_dataframe(
        self,
        filter_by: str,
        entity_id: int,
        year_month: str,
        include_daily: bool = False
    ) -> pd.DataFrame:
        """
        Convert data statistik ke pandas DataFrame

        Args:
            filter_by (str): Filter mode - "market", "city", atau "commodity"
            entity_id (int): ID entitas
            year_month (str): Periode YYYY-MM
            include_daily (bool): Include data harian dari recaps (default: False)

        Returns:
            pd.DataFrame: Data statistik dalam format tabel

        Example:
            >>> client = InfoPangan()
            >>> # Summary statistik (avg, max, min)
            >>> df = client.statistics_to_dataframe("market", 3, "2025-11")

            >>> # Include daily time series
            >>> df_daily = client.statistics_to_dataframe("market", 3, "2025-11", include_daily=True)
            >>> df_daily.to_csv('daily_prices.csv', index=False)
        """
        stats = self.get_statistics(filter_by, entity_id, year_month)

        if not stats or 'data' not in stats:
            return pd.DataFrame()

        records = []
        commodities = stats.get('data', [])

        for commodity in commodities:
            if include_daily:
                # Expand daily recaps
                recaps = commodity.get('recaps', [])
                for recap in recaps:
                    record = {
                        'filter_by': filter_by,
                        'entity_id': entity_id,
                        'year_month': year_month,
                        'date': recap.get('time'),
                        'commodity_id': commodity.get('commodity_id'),
                        'commodity_name': commodity.get('commodity_name'),
                        'price': recap.get('value'),
                        'avg_monthly': commodity.get('avg_value'),
                        'max_monthly': commodity.get('max_value'),
                        'min_monthly': commodity.get('min_value')
                    }
                    records.append(record)
            else:
                # Summary only
                record = {
                    'filter_by': filter_by,
                    'entity_id': entity_id,
                    'year_month': year_month,
                    'commodity_id': commodity.get('commodity_id'),
                    'commodity_name': commodity.get('commodity_name'),
                    'avg_value': commodity.get('avg_value'),
                    'max_value': commodity.get('max_value'),
                    'min_value': commodity.get('min_value'),
                    'data_points': len(commodity.get('recaps', []))
                }
                records.append(record)

        return pd.DataFrame(records)


# Convenience functions untuk quick access
def get_all_markets() -> List[Dict]:
    """Quick function to get all markets"""
    client = InfoPangan()
    return client.get_markets()


def get_market_prices(market_id: int) -> Dict:
    """Quick function to get prices for a market"""
    client = InfoPangan()
    return client.get_prices(market_id)


def search_market(keyword: str) -> List[Dict]:
    """Quick function to search markets"""
    client = InfoPangan()
    return client.get_markets(search=keyword)


def get_statistics(filter_by: str, entity_id: int, year_month: str) -> Dict:
    """Quick function to get statistics"""
    client = InfoPangan()
    return client.get_statistics(filter_by, entity_id, year_month)


def get_market_statistics(market_id: int, year_month: str) -> Dict:
    """Quick function to get market statistics"""
    client = InfoPangan()
    return client.get_statistics_by_market(market_id, year_month)


def get_city_statistics(city_id: int, year_month: str) -> Dict:
    """Quick function to get city statistics"""
    client = InfoPangan()
    return client.get_statistics_by_city(city_id, year_month)


def get_commodity_statistics(commodity_id: int, year_month: str) -> Dict:
    """Quick function to get commodity statistics"""
    client = InfoPangan()
    return client.get_statistics_by_commodity(commodity_id, year_month)


# Example usage
if __name__ == "__main__":
    print("="*70)
    print("InfoPangan API Client - Example Usage")
    print("="*70)

    # Initialize client
    client = InfoPangan()

    # Example 1: Get all markets
    print("\n[1] Getting all markets...")
    markets = client.get_markets()
    print(f"Total markets: {len(markets)}")
    print(f"First market: {markets[0]['market_name']}")

    # Example 2: Search market
    print("\n[2] Searching for 'Senen'...")
    results = client.get_markets(search="Senen")
    if results:
        print(f"Found: {results[0]['market_name']}")
        print(f"Address: {results[0]['market_address']}")
        print(f"Coordinates: {results[0]['market_latitude']}, {results[0]['market_longitude']}")

    # Example 3: Get prices for a market
    print("\n[3] Getting prices for Pasar Senen (ID: 3)...")
    prices = client.get_prices(market_id=3)
    if prices:
        print(f"Date: {prices['selected_price_date']}")
        print(f"Total commodities: {len(prices['data'])}")

        # Show top 5 expensive items
        print("\nTop 5 most expensive:")
        sorted_items = sorted(
            [c for c in prices['data'] if (c.get('newest_price') or 0) > 0],
            key=lambda x: (x.get('newest_price') or 0),
            reverse=True
        )[:5]

        for i, item in enumerate(sorted_items, 1):
            print(f"  {i}. {item['name']}: Rp {item['newest_price']:,}/{item['unit']}")

    # Example 4: Convert to DataFrame
    print("\n[4] Converting to DataFrame...")
    df = client.to_dataframe([3, 10, 21])
    print(f"DataFrame shape: {df.shape}")
    print(f"Columns: {', '.join(df.columns)}")

    # Save to CSV
    output_file = f"prices_{datetime.now().strftime('%Y%m%d')}.csv"
    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"\nData saved to: {output_file}")

    # Example 5: Get statistics (monthly time series)
    print("\n[5] Getting statistics for Pasar Senen (November 2025)...")
    stats = client.get_statistics_by_market(3, "2025-11")
    if stats and 'data' in stats:
        print(f"Total commodities: {len(stats['data'])}")

        # Show sample commodity with daily data
        if stats['data']:
            sample = stats['data'][0]
            print(f"\nSample commodity: {sample.get('commodity_name')}")
            print(f"  Average: Rp {sample.get('avg_value'):,}")
            print(f"  Max: Rp {sample.get('max_value'):,}")
            print(f"  Min: Rp {sample.get('min_value'):,}")
            print(f"  Daily data points: {len(sample.get('recaps', []))}")

    # Example 6: Convert statistics to DataFrame
    print("\n[6] Converting statistics to DataFrame (with daily data)...")
    df_stats = client.statistics_to_dataframe("market", 3, "2025-11", include_daily=True)
    if not df_stats.empty:
        print(f"DataFrame shape: {df_stats.shape}")
        print(f"Date range: {df_stats['date'].min()} to {df_stats['date'].max()}")

        # Save to CSV
        stats_file = f"statistics_daily_{datetime.now().strftime('%Y%m%d')}.csv"
        df_stats.to_csv(stats_file, index=False, encoding='utf-8-sig')
        print(f"Statistics data saved to: {stats_file}")

    print("\n" + "="*70)
    print("Done!")
    print("="*70)
