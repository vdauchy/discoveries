---
theme: default
title: Codex CLI hooks — complete workshop
info: Fourteen lifecycle events and eighteen practical labs for software engineers
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

<p class="lead">The complete workshop</p>

**14 lifecycle events · 18 practical labs**

Python scripts, a local MCP server, and observable results

<p class="caption">Software engineers · Modular 60–90 minute session · CLI reference: 0.166.0</p>

<!--
Welcome. The first three labs still form a five-minute introduction. For this extended session, choose modules or work through the complete lifecycle. Setup and trust are completed before the presentation.
Source: https://learn.chatgpt.com/docs/hooks
-->

---

# Workshop routes

| Route | Labs | Suggested time |
| --- | --- | --- |
| Introduction | 01–03 | 5 minutes |
| Every lifecycle event | 01–11 | 35–50 minutes |
| Behavior and failure labs | 12–18 | 25–40 minutes |

**For each lab:** inspect → trigger → observe → explain

<!--
Timing is a planning estimate, not a performance guarantee. Model response latency, permission setup, and compaction vary. Keep a separate terminal for evidence. Fixture playback is the offline alternative and must be labeled synthetic.
Source: https://learn.chatgpt.com/docs/hooks
-->

---

# The event lifecycle

<div class="flow"><b>SessionStart</b> → UserPromptSubmit → Model request</div>

<div class="flow"><b>PreToolUse</b> → Approval if needed → Tool → <b>PostToolUse</b></div>

<div class="flow">More work → <b>Stop</b> → Next user turn</div>

Compaction, subagent activity, and interruptions add their own events.

**SessionEnd** happens when the main session actually ends.

<!--
This is a conceptual path, not a complete guaranteed event ordering. Model attempts repeat; some tool paths opt out of hooks. PermissionRequest appears only when approval is actually needed. Stop ends a turn; SessionEnd closes the session.
Source: https://learn.chatgpt.com/docs/hooks
-->

---

# The JSON contract

```json
{
  "hook_event_name": "PreToolUse",
  "session_id": "example-session",
  "cwd": "/example/scenario",
  "tool_name": "Bash",
  "tool_input": { "command": "python3 hello.py" }
}
```

**stdin:** one event object · **stdout:** event-specific response

**stderr:** diagnostics · **exit 2:** event-specific denial or feedback

<!--
Fields shown are an excerpt, not the complete schema. JSON responses differ by event. An empty successful response normally continues, but Stop and SubagentStop require valid JSON when returning output. Plain text is context for SessionStart, SubagentStart, and UserPromptSubmit; it is ignored or invalid elsewhere. Read actual hook.py files and fixtures.json.
Source: https://learn.chatgpt.com/docs/hooks
-->

---

# Trust and configuration

- Project hooks: `.codex/hooks.json`
- Review definitions through **`/hooks`**
- User, project, plugin, and managed sources accumulate
- Matching command handlers can run concurrently

**One event → matcher → handler → response**

<!--
Trusted project layer and trusted hook definition are separate requirements. Review changed definitions or plugin scripts again. Inline TOML is equivalent, but do not activate both forms at one layer unless intentional. Managed hooks are trusted by policy. No global or managed hooks are installed by this workshop.
Source: https://learn.chatgpt.com/docs/hooks
-->

---

# Tool matchers

| Tool path | Matcher |
| --- | --- |
| Shell / exec_command | `Bash` |
| File patch | `apply_patch`, `Edit`, `Write` |
| MCP tool | Its canonical MCP tool name |
| Other local function | Its tool name; Agent also matches spawn_agent |

Hosted tools such as WebSearch are outside this path.

<!--
Matcher is a regex. It is ignored on UserPromptSubmit, Stop, Interrupt, and model-request events. SessionStart matches source; compaction matches trigger; subagent events match agent_type; SessionEnd matches reason. write_stdin does not rerun PreToolUse for an existing command. Tool hooks are guardrails, not a complete enforcement boundary.
Source: https://learn.chatgpt.com/docs/hooks
-->

---

# Fixture playback versus live execution

```sh
python3 codex-hooks-workshop/replay.py all
sh codex-hooks-workshop/demo.sh list
```

| Fixtures verify | Live CLI must verify |
| --- | --- |
| Script decisions and artifacts | Event delivery and matching |
| Response JSON and exit codes | Trust and approval policy |
| MCP stdio exchange | Background scheduling and spilling |

<!--
Fixtures run isolated copies with synthetic events. They do not mock the entire Codex runtime or establish enforcement. Never describe a fixture result as a recorded CLI run. The live checklist has no pre-marked results. The failure fixture intentionally spends five seconds reaching a timeout.
Source: https://learn.chatgpt.com/docs/hooks
-->

---
class: compact
---

# 01 · Startup context

**SessionStart** · Supply runtime environment information.

```json
{"hookSpecificOutput": {
  "hookEventName": "SessionStart",
  "additionalContext": "Selected environment: staging."
}}
```

<p class="caption">Response or mechanism excerpt; read the complete hook alongside it.</p>

<!--
Restart after hook review. Match startup, resume, clear, compact, or fork when needed; this example matches startup and resume.
Show 01-session-context/hook.py (server.py for lab 16) and its hook configuration. Explain where the JSON fields differ from other events.
Ask: Which deployment environment is selected? Answer without using tools.
Source: https://learn.chatgpt.com/docs/hooks
-->

---
class: compact
---

# Live lab 01

```sh
sh codex-hooks-workshop/demo.sh 01
```

Ask which deployment environment is selected, without tools.

Answer reflects **staging** from startup context.

<p class="caption">Use a new session after reviewing the hook.</p>

```sh
python3 codex-hooks-workshop/replay.py 01
```

<!--
Allow 2–5 minutes for this lab depending on event setup and discussion.
Full live action: Ask: Which deployment environment is selected? Answer without using tools.
Expected evidence: Codex answers staging from hook context.
Caveat: Restart after hook review. Match startup, resume, clear, compact, or fork when needed; this example matches startup and resume.
Fallback: run replay.py 01 and identify the result as synthetic contract inspection, not a runtime recording. Reset only between closed demo sessions. See LIVE-CHECKLIST.md for rehearsal evidence.
Source: https://learn.chatgpt.com/docs/hooks
-->

---
class: compact
---

# 02 · Command denial

**PreToolUse** · Check a specific shell command before execution.

```json
{"hookSpecificOutput": {
  "hookEventName": "PreToolUse",
  "permissionDecision": "deny",
  "permissionDecisionReason": "Production simulation blocked."
}}
```

<p class="caption">Response or mechanism excerpt; read the complete hook alongside it.</p>

<!--
This exact-token check is not a complete shell security policy. Both deployments are local simulations.
Show 02-command-guard/hook.py (server.py for lab 16) and its hook configuration. Explain where the JSON fields differ from other events.
Ask: Run exactly `python3 deploy.py --env production` once. If blocked, report the denial and do not retry. Then ask for `python3 deploy.py --env staging`.
Source: https://learn.chatgpt.com/docs/hooks
-->

---
class: compact
---

# Live lab 02

```sh
sh codex-hooks-workshop/demo.sh 02
```

Run the exact production simulation, then the staging simulation.

**Production denied; staging marker created.**

<p class="caption">An exact-token teaching check, not a complete shell policy.</p>

```sh
python3 codex-hooks-workshop/replay.py 02
```

<!--
Allow 2–5 minutes for this lab depending on event setup and discussion.
Full live action: Ask: Run exactly `python3 deploy.py --env production` once. If blocked, report the denial and do not retry. Then ask for `python3 deploy.py --env staging`.
Expected evidence: Production is denied; only the staging marker exists.
Caveat: This exact-token check is not a complete shell security policy. Both deployments are local simulations.
Fallback: run replay.py 02 and identify the result as synthetic contract inspection, not a runtime recording. Reset only between closed demo sessions. See LIVE-CHECKLIST.md for rehearsal evidence.
Source: https://learn.chatgpt.com/docs/hooks
-->

---
class: compact
---

# 03 · Tool logging

**PostToolUse** · Record metadata after supported tool completion.

```json
{
  "event": "PostToolUse",
  "tool": "Bash",
  "session_id": "example-session",
  "timestamp": "2026-11-04T18:00:00+00:00"
}
```

<p class="caption">Illustrative log record; the hook response itself is {}.</p>

<!--
A nonzero shell exit can still trigger PostToolUse. No raw prompt, command, or output is recorded by this logger.
Show 03-tool-log/hook.py (server.py for lab 16) and its hook configuration. Explain where the JSON fields differ from other events.
Ask: Run exactly `python3 hello.py` once. Inspect events.jsonl from a separate terminal.
Source: https://learn.chatgpt.com/docs/hooks
-->

---
class: compact
---

# Live lab 03

```sh
sh codex-hooks-workshop/demo.sh 03
```

Run `python3 hello.py`; inspect the JSONL from another terminal.

**A new tool-completion record.**

<p class="caption">Inspecting logs through Codex creates additional tool calls.</p>

```sh
python3 codex-hooks-workshop/replay.py 03
```

<!--
Allow 2–5 minutes for this lab depending on event setup and discussion.
Full live action: Ask: Run exactly `python3 hello.py` once. Inspect events.jsonl from a separate terminal.
Expected evidence: A new JSONL entry records the completed shell call.
Caveat: A nonzero shell exit can still trigger PostToolUse. No raw prompt, command, or output is recorded by this logger.
Fallback: run replay.py 03 and identify the result as synthetic contract inspection, not a runtime recording. Reset only between closed demo sessions. See LIVE-CHECKLIST.md for rehearsal evidence.
Source: https://learn.chatgpt.com/docs/hooks
-->

---
class: compact
---

# 04 · Prompt filtering

**UserPromptSubmit** · Reject a synthetic sensitive marker and add task context.

```json
{
  "decision": "block",
  "reason": "Remove the synthetic secret marker."
}
```

<p class="caption">Response or mechanism excerpt; read the complete hook alongside it.</p>

<!--
Only a synthetic marker is checked. Matcher is ignored for UserPromptSubmit. Never paste real credentials in the demo.
Show 04-prompt-filter/hook.py (server.py for lab 16) and its hook configuration. Explain where the JSON fields differ from other events.
Submit: Explain DEMO_SECRET_123. Observe rejection. Then submit: Explain how you would investigate a failing test.
Source: https://learn.chatgpt.com/docs/hooks
-->

---
class: compact
---

# Live lab 04

```sh
sh codex-hooks-workshop/demo.sh 04
```

Submit `Explain DEMO_SECRET_123`, then a normal test question.

**Marker rejected; normal prompt receives context.**

<p class="caption">Only use the synthetic marker. Matcher is ignored here.</p>

```sh
python3 codex-hooks-workshop/replay.py 04
```

<!--
Allow 2–5 minutes for this lab depending on event setup and discussion.
Full live action: Submit: Explain DEMO_SECRET_123. Observe rejection. Then submit: Explain how you would investigate a failing test.
Expected evidence: First prompt is blocked; the second receives brief explanation guidance.
Caveat: Only a synthetic marker is checked. Matcher is ignored for UserPromptSubmit. Never paste real credentials in the demo.
Fallback: run replay.py 04 and identify the result as synthetic contract inspection, not a runtime recording. Reset only between closed demo sessions. See LIVE-CHECKLIST.md for rehearsal evidence.
Source: https://learn.chatgpt.com/docs/hooks
-->

---
class: compact
---

# 05 · Permission decisions

**PermissionRequest** · Decide only when Codex is about to request approval.

```json
{"hookSpecificOutput": {
  "hookEventName": "PermissionRequest",
  "decision": {
    "behavior": "deny",
    "message": "Demo policy denies this requested write."
  }
}}
```

<p class="caption">Response or mechanism excerpt; read the complete hook alongside it.</p>

<!--
Depends on approval policy and a real escalation. No approval request means no event. policy.txt can be deny, allow, or abstain; restart after changes if required by trust review. Allow is restricted to the exact local simulation command.
Show 05-permission-request/hook.py (server.py for lab 16) and its hook configuration. Explain where the JSON fields differ from other events.
Launch this scenario in read-only sandbox mode (the launcher does this). Ask: Execute exactly `python3 write_marker.py`; if the sandbox rejects the write, request approval to rerun it with elevated permissions. Do not use another mechanism.
Source: https://learn.chatgpt.com/docs/hooks
-->

---
class: compact
---

# Live lab 05

```sh
sh codex-hooks-workshop/demo.sh 05
```

Run `python3 write_marker.py`; request escalation after sandbox rejection.

**The permission hook denies the requested write.**

<p class="caption">No approval request means no PermissionRequest event.</p>

```sh
python3 codex-hooks-workshop/replay.py 05
```

<!--
Allow 2–5 minutes for this lab depending on event setup and discussion.
Full live action: Launch this scenario in read-only sandbox mode (the launcher does this). Ask: Execute exactly `python3 write_marker.py`; if the sandbox rejects the write, request approval to rerun it with elevated permissions. Do not use another mechanism.
Expected evidence: PermissionRequest denies the escalation and .demo/write-marker.txt remains absent.
Caveat: Depends on approval policy and a real escalation. No approval request means no event. policy.txt can be deny, allow, or abstain; restart after changes if required by trust review. Allow is restricted to the exact local simulation command.
Fallback: run replay.py 05 and identify the result as synthetic contract inspection, not a runtime recording. Reset only between closed demo sessions. See LIVE-CHECKLIST.md for rehearsal evidence.
Source: https://learn.chatgpt.com/docs/hooks
-->

---
class: compact
---

# 06 · Completion check

**Stop** · Run a check when the main turn tries to finish.

```python
if check_passed:
    print("{}")
elif payload.get("stop_hook_active"):
    print(json.dumps({"systemMessage": "Demo retry limit reached."}))
else:
    print(json.dumps({"decision": "block", "reason": "Fix the check."}))
```

<p class="caption">Control-flow excerpt; the full script runs check.py.</p>

<!--
stop_hook_active bounds follow-ups to one. A failed second check produces a warning and releases the demo; this is not an indefinite quality gate.
Show 06-stop-check/hook.py (server.py for lab 16) and its hook configuration. Explain where the JSON fields differ from other events.
Reset first. Ask: Reply Ready. Let the Stop hook request its follow-up check.
Source: https://learn.chatgpt.com/docs/hooks
-->

---
class: compact
---

# Live lab 06

```sh
sh codex-hooks-workshop/demo.sh 06
```

With answer.txt reset to 41, ask Codex to reply Ready.

**Check fails → continuation → answer becomes 42 → PASS.**

<p class="caption">One follow-up maximum; a repeated failure is reported, not looped.</p>

```sh
python3 codex-hooks-workshop/replay.py 06
```

<!--
Allow 2–5 minutes for this lab depending on event setup and discussion.
Full live action: Reset first. Ask: Reply Ready. Let the Stop hook request its follow-up check.
Expected evidence: The hook detects answer.txt = 41, requests a continuation, and Codex changes it to 42 and runs check.py.
Caveat: stop_hook_active bounds follow-ups to one. A failed second check produces a warning and releases the demo; this is not an indefinite quality gate.
Fallback: run replay.py 06 and identify the result as synthetic contract inspection, not a runtime recording. Reset only between closed demo sessions. See LIVE-CHECKLIST.md for rehearsal evidence.
Source: https://learn.chatgpt.com/docs/hooks
-->

---
class: compact
---

# 07 · Compaction checkpoint

**PreCompact, PostCompact, SessionStart** · Save a small explicit task checkpoint and restore it after compaction.

```text
PreCompact                  Save synthetic checkpoint
PostCompact                 Record completed compaction
SessionStart source=compact Restore checkpoint as context
```

<p class="caption">Response or mechanism excerpt; read the complete hook alongside it.</p>

<!--
Checkpoint contents are synthetic, not an automatic transcript summary. Manual and automatic triggers are supported, but the live exercise uses manual compaction.
Show 07-compaction/hook.py (server.py for lab 16) and its hook configuration. Explain where the JSON fields differ from other events.
Have a short conversation about a synthetic failing test, then run `/compact`. Inspect .demo/events.jsonl and checkpoint.json.
Source: https://learn.chatgpt.com/docs/hooks
-->

---
class: compact
---

# Live lab 07

```sh
sh codex-hooks-workshop/demo.sh 07
```

Discuss a synthetic test task, then invoke `/compact`.

**Checkpoint saved, compaction recorded, context restored.**

<p class="caption">Use the event journal; do not assume an exact full event order.</p>

```sh
python3 codex-hooks-workshop/replay.py 07
```

<!--
Allow 2–5 minutes for this lab depending on event setup and discussion.
Full live action: Have a short conversation about a synthetic failing test, then run `/compact`. Inspect .demo/events.jsonl and checkpoint.json.
Expected evidence: PreCompact saves a checkpoint; PostCompact reports completion; SessionStart source compact supplies the saved task context.
Caveat: Checkpoint contents are synthetic, not an automatic transcript summary. Manual and automatic triggers are supported, but the live exercise uses manual compaction.
Fallback: run replay.py 07 and identify the result as synthetic contract inspection, not a runtime recording. Reset only between closed demo sessions. See LIVE-CHECKLIST.md for rehearsal evidence.
Source: https://learn.chatgpt.com/docs/hooks
-->

---
class: compact
---

# 08 · Subagent lifecycle

**SubagentStart, SubagentStop** · Give reviewers instructions and request a missing verification note.

```text
SubagentStart → additionalContext → reviewer instructions
SubagentStop  → decision: block   → request a verification note
              → {}               → report complete
```

<p class="caption">Response or mechanism excerpt; read the complete hook alongside it.</p>

<!--
Requires subagents enabled and an actual spawned child. A conforming report needs no retry; the missing-Tests fixture demonstrates continuation deterministically. SubagentStart cannot stop a child via continue:false.
Show 08-subagent-lifecycle/hook.py (server.py for lab 16) and its hook configuration. Explain where the JSON fields differ from other events.
Ask: Spawn one read-only subagent to inspect this scenario README and report a short summary. Have it state what tests it ran or did not run. Wait for it to finish.
Source: https://learn.chatgpt.com/docs/hooks
-->

---
class: compact
---

# Live lab 08

```sh
sh codex-hooks-workshop/demo.sh 08
```

Spawn one read-only reviewer to inspect this README and report tests.

**Start and stop records; a Tests: line in its report.**

<p class="caption">A conforming report needs no retry; use fixtures for that branch.</p>

```sh
python3 codex-hooks-workshop/replay.py 08
```

<!--
Allow 2–5 minutes for this lab depending on event setup and discussion.
Full live action: Ask: Spawn one read-only subagent to inspect this scenario README and report a short summary. Have it state what tests it ran or did not run. Wait for it to finish.
Expected evidence: Journal contains SubagentStart and SubagentStop with the child identifier; report includes Tests:.
Caveat: Requires subagents enabled and an actual spawned child. A conforming report needs no retry; the missing-Tests fixture demonstrates continuation deterministically. SubagentStart cannot stop a child via continue:false.
Fallback: run replay.py 08 and identify the result as synthetic contract inspection, not a runtime recording. Reset only between closed demo sessions. See LIVE-CHECKLIST.md for rehearsal evidence.
Source: https://learn.chatgpt.com/docs/hooks
-->

---
class: compact
---

# 09 · Model request telemetry

**PreModelRequest, PostModelRequest** · Observe each model request attempt, including retries.

```json
{
  "status": "completed",
  "token_usage": null,
  "has_error": false
}
```

<p class="caption">Illustrative completion metadata; hook output is diagnostic only.</p>

<!--
Diagnostic only: cannot block requests or inject context. One user turn can contain several request attempts. Failed/cancelled outcomes are synthetic fixture cases, not induced provider outages.
Show 09-model-requests/hook.py (server.py for lab 16) and its hook configuration. Explain where the JSON fields differ from other events.
Ask: Reply with one sentence describing a hook. Inspect .demo/events.jsonl and outcomes.jsonl.
Source: https://learn.chatgpt.com/docs/hooks
-->

---
class: compact
---

# Live lab 09

```sh
sh codex-hooks-workshop/demo.sh 09
```

Ask for a one-sentence reply; inspect events and outcomes.

**Request attempt and completion records.**

<p class="caption">Diagnostic only; failed/cancelled outcomes have fixture coverage.</p>

```sh
python3 codex-hooks-workshop/replay.py 09
```

<!--
Allow 2–5 minutes for this lab depending on event setup and discussion.
Full live action: Ask: Reply with one sentence describing a hook. Inspect .demo/events.jsonl and outcomes.jsonl.
Expected evidence: PreModelRequest and PostModelRequest record the model and outcome; token usage can be null.
Caveat: Diagnostic only: cannot block requests or inject context. One user turn can contain several request attempts. Failed/cancelled outcomes are synthetic fixture cases, not induced provider outages.
Fallback: run replay.py 09 and identify the result as synthetic contract inspection, not a runtime recording. Reset only between closed demo sessions. See LIVE-CHECKLIST.md for rehearsal evidence.
Source: https://learn.chatgpt.com/docs/hooks
-->

---
class: compact
---

# 10 · Interruption

**Interrupt** · Record an interrupted active main-thread turn.

```json
{
  "systemMessage": "Recorded interruption locally."
}
```

<p class="caption">Response or mechanism excerpt; read the complete hook alongside it.</p>

<!--
No event for idle threads or subagents. Output cannot prevent interruption or restart the turn. Stopping a turn does not guarantee rollback of tool side effects.
Show 10-interrupt/hook.py (server.py for lab 16) and its hook configuration. Explain where the JSON fields differ from other events.
Ask: Run `python3 slow.py` and wait for it to finish. Press Esc while the turn is active. Inspect .demo/interrupted.json.
Source: https://learn.chatgpt.com/docs/hooks
-->

---
class: compact
---

# Live lab 10

```sh
sh codex-hooks-workshop/demo.sh 10
```

Run `python3 slow.py`; press Esc while the turn is active.

**The interrupted turn ID is saved.**

<p class="caption">Does not run for idle threads or children; cannot restart the turn.</p>

```sh
python3 codex-hooks-workshop/replay.py 10
```

<!--
Allow 2–5 minutes for this lab depending on event setup and discussion.
Full live action: Ask: Run `python3 slow.py` and wait for it to finish. Press Esc while the turn is active. Inspect .demo/interrupted.json.
Expected evidence: A local record contains the interrupted turn ID.
Caveat: No event for idle threads or subagents. Output cannot prevent interruption or restart the turn. Stopping a turn does not guarantee rollback of tool side effects.
Fallback: run replay.py 10 and identify the result as synthetic contract inspection, not a runtime recording. Reset only between closed demo sessions. See LIVE-CHECKLIST.md for rehearsal evidence.
Source: https://learn.chatgpt.com/docs/hooks
-->

---
class: compact
---

# 11 · Session end

**SessionEnd** · Record normal closure for local bookkeeping.

```json
{
  "session_id": "example-session",
  "reason": "other"
}
```

<p class="caption">Illustrative local marker; hook output is advisory.</p>

<!--
Main thread only. Switching chats is not immediate session end. Abrupt process termination is not a reliable trigger; output is advisory.
Show 11-session-end/hook.py (server.py for lab 16) and its hook configuration. Explain where the JSON fields differ from other events.
Send a brief prompt, wait for the reply, then exit Codex normally using `/quit`. Inspect .demo/session-ended.json from another terminal.
Source: https://learn.chatgpt.com/docs/hooks
-->

---
class: compact
---

# Live lab 11

```sh
sh codex-hooks-workshop/demo.sh 11
```

Send a prompt, wait for a reply, then exit normally with `/quit`.

**The main-session end marker records reason other.**

<p class="caption">A chat switch or abrupt kill is not a reliable immediate trigger.</p>

```sh
python3 codex-hooks-workshop/replay.py 11
```

<!--
Allow 2–5 minutes for this lab depending on event setup and discussion.
Full live action: Send a brief prompt, wait for the reply, then exit Codex normally using `/quit`. Inspect .demo/session-ended.json from another terminal.
Expected evidence: The session-end marker records reason other.
Caveat: Main thread only. Switching chats is not immediate session end. Abrupt process termination is not a reliable trigger; output is advisory.
Fallback: run replay.py 11 and identify the result as synthetic contract inspection, not a runtime recording. Reset only between closed demo sessions. See LIVE-CHECKLIST.md for rehearsal evidence.
Source: https://learn.chatgpt.com/docs/hooks
-->

---
class: compact
---

# 12 · Tool input rewriting

**PreToolUse** · Add a default option to a known demo command.

```json
{"hookSpecificOutput": {
  "hookEventName": "PreToolUse",
  "permissionDecision": "allow",
  "updatedInput": {
    "command": "python3 greet.py --name workshop"
  }
}}
```

<p class="caption">Response or mechanism excerpt; read the complete hook alongside it.</p>

<!--
updatedInput must accompany permissionDecision allow. Bash/apply_patch require a string command. Existing input fields are preserved.
Show 12-input-rewrite/hook.py (server.py for lab 16) and its hook configuration. Explain where the JSON fields differ from other events.
Ask: Run exactly `python3 greet.py` once.
Source: https://learn.chatgpt.com/docs/hooks
-->

---
class: compact
---

# Live lab 12

```sh
sh codex-hooks-workshop/demo.sh 12
```

Ask Codex to run exactly `python3 greet.py`.

**Hello, workshop!** comes from the rewritten command.

<p class="caption">Retain other input fields; rewrite only with decision allow.</p>

```sh
python3 codex-hooks-workshop/replay.py 12
```

<!--
Allow 2–5 minutes for this lab depending on event setup and discussion.
Full live action: Ask: Run exactly `python3 greet.py` once.
Expected evidence: Codex runs the replacement command and prints Hello, workshop! rather than Hello, default!.
Caveat: updatedInput must accompany permissionDecision allow. Bash/apply_patch require a string command. Existing input fields are preserved.
Fallback: run replay.py 12 and identify the result as synthetic contract inspection, not a runtime recording. Reset only between closed demo sessions. See LIVE-CHECKLIST.md for rehearsal evidence.
Source: https://learn.chatgpt.com/docs/hooks
-->

---
class: compact
---

# 13 · Post-tool feedback

**PostToolUse** · Replace feedback after a generator already ran.

```json
{
  "decision": "block",
  "reason": "Generator already ran. Report that review is needed."
}
```

<p class="caption">Response or mechanism excerpt; read the complete hook alongside it.</p>

<!--
A PostToolUse block cannot undo the generated file. Code-mode promises reject for decision:block or exit 2, but continue:false has different behavior.
Show 13-post-tool-feedback/hook.py (server.py for lab 16) and its hook configuration. Explain where the JSON fields differ from other events.
Ask: Run exactly `python3 generate.py` once, then report the outcome without rerunning it.
Source: https://learn.chatgpt.com/docs/hooks
-->

---
class: compact
---

# Live lab 13

```sh
sh codex-hooks-workshop/demo.sh 13
```

Run `python3 generate.py` once and inspect the generated file.

**File exists; the tool result becomes review feedback.**

<p class="caption">The hook cannot undo the completed generator.</p>

```sh
python3 codex-hooks-workshop/replay.py 13
```

<!--
Allow 2–5 minutes for this lab depending on event setup and discussion.
Full live action: Ask: Run exactly `python3 generate.py` once, then report the outcome without rerunning it.
Expected evidence: The generated file exists and Codex receives review feedback instead of the original result.
Caveat: A PostToolUse block cannot undo the generated file. Code-mode promises reject for decision:block or exit 2, but continue:false has different behavior.
Fallback: run replay.py 13 and identify the result as synthetic contract inspection, not a runtime recording. Reset only between closed demo sessions. See LIVE-CHECKLIST.md for rehearsal evidence.
Source: https://learn.chatgpt.com/docs/hooks
-->

---
class: compact
---

# 14 · Background execution

**PostToolUse** · Move informational work off the synchronous path.

```json
{
  "type": "command",
  "command": "python3 .../hook.py",
  "async": true,
  "timeout": 5
}
```

<p class="caption">Handler excerpt; full path is in the scenario config.</p>

<!--
async:true cannot block, allow, rewrite, or request continuation. Delivery waits for a safe point; if idle, the next user turn. Unfinished work is cancelled at session end.
Show 14-background-hook/hook.py (server.py for lab 16) and its hook configuration. Explain where the JSON fields differ from other events.
Ask: Run exactly `python3 hello.py` and briefly explain the result. Keep the session open; inspect .demo/background-finished.txt after a second.
Source: https://learn.chatgpt.com/docs/hooks
-->

---
class: compact
---

# Live lab 14

```sh
sh codex-hooks-workshop/demo.sh 14
```

Run `python3 hello.py` and keep the session open.

**A delayed completion marker appears.**

<p class="caption">Background output waits for a safe point or next user turn.</p>

```sh
python3 codex-hooks-workshop/replay.py 14
```

<!--
Allow 2–5 minutes for this lab depending on event setup and discussion.
Full live action: Ask: Run exactly `python3 hello.py` and briefly explain the result. Keep the session open; inspect .demo/background-finished.txt after a second.
Expected evidence: Foreground completes while a delayed hook records completion.
Caveat: async:true cannot block, allow, rewrite, or request continuation. Delivery waits for a safe point; if idle, the next user turn. Unfinished work is cancelled at session end.
Fallback: run replay.py 14 and identify the result as synthetic contract inspection, not a runtime recording. Reset only between closed demo sessions. See LIVE-CHECKLIST.md for rehearsal evidence.
Source: https://learn.chatgpt.com/docs/hooks
-->

---
class: compact
---

# 15 · File-edit guard

**PreToolUse** · Inspect an apply_patch call rather than shell execution.

```json
{
  "matcher": "^apply_patch$",
  "hooks": [{
    "type": "command",
    "command": "python3 .../hook.py"
  }]
}
```

<p class="caption">Matcher-group excerpt; event input still reports apply_patch.</p>

<!--
Narrow header check for the exact relative path only. Shell writes and alternate spellings are outside this example. apply_patch also matches Edit and Write aliases.
Show 15-edit-guard/hook.py (server.py for lab 16) and its hook configuration. Explain where the JSON fields differ from other events.
Ask: Use apply_patch to change protected.txt to Changed. If blocked, report the denial and do not try another tool. Then ask apply_patch to add notes.txt.
Source: https://learn.chatgpt.com/docs/hooks
-->

---
class: compact
---

# Live lab 15

```sh
sh codex-hooks-workshop/demo.sh 15
```

Use apply_patch to edit protected.txt, then add notes.txt.

**Protected patch denied; unrelated patch allowed.**

<p class="caption">Alternate paths and other write tools are outside this checker.</p>

```sh
python3 codex-hooks-workshop/replay.py 15
```

<!--
Allow 2–5 minutes for this lab depending on event setup and discussion.
Full live action: Ask: Use apply_patch to change protected.txt to Changed. If blocked, report the denial and do not try another tool. Then ask apply_patch to add notes.txt.
Expected evidence: The protected patch is denied; an unrelated patch is allowed.
Caveat: Narrow header check for the exact relative path only. Shell writes and alternate spellings are outside this example. apply_patch also matches Edit and Write aliases.
Fallback: run replay.py 15 and identify the result as synthetic contract inspection, not a runtime recording. Reset only between closed demo sessions. See LIVE-CHECKLIST.md for rehearsal evidence.
Source: https://learn.chatgpt.com/docs/hooks
-->

---
class: compact
---

# 16 · MCP tool handler

**PreToolUse** · Route a policy check through an existing local MCP connection.

```json
{
  "type": "mcp_tool",
  "server": "workshop_checker",
  "tool": "check_command",
  "input": { "command": "${tool_input.command}" },
  "timeout": 5
}
```

<p class="caption">Handler configuration; values are expanded from the hook event.</p>

<!--
The handler does not connect servers itself. Missing servers, tool errors, and timeouts do not block. MCP handlers are synchronous and cannot handle SessionEnd.
Show 16-mcp-handler/hook.py (server.py for lab 16) and its hook configuration. Explain where the JSON fields differ from other events.
Check `/mcp` shows workshop_checker connected, then ask for the exact simulated production deployment command from scenario 02.
Source: https://learn.chatgpt.com/docs/hooks
-->

---
class: compact
---

# Live lab 16

```sh
sh codex-hooks-workshop/demo.sh 16
```

Confirm the MCP connection, then run the production simulation.

**Local check_command returns the denial.**

<p class="caption">Missing server, tool error, or timeout does not block the operation.</p>

```sh
python3 codex-hooks-workshop/replay.py 16
```

<!--
Allow 2–5 minutes for this lab depending on event setup and discussion.
Full live action: Check `/mcp` shows workshop_checker connected, then ask for the exact simulated production deployment command from scenario 02.
Expected evidence: Local check_command returns a denial; .demo/events.jsonl records the decision.
Caveat: The handler does not connect servers itself. Missing servers, tool errors, and timeouts do not block. MCP handlers are synchronous and cannot handle SessionEnd.
Fallback: run replay.py 16 and identify the result as synthetic contract inspection, not a runtime recording. Reset only between closed demo sessions. See LIVE-CHECKLIST.md for rehearsal evidence.
Source: https://learn.chatgpt.com/docs/hooks
-->

---
class: compact
---

# 17 · Failure modes

**PreToolUse** · Compare explicit denial with hook failures.

```text
deny-exit    Exit 2 with a reason on stderr
error        Exit 1: hook failure
invalid-json Invalid JSON output
unsupported  PreToolUse continue:false
timeout     Seven-second script, five-second handler timeout
```

<p class="caption">Response or mechanism excerpt; read the complete hook alongside it.</p>

<!--
Do not use errors as a policy mechanism. This scenario is intentionally broken in some modes. Restore mode.txt to pass with reset before leaving it.
Show 17-failure-modes/hook.py (server.py for lab 16) and its hook configuration. Explain where the JSON fields differ from other events.
Keep mode.txt as pass initially. Ask for `python3 hello.py`. Then set mode.txt to deny-exit, error, invalid-json, unsupported, or timeout, review changes if prompted, and repeat the command.
Source: https://learn.chatgpt.com/docs/hooks
-->

---
class: compact
---

# Live lab 17

```sh
sh codex-hooks-workshop/demo.sh 17
```

Change mode.txt and repeat `python3 hello.py` for each mode.

**Explicit denial differs from failure or ignored output.**

<p class="caption">Restore pass mode afterward; do not rely on failure for policy.</p>

```sh
python3 codex-hooks-workshop/replay.py 17
```

<!--
Allow 2–5 minutes for this lab depending on event setup and discussion.
Full live action: Keep mode.txt as pass initially. Ask for `python3 hello.py`. Then set mode.txt to deny-exit, error, invalid-json, unsupported, or timeout, review changes if prompted, and repeat the command.
Expected evidence: Exit 2 is a policy denial; other modes show a failing hook or unsupported-field report. Fixtures show each response separately.
Caveat: Do not use errors as a policy mechanism. This scenario is intentionally broken in some modes. Restore mode.txt to pass with reset before leaving it.
Fallback: run replay.py 17 and identify the result as synthetic contract inspection, not a runtime recording. Reset only between closed demo sessions. See LIVE-CHECKLIST.md for rehearsal evidence.
Source: https://learn.chatgpt.com/docs/hooks
-->

---
class: compact
---

# 18 · Large context output

**SessionStart** · Demonstrate the context-output spill threshold with bounded synthetic text.

```json
{
  "type": "command",
  "command": "python3 .../hook.py",
  "additionalContextLimit": 64,
  "timeout": 5
}
```

<p class="caption">Handler excerpt; output is capped at 40 synthetic lines.</p>

<!--
The limit is approximate tokens, not bytes. Fixture playback verifies the text only; spilling and file references require live CLI delivery. Do not put secrets in hook output.
Show 18-large-context/hook.py (server.py for lab 16) and its hook configuration. Explain where the JSON fields differ from other events.
Launch a new session and ask: Read the startup reference preview and state its topic briefly without tools.
Source: https://learn.chatgpt.com/docs/hooks
-->

---
class: compact
---

# Live lab 18

```sh
sh codex-hooks-workshop/demo.sh 18
```

Start a new session and ask for the startup reference topic.

**Bounded context spills to a preview plus file reference.**

<p class="caption">The threshold is approximate tokens; fixtures do not test spilling.</p>

```sh
python3 codex-hooks-workshop/replay.py 18
```

<!--
Allow 2–5 minutes for this lab depending on event setup and discussion.
Full live action: Launch a new session and ask: Read the startup reference preview and state its topic briefly without tools.
Expected evidence: The hook returns 40 bounded synthetic reference lines; with additionalContextLimit 64, Codex should provide a shortened preview and saved-file reference.
Caveat: The limit is approximate tokens, not bytes. Fixture playback verifies the text only; spilling and file references require live CLI delivery. Do not put secrets in hook output.
Fallback: run replay.py 18 and identify the result as synthetic contract inspection, not a runtime recording. Reset only between closed demo sessions. See LIVE-CHECKLIST.md for rehearsal evidence.
Source: https://learn.chatgpt.com/docs/hooks
-->

---
class: compact
---

# Control outputs are event-specific

| Event | “Block” means |
| --- | --- |
| UserPromptSubmit | Reject the prompt |
| PreToolUse | Prevent the supported tool call |
| PostToolUse | Replace feedback after execution |
| Stop | Create a continuation turn |
| SubagentStop | Continue the child flow |

**PermissionRequest** uses `decision.behavior`, not permissionDecision.

<!--
Never copy a single generic output shape across every event. For Stop/SubagentStop, continue:false takes precedence over continuation requests. For PreToolUse, continue:false is unsupported and can result in a failure followed by execution. Compare lab 17 carefully.
Source: https://learn.chatgpt.com/docs/hooks
-->

---

# Background and concurrent handlers

- Matching synchronous commands also launch concurrently
- Background handlers deliver information at a safe point
- Background hooks cannot control the triggering operation
- Up to eight background hooks run per session
- Session end cancels unfinished background work

**SessionEnd itself remains synchronous.**

<!--
Do not treat config order as a dependency graph. If one step must precede another, perform both inside one script. Use synchronous handlers for denial, approval, rewriting, prompt rejection, and continuations. Delayed output while idle does not initiate a new turn.
Source: https://learn.chatgpt.com/docs/hooks
-->

---
class: compact
---

# Handler and configuration choices

| Choice | Use |
| --- | --- |
| command | Local script receiving event JSON |
| mcp_tool | Callback on an existing connection |
| JSON or inline TOML | Equivalent config representations |
| Plugin hooks | Bundle scripts and configuration |

**prompt / agent handlers are parsed but skipped.**

<!--
Inactive examples are under reference/. The plugin example uses PLUGIN_ROOT. PLUGIN_DATA is writable plugin storage; compatibility aliases also exist. No global configuration or plugin is installed automatically. Managed configuration and cloud orchestration have different operational rules; the executable scope here is local Codex CLI.
Source: https://learn.chatgpt.com/docs/hooks
-->

---
class: compact
---

# Defaults and boundaries

- Keep context concise; the default spill threshold is about 2,500 tokens
- Use explicit short timeouts for demo scripts
- Interrupt permits 1–3 seconds; SessionEnd has a short budget
- Treat malformed output as a failure, not an explicit policy decision
- Avoid parsing transcript files as a stable API

**Read the contract for the exact event and CLI release.**

<!--
SessionEnd defaults to one second and permits up to three; most other command hooks default to 600 seconds, which is far too long for a live workshop. additionalContextLimit zero disables spilling and should only be used with a strict output cap. Unsupported PermissionRequest fields can fail closed, while some PreToolUse invalid outputs fail without blocking; never generalize one failure mode.
Source: https://learn.chatgpt.com/docs/hooks
-->

---
class: compact
---

# Choosing what to automate

| Need | Starting point |
| --- | --- |
| Persistent conventions | AGENTS.md |
| Runtime context | SessionStart / UserPromptSubmit |
| Tool checks | PreToolUse / PermissionRequest |
| Visibility | PostToolUse / model request hooks |
| Verification | Stop / SubagentStop |
| Bookkeeping | Compaction / Interrupt / SessionEnd |

<!--
Ask the audience to identify the lifecycle point for one current workflow. Separate instructional guidance from runtime actions. A useful first hook is small, observable, and has tested failure behavior. These sample checkers are deliberately narrow and not enterprise enforcement policies.
Source: https://learn.chatgpt.com/docs/hooks
-->

---
class: compact
---

# Sources and next steps

[Official hook contracts](https://learn.chatgpt.com/docs/hooks) · [Configuration](https://learn.chatgpt.com/docs/config-file/config-basic)

[Plugin packaging](https://developers.openai.com/plugins/build/plugins) · [Slidev](https://github.com/slidevjs/slidev)

**In this repository**

- COVERAGE.md — complete event and behavior matrix
- Each scenario README — exact prompt and observable evidence
- LIVE-CHECKLIST.md — record actual runtime rehearsal
- replay.py — isolated synthetic contract inspection

<!--
Official documentation consulted 2026-11-04. The 14 event names also appear in the local 0.166.0 generated app-server ManagedHooksRequirements schema; see reference/support-snapshot.json. Schema and fixture checks do not prove live delivery. MCP server protocol references: https://modelcontextprotocol.io/specification/2025-11-25/basic/transports and https://modelcontextprotocol.io/specification/2025-11-25/server/tools. Source for slide authoring: https://sli.dev/guide/syntax.html. Follow the rehearsal checklist before presenting.
Source: https://learn.chatgpt.com/docs/hooks
-->
