"""17-failure-modes — educational hook; see README for runtime limitations."""
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

mode = (folder / "mode.txt").read_text().strip()
if mode == "deny-exit":
    print("Deliberate demo denial via exit 2.", file=sys.stderr)
    sys.exit(2)
if mode == "error":
    print("Deliberate demo failure, not a policy decision.", file=sys.stderr)
    sys.exit(1)
if mode == "invalid-json":
    print("{broken json")
elif mode == "unsupported":
    print(json.dumps({"continue": False}))  # Unsupported on PreToolUse.
elif mode == "timeout":
    import time
    time.sleep(7)  # Deliberately exceeds the configured five seconds.
    print("{}")
else:
    print("{}")
