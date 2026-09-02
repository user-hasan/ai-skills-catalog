#!/usr/bin/env python3
"""Combine discovery outputs into a concise executive summary."""

import sys
from pathlib import Path

LIB = Path(__file__).resolve().parents[2] / "sdlc-system" / "python_lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from sdlc_common import execute_configured_script


CONFIG = {
  "file": "generate_summary_report.py",
  "mode": "summary",
  "summary": "Combine discovery outputs into a concise executive summary.",
  "title": "Requirements Summary Report",
  "default_output": "requirements_summary.md",
  "outcomes": [
    "Summarize scope, goals, and constraints.",
    "List the highest-risk assumptions and open questions.",
    "Recommend the next downstream SDLC role to activate."
  ]
}


if __name__ == "__main__":
    raise SystemExit(execute_configured_script(CONFIG))
