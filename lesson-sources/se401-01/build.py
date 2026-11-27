"""Render the lesson using the shared narrated-card layout."""
import json
from pathlib import Path
import sys
import tempfile

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "ai-tips-19"))
import render

render.STEM = "se401-01-build-the-baseline"
render.SCENES = json.loads((HERE / "scenes.json").read_text())
frames = {int(p.stem): p for p in (HERE / "frames").glob("*.png")}
with tempfile.TemporaryDirectory() as tmp:
    render.render(Path(tmp), "SE 401   /   LESSON 01", frames)
