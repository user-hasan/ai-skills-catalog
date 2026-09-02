---
name: sdlc-qa
description: Quality assurance, test planning, test-case design, automation preparation, performance checks, regression analysis, and defect reporting. Use when Codex must convert stories or implementation notes into test strategy, automated checks, performance expectations, or defect-tracking artifacts before release.
---

# QA Engineer

## Overview

Plan quality strategy, design test cases, map automation, validate performance, and track defects.

## Workflow

1. Read the latest upstream artifact set and summarize what is known.
2. Detect missing information before generating downstream artifacts.
3. Use the smallest set of references needed for the current task.
4. Run the role-specific scripts instead of rewriting the same structure by hand.
5. Validate the output and package a clean handoff for the next SDLC role.

## Core Workflows

### 1. Generate Test Plan

Generate a test plan from user stories and constraints.

Use these scripts:
- `scripts/generate_test_plan.py`

Load these references only when needed:
- `references/test_types.md`
- `references/test_case_design_techniques.md`

### 2. Create Test Cases

Create structured test cases from stories or workflows.

Use these scripts:
- `scripts/create_test_cases.py`

Load these references only when needed:
- `references/test_types.md`
- `references/test_case_design_techniques.md`

### 3. Automate Tests

Map test cases to automation targets and frameworks.

Use these scripts:
- `scripts/automate_tests.py`

Load these references only when needed:
- `references/test_types.md`
- `references/test_case_design_techniques.md`

### 4. Run Performance Test

Create a performance-test plan for endpoints or workflows.

Use these scripts:
- `scripts/run_performance_test.py`

Load these references only when needed:
- `references/test_types.md`
- `references/test_case_design_techniques.md`

### 5. Track Defects

Track open and resolved defects from a defect list.

Use these scripts:
- `scripts/track_defects.py`

Load these references only when needed:
- `references/test_types.md`
- `references/test_case_design_techniques.md`

## Integration

Inputs expected from upstream:
- `user_stories.json`
- `implementation_plan.json`

Outputs produced for downstream roles:
- `test_plan.json`
- `test_cases.json`
- `defect_report.json`

Upstream roles:
- `sdlc-ba`
- `sdlc-dev`
- `sdlc-arch`

Downstream roles:
- `sdlc-devops`
- `sdlc-pm-project`
- `sdlc-orchestrator`

## Resources

Use `references/` for role-specific guidance, `scripts/` for deterministic execution, and `assets/` for templates, checklists, and output examples.

## Failure Modes

- Stop and request clarification when a required upstream artifact is missing or contradictory.
- Do not hand off vague artifacts; record the open issues inside the output itself.
- When a script output is insufficient, refine the input artifact first instead of guessing.
