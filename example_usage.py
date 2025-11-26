"""
Example Usage - InfoPangan Module
==================================
Contoh penggunaan infopangan.py sebagai module di kode lain
"""

from infopangan import InfoPangan
import pandas as pd
from datetime import datetime

# ============================================================================
# EXAMPLE 1: Basic Usage - Get Market Data
# ============================================================================
def example_1_basic():
    print("\n" + "="*70)
    print("EXAMPLE 1: Basic Market Data")
    print("="*70)

    client = InfoPangan()

    # Get all markets
    markets = client.get_markets()
    print(f"Total pasar: {len(markets)}")

    # Search specific market
    results = client.get_markets(search="Tanah Abang")
    if results:
        market = results[0]
        print(f"\nPasar ditemukan:")
        print(f"  Nama: {market['market_name']}")
        print(f"  Alamat: {market['market_address']}")
        print(f"  Koordinat: {market['market_latitude']}, {market['market_longitude']}")


# ============================================================================
# EXAMPLE 2: Get Prices and Convert to DataFrame
# ============================================================================
def example_2_dataframe():
    print("\n" + "="*70)
    print("EXAMPLE 2: Convert to DataFrame")
    print("="*70)

    client = InfoPangan()

    # Get prices from multiple markets
    df = client.to_dataframe([3, 10, 21, 12], include_market_info=True)

    print(f"\nDataFrame Info:")
    print(f"  Shape: {df.shape}")
    print(f"  Columns: {len(df.columns)}")

    # Show sample
    print(f"\nSample data (5 rows):")
    print(df[['market_name', 'commodity_name', 'newest_price', 'unit']].head())

    # Save to CSV
    output = f"harga_pangan_{datetime.now().strftime('%Y%m%d')}.csv"
    df.to_csv(output, index=False, encoding='utf-8-sig')
    print(f"\nSaved to: {output}")

    return df


# ============================================================================
# EXAMPLE 3: Price Analysis
# ============================================================================
def example_3_analysis(df):
    print("\n" + "="*70)
    print("EXAMPLE 3: Price Analysis")
    print("="*70)

    # Top 10 most expensive
    print("\nTop 10 Komoditas Termahal:")
    top10 = df.nlargest(10, 'newest_price')[['commodity_name', 'newest_price', 'unit', 'market_name']]
    for idx, row in top10.iterrows():
        print(f"  {row['commodity_name']:40s} Rp {row['newest_price']:>10,} /{row['unit']}")

    # Average price by market
    print("\nHarga Rata-rata per Pasar:")
    avg_by_market = df.groupby('market_name')['newest_price'].mean().sort_values(ascending=False)
    for market, avg in avg_by_market.items():
        print(f"  {market:30s} Rp {avg:>10,.0f}")

    # Commodities that are rising
    rising = df[df['status'] == 'rise']
    print(f"\nKomoditas Naik Harga: {len(rising)}")
    if not rising.empty:
        print(rising[['commodity_name', 'market_name', 'newest_price', 'prev_price']].head())


# ============================================================================
# EXAMPLE 4: Filter Specific Commodities
# ============================================================================
def example_4_filter(df):
    print("\n" + "="*70)
    print("EXAMPLE 4: Filter Specific Commodities")
    print("="*70)

    # Filter beras
    print("\nHarga Beras di Berbagai Pasar:")
    beras = df[df['commodity_name'].str.contains('Beras IR. I', case=False, na=False)]

    if not beras.empty:
        pivot = beras.pivot_table(
            values='newest_price',
            index='market_name',
            columns='commodity_name',
            aggfunc='first'
        )
        print(pivot)

    # Filter cabe
    print("\n\nHarga Cabe Merah di Berbagai Pasar:")
    cabe = df[df['commodity_name'].str.contains('Cabe Merah Keriting', case=False, na=False)]

    for _, row in cabe.iterrows():
        status_icon = "▲" if row['status'] == 'rise' else "▼" if row['status'] == 'fall' else "="
        print(f"  {row['market_name']:30s} Rp {row['newest_price']:>8,}/kg {status_icon} {row['status']}")


# ============================================================================
# EXAMPLE 5: Export to Excel
# ============================================================================
def example_5_excel(df):
    print("\n" + "="*70)
    print("EXAMPLE 5: Export to Excel with Multiple Sheets")
    print("="*70)

    output = f"analisis_harga_{datetime.now().strftime('%Y%m%d')}.xlsx"

    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # Sheet 1: All data
        df.to_excel(writer, sheet_name='All Data', index=False)

        # Sheet 2: Summary by market
        summary = df.groupby('market_name').agg({
            'newest_price': ['mean', 'min', 'max'],
            'commodity_name': 'count'
        }).round(0)
        summary.to_excel(writer, sheet_name='Summary by Market')

        # Sheet 3: Summary by commodity
        commodity_summary = df.groupby('commodity_name').agg({
            'newest_price': ['mean', 'min', 'max'],
            'market_name': 'count'
        }).round(0).sort_values(('newest_price', 'mean'), ascending=False)
        commodity_summary.to_excel(writer, sheet_name='Summary by Commodity')

        # Sheet 4: Rising prices
        rising = df[df['status'] == 'rise']
        if not rising.empty:
            rising.to_excel(writer, sheet_name='Rising Prices', index=False)

    print(f"Excel file created: {output}")
    print(f"  - Sheet 1: All Data ({len(df)} rows)")
    print(f"  - Sheet 2: Summary by Market")
    print(f"  - Sheet 3: Summary by Commodity")
    print(f"  - Sheet 4: Rising Prices")


# ============================================================================
# EXAMPLE 6: Using as Import in Another Script
# ============================================================================
def example_6_import():
    print("\n" + "="*70)
    print("EXAMPLE 6: Using Convenience Functions")
    print("="*70)

    from infopangan import get_all_markets, get_market_prices, search_market

    # Quick access without initializing class
    markets = get_all_markets()
    print(f"Quick access - Total markets: {len(markets)}")

    # Search
    results = search_market("Senen")
    print(f"Quick search - Found: {results[0]['market_name']}")

    # Get prices
    prices = get_market_prices(3)
    print(f"Quick prices - Date: {prices['selected_price_date']}")
    print(f"Quick prices - Commodities: {len(prices['data'])}")


# ============================================================================
# MAIN
# ============================================================================
if __name__ == "__main__":
    print("\n" + "="*70)
    print("InfoPangan Module - Complete Examples")
    print("="*70)

    # Run all examples
    example_1_basic()

    df = example_2_dataframe()

    example_3_analysis(df)

    example_4_filter(df)

    example_5_excel(df)

    example_6_import()

    print("\n" + "="*70)
    print("All examples completed!")
    print("="*70 + "\n")
