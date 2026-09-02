#!/usr/bin/env python3
"""Create a performance-test plan for endpoints or workflows."""

import sys
from pathlib import Path

LIB = Path(__file__).resolve().parents[2] / "sdlc-system" / "python_lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from sdlc_common import execute_configured_script


CONFIG = {
  "file": "run_performance_test.py",
  "mode": "performance",
  "summary": "Create a performance-test plan for endpoints or workflows.",
  "title": "Performance Test Plan",
  "default_output": "performance_test.json",
  "preferred_item_keys": [
    "endpoints",
    "flows"
  ],
  "fallback_items": [
    "login",
    "search",
    "checkout"
  ],
  "thresholds": {
    "p95_ms": 500,
    "error_rate_percent": 1,
    "throughput_rps": 50
  }
}


if __name__ == "__main__":
    raise SystemExit(execute_configured_script(CONFIG))
