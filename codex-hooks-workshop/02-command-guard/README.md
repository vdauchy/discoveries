# 02 · Command denial

**Events:** `PreToolUse`

**Use case:** Check a specific shell command before execution.

## Official input/output contract

- [PreToolUse — event inputs and allowed outputs](https://learn.chatgpt.com/docs/hooks#pretooluse)

Every event also uses the [common input fields](https://learn.chatgpt.com/docs/hooks#common-input-fields). Check the [shared output fields and event-specific restrictions](https://learn.chatgpt.com/docs/hooks#common-output-fields) before returning a response. The event links above specify what each hook adds and which outputs it accepts.

## Run live

From the repository root:

```sh
sh codex-hooks-workshop/demo.sh 02
```

Trust the project, review this definition in `/hooks`, and inspect any other loaded sources. Trust changes can require review again. Setup is outside the demonstration. The launcher changes directory to this scenario.

Ask: Run exactly `python3 deploy.py --env production` once. If blocked, report the denial and do not retry. Then ask for `python3 deploy.py --env staging`.

**Expected evidence:** Production is denied; only the staging marker exists.

**Important behavior:** This exact-token check is not a complete shell security policy. Both deployments are local simulations.

## Inspect the contract without a model call

```sh
python3 codex-hooks-workshop/replay.py 02
```

This uses an isolated temporary copy and synthetic event inputs from fixtures.json. It checks response JSON, exit behavior, and local artifacts. It does **not** test CLI matching, trust, approval policy, timing, or runtime delivery. The replay of the background hook is synchronous Python execution; only the live CLI demonstrates background scheduling.

## Read the implementation

- `manifest.json`: scenario identity, description, and declared events.
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
