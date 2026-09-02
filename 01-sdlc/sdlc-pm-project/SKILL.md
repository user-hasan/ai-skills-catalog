---
name: sdlc-pm-project
description: Project management, sprint planning, work allocation, progress tracking, risk management, and stakeholder reporting for delivery execution. Use when Codex must plan execution cadence, distribute work, track velocity, manage delivery risks, or communicate project status to stakeholders during implementation.
---

# Project Manager

## Overview

Translate prepared product, engineering, QA, and DevOps work into sprint planning, task balance, status tracking, and stakeholder reporting.

## Workflow

1. Read the latest upstream artifact set and summarize what is known.
2. Detect missing information before generating downstream artifacts.
3. Use the smallest set of references needed for the current task.
4. Run the role-specific scripts instead of rewriting the same structure by hand.
5. Validate the output and package a clean handoff for the next SDLC role.

## Core Workflows

### 1. Plan Sprint

Create a sprint plan from prioritized work items.

Use these scripts:
- `scripts/plan_sprint.py`

Load these references only when needed:
- `references/agile_methodologies.md`
- `references/sprint_planning_guide.md`

### 2. Assign Tasks

Rank tasks or owners to balance work assignments.

Use these scripts:
- `scripts/assign_tasks.py`

Load these references only when needed:
- `references/agile_methodologies.md`
- `references/sprint_planning_guide.md`

### 3. Track Progress

Track project progress using issue or task status.

Use these scripts:
- `scripts/track_progress.py`

Load these references only when needed:
- `references/agile_methodologies.md`
- `references/sprint_planning_guide.md`

### 4. Calculate Velocity

Calculate completed work percentage as a simple velocity proxy.

Use these scripts:
- `scripts/calculate_velocity.py`

Load these references only when needed:
- `references/agile_methodologies.md`
- `references/sprint_planning_guide.md`

### 5. Manage Risks

Track project execution risk and mitigations.

Use these scripts:
- `scripts/manage_risks.py`

Load these references only when needed:
- `references/agile_methodologies.md`
- `references/sprint_planning_guide.md`

## Integration

Inputs expected from upstream:
- `prioritized_features.json`
- `test_plan.json`
- `cicd_plan.json`

Outputs produced for downstream roles:
- `sprint_plan.json`
- `project_status.json`
- `stakeholder_report.md`

Upstream roles:
- `sdlc-pm-product`
- `sdlc-qa`
- `sdlc-devops`

Downstream roles:
- `sdlc-orchestrator`

## Resources

Use `references/` for role-specific guidance, `scripts/` for deterministic execution, and `assets/` for templates, checklists, and output examples.

## Failure Modes

- Stop and request clarification when a required upstream artifact is missing or contradictory.
- Do not hand off vague artifacts; record the open issues inside the output itself.
- When a script output is insufficient, refine the input artifact first instead of guessing.
