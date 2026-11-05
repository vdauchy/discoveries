"""Behavior and coverage checks; no model calls or CLI trust bypass."""
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("replay", ROOT / "replay.py")
replay = importlib.util.module_from_spec(spec)
spec.loader.exec_module(replay)
demo_spec = importlib.util.spec_from_file_location("demo", ROOT / "demo.py")
demo = importlib.util.module_from_spec(demo_spec)
demo_spec.loader.exec_module(demo)

SUPPORTED = {"SessionStart", "SessionEnd", "UserPromptSubmit", "PreToolUse", "PermissionRequest",
             "PostToolUse", "PreModelRequest", "PostModelRequest", "PreCompact", "PostCompact",
             "SubagentStart", "SubagentStop", "Stop", "Interrupt"}

class Coverage(unittest.TestCase):
    def test_all_supported_events_have_config_fixture_and_guide(self):
        configured, fixtures = set(), set()
        scenarios = demo.discover()
        self.assertEqual(len(scenarios), 18)
        for item in scenarios:
            folder = ROOT / item["directory"]
            self.assertTrue((folder / "README.md").exists())
            hooks = json.loads((folder / ".codex/hooks.json").read_text())["hooks"]
            self.assertEqual(set(item["events"]), set(hooks))
            configured.update(hooks)
            cases = json.loads((folder / "fixtures.json").read_text())
            fixtures.update(case["input"]["hook_event_name"] for case in cases)
            for event, groups in hooks.items():
                for group in groups:
                    if event in ("UserPromptSubmit", "Stop", "Interrupt", "PreModelRequest", "PostModelRequest"):
                        self.assertNotIn("matcher", group)
                    for handler in group["hooks"]:
                        self.assertIn(handler["type"], ("command", "mcp_tool"))
                        self.assertLessEqual(handler["timeout"], 5)
                        if event in ("Interrupt", "SessionEnd"):
                            self.assertLessEqual(handler["timeout"], 3)
                        if event == "SessionEnd":
                            self.assertEqual(handler["type"], "command")
                    matching = [c for c in cases if c["input"]["hook_event_name"] == event]
                    self.assertTrue(matching, event)
                    key = {"SessionStart": "source", "SessionEnd": "reason", "PreCompact": "trigger",
                           "PostCompact": "trigger", "PreToolUse": "tool_name", "PostToolUse": "tool_name",
                           "PermissionRequest": "tool_name", "SubagentStart": "agent_type", "SubagentStop": "agent_type"}.get(event)
                    if key and group.get("matcher"):
                        self.assertTrue(any(re.search(group["matcher"], c["input"].get(key, "")) for c in matching))
        snapshot = json.loads((ROOT / "reference/support-snapshot.json").read_text())
        self.assertEqual(set(snapshot["event_names"]), SUPPORTED)
        self.assertEqual(configured, SUPPORTED)
        self.assertEqual(fixtures, SUPPORTED)

    def test_synthetic_contracts(self):
        for item in demo.discover():
            folder = ROOT / item["directory"]
            for case in json.loads((folder / "fixtures.json").read_text()):
                with self.subTest(scenario=folder.name, case=case["name"]):
                    replay.run_case(folder, case)

    def test_launcher_selects_each_scenario(self):
        with tempfile.TemporaryDirectory() as temp:
            fake = Path(temp) / "codex"
            fake.write_text('#!/bin/sh\nprintf "%s\\n" "$@"\n')
            fake.chmod(0o755)
            import os
            env = dict(os.environ, PATH=temp + os.pathsep + os.environ["PATH"])
            for item in demo.discover():
                result = subprocess.run(["sh", str(ROOT / "demo.sh"), item["id"]], env=env,
                    capture_output=True, text=True, check=True)
                args = result.stdout.splitlines()
                self.assertEqual(args[-1], str(ROOT / item["directory"]))
                if item["id"] == "05":
                    self.assertIn("read-only", args)
                    self.assertIn("on-request", args)

if __name__ == "__main__":
    unittest.main()
