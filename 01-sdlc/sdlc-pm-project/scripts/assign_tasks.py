#!/usr/bin/env python3
"""Rank tasks or owners to balance work assignments."""

import sys
from pathlib import Path

LIB = Path(__file__).resolve().parents[2] / "sdlc-system" / "python_lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from sdlc_common import execute_configured_script


CONFIG = {
  "file": "assign_tasks.py",
  "mode": "prioritize",
  "summary": "Rank tasks or owners to balance work assignments.",
  "title": "Task Assignment Suggestions",
  "default_output": "task_assignments.json",
  "preferred_item_keys": [
    "tasks",
    "backlog"
  ],
  "ranking_fields": {
    "priority": 3,
    "skill_match": 2,
    "risk": -1,
    "effort": -1
  }
}


if __name__ == "__main__":
    raise SystemExit(execute_configured_script(CONFIG))
