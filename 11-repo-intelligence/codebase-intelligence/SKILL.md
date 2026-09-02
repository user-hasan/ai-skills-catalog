---
name: codebase-intelligence
description: Deep repository and architecture analysis for large or complex software projects, including framework detection, entrypoint mapping, dependency tracing, file-to-file relationships, module boundaries, hotspot discovery, and durable project intelligence artifacts. Use when the user asks to understand a codebase, analyze project structure, map file relationships, audit architecture, study a large repository before implementation, or preserve reusable project understanding for future Codex runs.
---

# Codebase Intelligence

## Overview

Build a reliable understanding of an unfamiliar codebase before implementation or review starts. This skill generates a reusable project intelligence bundle so later Codex runs can reload the current architecture quickly instead of rediscovering it from scratch.

## Workflow

1. Start from the project root or the exact service/package the user wants analyzed.
2. If `.codex-project-intel/project_memory.md` already exists, read it first to understand prior findings and then refresh it if the repository changed.
3. Run `scripts/analyze_codebase.py` before making architectural claims.
4. Use the generated report to decide where deeper manual reading is needed: entrypoints, central modules, cross-directory edges, cycles, and oversized files.
5. Keep all durable analysis inside `.codex-project-intel/` unless the user explicitly wants another location.

## Durable Memory

Codex skills cannot write to the internal memory store directly from here. Treat the project-local artifacts below as the durable memory shared across sessions and agents:

- `.codex-project-intel/project_memory.md`
- `.codex-project-intel/project_intelligence.md`
- `.codex-project-intel/project_intelligence.json`

Future Codex runs should read `project_memory.md` first, then open the fuller report only when more detail is required.

## Core Workflow

### Analyze A Repository

Run:

```powershell
python scripts/analyze_codebase.py "C:\path\to\repo"
```

Default output is written under:

```text
<repo>/.codex-project-intel/
```

The analyzer produces:

- `project_intelligence.json` for structured downstream tooling
- `project_intelligence.md` for human-readable architecture review
- `project_memory.md` for compact future-session context

### Refresh Existing Intelligence

Run again after major repository changes:

```powershell
python scripts/analyze_codebase.py "C:\path\to\repo" --output-dir ".codex-project-intel"
```

### Deep-Dive After Baseline Analysis

After the baseline run:

1. Read `project_memory.md` first.
2. Read `project_intelligence.md` for entrypoints, central modules, and risks.
3. Open only the files that the graph identifies as important or ambiguous.
4. Keep follow-up analysis consistent with the saved intelligence bundle so later agents can reuse it.

## References

Load these only when needed:

- `references/analysis-playbook.md`
- `references/durable-memory.md`

## Failure Modes

- Do not claim codebase understanding before running the analyzer or reading an existing memory artifact.
- Do not treat vendor, generated, cache, or build directories as first-class architecture unless the user explicitly asks for them.
- Do not overwrite artifacts outside `.codex-project-intel/` without a direct request.
- Do not confuse project-local durable memory with Codex's internal memory store; this skill persists reusable understanding in the repository itself.
