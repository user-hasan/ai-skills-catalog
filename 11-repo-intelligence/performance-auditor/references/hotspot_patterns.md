# Hotspot Patterns

- Slow tests: `time.sleep`, `sleep(`, or deliberately delayed command invocations.
- Loop-scoped I/O: reading files, network calls, or shell commands inside loops.
- Nested loops: repeated O(n^2) style blocks that should be reviewed when they sit on hot paths.
- Oversized hotspots: files with high line counts or central orchestration roles.
- Expensive commands: explicit build or test commands that exceed the threshold provided in the request.
