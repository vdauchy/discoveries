# 05 · Permission decisions

**Events:** `PermissionRequest`

**Use case:** Decide only when Codex is about to request approval.

## Official input/output contract

- [PermissionRequest — event inputs and allowed outputs](https://learn.chatgpt.com/docs/hooks#permissionrequest)

Every event also uses the [common input fields](https://learn.chatgpt.com/docs/hooks#common-input-fields). Check the [shared output fields and event-specific restrictions](https://learn.chatgpt.com/docs/hooks#common-output-fields) before returning a response. The event links above specify what each hook adds and which outputs it accepts.

## Run live

From the repository root:

```sh
sh codex-hooks-workshop/demo.sh 05
```

Trust the project, review this definition in `/hooks`, and inspect any other loaded sources. Trust changes can require review again. Setup is outside the demonstration. The launcher changes directory to this scenario.

Launch this scenario in read-only sandbox mode (the launcher does this). Ask: Execute exactly `python3 write_marker.py`; if the sandbox rejects the write, request approval to rerun it with elevated permissions. Do not use another mechanism.

**Expected evidence:** PermissionRequest denies the escalation and .demo/write-marker.txt remains absent.

**Important behavior:** Depends on approval policy and a real escalation. No approval request means no event. policy.txt can be deny, allow, or abstain; restart after changes if required by trust review. Allow is restricted to the exact local simulation command.

## Inspect the contract without a model call

```sh
python3 codex-hooks-workshop/replay.py 05
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

To exercise the other branches: set `policy.txt` to `allow` or `abstain` and retry the same escalation. Allow suppresses that approval prompt; abstain leaves normal approval handling in place. Restore `deny` afterward.
