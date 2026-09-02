# Scoped Repair Policy

- Findings and verification requirements are prerequisites for any applied edit.
- Declarative edits must be explicit and file-bounded.
- Dry-run mode is the default and should still emit a repair plan.
- Verification remains mandatory after any applied edit, even if the edit itself was deterministic.
