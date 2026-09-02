---
name: release-manager
description: Release-planning skill for changelog drafting, semantic-version suggestion, release-note packaging, version tagging, draft-release preparation, and rollback-readiness checks. Use when the user asks for release notes, changelog updates, version bump advice, release packaging, draft release work, ship readiness, or rollback planning before deployment.
---

# Release Manager

## Overview

Bundle release changes into a versioned package that can be reviewed before deployment.

## Workflow

1. Collect the release scope from PRs, issue lists, or change summaries.
2. Run `scripts/build_release_bundle.py` to classify the changes and suggest the version bump.
3. Load the release references only when the repository has stricter labeling or deployment policy.
4. If the user wants a live GitHub release draft, prefer `gh release` after the notes are reviewed.
5. Keep rollback steps visible in the same artifact as the notes.

## Core Workflow

### Build A Release Bundle

Use these scripts:
- `scripts/build_release_bundle.py`

Load these references only when needed:
- `references/release_signal_rules.md`
- `references/changelog_structure.md`
- `references/rollback_policy.md`

## Resources

Use `references/` for policy rules and `assets/` for smoke inputs and sample bundles.

## Failure Modes

- Do not suggest a patch release when the changes include explicit breaking behavior.
- Do not draft release notes from unlabeled work without a manual review pass.
- Do not hide rollback prerequisites outside the final bundle.
