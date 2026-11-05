"""Inspect synthetic hook contracts in isolated copies; never claims runtime delivery."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent

def subset(expected, actual):
    if isinstance(expected, dict):
        return isinstance(actual, dict) and all(key in actual and subset(value, actual[key]) for key, value in expected.items())
    return expected == actual

def run_case(scenario, case):
    with tempfile.TemporaryDirectory(prefix="codex-hook-fixture-") as temp:
        folder = Path(temp) / scenario.name
        shutil.copytree(scenario, folder, ignore=shutil.ignore_patterns(".demo", "__pycache__", "events.jsonl", "deployment-*.txt"))
        for name, value in case.get("prepare", {}).items():
            target = folder / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(value)
        payload = dict(case["input"], cwd=str(folder))
        if case.get("handler") == "mcp":
            messages = [
                {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-11-25", "capabilities": {}, "clientInfo": {"name": "fixture", "version": "1"}}},
                {"jsonrpc": "2.0", "method": "notifications/initialized"},
                {"jsonrpc": "2.0", "id": 2, "method": "tools/list"},
                {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "check_command", "arguments": {"command": payload["tool_input"]["command"]}}}]
            script, stdin = "server.py", "\n".join(json.dumps(m) for m in messages) + "\n"
        else:
            script, stdin = "hook.py", json.dumps(payload)
        try:
            result = subprocess.run([sys.executable, str(folder / script)], input=stdin,
                capture_output=True, text=True, cwd=folder, timeout=5)
        except subprocess.TimeoutExpired:
            if case.get("timeout"):
                return {"case": case["name"], "timeout": True}
            raise
        if case.get("timeout"):
            raise AssertionError("Expected timeout")
        assert result.returncode == case.get("exit", 0), result.stderr
        assert case.get("stderr_contains", "") in result.stderr, result.stderr
        output = None
        if result.returncode == 0:
            try:
                output = json.loads(result.stdout) if case.get("handler") != "mcp" else None
                if case.get("handler") == "mcp":
                    responses = [json.loads(line) for line in result.stdout.splitlines()]
                    assert len(responses) == 3
                    assert responses[0]["result"]["protocolVersion"] == "2025-11-25"
                    assert responses[1]["result"]["tools"][0]["name"] == "check_command"
                    output = json.loads(responses[2]["result"]["content"][0]["text"])
                    assert output == responses[2]["result"]["structuredContent"]
                assert not case.get("invalid_json"), "Expected invalid JSON"
            except json.JSONDecodeError:
                assert case.get("invalid_json"), result.stdout
            if not case.get("invalid_json"):
                assert subset(case.get("expected", {}), output), (case["expected"], output)
                if case.get("expected", {}) == {}:
                    assert output == {}, output
        for name in case.get("files", []):
            assert (folder / name).is_file(), name
        for log in folder.rglob("*.jsonl"):
            for line in log.read_text().splitlines():
                json.loads(line)
        return {"case": case["name"], "exit": result.returncode,
                "stdout": result.stdout.strip(), "stderr": result.stderr.strip()}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scenario", help="Directory name, manifest ID, or all")
    args = parser.parse_args()
    from demo import discover
    try:
        scenarios = discover()
    except ValueError as error:
        parser.error(str(error))
    selected = [ROOT / item["directory"] for item in scenarios
                if args.scenario in ("all", item["directory"], item["id"])]
    if not selected:
        parser.error("Unknown scenario")
    count = 0
    for folder in selected:
        for case in json.loads((folder / "fixtures.json").read_text()):
            print(folder.name, json.dumps(run_case(folder, case)))
            count += 1
    print(f"{count} fixture cases passed. Synthetic playback only; no CLI trust, matching, or delivery tested.")

if __name__ == "__main__":
    main()
