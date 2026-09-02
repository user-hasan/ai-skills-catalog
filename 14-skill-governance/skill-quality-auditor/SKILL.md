---
name: skill-quality-auditor
description: Evaluate Codex skills for trigger quality, instruction clarity, resource design, determinism, validation strength, and update safety. Use when the user asks to review a skill, score its quality, diagnose why a skill feels weak, compare two skill revisions, or prepare a safe improvement plan before editing the skill.
---

# Skill Quality Auditor

## Overview

Score a local Codex skill with evidence instead of opinion. This skill diagnoses quality gaps and produces a structured report that can feed `skill-forge-master` or `skill-update-governor`.

## Workflow

1. Start from a specific skill name, not the whole skill root.
2. Run `scripts/audit_skill_quality.py` before proposing edits.
3. Read the resulting score breakdown and issue list.
4. Use the report to decide whether the skill needs metadata fixes, workflow tightening, better references, or smoke artifacts.

## Core Workflow

### Audit A Skill

Run:

```powershell
python scripts/audit_skill_quality.py --input assets/inputs/sample_input.json --output assets/outputs/sample_quality_report.json
```

Primary output:
- `skill_quality_report.json`

## References

Load when needed:
- `references/quality_dimensions.md`
- `references/remediation_playbook.md`

## Failure Modes

- Do not edit the skill directly from this auditor. This skill only diagnoses quality.
- Do not score a skill from its folder name alone; always inspect `SKILL.md` and `agents/openai.yaml`.
- Do not collapse all weaknesses into one vague rating; keep the dimensions separate.
