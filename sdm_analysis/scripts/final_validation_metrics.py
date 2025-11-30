
import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn.metrics import mean_absolute_percentage_error
import json

def run_metrics():
    results = {}
    
    # Load Data
    try:
        df = pd.read_csv('sdm_results_fixed/fase1/panel_data_with_lags.csv')
    except:
        print(json.dumps({"error": "File not found"}))
        return

    # Define predictors
    X_vars = [
        'price_lag1', 'precipitation_mm', 
        'rain_lag1', 'rain_lag2', 'rain_lag3',
        'temperature_mean_c', 'temp_lag1',
        'bbm_price_idr', 'bbm_lag1',
        'luas_panen_ha', 'avg_distance_km'
    ]
    month_cols = [col for col in df.columns if col.startswith('month_')]
    X_vars_all = X_vars + month_cols
    
    df_clean = df.dropna(subset=X_vars_all + ['price'])
    X = df_clean[X_vars_all]
    X_const = sm.add_constant(X)
    
    # 1. VIF
    vif_dict = {}
    for i in range(X_const.shape[1]):
        vif_dict[X_const.columns[i]] = variance_inflation_factor(X_const.values, i)
    results['vif'] = vif_dict
    
    # 2. Out of Sample MAPE
    df_clean['date'] = pd.to_datetime(df_clean['date'])
    df_sorted = df_clean.sort_values('date')
    dates = df_sorted['date'].unique()
    split_date = dates[-12] 
    
    train = df_sorted[df_sorted['date'] < split_date]
    test = df_sorted[df_sorted['date'] >= split_date]
    
    model_ols = sm.OLS(train['price'], sm.add_constant(train[X_vars_all])).fit()
    pred_test = model_ols.predict(sm.add_constant(test[X_vars_all], has_constant='add'))
    
    mape = mean_absolute_percentage_error(test['price'], pred_test)
    results['mape'] = mape
    
    # 3. BBM Correlation
    results['corr_bbm'] = df_clean['bbm_price_idr'].corr(df_clean['price'])
    results['corr_bbm_lag'] = df_clean['bbm_lag1'].corr(df_clean['price'])

    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    run_metrics()
