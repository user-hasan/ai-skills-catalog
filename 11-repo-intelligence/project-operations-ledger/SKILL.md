---
name: project-operations-ledger
description: Initialize and maintain the shared `.codex-project-intel/` workspace for large software repositories, including project memory, intelligence summaries, progress state, decision logs, and operations events. Use when Codex needs to start durable repository tracking, refresh shared project analysis artifacts, or record enterprise-skill activity before or after diagnostics and remediation work.
---

# Project Operations Ledger

## Overview

Create and update the shared project-intelligence workspace that all enterprise Wave 1 skills depend on. This skill is the durable memory and status layer for a target repository.

## Workflow

1. Resolve the target repository path.
2. Initialize `.codex-project-intel/` if it does not exist.
3. Refresh project intelligence metadata such as language mix and manifests.
4. Append operations events, progress-state updates, and decision-log entries.
5. Return the exact artifact paths that downstream skills should read.

## Core Workflow

Run:

```powershell
python scripts/run_project_operations_ledger.py --input assets/inputs/sample_input.json --output assets/outputs/sample_output.json
```

Primary outputs:

- `project_memory.md`
- `project_intelligence.json`
- `operations_log.jsonl`
- `progress_state.json`
- `decision_log.md`

## References

Load when needed:

- `references/project_intel_contract.md`

## Failure Modes

- Do not point this skill at a non-repository path by accident; the target root must be explicit.
- Do not invent findings or risks here; this skill only establishes memory, state, and logging.
- Do not overwrite downstream diagnostics blindly; append events and merge state carefully.
