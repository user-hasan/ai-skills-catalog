#!/usr/bin/env python3
"""Analyze regression exposure based on changed areas and existing tests."""

import sys
from pathlib import Path

LIB = Path(__file__).resolve().parents[2] / "sdlc-system" / "python_lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from sdlc_common import execute_configured_script


CONFIG = {
  "file": "regression_analyzer.py",
  "mode": "analysis",
  "summary": "Analyze regression exposure based on changed areas and existing tests.",
  "title": "Regression Analysis",
  "default_output": "regression_analysis.json",
  "required_fields": [
    "changed_areas"
  ],
  "keyword_findings": {
    "payment": "Payment changes should trigger expanded regression and security coverage.",
    "auth": "Authentication changes require session and authorization regression coverage."
  }
}


if __name__ == "__main__":
    raise SystemExit(execute_configured_script(CONFIG))
