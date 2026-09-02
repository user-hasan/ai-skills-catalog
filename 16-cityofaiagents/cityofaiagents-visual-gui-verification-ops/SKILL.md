---
name: cityofaiagents-visual-gui-verification-ops
description: Mirrored CityOfAIAgents skill for visual-gui-verification-ops. Use when Codex must turn a desktop visual-verification request into a safe evidence-oriented guide without editing product code or bypassing sandbox boundaries.
---

# CityOfAIAgents Visual GUI Verification Ops

## Overview

Create an evidence-first visual verification brief for real desktop GUI checks, screenshot capture, and safe root-cause proposal handoff.

## Workflow

1. Read the verification target, UI flow, and expected evidence from the request.
2. Preserve the internal CityOfAIAgents artifact identity as the source of truth.
3. Build a verification brief that captures the target flow, required evidence, and failure-recording expectations.
4. Keep the result sandbox-aware and guide-driven; do not mutate application code from this mirrored skill.
5. Return structured output that downstream verification or repair workflows can consume safely.

## Core Workflow

Run:

```powershell
python scripts/run_cityofaiagents_visual_gui_verification_ops.py --input assets/inputs/sample_input.json --output assets/outputs/sample_output.json
```

Primary outputs:

- `visual_gui_verification_plan.json`

## References

Load when needed:

- `references/verification_contract.md`

## Failure Modes

- Do not treat screenshots alone as sufficient proof without step or state expectations.
- Do not mutate application code or desktop state from this mirrored skill.
- Do not drop the internal CityOfAIAgents artifact identity or supported tags.
