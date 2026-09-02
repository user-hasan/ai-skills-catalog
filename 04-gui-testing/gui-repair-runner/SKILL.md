---
name: gui-repair-runner
description: Read recorded GUI failures, build scoped GUI repair plans, require regression scope and verification commands, and retest the original failing test or E2E flow after repair. Use when Codex must close GUI failures through defect-fixer and regression-guard without broad refactors.
---

# GUI Repair Runner

## Overview

Turn recorded GUI failures into small repair batches and retest reports.

## Workflow

1. Resolve the repository path and initialize `.codex-project-intel` when needed.
2. Read existing project intelligence, diagnostics, GUI artifacts, and verification state before producing new output.
3. Run the deterministic script for this skill and keep artifacts under `.codex-project-intel/gui/`.
4. Record every GUI failure with evidence, reproduction steps, affected files, severity, confidence, and status.
5. Route repairs through `regression-guard` and `defect-fixer`, then retest the original failing GUI path.

## Core Workflow

Run:

```powershell
python scripts/run_gui_repair_runner.py --input assets/inputs/sample_input.json --output assets/outputs/sample_output.json
```

Primary outputs:

- `gui/gui_repair_plan.json`
- `gui/gui_retest_report.json`
- `verification/verification_report.json`

## References

Load when needed:

- `references/gui_testing_contract.md`

## Failure Modes

- Do not repair without a recorded failure, reproduction steps, affected files, regression scope, and verification command.
- Do not start broad UI refactors from this skill.
- Do not hide failed retests or new GUI failures.
