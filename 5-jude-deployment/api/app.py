"""DDR-Classify API: tumour vs normal breast tissue from DNA-repair gene expression.

Endpoints
  GET  /health                 -> service status
  GET  /genes?model=full|panel -> required genes and input units
  POST /predict                -> JSON {"model": "full"|"panel", "samples": {id: {gene: value}}}
                                  or a CSV upload (field "file"): rows = samples, columns = genes
Values must be log2(RSEM normalized count + 1), as in TCGA RNA-seq v2.
Missing genes are imputed with the training mean (reported back as a warning).
"""
import io, os
import numpy as np
import pandas as pd
import joblib
from flask import Flask, jsonify, request

HERE = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.environ.get("MODEL_DIR", os.path.join(HERE, "..", "model"))
MODELS = {
    "full": joblib.load(os.path.join(MODEL_DIR, "ddr158_logreg.joblib")),
    "panel": joblib.load(os.path.join(MODEL_DIR, "ddr10_panel_logreg.joblib")),
}
MAX_MISSING_FRAC = 0.2

app = Flask(__name__)


def predict_frame(df: pd.DataFrame, which: str):
    bundle = MODELS[which]
    genes, model = bundle["genes"], bundle["model"]
    scaler, lr = model[0], model[-1]
    df = df.apply(pd.to_numeric, errors="coerce")
    missing = [g for g in genes if g not in df.columns]
    if len(missing) > MAX_MISSING_FRAC * len(genes):
        raise ValueError(f"{len(missing)} of {len(genes)} required genes missing (max {int(MAX_MISSING_FRAC*100)}%)")
    X = df.reindex(columns=genes)
    means = pd.Series(scaler.mean_, index=genes)
    X = X.fillna(means)
    if X.values.max() > 30:
        raise ValueError("values look like raw counts; send log2(RSEM + 1)")
    prob = model.predict_proba(X.values)[:, 1]
    contrib = ((X.values - scaler.mean_) / scaler.scale_) * lr.coef_[0]
    out = []
    for i, sid in enumerate(X.index):
        order = np.argsort(-np.abs(contrib[i]))[:5]
        out.append({
            "sample": str(sid),
            "prediction": "Tumour" if prob[i] >= 0.5 else "Normal",
            "p_tumour": round(float(prob[i]), 4),
            "top_drivers": [{"gene": genes[j], "contribution": round(float(contrib[i, j]), 3)} for j in order],
        })
    return out, missing


@app.get("/health")
def health():
    return {"status": "ok", "models": {k: len(v["genes"]) for k, v in MODELS.items()}}


@app.get("/genes")
def genes():
    which = request.args.get("model", "full")
    if which not in MODELS:
        return {"error": "model must be 'full' or 'panel'"}, 400
    return {"model": which, "genes": MODELS[which]["genes"], "units": "log2(RSEM normalized count + 1)"}


@app.post("/predict")
def predict():
    try:
        if "file" in request.files:
            which = request.form.get("model", "full")
            df = pd.read_csv(io.BytesIO(request.files["file"].read()), index_col=0)
        else:
            body = request.get_json(force=True, silent=True) or {}
            which = body.get("model", "full")
            samples = body.get("samples")
            if not isinstance(samples, dict) or not samples:
                return {"error": "send {'samples': {sample_id: {gene: value}}}"}, 400
            df = pd.DataFrame.from_dict(samples, orient="index")
        if which not in MODELS:
            return {"error": "model must be 'full' or 'panel'"}, 400
        results, missing = predict_frame(df, which)
    except ValueError as e:
        return {"error": str(e)}, 422
    resp = {"model": which, "n_samples": len(results), "results": results}
    if missing:
        resp["warning"] = f"{len(missing)} genes missing, imputed with training mean: {missing[:10]}"
    return jsonify(resp)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
