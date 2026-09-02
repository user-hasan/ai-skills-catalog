#!/usr/bin/env python3
"""Detect ambiguous, underspecified, or missing requirement categories."""

import sys
from pathlib import Path

LIB = Path(__file__).resolve().parents[2] / "sdlc-system" / "python_lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from sdlc_common import execute_configured_script


CONFIG = {
  "file": "check_ambiguities.py",
  "mode": "missing",
  "summary": "Detect ambiguous, underspecified, or missing requirement categories.",
  "title": "Ambiguity Review",
  "default_output": "ambiguities.json",
  "coverage_items": [
    {
      "name": "business outcome",
      "tokens": [
        "goal",
        "outcome",
        "metric"
      ],
      "why_it_matters": "Without a measurable outcome, prioritization becomes subjective."
    },
    {
      "name": "user segments",
      "tokens": [
        "user",
        "persona",
        "customer"
      ],
      "why_it_matters": "Feature value depends on the target audience."
    },
    {
      "name": "scope boundaries",
      "tokens": [
        "scope",
        "out-of-scope",
        "mvp"
      ],
      "why_it_matters": "Teams need a clear release boundary."
    },
    {
      "name": "constraints",
      "tokens": [
        "constraint",
        "budget",
        "timeline",
        "legacy"
      ],
      "why_it_matters": "Constraints drive tradeoffs."
    },
    {
      "name": "quality targets",
      "tokens": [
        "performance",
        "security",
        "availability"
      ],
      "why_it_matters": "Non-functional targets shape design and testing."
    }
  ]
}


if __name__ == "__main__":
    raise SystemExit(execute_configured_script(CONFIG))
