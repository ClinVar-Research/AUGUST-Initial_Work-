# ClinVar VUS Exploratory Data Analysis & Bioinformatics Pipeline (Ubuntu Linux Guide)

A fully reproducible, modular Python pipeline for analyzing **Variants of Uncertain Significance (VUS)** from ClinVar and evaluating ensemble in-silico pathogenicity prediction tools.

**GitHub Repository:** [https://github.com/ClinVar-Research/AUGUST-Initial_Work-](https://github.com/ClinVar-Research/AUGUST-Initial_Work-)

---

## 1. Directory & File Structure

```text
AUGUST_TASK1/
├── binary_df.csv                           # Binarized ClinVar predictor matrix (368,851 × 12)
├── vus_only_variants.csv                   # Raw continuous VUS matrix (369,993 × 14)
├── README.md                               # Project documentation & Ubuntu execution guide
├── requirements.txt                        # Python package dependencies
├── run_pipeline_log.py                     # Synchronous pipeline logger
│
├── scripts/                                # Modular Analysis Scripts (11 Files)
│   ├── 01_load_and_inventory.py            # Step 1: Load datasets & verify shapes/dtypes
│   ├── 02_quality_control.py               # Step 2: Quality control, missing data & duplicates
│   ├── 03_binary_analysis.py               # Step 3: Binary feature pathogenic call rates
│   ├── 04_alphamissense_analysis.py        # Step 4: AlphaMissense 3-class distribution
│   ├── 05_raw_score_analysis.py            # Step 5: Continuous raw score statistics & moments
│   ├── 06_correlation_analysis.py          # Step 6: Pearson & Spearman rank correlations
│   ├── 07_allele_frequency.py              # Step 7: Population allele frequency spectrum
│   ├── 08_concordance.py                   # Step 8: Multi-tool consensus spectrum
│   ├── 09_visualizations.py                # Step 9: Render 8 publication-grade 300 DPI figures
│   ├── 10_validation.py                    # Step 10: Complete pipeline validation suite
│   └── run_all.py                          # Master execution runner
│
├── results/                                # Output Analysis Tables (17 CSVs)
│   ├── dataset_summary.csv
│   ├── binary_dtypes.csv / vus_dtypes.csv
│   ├── binary_missing_data.csv / vus_missing_data.csv
│   ├── duplicate_summary.csv / infinite_values.csv
│   ├── binary_positive_rates.csv
│   ├── alphamissense_distribution.csv
│   ├── continuous_statistics.csv
│   ├── distribution_statistics.csv
│   ├── binary_correlation.csv / raw_correlation.csv / raw_spearman_correlation.csv
│   ├── allele_frequency_summary.csv
│   ├── tool_concordance.csv
│   └── concordance_groups.csv
│
├── visuals/                                # High-Resolution PNG Figures (8 Files)
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
│   └── full_analysis.log                   # Execution log & terminal output
│
└── report/                                 # Documentation & Assignment Answers
    ├── ANSWERED_50_QUESTIONS.md            # Detailed answers to all 50 bioinformatics questions
    └── ClinVar_VUS_EDA_Report.md           # Primary EDA research report
```

---

## 2. Ubuntu Linux System Setup

Open your terminal on Ubuntu (`Ctrl + Alt + T`) and execute the following setup commands:

### Step 2.1 — Update System Packages
```bash
sudo apt update
sudo apt upgrade -y
```

### Step 2.2 — Install Python 3, pip, Virtual Environment & Utilities
```bash
sudo apt install -y python3 python3-pip python3-venv tree xdg-utils
```

Verify Python installation:
```bash
python3 --version
```
*Expected output:* `Python 3.8+` or higher.

---

## 3. Environment Setup & Dependency Installation

### Step 3.1 — Clone or Move to the Repository Folder
```bash
git clone https://github.com/ClinVar-Research/AUGUST-Initial_Work-.git AUGUST_TASK1
cd AUGUST_TASK1
```

### Step 3.2 — Create Python Virtual Environment
```bash
python3 -m venv clinvar_eda_env
```

### Step 3.3 — Activate Virtual Environment
```bash
source clinvar_eda_env/bin/activate
```
*(Your terminal prompt will now show `(clinvar_eda_env)`).*

### Step 3.4 — Upgrade pip & Install Package Dependencies
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Verify package installation:
```bash
python -c "import pandas, numpy, matplotlib, seaborn, scipy, sklearn; print('ALL PACKAGES OK')"
```
*Expected output:* `ALL PACKAGES OK`

---

## 4. How to Run the Complete Pipeline on Ubuntu

### Option A — One-Command Master Pipeline Execution (Recommended)
Run all 10 analysis steps sequentially and log terminal output:
```bash
python3 scripts/run_all.py 2>&1 | tee logs/full_analysis.log
```

### Option B — Step-by-Step Manual Script Execution
You can also execute each modular script independently:

```bash
# Step 1: Inventory datasets
python3 scripts/01_load_and_inventory.py

# Step 2: Quality control & missing value analysis
python3 scripts/02_quality_control.py

# Step 3: Binary predictor positive call rate analysis
python3 scripts/03_binary_analysis.py

# Step 4: AlphaMissense 3-class breakdown
python3 scripts/04_alphamissense_analysis.py

# Step 5: Continuous raw score descriptive statistics
python3 scripts/05_raw_score_analysis.py

# Step 6: Pearson & Spearman rank correlations
python3 scripts/06_correlation_analysis.py

# Step 7: Population allele frequency spectrum
python3 scripts/07_allele_frequency.py

# Step 8: Multi-tool pathogenicity concordance spectrum
python3 scripts/08_concordance.py

# Step 9: Render 8 high-resolution 300 DPI figure PNGs
python3 scripts/09_visualizations.py

# Step 10: Run full pipeline validation suite
python3 scripts/10_validation.py
```

---

## 5. How to View Output Results & Figures on Ubuntu

### View Numerical Statistics Tables
```bash
cat results/dataset_summary.csv
cat results/binary_positive_rates.csv
cat results/continuous_statistics.csv
cat results/allele_frequency_summary.csv
```

### Open Visual Figures on Ubuntu Desktop
To view generated PNG plots using Ubuntu's default image viewer:
```bash
# Open individual figures
xdg-open visuals/01_binary_feature_positive_rates.png
xdg-open visuals/02_binary_correlation_heatmap.png

# Or open the entire visuals folder in Ubuntu Files manager
xdg-open visuals/
```

---

## 6. Pipeline Validation

To verify that all output CSVs, PNG figures, missing value profiles, and shapes are valid:

```bash
python3 scripts/10_validation.py
```

Expected final terminal output:
```text
======================================================================
FINAL STATUS: PASS
======================================================================
```

---

## 7. Key Methodological Principles & Clinical Notes

1. **Reproducibility:** All numerical metrics are computed dynamically directly from `binary_df.csv` and `vus_only_variants.csv`.
2. **Computational Evidence vs. Ground Truth:** High positivity rates in tools like `CADD_phred` (89.73%) or `GERP++` (88.41%) reflect threshold permissiveness, not clinical accuracy.
3. **ACMG/AMP Guidelines:** According to ACMG/AMP clinical interpretation guidelines, in-silico computational predictions provide supporting evidence only (PP3/BP4 criteria) and cannot replace functional experimental assays or clinical co-segregation studies.

---
*Maintained by ClinVar Research Group.*
