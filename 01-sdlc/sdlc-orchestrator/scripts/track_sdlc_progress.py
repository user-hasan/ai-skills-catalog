#!/usr/bin/env python3
"""Track suite progress across all SDLC stages."""

import sys
from pathlib import Path

LIB = Path(__file__).resolve().parents[2] / "sdlc-system" / "python_lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from sdlc_common import execute_configured_script


CONFIG = {
  "file": "track_sdlc_progress.py",
  "mode": "integrated",
  "summary": "Track suite progress across all SDLC stages.",
  "title": "SDLC Progress",
  "default_output": "sdlc_progress.json",
  "stages": [
    "requirements-discovery",
    "product-planning",
    "business-analysis",
    "architecture",
    "development",
    "quality-assurance",
    "devops",
    "project-management",
    "orchestration"
  ],
  "handoff_actions": [
    "Track completed phases.",
    "Show pending transitions.",
    "Highlight blocked stages."
  ]
}


if __name__ == "__main__":
    raise SystemExit(execute_configured_script(CONFIG))
