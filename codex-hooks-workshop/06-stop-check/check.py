from pathlib import Path
import sys
value = Path(__file__).with_name("answer.txt").read_text().strip()
print("PASS" if value == "42" else "FAIL: answer.txt must contain 42")
sys.exit(0 if value == "42" else 1)
