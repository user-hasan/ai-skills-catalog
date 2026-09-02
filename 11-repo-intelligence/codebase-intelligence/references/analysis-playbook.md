# Analysis Playbook

Use this playbook after the baseline analyzer has produced artifacts.

## What To Read First

1. `project_memory.md` for the condensed view.
2. `project_intelligence.md` for architecture, entrypoints, and risks.
3. Only then inspect source files chosen by the report.

## High-Value Follow-Ups

- Open the declared entrypoints before reading random modules.
- Inspect files with the highest inbound references to find orchestration centers.
- Inspect files with the highest outbound references to find coupling hotspots.
- Review any cross-directory edges that bridge API, domain, persistence, and UI boundaries.
- Review strongly connected components when the report flags cycles.

## Enterprise Repo Heuristics

- Monorepos usually need package-by-package reading after the global scan.
- Large service repos often have separate runtime, jobs, deployment, and test entrypaths.
- Configuration files are often as important as source files in distributed systems.
- A project with weak test coverage or many oversized files usually needs manual risk review before modification.

## When To Refresh

Refresh the intelligence bundle after:

- dependency or framework changes
- directory moves
- build pipeline changes
- service boundary changes
- large feature merges
