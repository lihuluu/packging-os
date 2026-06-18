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

if command -v pwsh >/dev/null 2>&1; then
  exec pwsh -NoProfile -File "$SCRIPT_DIR/init-project.ps1" -Root "$ROOT_DIR" "$@"
fi

echo "No runtime found. Install Python 3 or PowerShell 7, then run this script again." >&2
exit 127
