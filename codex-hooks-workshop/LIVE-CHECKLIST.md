# Live rehearsal checklist

Record on the presentation machine after project trust and /hooks review. No rows are pre-marked as executed. Use scenario READMEs for exact actions. Fixture checks are separate.

| Scenario | Required evidence | Rehearsed | Notes |
| --- | --- | --- | --- |
| 01 · Startup context | Codex answers staging from hook context. | [ ] | |
| 02 · Command denial | Production is denied; only the staging marker exists. | [ ] | |
| 03 · Tool logging | A new JSONL entry records the completed shell call. | [ ] | |
| 04 · Prompt filtering | First prompt is blocked; the second receives brief explanation guidance. | [ ] | |
| 05 · Permission decisions | PermissionRequest denies the escalation and .demo/write-marker.txt remains absent. | [ ] | |
| 06 · Completion check | The hook detects answer.txt = 41, requests a continuation, and Codex changes it to 42 and runs check.py. | [ ] | |
| 07 · Compaction checkpoint | PreCompact saves a checkpoint; PostCompact reports completion; SessionStart source compact supplies the saved task context. | [ ] | |
| 08 · Subagent lifecycle | Journal contains SubagentStart and SubagentStop with the child identifier; report includes Tests:. | [ ] | |
| 09 · Model request telemetry | PreModelRequest and PostModelRequest record the model and outcome; token usage can be null. | [ ] | |
| 10 · Interruption | A local record contains the interrupted turn ID. | [ ] | |
| 11 · Session end | The session-end marker records reason other. | [ ] | |
| 12 · Tool input rewriting | Codex runs the replacement command and prints Hello, workshop! rather than Hello, default!. | [ ] | |
| 13 · Post-tool feedback | The generated file exists and Codex receives review feedback instead of the original result. | [ ] | |
| 14 · Background execution | Foreground completes while a delayed hook records completion. | [ ] | |
| 15 · File-edit guard | The protected patch is denied; an unrelated patch is allowed. | [ ] | |
| 16 · MCP tool handler | Local check_command returns a denial; .demo/events.jsonl records the decision. | [ ] | |
| 17 · Failure modes | Exit 2 is a policy denial; other modes show a failing hook or unsupported-field report. Fixtures show each response separately. | [ ] | |
| 18 · Large context output | The hook returns 40 bounded synthetic reference lines; with additionalContextLimit 64, Codex should provide a shortened preview and saved-file reference. | [ ] | |
