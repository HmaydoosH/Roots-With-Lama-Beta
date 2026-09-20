from pathlib import Path
import runpy

story_app = (
    Path(__file__).resolve().parents[1]
    / "story_studio"
    / "story_app.py"
)

runpy.run_path(
    str(story_app),
    run_name="__main__"
)
