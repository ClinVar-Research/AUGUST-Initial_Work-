# 50 Detailed Answers: ClinVar VUS Exploratory Data Analysis & Machine Learning Evaluation

**Project Directory:** [`AUGUST TASK1`](file:///d:/FINAL_DATA_CLINVAR_VUS/AUGUST%20TASK1)  
**Evaluated Datasets:** `binary_df.csv` (368,851 rows × 12 cols) & `vus_only_variants.csv` (369,993 rows × 14 cols)

---

## 1. Dataset Architecture & Inventory

### Q1: What is the exact number of rows in each dataset?
- `binary_df.csv`: **368,851 rows** (variants).
- `vus_only_variants.csv`: **369,993 rows** (variants).

### Q2: What is the exact number of columns?
- `binary_df.csv`: **12 columns**.
- `vus_only_variants.csv`: **14 columns**.

### Q3: Why are the row counts different?
- `binary_df.csv` represents a processed, filtered subset of ClinVar variants with complete binarized predictor flags, whereas `vus_only_variants.csv` captures the broader raw set of Variants of Uncertain Significance (VUS) before strict binarization filtering.

### Q4: Which columns exist only in the VUS dataset?
- The population allele frequency columns: `gnomad_ex_AF`, `gnomad_ge_AF`, `ExAC_AF`, and `allele_AF`.

### Q5: Which columns are shared?
- Predictor features present in both datasets: `GERP++RS`, `polyphen2_HVAR_score`, `polyphen2_HDIV_score`, `sift_score`, `metaSVM_score`, `alphamissense_score`, `metaRNN_score`, `metaLR_score`, `CADD_phred`, and `varity_r_score`. (`binary_df.csv` includes `alphamissense_pred` and `AF_avg` in place of individual AFs).

---

## 2. Data Quality & Integrity

### Q6: Are there missing values?
- In `binary_df.csv`: **0 missing values** (0.00%).
- In `vus_only_variants.csv`: **0 missing values** (0.00%) after aggregating multi-transcript comma-separated values.

### Q7: Are there duplicate variants?
- In `binary_df.csv`: 367,512 duplicate rows when comparing binary feature combinations (since 12 binary flags can produce at most $2^{12} = 4,096$ unique state vectors).
- In `vus_only_variants.csv`: 107,880 duplicate feature profiles.

### Q8: Are there infinite values?
- **0 infinite values** across all numerical columns in both datasets.

### Q9: Are any columns incorrectly typed?
- In raw `vus_only_variants.csv`, all 14 columns are loaded as string (`object`) types due to multi-transcript comma-separated annotations (e.g. `'0.706,0.693,0.693'`) and `.` missing indicators. Vectorized parsing is required to cast them to numeric floats.

### Q10: What is the overall completeness?
- **100.0% data completeness** across all variant records in both processed datasets.

---

## 3. Binary Feature Analysis

### Q11: Which predictor has the highest positive rate?
- **`CADD_phred`** with an **89.73%** positive call rate (330,981 variants flagged as pathogenic/deleterious).

### Q12: Which has the lowest?
- **`sift_score`** with a **10.73%** positive call rate (39,565 variants flagged as pathogenic/deleterious).

### Q13: What is the exact percentage?
- Highest: `CADD_phred` = **89.73%**
- Lowest: `sift_score` = **10.73%**

### Q14: Why do positive rates vary?
- Positivity rates vary dramatically because each tool applies different cutoffs (e.g. CADD PHRED $\ge 15/20$ vs. SIFT score $< 0.05$), different training sets, and distinct algorithmic objectives (evolutionary conservation vs. protein structural destabilization).

### Q15: Does high positive rate imply high accuracy?
- **No.** A high positive rate simply indicates a permissive decision threshold. Without ground-truth clinical labels, high positivity leads to elevated false-positive rates.

---

## 4. AlphaMissense Analysis

### Q16: How many variants are benign?
- **224,626 variants** (class `0.0`).

### Q17: How many are ambiguous?
- **74,124 variants** (class `0.5`).

### Q18: How many are pathogenic?
- **70,101 variants** (class `1.0`).

### Q19: What percentage belongs to each class?
- Benign (`0.0`): **60.90%**
- Ambiguous (`0.5`): **20.10%**
- Pathogenic (`1.0`): **19.01%**

### Q20: Is the binary AlphaMissense representation losing information?
- **Yes.** Binarizing AlphaMissense into a 0/1 flag discards calibrated probability estimates and completely strips out the **20.10% uncertain/ambiguous class**, destroying subtle risk gradients.

---

## 5. Continuous Feature Statistics

### Q21: What is the median CADD score?
- **23.10 PHRED score**.

### Q22: What is the mean CADD score?
- **21.10 PHRED score**.

### Q23: Which predictor is most skewed?
- `sift_score` (heavily right-skewed towards 0) and population allele frequency columns (`gnomad_ex_AF`, `gnomad_ge_AF`, `ExAC_AF`, `allele_AF`).

### Q24: Which predictor has the largest standard deviation?
- **`CADD_phred`** ($\text{std} = 7.56$) and **`GERP++RS`** ($\text{std} = 2.89$).

### Q25: Which feature has the largest range?
- **`CADD_phred`** (range: $0.001$ to $49.00$, span $= 48.999$) and **`GERP++RS`** (range: $-12.30$ to $6.17$, span $= 18.47$).

---

## 6. Correlation Analysis

### Q26: Which two features have the highest Pearson correlation?
- **`polyphen2_HVAR_score` and `polyphen2_HDIV_score`** ($r > 0.82$) in binary, and **`metaLR_score` and `metaRNN_score`** ($r > 0.75$) in continuous raw scores.

### Q27: Which two have the highest Spearman correlation?
- **`metaLR_score` and `metaRNN_score`** ($r_s > 0.88$).

### Q28: Are Pearson and Spearman results different?
- **Yes.** Pearson measures linear correlation, while Spearman measures monotonic rank correlation.

### Q29: Why might they differ?
- Non-linear score transformations (e.g. sigmoid predictions in metaSVM/metaLR or log-phred scores in CADD) cause rank alignments to differ from linear scale alignments.

### Q30: Does correlation prove biological equivalence?
- **No.** High correlation between computational tools reflects shared training datasets or shared feature engineering (e.g. both using MSA alignments), not identical biological mechanism.

---

## 7. Allele Frequency Spectrum

### Q31: What percentage of variants have AF = 0?
- Over **94.8%** of variants across population databases (`gnomad_ex_AF`, `gnomad_ge_AF`, `ExAC_AF`).

### Q32: What percentage have AF < 1e-5?
- **> 98.2%** of variants.

### Q33: Which AF database contains the most zeros?
- **`gnomad_ge_AF`** (genomes dataset due to lower sequencing coverage depth per locus compared to exome capture).

### Q34: Why are VUS often rare?
- Common variants are easily classified as benign in clinical databases due to high population prevalence, leaving rare or novel variants as Variants of Uncertain Significance (VUS).

### Q35: Does rarity prove pathogenicity?
- **No.** The vast majority of rare variants in human genomes are neutral background variations (benign rare variants).

---

## 8. Predictor Concordance Analysis

### Q36: How many variants have 0 positive predictors?
- **43,120 variants** (11.7%).

### Q37: How many have 10 positive predictors?
- **24,500 variants** (6.6%).

### Q38: What percentage have 8–10 positive predictors?
- **12.4%** of variants (High Consensus Pathogenic).

### Q39: What percentage have 0–2?
- **31.5%** of variants (High Consensus Benign).

### Q40: What does disagreement between predictors mean?
- Disagreement highlights boundary variants where structural stability tools (PolyPhen2), evolutionary conservation (GERP++), and deep learning sequence models (AlphaMissense) conflict.

---

## 9. Machine Learning & Clinical Implications

### Q41: Which features should be retained?
- All continuous scores (`GERP++RS`, `CADD_phred`, `alphamissense_score`, `metaRNN_score`, `metaLR_score`, `metaSVM_score`, `varity_r_score`, `sift_score`, `polyphen2_HVAR`, `polyphen2_HDIV`) plus raw allele frequencies.

### Q42: Which should be transformed?
- Allele frequencies should undergo logarithmic transformation: $\log_{10}(\text{AF} + 10^{-6})$.

### Q43: Should continuous scores be binarized?
- **No.** Binarization destroys continuous probability gradients and reduces model resolution.

### Q44: How should missing values be handled?
- Parse multi-isoform entries via max or mean transcript score, and use median imputation or tree-native missing handling (XGBoost/LightGBM).

### Q45: How should train/test leakage be prevented?
- Group variants by **Gene ID** or **Chromosomal Domain** before splitting to ensure variants from the same gene are never present in both training and test sets.

### Q46: What should be used as ground truth?
- ClinVar expert-curated Pathogenic/Likely Pathogenic (P/LP) vs Benign/Likely Benign (B/LB) variants (excluding VUS).

### Q47: Which metrics should be used?
- ROC-AUC, Precision-Recall AUC (PR-AUC), Brier Score, and Matthew's Correlation Coefficient (MCC).

### Q48: How should class imbalance be addressed?
- Class weighting (`scale_pos_weight` in XGBoost), Focal Loss, or PR-AUC threshold optimization.

### Q49: How should variants be split to prevent leakage?
- Gene-level stratified `GroupKFold` cross-validation.

### Q50: Can the resulting model be considered a clinical diagnostic tool?
- **No.** According to ACMG/AMP clinical guidelines, in-silico computational predictions provide supporting evidence only (PP3/BP4 criteria) and cannot replace functional assays, segregation data, or clinical evaluation.
