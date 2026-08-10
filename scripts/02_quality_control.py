import pandas as pd
import numpy as np
import os

BASE = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

RESULTS = os.path.join(
    BASE,
    "results"
)

binary_df = pd.read_csv(
    os.path.join(BASE, "binary_df.csv"),
    low_memory=False
)

vus_df = pd.read_csv(
    os.path.join(BASE, "vus_only_variants.csv"),
    low_memory=False
)

# ==================================================
# MISSING DATA
# ==================================================

def missing_report(df):

    report = pd.DataFrame({
        "Feature": df.columns,
        "Missing_Count": df.isna().sum().values,
        "Missing_Percent":
            df.isna().mean().values * 100,
        "Completeness_Percent":
            (1 - df.isna().mean().values) * 100
    })

    return report


binary_missing = missing_report(
    binary_df
)

vus_missing = missing_report(
    vus_df
)

binary_missing.to_csv(
    os.path.join(
        RESULTS,
        "binary_missing_data.csv"
    ),
    index=False
)

vus_missing.to_csv(
    os.path.join(
        RESULTS,
        "vus_missing_data.csv"
    ),
    index=False
)

# ==================================================
# DUPLICATES
# ==================================================

duplicate_summary = pd.DataFrame({
    "Dataset": [
        "binary_df.csv",
        "vus_only_variants.csv"
    ],

    "Total_Rows": [
        len(binary_df),
        len(vus_df)
    ],

    "Duplicate_Rows": [
        binary_df.duplicated().sum(),
        vus_df.duplicated().sum()
    ]
})

duplicate_summary[
    "Duplicate_Percent"
] = (
    duplicate_summary["Duplicate_Rows"] /
    duplicate_summary["Total_Rows"] *
    100
)

duplicate_summary.to_csv(
    os.path.join(
        RESULTS,
        "duplicate_summary.csv"
    ),
    index=False
)

# ==================================================
# INFINITE VALUES
# ==================================================

numeric_binary = binary_df.select_dtypes(
    include=np.number
)

numeric_vus = vus_df.select_dtypes(
    include=np.number
)

infinite_summary = pd.DataFrame({
    "Dataset": [
        "binary_df",
        "vus_only_variants"
    ],

    "Infinite_Values": [
        np.isinf(numeric_binary).sum().sum() if not numeric_binary.empty else 0,
        np.isinf(numeric_vus).sum().sum() if not numeric_vus.empty else 0
    ]
})

infinite_summary.to_csv(
    os.path.join(
        RESULTS,
        "infinite_values.csv"
    ),
    index=False
)

print("=" * 60)
print("QUALITY CONTROL COMPLETE")
print("=" * 60)

print("\nBinary missing:")
print(binary_missing)

print("\nVUS missing:")
print(vus_missing)

print("\nDuplicates:")
print(duplicate_summary)

print("\nInfinite values:")
print(infinite_summary)
