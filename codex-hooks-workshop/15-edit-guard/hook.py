"""15-edit-guard — educational hook; see README for runtime limitations."""
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

# Narrow patch-header check: other edit mechanisms are not covered.
patch = payload["tool_input"].get("command", "")
headers = ("*** Update File: protected.txt", "*** Delete File: protected.txt", "*** Add File: protected.txt")
if any(line.strip() in headers for line in patch.splitlines()):
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse",
        "permissionDecision": "deny", "permissionDecisionReason": "Demo: protected.txt must remain unchanged."}}))
else:
    print("{}")
