# AUGUST TASK1: ClinVar VUS Exploratory Data Analysis & Bioinformatics Pipeline

Cross-platform (Windows & Ubuntu Linux) implementation of the ClinVar Variants of Uncertain Significance (VUS) exploratory data analysis pipeline.

## Project Structure

```text
AUGUST TASK1/
├── binary_df.csv
├── vus_only_variants.csv
├── README.md
├── requirements.txt
│
├── scripts/
│   ├── 01_load_and_inventory.py
│   ├── 02_quality_control.py
│   ├── 03_binary_analysis.py
│   ├── 04_alphamissense_analysis.py
│   ├── 05_raw_score_analysis.py
│   ├── 06_correlation_analysis.py
│   ├── 07_allele_frequency.py
│   ├── 08_concordance.py
│   ├── 09_visualizations.py
│   ├── 10_validation.py
│   └── run_all.py
│
├── results/
│   ├── dataset_summary.csv
│   ├── binary_positive_rates.csv
│   ├── continuous_statistics.csv
│   ├── distribution_statistics.csv
│   ├── binary_correlation.csv
│   ├── raw_correlation.csv
│   ├── raw_spearman_correlation.csv
│   ├── allele_frequency_summary.csv
│   ├── tool_concordance.csv
│   └── concordance_groups.csv
│
├── visuals/
│   ├── 01_binary_feature_positive_rates.png
│   ├── 02_binary_correlation_heatmap.png
│   ├── 03_alphamissense_pred_breakdown.png
│   ├── 04_vus_missing_data_profile.png
│   ├── 05_vus_raw_score_distributions.png
│   ├── 06_vus_allele_frequency_spectrum.png
│   ├── 07_binary_tool_concordance_spectrum.png
│   └── 08_dataset_comparison_overview.png
│
├── logs/
│   └── full_analysis.log
│
└── report/
    ├── ANSWERED_50_QUESTIONS.md
    └── ClinVar_VUS_EDA_Report.md
```

## Setup & Environment

### Ubuntu Linux
```bash
python3 -m venv clinvar_eda_env
source clinvar_eda_env/bin/activate
pip install -r requirements.txt
```

### Windows (PowerShell)
```powershell
python -m venv clinvar_eda_env
.\clinvar_eda_env\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Running the Complete Pipeline

Run all 10 analysis steps with one command:

```bash
python scripts/run_all.py 2>&1 | tee logs/full_analysis.log
```

Or run validation directly:

```bash
python scripts/10_validation.py
```

Expected output:
```text
======================================================================
FINAL STATUS: PASS
======================================================================
```
