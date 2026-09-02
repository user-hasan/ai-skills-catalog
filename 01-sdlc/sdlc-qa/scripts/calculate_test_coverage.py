#!/usr/bin/env python3
"""Calculate test coverage progress from scenario status."""

import sys
from pathlib import Path

LIB = Path(__file__).resolve().parents[2] / "sdlc-system" / "python_lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from sdlc_common import execute_configured_script


CONFIG = {
  "file": "calculate_test_coverage.py",
  "mode": "tracking",
  "summary": "Calculate test coverage progress from scenario status.",
  "title": "Test Coverage",
  "default_output": "test_coverage.json",
  "preferred_item_keys": [
    "test_cases",
    "items"
  ]
}


if __name__ == "__main__":
    raise SystemExit(execute_configured_script(CONFIG))
