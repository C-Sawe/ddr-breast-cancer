# 1 · Data acquisition and quality control
**Owner: Ibrahim Sudheysi (166344)**. Notebook stages 1–3.

## What I did
- Wrote the research question, 4 objectives and 2 hypotheses (Stage 1).
- Found and assessed the dataset: TCGA-BRCA PanCancer Atlas RNA-seq from cBioPortal, with 1,082 tumours and 114 patient-matched normals. Wrote the download code and a data dictionary for every file and variable (Stage 2).
- Curated the 158-gene DNA-repair set across 9 pathways, with alias mapping for old TCGA gene symbols.
- Built the preprocessing pipeline and QC: symbol cleaning, duplicate merging, log2 transform and expression filter, with before/after counts. Checked the data against known biology (Stage 3).

## Key results
- 20,531 → **17,640 genes** after QC. All 158 DDR genes kept. No missing values and no duplicate samples.
- Sanity checks pass: fat genes (ADIPOQ, PLIN1) are higher in normal tissue, division genes (MKI67, TOP2A) are higher in tumours, and ESR1 and ERBB2 follow PAM50 subtype.
- Flagged: 9.5:1 class imbalance, normals from only 6 of 40 hospitals, and two samples per patient (so CV must be grouped by patient).

## Files
| File | Content |
|---|---|
| `results/data_dictionary.csv` | Every file and variable used |
| `results/qc_before_after.csv` | Genes and samples after each QC step |
| `results/biology_sanity_checks.csv` | Known-biology checks |
| `results/ddr_gene_set.csv` | The 158 curated genes, pathway, TCGA symbol |
| `results/ddr_expression_log2.csv.gz` | Clean analysis matrix (1,196 samples × 158 genes) |
| `results/sample_metadata.csv` | Label, patient, hospital, PAM50 subtype per sample |
| `figures/qc_overview.png` | QC funnel and biology checks |
