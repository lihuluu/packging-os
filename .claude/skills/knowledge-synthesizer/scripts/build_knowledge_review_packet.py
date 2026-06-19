#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_knowledge_review_packet.py — 生成本轮知识整理会话包（跨平台，Packging OS）。

等价于原 build-knowledge-review-packet.ps1。扫描所有项目，按优先级排序，
生成 current-review-session.md，包含四段：Session Metadata / Priority Queue /
Recommended Review Order / Session Checklist。可被 start_knowledge_review_session.py import。

用法：
    python3 build_knowledge_review_packet.py [--root PATH] [--output-path PATH]
"""
from __future__ import annotations

import argparse
import io
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import knowledge_file_utils as utils

if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf-8-sig"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
if sys.stderr.encoding and sys.stderr.encoding.lower() not in ("utf-8", "utf-8-sig"):
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

DEFAULT_OUTPUT_RELATIVE = "Workspace/Knowledge/Operations/current/current-review-session.md"


def build_packet_rows(root: Path) -> list[dict]:
    """扫描项目，返回带优先级和推荐文件的行（按 priority、Project 排序，与 ps1 一致）。"""
    projects_root = root / "Workspace" / "Projects"
    rows: list[dict] = []
    for project_dir in sorted(
        p for p in projects_root.iterdir() if p.is_dir() and not p.name.startswith("_")
    ):
        files = utils.scan_project_files(project_dir)
        status = utils.classify_project_status(project_dir, files)
        priority = utils.status_to_priority(status)
        # 最近 5 个文件（按 mtime 降序），相对 projectsRoot
        recent = sorted(files, key=lambda f: f.stat().st_mtime, reverse=True)[:5]
        recommended = [str(f.relative_to(projects_root).as_posix()) for f in recent]
        last_updated = recent[0].stat().st_mtime if recent else None
        rows.append({
            "Project": project_dir.name,
            "Status": status,
            "Priority": priority,
            "RecommendedSources": recommended,
            "LastUpdated": utils.format_mtime(last_updated) if last_updated else "",
        })
    rows.sort(key=lambda r: (utils.PRIORITY_ORDER.get(r["Priority"], 4), r["Project"]))
    return rows


def build_packet_markdown(root: Path, scan_date: str) -> tuple[list[str], list[dict]]:
    """生成 current-review-session.md 的行列表，同时返回 rows。"""
    rows = build_packet_rows(root)
    active_rows = [r for r in rows if r["Priority"] != "Done"]

    lines: list[str] = []
    lines.append("# Current Knowledge Review Session")
    lines.append("")
    lines.append("## Session Metadata")
    lines.append(f"- Generated At: {scan_date}")
    lines.append(f"- Projects Scanned: {len(rows)}")
    lines.append(f"- Projects Needing Attention: {len(active_rows)}")
    lines.append("")
    lines.append("## Priority Queue")
    lines.append("")
    lines.append("| Project | Priority | Status | Latest Activity |")
    lines.append("| --- | --- | --- | --- |")
    for r in rows:
        lines.append(f"| {r['Project']} | {r['Priority']} | {r['Status']} | {r['LastUpdated']} |")
    lines.append("")
    lines.append("## Recommended Review Order")
    lines.append("")
    if not active_rows:
        lines.append("- No active projects require knowledge capture right now.")
    else:
        for r in active_rows:
            lines.append(f"### {r['Priority']} - {r['Project']}")
            lines.append(f"- Status: {r['Status']}")
            lines.append("- Suggested files:")
            for src in r["RecommendedSources"]:
                lines.append(f"  - {src}")
            lines.append("")
    lines.append("")
    lines.append("## Session Checklist")
    lines.append("")
    lines.append("1. Update `coverage/project-knowledge-coverage.md` if statuses changed.")
    lines.append("2. Add missing projects to `queue/knowledge-capture-inbox.md`.")
    lines.append("3. Complete project-level `knowledge-synthesis.md` for P1/P2 projects.")
    lines.append("4. Update `workspace-knowledge-digest.md` with this round's changes.")
    lines.append("5. Write a history entry under `Workspace/Knowledge/Operations/history/`.")
    return lines, rows


def main() -> int:
    parser = argparse.ArgumentParser(description="生成本轮知识整理会话包 current-review-session.md。")
    parser.add_argument("--root", default=None, help="Packging OS 根目录（默认脚本 parents[4]）")
    parser.add_argument("--output-path", default=None, help="输出文件路径（默认 Operations/current/current-review-session.md）")
    args = parser.parse_args()

    root = Path(args.root).resolve() if args.root else Path(__file__).resolve().parents[4]
    projects_root = root / "Workspace" / "Projects"
    if not projects_root.exists():
        print(f"错误：找不到项目目录：{projects_root}", file=sys.stderr)
        return 1

    output_path = Path(args.output_path).resolve() if args.output_path else root / DEFAULT_OUTPUT_RELATIVE

    scan_date = time.strftime("%Y-%m-%d %H:%M", time.localtime())
    lines, _ = build_packet_markdown(root, scan_date)
    utils.write_knowledge_file_atomic(output_path, lines)
    print(f"已生成会话包：{output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
