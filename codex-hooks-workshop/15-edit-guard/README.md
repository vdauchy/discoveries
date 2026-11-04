# 15 · File-edit guard

**Events:** `PreToolUse`

**Use case:** Inspect an apply_patch call rather than shell execution.

## Run live

From the repository root:

```sh
sh codex-hooks-workshop/demo.sh 15
```

Trust the project, review this definition in `/hooks`, and inspect any other loaded sources. Trust changes can require review again. Setup is outside the demonstration. The launcher changes directory to this scenario.

Ask: Use apply_patch to change protected.txt to Changed. If blocked, report the denial and do not try another tool. Then ask apply_patch to add notes.txt.

**Expected evidence:** The protected patch is denied; an unrelated patch is allowed.

**Important behavior:** Narrow header check for the exact relative path only. Shell writes and alternate spellings are outside this example. apply_patch also matches Edit and Write aliases.

## Inspect the contract without a model call

```sh
python3 codex-hooks-workshop/replay.py 15
```

This uses an isolated temporary copy and synthetic event inputs from fixtures.json. It checks response JSON, exit behavior, and local artifacts. It does **not** test CLI matching, trust, approval policy, timing, or runtime delivery. The replay of the background hook is synchronous Python execution; only the live CLI demonstrates background scheduling.

## Read the implementation

- `.codex/hooks.json`: event, matcher, handler, timeout.
- `hook.py`: JSON stdin, small action, event-specific response.
- `fixtures.json`: synthetic success and edge cases with expected results.

Reset generated artifacts before repeating:

```sh
sh codex-hooks-workshop/demo.sh reset
```

Reset also restores the documented initial answer, permission policy, and failure mode. It does not change your Codex configuration or hook trust.

## Verification status

Automated fixture checks are available. Live trust, matching, and model behavior must be rehearsed on the presentation machine; illustrative expected evidence is not a recorded CLI transcript.

Source: [Official hooks reference](https://learn.chatgpt.com/docs/hooks), checked 2026-11-04. Reference CLI: 0.166.0.
