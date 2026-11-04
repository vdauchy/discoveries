# 08 · Subagent lifecycle

**Events:** `SubagentStart`, `SubagentStop`

**Use case:** Give reviewers instructions and request a missing verification note.

## Official input/output contract

- [SubagentStart — event inputs and allowed outputs](https://learn.chatgpt.com/docs/hooks#subagentstart)
- [SubagentStop — event inputs and allowed outputs](https://learn.chatgpt.com/docs/hooks#subagentstop)

Every event also uses the [common input fields](https://learn.chatgpt.com/docs/hooks#common-input-fields). Check the [shared output fields and event-specific restrictions](https://learn.chatgpt.com/docs/hooks#common-output-fields) before returning a response. The event links above specify what each hook adds and which outputs it accepts.

## Run live

From the repository root:

```sh
sh codex-hooks-workshop/demo.sh 08
```

Trust the project, review this definition in `/hooks`, and inspect any other loaded sources. Trust changes can require review again. Setup is outside the demonstration. The launcher changes directory to this scenario.

Ask: Spawn one read-only subagent to inspect this scenario README and report a short summary. Have it state what tests it ran or did not run. Wait for it to finish.

**Expected evidence:** Journal contains SubagentStart and SubagentStop with the child identifier; report includes Tests:.

**Important behavior:** Requires subagents enabled and an actual spawned child. A conforming report needs no retry; the missing-Tests fixture demonstrates continuation deterministically. SubagentStart cannot stop a child via continue:false.

## Inspect the contract without a model call

```sh
python3 codex-hooks-workshop/replay.py 08
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
