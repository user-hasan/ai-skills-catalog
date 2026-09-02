#!/usr/bin/env python3
"""Generate user stories and acceptance criteria from product inputs."""

import sys
from pathlib import Path

LIB = Path(__file__).resolve().parents[2] / "sdlc-system" / "python_lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from sdlc_common import execute_configured_script


CONFIG = {
  "file": "generate_user_stories.py",
  "mode": "user-stories",
  "summary": "Generate user stories and acceptance criteria from product inputs.",
  "title": "User Stories",
  "default_output": "user_stories.json",
  "preferred_item_keys": [
    "features",
    "requirements"
  ]
}


if __name__ == "__main__":
    raise SystemExit(execute_configured_script(CONFIG))
