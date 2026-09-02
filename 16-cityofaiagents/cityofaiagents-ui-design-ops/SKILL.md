---
name: cityofaiagents-ui-design-ops
description: Mirrored CityOfAIAgents skill for ui-design-ops. Use when Codex must turn desktop UI critique, layout cleanup, or redesign intent into a structured design-operations brief without modifying application code directly.
---

# CityOfAIAgents UI Design Ops

## Overview

Convert desktop UI concerns into a research-backed design-operations brief that is safe to hand to implementation or review workflows.

## Workflow

1. Read the incoming UI description, screenshot notes, or redesign request.
2. Preserve the internal CityOfAIAgents artifact identity as the source of truth.
3. Extract the layout, hierarchy, navigation, accessibility, and theming concerns that materially affect the desktop UI.
4. Build a structured design brief with focus areas, supported tags, and reference links for the downstream implementer.
5. Keep the result in artifact form; do not mutate product code from this mirrored skill.

## Core Workflow

Run:

```powershell
python scripts/run_cityofaiagents_ui_design_ops.py --input assets/inputs/sample_input.json --output assets/outputs/sample_output.json
```

Primary outputs:

- `ui_design_ops_plan.json`

## References

Load when needed:

- `references/design_sources.md`

## Failure Modes

- Do not turn this mirrored skill into a code-edit workflow.
- Do not drop the internal CityOfAIAgents artifact identity or supported tags.
- Do not replace concrete layout or accessibility findings with generic design praise.
