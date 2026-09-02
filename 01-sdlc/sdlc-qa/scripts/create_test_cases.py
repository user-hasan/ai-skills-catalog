#!/usr/bin/env python3
"""Create structured test cases from stories or workflows."""

import sys
from pathlib import Path

LIB = Path(__file__).resolve().parents[2] / "sdlc-system" / "python_lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from sdlc_common import execute_configured_script


CONFIG = {
  "file": "create_test_cases.py",
  "mode": "tests",
  "summary": "Create structured test cases from stories or workflows.",
  "title": "Test Cases",
  "default_output": "test_cases.json",
  "preferred_item_keys": [
    "stories",
    "scenarios"
  ],
  "fallback_items": [
    "happy path",
    "negative path",
    "authorization",
    "boundary values"
  ]
}


if __name__ == "__main__":
    raise SystemExit(execute_configured_script(CONFIG))
