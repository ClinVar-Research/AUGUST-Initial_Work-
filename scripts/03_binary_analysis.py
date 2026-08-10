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

df = pd.read_csv(
    os.path.join(
        BASE,
        "binary_df.csv"
    ),
    low_memory=False
)

summary = []

for col in df.columns:

    values = set(
        df[col].dropna().unique()
    )

    # Only binary columns
    if values.issubset({0, 1}):

        total = len(df)

        zero_count = (
            df[col] == 0
        ).sum()

        one_count = (
            df[col] == 1
        ).sum()

        summary.append({

            "Feature": col,

            "Total": total,

            "Zero_Count":
                zero_count,

            "One_Count":
                one_count,

            "Zero_Percent":
                zero_count / total * 100,

            "Positive_Percent":
                one_count / total * 100

        })

summary = pd.DataFrame(summary)

summary = summary.sort_values(
    "Positive_Percent",
    ascending=False
)

summary.to_csv(
    os.path.join(
        RESULTS,
        "binary_positive_rates.csv"
    ),
    index=False
)

print("=" * 70)
print("BINARY FEATURE ANALYSIS")
print("=" * 70)

print(summary.to_string(index=False))
