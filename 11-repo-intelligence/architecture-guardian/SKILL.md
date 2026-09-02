---
name: architecture-guardian
description: Detect dependency cycles, boundary leaks, architectural drift, and oversized hub files in large repositories using import graphs and explicit layer rules. Use when Codex needs evidence-backed architecture findings before a refactor, when a codebase feels tightly coupled, or when enterprise diagnostics must explain why the current structure is becoming unsafe.
---

# Architecture Guardian

## Overview

Inspect the repository structure as a graph and emit architecture risks that are backed by file relationships and layer rules.

## Workflow

1. Resolve the repository and initialize project-intel artifacts if needed.
2. Build a local dependency graph from Python and JavaScript or TypeScript files.
3. Detect cycles, forbidden layer crossings, and oversized central hubs.
4. Write architecture risks into `risk_register.json`.
5. Return a concise summary of the structural pressure points.

## Core Workflow

Run:

```powershell
python scripts/run_architecture_guardian.py --input assets/inputs/sample_input.json --output assets/outputs/sample_output.json
```

Primary outputs:

- `risk_register.json`

## References

Load when needed:

- `references/layer_violation_rules.md`

## Failure Modes

- Do not call a file a hub without graph evidence.
- Do not flag a layer violation unless a concrete rule was supplied or inferred.
- Do not mix architecture findings into diagnostics or repair plans; keep them inside the risk register.
