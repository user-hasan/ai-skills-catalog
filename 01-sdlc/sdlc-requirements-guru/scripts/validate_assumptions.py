#!/usr/bin/env python3
"""Validate assumptions and identify the assumptions that need proof."""

import sys
from pathlib import Path

LIB = Path(__file__).resolve().parents[2] / "sdlc-system" / "python_lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from sdlc_common import execute_configured_script


CONFIG = {
  "file": "validate_assumptions.py",
  "mode": "validate",
  "summary": "Validate assumptions and identify the assumptions that need proof.",
  "title": "Assumption Validation",
  "default_output": "validated_assumptions.json",
  "required_fields": [
    "assumptions"
  ],
  "rules": [
    {
      "keyword": "owner",
      "message": "Each major assumption should have an owner or validation source.",
      "severity": "medium"
    },
    {
      "keyword": "date",
      "message": "Time-sensitive assumptions should include a validation date.",
      "severity": "medium"
    }
  ]
}


if __name__ == "__main__":
    raise SystemExit(execute_configured_script(CONFIG))
