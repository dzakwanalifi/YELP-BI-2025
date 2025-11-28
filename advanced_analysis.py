import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg') # Headless mode
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from statsmodels.tsa.api import VAR
from statsmodels.tsa.stattools import grangercausalitytests
from statsmodels.tsa.vector_ar.vecm import coint_johansen
import os
import warnings
import traceback

# Try importing folium for interactive maps
try:
    import folium
except ImportError:
    folium = None
    print("Folium not found. Interactive maps will be skipped.")

# Suppress warnings for cleaner output
warnings.filterwarnings("ignore")

# --- Configuration ---
BASE_DIR = r"d:\Arsip Kompetisi\YELP BI 2025"
OUTPUT_DIR = os.path.join(BASE_DIR, "final_paper_assets")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# --- Data Loading ---
print("Loading datasets...")
try:
    # 1. Prices (PIHPS)
    prices_df = pd.read_csv(os.path.join(BASE_DIR, "cleaned_pihps_data/cleaned_combined.csv"))
    prices_df['date'] = pd.to_datetime(prices_df['date'])
    
    # Filter for a key commodity
    commodity_name = "Cabai Rawit Merah"
    prices_df = prices_df[prices_df['commodity_name'] == commodity_name]
    
    # Map PIHPS name to Spatial name
    commodity_map = {
        "Cabai Rawit Merah": "Cabai",
        "Cabai Merah Keriting": "Cabai",
        "Bawang Merah": "Bawang Merah",
        "Bawang Putih": "Bawang Putih",
        "Daging Ayam Ras": "Daging Ayam",
        "Daging Sapi Kualitas 1": "Daging Sapi",
        "Telur Ayam Ras": "Telur Ayam",
        "Minyak Goreng Curah": "Minyak Goreng",
        "Gula Pasir Kualitas Premium": "Gula Pasir"
    }
    spatial_commodity = commodity_map.get(commodity_name, commodity_name)
    
    # 2. Supply Chain Spatial Features
    spatial_df = pd.read_csv(os.path.join(BASE_DIR, "supply_chain_spatial_fast/spatial_features_20251128_141527.csv"))
    spatial_df = spatial_df[spatial_df['commodity'] == spatial_commodity]
    print(f"Filtered Spatial Data for {spatial_commodity}: {spatial_df.shape}")
    
    # 3. Weather
    weather_df = pd.read_csv(os.path.join(BASE_DIR, "weather_pihps_historical.csv"))
    weather_df['date'] = pd.to_datetime(weather_df['date'])
    
    print("Data loaded successfully.")
except Exception as e:
    print(f"Error loading data: {e}")
    exit()

# --- Part 1: MGWR (Simulated via Weighted Regression) ---
print("\n--- Running MGWR Analysis (Spatial Heterogeneity) ---")

try:
    # Prepare Data for Regression
    recent_prices = prices_df[prices_df['date'] >= '2024-01-01'].groupby('location_name')['price'].mean().reset_index()
    reg_data = pd.merge(recent_prices, spatial_df, left_on='location_name', right_on='location', how='inner')
    recent_weather = weather_df[weather_df['date'] >= '2024-01-01'].groupby('location_name')['rain_mm'].mean().reset_index()
    reg_data = pd.merge(reg_data, recent_weather, on='location_name', how='inner')

    # City Coordinates
    city_coords = {
        'DKI Jakarta': (-6.2088, 106.8456),
        'Jakarta Pusat': (-6.1805, 106.8284),
        'Bandung': (-6.9175, 107.6191),
        'Bogor': (-6.5971, 106.8060),
        'Bekasi': (-6.2383, 106.9756),
        'Depok': (-6.4025, 106.7942),
        'Cirebon': (-6.7320, 108.5523),
        'Sukabumi': (-6.9277, 106.9300),
        'Tasikmalaya': (-7.3196, 108.2207),
        'Kab. Cirebon': (-6.75, 108.5),
        'Kab. Tasikmalaya': (-7.35, 108.25),
        'Jawa Barat': (-6.9, 107.6)
    }

    reg_data['lat'] = reg_data['location_name'].map(lambda x: city_coords.get(x, (0,0))[0])
    reg_data['lon'] = reg_data['location_name'].map(lambda x: city_coords.get(x, (0,0))[1])
    reg_data = reg_data[reg_data['lat'] != 0]

    # Define Variables
    X_cols = ['nearest_production_km', 'nearest_distribution_km', 'rain_mm']
    y_col = 'price'

    # Standardize
    reg_data_std = reg_data.copy()
    for col in X_cols + [y_col]:
        reg_data_std[col] = (reg_data[col] - reg_data[col].mean()) / reg_data[col].std()

    # Run Local Regressions (GWR-like)
    results = []
    bandwidth = 1.0 # Hardcoded bandwidth for competition speed

    for idx, target_row in reg_data_std.iterrows():
        dists = np.sqrt((reg_data_std['lat'] - target_row['lat'])**2 + (reg_data_std['lon'] - target_row['lon'])**2)
        weights = np.exp(-(dists**2) / (2 * bandwidth**2))
        
        X = sm.add_constant(reg_data_std[X_cols])
        y = reg_data_std[y_col]
        
        model = sm.WLS(y, X, weights=weights)
        res = model.fit()
        
        row_res = {'location': target_row['location_name'], 'lat': target_row['lat'], 'lon': target_row['lon'], 'R2': res.rsquared}
        for col in X_cols:
            row_res[f'coef_{col}'] = res.params[col]
        results.append(row_res)

    mgwr_results = pd.DataFrame(results)
    mgwr_results.to_csv(os.path.join(OUTPUT_DIR, "mgwr_results.csv"), index=False)
    print("MGWR Results saved.")

    # 1. Static Plot
    plt.figure(figsize=(10, 6))
    sc = plt.scatter(mgwr_results['lon'], mgwr_results['lat'], 
                     c=mgwr_results['coef_nearest_production_km'], 
                     cmap='RdBu_r', s=200, edgecolors='k')
    plt.colorbar(sc, label='Sensitivity to Production Distance')
    for i, txt in enumerate(mgwr_results['location']):
        plt.annotate(txt, (mgwr_results['lon'].iloc[i], mgwr_results['lat'].iloc[i]), xytext=(5, 5), textcoords='offset points')
    plt.title(f'Spatial Heterogeneity: Impact of Distance to Production on {commodity_name} Price')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.grid(True, alpha=0.3)
    plt.savefig(os.path.join(OUTPUT_DIR, "Fig1_MGWR_Coefficient_Map.png"))
    plt.close()
    print("Fig1_MGWR_Coefficient_Map.png saved.")

    # 2. Interactive Map (Folium) - NEW!
    if folium:
        m = folium.Map(location=[-6.9, 107.6], zoom_start=8, tiles='CartoDB positron')
        
        # Add color scale legend (simplified)
        
        for idx, row in mgwr_results.iterrows():
            coef = row['coef_nearest_production_km']
            # Color logic: Red = Negative Impact (Distance hurts), Blue = Positive/Neutral
            color = '#d73027' if coef < -0.3 else '#4575b4'
            
            folium.CircleMarker(
                location=[row['lat'], row['lon']],
                radius=10 + (abs(coef) * 10), # Size by magnitude
                popup=folium.Popup(f"<b>{row['location']}</b><br>Prod. Dist Coef: {coef:.3f}<br>R2: {row['R2']:.2f}", max_width=200),
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.7
            ).add_to(m)
        
        m.save(os.path.join(OUTPUT_DIR, "interactive_mgwr_map.html"))
        print("interactive_mgwr_map.html saved.")

except Exception as e:
    print(f"Error in MGWR: {e}")
    traceback.print_exc()

# --- Part 2: Network Stress Test (VAR & IRF) ---
print("\n--- Running Network Stress Test (VAR/IRF) ---")

try:
    ts_data = prices_df.pivot_table(index='date', columns='location_name', values='price')
    ts_data = ts_data.resample('W').mean().interpolate()

    nodes = ['Bandung', 'Tasikmalaya', 'Cirebon', 'Jakarta Pusat', 'Bogor']
    available_nodes = [c for c in nodes if c in ts_data.columns]
    ts_subset = ts_data[available_nodes].dropna()
    
    if ts_subset.empty:
        print("Error: Time series data is empty.")
    else:
        # 1. Cointegration Test (Johansen) - NEW!
        print("Performing Johansen Cointegration Test...")
        # det_order=0 (no deterministic trend), k_ar_diff=1 (lag order)
        johan_test = coint_johansen(ts_subset, det_order=0, k_ar_diff=1)
        # Store results
        coint_res = pd.DataFrame([johan_test.lr1, johan_test.cvt[:, 1]], index=['Trace Stat', 'Critical Val (5%)']).T
        coint_res.to_csv(os.path.join(OUTPUT_DIR, "johansen_cointegration_test.csv"))
        print("Cointegration test results saved.")

        # 2. Granger Causality Test - NEW!
        # Check if Bandung Granger-causes Jakarta
        if 'Bandung' in available_nodes and 'Jakarta Pusat' in available_nodes:
            print("Performing Granger Causality Test (Bandung -> Jakarta)...")
            granger_res = grangercausalitytests(ts_subset[['Jakarta Pusat', 'Bandung']], maxlag=4, verbose=False)
            # Extract p-value for lag 2
            p_val = granger_res[2][0]['ssr_chi2test'][1]
            print(f"Granger Causality p-value (Lag 2): {p_val:.4f}")
            with open(os.path.join(OUTPUT_DIR, "granger_causality.txt"), "w") as f:
                f.write(f"Granger Causality (Bandung -> Jakarta Pusat)\nLag 2 p-value: {p_val:.4f}\n")

        # 3. Fit VAR Model
        model = VAR(ts_subset)
        results = model.fit(maxlags=4, ic='aic')

        # 4. Impulse Response Analysis
        irf = results.irf(10)
        
        plt.figure(figsize=(10, 6))
        irf.plot(orth=False, impulse='Bandung', response='Jakarta Pusat', figsize=(10, 6))
        plt.title(f'Impulse Response: Shock in Bandung -> Impact on Jakarta Pusat ({commodity_name})')
        plt.tight_layout()
        plt.savefig(os.path.join(OUTPUT_DIR, "Fig2_Shock_Propagation_IRF.png"))
        plt.close()

        # Save IRF values
        irf_vals = irf.irfs
        name_to_idx = {name: i for i, name in enumerate(available_nodes)}
        impulse_idx = name_to_idx.get('Bandung')
        response_idx = name_to_idx.get('Jakarta Pusat')
        
        if impulse_idx is not None and response_idx is not None:
            irf_series = irf_vals[:, response_idx, impulse_idx]
            irf_df = pd.DataFrame({'week': range(11), 'response_jakarta_to_bandung_shock': irf_series})
            irf_df.to_csv(os.path.join(OUTPUT_DIR, "irf_shock_values.csv"), index=False)
            print("Stress Test completed.")

except Exception as e:
    print(f"Error in VAR/IRF: {e}")
    traceback.print_exc()


# --- Part 3: Asymmetric Price Transmission (NARDL-lite) ---
print("\n--- Running Asymmetry Analysis (Rockets & Feathers) ---")

try:
    if 'Bandung' in ts_subset.columns and 'Jakarta Pusat' in ts_subset.columns:
        pair_df = ts_subset[['Bandung', 'Jakarta Pusat']].copy()
        pair_df['d_Bandung'] = pair_df['Bandung'].diff()
        pair_df['d_Jakarta'] = pair_df['Jakarta Pusat'].diff()

        pair_df['d_Bandung_Pos'] = pair_df['d_Bandung'].apply(lambda x: x if x > 0 else 0)
        pair_df['d_Bandung_Neg'] = pair_df['d_Bandung'].apply(lambda x: x if x < 0 else 0)

        pair_df['d_Bandung_Pos_Lag1'] = pair_df['d_Bandung_Pos'].shift(1)
        pair_df['d_Bandung_Neg_Lag1'] = pair_df['d_Bandung_Neg'].shift(1)

        pair_df = pair_df.dropna()

        X = pair_df[['d_Bandung_Pos_Lag1', 'd_Bandung_Neg_Lag1']]
        X = sm.add_constant(X)
        y = pair_df['d_Jakarta']

        model_asym = sm.OLS(y, X).fit()
        
        with open(os.path.join(OUTPUT_DIR, "asymmetry_regression_summary.txt"), "w") as f:
            f.write(model_asym.summary().as_text())

        shock_magnitude = 1000
        response_pos = model_asym.params['d_Bandung_Pos_Lag1'] * shock_magnitude
        response_neg = model_asym.params['d_Bandung_Neg_Lag1'] * -shock_magnitude

        plt.figure(figsize=(8, 5))
        bars = plt.bar(['Price Increase (Rocket)', 'Price Decrease (Feather)'], 
                [response_pos, abs(response_neg)], 
                color=['red', 'green'])
        plt.title(f'Asymmetric Transmission: Impact of Rp {shock_magnitude} Change in Bandung on Jakarta')
        plt.ylabel('Price Change in Jakarta (Rp)')
        plt.bar_label(bars, fmt='%.0f')
        plt.savefig(os.path.join(OUTPUT_DIR, "Fig3_Price_Asymmetry.png"))
        plt.close()
        print("Asymmetry Analysis completed.")
    else:
        print("Skipping Asymmetry: Bandung or Jakarta Pusat missing.")

except Exception as e:
    print(f"Error in Asymmetry Analysis: {e}")
    traceback.print_exc()

# --- Part 4: Automated Narrative Generation - NEW! ---
print("\n--- Generating Narrative Summary ---")
try:
    narrative = []
    narrative.append("=== AUTOMATED ANALYSIS INSIGHTS ===\n")
    
    # MGWR Narrative
    if 'mgwr_results' in locals():
        jkt_coef = mgwr_results[mgwr_results['location'] == 'Jakarta Pusat']['coef_nearest_production_km'].values[0]
        cirebon_coef = mgwr_results[mgwr_results['location'] == 'Cirebon']['coef_nearest_production_km'].values[0]
        narrative.append(f"1. SPATIAL HETEROGENEITY (MGWR):")
        narrative.append(f"- Jakarta Pusat Sensitivity to Production Distance: {jkt_coef:.3f}")
        narrative.append(f"- Cirebon Sensitivity to Production Distance: {cirebon_coef:.3f}")
        if abs(jkt_coef) > abs(cirebon_coef):
            narrative.append("-> CONCLUSION: Jakarta is significantly more affected by physical distance/logistics friction than Cirebon.")
        narrative.append("")

    # Stress Test Narrative
    if 'irf_df' in locals():
        peak_week = irf_df['response_jakarta_to_bandung_shock'].abs().idxmax()
        peak_val = irf_df['response_jakarta_to_bandung_shock'].iloc[peak_week]
        narrative.append(f"2. SHOCK PROPAGATION (VAR/IRF):")
        narrative.append(f"- Peak Impact Week: Week {peak_week}")
        narrative.append(f"- Peak Impact Value: {peak_val:.3f}")
        narrative.append(f"-> CONCLUSION: There is a {peak_week}-week lag before a shock in Bandung fully hits Jakarta. This is the 'Golden Time' for intervention.")
        narrative.append("")

    # Asymmetry Narrative
    if 'model_asym' in locals():
        pos_coef = model_asym.params['d_Bandung_Pos_Lag1']
        neg_coef = model_asym.params['d_Bandung_Neg_Lag1']
        narrative.append(f"3. PRICE ASYMMETRY (NARDL):")
        narrative.append(f"- Transmission of Price Increase (Rocket): {pos_coef:.3f}")
        narrative.append(f"- Transmission of Price Decrease (Feather): {neg_coef:.3f}")
        if neg_coef > pos_coef:
             narrative.append("-> CONCLUSION: Price decreases transmit FASTER than increases. This suggests 'Panic Selling' behavior due to lack of storage.")
        else:
             narrative.append("-> CONCLUSION: Price increases transmit FASTER than decreases. This suggests 'Greed/Hoarding' behavior.")
    
    with open(os.path.join(OUTPUT_DIR, "automated_insights.txt"), "w") as f:
        f.write("\n".join(narrative))
    print("Narrative summary saved to automated_insights.txt")

except Exception as e:
    print(f"Error generating narrative: {e}")

print("\nAnalysis Complete. All assets generated in final_paper_assets/")
