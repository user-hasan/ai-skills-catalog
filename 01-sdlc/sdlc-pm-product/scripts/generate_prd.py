#!/usr/bin/env python3
"""Generate a PRD from requirement artifacts."""

import sys
from pathlib import Path

LIB = Path(__file__).resolve().parents[2] / "sdlc-system" / "python_lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from sdlc_common import execute_configured_script


CONFIG = {
  "file": "generate_prd.py",
  "mode": "document",
  "summary": "Generate a PRD from requirement artifacts.",
  "title": "Product Requirements Document",
  "default_output": "product_prd.md",
  "sections": [
    {
      "title": "Vision",
      "fields": [
        "vision",
        "goals"
      ],
      "fallback": "Summarize the product vision and target outcomes."
    },
    {
      "title": "Scope",
      "fields": [
        "scope",
        "mvp"
      ],
      "fallback": "Document the MVP and deferred scope."
    },
    {
      "title": "Requirements",
      "fields": [
        "requirements",
        "constraints"
      ],
      "fallback": "List product requirements and constraints."
    },
    {
      "title": "Metrics",
      "fields": [
        "metrics"
      ],
      "fallback": "List launch and adoption metrics."
    }
  ]
}


if __name__ == "__main__":
    raise SystemExit(execute_configured_script(CONFIG))
