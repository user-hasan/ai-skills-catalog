#!/usr/bin/env python3
"""Compare current and target states and list missing capabilities."""

import sys
from pathlib import Path

LIB = Path(__file__).resolve().parents[2] / "sdlc-system" / "python_lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from sdlc_common import execute_configured_script


CONFIG = {
  "file": "gap_analysis.py",
  "mode": "missing",
  "summary": "Compare current and target states and list missing capabilities.",
  "title": "Gap Analysis",
  "default_output": "gap_analysis.json",
  "coverage_items": [
    {
      "name": "current-state process",
      "tokens": [
        "current",
        "existing"
      ],
      "why_it_matters": "Gap analysis needs a baseline."
    },
    {
      "name": "target-state process",
      "tokens": [
        "target",
        "future"
      ],
      "why_it_matters": "Gap analysis needs an end state."
    },
    {
      "name": "data rules",
      "tokens": [
        "data",
        "validation"
      ],
      "why_it_matters": "Business-rule gaps often hide in data handling."
    }
  ]
}


if __name__ == "__main__":
    raise SystemExit(execute_configured_script(CONFIG))
