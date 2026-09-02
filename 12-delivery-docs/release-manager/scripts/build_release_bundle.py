#!/usr/bin/env python3
"""Build a release bundle with semver guidance and rollback actions."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

LIB = Path(__file__).resolve().parents[2] / "sdlc-system" / "python_lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from sdlc_common import flatten_text, list_from_payload, load_artifact, write_artifact  # noqa: E402


def classify_changes(payload):
    items = list_from_payload(payload, ["changes", "items", "pull_requests", "issues"])
    grouped = {"breaking": [], "features": [], "fixes": [], "docs": [], "ops": []}
    for item in items:
        title = item.get("title") if isinstance(item, dict) else str(item)
        text = f"{title} {flatten_text(item).lower() if isinstance(item, dict) else str(item).lower()}"
        if "breaking" in text or "migration" in text:
            grouped["breaking"].append(title)
        elif any(token in text for token in ("feature", "enhancement", "add", "support")):
            grouped["features"].append(title)
        elif any(token in text for token in ("fix", "bug", "regression", "crash")):
            grouped["fixes"].append(title)
        elif any(token in text for token in ("docs", "readme", "guide", "runbook")):
            grouped["docs"].append(title)
        else:
            grouped["ops"].append(title)
    return grouped


def choose_semver(grouped):
    if grouped["breaking"]:
        return "major"
    if grouped["features"]:
        return "minor"
    return "patch"


def main():
    parser = argparse.ArgumentParser(description="Build a release bundle from change items.")
    parser.add_argument("--input", required=True, help="Path to the release scope artifact")
    parser.add_argument("--output", default="release_bundle.json", help="Output artifact path")
    args = parser.parse_args()

    payload = load_artifact(args.input)
    grouped = classify_changes(payload)
    suggestion = choose_semver(grouped)

    report = {
        "artifact_type": "release-bundle",
        "suggested_version_bump": suggestion,
        "release_notes": grouped,
        "rollback_checklist": [
            "Confirm the previous stable version tag.",
            "Verify database or migration rollback steps.",
            "Confirm on-call and release owner availability.",
            "Prepare a post-release smoke-test checklist.",
        ],
    }

    path = write_artifact(report, args.output, "json")
    print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
