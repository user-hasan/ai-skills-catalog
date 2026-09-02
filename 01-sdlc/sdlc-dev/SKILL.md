---
name: sdlc-dev
description: Software development, project scaffolding, coding standards enforcement, code review support, unit-test generation, coverage analysis, and API documentation. Use when Codex must turn architecture or backlog artifacts into implementation structure, quality conventions, review feedback, or testable development packages.
---

# Developer

## Overview

Prepare implementation structures, coding standards, review loops, unit tests, and API documentation for engineering delivery.

## Workflow

1. Read the latest upstream artifact set and summarize what is known.
2. Detect missing information before generating downstream artifacts.
3. Use the smallest set of references needed for the current task.
4. Run the role-specific scripts instead of rewriting the same structure by hand.
5. Validate the output and package a clean handoff for the next SDLC role.

## Core Workflows

### 1. Generate Code Structure

Generate a language-specific project structure plan or scaffold.

Use these scripts:
- `scripts/generate_code_structure.py`

Load these references only when needed:
- `references/design_patterns.md`
- `references/solid_principles.md`

### 2. Enforce Coding Standards

Validate that implementation notes align with coding standards.

Use these scripts:
- `scripts/enforce_coding_standards.py`

Load these references only when needed:
- `references/design_patterns.md`
- `references/solid_principles.md`

### 3. Run Code Review

Apply a structured code-review checklist to code snippets or review notes.

Use these scripts:
- `scripts/run_code_review.py`

Load these references only when needed:
- `references/design_patterns.md`
- `references/solid_principles.md`

### 4. Generate Unit Tests

Generate unit-test cases from user stories or function lists.

Use these scripts:
- `scripts/generate_unit_tests.py`

Load these references only when needed:
- `references/design_patterns.md`
- `references/solid_principles.md`

### 5. Calculate Coverage

Calculate simple coverage progress from status items.

Use these scripts:
- `scripts/calculate_coverage.py`

Load these references only when needed:
- `references/design_patterns.md`
- `references/solid_principles.md`

## Integration

Inputs expected from upstream:
- `architecture_review.json`
- `user_stories.json`

Outputs produced for downstream roles:
- `implementation_plan.json`
- `unit_test_plan.json`
- `api_docs_outline.md`

Upstream roles:
- `sdlc-arch`
- `sdlc-ba`
- `sdlc-pm-product`

Downstream roles:
- `sdlc-qa`
- `sdlc-devops`

## Resources

Use `references/` for role-specific guidance, `scripts/` for deterministic execution, and `assets/` for templates, checklists, and output examples.

## Failure Modes

- Stop and request clarification when a required upstream artifact is missing or contradictory.
- Do not hand off vague artifacts; record the open issues inside the output itself.
- When a script output is insufficient, refine the input artifact first instead of guessing.
