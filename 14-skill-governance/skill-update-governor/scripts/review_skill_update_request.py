#!/usr/bin/env python3
"""Review a skill update request and emit governance decisions."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

LIB = Path(__file__).resolve().parents[2] / "_skill-governance" / "python_lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from skill_governance import (  # noqa: E402
    REGISTRY_PATH,
    SKILLS_ROOT,
    UPDATE_REQUESTS_DIR,
    find_skill_dir,
    impact_report,
    is_url_allowed,
    load_json,
    load_source_policies,
    log_operation,
    utc_now,
    write_json,
)


def load_request(args) -> dict:
    if args.input:
        payload = load_json(Path(args.input), {})
        if isinstance(payload, dict):
            return payload
    raise SystemExit("A JSON request is required.")


def decision_for_request(request: dict, impact: dict, policies: dict) -> tuple[str, list[str], dict]:
    skill_name = request["target_skill"]
    skill_dir = find_skill_dir(skill_name, SKILLS_ROOT)
    if not skill_dir:
        return "rejected", [f"Target skill does not exist: {skill_name}"], {}

    allowed_prefix = skill_dir.resolve()
    proposed_files = [Path(item) for item in request.get("proposed_scope", {}).get("files", [])]
    disallowed_files = []
    for path in proposed_files:
        try:
            path.resolve().relative_to(allowed_prefix)
            continue
        except ValueError:
            pass
        try:
            path.resolve().relative_to(UPDATE_REQUESTS_DIR.resolve())
            continue
        except ValueError:
            disallowed_files.append(str(path))

    disallowed_urls = []
    for url in request.get("source_urls", []):
        if not is_url_allowed(url, request.get("category", ""), policies):
            disallowed_urls.append(url)

    reasons = []
    if disallowed_files:
        reasons.append("The proposed scope includes files outside the target skill directory.")
    if disallowed_files:
        return "rejected", reasons, {"disallowed_files": disallowed_files, "disallowed_urls": disallowed_urls}

    source_policy_status = str(request.get("source_policy_status", "")).strip().lower()
    if disallowed_urls:
        if source_policy_status == "requires-allowlist-expansion":
            return (
                "needs policy review",
                ["The request relies on trustworthy sources outside the current strict allowlist and requires a source-policy decision before implementation."],
                {"disallowed_urls": disallowed_urls, "source_policy_status": source_policy_status},
            )
        reasons.append("One or more source URLs violate the strict allowlist.")
        return "rejected", reasons, {"disallowed_files": disallowed_files, "disallowed_urls": disallowed_urls}

    signals = request.get("signal_summary", [])
    if not signals or all(signal == "noise / irrelevant" for signal in signals):
        return "deferred", ["The request does not contain actionable update signals."], {}

    if any(signal == "breaking change" for signal in signals):
        return "needs review", ["Breaking change signals require manual review before implementation."], {}

    if impact["summary"]["requires_governance_review"]:
        return "needs review", ["The target skill has direct or governance-level dependencies."], {}

    return "approved", ["The request is source-compliant, scoped, and low enough risk to proceed."], {}


def main() -> int:
    parser = argparse.ArgumentParser(description="Review a skill update request under strict governance rules.")
    parser.add_argument("--input", help="JSON update request")
    parser.add_argument("--output", default="approval_decision.json", help="Primary decision output path")
    args = parser.parse_args()

    request = load_request(args)
    skill_name = str(request.get("target_skill", "")).strip()
    if not skill_name:
        raise SystemExit("target_skill is required in the request.")

    policies = load_source_policies()
    impact = impact_report(skill_name, SKILLS_ROOT)
    decision, reasons, extras = decision_for_request(request, impact, policies)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    scope_path = output_path.parent / "change_scope_report.json"
    verification_path = output_path.parent / "verification_requirements.json"

    scope_report = {
        "artifact_type": "change-scope-report",
        "generated_at": utc_now(),
        "target_skill": skill_name,
        "proposed_scope": request.get("proposed_scope", {}),
        "source_policy_status": request.get("source_policy_status"),
        "impact_summary": impact["summary"],
        "direct_skill_references": impact["direct_skill_references"],
        "decision_inputs": extras,
    }
    approval = {
        "artifact_type": "approval-decision",
        "generated_at": utc_now(),
        "request_id": request.get("request_id"),
        "target_skill": skill_name,
        "decision": decision,
        "reasons": reasons,
    }
    verification = {
        "artifact_type": "verification-requirements",
        "generated_at": utc_now(),
        "target_skill": skill_name,
        "required_checks": [
            "Run skill-quality-auditor against the updated skill.",
            "Run validate_authored_skills.py after the scoped update.",
            "Confirm only scoped files changed before publishing.",
        ]
        + (["Inspect referenced downstream skills before publishing."] if impact["summary"]["requires_governance_review"] else [])
        + (
            [
                "Record an explicit source-policy decision before editing the target skill.",
                "Keep the target skill unchanged while the request remains in policy-review status.",
            ]
            if decision == "needs policy review"
            else []
        ),
    }

    write_json(scope_path, scope_report)
    write_json(output_path, approval)
    write_json(verification_path, verification)
    registry = load_json(REGISTRY_PATH, {"governance_version": "1.0.0", "skills": {}, "updated_at": utc_now()})
    skills = registry.setdefault("skills", {})
    existing_entry = skills.get(skill_name, {})
    if not isinstance(existing_entry, dict):
        existing_entry = {}
    existing_entry.update(
        {
            "last_governor_decision": decision,
            "last_governor_reviewed_at": approval["generated_at"],
            "last_governor_request_id": request.get("request_id"),
        }
    )
    skills[skill_name] = existing_entry
    registry["updated_at"] = approval["generated_at"]
    write_json(REGISTRY_PATH, registry)
    log_operation("skill-update-governor", "review-update-request", skill_name, "completed", {"decision": decision, "output": str(output_path)})
    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
