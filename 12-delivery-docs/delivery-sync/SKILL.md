---
name: delivery-sync
description: Sync project-delivery artifacts into live tracking systems such as Linear, GitHub Projects, and Notion by translating local backlog, sprint, and status outputs into tracker-ready payloads. Use when Codex must bridge `sdlc-pm-project` outputs into actual tracking tools or prepare a safe sync plan before writing live state.
---

# Delivery Sync

## Overview

Turn local delivery artifacts into tracker-ready updates before touching Linear, GitHub Projects, or Notion.

## Workflow

1. Start from `project_status.json`, `sprint_plan.json`, or backlog-style artifacts rather than free-form notes.
2. Run `scripts/build_tracker_sync_payload.py` to normalize the delivery state and generate tracker-specific payloads.
3. For live sync, prefer the connected `Linear` and `Notion` tools in this environment, and use `gh` for GitHub repositories.
4. Apply the generated payload only after the target workspace, project, or repository is explicit.
5. Keep the sync summary in the thread so the next run can see what changed.

## Core Workflow

### Build Tracker Payloads

Use these scripts:
- `scripts/build_tracker_sync_payload.py`

Load these references only when needed:
- `references/tracker_mapping.md`
- `references/live_sync_workflow.md`
- `references/field_conventions.md`

## Resources

Use `references/` for tracker-specific field rules and `assets/` for smoke inputs and expected payloads.

## Failure Modes

- Do not push ambiguous owners or dates into live trackers.
- Do not overwrite richer tracker fields with weaker local artifacts.
- Do not create duplicate tasks when a stable external identifier already exists.
