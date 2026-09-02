#!/usr/bin/env python3
"""Detect performance hotspots from repository evidence and timed commands."""

from __future__ import annotations

import argparse
import re
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
    load_json,
    replace_items_for_source,
    risk,
    run_command,
    safe_read_text,
    write_json,
)
from skill_governance import utc_now  # noqa: E402


SOURCE_SKILL = "performance-auditor"


def load_request(args) -> dict:
    if args.input:
        payload = load_json(Path(args.input), {})
        if isinstance(payload, dict):
            return payload
    return {}


def line_count(path: Path) -> int:
    return len(safe_read_text(path).splitlines())


def main() -> int:
    parser = argparse.ArgumentParser(description="Detect slow-test patterns and likely performance hotspots.")
    parser.add_argument("--input", help="JSON input with repo_path and optional commands")
    parser.add_argument("--output", default="performance_auditor_output.json", help="Summary JSON output")
    args = parser.parse_args()

    request = load_request(args)
    repo_path = str(request.get("repo_path", "")).strip()
    if not repo_path:
        raise SystemExit("repo_path is required.")

    repo_root = Path(repo_path).resolve()
    paths = ensure_project_intel(repo_root)
    files = collect_repo_files(repo_root)
    graph = build_local_dependency_graph(repo_root)
    stats = fan_in_out(graph)
    risks = []
    counter = 0
    large_threshold = int(request.get("large_file_line_threshold", 400))

    for rel in files:
        full_path = repo_root / rel
        if rel.suffix.lower() not in {".py", ".js", ".jsx", ".ts", ".tsx"}:
            continue
        text = safe_read_text(full_path)
        rel_text = rel.as_posix()
        if ("test" in rel.name.lower() or "tests" in rel.parts) and re.search(r"\b(time\.sleep|sleep\()", text):
            counter += 1
            risks.append(
                risk(
                    f"slowtest-{counter:03d}",
                    f"Slow-test pattern detected in {rel_text}",
                    "performance",
                    "medium",
                    0.92,
                    SOURCE_SKILL,
                    [rel_text],
                    "Replace deliberate sleeps with condition-based waiting or narrower targeted assertions.",
                    "near-term",
                    ["sleep call inside a test file"],
                )
            )
        if re.search(r"for .*:\n(?:[ \t]+.*\n){0,6}[ \t]+with open\(", text):
            counter += 1
            risks.append(
                risk(
                    f"loopio-{counter:03d}",
                    f"Loop-scoped file I/O detected in {rel_text}",
                    "performance",
                    "medium",
                    0.84,
                    SOURCE_SKILL,
                    [rel_text],
                    "Move the I/O out of the loop or batch the reads to reduce repeated filesystem work.",
                    "near-term",
                    ["file I/O appears inside a loop"],
                )
            )
        if re.search(r"for .*:\n(?:[ \t]+.*\n){0,4}[ \t]+for .*:", text):
            counter += 1
            risks.append(
                risk(
                    f"nestedloop-{counter:03d}",
                    f"Nested loop hotspot detected in {rel_text}",
                    "performance",
                    "medium",
                    0.78,
                    SOURCE_SKILL,
                    [rel_text],
                    "Review whether the nested loop sits on a hot path and can be simplified or indexed.",
                    "near-term",
                    ["nested loop pattern"],
                )
            )
        if line_count(full_path) >= large_threshold and stats.get(rel_text, {}).get("fan_in", 0) >= 1:
            counter += 1
            risks.append(
                risk(
                    f"largehotspot-{counter:03d}",
                    f"Oversized hotspot file detected in {rel_text}",
                    "performance",
                    "low",
                    0.66,
                    SOURCE_SKILL,
                    [rel_text],
                    "Split the hotspot file so the high-traffic logic is easier to profile and optimize.",
                    "medium-term",
                    [f"lines>={large_threshold}", f"fan-in={stats.get(rel_text, {}).get('fan_in', 0)}"],
                )
            )

    slow_threshold = float(request.get("slow_command_threshold_seconds", 2.0))
    for command in request.get("commands", []):
        result = run_command([str(part) for part in command], repo_root)
        if float(result["duration_seconds"]) >= slow_threshold:
            counter += 1
            risks.append(
                risk(
                    f"slowcommand-{counter:03d}",
                    f"Command exceeded the slow-command threshold: {' '.join(result['command'])}",
                    "performance",
                    "medium",
                    0.95,
                    SOURCE_SKILL,
                    [],
                    "Profile or narrow the command scope before treating it as part of the fast inner loop.",
                    "near-term",
                    [f"duration={result['duration_seconds']}s", f"threshold={slow_threshold}s"],
                    extra={"command": result["command"]},
                )
            )

    replace_items_for_source(paths.risk_register, "risk-register", "risks", SOURCE_SKILL, risks)
    append_operation(paths, SOURCE_SKILL, "audit-performance", repo_root.name, "completed", {"risk_count": len(risks)})

    output = {
        "artifact_type": "performance-auditor-output",
        "generated_at": utc_now(),
        "repo_root": str(repo_root),
        "risk_count": len(risks),
        "artifacts": {
            "risk_register": str(paths.risk_register),
        },
    }
    write_json(Path(args.output), output)
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
