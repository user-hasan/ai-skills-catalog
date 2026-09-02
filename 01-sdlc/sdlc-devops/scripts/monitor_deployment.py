#!/usr/bin/env python3
"""Describe deployment monitoring dashboards and alerts."""

import sys
from pathlib import Path

LIB = Path(__file__).resolve().parents[2] / "sdlc-system" / "python_lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from sdlc_common import execute_configured_script


CONFIG = {
  "file": "monitor_deployment.py",
  "mode": "document",
  "summary": "Describe deployment monitoring dashboards and alerts.",
  "title": "Deployment Monitoring Plan",
  "default_output": "monitoring_plan.json",
  "sections": [
    {
      "title": "Dashboards",
      "fields": [
        "dashboards"
      ],
      "fallback": "Track latency, throughput, errors, and resource saturation."
    },
    {
      "title": "Alerts",
      "fields": [
        "alerts"
      ],
      "fallback": "Alert on failed deploys, elevated error rates, and saturation."
    },
    {
      "title": "Escalation",
      "fields": [
        "owners"
      ],
      "fallback": "List on-call and incident owners."
    }
  ]
}


if __name__ == "__main__":
    raise SystemExit(execute_configured_script(CONFIG))
