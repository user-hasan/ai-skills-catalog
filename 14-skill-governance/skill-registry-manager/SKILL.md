---
name: skill-registry-manager
description: Skill-lifecycle management for authored Codex skills, including available-skills troubleshooting, registry audits, metadata validation, publish planning, and cross-session smoke checks. Use when the user asks why a skill is not showing, wants to inspect the available skills list, compare authored versus published skills, validate skill metadata, or prepare a safe sync or install workflow for Codex skills.
---

# Skill Registry Manager

## Overview

Audit the local skill workspace and the published Codex skill directory so authored skills can be validated, published, and smoke-tested consistently.

## Workflow

1. Inspect the authored skill root and the published Codex skill root before assuming a skill is available.
2. Separate authored skill coverage from platform-managed or bundled published skills.
3. Run `scripts/audit_skill_registry.py` to compare coverage, metadata, publish status, authored registry gaps, and validation freshness.
4. When you need a full validation or publish step, use `python sdlc-system/validate_authored_skills.py` and `python sdlc-system/sync_authored_skills.py`.
5. Regenerate `agents/openai.yaml` through the local `skill-creator` tooling when metadata drifts.
6. Require a fresh Codex session before claiming a newly published skill is discoverable.

## Core Workflow

### Audit The Registry

Use these scripts:
- `scripts/audit_skill_registry.py`

Load these references only when needed:
- `references/registry_policy.md`
- `references/publish_workflow.md`
- `references/session_smoke_checklist.md`

## Resources

Use `references/` for policy guidance and `assets/` for smoke inputs and sample audit outputs.

## Failure Modes

- Do not assume authored skills are discoverable until they are published into the active Codex skill root.
- Do not treat platform-managed or bundled published skills as authored orphan warnings.
- Do not treat a stale authored validation report as proof of current publish readiness.
- Do not hand-edit stale metadata when the local generator can rebuild it deterministically.
- Do not claim session-level availability without restarting the session after publish.
