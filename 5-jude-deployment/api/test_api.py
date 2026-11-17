import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app import app

ex = json.load(open(os.path.join(os.path.dirname(__file__), "..", "model", "model.json")))["examples"]

def test_health():
    assert app.test_client().get("/health").json["status"] == "ok"

def test_predict_examples():
    c = app.test_client()
    for m in ("full", "panel"):
        r = c.post("/predict", json={"model": m, "samples": {e["id"]: e["values"] for e in ex}})
        assert r.status_code == 200
        got = {res["sample"]: res["prediction"] for res in r.json["results"]}
        for e in ex:
            assert got[e["id"]] == e["truth"], (m, e["id"], got[e["id"]])

def test_rejects_raw_counts():
    r = app.test_client().post("/predict", json={"samples": {"x": {g: 5000 for g in ex[0]["values"]}}})
    assert r.status_code == 422
