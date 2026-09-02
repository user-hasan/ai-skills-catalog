#!/usr/bin/env python3
"""Prioritize backlog items using weighted product heuristics."""

import sys
from pathlib import Path

LIB = Path(__file__).resolve().parents[2] / "sdlc-system" / "python_lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from sdlc_common import execute_configured_script


CONFIG = {
  "file": "prioritize_features.py",
  "mode": "prioritize",
  "summary": "Prioritize backlog items using weighted product heuristics.",
  "title": "Feature Prioritization",
  "default_output": "prioritized_features.json",
  "preferred_item_keys": [
    "features",
    "backlog"
  ],
  "ranking_fields": {
    "reach": 2,
    "impact": 3,
    "confidence": 2,
    "effort": -1
  }
}


if __name__ == "__main__":
    raise SystemExit(execute_configured_script(CONFIG))
