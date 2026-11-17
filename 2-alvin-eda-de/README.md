# 2 · Exploratory data analysis and differential expression
**Owner: Alvin Kimani (167148)**. Notebook stages 4–5.

## What I did
- EDA (Stage 4): normalisation check, expression distributions, cohort composition, PCA on all genes vs DDR genes only, and a clustered DDR correlation heatmap.
- Differential expression (Stage 5): Mann-Whitney U on all samples and Wilcoxon signed-rank on 114 matched pairs, with Benjamini-Hochberg FDR and log2 fold change.

## Key results
- PCA on DDR genes alone already separates normals (a tight cluster) from tumours (widely spread).
- **145/158 DDR genes differ** (FDR < 0.05); 134 hold within patients.
- **29 up ≥2-fold** (EXO1 11.9×, NEIL3 10.5×, UBE2T 8.7×, RAD54L, CLSPN, RECQL4, POLQ, RAD51); **3 down ≥2-fold** (REV3L, SHPRH, APLF).

## Files
| File | Content |
|---|---|
| `results/differential_expression_ddr.csv` | Full DE table: means, log2FC, p, FDR, paired stats |
| `figures/eda_1_distributions.png` … `eda_4_correlation_heatmap.png` | EDA plots |
| `figures/de_1_volcano.png` | Volcano plot |
| `figures/de_2_top_genes.png` | Most changed genes |
| `figures/de_3_paired_vs_unpaired.png` | Paired vs unpaired agreement |
