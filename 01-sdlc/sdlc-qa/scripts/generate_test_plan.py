#!/usr/bin/env python3
"""Generate a test plan from user stories and constraints."""

import sys
from pathlib import Path

LIB = Path(__file__).resolve().parents[2] / "sdlc-system" / "python_lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from sdlc_common import execute_configured_script


CONFIG = {
  "file": "generate_test_plan.py",
  "mode": "document",
  "summary": "Generate a test plan from user stories and constraints.",
  "title": "Test Plan",
  "default_output": "test_plan.json",
  "sections": [
    {
      "title": "Scope",
      "fields": [
        "scope",
        "stories"
      ],
      "fallback": "Define the release or change under test."
    },
    {
      "title": "Test Types",
      "fields": [
        "test_types"
      ],
      "fallback": "List functional, integration, regression, performance, and security coverage."
    },
    {
      "title": "Exit Criteria",
      "fields": [
        "exit_criteria"
      ],
      "fallback": "Describe pass/fail gates for release."
    }
  ]
}


if __name__ == "__main__":
    raise SystemExit(execute_configured_script(CONFIG))
