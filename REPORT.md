# Report: DNA-repair gene expression in breast tumour vs normal tissue

**Computing Bioinformatics group project, Strathmore University**
Ibrahim Sudheysi (166344) · Alvin Kimani (167148) · Latifah Jaafar (167074) · Caleb Kipchirchir (169391) · Jude Makau (166487)

---

## 1. Summary
We asked whether breast tumours and normal breast tissue differ in the expression of DNA damage repair (DDR) genes, and whether those genes alone can classify a sample as tumour or normal. We used TCGA-BRCA RNA-seq (1,082 tumours and 114 patient-matched normals). **145 of 158 DDR genes differ** (FDR < 0.05), mostly upward. The risers are replication-coupled repair genes (EXO1 ~12×, NEIL3, UBE2T, RAD54L, RAD51, POLQ). A logistic-regression classifier on DDR genes alone reaches **ROC-AUC 0.998 and balanced accuracy 0.98** under patient-grouped cross-validation, far above dummy baselines. However, **random gene sets of the same size classify equally well**, and the up-regulated repair genes track cell proliferation. DDR genes can classify, but that ability is not specific to DNA repair. We deployed the model as a GitHub Pages web app and a Dockerised REST API.

## 2. Question, objectives and hypotheses
| | |
|---|---|
| **Question** | Do breast tumour and normal tissues differ in DDR gene expression, and can those genes alone classify tumour vs normal? |
| **O1** | Compare 158 DDR genes between tumour and normal (unpaired and paired, FDR-corrected). |
| **O2** | Explain the changes biologically (pathways, co-expression network, proliferation, literature). |
| **O3** | Build DDR-only classifiers and evaluate them against proper baselines. |
| **O4** | Deploy the final model as a usable tool. |
| **H1** | Replication-coupled DDR pathways (HR, Fanconi anaemia, MMR, BER) are up-regulated in tumours. |
| **H2** | DDR-only classifiers beat dummy baselines with ROC-AUC > 0.90. We also test whether they beat random gene sets. |

## 3. Data
- **Source:** TCGA Breast Invasive Carcinoma, PanCancer Atlas 2018 (`brca_tcga_pan_can_atlas_2018`), downloaded from the public cBioPortal datahub. The notebook downloads it automatically.
- **Files:** a tumour RNA-seq matrix (20,531 genes × 1,082 samples), a normal RNA-seq matrix (20,531 × 114), and clinical patient and sample tables (PAM50 subtype, hospital). Values are RSEM-normalised counts.
- **Why it fits:** tumour and adjacent normal tissue from the **same patients**, processed in one pipeline, which allows within-patient comparison.
- **Gene set:** 158 DDR genes in 9 pathways (BER, MMR, NER, HR, NHEJ, Fanconi anaemia, translesion synthesis, direct reversal, DDR signalling). Compiled from the *Human DNA Repair Genes* list (Wood et al.) and KEGG.

## 4. Methods

### 4.1 Preprocessing and quality control
Rows without a gene symbol were removed (13) and duplicate symbols merged (7). We kept genes present in both matrices and applied a **log2(x + 1)** transform. This stabilises variance and makes fold changes additive. Low-expressed genes were removed (2,814 genes with log2 > 1 in under 20% of samples), leaving **17,640 genes**. All 158 DDR genes passed; old TCGA symbols were mapped through aliases.

**Biological sanity checks passed.** Adipocyte genes (ADIPOQ, PLIN1) are about 6.5 log2 units higher in normal tissue, proliferation genes (MKI67, TOP2A) are higher in tumours, ESR1 is highest in luminal subtypes, and ERBB2 peaks in HER2-enriched tumours.

**Issues flagged:**
- 9.5:1 class imbalance.
- All normals came from only 6 of 40 hospitals, a possible batch confounder.
- "Normal" is tissue adjacent to the tumour.
- Patients contribute two samples each, so validation must be grouped by patient.

### 4.2 Exploratory analysis
We plotted per-sample median expression (normalisation check), expression distributions, cohort composition, PCA on all genes and on DDR genes only, and a clustered DDR correlation heatmap.

### 4.3 Differential expression
| Method | Why |
|---|---|
| **Mann-Whitney U test** (all samples) | Non-parametric, so it does not assume normality. Robust to skewed RNA-seq values and very unequal group sizes. |
| **Wilcoxon signed-rank test** (114 matched pairs) | Compares each tumour with the same patient's normal. Removes patient and hospital effects. |
| **Benjamini-Hochberg FDR** | Controls false discoveries across 158 tests. Less conservative than Bonferroni. |
| **log2 fold change** | Effect size. With n = 1,196, p-values alone mark tiny shifts as significant. |

### 4.4 Biological interpretation
| Method | Why |
|---|---|
| **Pathway activity score** (mean z-score per pathway), Mann-Whitney + FDR | Summarises each repair pathway per sample, so pathways can be compared directly. |
| **Pathway enrichment** (one-sided Fisher's exact test, BH-FDR) | Tests whether a pathway has more ≥2-fold risers than expected by chance. |
| **Genome-wide enrichment** (Fisher's exact test, DDR vs all 17,482 other genes) | Asks whether repair genes are *more* altered than an average gene. |
| **Co-expression network** (NetworkX; Spearman ρ ≥ 0.6 within tumours; greedy modularity communities; node degree for hubs) | Shows which genes are switched on together as a programme and which genes are hubs. |
| **Proliferation correlation** (Spearman ρ with the MKI67/TOP2A/CCNB1/BUB1/AURKA score) | Tests the alternative explanation that the rise simply reflects dividing cells. |
| **Literature comparison** | Links the findings to known breast-cancer biology. |

### 4.5 Machine learning
**Validation:** 5-fold **StratifiedGroupKFold grouped by patient**, repeated 3 times. A patient's tumour and normal never land on both sides of a split, which would leak information. Stratification keeps the 9.5:1 ratio in every fold. **Metrics:** ROC-AUC, PR-AUC for the minority (normal) class, balanced accuracy, sensitivity, specificity and Matthews correlation coefficient (MCC). Accuracy alone would be misleading, since always predicting "tumour" scores 90.5%.

| Algorithm | Settings | Why we used it |
|---|---|---|
| **Logistic regression, L2** (final model) | standardised inputs, C = 0.1, balanced class weights | Linear and interpretable (one weight per gene). L2 regularisation copes with highly correlated genes. Calibrated probabilities. Simple enough to run in a browser. |
| **Logistic regression, L1** | C = 0.05, liblinear | Sparse model that selects genes automatically. Tests whether a few genes suffice. |
| **Random forest** | 400 trees, min leaf 2, balanced subsample weights | Non-linear with gene interactions, needs no scaling. A standard strong benchmark for tabular data. |
| **Support vector machine, RBF kernel** | C = 1, balanced weights, Platt probabilities | Non-linear margin classifier that works well with many correlated features and a small class. |

| Baseline | Why |
|---|---|
| Majority-class dummy | The floor (always "tumour"). |
| Stratified random dummy | Chance level at the class ratio. |
| Single gene, MKI67 | A one-gene biological benchmark (proliferation). |
| **100 random 158-gene sets** | Tests whether *DNA-repair* genes are special, or whether any genes would do. |

**Extra checks:**
- Training on the 114 matched pairs only.
- **Leave-hospital-out** validation (GroupKFold by tissue source site), to rule out learning the hospital or batch.
- Gene-panel sizes of 1–158, with genes ranked by Welch t **inside each training fold** to avoid selection leakage.

## 5. Results

### 5.1 Differential expression (O1)
| | Count |
|---|---|
| DDR genes significant (FDR < 0.05), unpaired | **145 / 158** |
| Still significant within patients (paired) | 134 / 158 |
| Up / down (any size) | 101 / 44 |
| Up ≥ 2-fold / down ≥ 2-fold | **29 / 3** |

The largest increases are EXO1 (11.9×), NEIL3 (10.5×), UBE2T (8.7×), RAD54L (8.1×), CLSPN (7.4×), RECQL4 (7.2×), POLQ (6.0×) and RAD51 (5.9×). Each is higher in the tumour than the matched normal in more than 94% of patients. The largest decreases are REV3L, SHPRH and APLF (about 0.43–0.49×). Paired and unpaired fold changes agree almost perfectly. **H1 is supported.**

### 5.2 Biological interpretation (O2)
- **Pathway scores** rise in Fanconi anaemia, HR, BER and MMR (all FDR < 0.001). NER, NHEJ and direct reversal show no clear change, and translesion synthesis falls slightly.
- **HR is significantly enriched** among ≥2-fold risers (12/31 genes, OR 4.1, FDR 0.02).
- **Genome-wide,** DDR genes are 2.5× more likely to be strongly up-regulated than other genes (17.4% vs 7.9%, p = 1.7 × 10⁻⁴).
- **Network:** one 22-gene module contains most risers (82% up ≥2-fold), with hubs EXO1, BLM, POLQ, NEIL3, RAD51AP1 and FANCI. The genes are co-regulated as one programme.
- **Proliferation:** within tumours, the risers correlate strongly with proliferation (median ρ = 0.72), while other DDR genes do not (ρ = 0.12).

Tumour cells divide fast and face replication stress, so they switch on the repair systems that work during DNA replication. This matches reports of HR/FA over-expression in proliferative and basal-like breast cancer, and of POLQ as a breast-cancer drug target.

### 5.3 Machine learning (O3)
| Model / baseline | ROC-AUC | Balanced acc. | Specificity | MCC |
|---|---|---|---|---|
| Majority-class dummy | 0.500 | 0.500 | 0.000 | 0.00 |
| Stratified random dummy | 0.480 | 0.480 | 0.044 | −0.04 |
| MKI67 only | 0.948 | 0.894 | 0.895 | 0.60 |
| **Logistic regression (L2)** | **0.998** | **0.983** | **0.980** | 0.92 |
| SVM (RBF) | 0.997 | 0.970 | 0.944 | **0.94** |
| Logistic regression (L1) | 0.996 | 0.967 | 0.980 | 0.81 |
| Random forest | 0.995 | 0.928 | 0.860 | 0.90 |
| *100 random 158-gene sets (L2 LR)* | *0.999 (mean)* | *0.992* | | |

- **Robustness:** matched pairs only, AUC 0.9996. Leave-hospital-out, AUC 0.997 and balanced accuracy 0.980. The model is not learning hospital identity.
- **Compact panel:** 10 genes (UBE2T, PARP1, FEN1, RAD51, PCNA, EME1, NEIL3, RFC2, EXO1, FANCI) reach AUC 0.987 and balanced accuracy 0.942. One gene alone reaches AUC 0.975.
- **Errors:** 17 of 1,196 samples are misclassified. 9 of the 14 missed tumours are PAM50 Normal-like, a subtype that resembles normal tissue.

**H2 is supported against dummy and single-gene baselines.** It is **not** supported against random gene sets, which do slightly better. Tumour vs normal is a very large biological difference, so any reasonable gene set separates the groups. This negative finding is a key result.

### 5.4 Deployment (O4)
- **Web app on GitHub Pages:** <https://c-sawe.github.io/ddr-breast-cancer/>. The model runs in the browser and shows the probability and the genes that drove each prediction. Its outputs were verified to match scikit-learn exactly.
- **REST API:** Flask + gunicorn in Docker, with `/health`, `/genes` and `/predict` (JSON or CSV). It validates input (rejects raw counts, imputes up to 20% missing genes) and passes 3 automated tests.

## 6. Conclusions
1. **O1:** DDR expression differs strongly between tumour and normal breast tissue, overwhelmingly upward.
2. **O2:** The rise is concentrated in replication-coupled repair (HR, FA, BER, MMR), acts as one co-expressed programme, and tracks proliferation.
3. **O3:** DDR genes alone classify tumour vs normal almost perfectly and robustly, but so do random genes. The classification ability is real but **not specific** to DNA repair.
4. **O4:** The model is deployed as a public web app and a containerised API.

## 7. Limitations and future work
**Limitations:**
- One cohort and one platform, with no independent validation set.
- Adjacent-normal tissue is not healthy breast.
- Class imbalance, and normals come from few hospitals.
- Bulk tissue: tumour purity and fat content shift expression.
- The findings are correlational, not causal.

**Future work:**
1. Validate on independent GEO cohorts.
2. Adjust for proliferation and purity to find repair changes beyond cell division.
3. Use the same genes for a harder, clinically useful task: predicting PAM50 subtype or homologous-recombination deficiency, which guides PARP-inhibitor therapy.
4. Add STRING protein-interaction networks.

## 8. Contributions
| Member | Responsibility | Deliverables (folder) |
|---|---|---|
| Ibrahim Sudheysi | Research question and objectives, data sourcing and documentation, preprocessing, QC, DDR gene curation | `1-ibrahim-data-qc/` |
| Alvin Kimani | Exploratory data analysis, differential expression (unpaired + paired, FDR) | `2-alvin-eda-de/` |
| Latifah Jaafar | Biological interpretation: pathway scores and enrichment, NetworkX co-expression network, proliferation analysis, literature comparison | `3-latifah-biology/` |
| Caleb Kipchirchir | Machine learning: model selection, patient-grouped CV, baselines, robustness checks, gene-panel analysis | `4-caleb-ml/` |
| Jude Makau | Model export, GitHub Pages web app, Flask API and Docker, tests, presentation | `5-jude-deployment/` |
| All | Conclusions, this report, review of each other's stages | `REPORT.md` |

## References
- The Cancer Genome Atlas Network. Comprehensive molecular portraits of human breast tumours. *Nature* 490, 61–70 (2012).
- Hoadley KA et al. Cell-of-origin patterns dominate the molecular classification of 10,000 tumors from 33 types of cancer. *Cell* 173, 291–304 (2018). (PanCancer Atlas)
- Cerami E et al. The cBio Cancer Genomics Portal. *Cancer Discovery* 2, 401–404 (2012).
- Wood RD, Mitchell M, Sgouros J, Lindahl T. Human DNA repair genes. *Science* 291, 1284–1289 (2001).
- Knijnenburg TA et al. Genomic and molecular landscape of DNA damage repair deficiency across The Cancer Genome Atlas. *Cell Reports* 23, 239–254 (2018).
- Benjamini Y, Hochberg Y. Controlling the false discovery rate. *J R Stat Soc B* 57, 289–300 (1995).
- Pedregosa F et al. Scikit-learn: Machine learning in Python. *JMLR* 12, 2825–2830 (2011).
- Hagberg A, Schult D, Swart P. Exploring network structure, dynamics, and function using NetworkX. *SciPy 2008*.
