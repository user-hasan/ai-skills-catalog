#!/usr/bin/env python3
"""This report combines handoff, readiness, and progress signals from the full SDLC suite."""

import sys
from pathlib import Path

LIB = Path(__file__).resolve().parents[2] / "sdlc-system" / "python_lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from sdlc_common import execute_configured_script


CONFIG = {
  "file": "generate_integrated_report.py",
  "mode": "summary",
  "summary": "This report combines handoff, readiness, and progress signals from the full SDLC suite.",
  "title": "Integrated SDLC Report",
  "default_output": "integrated_sdlc_report.md",
  "outcomes": [
    "Summarize suite status by phase.",
    "Highlight blocked or failed handoffs.",
    "List recommended next actions for the coordinating role."
  ]
}


if __name__ == "__main__":
    raise SystemExit(execute_configured_script(CONFIG))
