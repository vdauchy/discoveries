from pathlib import Path
Path(__file__).with_name(".demo").mkdir(exist_ok=True)
Path(__file__).with_name(".demo").joinpath("write-marker.txt").write_text("Local simulation only.\n")
print("Local marker written.")
