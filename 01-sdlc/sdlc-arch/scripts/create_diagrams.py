#!/usr/bin/env python3
"""Create Mermaid diagrams for architectural context and flows."""

import sys
from pathlib import Path

LIB = Path(__file__).resolve().parents[2] / "sdlc-system" / "python_lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from sdlc_common import execute_configured_script


CONFIG = {
  "file": "create_diagrams.py",
  "mode": "flowchart",
  "summary": "Create Mermaid diagrams for architectural context and flows.",
  "title": "Architecture Diagrams",
  "default_output": "architecture_diagrams.md",
  "preferred_item_keys": [
    "components",
    "services"
  ],
  "fallback_items": [
    {
      "name": "User"
    },
    {
      "name": "Frontend"
    },
    {
      "name": "Application Service"
    },
    {
      "name": "Data Store"
    }
  ]
}


if __name__ == "__main__":
    raise SystemExit(execute_configured_script(CONFIG))
