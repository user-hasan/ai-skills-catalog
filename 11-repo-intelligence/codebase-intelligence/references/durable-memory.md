# Durable Memory

This skill uses project-local artifacts as durable memory because internal Codex memory is not writable from a skill workflow here.

## Files

- `project_memory.md`
  Compact session handoff for future agents.
- `project_intelligence.md`
  Human-readable architecture report.
- `project_intelligence.json`
  Structured machine-readable analysis.

## Usage Pattern

1. If the folder exists, read `project_memory.md` before starting a new analysis session.
2. Refresh the bundle when the repository meaningfully changes.
3. Keep the bundle inside `.codex-project-intel/` so it remains easy to find and safe to ignore in normal source browsing.

## What Belongs In Durable Memory

- major runtime entrypoints
- top-level module boundaries
- important file relationships
- framework and dependency signals
- architectural risks and open questions

## What Does Not Belong

- secrets
- access tokens
- private credentials
- speculative claims that were not backed by the current repo state
