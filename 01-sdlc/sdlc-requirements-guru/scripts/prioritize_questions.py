#!/usr/bin/env python3
"""Rank discovery questions so the most decision-critical questions are asked first."""

import sys
from pathlib import Path

LIB = Path(__file__).resolve().parents[2] / "sdlc-system" / "python_lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from sdlc_common import execute_configured_script


CONFIG = {
  "file": "prioritize_questions.py",
  "mode": "prioritize",
  "summary": "Rank discovery questions so the most decision-critical questions are asked first.",
  "title": "Prioritized Questions",
  "default_output": "prioritized_questions.json",
  "preferred_item_keys": [
    "questions",
    "items"
  ],
  "ranking_fields": {
    "priority": 4,
    "impact": 3,
    "risk": 2,
    "effort": -1
  },
  "fallback_items": [
    {
      "name": "Business outcome",
      "priority": "high",
      "impact": 3,
      "risk": 2
    },
    {
      "name": "User segments",
      "priority": "high",
      "impact": 3,
      "risk": 1
    },
    {
      "name": "Scope boundary",
      "priority": "high",
      "impact": 3,
      "risk": 3
    }
  ]
}


if __name__ == "__main__":
    raise SystemExit(execute_configured_script(CONFIG))
