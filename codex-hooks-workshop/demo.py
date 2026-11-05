"""Discover scenario manifests and launch the selected local Codex session."""
import argparse
import json
import os
from pathlib import Path
import re
import shutil
import sys

ROOT = Path(__file__).resolve().parent
ALIASES = {"context": "01", "block": "02", "log": "03"}
TEXT_FIELDS = ("id", "directory", "title", "use_case", "action", "evidence", "caveat")


def discover(root=ROOT):
    """Read immediate child manifests; reject ambiguous or inconsistent cases."""
    scenarios = []
    ids = set()
    for path in sorted(root.glob("*/manifest.json")):
        folder = path.parent
        if folder.is_symlink() or path.is_symlink():
            raise ValueError(f"{path}: scenario manifests must be local files")
        try:
            item = json.loads(path.read_text())
            if not isinstance(item, dict):
                raise ValueError("manifest must contain an object")
            for field in TEXT_FIELDS:
                if not isinstance(item.get(field), str) or not item[field].strip():
                    raise ValueError(f"{field} must be a non-empty string")
            if not re.fullmatch(r"[0-9]{2,}", item["id"]):
                raise ValueError("id must contain at least two digits")
            if item["directory"] != folder.name:
                raise ValueError("directory must match the containing folder name")
            if item["id"] in ids:
                raise ValueError(f"duplicate scenario id {item['id']}")
            events = item.get("events")
            if not isinstance(events, list) or not events or not all(isinstance(e, str) and e for e in events):
                raise ValueError("events must be a non-empty list of event names")
            if len(set(events)) != len(events):
                raise ValueError("events must not contain duplicates")
            hooks = json.loads((folder / ".codex/hooks.json").read_text()).get("hooks")
            if not isinstance(hooks, dict) or set(events) != set(hooks):
                raise ValueError("events must match the keys in .codex/hooks.json")
            launch = item.get("launch", {})
            if not isinstance(launch, dict) or set(launch) - {"sandbox", "approval"}:
                raise ValueError("launch supports only sandbox and approval")
            if "sandbox" in launch and launch["sandbox"] not in ("read-only", "workspace-write"):
                raise ValueError("unsupported launch sandbox")
            if "approval" in launch and launch["approval"] not in ("on-request", "never"):
                raise ValueError("unsupported launch approval policy")
        except (OSError, ValueError, AttributeError) as error:
            raise ValueError(f"{path}: {error}") from error
        ids.add(item["id"])
        scenarios.append(item)
    return sorted(scenarios, key=lambda item: (int(item["id"]), item["id"]))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scenario", help="Scenario ID, list, reset, context, block, or log")
    args = parser.parse_args(argv)
    if args.scenario == "reset":
        os.execv(sys.executable, [sys.executable, str(ROOT / "reset.py")])
    try:
        scenarios = discover()
    except ValueError as error:
        parser.exit(2, f"Error: {error}\n")
    if args.scenario == "list":
        for item in scenarios:
            print(item["id"], item["title"], "(" + ", ".join(item["events"]) + ")")
        return
    selected = ALIASES.get(args.scenario, args.scenario)
    item = next((item for item in scenarios if item["id"] == selected), None)
    if item is None:
        parser.exit(2, f"Unknown scenario: {selected}. Run ./demo.sh list.\n")
    executable = shutil.which("codex")
    if executable is None:
        parser.exit(2, "Install Codex CLI first.\n")
    command = [executable, "--no-daemon"]
    launch = item.get("launch", {})
    if "sandbox" in launch:
        command += ["-s", launch["sandbox"]]
    if "approval" in launch:
        command += ["-a", launch["approval"]]
    command += ["-C", str(ROOT / item["directory"])]
    os.execv(executable, command)


if __name__ == "__main__":
    main()
