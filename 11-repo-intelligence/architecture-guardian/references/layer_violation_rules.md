# Layer Violation Rules

- Express forbidden dependencies as prefixes such as `src/ui -> src/infra`.
- Prefer a small explicit rule set over broad assumptions.
- Always attach the exact source and target files that crossed the layer boundary.
- Keep cycles separate from simple boundary leaks because the mitigations differ.
- Central hub findings should mention fan-in and fan-out counts.
