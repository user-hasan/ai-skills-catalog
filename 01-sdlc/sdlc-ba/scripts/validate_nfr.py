#!/usr/bin/env python3
"""Validate that non-functional requirements are explicit and testable."""

import sys
from pathlib import Path

LIB = Path(__file__).resolve().parents[2] / "sdlc-system" / "python_lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from sdlc_common import execute_configured_script


CONFIG = {
  "file": "validate_nfr.py",
  "mode": "validate",
  "summary": "Validate that non-functional requirements are explicit and testable.",
  "title": "NFR Validation",
  "default_output": "nfr_validation.json",
  "required_fields": [
    "non_functional_requirements"
  ],
  "rules": [
    {
      "keyword": "latency",
      "message": "NFRs should include measurable latency or throughput targets when performance matters.",
      "severity": "medium"
    },
    {
      "keyword": "availability",
      "message": "Availability-sensitive systems should include uptime or recovery targets.",
      "severity": "medium"
    }
  ]
}


if __name__ == "__main__":
    raise SystemExit(execute_configured_script(CONFIG))
