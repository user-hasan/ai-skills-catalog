---
name: gui-failure-recorder
description: Record every GUI test failure from pytest-qt, PyAutoGUI, visual regression, startup checks, missing elements, timing races, and interaction flows. Use when Codex must preserve screenshots, tracebacks, reproduction steps, affected files, severity, confidence, and status under `.codex-project-intel/gui/`.
---

# GUI Failure Recorder

## Overview

Normalize GUI failures into `gui_failure_catalog.json`, `gui_error_log.jsonl`, and diagnostic findings.

## Workflow

1. Resolve the repository path and initialize `.codex-project-intel` when needed.
2. Read existing project intelligence, diagnostics, GUI artifacts, and verification state before producing new output.
3. Run the deterministic script for this skill and keep artifacts under `.codex-project-intel/gui/`.
4. Record every GUI failure with evidence, reproduction steps, affected files, severity, confidence, and status.
5. Route repairs through `regression-guard` and `defect-fixer`, then retest the original failing GUI path.

## Core Workflow

Run:

```powershell
python scripts/run_gui_failure_recorder.py --input assets/inputs/sample_input.json --output assets/outputs/sample_output.json
```

Primary outputs:

- `gui/gui_failure_catalog.json`
- `gui/gui_error_log.jsonl`

## References

Load when needed:

- `references/gui_testing_contract.md`

## Failure Modes

- Do not drop screenshots, tracebacks, or reproduction steps when available.
- Do not merge unrelated GUI failures into one catalog entry.
- Do not mark a failure fixed before a retest report confirms the original flow.
