#!/usr/bin/env python3
"""Forecast future repository risks from graph and maintenance signals."""

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
    count_todo_markers,
    ensure_project_intel,
    fan_in_out,
    git_file_churn,
    load_json,
    matching_tests,
    replace_items_for_source,
    risk,
    write_json,
)
from skill_governance import utc_now  # noqa: E402


SOURCE_SKILL = "future-risk-forecast"


def load_request(args) -> dict:
    if args.input:
        payload = load_json(Path(args.input), {})
        if isinstance(payload, dict):
            return payload
    return {}


def main() -> int:
    parser = argparse.ArgumentParser(description="Forecast repository fragility and future risk.")
    parser.add_argument("--input", help="JSON input with repo_path and optional churn hints")
    parser.add_argument("--output", default="future_risk_forecast_output.json", help="Summary JSON output")
    args = parser.parse_args()

    request = load_request(args)
    repo_path = str(request.get("repo_path", "")).strip()
    if not repo_path:
        raise SystemExit("repo_path is required.")

    repo_root = Path(repo_path).resolve()
    paths = ensure_project_intel(repo_root)
    graph = build_local_dependency_graph(repo_root)
    stats = fan_in_out(graph)
    churn = git_file_churn(repo_root)
    churn.update({str(key).replace("\\", "/"): int(value) for key, value in dict(request.get("simulated_churn", {})).items()})
    todo_counts = count_todo_markers(repo_root)
    ownerless = {str(item).replace("\\", "/") for item in request.get("ownerless_paths", [])}
    fan_in_threshold = int(request.get("fan_in_threshold", 3))
    todo_threshold = int(request.get("todo_threshold", 3))

    risks = []
    counter = 0
    for file_name, item in stats.items():
        if item["fan_in"] < fan_in_threshold:
            continue
        tests = matching_tests(repo_root, [file_name])
        if not tests:
            counter += 1
            risks.append(
                risk(
                    f"undertestedcritical-{counter:03d}",
                    f"Critical path appears under-tested: {file_name}",
                    "future-risk",
                    "high",
                    0.82,
                    SOURCE_SKILL,
                    [file_name],
                    "Add targeted tests around this file before future repairs or feature work expand its responsibility.",
                    "near-term",
                    [f"fan-in={item['fan_in']}", "no matching tests found"],
                )
            )
        if churn.get(file_name, 0) >= 5:
            counter += 1
            risks.append(
                risk(
                    f"highchurnhub-{counter:03d}",
                    f"High-churn central file is likely to destabilize future work: {file_name}",
                    "future-risk",
                    "medium",
                    0.79,
                    SOURCE_SKILL,
                    [file_name],
                    "Reduce the file's centrality or protect it with stronger tests before future changes accumulate.",
                    "medium-term",
                    [f"fan-in={item['fan_in']}", f"churn={churn[file_name]}"],
                )
            )
        if file_name in ownerless:
            counter += 1
            risks.append(
                risk(
                    f"ownershipgap-{counter:03d}",
                    f"Critical path appears ownerless: {file_name}",
                    "future-risk",
                    "medium",
                    0.74,
                    SOURCE_SKILL,
                    [file_name],
                    "Assign an explicit owner or stewardship path before the file becomes a release bottleneck.",
                    "medium-term",
                    ["ownerless path declared in input"],
                )
            )

    for file_name, marker_count in todo_counts.items():
        if marker_count < todo_threshold:
            continue
        counter += 1
        risks.append(
            risk(
                f"tododensity-{counter:03d}",
                f"TODO or FIXME density suggests future fragility in {file_name}",
                "future-risk",
                "low",
                0.68,
                SOURCE_SKILL,
                [file_name],
                "Review whether deferred cleanup in this file is blocking safer future change velocity.",
                "medium-term",
                [f"markers={marker_count}"],
            )
        )

    replace_items_for_source(paths.risk_register, "risk-register", "risks", SOURCE_SKILL, risks)
    append_operation(paths, SOURCE_SKILL, "forecast-risks", repo_root.name, "completed", {"risk_count": len(risks)})

    output = {
        "artifact_type": "future-risk-forecast-output",
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
