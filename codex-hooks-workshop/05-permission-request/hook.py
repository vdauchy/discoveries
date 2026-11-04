"""05-permission-request — educational hook; see README for runtime limitations."""
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

import shlex
try:
    tokens = shlex.split(payload["tool_input"].get("command", ""))
except ValueError:
    tokens = []
result = {}
# Only this local simulation is eligible for a decision.
if tokens == ["python3", "write_marker.py"]:
    policy = (folder / "policy.txt").read_text().strip()
    if policy in ("allow", "deny"):
        result = {"hookSpecificOutput": {"hookEventName": "PermissionRequest",
            "decision": {"behavior": policy}}}
        if policy == "deny":
            result["hookSpecificOutput"]["decision"]["message"] = "Demo policy denies this requested write."
print(json.dumps(result))
