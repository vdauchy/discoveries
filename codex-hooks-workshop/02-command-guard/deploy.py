"""A simulation: no network requests or actual deployments."""
import argparse
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--env", choices=["staging", "production"], required=True)
args = parser.parse_args()
(Path(__file__).parent / f"deployment-{args.env}.txt").write_text("Simulated deployment only.\n")
print(f"Simulated {args.env} deployment completed.")
