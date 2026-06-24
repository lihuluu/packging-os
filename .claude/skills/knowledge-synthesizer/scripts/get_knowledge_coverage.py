#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""get_knowledge_coverage.py — 批量盘点项目知识沉淀覆盖率（跨平台，Packaging OS）。

等价于原 get-knowledge-coverage.ps1。扫描 Workspace/Projects 下每个项目，
判定知识沉淀状态，输出 JSON（stdout）。既可被 start_knowledge_review_session.py
import 复用，也可作为独立 CLI 使用。

用法：
    python3 get_knowledge_coverage.py [--root PATH]
"""
from __future__ import annotations

import argparse
import io
import json
import sys
from pathlib import Path

# 同目录平铺 import
sys.path.insert(0, str(Path(__file__).resolve().parent))
import knowledge_file_utils as utils

# Windows 终端编码兼容
if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf-8-sig"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
if sys.stderr.encoding and sys.stderr.encoding.lower() not in ("utf-8", "utf-8-sig"):
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")


def collect_coverage(root: Path) -> list[dict]:
    """扫描所有项目，返回覆盖率行（按 Status、Project 排序，与 ps1 Sort-Object 一致）。

    每行字段：Project, Status, HasMemoryCard, HasRetrospective,
    HasKnowledgeSynthesis, DocumentCount, LastUpdated。
    """
    projects_root = root / "Workspace" / "Projects"
    rows: list[dict] = []
    for project_dir in sorted(
        p for p in projects_root.iterdir() if p.is_dir() and not p.name.startswith("_")
    ):
        files = utils.scan_project_files(project_dir)
        status = utils.classify_project_status(project_dir, files)
        last_mtime = max((f.stat().st_mtime for f in files), default=None)
        rows.append({
            "Project": project_dir.name,
            "Status": status,
            "HasMemoryCard": (project_dir / utils.CARD_RELATIVE).exists(),
            "HasRetrospective": (project_dir / utils.RETRO_RELATIVE).exists(),
            "HasKnowledgeSynthesis": (project_dir / utils.SYNTHESIS_RELATIVE).exists(),
            "DocumentCount": len(files),
            "LastUpdated": utils.format_mtime(last_mtime) if last_mtime else "",
        })
    rows.sort(key=lambda r: (r["Status"], r["Project"]))
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description="批量盘点项目知识沉淀覆盖率，输出 JSON。")
    parser.add_argument("--root", default=None, help="Packaging OS 根目录（默认脚本 parents[4]）")
    args = parser.parse_args()

    root = Path(args.root).resolve() if args.root else Path(__file__).resolve().parents[4]
    projects_root = root / "Workspace" / "Projects"
    if not projects_root.exists():
        print(f"错误：找不到项目目录：{projects_root}", file=sys.stderr)
        return 1

    rows = collect_coverage(root)
    print(json.dumps(rows, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
