"""Scenario discovery and launcher compatibility, without a live Codex session."""
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("demo", ROOT / "demo.py")
demo = importlib.util.module_from_spec(spec)
spec.loader.exec_module(demo)


class Discovery(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(prefix="hook-discovery-")
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        for name in ("demo.sh", "demo.py", "reset.py"):
            shutil.copy(ROOT / name, self.root / name)

    def make_case(self, identifier="19", directory="extra-case"):
        folder = self.root / directory
        (folder / ".codex").mkdir(parents=True)
        item = dict(demo.discover()[1], id=identifier, directory=directory, title="Additional case")
        item.pop("launch", None)
        (folder / "manifest.json").write_text(json.dumps(item))
        hooks = {"hooks": {"PreToolUse": [{"hooks": [
            {"type": "command", "command": "python3 hook.py", "timeout": 5}]}]}}
        (folder / ".codex/hooks.json").write_text(json.dumps(hooks))
        (folder / "hook.py").write_text('print("{}")\n')
        return folder

    def invoke(self, *args, **kwargs):
        return subprocess.run(["sh", str(self.root / "demo.sh"), *args],
                              capture_output=True, text=True, **kwargs)

    def fake_codex(self):
        binary = self.root / "bin"
        binary.mkdir()
        fake = binary / "codex"
        fake.write_text('#!/bin/sh\nprintf "%s\\n" "$@"\n')
        fake.chmod(0o755)
        return dict(os.environ, PATH=str(binary) + os.pathsep + os.environ["PATH"])

    def test_new_directory_is_listed_and_launched_without_registration(self):
        folder = self.make_case()
        env = self.fake_codex()
        result = self.invoke("list", env=env, cwd="/tmp")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("19 Additional case (PreToolUse)", result.stdout)
        result = self.invoke("19", env=env, cwd="/tmp")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.splitlines(), ["--no-daemon", "-C", str(folder)])

    def test_duplicate_ids_are_rejected(self):
        self.make_case(directory="first")
        self.make_case(directory="second")
        result = self.invoke("list")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("duplicate scenario id 19", result.stderr)

    def test_directory_mismatch_is_rejected(self):
        folder = self.make_case()
        path = folder / "manifest.json"
        item = json.loads(path.read_text())
        item["directory"] = "../elsewhere"
        path.write_text(json.dumps(item))
        result = self.invoke("19")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("directory must match", result.stderr)

    def test_malformed_manifest_is_reported(self):
        folder = self.make_case()
        (folder / "manifest.json").write_text("{broken")
        result = self.invoke("list")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("manifest.json", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_event_mismatch_is_rejected(self):
        folder = self.make_case()
        path = folder / "manifest.json"
        item = json.loads(path.read_text())
        item["events"] = ["Stop"]
        path.write_text(json.dumps(item))
        result = self.invoke("list")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("events must match", result.stderr)

    def test_missing_metadata_is_rejected(self):
        folder = self.make_case()
        path = folder / "manifest.json"
        item = json.loads(path.read_text())
        del item["title"]
        path.write_text(json.dumps(item))
        self.assertIn("title must be", self.invoke("list").stderr)

    def test_unknown_id_and_unregistered_folders(self):
        (self.root / "unregistered").mkdir()
        self.assertEqual(demo.discover(self.root), [])
        result = self.invoke("99")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Unknown scenario: 99", result.stderr)

    def test_launch_settings_come_from_manifest_not_id(self):
        folder = self.make_case()
        path = folder / "manifest.json"
        item = json.loads(path.read_text())
        item["launch"] = {"sandbox": "read-only", "approval": "on-request"}
        path.write_text(json.dumps(item))
        result = self.invoke("19", env=self.fake_codex())
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.splitlines(), [
            "--no-daemon", "-s", "read-only", "-a", "on-request", "-C", str(folder)])

    def test_bad_launch_settings_are_rejected(self):
        folder = self.make_case()
        path = folder / "manifest.json"
        item = json.loads(path.read_text())
        item["launch"] = {"arguments": ["--unexpected"]}
        path.write_text(json.dumps(item))
        self.assertIn("launch supports only", self.invoke("19").stderr)

    def test_existing_aliases_still_select_the_same_cases(self):
        for identifier, alias in (("01", "context"), ("02", "block"), ("03", "log")):
            self.make_case(identifier, "case-" + identifier)
        env = self.fake_codex()
        for identifier, alias in (("01", "context"), ("02", "block"), ("03", "log")):
            self.assertEqual(self.invoke(identifier, env=env).stdout, self.invoke(alias, env=env).stdout)

    def test_reset_cleans_a_discovered_directory(self):
        folder = self.make_case()
        (folder / ".demo").mkdir()
        marker = folder / ".demo/output.txt"
        marker.write_text("generated")
        result = self.invoke("reset")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(marker.exists())
        self.assertTrue((folder / "manifest.json").exists())


if __name__ == "__main__":
    unittest.main()
