#!/bin/sh
set -eu
BASE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
case "${1:-}" in
  reset) exec python3 "$BASE/reset.py" ;;
  list) exec python3 -c 'import json,sys; [print(x["id"], x["title"], "("+", ".join(x["events"])+")") for x in json.load(open(sys.argv[1]))]' "$BASE/catalog.json" ;;
  context) ID=01 ;;
  block) ID=02 ;;
  log) ID=03 ;;
  [0-9][0-9]) ID=$1 ;;
  *) echo "Usage: sh codex-hooks-workshop/demo.sh {01..18|context|block|log|list|reset}" >&2; exit 1 ;;
esac
SCENARIO=$(python3 -c 'import json,sys; print(next((x["directory"] for x in json.load(open(sys.argv[1])) if x["id"]==sys.argv[2]), ""))' "$BASE/catalog.json" "$ID")
[ -n "$SCENARIO" ] || { echo "Unknown scenario: $ID" >&2; exit 1; }
command -v codex >/dev/null || { echo "Install Codex CLI first." >&2; exit 1; }
if [ "$ID" = 05 ]; then
  exec codex --no-daemon -s read-only -a on-request -C "$BASE/$SCENARIO"
fi
exec codex --no-daemon -C "$BASE/$SCENARIO"
