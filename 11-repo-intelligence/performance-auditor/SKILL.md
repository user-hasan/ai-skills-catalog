---
name: performance-auditor
description: Detect slow tests, oversized hotspot files, nested loop patterns, loop-scoped I/O, and expensive repository commands from local evidence. Use when Codex needs an early performance-risk pass before optimization work, when builds or tests feel slow, or when enterprise planning needs evidence for likely scaling bottlenecks.
---

# Performance Auditor

## Overview

Find performance pressure points that are already visible in the repository before the system reaches production scale.

## Workflow

1. Resolve the repository and initialize project-intel artifacts if needed.
2. Scan source and test files for slow-pattern heuristics and oversized hotspots.
3. Optionally time explicit commands from the request.
4. Write performance risks into the shared risk register.
5. Return a concise summary of the strongest bottleneck signals.

## Core Workflow

Run:

```powershell
python scripts/run_performance_auditor.py --input assets/inputs/sample_input.json --output assets/outputs/sample_output.json
```

Primary outputs:

- `risk_register.json`

## References

Load when needed:

- `references/hotspot_patterns.md`

## Failure Modes

- Do not present generic optimization advice without file-level evidence.
- Do not confuse architecture coupling with performance pressure; keep the risk labels separate.
- Do not claim a command is slow unless its measured duration crossed the declared threshold.
