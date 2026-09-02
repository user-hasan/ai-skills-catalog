#!/usr/bin/env python3
"""Compare authored skills with the published Codex skill registry."""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

def resolve_authoring_lib() -> Path:
    candidates = [
        Path(__file__).resolve().parents[2] / "sdlc-system" / "python_lib",
        Path.home() / ".agents" / "skills" / "sdlc-system" / "python_lib",
    ]
    for candidate in candidates:
        if (candidate / "authored_skill_tools.py").exists() and (candidate / "sdlc_common.py").exists():
            return candidate
    raise SystemExit(
        "Unable to locate authored-skill helper library. Expected sdlc-system/python_lib "
        "beside the authored skills root or under ~/.agents/skills."
    )


LIB = resolve_authoring_lib()
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from authored_skill_tools import authored_skill_dirs, validate_openai_yaml  # noqa: E402
from sdlc_common import load_artifact, write_artifact  # noqa: E402


SYSTEM_DIRS = {"_skill-governance", "sdlc-system", "superpowers", "__pycache__"}


def isoformat_timestamp(timestamp):
    if timestamp is None:
        return None
    return datetime.fromtimestamp(timestamp, tz=timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def newest_file_timestamp(path: Path):
    if not path.exists():
        return None
    newest = path.stat().st_mtime
    for child in path.rglob("*"):
        try:
            newest = max(newest, child.stat().st_mtime)
        except OSError:
            continue
    return newest


def skill_names(root: Path):
    if not root.exists():
        return set()
    return {path.name for path in root.iterdir() if path.is_dir()}


def local_governance_registry(authored_root: Path):
    path = authored_root / "_skill-governance" / "registry.json"
    if not path.exists():
        return {}
    try:
        payload = load_artifact(path)
    except Exception:
        return {}
    return payload.get("skills", {}) if isinstance(payload, dict) else {}


def main():
    parser = argparse.ArgumentParser(description="Audit authored and published skill registries.")
    parser.add_argument("--input", help="Optional JSON file with skills_root and published_root overrides")
    parser.add_argument("--output", default="skill_registry_audit.json", help="Output artifact path")
    args = parser.parse_args()

    authored_root = Path.home() / ".agents" / "skills"
    published_root = Path.home() / ".codex" / "skills"
    if args.input:
        payload = load_artifact(args.input)
        if isinstance(payload, dict):
            authored_root = Path(payload.get("skills_root", authored_root))
            published_root = Path(payload.get("published_root", published_root))

    authored = authored_skill_dirs(authored_root)
    authored_names = {path.name for path in authored}
    published_names = skill_names(published_root)
    platform_managed = sorted(name for name in published_names - authored_names if not name.startswith(".") and name not in SYSTEM_DIRS)
    local_system_entries = sorted(name for name in published_names - authored_names if name in SYSTEM_DIRS)
    registry = local_governance_registry(authored_root)
    authored_registry_gaps = sorted(name for name in authored_names if name not in registry)
    metadata_failures = []
    for skill_dir in authored:
        try:
            valid, details = validate_openai_yaml(skill_dir)
        except FileNotFoundError as exc:
            valid = False
            details = str(exc)
        if not valid:
            metadata_failures.append({"skill": skill_dir.name, "issue": details})

    authored_validation_report = authored_root / "sdlc-system" / "AUTHORED_VALIDATION_REPORT.md"
    validation_timestamp = authored_validation_report.stat().st_mtime if authored_validation_report.exists() else None
    skills_newer_than_validation = []
    newest_authored_skill = None
    newest_authored_skill_timestamp = None
    for skill_dir in authored:
        skill_timestamp = newest_file_timestamp(skill_dir)
        if newest_authored_skill_timestamp is None or (skill_timestamp is not None and skill_timestamp > newest_authored_skill_timestamp):
            newest_authored_skill = skill_dir.name
            newest_authored_skill_timestamp = skill_timestamp
        if validation_timestamp is not None and skill_timestamp is not None and skill_timestamp > validation_timestamp:
            skills_newer_than_validation.append(
                {
                    "skill": skill_dir.name,
                    "last_modified_at": isoformat_timestamp(skill_timestamp),
                }
            )

    if validation_timestamp is None:
        validation_status = "missing"
    elif skills_newer_than_validation:
        validation_status = "stale"
    else:
        validation_status = "current"

    report = {
        "artifact_type": "skill-registry-audit",
        "authored_count": len(authored_names),
        "published_count": len(published_names),
        "unpublished_skills": sorted(authored_names - published_names),
        "orphaned_published_skills": [],
        "platform_managed_published_skills": platform_managed,
        "local_system_published_entries": local_system_entries,
        "authored_registry_gaps": authored_registry_gaps,
        "metadata_failures": metadata_failures,
        "validation_artifacts": {
            "authored_validation_report": str(authored_validation_report),
            "authored_validation_report_exists": authored_validation_report.exists(),
            "authored_validation_report_last_modified_at": isoformat_timestamp(validation_timestamp),
            "status": validation_status,
            "skills_newer_than_validation": skills_newer_than_validation,
            "newest_authored_skill": newest_authored_skill,
            "newest_authored_skill_last_modified_at": isoformat_timestamp(newest_authored_skill_timestamp),
        },
    }

    path = write_artifact(report, args.output, "json")
    print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
