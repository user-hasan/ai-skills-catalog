#!/usr/bin/env python3
"""Document how to roll a failed SDLC phase back to a stable state."""

import sys
from pathlib import Path

LIB = Path(__file__).resolve().parents[2] / "sdlc-system" / "python_lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from sdlc_common import execute_configured_script


CONFIG = {
  "file": "rollback_phase.py",
  "mode": "document",
  "summary": "Document how to roll a failed SDLC phase back to a stable state.",
  "title": "Phase Rollback",
  "default_output": "phase_rollback.json",
  "sections": [
    {
      "title": "Trigger",
      "fields": [
        "trigger"
      ],
      "fallback": "Describe the failure that forces rollback."
    },
    {
      "title": "Rollback Steps",
      "fields": [
        "steps"
      ],
      "fallback": "Describe how to restore a valid upstream artifact set."
    },
    {
      "title": "Recovery Criteria",
      "fields": [
        "criteria"
      ],
      "fallback": "Document how to know rollback succeeded."
    }
  ]
}


if __name__ == "__main__":
    raise SystemExit(execute_configured_script(CONFIG))
