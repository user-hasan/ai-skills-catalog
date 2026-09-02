#!/usr/bin/env python3
"""Check whether the product vision is specific, measurable, and user-centered."""

import sys
from pathlib import Path

LIB = Path(__file__).resolve().parents[2] / "sdlc-system" / "python_lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from sdlc_common import execute_configured_script


CONFIG = {
  "file": "validate_product_vision.py",
  "mode": "validate",
  "summary": "Check whether the product vision is specific, measurable, and user-centered.",
  "title": "Product Vision Validation",
  "default_output": "product_vision_validation.json",
  "required_fields": [
    "vision",
    "users",
    "goals"
  ],
  "rules": [
    {
      "keyword": "metric",
      "message": "A product vision should reference measurable outcomes.",
      "severity": "medium"
    },
    {
      "keyword": "user",
      "message": "A product vision should stay anchored to an explicit target user.",
      "severity": "medium"
    }
  ]
}


if __name__ == "__main__":
    raise SystemExit(execute_configured_script(CONFIG))
