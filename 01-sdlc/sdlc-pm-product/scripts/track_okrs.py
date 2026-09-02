#!/usr/bin/env python3
"""Track OKR progress using structured status items."""

import sys
from pathlib import Path

LIB = Path(__file__).resolve().parents[2] / "sdlc-system" / "python_lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from sdlc_common import execute_configured_script


CONFIG = {
  "file": "track_okrs.py",
  "mode": "tracking",
  "summary": "Track OKR progress using structured status items.",
  "title": "OKR Tracking",
  "default_output": "okr_status.json",
  "preferred_item_keys": [
    "key_results",
    "items"
  ]
}


if __name__ == "__main__":
    raise SystemExit(execute_configured_script(CONFIG))
