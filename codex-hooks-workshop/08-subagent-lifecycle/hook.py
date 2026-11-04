"""08-subagent-lifecycle — educational hook; see README for runtime limitations."""
import json
from pathlib import Path
import sys
from datetime import datetime, timezone

payload = json.load(sys.stdin)
folder = Path(__file__).resolve().parent
state = folder / ".demo"
state.mkdir(exist_ok=True)
record = {"event": payload["hook_event_name"], "session_id": payload["session_id"],
          "timestamp": datetime.now(timezone.utc).isoformat()}
for key in ("source", "trigger", "reason", "turn_id", "agent_id", "agent_type", "model", "status"):
    if key in payload:
        record[key] = payload[key]
with (state / "events.jsonl").open("a") as log:
    log.write(json.dumps(record) + "\n")

if payload["hook_event_name"] == "SubagentStart":
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "SubagentStart",
        "additionalContext": "Workshop reviewer: end your report with Tests: and what you verified or did not run."}}))
elif "tests:" in (payload.get("last_assistant_message") or "").lower():
    print("{}")
elif payload.get("stop_hook_active"):
    print(json.dumps({"systemMessage": "Reviewer still omitted Tests; demo retry limit reached."}))
else:
    print(json.dumps({"decision": "block", "reason": "Add a Tests: line stating what you verified or did not run."}))
