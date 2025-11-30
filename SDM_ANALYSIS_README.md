# Spatial Durbin Model (SDM) Analysis - Complete Implementation

## YELP BI 2025: Rice Price Prediction

This repository contains a complete implementation of Spatial Durbin Model analysis for rice price prediction in Java, Indonesia, following best practices in spatial econometrics.

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Methodology](#methodology)
3. [Requirements](#requirements)
4. [Installation](#installation)
5. [Usage](#usage)
6. [Output Structure](#output-structure)
7. [Interpretation Guide](#interpretation-guide)

---

## 🎯 Overview

This analysis implements a **7-phase Spatial Durbin Model (SDM)** to:
- Analyze rice price dynamics across 15 locations in Java
- Quantify spatial spillover effects
- Decompose direct vs indirect effects
- Simulate policy interventions

### Key Features

✅ **Complete diagnostic testing** (stationarity, multicollinearity, heteroskedasticity)
✅ **Spatial autocorrelation analysis** (Global Moran's I, LISA)
✅ **Multiple spatial weights** (distance-based, k-NN, contiguity)
✅ **Effects decomposition** (Direct, Indirect, Total)
✅ **Robustness checks** (alternative specifications)
✅ **Policy simulations** (BBM shock, production increase, extreme weather)

---

## 📊 Methodology

### 7 Analysis Phases

#### **FASE 1: Data Preparation & Validation**
- Check missing values and panel structure
- Merge 5 datasets (PIHPS, Weather, BBM, Luas Panen, Distance)
- Validate data alignment and quality

#### **FASE 2: Exploratory Spatial Data Analysis (ESDA)**
- Global Moran's I (spatial autocorrelation test)
- Local Moran's I / LISA (cluster detection)
- Spatial weights matrix construction

#### **FASE 3: Model Specification & Diagnostic Tests**
- Stationarity tests (Augmented Dickey-Fuller)
- Multicollinearity tests (VIF)
- Heteroskedasticity tests (Breusch-Pagan)
- Spatial model selection (LM-Lag, LM-Error, Robust LM)
- Hausman test (Fixed vs Random Effects)

#### **FASE 4: Model Estimation**
- Spatial Durbin Model (SDM) with Fixed Effects
- Generalized Method of Moments (GM) estimation
- Maximum Likelihood (ML) estimation (fallback)

#### **FASE 5: Output & Interpretation**
- Model fit statistics (R², RMSE, MAPE, AIC, BIC)
- Effects decomposition (Direct, Indirect, Total)
- Spatial multiplier analysis

#### **FASE 6: Validation & Robustness**
- Residual diagnostics (spatial autocorrelation)
- Robustness checks (alternative weights matrices)
- Out-of-sample validation (optional)

#### **FASE 7: Policy Simulation**
- Scenario 1: BBM price shock (+15%)
- Scenario 2: Production increase (+10,000 ha)
- Scenario 3: Extreme weather (+50mm rainfall)

---

## 🛠️ Requirements

### Python Version
- Python 3.8 or higher

### Required Libraries

```txt
pandas>=1.3.0
numpy>=1.21.0
scipy>=1.7.0
statsmodels>=0.13.0
pysal>=2.6.0
spreg>=1.2.4
libpysal>=4.6.0
esda>=2.4.0
splot>=1.1.5
geopandas>=0.10.0
matplotlib>=3.4.0
seaborn>=0.11.0
```

### Data Requirements

The following datasets must be present in the base directory:

1. **PIHPS Data**: `cleaned_pihps_data/cleaned_combined.csv`
2. **Weather Data**: `weather_pihps_historical.csv`
3. **BBM Data**: `indonesia_gasoline_prices_5y.csv`
4. **Luas Panen**: `bps-jakarta-data/jawa_barat_rice_production_2020_2024.csv`
5. **Facility Data**: `supply_chain_spatial_fast/supply_chain_facilities_20251128_141527.csv`

---

## 📥 Installation

### Step 1: Clone or Download

```bash
cd "D:\Arsip Kompetisi\YELP BI 2025"
```

### Step 2: Install Dependencies

```bash
pip install pandas numpy scipy statsmodels pysal spreg libpysal esda splot geopandas matplotlib seaborn
```

### Step 3: Verify Data Files

Ensure all required datasets are in the correct locations (see Data Requirements).

---

## 🚀 Usage

### Option 1: Run Complete Analysis (Recommended)

Run all 7 phases automatically:

```bash
python run_complete_sdm_analysis.py
```

This will:
1. Run all diagnostic tests (Phases 1-3)
2. Estimate the SDM model (Phase 4)
3. Decompose effects (Phase 5)
4. Validate results (Phase 6)
5. Run policy simulations (Phase 7)

**Expected runtime**: 5-15 minutes

### Option 2: Run Phases Separately

#### Run Diagnostic Phases (1-3):

```python
from sdm_analysis_complete import SpatialDurbinAnalysis

sdm = SpatialDurbinAnalysis(base_dir='.')

# Phase 1
sdm.fase1a_check_data_quality()
sdm.fase1b_merge_datasets()

# Phase 2
sdm.fase2a_global_morans_i(commodity='com_1')
sdm.fase2b_local_morans_i(commodity='com_1')
sdm.fase2c_construct_spatial_weights()

# Phase 3
sdm.fase3a_stationarity_tests()
sdm.fase3b_multicollinearity_test()
sdm.fase3c_heteroskedasticity_test()
sdm.fase3d_spatial_diagnostics(commodity='com_1')
sdm.fase3e_hausman_test()
```

#### Run Estimation Phases (4-7):

```python
from sdm_estimation_advanced import SDMEstimation

sdm_est = SDMEstimation(base_dir='.')

# Load data
sdm_est.load_preprocessed_data()
sdm_est.reconstruct_spatial_weights()

# Phase 4-7
sdm_est.fase4_estimate_sdm(commodity='com_1', w_type='knn3')
sdm_est.fase5a_model_fit_statistics()
sdm_est.fase5b_effects_decomposition()
sdm_est.fase5c_spatial_multiplier()
sdm_est.fase6a_residual_diagnostics()
sdm_est.fase6b_robustness_checks()
sdm_est.fase7_policy_simulations()
```

---

## 📂 Output Structure

All results are saved in `sdm_results/` directory:

```
sdm_results/
├── fase1/                          # Data Preparation
│   ├── 1a_missing_values.csv
│   ├── 1a_missing_by_commodity.csv
│   ├── 1a_missing_by_location.csv
│   ├── 1a_time_consistency.csv
│   ├── 1a_descriptive_stats.csv
│   ├── 1b_merged_dataset.csv
│   ├── 1b_merge_missing_summary.csv
│   └── 1b_correlation_matrix.csv
│
├── fase2/                          # ESDA
│   ├── 2a_global_morans_i.csv
│   ├── 2b_lisa_clusters.csv
│   ├── 2b_cluster_summary.csv
│   ├── 2c_weights_comparison.csv
│   └── 2c_distance_matrix_km.csv
│
├── fase3/                          # Diagnostic Tests
│   ├── 3a_stationarity_tests.csv
│   ├── 3b_vif_results.csv
│   ├── 3b_correlation_matrix.csv
│   ├── 3c_heteroskedasticity_test.csv
│   ├── 3d_spatial_diagnostics.csv
│   ├── 3d_recommendation.txt
│   └── 3e_hausman_recommendation.txt
│
├── fase4/                          # Model Estimation
│   ├── 4_sdm_summary.txt
│   └── 4_coefficients.csv
│
├── fase5/                          # Effects & Interpretation
│   ├── 5a_model_fit.csv
│   ├── 5b_effects_decomposition.csv
│   ├── 5c_spatial_multiplier_matrix.csv
│   └── 5c_multiplier_summary.csv
│
├── fase6/                          # Validation
│   ├── 6a_residual_diagnostics.csv
│   └── 6b_robustness_checks.csv
│
└── fase7/                          # Policy Simulations
    └── 7_policy_simulations.csv
```

---

## 📖 Interpretation Guide

### Key Outputs Explained

#### 1. Global Moran's I (`2a_global_morans_i.csv`)

**What it shows**: Whether rice prices are spatially clustered

- **Moran's I > 0**: Positive spatial autocorrelation (high prices cluster together)
- **P-value < 0.05**: Statistically significant clustering
- **Interpretation**: If I = 0.65*** → Strong spatial clustering detected

#### 2. LISA Clusters (`2b_lisa_clusters.csv`)

**What it shows**: Local spatial patterns per region

- **HH (High-High)**: Regions with high prices surrounded by high prices → "Hot spots"
- **LL (Low-Low)**: Regions with low prices surrounded by low prices → "Cold spots"
- **HL (High-Low)**: High price region surrounded by low → Spatial outlier
- **LH (Low-High)**: Low price region surrounded by high → Spatial outlier

#### 3. SDM Coefficients (`4_coefficients.csv`)

**Direct variables** (e.g., `bbm_price_idr`):
- Effect of BBM price in location i on rice price in location i

**Spatial lag variables** (e.g., `W_bbm_price_idr`):
- Effect of BBM price in neighboring locations on local rice price

**Rho (ρ)**:
- Spatial autoregressive parameter
- If ρ = 0.42 → 1% price increase in neighbors → 0.42% local price increase

#### 4. Effects Decomposition (`5b_effects_decomposition.csv`)

**Direct Effect**:
- Impact of X in location i on Y in location i
- Example: BBM +Rp 1000 → local price +Rp 680

**Indirect Effect (Spillover)**:
- Impact of X in location j on Y in location i
- Example: BBM +Rp 1000 in neighbor → local price +Rp 450

**Total Effect**:
- Direct + Indirect = Total system impact
- Example: Total = Rp 1130

#### 5. Spatial Multiplier (`5c_spatial_multiplier_matrix.csv`)

**What it shows**: How a shock in one location propagates through the spatial network

- **Diagonal values**: Own-location multiplier (direct + feedback effects)
- **Off-diagonal values**: Cross-location spillovers
- **Interpretation**: Jakarta→Jakarta multiplier = 1.82 means a Rp 1 shock in Jakarta ultimately causes Rp 1.82 total effect in Jakarta

#### 6. Policy Simulations (`7_policy_simulations.csv`)

**Scenario results format**:
```
BBM +15% (Rp 1500):
  - Direct: +Rp 1020/kg
  - Spatial: +Rp 675/kg
  - Total: +Rp 1850/kg (with multiplier)
```

**Use cases**:
- Estimate impact of fuel subsidy removal
- Assess effect of expanding rice production
- Predict price response to extreme weather

---

## 🔍 Diagnostic Test Interpretation

### Stationarity (ADF Test)
- **H0**: Variable has unit root (non-stationary)
- **Decision**: If p-value < 0.05 → Reject H0 → Data is stationary ✓
- **Action if non-stationary**: Use time fixed effects or differencing

### Multicollinearity (VIF)
- **VIF < 5**: Low multicollinearity ✓
- **VIF 5-10**: Moderate multicollinearity (monitor)
- **VIF > 10**: High multicollinearity (consider dropping variable)

### Heteroskedasticity (Breusch-Pagan)
- **H0**: Homoskedasticity (constant variance)
- **Decision**: If p-value < 0.05 → Heteroskedasticity present
- **Action**: Use robust standard errors (White/HC3)

### Spatial Model Selection (LM Tests)
- **Both LM-Lag & LM-Error significant** → Use Spatial Durbin Model (SDM) ✓
- **Only LM-Lag significant** → Use Spatial Lag Model (SAR)
- **Only LM-Error significant** → Use Spatial Error Model (SEM)
- **Neither significant** → OLS sufficient

---

## 📊 Visualization Recommendations

While this implementation focuses on numerical output, you can create visualizations using:

### LISA Cluster Map
```python
import geopandas as gpd
import matplotlib.pyplot as plt

# Load LISA results
lisa_df = pd.read_csv('sdm_results/fase2/2b_lisa_clusters.csv')

# Create map (requires shapefile)
# gdf.plot(column='cluster_type', legend=True, cmap='RdYlGn')
```

### Coefficient Plot (Forest Plot)
```python
import matplotlib.pyplot as plt
import seaborn as sns

coefs = pd.read_csv('sdm_results/fase4/4_coefficients.csv')

plt.figure(figsize=(10, 6))
plt.errorbar(coefs['Coefficient'], range(len(coefs)),
             xerr=coefs['Std_Error'], fmt='o')
plt.yticks(range(len(coefs)), coefs['Variable'])
plt.axvline(0, color='red', linestyle='--')
plt.xlabel('Coefficient Estimate')
plt.title('SDM Coefficient Estimates with 95% CI')
plt.tight_layout()
plt.savefig('sdm_results/coefficient_plot.png', dpi=300)
```

---

## ⚠️ Common Issues & Solutions

### Issue 1: Import Error for `spreg` or `libpysal`
**Solution**:
```bash
pip install --upgrade pysal spreg libpysal esda
```

### Issue 2: "No spatial impacts available"
**Cause**: Model doesn't support impact decomposition
**Solution**: Ensure `spat_impacts=['simple', 'full']` is set in GM_Lag/ML_Lag

### Issue 3: Singular matrix error
**Cause**: Perfect multicollinearity or insufficient variation
**Solution**: Check VIF results, drop highly correlated variables

### Issue 4: Spatial weights mismatch
**Cause**: Different ordering between data and weights matrix
**Solution**: Ensure locations are sorted consistently before creating W

---

## 📚 References

### Theoretical Background
1. LeSage, J., & Pace, R. K. (2009). *Introduction to Spatial Econometrics*. CRC Press.
2. Elhorst, J. P. (2014). *Spatial Econometrics: From Cross-Sectional Data to Spatial Panels*. Springer.
3. Anselin, L. (1988). *Spatial Econometrics: Methods and Models*. Springer.

### Software Documentation
- PySAL: https://pysal.org/
- spreg: https://github.com/pysal/spreg
- libpysal: https://github.com/pysal/libpysal

---

## 📞 Support

For questions about this implementation:
1. Check the diagnostic test outputs first
2. Review the interpretation guide above
3. Consult PySAL documentation: https://pysal.org/notebooks/intro

---

## 📝 Citation

If you use this code, please cite:

```
Spatial Durbin Model Analysis for Rice Price Prediction
YELP BI 2025 Competition
Implementation based on PySAL ecosystem
```

---

## ✅ Checklist Before Running

- [ ] All 5 datasets are in correct locations
- [ ] Python 3.8+ is installed
- [ ] All required libraries are installed (`pip install ...`)
- [ ] Sufficient disk space (≈500MB for results)
- [ ] No conflicting `sdm_results/` directory exists (or backup first)

---

**Last Updated**: November 28, 2025
**Version**: 1.0
**Author**: YELP BI 2025 Analysis Team
