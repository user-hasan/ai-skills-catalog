---
name: dependency-governor
description: Detect dependency drift, risky package versions, missing lockfiles, and package hygiene gaps in enterprise repositories from local manifests and pinned-version heuristics. Use when Codex needs a repository-grounded dependency review before upgrades, security triage, architecture cleanup, or release readiness checks.
---

# Dependency Governor

## Overview

Inspect local dependency manifests and turn version and packaging signals into structured risks that are easy to act on.

## Workflow

1. Resolve the repository and inspect Python and Node dependency manifests.
2. Detect missing lockfiles, unpinned versions, and risky versions against explicit baselines.
3. Emit dependency risks into the shared risk register.
4. Return a concise summary of the hygiene and upgrade pressure.

## Core Workflow

Run:

```powershell
python scripts/run_dependency_governor.py --input assets/inputs/sample_input.json --output assets/outputs/sample_output.json
```

Primary outputs:

- `risk_register.json`

## References

Load when needed:

- `references/dependency_risk_heuristics.md`

## Failure Modes

- Do not pretend to have live package intelligence without an explicit source.
- Do not flag every old dependency as critical; use the baseline map and lockfile state.
- Do not mix dependency risks with build-command failures; those belong to diagnostics.
