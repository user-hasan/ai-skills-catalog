---
name: gui-test-data-sandbox
description: Prepare isolated GUI test data, temporary databases, settings, config files, screenshots folders, and cleanup instructions. Use when Codex must test desktop UI flows without touching real user data or persistent production settings.
---

# GUI Test Data Sandbox

## Overview

Create a safe GUI test sandbox contract under `.codex-project-intel/gui/`.

## Workflow

1. Resolve the repository path and initialize `.codex-project-intel` when needed.
2. Read existing project intelligence, diagnostics, GUI artifacts, and verification state before producing new output.
3. Run the deterministic script for this skill and keep artifacts under `.codex-project-intel/gui/`.
4. Record every GUI failure with evidence, reproduction steps, affected files, severity, confidence, and status.
5. Route repairs through `regression-guard` and `defect-fixer`, then retest the original failing GUI path.

## Core Workflow

Run:

```powershell
python scripts/run_gui_test_data_sandbox.py --input assets/inputs/sample_input.json --output assets/outputs/sample_output.json
```

Primary outputs:

- `gui/gui_test_plan.json`

## References

Load when needed:

- `references/gui_testing_contract.md`

## Failure Modes

- Do not point GUI tests at production data.
- Do not leave temporary settings or database paths undocumented.
- Do not clean outside the declared sandbox root.
