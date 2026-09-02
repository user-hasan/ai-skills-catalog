#!/usr/bin/env python3
"""Extract backlog artifacts from meeting notes or transcript summaries."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

LIB = Path(__file__).resolve().parents[2] / "sdlc-system" / "python_lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from sdlc_common import flatten_text, load_artifact, write_artifact  # noqa: E402


def split_sentences(text):
    return [segment.strip(" -") for segment in re.split(r"[\n\.]+", text) if segment.strip()]


def main():
    parser = argparse.ArgumentParser(description="Convert meeting notes into backlog artifacts.")
    parser.add_argument("--input", required=True, help="Path to the meeting notes artifact")
    parser.add_argument("--output", default="meeting_backlog.json", help="Output artifact path")
    args = parser.parse_args()

    payload = load_artifact(args.input)
    sentences = split_sentences(flatten_text(payload))
    decisions = [line for line in sentences if any(token in line.lower() for token in ("decide", "decision", "approved"))]
    risks = [line for line in sentences if any(token in line.lower() for token in ("risk", "blocker", "dependency"))]
    actions = [line for line in sentences if any(token in line.lower() for token in ("need", "should", "must", "action"))]

    stories = []
    for index, action in enumerate(actions, start=1):
        stories.append(
            {
                "story_id": f"MTB-{index:03d}",
                "title": action,
                "status": "todo",
            }
        )

    report = {
        "artifact_type": "meeting-to-backlog",
        "decisions": decisions,
        "risks": risks,
        "stories": stories,
        "next_questions": [
            "Which owner is accountable for each open action?",
            "Which stories belong in the first sprint or release?",
        ],
    }

    path = write_artifact(report, args.output, "json")
    print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
