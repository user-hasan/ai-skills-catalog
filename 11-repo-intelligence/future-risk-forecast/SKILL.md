---
name: future-risk-forecast
description: Forecast future repository fragility from dependency-graph centrality, test gaps, churn signals, ownerless paths, and TODO density before incidents occur. Use when Codex needs a predictive risk view after diagnostics, when a codebase feels stable now but structurally fragile, or when enterprise planning needs early warning signals for likely future failures.
---

# Future Risk Forecast

## Overview

Turn structural and maintenance signals into future-facing risks with explicit time horizons and trigger signals.

## Workflow

1. Resolve the repository and initialize project-intel artifacts if needed.
2. Measure centrality, test coverage gaps, churn hints, and TODO density.
3. Convert those signals into predictive risks with clear horizons.
4. Write the risks into the shared risk register.
5. Return a summary of the most fragile future hotspots.

## Core Workflow

Run:

```powershell
python scripts/run_future_risk_forecast.py --input assets/inputs/sample_input.json --output assets/outputs/sample_output.json
```

Primary outputs:

- `risk_register.json`

## References

Load when needed:

- `references/predictive_signals.md`

## Failure Modes

- Do not present current breakages as future risks.
- Do not omit the time horizon or trigger signals.
- Do not rely on churn guesses when real churn data or explicit simulated data is absent.
