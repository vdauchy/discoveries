"""06-stop-check — educational hook; see README for runtime limitations."""
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

import subprocess
check = subprocess.run([sys.executable, str(folder / "check.py")], capture_output=True, text=True, timeout=2)
if check.returncode == 0:
    print("{}")
elif payload.get("stop_hook_active"):
    # Bounded demo: never request an unending series of continuations.
    print(json.dumps({"systemMessage": "Check still fails after continuation; stopping this demo retry."}))
else:
    print(json.dumps({"decision": "block", "reason":
        "Workshop check failed. Set answer.txt to 42, run python3 check.py, then report the result."}))
