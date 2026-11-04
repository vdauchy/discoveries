"""Minimal local MCP stdio server for the hooks workshop, not a production SDK."""
import json
from pathlib import Path
import sys

SUPPORTED = ("2025-11-25", "2025-06-18", "2025-03-26", "2024-11-05")

def dispatch(method, params):
    if method == "initialize":
        version = params.get("protocolVersion")
        return {"protocolVersion": version if version in SUPPORTED else SUPPORTED[0],
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "workshop-checker", "version": "1.0.0"}}
    if method == "ping":
        return {}
    if method == "tools/list":
        return {"tools": [{"name": "check_command", "description": "Check a synthetic workshop command.",
            "inputSchema": {"type": "object", "properties": {"command": {"type": "string"}},
                            "required": ["command"], "additionalProperties": False}}]}
    if method == "tools/call":
        if params.get("name") != "check_command":
            raise ValueError("Unknown tool")
        args = params.get("arguments", {})
        if not isinstance(args.get("command"), str):
            raise ValueError("command must be a string")
        import shlex
        try:
            denied = shlex.split(args["command"]) == ["python3", "deploy.py", "--env", "production"]
        except ValueError:
            denied = False
        output = {"hookSpecificOutput": {"hookEventName": "PreToolUse",
            "permissionDecision": "deny", "permissionDecisionReason": "Local MCP policy denied production simulation."}} if denied else {}
        state = Path(__file__).parent / ".demo"
        state.mkdir(exist_ok=True)
        with (state / "events.jsonl").open("a") as log:
            log.write(json.dumps({"event": "mcp_policy_check", "denied": denied}) + "\n")
        return {"content": [{"type": "text", "text": json.dumps(output)}],
                "structuredContent": output, "isError": False}
    raise LookupError("Method not found")

for line in sys.stdin:
    request = None
    try:
        request = json.loads(line)
        if "id" not in request:  # notifications never get responses
            continue
        result = dispatch(request["method"], request.get("params", {}))
        response = {"jsonrpc": "2.0", "id": request["id"], "result": result}
    except Exception as error:
        response = {"jsonrpc": "2.0", "id": request.get("id") if isinstance(request, dict) else None,
                    "error": {"code": -32601 if isinstance(error, LookupError) else -32602,
                              "message": str(error)}}
    print(json.dumps(response), flush=True)
