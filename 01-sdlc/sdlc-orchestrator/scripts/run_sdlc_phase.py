#!/usr/bin/env python3
"""Run a selected SDLC phase and summarize readiness."""

import sys
from pathlib import Path

LIB = Path(__file__).resolve().parents[2] / "sdlc-system" / "python_lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from sdlc_common import execute_configured_script


CONFIG = {
  "file": "run_sdlc_phase.py",
  "mode": "integrated",
  "summary": "Run a selected SDLC phase and summarize readiness.",
  "title": "SDLC Phase Runner",
  "default_output": "phase_run.json",
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
    "Validate required upstream artifacts.",
    "Run the target role scripts.",
    "Publish handoff status for the next role."
  ]
}


if __name__ == "__main__":
    raise SystemExit(execute_configured_script(CONFIG))
