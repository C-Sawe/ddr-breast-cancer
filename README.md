# DNA-repair genes in breast tumour vs normal tissue

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/C-Sawe/ddr-breast-cancer/blob/main/DDR_Breast_Cancer_Analysis.ipynb)
**Live app:** https://c-sawe.github.io/ddr-breast-cancer/ · **Report:** [REPORT.md](REPORT.md)

**Research question:** Do breast tumour and normal tissues differ in the expression of DNA-repair genes, and can those genes alone classify tumour vs normal?

**Answer in brief:**
- Yes, they differ: 145 of 158 DNA-repair genes change, mostly upward, led by replication-coupled repair (EXO1, NEIL3, UBE2T, RAD51, POLQ).
- Yes, they classify: ROC-AUC 0.998 and balanced accuracy 0.98 with patient-grouped CV.
- But random gene sets do just as well, so the signal is not specific to DNA repair.

## Team and folders
| # | Member | ID | Role | Folder |
|---|---|---|---|---|
| 1 | Ibrahim Sudheysi | 166344 | Question, data acquisition, preprocessing & QC | [`1-ibrahim-data-qc/`](1-ibrahim-data-qc) |
| 2 | Alvin Kimani | 167148 | Exploratory analysis, differential expression | [`2-alvin-eda-de/`](2-alvin-eda-de) |
| 3 | Latifah Jaafar | 167074 | Biological interpretation (pathways, network) | [`3-latifah-biology/`](3-latifah-biology) |
| 4 | Caleb Kipchirchir | 169391 | Machine learning and baselines | [`4-caleb-ml/`](4-caleb-ml) |
| 5 | Jude Makau | 166487 | Deployment (web app, API) and presentation | [`5-jude-deployment/`](5-jude-deployment) |

Each folder has a README listing what that member did, their key results, and their figures and tables.

## Structure
```
DDR_Breast_Cancer_Analysis.ipynb   the full analysis: 8 stages, runs top to bottom in Colab, outputs saved
REPORT.md                          methods (algorithms and why), results, conclusions
1-ibrahim-data-qc/                 stages 1–3
2-alvin-eda-de/                    stages 4–5
3-latifah-biology/                 stage 6
4-caleb-ml/                        stage 7
5-jude-deployment/                 model files, web app (GitHub Pages), Flask API + Docker
index.html                         GitHub Pages entry, opens the web app
```

## Run it
**Colab:** click the badge, then *Runtime → Run all* (about 3 minutes; it downloads the data itself).
**Locally:** `pip install -r requirements.txt && jupyter nbconvert --to notebook --execute --inplace DDR_Breast_Cancer_Analysis.ipynb`

Data: TCGA-BRCA PanCancer Atlas RNA-seq via the cBioPortal datahub. Research and teaching use only, not for diagnosis.
