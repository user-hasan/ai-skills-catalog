#!/usr/bin/env python3
"""Analyze the likely impact of changing a skill."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

LIB = Path(__file__).resolve().parents[2] / "_skill-governance" / "python_lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from skill_governance import (  # noqa: E402
    SKILLS_ROOT,
    impact_report,
    load_json,
    log_operation,
    write_json,
    write_registry_entry,
)


def load_request(args) -> dict:
    if args.input:
        payload = load_json(Path(args.input), {})
        if isinstance(payload, dict):
            return payload
    payload = {}
    if args.skill:
        payload["skill"] = args.skill
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze downstream impact before changing a skill.")
    parser.add_argument("--input", help="Optional JSON input with skill")
    parser.add_argument("--skill", help="Skill name override")
    parser.add_argument("--output", default="skill_change_impact_report.json", help="Output JSON path")
    args = parser.parse_args()

    request = load_request(args)
    skill_name = str(request.get("skill", "")).strip()
    if not skill_name:
        raise SystemExit("A skill name is required.")

    report = impact_report(skill_name, SKILLS_ROOT)
    output_path = write_json(Path(args.output), report)
    write_registry_entry(
        skill_name,
        {
            "last_impact_review": report["generated_at"],
            "direct_reference_count": report["summary"]["direct_reference_count"],
            "requires_governance_review": report["summary"]["requires_governance_review"],
        },
    )
    log_operation("skill-change-impact-analyzer", "analyze-impact", skill_name, "completed", {"output": str(output_path)})
    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
