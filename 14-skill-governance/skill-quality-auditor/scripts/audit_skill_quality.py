#!/usr/bin/env python3
"""Audit a Codex skill and emit a scored quality report."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

LIB = Path(__file__).resolve().parents[2] / "_skill-governance" / "python_lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from skill_governance import (  # noqa: E402
    SKILLS_ROOT,
    find_skill_dir,
    load_json,
    log_operation,
    quality_report,
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
    parser = argparse.ArgumentParser(description="Audit a local Codex skill for quality.")
    parser.add_argument("--input", help="Optional JSON input with skill")
    parser.add_argument("--skill", help="Skill name override")
    parser.add_argument("--output", default="skill_quality_report.json", help="Output JSON path")
    args = parser.parse_args()

    request = load_request(args)
    skill_name = str(request.get("skill", "")).strip()
    if not skill_name:
        raise SystemExit("A skill name is required.")

    skill_dir = find_skill_dir(skill_name, SKILLS_ROOT)
    if not skill_dir:
        raise SystemExit(f"Skill not found: {skill_name}")

    report = quality_report(skill_dir)
    output_path = write_json(Path(args.output), report)
    write_registry_entry(
        skill_name,
        {
            "last_quality_audit": report["generated_at"],
            "quality_grade": report["quality_grade"],
            "total_score": report["total_score"],
        },
    )
    log_operation("skill-quality-auditor", "audit-skill", skill_name, "completed", {"output": str(output_path)})
    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
