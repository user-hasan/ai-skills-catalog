#!/usr/bin/env python3
"""Validate artifact completeness before phase transitions."""

import sys
from pathlib import Path

LIB = Path(__file__).resolve().parents[2] / "sdlc-system" / "python_lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from sdlc_common import execute_configured_script


CONFIG = {
  "file": "validate_artifacts.py",
  "mode": "validate",
  "summary": "Validate artifact completeness before phase transitions.",
  "title": "Artifact Validation",
  "default_output": "artifact_validation.json",
  "required_fields": [
    "artifact_type"
  ],
  "rules": [
    {
      "keyword": "owner",
      "message": "Artifacts should identify an owner or role.",
      "severity": "medium"
    },
    {
      "keyword": "status",
      "message": "Artifacts should expose a status or readiness value.",
      "severity": "medium"
    }
  ]
}


if __name__ == "__main__":
    raise SystemExit(execute_configured_script(CONFIG))
