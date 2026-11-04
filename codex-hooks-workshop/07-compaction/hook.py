"""07-compaction — educational hook; see README for runtime limitations."""
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

event = payload["hook_event_name"]
if event == "PreCompact":
    checkpoint = {"task": "Investigate a synthetic failing test", "next_step": "Run the focused test"}
    (state / "checkpoint.json").write_text(json.dumps(checkpoint))
    print(json.dumps({"systemMessage": "Demo checkpoint saved before compaction."}))
elif event == "PostCompact":
    print(json.dumps({"systemMessage": "Compaction finished; inspect .demo/checkpoint.json."}))
else:  # SessionStart with source compact: restore context through its supported contract.
    checkpoint = state / "checkpoint.json"
    context = checkpoint.read_text() if checkpoint.exists() else "No demo checkpoint exists yet."
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": context}}))
