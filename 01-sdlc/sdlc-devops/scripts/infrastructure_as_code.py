#!/usr/bin/env python3
"""Plan infrastructure resources and environment strategy."""

import sys
from pathlib import Path

LIB = Path(__file__).resolve().parents[2] / "sdlc-system" / "python_lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from sdlc_common import execute_configured_script


CONFIG = {
  "file": "infrastructure_as_code.py",
  "mode": "iac",
  "summary": "Plan infrastructure resources and environment strategy.",
  "title": "Infrastructure as Code Plan",
  "default_output": "infrastructure_plan.json",
  "default_provider": "aws",
  "providers": {
    "aws": [
      "vpc",
      "private_subnets",
      "ecs_service",
      "rds_instance"
    ],
    "azure": [
      "virtual_network",
      "app_service",
      "postgresql",
      "key_vault"
    ],
    "gcp": [
      "vpc",
      "cloud_run",
      "cloud_sql",
      "secret_manager"
    ]
  },
  "environment_strategy": [
    "separate environments for dev, staging, prod",
    "versioned IaC changes",
    "automated drift review"
  ]
}


if __name__ == "__main__":
    raise SystemExit(execute_configured_script(CONFIG))
