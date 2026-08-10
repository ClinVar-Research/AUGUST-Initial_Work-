# ClinVar VUS Exploratory Data Analysis Report

**Folder:** [`AUGUST TASK1`](file:///d:/FINAL_DATA_CLINVAR_VUS/AUGUST%20TASK1)  
**Date:** August 10, 2026  
**Primary Datasets:**
1. `binary_df.csv` (368,851 variants × 12 features)
2. `vus_only_variants.csv` (369,993 variants × 14 features)

---

## 1. Executive Summary
- **Volume & Dimensions:** The binarized matrix `binary_df.csv` contains 368,851 variants across 12 features. The raw VUS matrix `vus_only_variants.csv` contains 369,993 variants across 14 raw feature columns.
- **Predictor Threshold Heterogeneity:** Computational tools demonstrate vast variation in their positivity (pathogenic call) rates:
  - High-permissiveness tools: **CADD_phred (89.73%)** and **GERP++RS (88.41%)** classify the vast majority of variants as pathogenic/deleterious under standard cutoff thresholds.
  - Low-permissiveness tools: **SIFT (10.73%)**, **metaSVM (19.65%)**, **AlphaMissense score (23.76%)**, and **VARITY_r (28.64%)** maintain stricter criteria.
- **AlphaMissense Classification:** AlphaMissense categorizes **60.90% (224,626)** of variants as Benign, **20.10% (74,124)** as Ambiguous (0.5), and **19.01% (70,101)** as Pathogenic.
- **Population Allele Frequency Spectrum:** All VUS variants demonstrate ultra-rare population allele frequency distributions (Mean AF ≈ 0.0001, Median AF = 0.0), confirming their enrichment in rare genomic variants where clinical interpretation is challenging.

---

## 2. Generated Visualizations Summary in [`visuals/`](file:///d:/FINAL_DATA_CLINVAR_VUS/AUGUST%20TASK1/visuals)

1. `01_binary_feature_positive_rates.png` — Pathogenic positivity rate comparison across binary tools.
2. `02_binary_correlation_heatmap.png` — Correlation matrix of binarized pathogenicity annotations.
3. `03_alphamissense_pred_breakdown.png` — AlphaMissense 3-class and binary distribution.
4. `04_vus_missing_data_profile.png` — Data completeness profile across columns.
5. `05_vus_raw_score_distributions.png` — Histograms and KDE curves of raw computational scores.
6. `06_vus_allele_frequency_spectrum.png` — Log-scale population allele frequency distributions.
7. `07_binary_tool_concordance_spectrum.png` — Distribution of variant pathogenicity concordance.
8. `08_dataset_comparison_overview.png` — Architectural comparison between binarized and raw datasets.

---

## 3. Results Summary in [`results/`](file:///d:/FINAL_DATA_CLINVAR_VUS/AUGUST%20TASK1/results)

- `dataset_summary.csv` — Dataset record counts, column counts, missing values, duplicates.
- `binary_positive_rates.csv` — Rank-ordered positive call rates for all binary predictors.
- `continuous_statistics.csv` — Min, 25%, median, mean, 75%, max, std for raw score features.
- `distribution_statistics.csv` — Skewness and kurtosis metrics for raw continuous features.
- `binary_correlation.csv` — Pearson correlation matrix for binarized predictions.
- `raw_correlation.csv` — Pearson correlation matrix for raw continuous predictions.
- `raw_spearman_correlation.csv` — Spearman rank correlation matrix for continuous features.
- `allele_frequency_summary.csv` — Allele frequency spectrum, zero count, and ultra-rare variant counts.
- `tool_concordance.csv` — Distribution of variants by number of concordant positive tools.
- `concordance_groups.csv` — Variant counts across consensus categories (Benign vs Moderate vs Pathogenic).

---

## 4. Final Validation

Executing `python scripts/10_validation.py` verifies all required files, dataset shapes, missing data profiles, duplicate checks, numerical features, AlphaMissense classes, 8 visual figures, and 10 result CSVs:

```text
======================================================================
FINAL STATUS: PASS
======================================================================
```
