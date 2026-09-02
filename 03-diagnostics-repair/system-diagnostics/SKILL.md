---
name: system-diagnostics
description: Detect build failures, test failures, broken imports, missing runtime configuration, and startup hazards in large software repositories with durable evidence under `.codex-project-intel/diagnostics/`. Use when Codex needs a diagnosis-first view of current project faults before planning repairs, regression checks, or broader architecture and performance analysis.
---

# System Diagnostics

## Overview

Inspect a repository for current operational faults and emit structured findings instead of vague summaries. This skill is read-only and feeds every repair-oriented skill that follows.

## Workflow

1. Resolve the repository path and initialize project-intel artifacts if needed.
2. Collect manifests, source files, and local dependency information.
3. Detect syntax, import, config, and command-level failures.
4. Write findings into `diagnostic_findings.json` and aggregate them into `failure_catalog.json`.
5. Return a concise execution summary with evidence references.

## Core Workflow

Run:

```powershell
python scripts/run_system_diagnostics.py --input assets/inputs/sample_input.json --output assets/outputs/sample_output.json
```

Primary outputs:

- `diagnostic_findings.json`
- `failure_catalog.json`

## References

Load when needed:

- `references/finding_taxonomy.md`

## Failure Modes

- Do not repair code from this skill; diagnostics are read-only.
- Do not emit findings without evidence and affected files.
- Do not collapse command failures, import failures, and config drift into one generic issue.
