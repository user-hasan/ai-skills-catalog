# Registry Policy

- `~/.agents/skills` is the authoring workspace.
- `~/.codex/skills` is the publish target for discoverability in this environment.
- `superpowers` remains an external bundle and should not be duplicated blindly.
- authored validation freshness is part of registry health; a report is stale if any authored skill directory is newer than `sdlc-system/AUTHORED_VALIDATION_REPORT.md`.
- missing `agents/openai.yaml` metadata and unpublished authored skills should be surfaced directly in the audit output rather than inferred from downstream failures.
