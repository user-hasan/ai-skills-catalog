#!/usr/bin/env python3
"""Generate a secret inventory and rotation plan."""

import sys
from pathlib import Path

LIB = Path(__file__).resolve().parents[2] / "sdlc-system" / "python_lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from sdlc_common import execute_configured_script


CONFIG = {
  "file": "manage_secrets.py",
  "mode": "secrets",
  "summary": "Generate a secret inventory and rotation plan.",
  "title": "Secret Management Plan",
  "default_output": "secret_management.json",
  "fallback_items": [
    "database_url",
    "api_key",
    "jwt_signing_key"
  ],
  "storage": "vault-or-secrets-manager"
}


if __name__ == "__main__":
    raise SystemExit(execute_configured_script(CONFIG))
