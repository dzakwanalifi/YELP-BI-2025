"""
Example Usage - InfoPangan Statistics Module
=============================================
Contoh penggunaan statistics endpoint dari infopangan.py
"""

from infopangan import InfoPangan
import pandas as pd
from datetime import datetime

# ============================================================================
# EXAMPLE 1: Get Statistics for a Market
# ============================================================================
def example_1_market_statistics():
    print("\n" + "="*70)
    print("EXAMPLE 1: Market Statistics")
    print("="*70)

    client = InfoPangan()

    # Get statistics untuk Pasar Senen di November 2025
    stats = client.get_statistics_by_market(3, "2025-11")

    if stats and 'data' in stats:
        print(f"Total commodities: {len(stats['data'])}")

        # Show top 5 commodities by average price
        print("\nTop 5 Komoditas (by average price):")
        sorted_commodities = sorted(
            stats['data'],
            key=lambda x: x.get('avg_value', 0),
            reverse=True
        )[:5]

        for idx, commodity in enumerate(sorted_commodities, 1):
            print(f"{idx}. {commodity['commodity_name']}")
            print(f"   Avg: Rp {commodity['avg_value']:>10,}")
            print(f"   Min: Rp {commodity['min_value']:>10,}")
            print(f"   Max: Rp {commodity['max_value']:>10,}")
            print(f"   Daily data: {len(commodity.get('recaps', []))} points")


# ============================================================================
# EXAMPLE 2: Get Statistics for Multiple Months
# ============================================================================
def example_2_multiple_months():
    print("\n" + "="*70)
    print("EXAMPLE 2: Multiple Months Statistics")
    print("="*70)

    client = InfoPangan()

    # Get 3 bulan terakhir untuk Pasar Senen
    print("Fetching 3 months of data for Pasar Senen...")
    stats_range = client.get_statistics_range(
        filter_by="market",
        entity_id=3,
        start_month="2025-09",
        months=3
    )

    print(f"Total months fetched: {len(stats_range)}")

    for month_data in stats_range:
        print(f"\n{month_data['year_month']}: {len(month_data['data']['data'])} commodities")


# ============================================================================
# EXAMPLE 3: Convert to DataFrame (Summary)
# ============================================================================
def example_3_dataframe_summary():
    print("\n" + "="*70)
    print("EXAMPLE 3: DataFrame Summary (Monthly Aggregates)")
    print("="*70)

    client = InfoPangan()

    # Get summary statistics (avg, max, min)
    df = client.statistics_to_dataframe("market", 3, "2025-11", include_daily=False)

    print(f"DataFrame shape: {df.shape}")
    print(f"\nColumns: {list(df.columns)}")

    # Show sample
    print("\nSample data (5 rows):")
    print(df[['commodity_name', 'avg_value', 'min_value', 'max_value', 'data_points']].head())

    # Save to CSV
    output = f"statistics_summary_{datetime.now().strftime('%Y%m%d')}.csv"
    df.to_csv(output, index=False, encoding='utf-8-sig')
    print(f"\nSaved to: {output}")

    return df


# ============================================================================
# EXAMPLE 4: Convert to DataFrame (Daily Time Series)
# ============================================================================
def example_4_dataframe_daily():
    print("\n" + "="*70)
    print("EXAMPLE 4: DataFrame with Daily Time Series")
    print("="*70)

    client = InfoPangan()

    # Get daily time series data
    df = client.statistics_to_dataframe("market", 3, "2025-11", include_daily=True)

    print(f"DataFrame shape: {df.shape}")
    print(f"\nColumns: {list(df.columns)}")

    # Show date range
    print(f"\nDate range: {df['date'].min()} to {df['date'].max()}")

    # Show sample
    print("\nSample data (5 rows):")
    print(df[['date', 'commodity_name', 'price', 'avg_monthly']].head())

    # Save to CSV
    output = f"statistics_daily_{datetime.now().strftime('%Y%m%d')}.csv"
    df.to_csv(output, index=False, encoding='utf-8-sig')
    print(f"\nSaved to: {output}")

    return df


# ============================================================================
# EXAMPLE 5: Analyze Price Trends
# ============================================================================
def example_5_price_trends(df_daily):
    print("\n" + "="*70)
    print("EXAMPLE 5: Price Trends Analysis")
    print("="*70)

    # Filter for specific commodity (e.g., Beras)
    beras = df_daily[df_daily['commodity_name'].str.contains('Beras IR. I', case=False, na=False)]

    if not beras.empty:
        print("\nBeras IR. I Price Trend:")
        print(f"Date range: {beras['date'].min()} to {beras['date'].max()}")
        print(f"Data points: {len(beras)}")
        print(f"\nPrice statistics:")
        print(f"  Average: Rp {beras['price'].mean():,.0f}")
        print(f"  Min: Rp {beras['price'].min():,.0f} on {beras[beras['price'] == beras['price'].min()]['date'].iloc[0]}")
        print(f"  Max: Rp {beras['price'].max():,.0f} on {beras[beras['price'] == beras['price'].max()]['date'].iloc[0]}")

        # Show daily trend (first 10 days)
        print("\nDaily prices (first 10 days):")
        for _, row in beras.head(10).iterrows():
            print(f"  {row['date']}: Rp {row['price']:>8,}")


# ============================================================================
# EXAMPLE 6: Compare Across Filter Types
# ============================================================================
def example_6_filter_types():
    print("\n" + "="*70)
    print("EXAMPLE 6: Compare Different Filter Types")
    print("="*70)

    client = InfoPangan()

    # Get statistics by market
    print("\n1. By Market (Pasar Senen - ID: 3):")
    stats_market = client.get_statistics("market", 3, "2025-11")
    if stats_market and 'data' in stats_market:
        print(f"   Total commodities: {len(stats_market['data'])}")

    # Get statistics by city (Jakarta Pusat - ID: 31)
    print("\n2. By City (Jakarta Pusat - ID: 31):")
    stats_city = client.get_statistics("city", 31, "2025-11")
    if stats_city and 'data' in stats_city:
        print(f"   Total commodities: {len(stats_city['data'])}")

    # Get statistics by commodity (Beras - ID: 1)
    print("\n3. By Commodity (Beras IR. I - ID: 1):")
    stats_commodity = client.get_statistics("commodity", 1, "2025-11")
    if stats_commodity and 'data' in stats_commodity:
        print(f"   Total data entries: {len(stats_commodity['data'])}")


# ============================================================================
# EXAMPLE 7: Export to Excel with Multiple Sheets
# ============================================================================
def example_7_excel_export():
    print("\n" + "="*70)
    print("EXAMPLE 7: Export to Excel (Multiple Sheets)")
    print("="*70)

    client = InfoPangan()

    # Get both summary and daily data
    df_summary = client.statistics_to_dataframe("market", 3, "2025-11", include_daily=False)
    df_daily = client.statistics_to_dataframe("market", 3, "2025-11", include_daily=True)

    output = f"statistics_analysis_{datetime.now().strftime('%Y%m%d')}.xlsx"

    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # Sheet 1: Summary
        df_summary.to_excel(writer, sheet_name='Summary', index=False)

        # Sheet 2: Daily Time Series
        df_daily.to_excel(writer, sheet_name='Daily Data', index=False)

        # Sheet 3: Top 10 Most Expensive (by average)
        top10 = df_summary.nlargest(10, 'avg_value')[
            ['commodity_name', 'avg_value', 'min_value', 'max_value']
        ]
        top10.to_excel(writer, sheet_name='Top 10 Expensive', index=False)

        # Sheet 4: Commodity Analysis (pivot by date)
        if not df_daily.empty:
            # Select a few commodities for pivot
            sample_commodities = df_daily['commodity_name'].unique()[:5]
            df_sample = df_daily[df_daily['commodity_name'].isin(sample_commodities)]

            pivot = df_sample.pivot_table(
                values='price',
                index='date',
                columns='commodity_name',
                aggfunc='first'
            )
            pivot.to_excel(writer, sheet_name='Price Matrix')

    print(f"Excel file created: {output}")
    print(f"  - Sheet 1: Summary ({len(df_summary)} rows)")
    print(f"  - Sheet 2: Daily Data ({len(df_daily)} rows)")
    print(f"  - Sheet 3: Top 10 Expensive")
    print(f"  - Sheet 4: Price Matrix")


# ============================================================================
# EXAMPLE 8: Using Convenience Functions
# ============================================================================
def example_8_convenience_functions():
    print("\n" + "="*70)
    print("EXAMPLE 8: Using Convenience Functions")
    print("="*70)

    from infopangan import get_market_statistics, get_city_statistics

    # Quick access without class initialization
    print("Using convenience functions for quick access...")

    # Market statistics
    stats = get_market_statistics(3, "2025-11")
    print(f"\nMarket stats: {len(stats.get('data', []))} commodities")

    # City statistics
    stats = get_city_statistics(31, "2025-11")
    print(f"City stats: {len(stats.get('data', []))} commodities")


# ============================================================================
# MAIN
# ============================================================================
if __name__ == "__main__":
    print("\n" + "="*70)
    print("InfoPangan Statistics Module - Complete Examples")
    print("="*70)

    # Run all examples
    example_1_market_statistics()

    example_2_multiple_months()

    df_summary = example_3_dataframe_summary()

    df_daily = example_4_dataframe_daily()

    example_5_price_trends(df_daily)

    example_6_filter_types()

    example_7_excel_export()

    example_8_convenience_functions()

    print("\n" + "="*70)
    print("All examples completed!")
    print("="*70 + "\n")
