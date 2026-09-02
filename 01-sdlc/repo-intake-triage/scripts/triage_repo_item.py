#!/usr/bin/env python3
"""Classify a GitHub issue or PR intake item and suggest routing metadata."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

LIB = Path(__file__).resolve().parents[2] / "sdlc-system" / "python_lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from sdlc_common import flatten_text, keyword_set, load_artifact, write_artifact  # noqa: E402


CATEGORY_RULES = [
    ("security", {"security", "vulnerability", "cve", "xss", "auth", "token"}),
    ("bug", {"bug", "error", "exception", "crash", "regression", "broken"}),
    ("docs", {"docs", "documentation", "readme", "guide", "typo"}),
    ("release", {"release", "version", "deploy", "changelog", "rollback"}),
    ("feature", {"feature", "enhancement", "improve", "add", "support"}),
]

READINESS_FIELDS = {
    "bug": ["title", "actual_behavior", "expected_behavior", "steps_to_reproduce"],
    "feature": ["title", "user_value", "requested_outcome"],
    "security": ["title", "impact", "affected_surface", "mitigation_expectation"],
    "docs": ["title", "audience", "doc_target"],
    "release": ["title", "target_version", "rollback_owner"],
}

LABELS = {
    "security": ["type:security", "priority:high"],
    "bug": ["type:bug"],
    "docs": ["type:docs"],
    "release": ["type:release"],
    "feature": ["type:feature"],
}

OWNERS = {
    "security": "security-owner",
    "bug": "engineering-owner",
    "docs": "docs-owner",
    "release": "release-owner",
    "feature": "product-owner",
}


def choose_category(words):
    for name, triggers in CATEGORY_RULES:
        if words.intersection(triggers):
            return name
    return "feature"


def find_missing_fields(payload, required_fields):
    if not isinstance(payload, dict):
        return required_fields
    missing = []
    for field in required_fields:
        value = payload.get(field)
        if value in (None, "", [], {}):
            missing.append(field)
    return missing


def main():
    parser = argparse.ArgumentParser(description="Triage a GitHub issue or PR intake item.")
    parser.add_argument("--input", required=True, help="Path to the issue/PR export JSON or markdown file")
    parser.add_argument("--output", default="triage_report.json", help="Output artifact path")
    args = parser.parse_args()

    payload = load_artifact(args.input)
    words = keyword_set(payload)
    text = flatten_text(payload).lower()
    category = choose_category(words)
    required_fields = READINESS_FIELDS.get(category, ["title"])
    missing = find_missing_fields(payload, required_fields)

    severity = "medium"
    if category == "security" or "production" in text or "outage" in text:
        severity = "high"
    elif category == "docs":
        severity = "low"

    report = {
        "artifact_type": "repo-intake-triage",
        "category": category,
        "severity": severity,
        "ready_for_execution": not missing,
        "missing_context": missing,
        "suggested_labels": LABELS.get(category, []) + ([f"severity:{severity}"] if severity != "low" else []),
        "routing": {
            "owner_group": OWNERS.get(category, "engineering-owner"),
            "next_skill": "delivery-sync" if category in {"feature", "release"} else "sdlc-pm-project",
        },
        "follow_up_questions": [
            f"Provide {field.replace('_', ' ')}." for field in missing
        ],
    }

    path = write_artifact(report, args.output, "json")
    print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
