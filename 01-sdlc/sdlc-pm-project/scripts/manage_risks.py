#!/usr/bin/env python3
"""Track project execution risk and mitigations."""

import sys
from pathlib import Path

LIB = Path(__file__).resolve().parents[2] / "sdlc-system" / "python_lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from sdlc_common import execute_configured_script


CONFIG = {
  "file": "manage_risks.py",
  "mode": "risk",
  "summary": "Track project execution risk and mitigations.",
  "title": "Project Risk Register",
  "default_output": "project_risks.json",
  "risk_factors": [
    {
      "title": "Unowned dependency",
      "triggers": [
        "dependency",
        "blocked"
      ],
      "points": 4,
      "level": "high",
      "mitigation": "Assign an owner and due date."
    },
    {
      "title": "Capacity pressure",
      "triggers": [
        "capacity",
        "overload"
      ],
      "points": 3,
      "level": "medium",
      "mitigation": "Reduce scope or rebalance work."
    },
    {
      "title": "Cross-team waiting",
      "triggers": [
        "external",
        "approval"
      ],
      "points": 4,
      "level": "high",
      "mitigation": "Pull approvals forward and define escalations."
    }
  ]
}


if __name__ == "__main__":
    raise SystemExit(execute_configured_script(CONFIG))
