#!/usr/bin/env python3
"""Generate a CI/CD plan and starter snippet for the chosen platform."""

import sys
from pathlib import Path

LIB = Path(__file__).resolve().parents[2] / "sdlc-system" / "python_lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from sdlc_common import execute_configured_script


CONFIG = {
  "file": "setup_cicd.py",
  "mode": "cicd",
  "summary": "Generate a CI/CD plan and starter snippet for the chosen platform.",
  "title": "CI/CD Plan",
  "default_output": "cicd_plan.json",
  "default_platform": "github-actions",
  "snippets": {
    "github-actions": "name: ci\non: [push]\njobs:\n  build:\n    runs-on: ubuntu-latest\n",
    "gitlab-ci": "stages:\n  - build\n  - test\n",
    "jenkins": "pipeline { agent any; stages { stage('build') { steps { echo 'build' } } } }\n"
  }
}


if __name__ == "__main__":
    raise SystemExit(execute_configured_script(CONFIG))
