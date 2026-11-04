"""PostToolUse: record metadata after a command has completed."""
from datetime import datetime, timezone
import json
from pathlib import Path
import sys

payload = json.load(sys.stdin)
record = {
    "event": payload["hook_event_name"],
    "tool": payload["tool_name"],
    "session_id": payload["session_id"],
    "timestamp": datetime.now(timezone.utc).isoformat(),
}
# One short append per invocation; no commands, prompts, or outputs are logged.
with (Path(__file__).parent / "events.jsonl").open("a") as log:
    log.write(json.dumps(record) + "\n")
print("{}")
