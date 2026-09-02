#!/usr/bin/env python3
"""Build normalized payloads for Linear, GitHub, and Notion from delivery artifacts."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

LIB = Path(__file__).resolve().parents[2] / "sdlc-system" / "python_lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from sdlc_common import list_from_payload, load_artifact, write_artifact  # noqa: E402


def normalize_items(primary, secondary):
    items = list_from_payload(primary, ["tasks", "items", "stories", "features"])
    if not items:
        items = list_from_payload(secondary, ["tasks", "items", "stories", "features"])
    normalized = []
    for index, item in enumerate(items, start=1):
        if isinstance(item, dict):
            normalized.append(
                {
                    "external_key": item.get("id") or item.get("story_id") or f"TASK-{index:03d}",
                    "title": item.get("title") or item.get("name") or item.get("story") or f"Task {index}",
                    "status": item.get("status", "todo"),
                    "owner": item.get("owner") or item.get("assignee") or "unassigned",
                    "priority": item.get("priority", "medium"),
                }
            )
        else:
            normalized.append(
                {
                    "external_key": f"TASK-{index:03d}",
                    "title": str(item),
                    "status": "todo",
                    "owner": "unassigned",
                    "priority": "medium",
                }
            )
    return normalized


def main():
    parser = argparse.ArgumentParser(description="Build tracker sync payloads from delivery artifacts.")
    parser.add_argument("--input", required=True, help="Primary delivery artifact path")
    parser.add_argument("--secondary-input", help="Optional sprint or backlog artifact path")
    parser.add_argument("--output", default="tracker_sync_payload.json", help="Output artifact path")
    args = parser.parse_args()

    primary = load_artifact(args.input)
    secondary = load_artifact(args.secondary_input) if args.secondary_input else {}
    items = normalize_items(primary, secondary)
    project_name = primary.get("project_name") if isinstance(primary, dict) else None
    project_name = project_name or (secondary.get("project_name") if isinstance(secondary, dict) else None) or "delivery-sync"

    report = {
        "artifact_type": "delivery-sync-payload",
        "project_name": project_name,
        "normalized_items": items,
        "linear": {
            "project_update": {
                "title": f"{project_name} delivery sync",
                "summary": f"Sync {len(items)} delivery items into Linear.",
            },
            "issues": items,
        },
        "github": {
            "project_note": f"{project_name}: sync {len(items)} items into the active project board.",
            "issues": items,
        },
        "notion": {
            "database_name": f"{project_name} Delivery Board",
            "pages": items,
        },
    }

    path = write_artifact(report, args.output, "json")
    print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
