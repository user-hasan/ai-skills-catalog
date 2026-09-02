#!/usr/bin/env python3
"""Evaluate candidate architectures against system constraints."""

import sys
from pathlib import Path

LIB = Path(__file__).resolve().parents[2] / "sdlc-system" / "python_lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from sdlc_common import execute_configured_script


CONFIG = {
  "file": "evaluate_architecture.py",
  "mode": "architecture",
  "summary": "Evaluate candidate architectures against system constraints.",
  "title": "Architecture Evaluation",
  "default_output": "architecture_evaluation.json",
  "patterns": [
    {
      "name": "Modular monolith",
      "triggers": [
        "monolith",
        "simple",
        "single-team"
      ],
      "why": "Optimizes cohesion and delivery speed for small to medium systems.",
      "tradeoffs": [
        "Lower operational complexity",
        "Scaling boundaries need discipline"
      ]
    },
    {
      "name": "Event-driven services",
      "triggers": [
        "integration",
        "async",
        "throughput"
      ],
      "why": "Improves decoupling and resilience across service boundaries.",
      "tradeoffs": [
        "More observability and contract management required"
      ]
    },
    {
      "name": "Layered service",
      "triggers": [
        "enterprise",
        "audit",
        "workflow"
      ],
      "why": "Fits regulated and business-rule heavy systems.",
      "tradeoffs": [
        "Can accumulate cross-layer coupling"
      ]
    }
  ]
}


if __name__ == "__main__":
    raise SystemExit(execute_configured_script(CONFIG))
