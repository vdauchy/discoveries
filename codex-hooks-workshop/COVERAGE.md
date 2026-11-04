# Supported hook coverage

Reference: [official release-behavior guide](https://learn.chatgpt.com/docs/hooks), checked 2026-11-04. Local reference binary: **codex-cli 0.166.0**. All 14 documented event names also occur in the installed CLI generated ManagedHooksRequirements schema; see reference/support-snapshot.json. A schema match is not a live execution test.

| Event | Matcher | Main supported effect | Demo(s) |
| --- | --- | --- | --- |
| `SessionStart` | source: startup / resume / clear / compact / fork | Add developer context | [01](01-session-context/README.md), [07](07-compaction/README.md), [18](18-large-context/README.md) |
| `SessionEnd` | reason: other | Advisory bookkeeping only | [11](11-session-end/README.md) |
| `UserPromptSubmit` | ignored | Add context or reject prompt | [04](04-prompt-filter/README.md) |
| `PreToolUse` | tool name and aliases | Deny, add context, or rewrite supported call | [02](02-command-guard/README.md), [12](12-input-rewrite/README.md), [15](15-edit-guard/README.md), [16](16-mcp-handler/README.md), [17](17-failure-modes/README.md) |
| `PermissionRequest` | tool name and aliases | Allow, deny, or leave approval unchanged | [05](05-permission-request/README.md) |
| `PostToolUse` | tool name and aliases | Add context or replace feedback; cannot undo action | [03](03-tool-log/README.md), [13](13-post-tool-feedback/README.md), [14](14-background-hook/README.md) |
| `PreCompact` | trigger: manual / auto | Observe; continue:false stops before compaction | [07](07-compaction/README.md) |
| `PostCompact` | trigger: manual / auto | Observe; continue:false stops after compaction | [07](07-compaction/README.md) |
| `SubagentStart` | agent_type | Add child context; continue:false does not stop start | [08](08-subagent-lifecycle/README.md) |
| `SubagentStop` | agent_type | Continue child flow; continue:false overrides continuation | [08](08-subagent-lifecycle/README.md) |
| `PreModelRequest` | ignored | Diagnostics only | [09](09-model-requests/README.md) |
| `PostModelRequest` | ignored | Diagnostics only | [09](09-model-requests/README.md) |
| `Stop` | ignored | Request another turn; continue:false overrides continuation | [06](06-stop-check/README.md) |
| `Interrupt` | ignored | Advisory; cannot prevent interruption or restart | [10](10-interrupt/README.md) |

## Handler coverage

| Handler | Status in the referenced CLI | Coverage |
| --- | --- | --- |
| command | Supported; receives JSON stdin | All labs except 16 |
| mcp_tool | Supported; existing connection required | Lab 16, local stdio server |
| prompt / agent | Parsed but skipped | Reference only; not presented as working demos |

## Tool coverage and boundaries

- Shell execution, including exec_command, matches Bash. A later write_stdin completion can deliver PostToolUse for the original command; polling/input does not rerun PreToolUse.
- apply_patch matches its own name and Edit/Write aliases. The event still reports apply_patch. Lab 15 covers that path.
- MCP tools match their canonical MCP tool name; other local function tools match their names. spawn_agent also matches Agent.
- Hosted tools such as WebSearch do not use local tool hooks. Some specialized paths opt out. These demos do not establish a complete security boundary.
- A PostToolUse block/exit 2 replaces feedback after execution. In code mode it rejects the nested tool promise. continue:false replaces model-facing feedback without that rejection.

## Variations beyond event names

| Behavior | Implementation or reference |
| --- | --- |
| JSON context output | 01, 04, 07, 08 |
| Explicit deny and allow / abstain | 02, 05 |
| Rewrite arguments | 12 |
| Post-execution feedback | 13 |
| Background scheduling | 14 |
| Large context spilling | 18 |
| Exit 2 vs failure, invalid output, unsupported field, timeout | 17 |
| Inline TOML | reference/inline-hooks.toml (inactive example) |
| Plugin packaging and environment variables | reference/plugin/ (inactive example) |
| User and managed config layers | Reference section below; no host settings changed |

## Configuration, trust, and lifecycle

Project hooks require project trust. Non-managed definitions require review through /hooks. User/project/plugin sources accumulate; higher config precedence does not remove lower hook sources. Multiple matching command handlers run concurrently: do not use their file order as a dependency graph. One representation per layer avoids duplicate hooks and warnings.

Inline TOML is equivalent to hooks.json. User hooks can live next to user config. Managed hooks may be delivered by system policy or requirements.toml, are trusted by policy, and cannot be disabled in the user hook browser. This repository does not install global, plugin, or managed hooks automatically. The reference plugin shows PLUGIN_ROOT; PLUGIN_DATA is the writable plugin data location. Compatibility aliases CLAUDE_PLUGIN_ROOT and CLAUDE_PLUGIN_DATA also exist. Review again after definition or bundled-script changes.

features.hooks = false disables hooks unless managed policy pins the setting. The former codex_hooks key is a deprecated alias. Do not use a trust-bypass flag for these workshops.

Command hooks are synchronous unless async is true. Background hooks cannot control the triggering operation; results arrive at a safe point or the next user turn. At most eight background hooks run concurrently per session; order is not guaranteed; unfinished work is cancelled at session end. SessionEnd remains synchronous. Interrupt uses a 1–3 second timeout; SessionEnd defaults to one second with a three-second maximum. Other examples set five seconds instead of the long default.

additionalContextLimit is an approximate token threshold per handler (default 2500). A positive value changes spilling; zero disables it and requires your own strict output bound. Tool feedback and continuation prompts retain their default limit. Avoid large or sensitive context. Transcript files are convenient but their format is not a stable hook API; these demos never parse them.

MCP hooks use an existing connection, are synchronous, bypass normal tool approval for the hook callback, and do not trigger more hooks. Connection absence, callback errors, and timeout do not block operations. SessionStart may run before the server is ready; SessionEnd cannot use MCP handlers. The shortest hook/server timeout wins; elicitation wait time is excluded. Lab 16 uses PreToolUse after server readiness.

The supported output contract depends on the event. PreToolUse does not support permissionDecision ask, continue:false, stopReason, or suppressOutput; invalid use is a hook failure and can leave the tool running. PermissionRequest uses decision.behavior, not permissionDecision; updatedInput, updatedPermissions, and interrupt are reserved and fail closed. PostToolUse does not implement updatedMCPToolOutput or suppressOutput. Never translate a generic “block” into the same effect for every event.

## Execution status

All event branches have isolated synthetic fixtures, including diagnostic outcome variants. Matching, trust, compaction scheduling, approval decisions, subagent creation, asynchronous delivery, spilling, and final session cleanup remain live-runtime checks. Use each README's exact actions; mark the live rehearsal checklist after observing evidence on the presentation machine.
