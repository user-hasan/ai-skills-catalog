#!/usr/bin/env python3
"""Create a sprint plan from prioritized work items."""

import sys
from pathlib import Path

LIB = Path(__file__).resolve().parents[2] / "sdlc-system" / "python_lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from sdlc_common import execute_configured_script


CONFIG = {
  "file": "plan_sprint.py",
  "mode": "document",
  "summary": "Create a sprint plan from prioritized work items.",
  "title": "Sprint Plan",
  "default_output": "sprint_plan.json",
  "sections": [
    {
      "title": "Sprint Goal",
      "fields": [
        "goal"
      ],
      "fallback": "State the sprint outcome in one sentence."
    },
    {
      "title": "Committed Work",
      "fields": [
        "backlog"
      ],
      "fallback": "List committed items and dependencies."
    },
    {
      "title": "Capacity and Risks",
      "fields": [
        "capacity",
        "risks"
      ],
      "fallback": "Document available capacity and known risks."
    }
  ]
}


if __name__ == "__main__":
    raise SystemExit(execute_configured_script(CONFIG))
