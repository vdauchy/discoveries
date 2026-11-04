"""09-model-requests — educational hook; see README for runtime limitations."""
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

# Diagnostic only: no model context or request control output.
if payload["hook_event_name"] == "PostModelRequest":
    outcome = {"status": payload["status"], "token_usage": payload.get("token_usage")}
    # Do not store raw error strings: they may contain sensitive provider details.
    outcome["has_error"] = bool(payload.get("error"))
    with (state / "outcomes.jsonl").open("a") as log:
        log.write(json.dumps(outcome) + "\n")
print("{}")
