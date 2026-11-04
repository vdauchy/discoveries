---
theme: default
title: Codex CLI hooks
info: Three practical examples for software engineers in five minutes
colorSchema: dark
fonts:
  sans: Arial
  mono: monospace
  provider: none
highlighter: shiki
drawings:
  persist: false
transition: none
mdc: true
---

# Codex CLI hooks

<p class="lead">Add context. Check a command.<br>Observe the result.</p>

Three Python scripts · Five minutes · Software engineers

<div class="flow"><b>SessionStart</b> → <b>PreToolUse</b> → <b>PostToolUse</b></div>

<p class="caption">Examples prepared for Codex CLI 0.166.0 · 4 November 2026</p>

<!--
0:00–0:15. Today we will see three places where a small script can participate in the Codex lifecycle. No services or actual deployments are involved.
Source: https://learn.chatgpt.com/docs/hooks
-->

---

# The hook contract

<div class="flow">Codex event → <b>Matcher</b> → Script → <b>Response</b></div>

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "^Bash$",
      "hooks": [{ "type": "command", "command": "python3 .../hook.py" }]
    }]
  }
}
```

**JSON in** through stdin · **JSON out** through stdout

<p class="caption">Project configuration: .codex/hooks.json · Review and trust through /hooks</p>

<!--
0:15–0:40. Show the actual 02-command-guard/.codex/hooks.json, explaining that the slide abbreviates the script path. Event chooses when, matcher chooses which tool, command chooses what runs. Bash matches CLI shell execution. Hooks run automatically after review; the model does not choose whether to invoke them. Preparation and trust are already complete.
Source: https://learn.chatgpt.com/docs/hooks
-->

---

# 1 · Supply runtime context

**SessionStart** reads the selected environment before the model starts.

```python
context = f"Selected deployment environment: {environment}."
print(json.dumps({"hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": context
}}))
```

**Ask:** Which deployment environment is selected?<br>Answer in one sentence without using tools.

```text
Expected: The selected deployment environment is staging.
```

<!--
0:40–1:40. Terminal: sh codex-hooks-workshop/demo.sh context. If already opened during prep, use the prepared fresh session. Paste the prompt on the slide. Show environment.txt contains staging and hook.py reads it at startup. The result is illustrative, not an exact wording assertion. The model receives context calculated by a script. Use AGENTS.md for enduring written conventions.
If latency is high, use the expected answer and show the actual hook response with the local fixture command from the appendix.
Source: https://learn.chatgpt.com/docs/hooks#sessionstart
-->

---

# 2 · Check before execution

**PreToolUse** denies the simulated production command.

```sh
python3 deploy.py --env production
```

```json
{"hookSpecificOutput": {
  "hookEventName": "PreToolUse",
  "permissionDecision": "deny",
  "permissionDecisionReason":
    "Workshop policy: production deployment is blocked. Use staging."
}}
```

Then run `python3 deploy.py --env staging` → **local marker created**

<p class="caption">Exact demo command check only. No actual deployment or complete shell policy.</p>

<!--
1:40–3:10. Terminal: sh codex-hooks-workshop/demo.sh block.
Prompt: Run exactly `python3 deploy.py --env production` once. This is a local simulation. If blocked, report the denial and do not try another command.
Show the denial and absence of deployment-production.txt. Then prompt: Run exactly `python3 deploy.py --env staging`. Show simulated staging output and deployment-staging.txt. The guard deliberately only recognizes this token sequence; do not imply it prevents all ways to modify production. Do not run deploy.py production directly from the presenter terminal as a hook demonstration: only Codex tool calls trigger the hook.
Source: https://learn.chatgpt.com/docs/hooks#pretooluse
-->

---

# 3 · Observe a completed command

**PostToolUse** appends metadata to a local JSONL file.

```sh
python3 hello.py
# Hello from the hooks workshop!
```

```json
{
  "event": "PostToolUse",
  "tool": "Bash",
  "session_id": "example-session",
  "timestamp": "2026-11-04T18:00:00+00:00"
}
```

**Use for:** debugging and workflow visibility

<p class="caption">Illustrative entry · Actual records are one JSON object per line · The command already ran</p>

<!--
3:10–4:20. Terminal: sh codex-hooks-workshop/demo.sh log.
Prompt: Run exactly `python3 hello.py` once, then briefly report its output.
Separate terminal from repository root: cat codex-hooks-workshop/03-tool-log/events.jsonl
Explain that no command contents, outputs, or prompts are stored. Additional calls can create more entries. PostToolUse cannot undo side effects. The example ID and timestamp on the slide are illustrative.
Source: https://learn.chatgpt.com/docs/hooks#posttooluse
-->

---

# Choosing the right mechanism

| Need | Mechanism |
| --- | --- |
| Persistent project conventions | AGENTS.md |
| Context calculated at startup | SessionStart |
| Check a supported tool call first | PreToolUse |
| Observe a completed tool call | PostToolUse |

**Event → matcher → script → response**

<p class="caption">Start with one small script and one observable result</p>

<!--
4:20–5:00. Recap the three outputs: context, denial, log. Static instructions fit AGENTS.md. Runtime hooks are useful when a repeatable action should happen at a defined lifecycle point. The examples are in the repository and can be read independently. Stop the timed presentation here. The remaining slides are optional reference.
Sources: https://learn.chatgpt.com/docs/hooks and https://learn.chatgpt.com/docs/agents-md
-->

---

# Reference · Setup and local checks

```sh
# From the repository root
codex --version
codex features list
python3 -m unittest discover -s codex-hooks-workshop/tests -v
sh codex-hooks-workshop/demo.sh reset
```

- Trust the project and review definitions in `/hooks`
- Restart the context session after review
- Inspect all loaded sources: global hooks also run
- Hook failures are not guaranteed denials

<!--
Outside the five-minute path. Setup should be completed before presenting. Tests exercise hook scripts and fixtures, not runtime enforcement. Trust and live rehearsal are distinct acceptance steps. Never bypass trust or sandboxing for convenience. See README troubleshooting if a hook is absent or fails.
Sources: https://learn.chatgpt.com/docs/hooks and https://learn.chatgpt.com/docs/config-file/config-basic
-->

---

# Reference · Sources and fallback

[Official Codex hooks guide](https://learn.chatgpt.com/docs/hooks) · [Configuration layers](https://learn.chatgpt.com/docs/config-file/config-basic)

[Slidev source](https://github.com/slidevjs/slidev) · [Syntax](https://sli.dev/guide/syntax.html) · [Export](https://sli.dev/guide/exporting.html)

Direct hook inspection, without a model call:

```sh
printf '{"hook_event_name":"SessionStart"}' | \
  python3 codex-hooks-workshop/01-session-context/hook.py
```

**This prints the response contract; it does not demonstrate CLI delivery.**

<p class="caption">Scenario READMEs contain prompts and illustrative expected results</p>

<!--
Outside the five-minute path. Use fixture invocation to explain the wire contract when offline; explicitly distinguish this from live Codex runtime execution. All example outputs in the slides are illustrative. Official docs consulted 2026-11-04.
-->
