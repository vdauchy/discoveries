# 17 · Failure modes

**Events:** `PreToolUse`

**Use case:** Compare explicit denial with hook failures.

## Official input/output contract

- [PreToolUse — event inputs and allowed outputs](https://learn.chatgpt.com/docs/hooks#pretooluse)

Every event also uses the [common input fields](https://learn.chatgpt.com/docs/hooks#common-input-fields). Check the [shared output fields and event-specific restrictions](https://learn.chatgpt.com/docs/hooks#common-output-fields) before returning a response. The event links above specify what each hook adds and which outputs it accepts.

## Run live

From the repository root:

```sh
sh codex-hooks-workshop/demo.sh 17
```

Trust the project, review this definition in `/hooks`, and inspect any other loaded sources. Trust changes can require review again. Setup is outside the demonstration. The launcher changes directory to this scenario.

Keep mode.txt as pass initially. Ask for `python3 hello.py`. Then set mode.txt to deny-exit, error, invalid-json, unsupported, or timeout, review changes if prompted, and repeat the command.

**Expected evidence:** Exit 2 is a policy denial; other modes show a failing hook or unsupported-field report. Fixtures show each response separately.

**Important behavior:** Do not use errors as a policy mechanism. This scenario is intentionally broken in some modes. Restore mode.txt to pass with reset before leaving it.

## Inspect the contract without a model call

```sh
python3 codex-hooks-workshop/replay.py 17
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
