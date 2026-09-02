#!/usr/bin/env python3
"""Prepare recurring meeting agendas and expected outcomes."""

import sys
from pathlib import Path

LIB = Path(__file__).resolve().parents[2] / "sdlc-system" / "python_lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from sdlc_common import execute_configured_script


CONFIG = {
  "file": "coordinate_meetings.py",
  "mode": "document",
  "summary": "Prepare recurring meeting agendas and expected outcomes.",
  "title": "Meeting Coordination Plan",
  "default_output": "meeting_plan.json",
  "sections": [
    {
      "title": "Cadence",
      "fields": [
        "cadence"
      ],
      "fallback": "Document meeting frequency and attendees."
    },
    {
      "title": "Agenda",
      "fields": [
        "agenda"
      ],
      "fallback": "List agenda topics and owners."
    },
    {
      "title": "Decisions",
      "fields": [
        "decisions"
      ],
      "fallback": "List decisions expected from the meeting."
    }
  ]
}


if __name__ == "__main__":
    raise SystemExit(execute_configured_script(CONFIG))
