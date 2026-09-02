#!/usr/bin/env python3
"""Generate a stakeholder-facing status report from delivery data."""

import sys
from pathlib import Path

LIB = Path(__file__).resolve().parents[2] / "sdlc-system" / "python_lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from sdlc_common import execute_configured_script


CONFIG = {
  "file": "generate_reports.py",
  "mode": "summary",
  "summary": "Generate a stakeholder-facing status report from delivery data.",
  "title": "Stakeholder Report",
  "default_output": "stakeholder_report.md",
  "outcomes": [
    "Report progress, blockers, and next milestones.",
    "Summarize risks and mitigation status.",
    "List decisions or approvals needed from stakeholders."
  ]
}


if __name__ == "__main__":
    raise SystemExit(execute_configured_script(CONFIG))
