#!/usr/bin/env python3
"""Build a repair plan and optionally apply scoped declarative edits."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

LIB = Path(__file__).resolve().parents[2] / "_skill-governance" / "python_lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from project_intel import (  # noqa: E402
    append_operation,
    ensure_project_intel,
    load_json,
    write_json,
)
from skill_governance import utc_now  # noqa: E402


SOURCE_SKILL = "defect-fixer"


def load_request(args) -> dict:
    if args.input:
        payload = load_json(Path(args.input), {})
        if isinstance(payload, dict):
            return payload
    return {}


def path_within_repo(repo_root: Path, relative_path: str) -> Path:
    path = (repo_root / relative_path).resolve()
    path.relative_to(repo_root.resolve())
    return path


def build_repair_step(index: int, finding: dict) -> dict:
    return {
        "id": f"repair-{index:03d}",
        "finding_id": finding.get("id"),
        "title": finding.get("title"),
        "target_files": list(finding.get("affected_files", [])),
        "recommended_action": finding.get("recommended_action"),
        "status": "planned",
    }


def apply_edit_instruction(repo_root: Path, instruction: dict, allowed_files: set[str]) -> dict:
    operation = str(instruction.get("operation", "")).strip()
    relative_path = str(instruction.get("file", "")).replace("\\", "/").strip()
    if not relative_path:
        raise ValueError("Each edit instruction requires a file path.")
    if allowed_files and relative_path not in allowed_files:
        raise ValueError(f"Edit is outside the approved scope: {relative_path}")

    target_path = path_within_repo(repo_root, relative_path)
    if operation == "replace_text":
        old = str(instruction.get("old", ""))
        new = str(instruction.get("new", ""))
        text = target_path.read_text(encoding="utf-8")
        if old not in text:
            raise ValueError(f"replace_text could not find the expected text in {relative_path}")
        target_path.write_text(text.replace(old, new, 1), encoding="utf-8")
    elif operation == "append_text":
        target_path.parent.mkdir(parents=True, exist_ok=True)
        with target_path.open("a", encoding="utf-8") as handle:
            handle.write(str(instruction.get("text", "")))
    elif operation == "create_file":
        if target_path.exists() and bool(instruction.get("only_if_missing", False)):
            return {"operation": operation, "file": relative_path, "status": "skipped"}
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_text(str(instruction.get("content", "")), encoding="utf-8")
    else:
        raise ValueError(f"Unsupported operation: {operation}")
    return {"operation": operation, "file": relative_path, "status": "applied"}


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a repair plan and optionally apply scoped declarative edits.")
    parser.add_argument("--input", help="JSON input with repo_path, findings, and optional repair instructions")
    parser.add_argument("--output", default="defect_fixer_output.json", help="Summary JSON output")
    args = parser.parse_args()

    request = load_request(args)
    repo_path = str(request.get("repo_path", "")).strip()
    if not repo_path:
        raise SystemExit("repo_path is required.")

    findings = list(request.get("findings", []))
    if not findings:
        raise SystemExit("findings are required.")

    repo_root = Path(repo_path).resolve()
    paths = ensure_project_intel(repo_root)
    verification_requirements = dict(request.get("verification_requirements", {}))
    allowed_files = {str(item).replace("\\", "/") for item in verification_requirements.get("target_files", [])}
    allowed_files.update(str(item).replace("\\", "/") for item in verification_requirements.get("impacted_files", []))

    repair_steps = [build_repair_step(index, finding) for index, finding in enumerate(findings, 1)]
    repair_plan = {
        "artifact_type": "repair-plan",
        "generated_at": utc_now(),
        "repo_root": str(repo_root),
        "source_skill": SOURCE_SKILL,
        "repairs": repair_steps,
    }
    write_json(paths.repair_plan, repair_plan)

    applied_changes = []
    allow_edits = bool(request.get("allow_edits", False))
    if allow_edits:
        for instruction in request.get("repair_instructions", []):
            applied_changes.append(apply_edit_instruction(repo_root, dict(instruction), allowed_files))

    verification_report = {
        "artifact_type": "verification-report",
        "generated_at": utc_now(),
        "repo_root": str(repo_root),
        "source_skill": SOURCE_SKILL,
        "changes_applied": applied_changes,
        "required_checks": list(verification_requirements.get("required_checks", [])),
        "status": "changes-applied" if allow_edits and applied_changes else "plan-only",
    }
    write_json(paths.verification_report, verification_report)
    append_operation(paths, SOURCE_SKILL, "prepare-repair-plan", repo_root.name, "completed", {"repair_steps": len(repair_steps), "applied_changes": len(applied_changes)})

    output = {
        "artifact_type": "defect-fixer-output",
        "generated_at": utc_now(),
        "repo_root": str(repo_root),
        "artifacts": {
            "repair_plan": str(paths.repair_plan),
            "verification_report": str(paths.verification_report),
        },
        "repair_step_count": len(repair_steps),
        "applied_change_count": len(applied_changes),
    }
    write_json(Path(args.output), output)
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
