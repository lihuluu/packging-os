#!/usr/bin/env sh
set -u

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
ROOT_DIR=$(CDPATH= cd -- "$SCRIPT_DIR/../../../.." && pwd)
FAILED=0

printf 'Packging OS - daily governance check\n'
printf 'Repository: %s\n\n' "$ROOT_DIR"

printf '[1/3] Governance validation\n'
sh "$SCRIPT_DIR/validate-packging-os.sh" || FAILED=1
printf '\n'

printf '[2/3] Project temp cleanup dry-run\n'
if command -v bash >/dev/null 2>&1; then
  bash "$SCRIPT_DIR/../../project-memory-manager/scripts/cleanup-project-temp-files.sh" || FAILED=1
else
  sh "$SCRIPT_DIR/../../project-memory-manager/scripts/cleanup-project-temp-files.sh" || FAILED=1
fi
printf '\n'

printf '[3/3] Project memory drift check\n'
if command -v python3 >/dev/null 2>&1; then
  python3 "$SCRIPT_DIR/../../project-memory-manager/scripts/check-memory-drift.py" --root "$ROOT_DIR" --all || FAILED=1
elif command -v python >/dev/null 2>&1; then
  python "$SCRIPT_DIR/../../project-memory-manager/scripts/check-memory-drift.py" --root "$ROOT_DIR" --all || FAILED=1
else
  printf '[skip] Python was not found, so project memory drift check was skipped.\n'
fi

printf '\n'
if [ "$FAILED" -ne 0 ]; then
  printf 'Daily governance check completed with issues.\n'
  exit 1
fi

printf 'Daily governance check passed.\n'
exit 0
