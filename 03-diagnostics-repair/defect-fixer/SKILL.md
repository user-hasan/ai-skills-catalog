---
name: defect-fixer
description: Convert repository findings into scoped repair plans and optionally apply declarative file edits inside an approved verification scope. Use when Codex already has diagnostics and blast-radius information, when a repair plan must stay tightly bounded, or when a structured fix workflow is needed before a human reviews the resulting changes.
---

# Defect Fixer

## Overview

Turn structured findings into an explicit remediation plan, and optionally execute declarative edits when scope and verification inputs are present.

## Workflow

1. Resolve the repository and initialize project-intel artifacts if needed.
2. Load findings and any verification-scope information.
3. Build a scoped `repair_plan.json`.
4. Optionally apply declarative edits when `allow_edits` is true.
5. Write a `verification_report.json` describing applied changes and pending checks.

## Core Workflow

Run:

```powershell
python scripts/run_defect_fixer.py --input assets/inputs/sample_input.json --output assets/outputs/sample_output.json
```

Primary outputs:

- `repair_plan.json`
- `verification_report.json`

## References

Load when needed:

- `references/scoped_repair_policy.md`

## Failure Modes

- Do not apply edits without `allow_edits=true`.
- Do not repair files outside the repository root or outside the declared verification scope.
- Do not mark the repair complete if verification steps remain pending.
