#!/usr/bin/env sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
ROOT_DIR=$(CDPATH= cd -- "$SCRIPT_DIR/../../../.." && pwd)

if [ $# -lt 1 ]; then
  echo "Usage: sh init-project.sh \"Project Name\" [--dry-run]" >&2
  exit 1
fi

if command -v python3 >/dev/null 2>&1; then
  exec python3 "$SCRIPT_DIR/init-project.py" --root "$ROOT_DIR" "$@"
fi

if command -v python >/dev/null 2>&1; then
  exec python "$SCRIPT_DIR/init-project.py" --root "$ROOT_DIR" "$@"
fi

echo "Error: init-project requires Python (python3/python) on PATH." >&2
exit 1
