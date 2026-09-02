#!/usr/bin/env python3
"""Score delivery risk and list concrete mitigation actions."""

import sys
from pathlib import Path

LIB = Path(__file__).resolve().parents[2] / "sdlc-system" / "python_lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from sdlc_common import execute_configured_script


CONFIG = {
  "file": "calculate_risk_score.py",
  "mode": "risk",
  "summary": "Score delivery risk and list concrete mitigation actions.",
  "title": "Risk Score",
  "default_output": "risk_score.json",
  "risk_factors": [
    {
      "title": "Legacy dependencies",
      "triggers": [
        "legacy",
        "migration"
      ],
      "points": 5,
      "level": "high",
      "mitigation": "Create rollback and migration rehearsal plans."
    },
    {
      "title": "Compliance pressure",
      "triggers": [
        "compliance",
        "audit",
        "regulation"
      ],
      "points": 4,
      "level": "high",
      "mitigation": "Capture policy checkpoints and evidence artifacts early."
    },
    {
      "title": "Scale sensitivity",
      "triggers": [
        "scale",
        "performance",
        "throughput"
      ],
      "points": 3,
      "level": "medium",
      "mitigation": "Define load profiles and measurable thresholds."
    },
    {
      "title": "Cross-team dependency",
      "triggers": [
        "integration",
        "enterprise",
        "third-party"
      ],
      "points": 4,
      "level": "high",
      "mitigation": "Track dependencies with owners and dates."
    },
    {
      "title": "Undefined success metrics",
      "triggers": [
        "goal",
        "metric"
      ],
      "points": 2,
      "level": "medium",
      "mitigation": "Publish outcome metrics before delivery starts."
    }
  ]
}


if __name__ == "__main__":
    raise SystemExit(execute_configured_script(CONFIG))
