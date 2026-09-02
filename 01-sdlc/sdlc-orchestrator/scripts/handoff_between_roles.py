#!/usr/bin/env python3
"""Create a structured handoff package between two SDLC roles."""

import sys
from pathlib import Path

LIB = Path(__file__).resolve().parents[2] / "sdlc-system" / "python_lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from sdlc_common import execute_configured_script


CONFIG = {
  "file": "handoff_between_roles.py",
  "mode": "summary",
  "summary": "Create a structured handoff package between two SDLC roles.",
  "title": "Role Handoff",
  "default_output": "role_handoff.json",
  "outcomes": [
    "Summarize source artifact quality.",
    "List mandatory downstream actions.",
    "Call out missing or risky handoff details."
  ]
}


if __name__ == "__main__":
    raise SystemExit(execute_configured_script(CONFIG))
