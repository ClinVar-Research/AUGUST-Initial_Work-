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

df_raw = pd.read_csv(
    os.path.join(
        BASE,
        "vus_only_variants.csv"
    ),
    low_memory=False
)

def parse_to_numeric(s):
    s_str = s.astype(str).str.replace('.', 'nan', regex=False)
    split_df = s_str.str.split(',', expand=True)
    for c in split_df.columns:
        split_df[c] = pd.to_numeric(split_df[c], errors='coerce')
    return split_df.mean(axis=1)

df = pd.DataFrame()
for col in df_raw.columns:
    df[col] = parse_to_numeric(df_raw[col])

# Identify AF columns
af_columns = [
    col
    for col in df.columns
    if "AF" in col or "af" in col
]

print(
    "Allele frequency columns:"
)

for col in af_columns:
    print(col)

results = []

for col in af_columns:

    values = pd.to_numeric(
        df[col],
        errors="coerce"
    ).dropna()

    zero = (
        values == 0
    ).sum()

    rare = (
        values < 1e-5
    ).sum()

    results.append({

        "Feature": col,

        "Count": len(values),

        "Minimum": values.min() if len(values) > 0 else np.nan,

        "Mean": values.mean() if len(values) > 0 else np.nan,

        "Median": values.median() if len(values) > 0 else np.nan,

        "Maximum": values.max() if len(values) > 0 else np.nan,

        "Zero_Count": zero,

        "Zero_Percent":
            zero / len(values) * 100 if len(values) > 0 else 0,

        "Below_1e-5":
            rare,

        "Below_1e-5_Percent":
            rare / len(values) * 100 if len(values) > 0 else 0

    })

results = pd.DataFrame(
    results
)

results.to_csv(
    os.path.join(
        RESULTS,
        "allele_frequency_summary.csv"
    ),
    index=False
)

print(results)
