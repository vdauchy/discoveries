"""04-prompt-filter — educational hook; see README for runtime limitations."""
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

# A synthetic marker, never a real credential.
if "DEMO_SECRET_123" in payload["prompt"]:
    print(json.dumps({"decision": "block", "reason": "Remove the synthetic secret marker before submitting."}))
else:
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "UserPromptSubmit",
        "additionalContext": "Workshop: explain the reasoning behind any suggested change briefly."}}))
