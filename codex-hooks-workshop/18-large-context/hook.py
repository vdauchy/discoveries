"""Bounded synthetic context to demonstrate output spilling."""
import json
import sys
payload = json.load(sys.stdin)
context = "\n".join(
    f"Synthetic reference item {i:02}: inspect a small focused test before changing behavior."
    for i in range(40)
)
print(json.dumps({"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": context}}))
