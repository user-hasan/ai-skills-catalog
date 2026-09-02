#!/usr/bin/env python3
"""Generate rollback criteria and rollback steps."""

import sys
from pathlib import Path

LIB = Path(__file__).resolve().parents[2] / "sdlc-system" / "python_lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from sdlc_common import execute_configured_script


CONFIG = {
  "file": "rollback_manager.py",
  "mode": "document",
  "summary": "Generate rollback criteria and rollback steps.",
  "title": "Rollback Plan",
  "default_output": "rollback_plan.json",
  "sections": [
    {
      "title": "Rollback Triggers",
      "fields": [
        "triggers"
      ],
      "fallback": "List metrics or incidents that force rollback."
    },
    {
      "title": "Rollback Steps",
      "fields": [
        "steps"
      ],
      "fallback": "Document technical rollback actions and verification checks."
    },
    {
      "title": "Communication",
      "fields": [
        "communication"
      ],
      "fallback": "Describe who is notified during rollback."
    }
  ]
}


if __name__ == "__main__":
    raise SystemExit(execute_configured_script(CONFIG))
