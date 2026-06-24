#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""start_knowledge_review_session.py — 一键启动本轮知识整理会话（跨平台，Packaging OS）。

等价于原 start-knowledge-review-session.ps1。编排 get_knowledge_coverage 与
build_knowledge_review_packet，生成 Operations 下的 coverage / queue / current 三类文件
与会话日志草稿，输出 JSON（stdout）。通过 import 复用（不走 subprocess）。

用法：
    python3 start_knowledge_review_session.py [--root PATH] [--knowledge-root PATH]
"""
from __future__ import annotations

import argparse
import io
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import knowledge_file_utils as utils
from get_knowledge_coverage import collect_coverage
from build_knowledge_review_packet import build_packet_markdown

if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf-8-sig"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
if sys.stderr.encoding and sys.stderr.encoding.lower() not in ("utf-8", "utf-8-sig"):
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# 每个 Status 对应的下一步动作（与 ps1 Get-NextAction 一致；default 兜底 Done）
NEXT_ACTION_MAP = {
    "Missing Synthesis": "Create or update project-level knowledge-synthesis.md, then write back shared knowledge.",
    "Synthesis Created": "Keep the synthesis in sync when supplier feedback, validation results, or a retrospective is added.",
    "Ready": "Confirm the project has enough review signal, then start a knowledge-synthesis draft.",
    "Low Signal": "Keep collecting stage outputs before extracting shared knowledge.",
}
NEXT_ACTION_DEFAULT = "Track only if the project changes again."

TRIGGER_SCRIPT = ".claude/skills/knowledge-synthesizer/scripts/start_knowledge_review_session.py"


def _yes_no(value: bool) -> str:
    return "Yes" if value else "No"


def _join_project_list(items: list[str]) -> str:
    return ", ".join(items) if items else "none"


def _build_coverage_markdown(rows: list[dict]) -> list[str]:
    lines = [
        "# Project Knowledge Coverage",
        "",
        "## Status Definitions",
        "",
        "- `Done`: project-level knowledge capture exists.",
        "- `Synthesis Created`: `knowledge-synthesis.md` exists, but the project is still active or waiting for a retrospective update.",
        "- `Missing Synthesis`: the project has enough output or a retrospective, but no `knowledge-synthesis.md` yet.",
        "- `Ready`: the project looks mature enough to start knowledge capture.",
        "- `Low Signal`: not enough project output yet.",
        "",
        "## Coverage Table",
        "",
        "| Project | Status | Memory Card | Retrospective | Knowledge Synthesis | Doc Count | Last Updated |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for r in rows:
        lines.append(
            f"| {r['Project']} | {r['Status']} | {_yes_no(r['HasMemoryCard'])} | "
            f"{_yes_no(r['HasRetrospective'])} | {_yes_no(r['HasKnowledgeSynthesis'])} | "
            f"{r['DocumentCount']} | {r['LastUpdated']} |"
        )
    lines += [
        "",
        "## Next Actions",
        "",
        "- New projects should create `project-memory-card.md` first.",
        "- Projects with a retrospective but no `knowledge-synthesis.md` should enter the next review pass.",
    ]
    return lines


def _build_inbox_markdown(active_rows: list[dict]) -> list[str]:
    lines = [
        "# Knowledge Capture Inbox",
        "",
        "## Purpose",
        "",
        "This file tracks projects or observations that should be turned into reusable knowledge but are not finished yet.",
        "",
        "Rules:",
        "- Keep only active items here.",
        "- Remove items after they are handled.",
        "- If an observation is low confidence, write how it should be validated.",
        "",
        "## Current Queue",
        "",
    ]
    if not active_rows:
        lines.append("- none")
    else:
        for r in active_rows:
            lines.append(f"### {r['Priority']} - {r['Project']}")
            lines.append(f"- Status: {r['Status']}")
            lines.append(f"- Last Updated: {r['LastUpdated']}")
            lines.append(f"- Suggested Action: {r['NextAction']}")
            lines.append("")
    return lines


def _build_draft_log_markdown(today: str, rows: list[dict], active_rows: list[dict]) -> list[str]:
    p1 = [r["Project"] for r in active_rows if r["Priority"] == "P1"]
    p2 = [r["Project"] for r in active_rows if r["Priority"] == "P2"]
    p3 = [r["Project"] for r in active_rows if r["Priority"] == "P3"]
    return [
        "# Current Review Log Draft",
        "",
        "## Session Info",
        f"- Date: {today}",
        f"- Trigger: `{TRIGGER_SCRIPT}`",
        f"- Projects Scanned: {len(rows)}",
        f"- Projects Needing Attention: {len(active_rows)}",
        "",
        "## Current Priority Queue",
        f"- P1: {_join_project_list(p1)}",
        f"- P2: {_join_project_list(p2)}",
        f"- P3: {_join_project_list(p3)}",
        "",
        "## Planned Actions",
        "1. Handle all P1 projects first.",
        "2. Then cover P2 projects that are ready for synthesis.",
        "3. Update the workspace digest and finalize the history log.",
        "",
        "## Findings During The Session",
        "- ",
        "",
        "## Before Finalizing The History Log",
        "- [ ] `workspace-knowledge-digest.md` is updated",
        "- [ ] completed inbox items are removed",
        "- [ ] project-level synthesis files were reviewed",
    ]


def run_session(root: Path, knowledge_root: Path) -> dict:
    """执行一轮会话，生成 4 个文件，返回元数据 dict。"""
    knowledge_root.mkdir(parents=True, exist_ok=True)

    coverage_path = knowledge_root / "coverage" / "project-knowledge-coverage.md"
    inbox_path = knowledge_root / "queue" / "knowledge-capture-inbox.md"
    review_packet_path = knowledge_root / "current" / "current-review-session.md"
    draft_log_path = knowledge_root / "current" / "current-review-log-draft.md"

    scan_date = time.strftime("%Y-%m-%d %H:%M", time.localtime())

    # coverage（import，不 subprocess）
    rows = collect_coverage(root)

    # packet session md（import，自己写到 review_packet_path）
    packet_lines, _ = build_packet_markdown(root, scan_date)
    utils.write_knowledge_file_atomic(review_packet_path, packet_lines)

    # coverage md
    utils.write_knowledge_file_atomic(coverage_path, _build_coverage_markdown(rows))

    # active rows（非 Done），附 priority + next action + last updated
    active_rows = [
        {
            "Project": r["Project"],
            "Status": r["Status"],
            "Priority": utils.status_to_priority(r["Status"]),
            "NextAction": NEXT_ACTION_MAP.get(r["Status"], NEXT_ACTION_DEFAULT),
            "LastUpdated": r["LastUpdated"],
        }
        for r in rows
        if r["Status"] != "Done"
    ]
    active_rows.sort(key=lambda r: (utils.PRIORITY_ORDER.get(r["Priority"], 4), r["Project"]))

    # inbox md
    utils.write_knowledge_file_atomic(inbox_path, _build_inbox_markdown(active_rows))

    # draft log md
    today = time.strftime("%Y-%m-%d", time.localtime())
    utils.write_knowledge_file_atomic(draft_log_path, _build_draft_log_markdown(today, rows, active_rows))

    return {
        "CoveragePath": str(coverage_path),
        "InboxPath": str(inbox_path),
        "ReviewPacketPath": str(review_packet_path),
        "DraftLogPath": str(draft_log_path),
        "ProjectsScanned": len(rows),
        "ProjectsNeedingAttention": len(active_rows),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="一键启动本轮知识整理会话，生成 coverage/inbox/session/draft。")
    parser.add_argument("--root", default=None, help="Packaging OS 根目录（默认脚本 parents[4]）")
    parser.add_argument("--knowledge-root", default=None, help="知识库 Operations 目录（默认 Workspace/Knowledge/Operations）")
    args = parser.parse_args()

    root = Path(args.root).resolve() if args.root else Path(__file__).resolve().parents[4]
    projects_root = root / "Workspace" / "Projects"
    if not projects_root.exists():
        print(f"错误：找不到项目目录：{projects_root}", file=sys.stderr)
        return 1

    knowledge_root = (
        Path(args.knowledge_root).resolve()
        if args.knowledge_root
        else root / "Workspace" / "Knowledge" / "Operations"
    )

    result = run_session(root, knowledge_root)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
