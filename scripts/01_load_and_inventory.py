import pandas as pd
import os

BASE = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

BINARY_FILE = os.path.join(
    BASE,
    "binary_df.csv"
)

VUS_FILE = os.path.join(
    BASE,
    "vus_only_variants.csv"
)

RESULTS = os.path.join(
    BASE,
    "results"
)

os.makedirs(
    RESULTS,
    exist_ok=True
)

print("=" * 70)
print("CLINVAR DATASET INVENTORY")
print("=" * 70)

# --------------------------------------------------
# Load datasets
# --------------------------------------------------

print("\nLoading binary dataset...")

binary_df = pd.read_csv(
    BINARY_FILE,
    low_memory=False
)

print("Binary dataset loaded.")

print("\nLoading VUS dataset...")

vus_df = pd.read_csv(
    VUS_FILE,
    low_memory=False
)

print("VUS dataset loaded.")

# --------------------------------------------------
# Dimensions
# --------------------------------------------------

print("\nBinary shape:")
print(binary_df.shape)

print("\nVUS shape:")
print(vus_df.shape)

# --------------------------------------------------
# Column names
# --------------------------------------------------

print("\nBinary columns:")

for col in binary_df.columns:
    print(" -", col)

print("\nVUS columns:")

for col in vus_df.columns:
    print(" -", col)

# --------------------------------------------------
# Dataset summary
# --------------------------------------------------

summary = pd.DataFrame({
    "Dataset": [
        "binary_df.csv",
        "vus_only_variants.csv"
    ],
    "Rows": [
        binary_df.shape[0],
        vus_df.shape[0]
    ],
    "Columns": [
        binary_df.shape[1],
        vus_df.shape[1]
    ],
    "Missing_Values": [
        binary_df.isna().sum().sum(),
        vus_df.isna().sum().sum()
    ],
    "Duplicate_Rows": [
        binary_df.duplicated().sum(),
        vus_df.duplicated().sum()
    ]
})

summary.to_csv(
    os.path.join(
        RESULTS,
        "dataset_summary.csv"
    ),
    index=False
)

print("\nDataset summary:")
print(summary)

# --------------------------------------------------
# Data types
# --------------------------------------------------

binary_dtypes = pd.DataFrame({
    "Feature": binary_df.columns,
    "Data_Type":
        binary_df.dtypes.astype(str).values
})

vus_dtypes = pd.DataFrame({
    "Feature": vus_df.columns,
    "Data_Type":
        vus_df.dtypes.astype(str).values
})

binary_dtypes.to_csv(
    os.path.join(
        RESULTS,
        "binary_dtypes.csv"
    ),
    index=False
)

vus_dtypes.to_csv(
    os.path.join(
        RESULTS,
        "vus_dtypes.csv"
    ),
    index=False
)

print("\nInventory completed.")
