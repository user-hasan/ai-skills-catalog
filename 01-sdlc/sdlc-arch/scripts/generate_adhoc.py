#!/usr/bin/env python3
"""Generate ADR-style decision notes from architecture findings."""

import sys
from pathlib import Path

LIB = Path(__file__).resolve().parents[2] / "sdlc-system" / "python_lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from sdlc_common import execute_configured_script


CONFIG = {
  "file": "generate_adhoc.py",
  "mode": "document",
  "summary": "Generate ADR-style decision notes from architecture findings.",
  "title": "Architecture Decision Record",
  "default_output": "architecture_adrs.md",
  "sections": [
    {
      "title": "Context",
      "fields": [
        "context",
        "constraints"
      ],
      "fallback": "Describe the system context and the forces driving the decision."
    },
    {
      "title": "Decision",
      "fields": [
        "decision"
      ],
      "fallback": "State the chosen architecture or technology direction."
    },
    {
      "title": "Consequences",
      "fields": [
        "tradeoffs",
        "risks"
      ],
      "fallback": "List positive and negative consequences."
    }
  ]
}


if __name__ == "__main__":
    raise SystemExit(execute_configured_script(CONFIG))
