#!/usr/bin/env python3
"""Validate that deployment inputs mention security checks and secret handling."""

import sys
from pathlib import Path

LIB = Path(__file__).resolve().parents[2] / "sdlc-system" / "python_lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from sdlc_common import execute_configured_script


CONFIG = {
  "file": "security_scanner.py",
  "mode": "validate",
  "summary": "Validate that deployment inputs mention security checks and secret handling.",
  "title": "Security Scanner Plan",
  "default_output": "security_scan_plan.json",
  "required_fields": [
    "security"
  ],
  "rules": [
    {
      "keyword": "secret",
      "message": "Security plans should reference secret handling.",
      "severity": "high"
    },
    {
      "keyword": "scan",
      "message": "Deployment plans should define at least one automated security scan.",
      "severity": "medium"
    }
  ]
}


if __name__ == "__main__":
    raise SystemExit(execute_configured_script(CONFIG))
