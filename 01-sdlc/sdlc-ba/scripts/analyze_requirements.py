#!/usr/bin/env python3
"""Analyze requirements for clarity, completeness, and dependency awareness."""

import sys
from pathlib import Path

LIB = Path(__file__).resolve().parents[2] / "sdlc-system" / "python_lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from sdlc_common import execute_configured_script


CONFIG = {
  "file": "analyze_requirements.py",
  "mode": "analysis",
  "summary": "Analyze requirements for clarity, completeness, and dependency awareness.",
  "title": "Requirement Analysis",
  "default_output": "requirement_analysis.json",
  "required_fields": [
    "requirements"
  ],
  "keyword_findings": {
    "integration": "Integration requirements should name protocols, owners, and failure behavior."
  }
}


if __name__ == "__main__":
    raise SystemExit(execute_configured_script(CONFIG))
