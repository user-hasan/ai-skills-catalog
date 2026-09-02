# Verification Mapping

- Start from the explicit target files, then expand to reverse dependencies.
- Always search for likely affected tests after the impacted file set is known.
- Promote command-level follow-up checks when the original findings came from failing commands.
- Keep the verification checklist scoped to the change surface instead of re-running the entire repository blindly.
