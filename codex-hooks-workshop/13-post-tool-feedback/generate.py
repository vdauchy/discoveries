from pathlib import Path
p = Path(__file__).with_name(".demo")
p.mkdir(exist_ok=True)
(p / "generated.txt").write_text("Synthetic generated content.\n")
print("Generated content successfully.")
