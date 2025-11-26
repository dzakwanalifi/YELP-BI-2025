"""
InfoPangan Jakarta API Client
==============================
Modular Python library untuk mengakses data harga pangan Jakarta.

Usage:
    from infopangan import InfoPangan

    # Initialize client
    client = InfoPangan()

    # Get all markets
    markets = client.get_markets()

    # Get market by ID
    market = client.get_market(market_id=3)

    # Get commodity prices
    prices = client.get_prices(market_id=3)

    # Get prices for date range
    data = client.get_prices_range(
        market_ids=[3, 10, 21],
        days=7
    )

Author: InfoPangan Scraper
Version: 1.0.0
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
            date (str, optional): Tanggal dalam format YYYY-MM-DD (API selalu return data hari ini)

        Returns:
            Dict: Data harga komoditas dengan metadata

        Example:
            >>> client = InfoPangan()
            >>> prices = client.get_prices(market_id=3)
            >>> print(f"Tanggal: {prices['selected_price_date']}")
            >>> print(f"Jumlah komoditas: {len(prices['data'])}")

            >>> # Get specific commodity
            >>> for commodity in prices['data']:
            ...     if 'Beras' in commodity['name']:
            ...         print(f"{commodity['name']}: Rp {commodity['newest_price']:,}")
        """
        url = f"{self.BASE_URL}/v2/public/master-data/commodity/markets/{market_id}"

        try:
            response = self.session.get(url, timeout=self.timeout)
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
        days: int = 7,
        delay: float = 1.0
    ) -> pd.DataFrame:
        """
        Simulasi data harga untuk beberapa hari (karena API hanya return data hari ini)

        Args:
            market_ids (List[int]): Daftar ID pasar
            days (int): Jumlah hari (default: 7)
            delay (float): Delay antar request (default: 1.0)

        Returns:
            pd.DataFrame: DataFrame dengan data harga multiple hari

        Note:
            API InfoPangan hanya menyediakan data hari ini.
            Untuk data historis, jalankan script ini secara terjadwal.

        Example:
            >>> client = InfoPangan()
            >>> df = client.get_prices_range([3, 10, 21], days=7)
            >>> print(df.head())
            >>> df.to_csv('prices.csv', index=False)
        """
        # Ambil data hari ini
        today_data = self.get_prices_multiple(market_ids, delay)

        if not today_data:
            return pd.DataFrame()

        records = []

        # Generate data untuk setiap hari (hari ini saja karena API limitation)
        for day_offset in range(days):
            date = datetime.now() - timedelta(days=(days - 1 - day_offset))
            date_str = date.strftime("%Y-%m-%d")

            for market_id, market_data in today_data.items():
                commodities = market_data.get('data', [])

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

    print("\n" + "="*70)
    print("Done!")
    print("="*70)
