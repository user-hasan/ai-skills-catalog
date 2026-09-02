---
name: gui-flake-stabilizer
description: Diagnose unstable GUI tests caused by event-loop leakage, timers, teardown gaps, focus issues, delayed widgets, race conditions, and flaky visual checks. Use when Codex must classify GUI flakiness and produce a small stabilization plan before repair.
---

# GUI Flake Stabilizer

## Overview

Analyze recorded GUI failures and produce a flake report with stabilization steps.

## Workflow

1. Resolve the repository path and initialize `.codex-project-intel` when needed.
2. Read existing project intelligence, diagnostics, GUI artifacts, and verification state before producing new output.
3. Run the deterministic script for this skill and keep artifacts under `.codex-project-intel/gui/`.
4. Record every GUI failure with evidence, reproduction steps, affected files, severity, confidence, and status.
5. Route repairs through `regression-guard` and `defect-fixer`, then retest the original failing GUI path.

## Core Workflow

Run:

```powershell
python scripts/run_gui_flake_stabilizer.py --input assets/inputs/sample_input.json --output assets/outputs/sample_output.json
```

Primary outputs:

- `gui/flake_report.json`

## References

Load when needed:

- `references/gui_testing_contract.md`

## Failure Modes

- Do not call a GUI failure flaky without repeated or timing-related evidence.
- Do not fix flake signals with broad sleeps as the default strategy.
- Do not skip full-file or original-flow verification after stabilizing a slice.
