---
name: skill-forge-master
description: Design new Codex skills and improve existing ones with strong triggers, clear instructions, deterministic scripts, scoped patch plans, and governance-aware outputs. Use when the user asks to create a new skill, upgrade an existing skill, compare a skill against quality standards, or produce a decision-complete skill design before implementation starts.
---

# Skill Forge Master

## Overview

This is the primary architect for skill creation and skill improvement. It turns a skill request or an existing skill into a structured design spec, a quality diagnosis, a scoped patch plan, and a governance-friendly update request.

## Workflow

1. Start from a concrete skill name and intent.
2. If the skill already exists, audit it before proposing edits.
3. Produce the four core artifacts before implementation begins.
4. Keep every proposed change scoped to the target skill unless governance explicitly requires more.
5. Hand update-driven work to `skill-update-governor` before treating it as approved.

## Core Workflow

### Forge A Skill Plan

Run:

```powershell
python scripts/forge_skill_plan.py --input assets/inputs/sample_input.json --output assets/outputs/sample_update_request.json
```

Primary outputs:
- `skill_design_spec.md`
- `skill_quality_report.json`
- `skill_patch_plan.md`
- `skill_update_request.json`

## References

Load when needed:
- `references/design_principles.md`
- `references/improvement_heuristics.md`
- `references/scoped_change_rules.md`

## Failure Modes

- Do not start from implementation details before defining the trigger and workflow shape.
- Do not widen the patch scope beyond the target skill without governance evidence.
- Do not treat a low-quality skill as a rewrite target by default; propose the smallest repair that fixes the identified weakness.
