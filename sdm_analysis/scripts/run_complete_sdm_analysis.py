"""
MASTER SCRIPT: Complete Spatial Durbin Model Analysis
YELP BI 2025 - Rice Price Prediction

This script orchestrates the entire SDM analysis pipeline:
1. Data Preparation & Validation
2. Exploratory Spatial Data Analysis
3. Model Specification & Diagnostics
4. Model Estimation
5. Output & Interpretation
6. Validation & Robustness
7. Policy Simulation

Usage:
    python run_complete_sdm_analysis.py

Requirements:
    pip install pandas numpy scipy statsmodels pysal spreg libpysal esda splot geopandas matplotlib seaborn
"""

import os
import sys
from datetime import datetime
import warnings

warnings.filterwarnings('ignore')

# Import the analysis classes
from sdm_analysis_complete import SpatialDurbinAnalysis
from sdm_estimation_advanced import SDMEstimation


def print_banner(text):
    """Print formatted banner"""
    print("\n" + "="*80)
    print(text.center(80))
    print("="*80 + "\n")


def main():
    """Main execution function"""

    print_banner("SPATIAL DURBIN MODEL - COMPLETE ANALYSIS")
    print(f"Analysis started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\nThis script will run all 7 phases of the SDM analysis.")
    print("Expected time: 5-15 minutes depending on your machine.\n")

    input("Press Enter to continue...")

    # =========================================================================
    # PART 1: DIAGNOSTIC PHASES (1-3)
    # =========================================================================

    print_banner("PART 1: DIAGNOSTIC PHASES (1-3)")

    print("Initializing SDM Analysis...")
    sdm = SpatialDurbinAnalysis(base_dir='.')

    try:
        # FASE 1: Data Preparation & Validation
        print_banner("FASE 1: DATA PREPARATION & VALIDATION")

        print("\n[1/7] Running FASE 1A: Data Quality Check...")
        sdm.fase1a_check_data_quality()

        print("\n[2/7] Running FASE 1B: Dataset Merging...")
        sdm.fase1b_merge_datasets()

        # FASE 2: Exploratory Spatial Data Analysis
        print_banner("FASE 2: EXPLORATORY SPATIAL DATA ANALYSIS")

        print("\n[3/7] Running FASE 2A: Global Moran's I...")
        sdm.fase2a_global_morans_i(commodity='com_1')

        print("\n[4/7] Running FASE 2B: Local Moran's I (LISA)...")
        sdm.fase2b_local_morans_i(commodity='com_1')

        print("\n[5/7] Running FASE 2C: Spatial Weights Construction...")
        sdm.fase2c_construct_spatial_weights()

        # FASE 3: Model Specification & Diagnostics
        print_banner("FASE 3: MODEL SPECIFICATION & DIAGNOSTICS")

        print("\n[6/7] Running FASE 3A: Stationarity Tests...")
        sdm.fase3a_stationarity_tests()

        print("\n[7/7] Running FASE 3B: Multicollinearity Test...")
        sdm.fase3b_multicollinearity_test()

        print("\n[8/7] Running FASE 3C: Heteroskedasticity Test...")
        sdm.fase3c_heteroskedasticity_test()

        print("\n[9/7] Running FASE 3D: Spatial Diagnostic Tests...")
        diag_results, recommendation = sdm.fase3d_spatial_diagnostics(commodity='com_1')

        print("\n[10/7] Running FASE 3E: Hausman Test...")
        fe_recommendation = sdm.fase3e_hausman_test()

        print_banner("PART 1 COMPLETED: DIAGNOSTIC PHASES")

        print("\n" + "="*60)
        print("DIAGNOSTIC TEST SUMMARY")
        print("="*60)

        print(f"\n1. Spatial Model Recommendation: {recommendation}")
        print(f"2. Fixed/Random Effects: {fe_recommendation}")
        print(f"3. Results saved in: sdm_results/fase1/, fase2/, fase3/")

        print("\n" + "-"*60)
        input("\nPart 1 completed. Press Enter to continue to Part 2 (Estimation)...")

    except Exception as e:
        print(f"\n✗ ERROR in Part 1: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    # =========================================================================
    # PART 2: ESTIMATION & ANALYSIS PHASES (4-7)
    # =========================================================================

    print_banner("PART 2: ESTIMATION & ANALYSIS PHASES (4-7)")

    print("Initializing SDM Estimation...")
    sdm_est = SDMEstimation(base_dir='.')

    try:
        # Load preprocessed data
        print("\nLoading preprocessed data...")
        sdm_est.load_preprocessed_data()
        sdm_est.reconstruct_spatial_weights()

        # FASE 4: Model Estimation
        print_banner("FASE 4: SPATIAL DURBIN MODEL ESTIMATION")

        print("\n[11/7] Estimating SDM with Fixed Effects...")
        model = sdm_est.fase4_estimate_sdm(commodity='com_1', w_type='knn3')

        # FASE 5: Output & Interpretation
        print_banner("FASE 5: OUTPUT & INTERPRETATION")

        print("\n[12/7] Running FASE 5A: Model Fit Statistics...")
        fit_stats = sdm_est.fase5a_model_fit_statistics()

        print("\n[13/7] Running FASE 5B: Effects Decomposition...")
        effects = sdm_est.fase5b_effects_decomposition()

        print("\n[14/7] Running FASE 5C: Spatial Multiplier Analysis...")
        multipliers = sdm_est.fase5c_spatial_multiplier()

        # FASE 6: Validation & Robustness
        print_banner("FASE 6: VALIDATION & ROBUSTNESS")

        print("\n[15/7] Running FASE 6A: Residual Diagnostics...")
        resid_diag = sdm_est.fase6a_residual_diagnostics()

        print("\n[16/7] Running FASE 6B: Robustness Checks...")
        robust_results = sdm_est.fase6b_robustness_checks()

        # FASE 7: Policy Simulation
        print_banner("FASE 7: POLICY SIMULATIONS")

        print("\n[17/7] Running Policy Simulations...")
        simulations = sdm_est.fase7_policy_simulations()

        print_banner("PART 2 COMPLETED: ESTIMATION & ANALYSIS")

        print("\n" + "="*60)
        print("ANALYSIS SUMMARY")
        print("="*60)

        if fit_stats is not None and len(fit_stats) > 0:
            print("\nModel Fit:")
            if 'Pseudo_R2' in fit_stats.columns:
                print(f"  - Pseudo R²: {fit_stats['Pseudo_R2'].values[0]:.4f}")
            if 'RMSE' in fit_stats.columns:
                print(f"  - RMSE: Rp {fit_stats['RMSE'].values[0]:.2f}/kg")
            if 'MAPE' in fit_stats.columns:
                print(f"  - MAPE: {fit_stats['MAPE'].values[0]:.2f}%")

        print("\nResults saved in:")
        print("  - sdm_results/fase4/ (Model estimation)")
        print("  - sdm_results/fase5/ (Effects & multipliers)")
        print("  - sdm_results/fase6/ (Diagnostics & robustness)")
        print("  - sdm_results/fase7/ (Policy simulations)")

    except Exception as e:
        print(f"\n✗ ERROR in Part 2: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    # =========================================================================
    # FINAL SUMMARY
    # =========================================================================

    print_banner("ANALYSIS COMPLETE!")

    print(f"\nAnalysis finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    print("\n" + "="*80)
    print("ALL 7 PHASES COMPLETED SUCCESSFULLY!")
    print("="*80)

    print("\n📊 DELIVERABLES:")
    print("\n1. Data Quality Report:")
    print("   - sdm_results/fase1/1a_missing_values.csv")
    print("   - sdm_results/fase1/1a_descriptive_stats.csv")
    print("   - sdm_results/fase1/1b_merged_dataset.csv")

    print("\n2. ESDA Results:")
    print("   - sdm_results/fase2/2a_global_morans_i.csv")
    print("   - sdm_results/fase2/2b_lisa_clusters.csv")
    print("   - sdm_results/fase2/2c_distance_matrix_km.csv")

    print("\n3. Diagnostic Tests:")
    print("   - sdm_results/fase3/3a_stationarity_tests.csv")
    print("   - sdm_results/fase3/3b_vif_results.csv")
    print("   - sdm_results/fase3/3c_heteroskedasticity_test.csv")
    print("   - sdm_results/fase3/3d_spatial_diagnostics.csv")

    print("\n4. SDM Estimation Output:")
    print("   - sdm_results/fase4/4_sdm_summary.txt")
    print("   - sdm_results/fase4/4_coefficients.csv")

    print("\n5. Effects Decomposition:")
    print("   - sdm_results/fase5/5a_model_fit.csv")
    print("   - sdm_results/fase5/5b_effects_decomposition.csv")
    print("   - sdm_results/fase5/5c_spatial_multiplier_matrix.csv")

    print("\n6. Validation Results:")
    print("   - sdm_results/fase6/6a_residual_diagnostics.csv")
    print("   - sdm_results/fase6/6b_robustness_checks.csv")

    print("\n7. Policy Simulations:")
    print("   - sdm_results/fase7/7_policy_simulations.csv")

    print("\n" + "="*80)
    print("🎉 ANALYSIS COMPLETE! Check sdm_results/ for all outputs.")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
