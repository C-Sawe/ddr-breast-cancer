# 4 · Machine learning
**Owner: Caleb Kipchirchir (169391)**. Notebook stage 7.

## What I did
- Designed the validation: 5-fold StratifiedGroupKFold **grouped by patient**, repeated 3×, with imbalance-aware metrics (balanced accuracy, PR-AUC for normals, MCC).
- Trained and compared logistic regression (L2 and L1), random forest and an RBF-kernel SVM.
- Baselines: majority-class and stratified dummies, a single gene (MKI67), and **100 random 158-gene sets**.
- Robustness: matched pairs only, and leave-hospital-out.
- Gene-panel analysis (1–158 genes, selected inside each training fold). Trained the final models.

## Key results
| | ROC-AUC | Balanced acc. |
|---|---|---|
| Majority-class baseline | 0.500 | 0.500 |
| MKI67 only | 0.948 | 0.894 |
| **Logistic regression (L2), 158 DDR genes** | **0.998** | **0.983** |
| 10-gene panel | 0.987 | 0.942 |
| Random 158-gene sets (mean) | 0.999 | 0.992 |

Robust to matched pairs (0.9996) and held-out hospitals (0.997). **Negative finding:** random genes do as well, so the signal is not repair-specific.

## Files
`results/model_comparison.csv`, `robustness.csv`, `random_geneset_baseline.csv`, `panel_size_curve.csv`, `model_coefficients.csv`, `misclassified.csv`, `figures/ml_1_roc.png`, `ml_4_confusion_matrix.png`, `ml_2_random_baseline.png`, `ml_3_panel_size.png`.
