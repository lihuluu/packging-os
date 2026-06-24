#!/usr/bin/env bash
# cleanup-project-temp-files.sh — 清理 Workspace/Projects/ 下的临时文件
#
# 用法：
#   bash .claude/skills/project-memory-manager/scripts/cleanup-project-temp-files.sh [--execute]
#
# 默认模式（dry-run）：只列出将被删除的文件，不实际删除。
# 传入 --execute 时才真正删除。
#
# 清理目标（以下类型文件）：
#   .DS_Store, Thumbs.db, desktop.ini, .gitkeep（空占位）
#   ~$*（Office 临时锁定文件）
#   *.tmp, *.tmp.*, *.bak, *.log
#   __pycache__/ 目录

set -euo pipefail

# ── 定位仓库根目录 ──────────────────────────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# scripts/ -> project-memory-manager/ -> skills/ -> .claude/ -> root
REPO_ROOT="$(cd "$SCRIPT_DIR/../../../.." && pwd)"
PROJECTS_DIR="$REPO_ROOT/Workspace/Projects"

# ── 参数解析 ────────────────────────────────────────────────────────────────
EXECUTE=false
for arg in "$@"; do
  case "$arg" in
    --execute) EXECUTE=true ;;
    --help|-h)
      sed -n '2,14p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
      exit 0
      ;;
    *)
      echo "未知参数：$arg" >&2
      echo "用法：$0 [--execute]" >&2
      exit 1
      ;;
  esac
done

# ── 检查目录 ────────────────────────────────────────────────────────────────
if [[ ! -d "$PROJECTS_DIR" ]]; then
  echo "错误：找不到 Workspace/Projects/ 目录（在 $REPO_ROOT）" >&2
  exit 1
fi

# ── 扫描临时文件 ────────────────────────────────────────────────────────────
echo "Packaging OS — 项目临时文件清理"
echo "扫描目录：$PROJECTS_DIR"
echo "模式：$( [[ "$EXECUTE" == true ]] && echo '实际删除' || echo 'dry-run（只列出，不删除）' )"
echo ""

FOUND=0
DELETED=0
ERRORS=0

while IFS= read -r -d '' file; do
  ((FOUND++)) || true
  if [[ "$EXECUTE" == true ]]; then
    if rm -f "$file" 2>/dev/null; then
      echo "  [删除] $file"
      ((DELETED++)) || true
    else
      echo "  [失败] $file" >&2
      ((ERRORS++)) || true
    fi
  else
    echo "  [待删除] $file"
  fi
done < <(find "$PROJECTS_DIR" \
  \( \
    -name ".DS_Store" \
    -o -name "Thumbs.db" \
    -o -name "desktop.ini" \
    -o -name "~\$*" \
    -o -name "*.tmp" \
    -o -name "*.tmp.*" \
    -o -name "*.bak" \
    -o -name "*.log" \
  \) -print0 2>/dev/null)

# 空的 .gitkeep 文件（只在文件大小为 0 时删除）
while IFS= read -r -d '' file; do
  if [[ ! -s "$file" ]]; then
    ((FOUND++)) || true
    if [[ "$EXECUTE" == true ]]; then
      if rm -f "$file" 2>/dev/null; then
        echo "  [删除] $file  (空 .gitkeep)"
        ((DELETED++)) || true
      else
        echo "  [失败] $file" >&2
        ((ERRORS++)) || true
      fi
    else
      echo "  [待删除] $file  (空 .gitkeep)"
    fi
  fi
done < <(find "$PROJECTS_DIR" -name ".gitkeep" -print0 2>/dev/null)

echo ""
if [[ "$EXECUTE" == true ]]; then
  echo "完成：共发现 $FOUND 个临时文件，已删除 $DELETED 个，失败 $ERRORS 个。"
  [[ $ERRORS -gt 0 ]] && exit 1 || exit 0
else
  if [[ $FOUND -eq 0 ]]; then
    echo "未发现任何临时文件。"
  else
    echo "发现 $FOUND 个临时文件。如需实际删除，请加 --execute 参数重新运行。"
  fi
  exit 0
fi
