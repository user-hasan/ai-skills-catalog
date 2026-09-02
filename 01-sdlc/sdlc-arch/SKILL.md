---
name: sdlc-arch
description: Software architecture, ADR generation, pattern selection, tradeoff analysis, non-functional requirement mapping, security review, and scalability planning. Use when Codex must choose a system design, compare architecture patterns, record key decisions, or prove that an architecture satisfies security, scale, and operational targets before build-out.
---

# Architect

## Overview

Design system structure, record architectural decisions, choose technologies, and map non-functional goals to architecture patterns.

## Workflow

1. Read the latest upstream artifact set and summarize what is known.
2. Detect missing information before generating downstream artifacts.
3. Use the smallest set of references needed for the current task.
4. Run the role-specific scripts instead of rewriting the same structure by hand.
5. Validate the output and package a clean handoff for the next SDLC role.

## Core Workflows

### 1. Evaluate Architecture

Evaluate candidate architectures against system constraints.

Use these scripts:
- `scripts/evaluate_architecture.py`

Load these references only when needed:
- `references/architectural_patterns.md`
- `references/technology_radar.md`

### 2. Generate Adhoc

Generate ADR-style decision notes from architecture findings.

Use these scripts:
- `scripts/generate_adhoc.py`

Load these references only when needed:
- `references/architectural_patterns.md`
- `references/technology_radar.md`

### 3. Calculate Tradeoffs

Compare architecture options using weighted tradeoff scoring.

Use these scripts:
- `scripts/calculate_tradeoffs.py`

Load these references only when needed:
- `references/architectural_patterns.md`
- `references/technology_radar.md`

### 4. Validate Patterns

Check whether selected patterns cover the required qualities.

Use these scripts:
- `scripts/validate_patterns.py`

Load these references only when needed:
- `references/architectural_patterns.md`
- `references/technology_radar.md`

### 5. Create Diagrams

Create Mermaid diagrams for architectural context and flows.

Use these scripts:
- `scripts/create_diagrams.py`

Load these references only when needed:
- `references/architectural_patterns.md`
- `references/technology_radar.md`

## Integration

Inputs expected from upstream:
- `business_analysis.json`
- `requirements_spec.yaml`

Outputs produced for downstream roles:
- `architecture_review.json`
- `architecture_adrs.md`
- `c4_context.md`

Upstream roles:
- `sdlc-ba`
- `sdlc-requirements-guru`

Downstream roles:
- `sdlc-dev`
- `sdlc-devops`
- `sdlc-qa`

## Resources

Use `references/` for role-specific guidance, `scripts/` for deterministic execution, and `assets/` for templates, checklists, and output examples.

## Failure Modes

- Stop and request clarification when a required upstream artifact is missing or contradictory.
- Do not hand off vague artifacts; record the open issues inside the output itself.
- When a script output is insufficient, refine the input artifact first instead of guessing.
