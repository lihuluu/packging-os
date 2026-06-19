#!/usr/bin/env sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
ROOT_DIR=$(CDPATH= cd -- "$SCRIPT_DIR/../../../.." && pwd)

if command -v python3 >/dev/null 2>&1; then
  PYTHON=python3
elif command -v python >/dev/null 2>&1; then
  PYTHON=python
else
  echo "Error: get-knowledge-coverage requires Python (python3/python) on PATH." >&2
  exit 1
fi

exec "$PYTHON" "$SCRIPT_DIR/get_knowledge_coverage.py" --root "$ROOT_DIR" "$@"
