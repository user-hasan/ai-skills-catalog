#!/usr/bin/env python3
"""Compare architecture options using weighted tradeoff scoring."""

import sys
from pathlib import Path

LIB = Path(__file__).resolve().parents[2] / "sdlc-system" / "python_lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from sdlc_common import execute_configured_script


CONFIG = {
  "file": "calculate_tradeoffs.py",
  "mode": "prioritize",
  "summary": "Compare architecture options using weighted tradeoff scoring.",
  "title": "Architecture Tradeoffs",
  "default_output": "architecture_tradeoffs.json",
  "preferred_item_keys": [
    "options"
  ],
  "ranking_fields": {
    "fitness": 3,
    "cost": -1,
    "operability": 2,
    "complexity": -1
  }
}


if __name__ == "__main__":
    raise SystemExit(execute_configured_script(CONFIG))
