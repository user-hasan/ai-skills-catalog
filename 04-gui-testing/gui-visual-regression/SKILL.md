---
name: gui-visual-regression
description: Compare GUI screenshots and detect visual regressions such as missing elements, layout overlap, blank windows, clipped content, or unexpected rendering changes. Use when Codex must validate desktop UI appearance with screenshots, Pillow, and structured visual evidence.
---

# GUI Visual Regression

## Overview

Build visual regression reports from screenshots and register visual failures when thresholds are exceeded.

## Workflow

1. Resolve the repository path and initialize `.codex-project-intel` when needed.
2. Read existing project intelligence, diagnostics, GUI artifacts, and verification state before producing new output.
3. Run the deterministic script for this skill and keep artifacts under `.codex-project-intel/gui/`.
4. Record every GUI failure with evidence, reproduction steps, affected files, severity, confidence, and status.
5. Route repairs through `regression-guard` and `defect-fixer`, then retest the original failing GUI path.

## Core Workflow

Run:

```powershell
python scripts/run_gui_visual_regression.py --input assets/inputs/sample_input.json --output assets/outputs/sample_output.json
```

Primary outputs:

- `gui/visual_regression_report.json`
- `gui/gui_failure_catalog.json`

## References

Load when needed:

- `references/gui_testing_contract.md`

## Failure Modes

- Do not treat a screenshot capture as proof of correctness by itself.
- Do not compare unstable dynamic regions without masking or a clear threshold.
- Do not hide visual mismatches; store their screenshot paths and metrics.
