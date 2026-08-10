import pandas as pd
import numpy as np
import os
from scipy.stats import skew, kurtosis

BASE = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

RESULTS = os.path.join(
    BASE,
    "results"
)

df_raw = pd.read_csv(
    os.path.join(
        BASE,
        "vus_only_variants.csv"
    ),
    low_memory=False
)

# Convert string columns (with commas and '.') to float numeric values
def parse_to_numeric(s):
    s_str = s.astype(str).str.replace('.', 'nan', regex=False)
    split_df = s_str.str.split(',', expand=True)
    for c in split_df.columns:
        split_df[c] = pd.to_numeric(split_df[c], errors='coerce')
    return split_df.mean(axis=1)

df = pd.DataFrame()
for col in df_raw.columns:
    df[col] = parse_to_numeric(df_raw[col])

numeric_columns = list(
    df.select_dtypes(
        include=np.number
    ).columns
)

print(
    "Numerical columns:"
)

for col in numeric_columns:
    print(col)

# ==================================================
# DESCRIPTIVE STATISTICS
# ==================================================

stats = df[
    numeric_columns
].describe().T

stats = stats[
    [
        "min",
        "25%",
        "50%",
        "mean",
        "75%",
        "max",
        "std"
    ]
]

stats.to_csv(
    os.path.join(
        RESULTS,
        "continuous_statistics.csv"
    )
)

# ==================================================
# SKEWNESS AND KURTOSIS
# ==================================================

distribution = []

for col in numeric_columns:

    values = (
        df[col]
        .dropna()
        .values
    )

    distribution.append({

        "Feature": col,

        "Skewness":
            skew(values) if len(values) > 0 else np.nan,

        "Kurtosis":
            kurtosis(values) if len(values) > 0 else np.nan

    })

distribution = pd.DataFrame(
    distribution
)

distribution.to_csv(
    os.path.join(
        RESULTS,
        "distribution_statistics.csv"
    ),
    index=False
)

print("\nDescriptive statistics:")
print(stats)

print(
    "\nDistribution statistics:"
)

print(distribution)
