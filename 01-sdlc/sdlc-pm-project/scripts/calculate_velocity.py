#!/usr/bin/env python3
"""Calculate completed work percentage as a simple velocity proxy."""

import sys
from pathlib import Path

LIB = Path(__file__).resolve().parents[2] / "sdlc-system" / "python_lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from sdlc_common import execute_configured_script


CONFIG = {
  "file": "calculate_velocity.py",
  "mode": "tracking",
  "summary": "Calculate completed work percentage as a simple velocity proxy.",
  "title": "Velocity Snapshot",
  "default_output": "velocity.json",
  "preferred_item_keys": [
    "tasks",
    "stories"
  ]
}


if __name__ == "__main__":
    raise SystemExit(execute_configured_script(CONFIG))
