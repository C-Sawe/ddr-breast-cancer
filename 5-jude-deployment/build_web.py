"""Embed model/model.json into web/template.html -> web/index.html (static, GitHub Pages)."""
import os
here = os.path.dirname(os.path.abspath(__file__))
tpl = open(os.path.join(here, "web", "template.html")).read()
model = open(os.path.join(here, "model", "model.json")).read()
open(os.path.join(here, "web", "index.html"), "w").write(tpl.replace("/*MODEL_JSON*/null", model))
print("wrote web/index.html")
