---
name: skill-knowledge-updater
description: Gather new skill-relevant knowledge from approved official sources, classify the signal, and convert it into a scoped skill update request. Use when the user asks to refresh a skill from current documentation, advisories, or official guidance without editing the skill directly.
---

# Skill Knowledge Updater

## Overview

Collect current knowledge from a strict allowlist and translate it into a clean update request. This skill does not edit the target skill; it prepares the evidence and the proposed scope for the next stage.

## Workflow

1. Identify the target skill and update category.
2. Validate every source URL against the strict allowlist.
3. Prefer OpenAI Docs MCP or official OpenAI documentation for OpenAI and Codex runtime guidance.
4. Gather evidence and classify each source into signal types, including tool-surface, background-mode, Structured Outputs, and MCP approval signals when present.
5. Produce an update request that stays scoped to the target skill and records runtime approval, polling, and source-discipline notes when relevant.
6. Hand the request to `skill-update-governor` for review.

## Core Workflow

### Collect Skill Update Intelligence

Run:

```powershell
python scripts/collect_skill_update_intelligence.py --input assets/inputs/sample_input.json --output assets/outputs/sample_update_request.json
```

Primary outputs:
- `source_evidence.json`
- `update_intelligence.md`
- `skill_update_request.json`

## References

Load when needed:
- `references/source_classification.md`
- `references/strict_allowlist_rules.md`
- `references/openai_runtime_update_signals.md`

## Failure Modes

- Do not browse outside the configured allowlist.
- Do not turn new evidence into code changes directly.
- Do not treat generic blog content or unsourced discussion as update evidence.
- Do not treat MCP tool calls that require approval as equivalent to approval-free local evidence.
- Do not recommend background-mode use without preserving polling and retention caveats.
