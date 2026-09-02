# OpenAI Runtime Update Signals

Use this reference when an approved OpenAI or Codex source changes runtime guidance.

## Signal Types

- `tool-surface`: built-in tools, hosted tools, shell tools, computer-use tools, tool search, or hosted skills are part of the guidance.
- `mcp-approval`: a source describes remote MCP, connector approval, `mcp_approval_request`, or user approval before a tool call.
- `background-mode`: a source describes asynchronous background responses, polling, cancellation, retention, or ZDR limits.
- `structured-output`: a source recommends schema-bound output, Structured Outputs, or replacing loose JSON mode with stricter schema adherence.
- `source-discipline`: a source changes official-source preference, provider-hosted MCP guidance, or restrictions around non-official material.

## Update Request Notes

When these signals are present, generated update requests should include optional runtime notes:

- `approval_required`: true when MCP or connector approval is part of the workflow.
- `polling_required`: true when background responses or async status checks are needed.
- `schema_adherence_required`: true when Structured Outputs are central to the recommendation.
- `official_source_required`: true for OpenAI/Codex guidance that should not be sourced from blogs or secondary summaries.
