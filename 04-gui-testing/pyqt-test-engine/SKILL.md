---
name: pyqt-test-engine
description: Build and run pytest-qt test slices for PyQt/PySide widgets, dialogs, windows, QApplication lifecycle, event-loop flushing, and widget cleanup. Use when Codex must test internal Qt UI behavior with qtbot and record every failure into the GUI failure catalog.
---

# PyQt Test Engine

## Overview

Run or prepare pytest-qt checks and capture structured results and failures.

## Workflow

1. Resolve the repository path and initialize `.codex-project-intel` when needed.
2. Read existing project intelligence, diagnostics, GUI artifacts, and verification state before producing new output.
3. Run the deterministic script for this skill and keep artifacts under `.codex-project-intel/gui/`.
4. Record every GUI failure with evidence, reproduction steps, affected files, severity, confidence, and status.
5. Route repairs through `regression-guard` and `defect-fixer`, then retest the original failing GUI path.

## Core Workflow

Run:

```powershell
python scripts/run_pyqt_test_engine.py --input assets/inputs/sample_input.json --output assets/outputs/sample_output.json
```

Primary outputs:

- `gui/gui_test_results.json`
- `gui/gui_failure_catalog.json`

## References

Load when needed:

- `references/gui_testing_contract.md`

## Failure Modes

- Do not leave top-level widgets, timers, or event-loop work unaccounted for.
- Do not close a GUI failure from a narrow slice unless the original verification command passes.
- Do not hide pytest tracebacks; record them as evidence.
