#!/usr/bin/env python3
"""Check whether selected patterns cover the required qualities."""

import sys
from pathlib import Path

LIB = Path(__file__).resolve().parents[2] / "sdlc-system" / "python_lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from sdlc_common import execute_configured_script


CONFIG = {
  "file": "validate_patterns.py",
  "mode": "validate",
  "summary": "Check whether selected patterns cover the required qualities.",
  "title": "Pattern Validation",
  "default_output": "pattern_validation.json",
  "required_fields": [
    "patterns"
  ],
  "rules": [
    {
      "keyword": "security",
      "message": "Security-sensitive designs should include explicit security patterns.",
      "severity": "high"
    },
    {
      "keyword": "availability",
      "message": "Availability-sensitive designs should include resilience patterns.",
      "severity": "medium"
    }
  ]
}


if __name__ == "__main__":
    raise SystemExit(execute_configured_script(CONFIG))
