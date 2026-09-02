#!/usr/bin/env python3
"""Rank candidate features and identify the MVP cut line."""

import sys
from pathlib import Path

LIB = Path(__file__).resolve().parents[2] / "sdlc-system" / "python_lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from sdlc_common import execute_configured_script


CONFIG = {
  "file": "calculate_mvp_scope.py",
  "mode": "prioritize",
  "summary": "Rank candidate features and identify the MVP cut line.",
  "title": "MVP Scope",
  "default_output": "mvp_scope.json",
  "preferred_item_keys": [
    "features",
    "backlog"
  ],
  "ranking_fields": {
    "value": 3,
    "risk": -1,
    "effort": -1,
    "urgency": 2
  }
}


if __name__ == "__main__":
    raise SystemExit(execute_configured_script(CONFIG))
