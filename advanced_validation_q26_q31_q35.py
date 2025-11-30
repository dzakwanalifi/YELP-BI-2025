
import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn.metrics import mean_absolute_percentage_error
import os

def advanced_validation():
    print("========================================================")
    print("ADVANCED VALIDATION: VIF, OUT-OF-SAMPLE, & VULNERABILITY")
    print("========================================================")

    # 1. Load Data
    # Try to load the panel data created in the previous step
    try:
        df = pd.read_csv('sdm_results_fixed/fase1/panel_data_with_lags.csv')
        print(f"Data Loaded: {len(df)} observations")
    except FileNotFoundError:
        print("Error: Panel data file not found. Please run the fixed SDM estimation first.")
        return

    # Define predictors used in the model
    X_vars = [
        'price_lag1', 'precipitation_mm', 
        'rain_lag1', 'rain_lag2', 'rain_lag3',
        'temperature_mean_c', 'temp_lag1',
        'bbm_price_idr', 'bbm_lag1',
        'luas_panen_ha', 'avg_distance_km'
    ]
    
    # Add month dummies
    month_cols = [col for col in df.columns if col.startswith('month_')]
    X_vars_all = X_vars + month_cols
    
    # Filter data to ensure no NaNs for VIF calculation
    df_clean = df.dropna(subset=X_vars_all + ['price'])
    X = df_clean[X_vars_all]
    
    # ---------------------------------------------------------
    # Q26: Calculate VIF
    # ---------------------------------------------------------
    print("\n[Q26] VARIANCE INFLATION FACTOR (VIF) ANALYSIS")
    print("-" * 50)
    
    # Add constant for VIF calculation
    X_const = sm.add_constant(X)
    
    vif_data = pd.DataFrame()
    vif_data["Variable"] = X_const.columns
    vif_data["VIF"] = [variance_inflation_factor(X_const.values, i) for i in range(X_const.shape[1])]
    
    print(vif_data.sort_values('VIF', ascending=False).to_string(index=False))
    
    # ---------------------------------------------------------
    # Q9: BBM Correlation Check
    # ---------------------------------------------------------
    print("\n[Q9] BBM vs PRICE CORRELATION CHECK")
    print("-" * 50)
    corr_bbm = df_clean['bbm_price_idr'].corr(df_clean['price'])
    corr_bbm_lag = df_clean['bbm_lag1'].corr(df_clean['price'])
    print(f"Correlation (Current BBM vs Price): {corr_bbm:.4f}")
    print(f"Correlation (Lagged BBM vs Price):  {corr_bbm_lag:.4f}")
    
    # ---------------------------------------------------------
    # Q31: Out-of-Sample Validation (Train-Test Split)
    # ---------------------------------------------------------
    print("\n[Q31] OUT-OF-SAMPLE VALIDATION (MAPE)")
    print("-" * 50)
    
    # Sort by date
    df_clean['date'] = pd.to_datetime(df_clean['date'])
    df_sorted = df_clean.sort_values('date')
    
    # Split: Train (First 48 months), Test (Last 12 months)
    dates = df_sorted['date'].unique()
    split_date = dates[-12] # Last 12 months as test set
    
    train = df_sorted[df_sorted['date'] < split_date]
    test = df_sorted[df_sorted['date'] >= split_date]
    
    print(f"Train set: {train['date'].min().date()} to {train['date'].max().date()} ({len(train)} obs)")
    print(f"Test set:  {test['date'].min().date()} to {test['date'].max().date()} ({len(test)} obs)")
    
    # Simple OLS for prediction (proxy for SDM prediction power without full spatial matrix reconstruction here)
    # Note: Full SDM prediction requires W matrix subsetting which is complex in this script. 
    # We use OLS with Lag Y as a strong proxy since rho was not significant in SDM.
    
    model_ols = sm.OLS(train['price'], sm.add_constant(train[X_vars_all])).fit()
    
    # Predict
    pred_test = model_ols.predict(sm.add_constant(test[X_vars_all], has_constant='add'))
    actual_test = test['price']
    
    mape = mean_absolute_percentage_error(actual_test, pred_test)
    rmse = np.sqrt(((pred_test - actual_test) ** 2).mean())
    
    print(f"\nOut-of-Sample Metrics (Last 12 Months):")
    print(f"MAPE: {mape:.4%}")
    print(f"RMSE: {rmse:.2f} IDR")
    
    # ---------------------------------------------------------
    # Q35: Vulnerability Analysis
    # ---------------------------------------------------------
    print("\n[Q35] REGIONAL VULNERABILITY ANALYSIS")
    print("-" * 50)
    
    # Calculate average price volatility per region
    volatility = df_clean.groupby('location_name')['price'].std().sort_values(ascending=False)
    
    # Calculate sensitivity to Temperature (using the SDM coefficient +67.71)
    # Vulnerability = Avg Temp * Coef (Potential Impact) + Volatility
    # Or simply rank by historical max price or volatility
    
    print("Top 5 Most Volatile Regions (Std Dev of Price):")
    print(volatility.head(5))
    
    # Identify regions with highest average temperature (most prone to heat shock impact)
    avg_temp = df_clean.groupby('location_name')['temperature_mean_c'].mean().sort_values(ascending=False)
    print("\nTop 5 Hottest Regions (Highest Risk from W_temp shock):")
    print(avg_temp.head(5))

if __name__ == "__main__":
    advanced_validation()
