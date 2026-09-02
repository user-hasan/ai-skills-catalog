#!/usr/bin/env python3
"""Compute blast radius and verification requirements for a proposed repair."""

from __future__ import annotations

import argparse
from collections import deque
import sys
from pathlib import Path

LIB = Path(__file__).resolve().parents[2] / "_skill-governance" / "python_lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from project_intel import (  # noqa: E402
    append_operation,
    build_local_dependency_graph,
    ensure_project_intel,
    load_json,
    matching_tests,
    reverse_graph,
    write_json,
)
from skill_governance import utc_now  # noqa: E402


SOURCE_SKILL = "regression-guard"


def load_request(args) -> dict:
    if args.input:
        payload = load_json(Path(args.input), {})
        if isinstance(payload, dict):
            return payload
    return {}


def expand_impacted_files(target_files: list[str], reversed_graph: dict[str, list[str]], max_depth: int = 4) -> list[str]:
    queue = deque((item, 0) for item in target_files)
    seen = set(target_files)
    while queue:
        current, depth = queue.popleft()
        if depth >= max_depth:
            continue
        for dependent in reversed_graph.get(current, []):
            if dependent not in seen:
                seen.add(dependent)
                queue.append((dependent, depth + 1))
    return sorted(seen)


def main() -> int:
    parser = argparse.ArgumentParser(description="Calculate blast radius and verification requirements.")
    parser.add_argument("--input", help="JSON input with repo_path, target_files, and findings")
    parser.add_argument("--output", default="regression_guard_output.json", help="Summary JSON output")
    args = parser.parse_args()

    request = load_request(args)
    repo_path = str(request.get("repo_path", "")).strip()
    if not repo_path:
        raise SystemExit("repo_path is required.")

    target_files = [str(item).replace("\\", "/") for item in request.get("target_files", [])]
    if not target_files:
        raise SystemExit("target_files must include at least one repository-relative file.")

    repo_root = Path(repo_path).resolve()
    paths = ensure_project_intel(repo_root)
    graph = build_local_dependency_graph(repo_root)
    reversed_graph = reverse_graph(graph)
    impacted_files = expand_impacted_files(target_files, reversed_graph, int(request.get("max_depth", 4)))
    impacted_tests = matching_tests(repo_root, impacted_files)
    findings = list(request.get("findings", []))

    required_checks = [
        f"Run targeted verification for: {', '.join(impacted_files)}",
    ]
    if impacted_tests:
        required_checks.append(f"Run impacted tests: {', '.join(impacted_tests)}")
    if any(item.get("type") == "commands" for item in findings):
        required_checks.append("Re-run the previously failing command after the repair.")
    if any(item.get("type") == "imports" for item in findings):
        required_checks.append("Compile or import-check the affected Python entrypoints after the repair.")

    verification = {
        "artifact_type": "verification-requirements",
        "generated_at": utc_now(),
        "repo_root": str(repo_root),
        "target_files": target_files,
        "impacted_files": impacted_files,
        "impacted_tests": impacted_tests,
        "required_checks": required_checks,
        "source_skill": SOURCE_SKILL,
    }
    requirements_path = paths.verification_dir / "verification_requirements.json"
    write_json(requirements_path, verification)
    append_operation(paths, SOURCE_SKILL, "map-blast-radius", repo_root.name, "completed", {"impacted_files": len(impacted_files), "impacted_tests": len(impacted_tests)})

    output = {
        "artifact_type": "regression-guard-output",
        "generated_at": utc_now(),
        "repo_root": str(repo_root),
        "artifacts": {
            "verification_requirements": str(requirements_path),
        },
        "impacted_files": impacted_files,
        "impacted_tests": impacted_tests,
    }
    write_json(Path(args.output), output)
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
