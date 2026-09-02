---
name: security-gate
description: Security-review skill for scanner finding triage, CVE and dependency-review analysis, code-scanning and secret-scanning review, release gating, remediation ordering, and owner routing. Use when the user asks about security findings, code scanning, dependency review, secret scanning, vulnerability triage, release blocking security issues, or remediation priority.
---

# Security Gate

## Overview

Turn raw scanner output into a release decision, remediation order, and owner-ready action list.

## Workflow

1. Gather structured findings from code scanning, dependency review, secret scanning, or manual review.
2. Run `scripts/triage_security_findings.py` to compute the gate status and ranked findings.
3. Load the references when severity definitions or scanner semantics are unclear.
4. If the user wants repository changes, prefer security fixes before labels or reporting polish.
5. Keep the gate decision and owners explicit so release work can stop safely when needed.

## Core Workflow

### Triage Findings

Use these scripts:
- `scripts/triage_security_findings.py`

Load these references only when needed:
- `references/severity_matrix.md`
- `references/github_scanning_workflow.md`
- `references/remediation_order.md`

## Resources

Use `references/` for security policy rules and `assets/` for smoke inputs and expected outputs.

## Failure Modes

- Do not pass a release with unresolved critical findings.
- Do not collapse dependency noise and exploitable vulnerabilities into the same priority bucket.
- Do not assign security work without a named technical owner.
