---
name: stability-hardener
description: Prepare scoped stability hardening work for startup resilience, teardown leaks, retry behavior, timer cleanup, config fallbacks, null guards, and fragile runtime paths. Use after diagnostics, incidents, or risks provide evidence that a narrow hardening patch is justified.
---

# Stability Hardener

## Overview

Convert proven instability evidence into small hardening plans and verification requirements.

## Workflow

1. Read incidents, risks, failure catalog, and change-impact map.
2. Select only evidence-backed stability targets.
3. Build a hardening plan with small, verifiable work items.
4. Write `stability/hardening_plan.json` and add scoped repair-plan entries.
5. Require verification evidence before marking hardening work complete.

## Core Workflow

Run:

```powershell
python scripts/run_stability_hardener.py --input assets/inputs/sample_input.json --output assets/outputs/sample_output.json
```

Primary outputs:

- `stability/hardening_plan.json`
- `remediation/repair_plan.json`

## References

Load when needed:

- `references/wave2_contract.md`

## Failure Modes

- Do not start from generic robustness advice.
- Do not widen hardening into architecture refactors.
- Do not change behavior without a verification path.
