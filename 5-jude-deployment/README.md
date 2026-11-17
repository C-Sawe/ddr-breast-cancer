# 5 · Deployment and presentation
**Owner: Jude Makau (166487)**

## What I did
- Exported the final models: `model/ddr158_logreg.joblib`, `model/ddr10_panel_logreg.joblib`, and `model/model.json` for the browser.
- **Web app** (`web/`): static page on GitHub Pages. The model runs in JavaScript (standardise → weighted sum → sigmoid), so no server is needed. It shows the probability and the genes that drove each prediction, and accepts pasted or uploaded CSV values. Verified to give identical probabilities to scikit-learn.
- **REST API** (`api/`): Flask + gunicorn with `/health`, `/genes` and `/predict` (JSON or CSV upload). It rejects raw counts and imputes up to 20% missing genes. Includes 3 pytest tests and a Dockerfile.
- Built the presentation slides.

## Run
```bash
python build_web.py                 # rebuild web/index.html from model/model.json
pip install -r api/requirements.txt && pytest api   # tests
docker build -t ddr-classify . && docker run -p 8000:8000 ddr-classify
curl -F model=panel -F file=@api/example_samples.csv localhost:8000/predict
```
Live app: https://c-sawe.github.io/ddr-breast-cancer/
