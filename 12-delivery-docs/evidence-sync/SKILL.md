---
name: evidence-sync
description: Synchronize diagnostics, remediation, verification, CI, security, incidents, stability, release, docs, and delivery evidence into one bundle. Use when Codex must prepare docs-automation, release-manager, and delivery-sync inputs from the same verified source artifacts without pushing live tracker changes.
---

# Evidence Sync

## Overview

Build a single evidence bundle and handoff payloads from project-intel artifacts.

## Workflow

1. Read all Wave 1 and Wave 2 project-intel artifacts that exist.
2. Extract closed items, open risks, verification results, CI failures, security remediations, incidents, and hardening work.
3. Write `evidence/evidence_bundle.json` with handoffs for docs, release, and delivery skills.
4. Do not push to Linear, GitHub, Notion, or release systems directly.
5. Return the handoff summary and artifact paths.

## Core Workflow

Run:

```powershell
python scripts/run_evidence_sync.py --input assets/inputs/sample_input.json --output assets/outputs/sample_output.json
```

Primary outputs:

- `evidence/evidence_bundle.json`

## References

Load when needed:

- `references/wave2_contract.md`

## Failure Modes

- Do not overwrite richer tracker or documentation state.
- Do not treat unverified repairs as release-ready evidence.
- Do not perform live sync; hand off to delivery-sync.
