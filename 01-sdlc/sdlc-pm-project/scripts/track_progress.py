#!/usr/bin/env python3
"""Track project progress using issue or task status."""

import sys
from pathlib import Path

LIB = Path(__file__).resolve().parents[2] / "sdlc-system" / "python_lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from sdlc_common import execute_configured_script


CONFIG = {
  "file": "track_progress.py",
  "mode": "tracking",
  "summary": "Track project progress using issue or task status.",
  "title": "Project Progress",
  "default_output": "project_progress.json",
  "preferred_item_keys": [
    "tasks",
    "items"
  ]
}


if __name__ == "__main__":
    raise SystemExit(execute_configured_script(CONFIG))
