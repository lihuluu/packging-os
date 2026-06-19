#!/usr/bin/env sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
ROOT_DIR=$(CDPATH= cd -- "$SCRIPT_DIR/../../../.." && pwd)

if command -v python3 >/dev/null 2>&1; then
  exec python3 "$SCRIPT_DIR/validate-packging-os.py" --root "$ROOT_DIR"
fi

if command -v python >/dev/null 2>&1; then
  exec python "$SCRIPT_DIR/validate-packging-os.py" --root "$ROOT_DIR"
fi

echo "Error: validate-packging-os requires Python (python3/python) on PATH." >&2
exit 1
