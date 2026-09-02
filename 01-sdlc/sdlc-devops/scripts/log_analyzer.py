#!/usr/bin/env python3
"""Summarize logs and highlight high-signal failures."""

import sys
from pathlib import Path

LIB = Path(__file__).resolve().parents[2] / "sdlc-system" / "python_lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from sdlc_common import execute_configured_script


CONFIG = {
  "file": "log_analyzer.py",
  "mode": "logs",
  "summary": "Summarize logs and highlight high-signal failures.",
  "title": "Log Analysis",
  "default_output": "log_analysis.json"
}


if __name__ == "__main__":
    raise SystemExit(execute_configured_script(CONFIG))
