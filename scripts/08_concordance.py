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

# ==================================================
# Find true binary predictors
# ==================================================

binary_predictors = []

for col in df.columns:

    values = set(
        df[col].dropna().unique()
    )

    if values.issubset({0, 1}):

        binary_predictors.append(col)

print(
    "Binary predictors:"
)

for col in binary_predictors:
    print(col)

# ==================================================
# Consensus score
# ==================================================

df["tool_consensus"] = (
    df[binary_predictors]
    .sum(axis=1)
)

# ==================================================
# Consensus distribution
# ==================================================

distribution = (
    df["tool_consensus"]
    .value_counts()
    .sort_index()
)

summary = pd.DataFrame({

    "Number_of_Positive_Tools":
        distribution.index,

    "Variant_Count":
        distribution.values,

    "Percentage":
        distribution.values /
        len(df) * 100

})

summary.to_csv(
    os.path.join(
        RESULTS,
        "tool_concordance.csv"
    ),
    index=False
)

# ==================================================
# Group classification
# ==================================================

def classify(x):

    if x <= 2:
        return "High Consensus Benign"

    if x <= 4:
        return "Low/Moderate"

    if x <= 7:
        return "Moderate Consensus"

    return "High Consensus Pathogenic"


df["consensus_group"] = (
    df["tool_consensus"]
    .apply(classify)
)

groups = (
    df["consensus_group"]
    .value_counts()
)

group_summary = pd.DataFrame({

    "Group":
        groups.index,

    "Count":
        groups.values,

    "Percentage":
        groups.values /
        len(df) * 100

})

group_summary.to_csv(
    os.path.join(
        RESULTS,
        "concordance_groups.csv"
    ),
    index=False
)

print("\nConcordance:")
print(summary)

print("\nGroups:")
print(group_summary)
