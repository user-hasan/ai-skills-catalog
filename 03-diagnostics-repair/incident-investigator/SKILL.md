---
name: incident-investigator
description: Investigate production-like incidents, user-reported crashes, logs, tracebacks, Sentry exports, and runtime symptoms. Use when Codex must separate symptoms from triggers, suspected root cause, confirmed root cause, and verification gaps before repairs or hardening.
---

# Incident Investigator

## Overview

Turn runtime symptoms and logs into a durable incident report with evidence and follow-up diagnostics.

## Workflow

1. Load incident description, logs, traces, or crash text.
2. Extract symptoms, file paths, stack frames, trigger signals, and missing verification.
3. Compare the incident against project memory and current failure catalog.
4. Write `incidents/incident_report.json` and add diagnostic findings when evidence is strong enough.
5. Record decisions only when the report changes operating assumptions.

## Core Workflow

Run:

```powershell
python scripts/run_incident_investigator.py --input assets/inputs/sample_input.json --output assets/outputs/sample_output.json
```

Primary outputs:

- `incidents/incident_report.json`
- `diagnostics/diagnostic_findings.json`

## References

Load when needed:

- `references/wave2_contract.md`

## Failure Modes

- Do not declare a final root cause without evidence.
- Do not edit code from this skill.
- Do not collapse symptoms, triggers, and root causes into one field.
