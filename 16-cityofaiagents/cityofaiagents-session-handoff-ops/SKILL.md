---
name: cityofaiagents-session-handoff-ops
description: Mirrored CityOfAIAgents session handoff skill for split-credit behavior, user-switch timer boundaries, and regression evidence.
---

# session-handoff-ops

## Purpose
Support session-handoff tasks and workflows.

## Use When
- Split-credit handoff behavior must be verified.
- User-switch timer continuity boundaries need tracing.
- Regression evidence is needed for session handoff ledger items.

## Guidance
- Treat the internal CityOfAIAgents skill artifact as the source of truth.
- Preserve domain semantics around active sessions, historical state, and handoff ownership.
- Keep evidence tied to the exact session or ledger item being inspected.
- Supported tag: session-handoff

## Internal Metadata
- artifact_id: SKL-0007
- revision: 2
