---
name: sdlc-ba
description: Business analysis, user-story generation, acceptance-criteria design, BPMN-style process mapping, gap analysis, and business-rule documentation. Use when Codex must convert product artifacts into implementable stories, process models, traceability matrices, or detailed analysis for architecture, development, and testing.
---

# Business Analyst

## Overview

Translate product intent into executable stories, acceptance criteria, process flows, and requirement traceability.

## Workflow

1. Read the latest upstream artifact set and summarize what is known.
2. Detect missing information before generating downstream artifacts.
3. Use the smallest set of references needed for the current task.
4. Run the role-specific scripts instead of rewriting the same structure by hand.
5. Validate the output and package a clean handoff for the next SDLC role.

## Core Workflows

### 1. Analyze Requirements

Analyze requirements for clarity, completeness, and dependency awareness.

Use these scripts:
- `scripts/analyze_requirements.py`

Load these references only when needed:
- `references/requirements_types.md`
- `references/bpmn_standards.md`

### 2. Generate User Stories

Generate user stories and acceptance criteria from product inputs.

Use these scripts:
- `scripts/generate_user_stories.py`

Load these references only when needed:
- `references/requirements_types.md`
- `references/bpmn_standards.md`

### 3. Create Flowcharts

Create Mermaid flowcharts for business processes.

Use these scripts:
- `scripts/create_flowcharts.py`

Load these references only when needed:
- `references/requirements_types.md`
- `references/bpmn_standards.md`

### 4. Gap Analysis

Compare current and target states and list missing capabilities.

Use these scripts:
- `scripts/gap_analysis.py`

Load these references only when needed:
- `references/requirements_types.md`
- `references/bpmn_standards.md`

### 5. Validate Nfr

Validate that non-functional requirements are explicit and testable.

Use these scripts:
- `scripts/validate_nfr.py`

Load these references only when needed:
- `references/requirements_types.md`
- `references/bpmn_standards.md`

## Integration

Inputs expected from upstream:
- `product_prd.md`
- `mvp_scope.json`

Outputs produced for downstream roles:
- `business_analysis.json`
- `user_stories.json`
- `traceability_matrix.json`

Upstream roles:
- `sdlc-pm-product`
- `sdlc-requirements-guru`

Downstream roles:
- `sdlc-arch`
- `sdlc-dev`
- `sdlc-qa`

## Resources

Use `references/` for role-specific guidance, `scripts/` for deterministic execution, and `assets/` for templates, checklists, and output examples.

## Failure Modes

- Stop and request clarification when a required upstream artifact is missing or contradictory.
- Do not hand off vague artifacts; record the open issues inside the output itself.
- When a script output is insufficient, refine the input artifact first instead of guessing.
