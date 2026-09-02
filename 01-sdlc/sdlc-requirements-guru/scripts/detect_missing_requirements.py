#!/usr/bin/env python3
"""Flag missing requirements categories before planning begins."""

import sys
from pathlib import Path

LIB = Path(__file__).resolve().parents[2] / "sdlc-system" / "python_lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from sdlc_common import execute_configured_script


CONFIG = {
  "file": "detect_missing_requirements.py",
  "mode": "missing",
  "summary": "Flag missing requirements categories before planning begins.",
  "title": "Missing Requirements",
  "default_output": "missing_requirements.json",
  "coverage_items": [
    {
      "name": "stakeholders",
      "tokens": [
        "stakeholder",
        "owner",
        "approver"
      ],
      "why_it_matters": "Approval flow changes schedule and scope."
    },
    {
      "name": "data inputs",
      "tokens": [
        "data",
        "source",
        "import"
      ],
      "why_it_matters": "Data availability and quality affect design and testing."
    },
    {
      "name": "error handling",
      "tokens": [
        "error",
        "retry",
        "failure"
      ],
      "why_it_matters": "Resilience assumptions must be explicit."
    },
    {
      "name": "support model",
      "tokens": [
        "support",
        "ops",
        "runbook"
      ],
      "why_it_matters": "Operational readiness needs owners and procedures."
    }
  ]
}


if __name__ == "__main__":
    raise SystemExit(execute_configured_script(CONFIG))
