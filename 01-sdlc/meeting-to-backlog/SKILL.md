---
name: meeting-to-backlog
description: Convert meeting notes, workshop transcripts, and rough briefs into executable backlog items, decisions, risks, and owner-ready follow-ups. Use when Codex must digest discussion notes and produce epics, stories, questions, or action items suitable for planning or tracker sync.
---

# Meeting To Backlog

## Overview

Transform conversational project input into structured backlog artifacts without losing decisions and risk signals.

## Workflow

1. Start from meeting notes, workshop summaries, or transcript extracts.
2. Run `scripts/meeting_notes_to_backlog.py` to extract epics, stories, risks, decisions, and follow-ups.
3. Load the references only when the team needs a stricter story or decision format.
4. If the result is heading to live trackers, hand it to `delivery-sync` rather than pushing raw notes directly.
5. Keep explicit decisions separate from inferred action items.

## Core Workflow

### Convert Notes Into Backlog Artifacts

Use these scripts:
- `scripts/meeting_notes_to_backlog.py`

Load these references only when needed:
- `references/story_format.md`
- `references/decision_log_schema.md`
- `references/facilitation_signals.md`

## Resources

Use `references/` for structuring rules and `assets/` for smoke inputs and sample outputs.

## Failure Modes

- Do not merge explicit decisions with speculative assumptions.
- Do not invent owners when the notes only mention teams.
- Do not sync discussion notes directly into trackers without normalization.
