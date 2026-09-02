---
name: security-remediator
description: Convert confirmed security-gate findings, vulnerabilities, dependency advisories, secret-scanning alerts, and security risks into scoped remediation plans. Use when Codex needs a governed security fix path after security-gate, with change-impact and regression checks before any code or dependency edits.
---

# Security Remediator

## Overview

Prepare a safe security remediation plan from confirmed security evidence and route it into repair and verification artifacts.

## Workflow

1. Read security-gate output, security findings, risks, and dependency evidence.
2. Reject work without a confirmed security finding or documented risk.
3. Prioritize KEV-listed or actively exploited evidence before general hardening.
4. Map remediation planning to Secure by Design, memory-safety, ASVS, GHSA, and NVD evidence when those signals are present.
5. Build a scoped remediation plan with required impact mapping and regression checks.
6. Write `security/security_remediation_plan.json` and mirror planned work into `remediation/repair_plan.json`.
7. Leave live secrets and production credentials outside the editable scope.

## Core Workflow

Run:

```powershell
python scripts/run_security_remediator.py --input assets/inputs/sample_input.json --output assets/outputs/sample_output.json
```

Primary outputs:

- `security/security_remediation_plan.json`
- `remediation/repair_plan.json`

## References

Load when needed:

- `references/wave2_contract.md`
- `references/security_prioritization.md`

## Failure Modes

- Do not perform broad dependency upgrades unless the safe target version is explicit.
- Do not modify secrets, credentials, or production settings.
- Do not bypass change-impact-mapper or regression-guard for executable fixes.
- Do not infer active exploitation from CVE presence alone without KEV, advisory, incident, or runtime evidence.
- Do not treat ASVS mapping as proof of remediation; it is a verification planning aid.
