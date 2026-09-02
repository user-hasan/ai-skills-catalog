#!/usr/bin/env python3
"""Measure how complete and implementation-ready a project brief is."""

import sys
from pathlib import Path

LIB = Path(__file__).resolve().parents[2] / "sdlc-system" / "python_lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from sdlc_common import execute_configured_script


CONFIG = {
  "file": "analyze_project_completeness.py",
  "mode": "analysis",
  "summary": "Measure how complete and implementation-ready a project brief is.",
  "title": "Project Completeness Analysis",
  "default_output": "project_completeness.json",
  "required_fields": [
    "problem_statement",
    "users",
    "goals",
    "scope",
    "constraints"
  ],
  "recommendations": [
    {
      "title": "Clarify user outcomes",
      "reason": "The brief must connect scope to measurable user value.",
      "triggers": [
        "user",
        "customer"
      ],
      "priority": "high"
    },
    {
      "title": "Document constraints",
      "reason": "Architectural and delivery choices depend on explicit constraints.",
      "triggers": [
        "legacy",
        "integration",
        "compliance"
      ],
      "priority": "high"
    },
    {
      "title": "Capture non-functional goals",
      "reason": "Performance, security, and availability targets shape every later phase.",
      "triggers": [
        "security",
        "performance",
        "scale"
      ],
      "priority": "medium"
    }
  ],
  "keyword_findings": {
    "legacy": "Legacy-system work usually needs migration and rollback planning.",
    "enterprise": "Enterprise delivery usually needs stakeholder and compliance mapping."
  }
}


if __name__ == "__main__":
    raise SystemExit(execute_configured_script(CONFIG))
