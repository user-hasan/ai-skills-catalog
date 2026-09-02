---
name: repo-intake-triage
description: Repository intake triage for GitHub issues, pull requests, bug reports, and feature requests, including readiness checks, missing-context detection, label suggestions, and routing guidance. Use when the user asks to triage an issue, triage a PR, classify a bug report, route a feature request, suggest labels, check definition-of-ready, or prepare a clean handoff into planning or implementation.
---

# Repo Intake Triage

## Overview

Normalize new repository work, detect what is missing, and route the item into the right delivery path before engineering time is spent.

## Workflow

1. Capture the issue, PR, or backlog item context from export files or a live GitHub session.
2. If the user wants live repository context, prefer `gh issue view`, `gh pr view`, `gh label list`, and `gh repo view` before guessing.
3. Run `scripts/triage_repo_item.py` on the normalized input to classify the work and identify missing context.
4. Use the references only when the route is unclear or the repository uses stricter intake gates.
5. When the user wants labels, comments, or issue edits applied, confirm the exact repo and item before changing GitHub state.

## Core Workflow

### Triage A Repository Item

Use these scripts:
- `scripts/triage_repo_item.py`

Load these references only when needed:
- `references/triage_matrix.md`
- `references/github_cli_workflow.md`
- `references/definition_of_ready.md`

## Resources

Use `references/` for triage rules and `assets/` for smoke inputs and expected outputs.

## Failure Modes

- Do not treat missing reproduction steps as implementation-ready bug work.
- Do not auto-assign security or production incidents to a generic backlog bucket.
- Do not mutate GitHub state until the target repository and item number are explicit.
