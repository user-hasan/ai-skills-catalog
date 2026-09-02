# GitHub CLI Workflow

- Inspect an issue with `gh issue view <number> --json title,body,labels,assignees,state,url`.
- Inspect a PR with `gh pr view <number> --json title,body,labels,reviewRequests,mergeStateStatus,files`.
- List labels with `gh label list`.
- Only write state after the user confirms the exact repository and item.
