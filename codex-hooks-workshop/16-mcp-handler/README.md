# 16 · MCP tool handler

**Events:** `PreToolUse`

**Use case:** Route a policy check through an existing local MCP connection.

## Run live

From the repository root:

```sh
sh codex-hooks-workshop/demo.sh 16
```

Trust the project, review this definition in `/hooks`, and inspect any other loaded sources. Trust changes can require review again. Setup is outside the demonstration. The launcher changes directory to this scenario.

Check `/mcp` shows workshop_checker connected, then ask for the exact simulated production deployment command from scenario 02.

**Expected evidence:** Local check_command returns a denial; .demo/events.jsonl records the decision.

**Important behavior:** The handler does not connect servers itself. Missing servers, tool errors, and timeouts do not block. MCP handlers are synchronous and cannot handle SessionEnd.

## Inspect the contract without a model call

```sh
python3 codex-hooks-workshop/replay.py 16
```

This uses an isolated temporary copy and synthetic event inputs from fixtures.json. It checks response JSON, exit behavior, and local artifacts. It does **not** test CLI matching, trust, approval policy, timing, or runtime delivery. The replay of the background hook is synchronous Python execution; only the live CLI demonstrates background scheduling.

## Read the implementation

- `.codex/hooks.json`: event, matcher, handler, timeout.
- `server.py`: local JSON-RPC server; `.codex/config.toml`: connection configuration.
- `fixtures.json`: synthetic success and edge cases with expected results.

Reset generated artifacts before repeating:

```sh
sh codex-hooks-workshop/demo.sh reset
```

Reset also restores the documented initial answer, permission policy, and failure mode. It does not change your Codex configuration or hook trust.

## Verification status

Automated fixture checks are available. Live trust, matching, and model behavior must be rehearsed on the presentation machine; illustrative expected evidence is not a recorded CLI transcript.

Source: [Official hooks reference](https://learn.chatgpt.com/docs/hooks), checked 2026-11-04. Reference CLI: 0.166.0.

MCP protocol references: [stdio](https://modelcontextprotocol.io/specification/2025-11-25/basic/transports), [tools](https://modelcontextprotocol.io/specification/2025-11-25/server/tools). This teaching server supports a small JSON-RPC subset and is not intended for general deployment.
