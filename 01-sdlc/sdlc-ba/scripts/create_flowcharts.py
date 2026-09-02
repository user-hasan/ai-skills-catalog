#!/usr/bin/env python3
"""Create Mermaid flowcharts for business processes."""

import sys
from pathlib import Path

LIB = Path(__file__).resolve().parents[2] / "sdlc-system" / "python_lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from sdlc_common import execute_configured_script


CONFIG = {
  "file": "create_flowcharts.py",
  "mode": "flowchart",
  "summary": "Create Mermaid flowcharts for business processes.",
  "title": "Process Flowchart",
  "default_output": "process_flowchart.md",
  "preferred_item_keys": [
    "processes",
    "steps"
  ],
  "fallback_items": [
    {
      "name": "Receive request"
    },
    {
      "name": "Validate input"
    },
    {
      "name": "Execute workflow"
    },
    {
      "name": "Return result"
    }
  ]
}


if __name__ == "__main__":
    raise SystemExit(execute_configured_script(CONFIG))
