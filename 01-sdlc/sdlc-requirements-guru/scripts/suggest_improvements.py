#!/usr/bin/env python3
"""Suggest architectural, process, feature, quality, and cost improvements."""

import sys
from pathlib import Path

LIB = Path(__file__).resolve().parents[2] / "sdlc-system" / "python_lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from sdlc_common import execute_configured_script


CONFIG = {
  "file": "suggest_improvements.py",
  "mode": "improvement",
  "summary": "Suggest architectural, process, feature, quality, and cost improvements.",
  "title": "Improvement Suggestions",
  "default_output": "improvements.json",
  "recommendations": [
    {
      "title": "Add release metrics",
      "reason": "Metrics align discovery, delivery, and validation.",
      "triggers": [
        "metric",
        "goal"
      ],
      "priority": "medium"
    },
    {
      "title": "Introduce risk-based sequencing",
      "reason": "High-risk dependencies should be explored before implementation expands.",
      "triggers": [
        "legacy",
        "integration",
        "migration"
      ],
      "priority": "high"
    },
    {
      "title": "Split scope into MVP and deferred tracks",
      "reason": "Separating must-have from later work reduces delivery risk.",
      "triggers": [
        "mvp",
        "scope",
        "release"
      ],
      "priority": "high"
    },
    {
      "title": "Define operational ownership",
      "reason": "Availability and incident handling need named owners early.",
      "triggers": [
        "availability",
        "production",
        "support"
      ],
      "priority": "medium"
    }
  ]
}


if __name__ == "__main__":
    raise SystemExit(execute_configured_script(CONFIG))
