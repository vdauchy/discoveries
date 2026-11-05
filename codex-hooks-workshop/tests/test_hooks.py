import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]

class Hooks(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        for scenario in ROOT.glob("0*"):
            shutil.copytree(scenario, self.root / scenario.name)

    def call(self, scenario, event, command=""):
        payload = {"hook_event_name": event, "session_id": "test-session",
                   "cwd": str(self.root / scenario), "tool_name": "Bash",
                   "tool_input": {"command": command}}
        result = subprocess.run(["python3", str(self.root / scenario / "hook.py")],
            input=json.dumps(payload), text=True, capture_output=True, check=True)
        return json.loads(result.stdout)

    def test_context_reads_environment(self):
        folder = self.root / "01-session-context"
        (folder / "environment.txt").write_text("development\n")
        result = self.call(folder.name, "SessionStart")
        self.assertIn("development", result["hookSpecificOutput"]["additionalContext"])

    def test_production_denied_staging_allowed(self):
        scenario = "02-command-guard"
        result = self.call(scenario, "PreToolUse", "python3 deploy.py --env production")
        self.assertEqual(result["hookSpecificOutput"]["permissionDecision"], "deny")
        self.assertEqual(self.call(scenario, "PreToolUse", "python3 deploy.py --env staging"), {})
        self.assertEqual(self.call(scenario, "PreToolUse", "python3 hello.py"), {})
        self.assertFalse((self.root / scenario / "deployment-production.txt").exists())
        subprocess.run(["python3", str(self.root / scenario / "deploy.py"), "--env", "staging"],
                       capture_output=True, check=True)
        self.assertTrue((self.root / scenario / "deployment-staging.txt").exists())

    def test_log_appends_metadata_only(self):
        scenario = "03-tool-log"
        for _ in range(2):
            self.assertEqual(self.call(scenario, "PostToolUse", "do not log this"), {})
        entries = [json.loads(line) for line in (self.root / scenario / "events.jsonl").read_text().splitlines()]
        self.assertEqual(len(entries), 2)
        self.assertEqual(set(entries[0]), {"event", "tool", "session_id", "timestamp"})
        self.assertEqual(entries[0]["event"], "PostToolUse")

    def test_configuration(self):
        for path in [ROOT / name / ".codex/hooks.json" for name in ("01-session-context", "02-command-guard", "03-tool-log")]:
            config = json.loads(path.read_text())
            self.assertEqual(len(config["hooks"]), 1)
            for groups in config["hooks"].values():
                self.assertEqual(groups[0]["hooks"][0]["timeout"], 5)

    def test_reset_preserves_sources(self):
        shutil.copy(ROOT / "demo.sh", self.root / "demo.sh")
        shutil.copy(ROOT / "demo.py", self.root / "demo.py")
        shutil.copy(ROOT / "reset.py", self.root / "reset.py")
        marker = self.root / "02-command-guard/deployment-staging.txt"
        marker.write_text("generated")
        subprocess.run(["sh", str(self.root / "demo.sh"), "reset"], capture_output=True, check=True)
        self.assertFalse(marker.exists())
        self.assertTrue((self.root / "02-command-guard/deploy.py").exists())

if __name__ == "__main__":
    unittest.main()
