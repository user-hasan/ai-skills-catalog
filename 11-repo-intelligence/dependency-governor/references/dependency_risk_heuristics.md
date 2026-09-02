# Dependency Risk Heuristics

- Prefer explicit baseline maps over vague “looks old” statements.
- Flag missing lockfiles separately from outdated package versions.
- Treat unpinned dependencies as medium risk unless they sit on a critical path.
- Distinguish ecosystem-specific signals such as `package-lock.json` versus `poetry.lock`.
- Always recommend the next verification step, not just the problem statement.
