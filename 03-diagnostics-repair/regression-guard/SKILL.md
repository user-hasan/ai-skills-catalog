---
name: regression-guard
description: Map blast radius and verification requirements before repairs by expanding from target files and findings through the local dependency graph and likely affected tests. Use when Codex needs to know what might break before applying a fix, when a hot path is about to change, or when a remediation plan must stay narrowly scoped.
---

# Regression Guard

## Overview

Translate findings and target files into a concrete verification scope before any code is changed.

## Workflow

1. Resolve the repository and initialize project-intel artifacts if needed.
2. Load target files plus findings or a diagnostics artifact.
3. Expand through the reverse dependency graph to estimate blast radius.
4. Match likely affected tests and build `verification_requirements.json`.
5. Return the impacted files, tests, and verification checklist.

## Core Workflow

Run:

```powershell
python scripts/run_regression_guard.py --input assets/inputs/sample_input.json --output assets/outputs/sample_output.json
```

Primary outputs:

- `verification_requirements.json`

## References

Load when needed:

- `references/verification_mapping.md`

## Failure Modes

- Do not approve code edits from this skill.
- Do not omit the original target files from the scope summary.
- Do not call the scope complete unless impacted files and tests were both considered.
