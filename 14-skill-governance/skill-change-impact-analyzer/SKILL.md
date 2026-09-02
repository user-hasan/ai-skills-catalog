---
name: skill-change-impact-analyzer
description: Analyze the downstream impact of changing a Codex skill by inspecting direct skill references, governance files, and shared dependency hints. Use when the user asks what will break if a skill changes, wants to scope a skill update safely, or needs impact evidence before approving changes to a shared or sensitive skill.
---

# Skill Change Impact Analyzer

## Overview

Map the blast radius of a skill change before anything is edited. This skill is the dependency and governance impact lens for `skill-update-governor` and `skill-forge-master`.

## Workflow

1. Start from the exact skill name.
2. Run `scripts/analyze_skill_change_impact.py` before approving a patch plan.
3. Review direct references from other skills and the governance files that must be checked.
4. Use the report to decide whether the change is local, shared, or high-sensitivity.

## Core Workflow

### Analyze Skill Change Impact

Run:

```powershell
python scripts/analyze_skill_change_impact.py --input assets/inputs/sample_input.json --output assets/outputs/sample_impact_report.json
```

Primary output:
- `skill_change_impact_report.json`

## References

Load when needed:
- `references/impact_rules.md`
- `references/high_sensitivity_conditions.md`

## Failure Modes

- Do not approve a change just because the target skill folder is local; inspect direct references first.
- Do not assume a skill is isolated if governance files or shared policies are involved.
- Do not convert impact analysis into an edit plan; this skill only maps the blast radius.
