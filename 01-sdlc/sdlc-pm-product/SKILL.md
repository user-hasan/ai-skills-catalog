---
name: sdlc-pm-product
description: Product management, PRD creation, MVP scoping, backlog prioritization, OKR planning, and market analysis for delivery-ready products. Use when Codex must convert requirement artifacts into a product strategy, release scope, roadmap, measurable goals, or prioritization decisions before business analysis and implementation.
---

# Product Manager

## Overview

Turn validated requirements into a product strategy, release scope, backlog, and measurable product success plan.

## Workflow

1. Read the latest upstream artifact set and summarize what is known.
2. Detect missing information before generating downstream artifacts.
3. Use the smallest set of references needed for the current task.
4. Run the role-specific scripts instead of rewriting the same structure by hand.
5. Validate the output and package a clean handoff for the next SDLC role.

## Core Workflows

### 1. Generate Prd

Generate a PRD from requirement artifacts.

Use these scripts:
- `scripts/generate_prd.py`

Load these references only when needed:
- `references/prd_template.md`
- `references/okr_guidelines.md`

### 2. Calculate Mvp Scope

Rank candidate features and identify the MVP cut line.

Use these scripts:
- `scripts/calculate_mvp_scope.py`

Load these references only when needed:
- `references/prd_template.md`
- `references/okr_guidelines.md`

### 3. Prioritize Features

Prioritize backlog items using weighted product heuristics.

Use these scripts:
- `scripts/prioritize_features.py`

Load these references only when needed:
- `references/prd_template.md`
- `references/okr_guidelines.md`

### 4. Track Okrs

Track OKR progress using structured status items.

Use these scripts:
- `scripts/track_okrs.py`

Load these references only when needed:
- `references/prd_template.md`
- `references/okr_guidelines.md`

### 5. Validate Product Vision

Check whether the product vision is specific, measurable, and user-centered.

Use these scripts:
- `scripts/validate_product_vision.py`

Load these references only when needed:
- `references/prd_template.md`
- `references/okr_guidelines.md`

## Integration

Inputs expected from upstream:
- `requirements_spec.yaml`
- `project_understanding_report.md`

Outputs produced for downstream roles:
- `product_prd.md`
- `mvp_scope.json`
- `product_okrs.json`

Upstream roles:
- `sdlc-requirements-guru`

Downstream roles:
- `sdlc-ba`
- `sdlc-pm-project`
- `sdlc-dev`

## Resources

Use `references/` for role-specific guidance, `scripts/` for deterministic execution, and `assets/` for templates, checklists, and output examples.

## Failure Modes

- Stop and request clarification when a required upstream artifact is missing or contradictory.
- Do not hand off vague artifacts; record the open issues inside the output itself.
- When a script output is insufficient, refine the input artifact first instead of guessing.
