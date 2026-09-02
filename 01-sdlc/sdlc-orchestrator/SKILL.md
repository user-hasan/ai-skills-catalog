---
name: sdlc-orchestrator
description: End-to-end SDLC orchestration, phase coordination, artifact validation, handoff enforcement, progress tracking, and integrated reporting across the full skill suite. Use when Codex must run the complete SDLC workflow, validate cross-role outputs, gate phase transitions, or produce a unified delivery status view across planning, build, QA, DevOps, and project management.
---

# SDLC Orchestrator

## Overview

Coordinate all other SDLC skills, enforce handoff quality, and produce integrated reporting across the suite.

## Workflow

1. Read the latest upstream artifact set and summarize what is known.
2. Detect missing information before generating downstream artifacts.
3. Use the smallest set of references needed for the current task.
4. Run the role-specific scripts instead of rewriting the same structure by hand.
5. Validate the output and package a clean handoff for the next SDLC role.

## Core Workflows

### 1. Run Sdlc Phase

Run a selected SDLC phase and summarize readiness.

Use these scripts:
- `scripts/run_sdlc_phase.py`

Load these references only when needed:
- `references/sdlc_workflow.md`
- `references/artifact_schemas.md`

### 2. Handoff Between Roles

Create a structured handoff package between two SDLC roles.

Use these scripts:
- `scripts/handoff_between_roles.py`

Load these references only when needed:
- `references/sdlc_workflow.md`
- `references/artifact_schemas.md`

### 3. Validate Artifacts

Validate artifact completeness before phase transitions.

Use these scripts:
- `scripts/validate_artifacts.py`

Load these references only when needed:
- `references/sdlc_workflow.md`
- `references/artifact_schemas.md`

### 4. Track Sdlc Progress

Track suite progress across all SDLC stages.

Use these scripts:
- `scripts/track_sdlc_progress.py`

Load these references only when needed:
- `references/sdlc_workflow.md`
- `references/artifact_schemas.md`

### 5. Rollback Phase

Document how to roll a failed SDLC phase back to a stable state.

Use these scripts:
- `scripts/rollback_phase.py`

Load these references only when needed:
- `references/sdlc_workflow.md`
- `references/artifact_schemas.md`

## Integration

Inputs expected from upstream:
- `suite_artifacts/`
- `project_status.json`

Outputs produced for downstream roles:
- `integrated_sdlc_report.md`
- `suite_validation.json`
- `phase_status.json`

Upstream roles:
- `sdlc-requirements-guru`
- `sdlc-pm-product`
- `sdlc-ba`
- `sdlc-arch`
- `sdlc-dev`
- `sdlc-qa`
- `sdlc-devops`
- `sdlc-pm-project`

Downstream roles:
- `suite-complete`

## Resources

Use `references/` for role-specific guidance, `scripts/` for deterministic execution, and `assets/` for templates, checklists, and output examples.

## Failure Modes

- Stop and request clarification when a required upstream artifact is missing or contradictory.
- Do not hand off vague artifacts; record the open issues inside the output itself.
- When a script output is insufficient, refine the input artifact first instead of guessing.
