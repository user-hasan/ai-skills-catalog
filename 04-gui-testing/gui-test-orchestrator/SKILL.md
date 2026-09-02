---
name: gui-test-orchestrator
description: Plan and coordinate desktop GUI testing across pytest-qt, PyAutoGUI, visual regression, sandboxing, failure recording, and repair retest loops. Use when Codex must decide the right GUI test path for Python/PyQt5 or other desktop UI projects and keep all evidence under `.codex-project-intel/gui/`.
---

# GUI Test Orchestrator

## Overview

Create an end-to-end GUI test plan that routes unit, integration, E2E, visual, flake, sandbox, failure, and retest work.

## Workflow

1. Resolve the repository path and initialize `.codex-project-intel` when needed.
2. Read existing project intelligence, diagnostics, GUI artifacts, and verification state before producing new output.
3. Run the deterministic script for this skill and keep artifacts under `.codex-project-intel/gui/`.
4. Record every GUI failure with evidence, reproduction steps, affected files, severity, confidence, and status.
5. Route repairs through `regression-guard` and `defect-fixer`, then retest the original failing GUI path.

## Core Workflow

Run:

```powershell
python scripts/run_gui_test_orchestrator.py --input assets/inputs/sample_input.json --output assets/outputs/sample_output.json
```

Primary outputs:

- `gui/gui_test_plan.json`

## References

Load when needed:

- `references/gui_testing_contract.md`

## Failure Modes

- Do not run broad GUI automation before a plan exists.
- Do not use PyAutoGUI for widget-level tests when pytest-qt is available.
- Do not skip failure recording for GUI test failures.
