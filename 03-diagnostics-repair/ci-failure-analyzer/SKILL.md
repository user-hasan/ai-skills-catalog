---
name: ci-failure-analyzer
description: Analyze CI, GitHub Actions, or pipeline logs and turn them into repository-grounded failure reports and diagnostic findings. Use when Codex must classify failed jobs, extract failing commands, detect flaky or environment-only failures, and prepare local reproduction evidence before repair work.
---

# CI Failure Analyzer

## Overview

Convert long CI logs into structured failure evidence that can feed diagnostics, regression planning, and repair.

## Workflow

1. Load CI log text or a log file path from the request.
2. Extract failing commands, test names, paths, exit codes, traceback hints, and workflow references.
3. Preserve GitHub Actions evidence such as debug flags, workflow command groups, step-summary output, reusable workflow boundaries, and artifact-attestation references.
4. Classify failures as command, test, environment, configuration, or flaky signals.
5. Write `ci/ci_failure_report.json` and update `diagnostics/diagnostic_findings.json` with CI-sourced findings.
6. Return a concise reproduction and repair-routing summary without editing workflows.

## Core Workflow

Run:

```powershell
python scripts/run_ci_failure_analyzer.py --input assets/inputs/sample_input.json --output assets/outputs/sample_output.json
```

Primary outputs:

- `ci/ci_failure_report.json`
- `diagnostics/diagnostic_findings.json`

## References

Load when needed:

- `references/wave2_contract.md`
- `references/github_actions_evidence.md`

## Failure Modes

- Do not edit CI workflow files.
- Do not treat all CI failures as code defects; preserve environment-only and flaky classifications.
- Do not claim local reproduction without an explicit command or evidence.
- Do not treat artifact attestations as proof that an artifact is secure; record them only as provenance evidence.
- Do not collapse reusable workflow caller and callee paths into one generic workflow reference.
