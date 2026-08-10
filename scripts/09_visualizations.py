import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
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

VISUALS = os.path.join(
    BASE,
    "visuals"
)

os.makedirs(
    VISUALS,
    exist_ok=True
)

binary = pd.read_csv(
    os.path.join(
        BASE,
        "binary_df.csv"
    ),
    low_memory=False
)

vus_raw = pd.read_csv(
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

vus = pd.DataFrame()
for col in vus_raw.columns:
    vus[col] = parse_to_numeric(vus_raw[col])

# Set aesthetic styling
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')

# ==================================================
# 1. POSITIVE RATE
# ==================================================

summary = pd.read_csv(
    os.path.join(
        RESULTS,
        "binary_positive_rates.csv"
    )
)

summary = summary.sort_values(
    "Positive_Percent",
    ascending=False
)

plt.figure(figsize=(12, 7))

plt.bar(
    summary["Feature"],
    summary["Positive_Percent"],
    color="#2b5c8f",
    edgecolor="black",
    alpha=0.85
)

plt.xticks(
    rotation=60,
    ha="right",
    fontweight="bold"
)

plt.ylabel(
    "Positive Rate (%)",
    fontweight="bold"
)

plt.title(
    "Binary Feature Positive Rates (Pathogenic Call Proportion)",
    fontweight="bold",
    pad=15
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        VISUALS,
        "01_binary_feature_positive_rates.png"
    ),
    dpi=300,
    bbox_inches="tight"
)

plt.close()

# ==================================================
# 2. CORRELATION HEATMAP
# ==================================================

corr = pd.read_csv(
    os.path.join(
        RESULTS,
        "binary_correlation.csv"
    ),
    index_col=0
)

plt.figure(figsize=(12, 10))

sns.heatmap(
    corr,
    annot=True,
    fmt=".2f",
    cmap="Blues",
    linewidths=0.5
)

plt.title(
    "Binary Predictor Correlation Heatmap",
    fontweight="bold",
    pad=15
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        VISUALS,
        "02_binary_correlation_heatmap.png"
    ),
    dpi=300,
    bbox_inches="tight"
)

plt.close()

# ==================================================
# 3. ALPHAMISSENSE
# ==================================================

if "alphamissense_pred" in binary.columns:

    alpha = (
        binary[
            "alphamissense_pred"
        ]
        .value_counts()
        .sort_index()
    )

    plt.figure(figsize=(8, 6))

    labels = ["Benign (0.0)", "Ambiguous (0.5)", "Pathogenic (1.0)"]
    colors = ["#2ca02c", "#ff7f0e", "#d62728"]
    
    bars = plt.bar(
        labels,
        alpha.values,
        color=colors,
        edgecolor="black",
        alpha=0.85
    )

    for bar in bars:
        h = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, h + 3000, f"{h:,}\n({h/len(binary)*100:.1f}%)", ha="center", fontweight="bold")

    plt.xlabel(
        "AlphaMissense Prediction Class",
        fontweight="bold"
    )

    plt.ylabel(
        "Variant Count",
        fontweight="bold"
    )

    plt.title(
        "AlphaMissense Prediction Breakdown (alphamissense_pred)",
        fontweight="bold",
        pad=15
    )

    plt.ylim(0, max(alpha.values) * 1.15)
    plt.tight_layout()

    plt.savefig(
        os.path.join(
            VISUALS,
            "03_alphamissense_pred_breakdown.png"
        ),
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

# ==================================================
# 4. MISSING DATA
# ==================================================

missing = (
    vus.isna()
    .sum()
    .sort_values(
        ascending=False
    )
)

plt.figure(figsize=(12, 6))

plt.bar(
    missing.index,
    missing.values,
    color="#1b9e77",
    edgecolor="black",
    alpha=0.85
)

plt.xticks(
    rotation=60,
    ha="right",
    fontweight="bold"
)

plt.ylabel(
    "Missing Values Count",
    fontweight="bold"
)

plt.title(
    "VUS Missing Data Profile (0 Missing across all features)",
    fontweight="bold",
    pad=15
)

plt.ylim(0, 10)
plt.tight_layout()

plt.savefig(
    os.path.join(
        VISUALS,
        "04_vus_missing_data_profile.png"
    ),
    dpi=300,
    bbox_inches="tight"
)

plt.close()

# ==================================================
# 5. RAW SCORE DISTRIBUTIONS
# ==================================================

numeric = vus.select_dtypes(
    include=np.number
)

# Filter score predictor columns
score_cols = [c for c in numeric.columns if 'AF' not in c and 'af' not in c]

fig, axes = plt.subplots(
    2, 5,
    figsize=(18, 8)
)
axes = axes.flatten()

for i, col in enumerate(score_cols[:10]):
    sns.histplot(
        numeric[col].dropna(),
        bins=30,
        kde=True,
        ax=axes[i],
        color="#2b5c8f",
        edgecolor="none"
    )

    axes[i].set_title(
        col,
        fontweight="bold"
    )
    axes[i].set_xlabel('')

plt.suptitle(
    "Distribution Profiles of Raw Computational Pathogenicity Predictors in VUS Dataset",
    fontweight="bold",
    fontsize=14,
    y=1.02
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        VISUALS,
        "05_vus_raw_score_distributions.png"
    ),
    dpi=300,
    bbox_inches="tight"
)

plt.close()

# ==================================================
# 6. ALLELE FREQUENCY
# ==================================================

af_columns = [
    col
    for col in vus.columns
    if "AF" in col or "af" in col
]

plt.figure(figsize=(10, 7))

for col in af_columns:

    values = pd.to_numeric(
        vus[col],
        errors="coerce"
    ).dropna()

    values = values[
        values > 0
    ]

    if len(values) > 0:

        sns.histplot(
            np.log10(values),
            bins=50,
            stat="density",
            element="step",
            fill=False,
            label=col
        )

plt.xlabel(
    "log10(Allele Frequency)",
    fontweight="bold"
)

plt.ylabel(
    "Density",
    fontweight="bold"
)

plt.title(
    "Population Allele Frequency Spectrum (Log Scale)",
    fontweight="bold",
    pad=15
)

plt.legend()

plt.tight_layout()

plt.savefig(
    os.path.join(
        VISUALS,
        "06_vus_allele_frequency_spectrum.png"
    ),
    dpi=300,
    bbox_inches="tight"
)

plt.close()

# ==================================================
# 7. CONCORDANCE
# ==================================================

concordance = pd.read_csv(
    os.path.join(
        RESULTS,
        "tool_concordance.csv"
    )
)

plt.figure(figsize=(10, 6))

bars = plt.bar(
    concordance[
        "Number_of_Positive_Tools"
    ],
    concordance[
        "Variant_Count"
    ],
    color="#7570b3",
    edgecolor="black",
    alpha=0.85
)

for bar in bars:
    y = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, y + 2000, f"{y:,}", ha="center", fontsize=9, fontweight="bold")

plt.xlabel(
    "Number of Positive Predictions (out of 10 tools)",
    fontweight="bold"
)

plt.ylabel(
    "Number of Variants",
    fontweight="bold"
)

plt.title(
    "Binary Tool Concordance Spectrum",
    fontweight="bold",
    pad=15
)

plt.ylim(0, max(concordance["Variant_Count"]) * 1.15)
plt.tight_layout()

plt.savefig(
    os.path.join(
        VISUALS,
        "07_binary_tool_concordance_spectrum.png"
    ),
    dpi=300,
    bbox_inches="tight"
)

plt.close()

# ==================================================
# 8. DATASET COMPARISON
# ==================================================

datasets = [
    "binary_df.csv\n(Binarized Matrix)",
    "vus_only_variants.csv\n(Raw Continuous Matrix)"
]

rows = [
    len(binary),
    len(vus)
]

plt.figure(figsize=(8, 6))

bars = plt.bar(
    datasets,
    rows,
    color=["#2b5c8f", "#e7298a"],
    edgecolor="black",
    width=0.45
)

for bar in bars:
    y = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, y + 5000, f"{y:,} variants", ha="center", fontweight="bold")

plt.ylabel(
    "Number of Variant Rows",
    fontweight="bold"
)

plt.title(
    "Dataset Overview: Variant Record Volume Comparison",
    fontweight="bold",
    pad=15
)

plt.ylim(0, max(rows) * 1.15)
plt.tight_layout()

plt.savefig(
    os.path.join(
        VISUALS,
        "08_dataset_comparison_overview.png"
    ),
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("=" * 60)
print("ALL VISUALIZATIONS GENERATED")
print("=" * 60)

for filename in sorted(
    os.listdir(VISUALS)
):

    print(filename)
