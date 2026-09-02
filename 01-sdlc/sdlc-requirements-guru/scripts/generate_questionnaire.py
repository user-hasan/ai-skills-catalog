#!/usr/bin/env python3
"""Generate a discovery questionnaire tailored to the current project context."""

import sys
from pathlib import Path

LIB = Path(__file__).resolve().parents[2] / "sdlc-system" / "python_lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from sdlc_common import execute_configured_script


CONFIG = {
  "file": "generate_questionnaire.py",
  "mode": "questionnaire",
  "summary": "Generate a discovery questionnaire tailored to the current project context.",
  "title": "Requirements Questionnaire",
  "default_output": "requirements_questionnaire.json",
  "required_fields": [
    "problem_statement",
    "users",
    "goals"
  ],
  "questions": [
    {
      "priority": "high",
      "text": "What business problem becomes smaller after this project ships?"
    },
    {
      "priority": "high",
      "text": "Which user groups depend on this system and what outcome matters most to each group?"
    },
    {
      "priority": "high",
      "text": "What must be delivered in the first release versus later releases?"
    },
    {
      "priority": "medium",
      "text": "Which integrations, data sources, or external systems are already fixed?"
    },
    {
      "priority": "medium",
      "text": "Which security, privacy, audit, or regulatory constraints already exist?"
    }
  ],
  "domain_questions": {
    "web": [
      "Which browsers, devices, and responsive breakpoints must be supported?",
      "Are SEO, analytics, and public caching part of scope?"
    ],
    "mobile": [
      "Which mobile OS versions and offline behaviors must be supported?",
      "Do push notifications, background sync, or device permissions matter?"
    ],
    "enterprise": [
      "Which teams sign off each milestone and what governance gates block release?",
      "What data retention, audit logging, and role-based access rules are mandatory?"
    ]
  }
}


if __name__ == "__main__":
    raise SystemExit(execute_configured_script(CONFIG))
