"""Reset only known workshop outputs and the three demo control files."""
from pathlib import Path
import shutil

root = Path(__file__).resolve().parent
for manifest in root.glob("*/manifest.json"):
    folder = manifest.parent
    if not folder.is_dir() or folder.is_symlink():
        continue
    state = folder / ".demo"
    if state.is_symlink():
        state.unlink()
    elif state.is_dir():
        shutil.rmtree(state)
    for name in ("events.jsonl", "deployment-staging.txt", "deployment-production.txt"):
        (folder / name).unlink(missing_ok=True)
(root / "15-edit-guard/notes.txt").unlink(missing_ok=True)
for relative, baseline in [("06-stop-check/answer.txt", "41\n"),
                           ("05-permission-request/policy.txt", "deny\n"),
                           ("17-failure-modes/mode.txt", "pass\n")]:
    path = root / relative
    if path.is_file() and not path.is_symlink():
        path.write_text(baseline)
print("Reset demo outputs, answer, permission policy, and failure mode.")
