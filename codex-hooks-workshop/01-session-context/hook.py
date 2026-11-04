"""SessionStart: calculate context before the model starts."""
import json
from pathlib import Path
import sys

payload = json.load(sys.stdin)
environment = (Path(__file__).parent / "environment.txt").read_text().strip()
print(json.dumps({"hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": f"The selected workshop deployment environment is {environment}."
}}))
