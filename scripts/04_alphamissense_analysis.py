import pandas as pd
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

if "alphamissense_pred" not in df.columns:

    print(
        "alphamissense_pred not found."
    )

    raise SystemExit

counts = (
    df[
        "alphamissense_pred"
    ]
    .value_counts()
    .sort_index()
)

percent = (
    counts /
    len(df) *
    100
)

summary = pd.DataFrame({

    "AlphaMissense_Class":
        counts.index,

    "Count":
        counts.values,

    "Percentage":
        percent.values

})

summary.to_csv(
    os.path.join(
        RESULTS,
        "alphamissense_distribution.csv"
    ),
    index=False
)

print(summary)
