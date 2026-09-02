---
name: sdlc-requirements-guru
description: Requirements discovery, scope clarification, ambiguity detection, readiness checks, and risk screening for software projects. Use when Codex starts a new product, receives incomplete requirements, needs a discovery questionnaire, wants improvement ideas, or must produce project-understanding, improvement, and requirements artifacts before planning, architecture, or implementation.
---

# Requirements Guru

## Overview

Act as the mandatory front door for new initiatives by clarifying scope, exposing ambiguity, scoring readiness, and producing structured requirement artifacts.

## Workflow

1. Read the latest upstream artifact set and summarize what is known.
2. Detect missing information before generating downstream artifacts.
3. Use the smallest set of references needed for the current task.
4. Run the role-specific scripts instead of rewriting the same structure by hand.
5. Validate the output and package a clean handoff for the next SDLC role.

## Core Workflows

### 1. Analyze Project Completeness

Measure how complete and implementation-ready a project brief is.

Use these scripts:
- `scripts/analyze_project_completeness.py`

Load these references only when needed:
- `references/requirement_categories.md`
- `references/question_bank_by_domain.md`

### 2. Generate Questionnaire

Generate a discovery questionnaire tailored to the current project context.

Use these scripts:
- `scripts/generate_questionnaire.py`

Load these references only when needed:
- `references/requirement_categories.md`
- `references/question_bank_by_domain.md`

### 3. Check Ambiguities

Detect ambiguous, underspecified, or missing requirement categories.

Use these scripts:
- `scripts/check_ambiguities.py`

Load these references only when needed:
- `references/requirement_categories.md`
- `references/question_bank_by_domain.md`

### 4. Suggest Improvements

Suggest architectural, process, feature, quality, and cost improvements.

Use these scripts:
- `scripts/suggest_improvements.py`

Load these references only when needed:
- `references/requirement_categories.md`
- `references/question_bank_by_domain.md`

### 5. Calculate Risk Score

Score delivery risk and list concrete mitigation actions.

Use these scripts:
- `scripts/calculate_risk_score.py`

Load these references only when needed:
- `references/requirement_categories.md`
- `references/question_bank_by_domain.md`

## Integration

Inputs expected from upstream:
- `User brief`
- `existing notes`
- `legacy system context`
- `business goals`

Outputs produced for downstream roles:
- `project_understanding_report.md`
- `improvement_report.md`
- `requirements_spec.yaml`

Upstream roles:
- `user-request`

Downstream roles:
- `sdlc-pm-product`
- `sdlc-ba`
- `sdlc-arch`

## Resources

Use `references/` for role-specific guidance, `scripts/` for deterministic execution, and `assets/` for templates, checklists, and output examples.

## Failure Modes

- Stop and request clarification when a required upstream artifact is missing or contradictory.
- Do not hand off vague artifacts; record the open issues inside the output itself.
- When a script output is insufficient, refine the input artifact first instead of guessing.
