---
name: sdlc-devops
description: DevOps planning, CI/CD pipeline generation, infrastructure-as-code guidance, observability, secrets management, security scanning, and rollback preparation. Use when Codex must turn architecture and QA outputs into deployable delivery workflows, infrastructure plans, operational controls, or production readiness artifacts.
---

# DevOps Engineer

## Overview

Prepare delivery automation, infrastructure plans, monitoring, secret handling, security scanning, and rollback procedures.

## Workflow

1. Read the latest upstream artifact set and summarize what is known.
2. Detect missing information before generating downstream artifacts.
3. Use the smallest set of references needed for the current task.
4. Run the role-specific scripts instead of rewriting the same structure by hand.
5. Validate the output and package a clean handoff for the next SDLC role.

## Core Workflows

### 1. Setup Cicd

Generate a CI/CD plan and starter snippet for the chosen platform.

Use these scripts:
- `scripts/setup_cicd.py`

Load these references only when needed:
- `references/cicd_patterns.md`
- `references/infrastructure_tools.md`

### 2. Infrastructure As Code

Plan infrastructure resources and environment strategy.

Use these scripts:
- `scripts/infrastructure_as_code.py`

Load these references only when needed:
- `references/cicd_patterns.md`
- `references/infrastructure_tools.md`

### 3. Monitor Deployment

Describe deployment monitoring dashboards and alerts.

Use these scripts:
- `scripts/monitor_deployment.py`

Load these references only when needed:
- `references/cicd_patterns.md`
- `references/infrastructure_tools.md`

### 4. Manage Secrets

Generate a secret inventory and rotation plan.

Use these scripts:
- `scripts/manage_secrets.py`

Load these references only when needed:
- `references/cicd_patterns.md`
- `references/infrastructure_tools.md`

### 5. Log Analyzer

Summarize logs and highlight high-signal failures.

Use these scripts:
- `scripts/log_analyzer.py`

Load these references only when needed:
- `references/cicd_patterns.md`
- `references/infrastructure_tools.md`

## Integration

Inputs expected from upstream:
- `architecture_review.json`
- `test_plan.json`

Outputs produced for downstream roles:
- `cicd_plan.json`
- `infrastructure_plan.json`
- `operations_readiness.json`

Upstream roles:
- `sdlc-arch`
- `sdlc-qa`
- `sdlc-dev`

Downstream roles:
- `sdlc-pm-project`
- `sdlc-orchestrator`

## Resources

Use `references/` for role-specific guidance, `scripts/` for deterministic execution, and `assets/` for templates, checklists, and output examples.

## Failure Modes

- Stop and request clarification when a required upstream artifact is missing or contradictory.
- Do not hand off vague artifacts; record the open issues inside the output itself.
- When a script output is insufficient, refine the input artifact first instead of guessing.
