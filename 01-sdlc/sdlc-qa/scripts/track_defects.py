#!/usr/bin/env python3
"""Track open and resolved defects from a defect list."""

import sys
from pathlib import Path

LIB = Path(__file__).resolve().parents[2] / "sdlc-system" / "python_lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from sdlc_common import execute_configured_script


CONFIG = {
  "file": "track_defects.py",
  "mode": "tracking",
  "summary": "Track open and resolved defects from a defect list.",
  "title": "Defect Tracking",
  "default_output": "defect_tracking.json",
  "preferred_item_keys": [
    "defects",
    "items"
  ]
}


if __name__ == "__main__":
    raise SystemExit(execute_configured_script(CONFIG))
