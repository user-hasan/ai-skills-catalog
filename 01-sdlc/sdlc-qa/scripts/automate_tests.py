#!/usr/bin/env python3
"""Map test cases to automation targets and frameworks."""

import sys
from pathlib import Path

LIB = Path(__file__).resolve().parents[2] / "sdlc-system" / "python_lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from sdlc_common import execute_configured_script


CONFIG = {
  "file": "automate_tests.py",
  "mode": "document",
  "summary": "Map test cases to automation targets and frameworks.",
  "title": "Automation Plan",
  "default_output": "automation_plan.json",
  "sections": [
    {
      "title": "Framework",
      "fields": [
        "framework"
      ],
      "fallback": "Choose the automation framework and explain why."
    },
    {
      "title": "Targets",
      "fields": [
        "tests"
      ],
      "fallback": "List test cases that should become automated regression checks."
    },
    {
      "title": "Execution Strategy",
      "fields": [
        "pipeline"
      ],
      "fallback": "Describe how automation runs in CI and nightly jobs."
    }
  ]
}


if __name__ == "__main__":
    raise SystemExit(execute_configured_script(CONFIG))
