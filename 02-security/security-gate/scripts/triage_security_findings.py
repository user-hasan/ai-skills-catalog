#!/usr/bin/env python3
"""Rank security findings and decide whether the gate passes."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

LIB = Path(__file__).resolve().parents[2] / "sdlc-system" / "python_lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from sdlc_common import list_from_payload, load_artifact, write_artifact  # noqa: E402


SEVERITY_SCORE = {"critical": 4, "high": 3, "medium": 2, "low": 1}


def normalize_finding(item):
    if not isinstance(item, dict):
        return {"title": str(item), "severity": "medium", "owner": "security-owner", "status": "open"}
    return {
        "title": item.get("title") or item.get("rule") or "Unnamed finding",
        "severity": str(item.get("severity", "medium")).lower(),
        "owner": item.get("owner") or "security-owner",
        "status": str(item.get("status", "open")).lower(),
    }


def main():
    parser = argparse.ArgumentParser(description="Triage security findings into a gate decision.")
    parser.add_argument("--input", required=True, help="Path to the findings artifact")
    parser.add_argument("--output", default="security_gate.json", help="Output artifact path")
    args = parser.parse_args()

    payload = load_artifact(args.input)
    findings = [normalize_finding(item) for item in list_from_payload(payload, ["findings", "items", "alerts"])]
    findings.sort(key=lambda item: (-SEVERITY_SCORE.get(item["severity"], 0), item["title"]))

    open_findings = [item for item in findings if item["status"] not in {"resolved", "fixed", "closed"}]
    if any(item["severity"] == "critical" for item in open_findings):
        gate_status = "fail"
    elif any(item["severity"] == "high" for item in open_findings):
        gate_status = "warn"
    else:
        gate_status = "pass"

    report = {
        "artifact_type": "security-gate",
        "gate_status": gate_status,
        "open_findings": open_findings,
        "recommended_actions": [
            "Resolve all critical findings before release.",
            "Create owner-tracked remediation tickets for all high findings.",
            "Document accepted risk explicitly for any deferred medium findings.",
        ],
    }

    path = write_artifact(report, args.output, "json")
    print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
