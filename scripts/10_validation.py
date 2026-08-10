import pandas as pd
import numpy as np
import os
import sys

BASE = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

binary_file = os.path.join(
    BASE,
    "binary_df.csv"
)

vus_file = os.path.join(
    BASE,
    "vus_only_variants.csv"
)

visuals = os.path.join(
    BASE,
    "visuals"
)

results = os.path.join(
    BASE,
    "results"
)

print("=" * 70)
print("CLINVAR VUS EDA FINAL VALIDATION")
print("=" * 70)

# ==================================================
# FILE CHECK
# ==================================================

print("\n[1] FILE CHECK")

for file in [
    binary_file,
    vus_file
]:

    if os.path.exists(file):

        print(
            "PASS:",
            file
        )

    else:

        print(
            "FAIL:",
            file
        )

# ==================================================
# LOAD
# ==================================================

binary = pd.read_csv(
    binary_file,
    low_memory=False
)

vus_raw = pd.read_csv(
    vus_file,
    low_memory=False
)

def parse_to_numeric(s):
    s_str = s.astype(str).str.replace('.', 'nan', regex=False)
    split_df = s_str.str.split(',', expand=True)
    for c in split_df.columns:
        split_df[c] = pd.to_numeric(split_df[c], errors='coerce')
    return split_df.mean(axis=1)

vus = pd.DataFrame()
for col in vus_raw.columns:
    vus[col] = parse_to_numeric(vus_raw[col])

# ==================================================
# SHAPE
# ==================================================

print("\n[2] DATASET SHAPE")

print(
    "Binary:",
    binary.shape
)

print(
    "VUS:",
    vus.shape
)

# ==================================================
# MISSING
# ==================================================

print("\n[3] MISSING VALUES")

binary_missing = (
    binary.isna()
    .sum()
    .sum()
)

vus_missing = (
    vus.isna()
    .sum()
    .sum()
)

print(
    "Binary:",
    binary_missing
)

print(
    "VUS:",
    vus_missing
)

# ==================================================
# DUPLICATES
# ==================================================

print("\n[4] DUPLICATES")

print(
    "Binary:",
    binary.duplicated().sum()
)

print(
    "VUS:",
    vus.duplicated().sum()
)

# ==================================================
# NUMERICAL FEATURES
# ==================================================

print(
    "\n[5] NUMERICAL FEATURES"
)

numeric = vus.select_dtypes(
    include=np.number
)

for col in numeric.columns:
    print(
        " -",
        col
    )

# ==================================================
# ALPHAMISSENSE
# ==================================================

print(
    "\n[6] ALPHAMISSENSE"
)

if "alphamissense_pred" in binary.columns:

    print(
        binary[
            "alphamissense_pred"
        ]
        .value_counts()
        .sort_index()
    )

else:

    print(
        "alphamissense_pred not found"
    )

# ==================================================
# VISUAL CHECK
# ==================================================

print(
    "\n[7] VISUAL CHECK"
)

required_visuals = [

    "01_binary_feature_positive_rates.png",

    "02_binary_correlation_heatmap.png",

    "03_alphamissense_pred_breakdown.png",

    "04_vus_missing_data_profile.png",

    "05_vus_raw_score_distributions.png",

    "06_vus_allele_frequency_spectrum.png",

    "07_binary_tool_concordance_spectrum.png",

    "08_dataset_comparison_overview.png"

]

failed = 0

for filename in required_visuals:

    path = os.path.join(
        visuals,
        filename
    )

    if os.path.exists(path):

        print(
            "PASS:",
            filename
        )

    else:

        print(
            "FAIL:",
            filename
        )

        failed += 1

# ==================================================
# RESULT CHECK
# ==================================================

print(
    "\n[8] RESULT FILE CHECK"
)

required_results = [

    "dataset_summary.csv",

    "binary_positive_rates.csv",

    "continuous_statistics.csv",

    "distribution_statistics.csv",

    "binary_correlation.csv",

    "raw_correlation.csv",

    "raw_spearman_correlation.csv",

    "allele_frequency_summary.csv",

    "tool_concordance.csv",

    "concordance_groups.csv"

]

for filename in required_results:

    path = os.path.join(
        results,
        filename
    )

    if os.path.exists(path):

        print(
            "PASS:",
            filename
        )

    else:

        print(
            "FAIL:",
            filename
        )

        failed += 1

# ==================================================
# FINAL
# ==================================================

print("\n" + "=" * 70)

if failed == 0:

    print(
        "FINAL STATUS: PASS"
    )

else:

    print(
        "FINAL STATUS: FAIL"
    )

    print(
        "Missing items:",
        failed
    )

print("=" * 70)
