#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname "$0")" && pwd)
REPO_ROOT=$(CDPATH= cd -- "$SCRIPT_DIR/../../../.." && pwd)
KNOWLEDGE_ROOT="$REPO_ROOT/Workspace/Knowledge"

find "$KNOWLEDGE_ROOT" -type f -name "*.tmp.*" -delete
find "$KNOWLEDGE_ROOT" -type f -name ".DS_Store" -delete
printf 'Cleaned temporary knowledge files under %s\n' "$KNOWLEDGE_ROOT"
