---
name: change-impact-mapper
description: Map the blast radius of proposed code, dependency, security, migration, or refactor changes before repair work begins. Use when Codex needs to identify impacted files, tests, docs, manifests, and downstream modules before invoking regression-guard, defect-fixer, security-remediator, or stability-hardener.
---

# Change Impact Mapper

## Overview

Build a read-only change-impact map from repository dependency graph, project-intel artifacts, and explicit target files.

## Workflow

1. Resolve the repository and initialize `.codex-project-intel` if needed.
2. Read target files from the request, findings, risks, or repair plans.
3. Use the local dependency graph and test matching helpers to find affected files and verification surfaces.
4. Write `impact/change_impact_map.json` and append an operations-log event.
5. Return the impact summary without changing repository code.

## Core Workflow

Run:

```powershell
python scripts/run_change_impact_mapper.py --input assets/inputs/sample_input.json --output assets/outputs/sample_output.json
```

Primary outputs:

- `impact/change_impact_map.json`

## References

Load when needed:

- `references/wave2_contract.md`

## Failure Modes

- Do not include virtualenv, vendor, generated, or dependency-cache paths unless explicitly targeted.
- Do not turn impact mapping into an implementation plan.
- Do not close findings or risks from this skill.
