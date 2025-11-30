# 🚀 Quick Start Guide - Spatial Durbin Model Analysis

## YELP BI 2025: Rice Price Prediction

### ⏱️ 5-Minute Setup

---

## Step 1: Install Dependencies (2 minutes)

Open terminal/command prompt and run:

```bash
pip install -r requirements_sdm.txt
```

**Alternative** (if requirements file fails):
```bash
pip install pandas numpy scipy statsmodels pysal spreg libpysal esda splot geopandas matplotlib seaborn
```

---

## Step 2: Verify Data Files (1 minute)

Make sure these files exist in your directory:

```
D:\Arsip Kompetisi\YELP BI 2025\
├── cleaned_pihps_data/
│   └── cleaned_combined.csv                    ✓
├── weather_pihps_historical.csv                ✓
├── indonesia_gasoline_prices_5y.csv            ✓
├── bps-jakarta-data/
│   └── jawa_barat_rice_production_2020_2024.csv ✓
└── supply_chain_spatial_fast/
    └── supply_chain_facilities_20251128_141527.csv ✓
```

---

## Step 3: Run Analysis (2 minutes to start)

### Option A: Complete Analysis (Recommended)

```bash
python run_complete_sdm_analysis.py
```

**What happens:**
- Runs all 7 phases automatically
- Creates `sdm_results/` folder with all outputs
- Takes 5-15 minutes total

### Option B: Run Diagnostics Only (Phases 1-3)

```python
from sdm_analysis_complete import SpatialDurbinAnalysis

sdm = SpatialDurbinAnalysis()
sdm.fase1a_check_data_quality()
sdm.fase1b_merge_datasets()
sdm.fase2a_global_morans_i()
sdm.fase2b_local_morans_i()
sdm.fase2c_construct_spatial_weights()
sdm.fase3a_stationarity_tests()
sdm.fase3b_multicollinearity_test()
sdm.fase3c_heteroskedasticity_test()
sdm.fase3d_spatial_diagnostics()
sdm.fase3e_hausman_test()
```

---

## 📊 Quick Results Check

After running, check these key files:

### 1. Data Quality
```bash
sdm_results/fase1/1a_missing_values.csv
```
**Look for**: Missing percentage < 5%

### 2. Spatial Autocorrelation
```bash
sdm_results/fase2/2a_global_morans_i.csv
```
**Look for**: Moran's I > 0 and p-value < 0.05

### 3. Model Recommendation
```bash
sdm_results/fase3/3d_recommendation.txt
```
**Expected**: "Spatial Durbin Model (SDM)"

### 4. Model Results
```bash
sdm_results/fase4/4_sdm_summary.txt
```
**Look for**: Coefficient estimates and significance

### 5. Effects Decomposition
```bash
sdm_results/fase5/5b_effects_decomposition.csv
```
**Look for**: Direct, Indirect, Total effects for each variable

### 6. Policy Simulations
```bash
sdm_results/fase7/7_policy_simulations.csv
```
**Look for**: Impact estimates for BBM shock, production increase, weather

---

## 🔍 Interpret Key Results

### Global Moran's I Result
```
Moran's I = 0.65*** (p < 0.001)
```
**Meaning**: Strong spatial clustering → prices in nearby regions influence each other

### LISA Clusters
```
HH (High-High): Jakarta, Bandung
LL (Low-Low): Indramayu, Karawang
```
**Meaning**:
- HH = Price hot spots (intervention priority)
- LL = Price cold spots (stable regions)

### SDM Coefficients
```
BBM: β = 0.68*** (Direct), θ = 0.45** (Spatial lag)
```
**Meaning**:
- Direct: BBM +Rp 1000 → local price +Rp 680
- Spatial: BBM +Rp 1000 in neighbor → local price +Rp 450

### Effects Decomposition
```
BBM Total Effect = 1.13***
```
**Meaning**: BBM +Rp 1000 → total system effect +Rp 1130/kg (direct + spillover)

### Policy Simulation
```
Scenario: BBM +15%
Total Effect: +Rp 1850/kg
```
**Meaning**: Fuel subsidy removal → rice price increase Rp 1,850/kg

---

## ⚠️ Troubleshooting

### Error: "ModuleNotFoundError: No module named 'spreg'"
**Fix**:
```bash
pip install spreg libpysal esda
```

### Error: "FileNotFoundError: cleaned_combined.csv"
**Fix**: Check that data files are in correct locations (see Step 2)

### Error: "Singular matrix"
**Fix**: Check VIF results (fase3/3b_vif_results.csv), drop high-VIF variables

### Warning: "No spatial impacts available"
**Fix**: This is OK for diagnostic phases. Impacts appear in Phase 5.

---

## 📋 Checklist: Did It Work?

- [ ] No import errors
- [ ] `sdm_results/` folder created
- [ ] Files in `sdm_results/fase1/` to `sdm_results/fase7/`
- [ ] Global Moran's I is significant (p < 0.05)
- [ ] SDM model estimated successfully
- [ ] Effects decomposition table exists
- [ ] Policy simulations completed

---

## 🎯 Next Steps

### For Analysis Report

1. **Data Quality Section**
   - Use: `fase1/1a_descriptive_stats.csv`
   - Report: Missing values, sample size, date range

2. **Spatial Patterns Section**
   - Use: `fase2/2a_global_morans_i.csv`, `fase2/2b_lisa_clusters.csv`
   - Report: Moran's I, hot spots, cold spots

3. **Model Diagnostics Section**
   - Use: `fase3/3a_stationarity_tests.csv`, `fase3/3b_vif_results.csv`, `fase3/3d_spatial_diagnostics.csv`
   - Report: Test results, model selection justification

4. **Model Results Section**
   - Use: `fase4/4_coefficients.csv`, `fase5/5a_model_fit.csv`
   - Report: Coefficients, R², RMSE, significance

5. **Interpretation Section**
   - Use: `fase5/5b_effects_decomposition.csv`
   - Report: Direct vs indirect effects, spatial multipliers

6. **Policy Recommendations Section**
   - Use: `fase7/7_policy_simulations.csv`
   - Report: Impact scenarios, intervention priorities

### For Presentation Slides

**Slide 1: Spatial Clustering Evidence**
- Show Global Moran's I result
- Display LISA cluster map

**Slide 2: Model Specification**
- Why SDM? (LM test results)
- Diagnostic test summary

**Slide 3: Key Findings**
- Coefficient estimates (forest plot)
- Direct vs Indirect effects

**Slide 4: Policy Implications**
- Simulation results table
- Regional vulnerability ranking

**Slide 5: Recommendations**
- High-priority intervention regions
- Estimated policy impacts

---

## 📚 Additional Resources

- **Full Documentation**: `SDM_ANALYSIS_README.md`
- **Code Files**:
  - Diagnostics: `sdm_analysis_complete.py`
  - Estimation: `sdm_estimation_advanced.py`
  - Master runner: `run_complete_sdm_analysis.py`

- **PySAL Documentation**: https://pysal.org/
- **Spatial Econometrics Guide**: LeSage & Pace (2009)

---

## 💡 Pro Tips

1. **Run diagnostics first** (Phases 1-3) before full estimation
2. **Check VIF** - if > 10, consider dropping variables
3. **Verify Moran's I** - if not significant, spatial model may not be needed
4. **Compare W matrices** - check robustness across knn3, knn5, knn8
5. **Interpret carefully** - spatial spillovers can be larger than direct effects

---

## ✅ Success Indicators

Your analysis is successful if:

1. ✅ Global Moran's I is positive and significant (p < 0.05)
2. ✅ LM tests recommend SDM (both lag and error significant)
3. ✅ VIF < 10 for all variables
4. ✅ Spatial rho (ρ) is significant and 0 < ρ < 1
5. ✅ Residual Moran's I is not significant (p > 0.05)
6. ✅ Effects decomposition shows sensible magnitudes
7. ✅ Robustness checks show stable coefficients

---

**Ready to run?**

```bash
python run_complete_sdm_analysis.py
```

**Time to results**: 5-15 minutes ⏱️

---

*Last updated: November 28, 2025*
