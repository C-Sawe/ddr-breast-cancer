# 3 · Biological interpretation
**Owner: Latifah Jaafar (167074)**. Notebook stage 6.

## What I did
- Pathway activity scores (mean z per pathway) and pathway enrichment of ≥2-fold risers (Fisher's exact test, FDR).
- Genome-wide test of whether DDR genes are more altered than average genes.
- **NetworkX co-expression network** of DDR genes in tumours (Spearman ρ ≥ 0.6), with modularity communities and hub genes.
- Proliferation analysis and literature comparison.

## Key results
- Fanconi anaemia, HR, BER and MMR scores rise (FDR < 0.001); NER and NHEJ do not. HR is significantly enriched among risers (OR 4.1, FDR 0.02).
- DDR genes are **2.5×** more likely to be strongly up-regulated than other genes (p = 1.7e-4).
- A 22-gene module holds most risers (82%), with hubs EXO1, BLM, POLQ, NEIL3, RAD51AP1 and FANCI.
- Risers track proliferation (median ρ 0.72 vs 0.12 for other DDR genes), consistent with replication stress in dividing tumour cells.

## Files
| File | Content |
|---|---|
| `results/pathway_enrichment.csv` | Pathway scores, enrichment, AUC per pathway |
| `results/network_modules.csv`, `results/network_hub_degree.csv` | Network modules and hub genes |
| `results/ddr_vs_proliferation.csv` | Correlation of each gene with proliferation |
| `figures/bio_1_pathways.png`, `bio_2_network.png`, `bio_3_proliferation.png` | Figures |
