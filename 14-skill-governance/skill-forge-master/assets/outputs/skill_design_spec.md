# Skill Design Spec: system-diagnostics

- Generated at: `2026-04-28T01:30:05Z`
- Mode: `create`
- Existing skill: `False`
- Category: `frameworks-languages-infra`

## Intent

- Create a diagnostics skill for enterprise projects
- Detect current faults, build issues, runtime hazards, and likely future failures with durable evidence.

## Trigger Contract

- The skill must trigger when the user explicitly names `system-diagnostics` or when the task clearly matches its narrow domain.
- The frontmatter description must include both what the skill does and when it should be used.
- `agents/openai.yaml` must include an explicit `$skill-name` default prompt.

## Required Structure

- `SKILL.md` with concise overview, workflow, references, and failure modes
- `agents/openai.yaml` with `policy.allow_implicit_invocation: true` unless the skill must stay explicit-only
- `scripts/` for deterministic transforms
- `references/` for progressive disclosure
- `assets/inputs` and `assets/outputs` for smoke validation when scripts exist

## Quality Signals

- Current quality grade: `new`
- Current total score: `0`

## Constraints

- Keep the initial version read-only and diagnosis-first
- Require durable evidence outputs under the skill assets model

## Expected Outputs

- `skill_design_spec.md`
- `skill_quality_report.json`
- `skill_patch_plan.md`
- `skill_update_request.json`
