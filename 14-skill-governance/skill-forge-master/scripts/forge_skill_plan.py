#!/usr/bin/env python3
"""Produce a skill design spec, quality report, patch plan, and update request."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

LIB = Path(__file__).resolve().parents[2] / "_skill-governance" / "python_lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from skill_governance import (  # noqa: E402
    GOVERNANCE_ROOT,
    SKILLS_ROOT,
    find_skill_dir,
    infer_category_from_skill,
    load_json,
    log_operation,
    patch_plan,
    quality_report,
    utc_now,
    write_json,
    write_registry_entry,
)


def load_request(args) -> dict:
    payload = {}
    if args.input:
        data = load_json(Path(args.input), {})
        if isinstance(data, dict):
            payload.update(data)
    if args.skill:
        payload["skill_name"] = args.skill
    if args.mode:
        payload["mode"] = args.mode
    if args.intent:
        payload["intent"] = args.intent
    return payload


def output_paths(base_output: Path) -> dict:
    base_output.parent.mkdir(parents=True, exist_ok=True)
    output_dir = base_output.parent
    return {
        "request": base_output,
        "design": output_dir / "skill_design_spec.md",
        "quality": output_dir / "skill_quality_report.json",
        "patch": output_dir / "skill_patch_plan.md",
    }


def render_design_spec(request: dict, existing: bool, skill_dir: Path | None, report: dict) -> str:
    skill_name = request["skill_name"]
    mode = request.get("mode", "improve" if existing else "create")
    intent = request.get("intent", "create or improve a Codex skill")
    category = request.get("category") or infer_category_from_skill(skill_name)
    purpose = request.get("purpose", "Provide a high-signal workflow for the target task.")
    constraints = request.get("constraints", [])
    outputs = request.get("required_outputs", [])

    lines = [
        f"# Skill Design Spec: {skill_name}",
        "",
        f"- Generated at: `{utc_now()}`",
        f"- Mode: `{mode}`",
        f"- Existing skill: `{existing}`",
        f"- Category: `{category}`",
        "",
        "## Intent",
        "",
        f"- {intent}",
        f"- {purpose}",
        "",
        "## Trigger Contract",
        "",
        f"- The skill must trigger when the user explicitly names `{skill_name}` or when the task clearly matches its narrow domain.",
        "- The frontmatter description must include both what the skill does and when it should be used.",
        "- `agents/openai.yaml` must include an explicit `$skill-name` default prompt.",
        "",
        "## Required Structure",
        "",
        "- `SKILL.md` with concise overview, workflow, references, and failure modes",
        "- `agents/openai.yaml` with `policy.allow_implicit_invocation: true` unless the skill must stay explicit-only",
        "- `scripts/` for deterministic transforms",
        "- `references/` for progressive disclosure",
        "- `assets/inputs` and `assets/outputs` for smoke validation when scripts exist",
        "",
        "## Quality Signals",
        "",
        f"- Current quality grade: `{report.get('quality_grade', 'new')}`",
        f"- Current total score: `{report.get('total_score', 0)}`",
        "",
        "## Constraints",
        "",
    ]
    if constraints:
        lines.extend(f"- {item}" for item in constraints)
    else:
        lines.extend(
            [
                "- Keep changes scoped to the target skill directory.",
                "- Avoid introducing unrelated dependencies.",
                "- Prefer the smallest repair that resolves the observed weakness.",
            ]
        )
    lines.extend(["", "## Expected Outputs", ""])
    if outputs:
        lines.extend(f"- `{item}`" for item in outputs)
    else:
        lines.extend(
            [
                "- `skill_design_spec.md`",
                "- `skill_quality_report.json`",
                "- `skill_patch_plan.md`",
                "- `skill_update_request.json`",
            ]
        )
    if existing and skill_dir:
        lines.extend(["", "## Current Skill Path", "", f"- `{skill_dir}`"])
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Forge a design and improvement plan for a Codex skill.")
    parser.add_argument("--input", help="Optional JSON request")
    parser.add_argument("--skill", help="Skill name override")
    parser.add_argument("--mode", choices=["create", "improve"], help="Mode override")
    parser.add_argument("--intent", help="Intent override")
    parser.add_argument("--output", default="skill_update_request.json", help="Primary JSON output path")
    args = parser.parse_args()

    request = load_request(args)
    skill_name = str(request.get("skill_name", "")).strip()
    if not skill_name:
        raise SystemExit("A skill_name is required.")

    skill_dir = find_skill_dir(skill_name, SKILLS_ROOT)
    existing = skill_dir is not None
    if "mode" not in request:
        request["mode"] = "improve" if existing else "create"

    quality = quality_report(skill_dir) if existing and skill_dir else {
        "artifact_type": "skill-quality-report",
        "generated_at": utc_now(),
        "skill": skill_name,
        "quality_grade": "new",
        "total_score": 0,
        "issues": [{"code": "skill_missing", "message": "Skill does not exist yet."}],
    }
    patch = patch_plan(skill_dir, quality, str(request.get("intent", "create or improve the skill"))) if existing and skill_dir else {
        "artifact_type": "skill-patch-plan",
        "generated_at": utc_now(),
        "skill": skill_name,
        "intent": request.get("intent", "create a new skill"),
        "scoped_files": [
            str(SKILLS_ROOT / skill_name / "SKILL.md"),
            str(SKILLS_ROOT / skill_name / "agents" / "openai.yaml"),
            str(SKILLS_ROOT / skill_name / "scripts"),
            str(SKILLS_ROOT / skill_name / "references"),
            str(SKILLS_ROOT / skill_name / "assets"),
        ],
        "actions": [
            "Create the new skill directory and core files.",
            "Write SKILL.md with precise triggers and workflow steps.",
            "Add deterministic scripts, references, and smoke artifacts as needed.",
        ],
        "non_goals": [
            "Do not edit unrelated skills.",
            "Do not change global governance policy while creating a normal skill.",
        ],
    }
    update_request = {
        "artifact_type": "skill-update-request",
        "generated_at": utc_now(),
        "request_id": f"{skill_name}-{utc_now().replace(':', '').replace('-', '')}",
        "target_skill": skill_name,
        "category": request.get("category") or infer_category_from_skill(skill_name),
        "origin": "skill-forge-master",
        "intent": request.get("intent", "create or improve a Codex skill"),
        "mode": request["mode"],
        "proposed_scope": {
            "files": patch["scoped_files"],
            "shared_dependency_declared": False,
        },
        "quality_summary": {
            "quality_grade": quality.get("quality_grade", "new"),
            "total_score": quality.get("total_score", 0),
            "issue_codes": [item["code"] for item in quality.get("issues", [])],
        },
        "constraints": request.get("constraints", []),
    }

    paths = output_paths(Path(args.output))
    paths["design"].write_text(render_design_spec(request, existing, skill_dir, quality), encoding="utf-8")
    write_json(paths["quality"], quality)
    paths["patch"].write_text(json.dumps(patch, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_json(paths["request"], update_request)

    write_registry_entry(
        skill_name,
        {
            "last_forge_run": update_request["generated_at"],
            "last_forge_mode": request["mode"],
            "quality_grade": quality.get("quality_grade", "new"),
            "governance_root": str(GOVERNANCE_ROOT),
        },
    )
    log_operation("skill-forge-master", "forge-skill-plan", skill_name, "completed", {"output": str(paths["request"])})
    print(paths["request"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
