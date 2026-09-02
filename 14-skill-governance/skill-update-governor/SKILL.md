---
name: skill-update-governor
description: Review skill update requests, verify that the proposed scope is constrained, analyze downstream impact, and produce an approval decision with verification requirements. Use when a skill update request exists and the user wants a disciplined yes/no/review decision before editing the skill.
---

# Skill Update Governor

## Overview

This skill is the gate between update intelligence and implementation. It approves, defers, rejects, routes policy-blocked requests for review, or escalates updates based on scope, impact, and source discipline.

## Workflow

1. Start from a structured `skill_update_request.json`.
2. Validate the target skill, source policy, and proposed file scope.
3. Run impact analysis before deciding.
4. Emit the decision and verification requirements without editing the skill.
5. Only approved requests should move on to implementation.

## Core Workflow

### Review A Skill Update Request

Run:

```powershell
python scripts/review_skill_update_request.py --input assets/inputs/sample_update_request.json --output assets/outputs/sample_approval_decision.json
```

Primary outputs:
- `change_scope_report.json`
- `approval_decision.json`
- `verification_requirements.json`

## References

Load when needed:
- `references/decision_rules.md`
- `references/scope_control.md`

## Failure Modes

- Do not approve updates with out-of-scope file edits.
- Do not approve sources that violate the strict allowlist.
- Do not collapse trustworthy but policy-blocked primary-doc requests into a normal rejection when they require a separate source-policy decision.
- Do not skip impact review for shared, governance, or security-sensitive skills.
