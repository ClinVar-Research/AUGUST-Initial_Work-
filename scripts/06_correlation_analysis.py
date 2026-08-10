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

vus_df = pd.DataFrame()
for col in vus_raw.columns:
    vus_df[col] = parse_to_numeric(vus_raw[col])

# ==================================================
# BINARY CORRELATION
# ==================================================

binary_numeric = binary_df.select_dtypes(
    include=np.number
)

binary_corr = binary_numeric.corr(
    method="pearson"
)

binary_corr.to_csv(
    os.path.join(
        RESULTS,
        "binary_correlation.csv"
    )
)

# ==================================================
# RAW CORRELATION
# ==================================================

raw_numeric = vus_df.select_dtypes(
    include=np.number
)

raw_corr = raw_numeric.corr(
    method="pearson"
)

raw_corr.to_csv(
    os.path.join(
        RESULTS,
        "raw_correlation.csv"
    )
)

# ==================================================
# SPEARMAN (Fast Sampled Rank)
# ==================================================

sample_df = raw_numeric.sample(n=min(50000, len(raw_numeric)), random_state=42)
spearman_corr = sample_df.corr(
    method="spearman"
)

spearman_corr.to_csv(
    os.path.join(
        RESULTS,
        "raw_spearman_correlation.csv"
    )
)

print("Correlation analysis completed.")
