"""
Answer validation questions Q12-Q20: Seasonality and Spatial Effects
"""
import pandas as pd
import numpy as np

print("="*80)
print("VALIDATION QUESTIONS Q12-Q20: SEASONALITY & SPATIAL EFFECTS")
print("="*80)

# Load coefficients
coef = pd.read_csv('sdm_results_fixed/fase4/panel_coefficients.csv')

# Q12: Which months are most significant?
print("\n[Q12] Which months show significant seasonality?")
print("-" * 60)
month_vars = coef[coef['Variable'].str.contains('month_', na=False)].copy()
month_vars['abs_coef'] = month_vars['Coefficient'].abs()
month_vars_sorted = month_vars.sort_values('P_value')
print("\nMonth dummies ranked by significance:")
print(month_vars_sorted[['Variable', 'Coefficient', 'P_value', 'Sig']].to_string(index=False))

significant_months = month_vars[month_vars['P_value'] < 0.05]
print(f"\n[RESULT] {len(significant_months)} months are significant at alpha=0.05:")
for _, row in significant_months.iterrows():
    direction = "lower" if row['Coefficient'] < 0 else "higher"
    print(f"  - {row['Variable']}: {row['Coefficient']:.2f} IDR ({direction} than baseline)")

# Q13: W_temperature interpretation
print("\n[Q13] Economic interpretation of W_temperature_mean_c = +67.71")
print("-" * 60)
w_temp = coef[coef['Variable'] == 'W_temperature_mean_c'].iloc[0]
print(f"Coefficient: {w_temp['Coefficient']:.2f}")
print(f"Std Error: {w_temp['Std_Error']:.2f}")
print(f"P-value: {w_temp['P_value']:.2e}")
print(f"Significance: {w_temp['Sig']}")
print("\nInterpretation:")
print("When neighboring regions' temperature rises by 1 deg C (weighted average),")
print(f"local rice prices INCREASE by {w_temp['Coefficient']:.2f} IDR/kg.")
print("\nThis is a POSITIVE spatial spillover effect, suggesting:")
print("1. Higher neighbor temperature -> Lower neighbor supply -> Higher neighbor prices")
print("2. Price transmission through spatial arbitrage (traders buy local, sell to hot neighbors)")
print("3. Substitution effect: Consumers in hot regions buy from cooler neighbors")

# Q14: W_precipitation vs W_temperature
print("\n[Q14] Why is W_precipitation not significant but W_temperature is?")
print("-" * 60)
w_precip = coef[coef['Variable'] == 'W_precipitation_mm'].iloc[0]
print(f"W_precipitation: coef={w_precip['Coefficient']:.4f}, p={w_precip['P_value']:.4f}")
print(f"W_temperature:   coef={w_temp['Coefficient']:.2f}, p={w_temp['P_value']:.2e}")

print("\nPossible reasons:")
print("1. Rainfall effects are LOCALIZED (absorbed by rain_lag1/2/3 direct effects)")
print("   -> Rainfall shocks don't transmit spatially as much as temperature")
print("2. Temperature has BROADER spatial correlation (heat waves affect large areas)")
print("   -> Temperature creates synchronized supply shocks -> stronger price spillovers")
print("3. TEMPORAL LAG STRUCTURE captures local rainfall impacts (30/60/90 days)")
print("   -> Little residual variation left for spatial spillover")
print("4. IRRIGATION systems buffer rainfall shocks locally (no spillover needed)")
print("   -> But temperature affects yield quality across regions simultaneously")

# Q15: Spatial lag of dependent variable (W_price or rho)
print("\n[Q15] Is there a spatial lag of price (W_price or rho)?")
print("-" * 60)
w_price = coef[coef['Variable'].str.contains('W_price', na=False)]
if len(w_price) > 0:
    print("[YES] Found W_price_lag1:")
    print(w_price[['Variable', 'Coefficient', 'P_value', 'Sig']].to_string(index=False))
else:
    print("No explicit W_price variable found.")

# Check for rho
rho_row = coef[coef['Variable'] == 'rho']
if len(rho_row) > 0:
    print("\n[YES] Spatial autoregressive parameter rho exists:")
    rho = rho_row.iloc[0]
    print(f"  rho = {rho['Coefficient']:.4f}")
    print(f"  Std Error = {rho['Std_Error']:.4f}")
    print(f"  P-value = {rho['P_value']:.4f}")
    print(f"  Significance: {rho['Sig']}")
    print("\nInterpretation:")
    print(f"A 1 IDR/kg increase in neighboring prices -> {rho['Coefficient']:.4f} IDR/kg increase locally")
    if rho['P_value'] < 0.05:
        print("[RESULT] Spatial price transmission is SIGNIFICANT")
    else:
        print("[RESULT] Spatial price transmission is NOT SIGNIFICANT")
        print("  -> Price spillovers work through W_X variables (temperature, BBM) instead")
else:
    print("\n[NO] No rho parameter found in coefficients.")

# Q16: Value and interpretation of rho
print("\n[Q16] What is the value and interpretation of rho?")
print("-" * 60)
if len(rho_row) > 0:
    rho = rho_row.iloc[0]
    print(f"rho = {rho['Coefficient']:.4f} (p={rho['P_value']:.4f})")

    if rho['P_value'] < 0.05:
        print(f"\n[SIGNIFICANT] spatial autoregression at alpha=0.05")
        print(f"\nSpatial multiplier = 1 / (1 - rho) = 1 / (1 - {rho['Coefficient']:.4f}) = {1/(1-rho['Coefficient']):.4f}")
        print("\nThis means a 1 IDR/kg shock in one location creates:")
        print(f"  - Direct effect: 1.00 IDR/kg in origin location")
        print(f"  - Indirect effect: {1/(1-rho['Coefficient']) - 1:.4f} IDR/kg across all neighbors (cumulative)")
        print(f"  - Total effect: {1/(1-rho['Coefficient']):.4f} IDR/kg system-wide")
    else:
        print(f"\n[NOT SIGNIFICANT] at alpha=0.05")
        print("\nThis suggests:")
        print("1. Spatial price transmission is WEAK or ALREADY CAPTURED by W_X variables")
        print("2. Price spillovers work through INDIRECT CHANNELS (temperature, BBM)")
        print("3. Direct spatial arbitrage may be limited by:")
        print("   - Transportation costs")
        print("   - Market segmentation")
        print("   - Local price controls")
else:
    print("rho parameter not found - may be a GM_Lag model without explicit rho in output")
    print("Check if model used spatial lag specification.")

# Q17-Q20: Effects decomposition
print("\n[Q17-Q20] Direct, Indirect, and Total Effects Decomposition")
print("-" * 60)
print("\nNOTE: spreg.GM_Lag does not automatically compute effects decomposition.")
print("We need to manually calculate using the formula:")
print("  Direct Effect = β (from own variable)")
print("  Indirect Effect = θ × spatial multiplier (from W_variable)")
print("  Total Effect = Direct + Indirect")
print("\nKey variables for decomposition:")

# Select key variables for effects analysis
key_vars = ['precipitation_mm', 'temperature_mean_c', 'bbm_price_idr', 'rain_lag1', 'rain_lag2']
for var in key_vars:
    direct_row = coef[coef['Variable'] == var]
    spatial_row = coef[coef['Variable'] == f'W_{var}']

    if len(direct_row) > 0:
        direct_coef = direct_row.iloc[0]['Coefficient']
        direct_sig = direct_row.iloc[0]['Sig']

        if len(spatial_row) > 0:
            indirect_coef = spatial_row.iloc[0]['Coefficient']
            indirect_sig = spatial_row.iloc[0]['Sig']

            # Spatial multiplier (assuming rho exists)
            if len(rho_row) > 0:
                multiplier = 1 / (1 - rho_row.iloc[0]['Coefficient'])
            else:
                multiplier = 1.0  # No spatial multiplier if rho=0

            total_effect = direct_coef + indirect_coef * multiplier

            print(f"\n{var}:")
            print(f"  Direct:   {direct_coef:>10.4f} {direct_sig}")
            print(f"  Indirect: {indirect_coef:>10.4f} {indirect_sig} × {multiplier:.4f} = {indirect_coef * multiplier:.4f}")
            print(f"  Total:    {total_effect:>10.4f}")
        else:
            print(f"\n{var}:")
            print(f"  Direct:   {direct_coef:>10.4f} {direct_sig}")
            print(f"  Indirect: (no W_{var} found)")
            print(f"  Total:    {direct_coef:>10.4f} (direct only)")

print("\n" + "="*80)
print("Q12-Q20 COMPLETE - See answers above")
print("="*80)
