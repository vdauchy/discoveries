"""PreToolUse: a deliberately narrow check for the demonstrated command."""
import json
import shlex
import sys

payload = json.load(sys.stdin)
command = payload.get("tool_input", {}).get("command", "")
try:
    tokens = shlex.split(command)
except ValueError:
    tokens = []
# This is a teaching example, not a general shell parser or security boundary.
if tokens == ["python3", "deploy.py", "--env", "production"]:
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": "Workshop policy: production deployment is blocked. Use staging."
    }}))
else:
    print("{}")
