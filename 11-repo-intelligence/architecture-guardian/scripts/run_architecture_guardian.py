#!/usr/bin/env python3
"""Detect architecture risks from a repository dependency graph."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

LIB = Path(__file__).resolve().parents[2] / "_skill-governance" / "python_lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from project_intel import (  # noqa: E402
    append_operation,
    build_local_dependency_graph,
    collect_repo_files,
    ensure_project_intel,
    fan_in_out,
    find_cycles,
    load_json,
    replace_items_for_source,
    risk,
    safe_read_text,
    write_json,
)
from skill_governance import utc_now  # noqa: E402


SOURCE_SKILL = "architecture-guardian"


def load_request(args) -> dict:
    if args.input:
        payload = load_json(Path(args.input), {})
        if isinstance(payload, dict):
            return payload
    return {}


def line_count(path: Path) -> int:
    return len(safe_read_text(path).splitlines())


def main() -> int:
    parser = argparse.ArgumentParser(description="Detect cycles, boundary leaks, and oversized hubs.")
    parser.add_argument("--input", help="JSON input with repo_path and optional layer rules")
    parser.add_argument("--output", default="architecture_guardian_output.json", help="Summary JSON output")
    args = parser.parse_args()

    request = load_request(args)
    repo_path = str(request.get("repo_path", "")).strip()
    if not repo_path:
        raise SystemExit("repo_path is required.")

    repo_root = Path(repo_path).resolve()
    paths = ensure_project_intel(repo_root)
    graph = build_local_dependency_graph(repo_root)
    stats = fan_in_out(graph)
    cycles = find_cycles(graph)

    risks = []
    counter = 0
    for cycle in cycles:
        counter += 1
        risks.append(
            risk(
                f"archcycle-{counter:03d}",
                "Dependency cycle detected",
                "architecture",
                "high",
                0.96,
                SOURCE_SKILL,
                cycle,
                "Break the cycle by moving shared logic behind a boundary or extracting a lower-level abstraction.",
                "current",
                ["cyclic dependency graph edge"],
                extra={"cycle": cycle},
            )
        )

    rules = request.get("layer_rules", [])
    for rule in rules:
        source_prefix = str(rule.get("source_prefix", "")).strip().replace("\\", "/")
        forbidden_prefixes = [str(item).replace("\\", "/") for item in rule.get("forbidden_prefixes", [])]
        for source, targets in graph.items():
            if not source.startswith(source_prefix):
                continue
            for target in targets:
                for forbidden in forbidden_prefixes:
                    if target.startswith(forbidden):
                        counter += 1
                        risks.append(
                            risk(
                                f"boundaryleak-{counter:03d}",
                                f"Layer violation from {source_prefix} to {forbidden}",
                                "architecture",
                                "high",
                                0.91,
                                SOURCE_SKILL,
                                [source, target],
                                str(rule.get("reason", "Route the dependency through an allowed boundary.")),
                                "current",
                                [f"{source} depends on {target}"],
                            )
                        )

    large_threshold = int(request.get("large_file_line_threshold", 400))
    hub_threshold = int(request.get("hub_fan_in_threshold", 6))
    for rel, item in stats.items():
        if item["fan_in"] < hub_threshold:
            continue
        file_lines = line_count(repo_root / rel)
        if file_lines < large_threshold:
            continue
        counter += 1
        risks.append(
            risk(
                f"hubpressure-{counter:03d}",
                f"Oversized central hub: {rel}",
                "architecture",
                "medium",
                0.8,
                SOURCE_SKILL,
                [rel],
                "Split orchestration from low-level responsibilities to reduce centrality and review risk.",
                "near-term",
                [f"fan-in={item['fan_in']}", f"fan-out={item['fan_out']}", f"lines={file_lines}"],
            )
        )

    replace_items_for_source(paths.risk_register, "risk-register", "risks", SOURCE_SKILL, risks)
    append_operation(paths, SOURCE_SKILL, "analyze-architecture", repo_root.name, "completed", {"risk_count": len(risks)})

    output = {
        "artifact_type": "architecture-guardian-output",
        "generated_at": utc_now(),
        "repo_root": str(repo_root),
        "risk_count": len(risks),
        "cycles_detected": len(cycles),
        "artifacts": {
            "risk_register": str(paths.risk_register),
        },
    }
    write_json(Path(args.output), output)
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
