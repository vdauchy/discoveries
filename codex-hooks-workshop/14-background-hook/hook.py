"""14-background-hook — educational hook; see README for runtime limitations."""
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

import time
time.sleep(1)
(state / "background-finished.txt").write_text("Background demo completed.\n")
print(json.dumps({"hookSpecificOutput": {"hookEventName": "PostToolUse",
    "additionalContext": "The background demo completed. See .demo/background-finished.txt."}}))
