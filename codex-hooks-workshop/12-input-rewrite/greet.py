import argparse
p = argparse.ArgumentParser()
p.add_argument("--name", default="default")
print(f"Hello, {p.parse_args().name}!")
