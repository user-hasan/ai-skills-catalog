#!/usr/bin/env python3
"""Detect dependency drift, risky versions, and lockfile gaps."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

LIB = Path(__file__).resolve().parents[2] / "_skill-governance" / "python_lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from project_intel import (  # noqa: E402
    append_operation,
    detect_manifests,
    ensure_project_intel,
    load_json,
    parse_dependency_files,
    replace_items_for_source,
    risk,
    semantic_major,
    semantic_minor,
    write_json,
)
from skill_governance import utc_now  # noqa: E402


SOURCE_SKILL = "dependency-governor"


def load_request(args) -> dict:
    if args.input:
        payload = load_json(Path(args.input), {})
        if isinstance(payload, dict):
            return payload
    return {}


def has_python_lock(repo_root: Path) -> bool:
    return any((repo_root / name).exists() for name in ("poetry.lock", "uv.lock", "Pipfile.lock", "requirements.lock"))


def has_node_lock(repo_root: Path) -> bool:
    return any((repo_root / name).exists() for name in ("package-lock.json", "pnpm-lock.yaml", "yarn.lock"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect dependency manifests and flag local dependency risks.")
    parser.add_argument("--input", help="JSON input with repo_path and optional baselines")
    parser.add_argument("--output", default="dependency_governor_output.json", help="Summary JSON output")
    args = parser.parse_args()

    request = load_request(args)
    repo_path = str(request.get("repo_path", "")).strip()
    if not repo_path:
        raise SystemExit("repo_path is required.")

    repo_root = Path(repo_path).resolve()
    paths = ensure_project_intel(repo_root)
    dependencies = parse_dependency_files(repo_root)
    manifests = detect_manifests(repo_root)
    baselines = {str(key).lower(): value for key, value in dict(request.get("baselines", {})).items()}
    abandoned = {str(item).lower() for item in request.get("abandoned_packages", [])}

    risks = []
    counter = 0

    if "package.json" in manifests and not has_node_lock(repo_root):
        counter += 1
        risks.append(
            risk(
                f"lockfilegap-{counter:03d}",
                "Node dependency manifest has no lockfile",
                "dependency",
                "medium",
                0.95,
                SOURCE_SKILL,
                ["package.json"],
                "Commit a lockfile so dependency resolution is reproducible across machines and CI.",
                "near-term",
                ["package.json present", "lockfile missing"],
            )
        )
    if "requirements.txt" in manifests and not has_python_lock(repo_root):
        counter += 1
        risks.append(
            risk(
                f"pythonlockgap-{counter:03d}",
                "Python dependency manifest has no lock artifact",
                "dependency",
                "medium",
                0.86,
                SOURCE_SKILL,
                ["requirements.txt"],
                "Add a lock or compile step so Python dependency resolution stays reproducible.",
                "near-term",
                ["requirements.txt present", "lock artifact missing"],
            )
        )

    for item in dependencies:
        name = item["name"].lower()
        version = item.get("version", "")
        file_name = item["file"]
        if not version or version.startswith(("^", "~", ">", "<")):
            counter += 1
            risks.append(
                risk(
                    f"unpinneddep-{counter:03d}",
                    f"Dependency is not tightly pinned: {item['name']}",
                    "dependency",
                    "medium",
                    0.78,
                    SOURCE_SKILL,
                    [file_name],
                    "Pin the dependency or document why a floating range is acceptable for this repository.",
                    "near-term",
                    [f"version specifier={version or 'missing'}"],
                )
            )
        if name in abandoned:
            counter += 1
            risks.append(
                risk(
                    f"abandoneddep-{counter:03d}",
                    f"Package is marked abandoned in the local baseline: {item['name']}",
                    "dependency",
                    "high",
                    0.9,
                    SOURCE_SKILL,
                    [file_name],
                    "Replace the package or justify why it remains on the dependency graph.",
                    "near-term",
                    ["baseline flagged package as abandoned"],
                )
            )

        baseline = baselines.get(name)
        if not baseline:
            continue
        min_major = baseline.get("min_major")
        min_minor = baseline.get("min_minor")
        current_major = semantic_major(version)
        current_minor = semantic_minor(version)
        if min_major is not None and current_major is not None and current_major < int(min_major):
            counter += 1
            risks.append(
                risk(
                    f"outdatedmajor-{counter:03d}",
                    f"Dependency is below the expected major baseline: {item['name']} {version}",
                    "dependency",
                    "high",
                    0.89,
                    SOURCE_SKILL,
                    [file_name],
                    "Plan a controlled upgrade to reach the supported major-version floor.",
                    "near-term",
                    [f"expected major>={min_major}", f"current major={current_major}"],
                )
            )
        elif min_minor is not None and current_minor is not None and current_minor < int(min_minor):
            counter += 1
            risks.append(
                risk(
                    f"outdatedminor-{counter:03d}",
                    f"Dependency is below the expected minor baseline: {item['name']} {version}",
                    "dependency",
                    "medium",
                    0.76,
                    SOURCE_SKILL,
                    [file_name],
                    "Review the upgrade path and verify whether the package should move to a newer maintained baseline.",
                    "near-term",
                    [f"expected minor>={min_minor}", f"current minor={current_minor}"],
                )
            )

    replace_items_for_source(paths.risk_register, "risk-register", "risks", SOURCE_SKILL, risks)
    append_operation(paths, SOURCE_SKILL, "audit-dependencies", repo_root.name, "completed", {"risk_count": len(risks)})

    output = {
        "artifact_type": "dependency-governor-output",
        "generated_at": utc_now(),
        "repo_root": str(repo_root),
        "dependency_count": len(dependencies),
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
