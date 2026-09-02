---
name: desktop-e2e-automation
description: Plan and run desktop end-to-end GUI automation with PyAutoGUI where external window control is required. Use when Codex must launch a real desktop app, click, type, navigate, capture screenshots, and record E2E evidence without manual intervention.
---

# Desktop E2E Automation

## Overview

Create PyAutoGUI-oriented E2E run logs and failure evidence for real desktop flows.

## Workflow

1. Resolve the repository path and initialize `.codex-project-intel` when needed.
2. Read existing project intelligence, diagnostics, GUI artifacts, and verification state before producing new output.
3. Run the deterministic script for this skill and keep artifacts under `.codex-project-intel/gui/`.
4. Record every GUI failure with evidence, reproduction steps, affected files, severity, confidence, and status.
5. Route repairs through `regression-guard` and `defect-fixer`, then retest the original failing GUI path.

## Core Workflow

Run:

```powershell
python scripts/run_desktop_e2e_automation.py --input assets/inputs/sample_input.json --output assets/outputs/sample_output.json
```

Primary outputs:

- `gui/e2e_run_log.json`
- `gui/screenshots/`

## References

Load when needed:

- `references/gui_testing_contract.md`

## Failure Modes

- Do not require PyAutoGUI for headless widget tests.
- Do not rely on screenshots alone without a logical assertion or expected state.
- Do not run destructive desktop flows without an explicit sandbox or test target.
