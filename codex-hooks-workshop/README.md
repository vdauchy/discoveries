# Codex CLI hooks — complete workshop

**14 supported lifecycle events, 18 runnable labs, and a full Slidev presentation.** The original five-minute introduction remains available as presentation/quickstart.md. The expanded workshop is modular; allow approximately 60–90 minutes for all live exercises and discussion.

## Start the presentation

From the repository root:

```sh
make start
```

Dependencies install if needed. Open the local URL printed by Slidev; `/presenter/1` opens presenter view with complete notes. Ctrl+C stops the server. Node 22+ is needed for slides, not for the Python examples. The Makefile retains one target.

## Run a demo

```sh
sh codex-hooks-workshop/demo.sh list
sh codex-hooks-workshop/demo.sh 01
```

Replace 01 with any ID below. The original context, block, and log aliases still work. Each scenario has its own hook configuration, Python implementation, fixtures, and live guide. The permission scenario starts Codex with read-only sandbox and on-request approvals; the others use normal local policy.

## All scenarios

| ID | Demo | Events |
| --- | --- | --- |
| 01 | [Startup context](01-session-context/README.md) | SessionStart |
| 02 | [Command denial](02-command-guard/README.md) | PreToolUse |
| 03 | [Tool logging](03-tool-log/README.md) | PostToolUse |
| 04 | [Prompt filtering](04-prompt-filter/README.md) | UserPromptSubmit |
| 05 | [Permission decisions](05-permission-request/README.md) | PermissionRequest |
| 06 | [Completion check](06-stop-check/README.md) | Stop |
| 07 | [Compaction checkpoint](07-compaction/README.md) | PreCompact, PostCompact, SessionStart |
| 08 | [Subagent lifecycle](08-subagent-lifecycle/README.md) | SubagentStart, SubagentStop |
| 09 | [Model request telemetry](09-model-requests/README.md) | PreModelRequest, PostModelRequest |
| 10 | [Interruption](10-interrupt/README.md) | Interrupt |
| 11 | [Session end](11-session-end/README.md) | SessionEnd |
| 12 | [Tool input rewriting](12-input-rewrite/README.md) | PreToolUse |
| 13 | [Post-tool feedback](13-post-tool-feedback/README.md) | PostToolUse |
| 14 | [Background execution](14-background-hook/README.md) | PostToolUse |
| 15 | [File-edit guard](15-edit-guard/README.md) | PreToolUse |
| 16 | [MCP tool handler](16-mcp-handler/README.md) | PreToolUse |
| 17 | [Failure modes](17-failure-modes/README.md) | PreToolUse |
| 18 | [Large context output](18-large-context/README.md) | SessionStart |

Read [COVERAGE.md](COVERAGE.md) for the full event/matcher/effect matrix, handler types, unsupported fields, trust/config layers, and tool coverage. The reference directory contains inactive TOML/plugin examples and an installed-CLI event support snapshot.

## Prepare for live exercises

1. Use this checkout with Git, Python 3.10+, and Codex CLI installed and authenticated. Reference binary: codex-cli 0.166.0; official release behavior checked 2026-11-04. Validate the supported set again after a CLI upgrade.
2. Launch each selected scenario and review its definition in `/hooks`, trusting the project layer as needed. Restart startup-context demos after review. Project, user, plugin, and managed hook sources accumulate; inspect all loaded sources for conflicts.
3. Verify subagents are available for lab 08 and the local MCP server is connected for lab 16. Permission lab 05 requires a real approval request; it cannot fire on an already-permitted operation. Fix sandbox issues before presenting rather than bypassing protections.
4. Reset the sample state before rehearsing: `sh codex-hooks-workshop/demo.sh reset`. This removes known generated outputs and restores answer.txt, policy.txt, and mode.txt; it does not change host configuration or trust. Stop any running demo sessions before reset.
5. Follow [LIVE-CHECKLIST.md](LIVE-CHECKLIST.md). Long-running, asynchronous, compaction, request retry, and session-end behavior needs actual runtime observation. Expected results in slides are illustrative, not recordings.

## Offline contract playback and tests

```sh
python3 codex-hooks-workshop/replay.py 05
python3 codex-hooks-workshop/replay.py all
python3 -m unittest discover -s codex-hooks-workshop/tests -v
```

Playback uses synthetic event objects in isolated temporary copies, checks response contracts, and removes generated data afterward. It does not invoke a model, match hooks, establish trust, enforce decisions, or prove event delivery. The timeout case intentionally takes five seconds. Background replay runs the Python process normally; only Codex supplies actual background scheduling. MCP fixtures exercise initialize/list/call over stdio, not Codex interpolation or callback routing.

## Presentation maintenance

The default deck includes speaker notes, live actions, expected evidence, and event-specific caveats. The retained short deck is optional: from presentation/, run `npx --no-install slidev quickstart.md`. Build or export the full deck from that directory using `npm run build` or `npm run export`; install Chromium with `npx --no-install playwright install chromium` before PDF export if needed.

The npm overrides pin patched dompurify and image-size versions pending upstream dependency updates. No CI, global hooks, plugin installation, or managed policies are installed by this repository.

## Sources

- [Official hook contracts and current limitations](https://learn.chatgpt.com/docs/hooks)
- [Configuration layers and project trust](https://learn.chatgpt.com/docs/config-file/config-basic)
- [Plugin hook packaging](https://developers.openai.com/plugins/build/plugins)
- [Slidev source](https://github.com/slidevjs/slidev), [syntax](https://sli.dev/guide/syntax.html), [exporting](https://sli.dev/guide/exporting.html)
- [MCP stdio transport](https://modelcontextprotocol.io/specification/2025-11-25/basic/transports), [tools](https://modelcontextprotocol.io/specification/2025-11-25/server/tools)
