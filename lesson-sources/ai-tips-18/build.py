"""Render the lesson using the shared narrated-card layout."""
import json
from pathlib import Path
import sys
import tempfile

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "ai-tips-19"))
import render

render.STEM = "ai-tips-18-save-the-case-that-failed"
render.SCENES = json.loads((HERE / "scenes.json").read_text())
with tempfile.TemporaryDirectory() as tmp:
    render.render(Path(tmp), "AI TIPS   /   18")
