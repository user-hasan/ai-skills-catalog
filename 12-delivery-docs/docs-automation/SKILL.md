---
name: docs-automation
description: Documentation automation skill for keeping README, spec, runbook, status, and release docs aligned with current delivery artifacts. Use when Codex must detect documentation drift, build a docs backlog, or prepare a precise update plan before editing project documentation.
---

# Docs Automation

## Overview

Map project changes to the documentation surfaces that must be updated so the repository does not drift away from reality.

## Workflow

1. Start from release, sprint, architecture, or support artifacts instead of rewriting docs from memory.
2. Run `scripts/build_docs_sync_plan.py` to generate a docs-update backlog and ownership map.
3. Read the references only when the right source of truth or runbook structure is unclear.
4. Apply documentation edits only after the update plan is stable.
5. Keep operational docs, stakeholder status, and developer docs separated in the final plan.

## Core Workflow

### Build A Docs Sync Plan

Use these scripts:
- `scripts/build_docs_sync_plan.py`

Load these references only when needed:
- `references/source_of_truth.md`
- `references/runbook_patterns.md`
- `references/update_triggers.md`

## Resources

Use `references/` for documentation policy and `assets/` for smoke inputs and sample outputs.

## Failure Modes

- Do not update README while leaving runbooks and status artifacts stale.
- Do not treat generated summaries as a replacement for exact operational steps.
- Do not change docs blindly when the related code or release artifact is missing.
