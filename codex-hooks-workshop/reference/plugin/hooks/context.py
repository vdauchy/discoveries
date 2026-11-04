"""Inactive packaging example; hook trust is still required after installation."""
import json
import os
print(json.dumps({"hookSpecificOutput": {"hookEventName": "SessionStart",
    "additionalContext": "Plugin context loaded from " + os.environ["PLUGIN_ROOT"]}}))
