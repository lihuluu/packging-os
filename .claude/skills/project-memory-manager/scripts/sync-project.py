#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""sync-project: 项目状态一键同步.

读取 project-memory-card.md，刷新以下文件让它们与项目卡保持一致：
  1. 00_Project_Control/project-tracker.md（从项目卡提取当前阶段/里程碑/任务/风险）
  2. 03_Design/01_Working/decision-log.md（如果项目卡"本次更新"含结构性决策关键词，提示用户追加；不自动写入）

用法：
  python sync-project.py --project HGT235_特级高山绿茶500g
  python sync-project.py --root . --project HGT235_特级高山绿茶500g
"""
from __future__ import annotations

import argparse
import io
import re
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path


if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf-8-sig"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
if sys.stderr.encoding and sys.stderr.encoding.lower() not in ("utf-8", "utf-8-sig"):
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")


# 项目卡里"本次更新"中暗示结构性决策的关键词，触发 decision-log 提示
STRUCTURAL_DECISION_KEYWORDS = (
    "锁定", "确认", "变更", "跳过", "更正", "改为", "切换", "重新",
    "概念方向", "结构选型", "视觉方向", "材质工艺", "阶段跳过",
    "客户确认", "客户已确认", "已通过",
)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    try:
        return path.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def split_sections(text: str) -> dict[str, list[str]]:
    sections: dict[str, list[str]] = {}
    current: str | None = None
    for line in text.splitlines():
        m = re.match(r"^##\s+(.+?)\s*$", line)
        if m:
            current = m.group(1).strip()
            sections.setdefault(current, [])
            continue
        if current is not None:
            sections[current].append(line.rstrip())
    return sections


def section_lines(sections: dict[str, list[str]], names: tuple[str, ...]) -> list[str]:
    for name, lines in sections.items():
        if any(token in name for token in names):
            return lines
    return []


def clean_text(value: str) -> str:
    value = re.sub(r"`([^`]+)`", r"\1", value)
    value = re.sub(r"\*\*([^*]+)\*\*", r"\1", value)
    value = value.replace("~~", "")
    value = re.sub(r"<[^>]+>", "", value)
    value = value.strip()
    value = re.sub(r"^[\-*]\s+", "", value)
    value = re.sub(r"^\d+[.)]\s+", "", value)
    value = re.sub(r"^\[[ xX]\]\s*", "", value)
    return value.strip()


def is_resolved(value: str) -> bool:
    resolved_markers = ("✅", "已完成", "通过", "跳过", "⏭")
    unresolved_markers = ("❌", "未开始", "待安排", "待确认", "待推进", "🟡", "🔴")
    if any(marker in value for marker in unresolved_markers):
        return False
    return any(marker in value for marker in resolved_markers) or "~~" in value


def bullet_field(lines: list[str], key: str) -> str:
    """从项目摘要等 bullet 列表里取字段。"""
    for line in lines:
        stripped = line.strip()
        if not stripped.startswith(("-", "*")):
            continue
        item = clean_text(stripped)
        if key in item:
            for sep in ("：", ":"):
                if sep in item:
                    return item.split(sep, 1)[1].strip().strip("`")
    return ""


def list_items(lines: list[str], limit: int = 6, skip_resolved: bool = False) -> list[str]:
    items: list[str] = []
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("|") or set(stripped) <= {"-", "|", " "}:
            continue
        if skip_resolved and is_resolved(stripped):
            continue
        if stripped.startswith(("-", "*")) or re.match(r"^\d+[.)]\s+", stripped):
            item = clean_text(stripped)
            if item:
                items.append(item)
        if len(items) >= limit:
            break
    return items


def parse_tables(lines: list[str]) -> tuple[list[str], list[dict[str, str]]]:
    table_lines = [line.strip() for line in lines if line.strip().startswith("|")]
    if len(table_lines) < 2:
        return [], []
    headers: list[str] = []
    rows: list[dict[str, str]] = []
    for line in table_lines:
        cells = [clean_text(c) for c in line.strip("|").split("|")]
        if not headers:
            headers = cells
            continue
        if all(re.fullmatch(r":?-{3,}:?", c.replace(" ", "")) for c in cells):
            continue
        if len(cells) != len(headers):
            continue
        rows.append(dict(zip(headers, cells)))
    return headers, rows


def find_project_dir(root: Path, project_name: str) -> Path:
    projects_dir = root / "Workspace" / "Projects"
    if not projects_dir.exists():
        raise FileNotFoundError(f"Cannot find Workspace/Projects under {root}")
    # 精确匹配
    target = projects_dir / project_name
    if target.is_dir():
        return target
    # 模糊匹配
    candidates = [p for p in projects_dir.iterdir() if p.is_dir() and project_name in p.name]
    if len(candidates) == 1:
        return candidates[0]
    if not candidates:
        raise FileNotFoundError(f"Project not found: {project_name}")
    raise ValueError(f"Multiple projects match '{project_name}': {[p.name for p in candidates]}")


def extract_card_data(card_path: Path) -> dict:
    """从项目卡提取生成 tracker 需要的字段。"""
    text = read_text(card_path)
    sections = split_sections(text)

    summary_lines = section_lines(sections, ("项目摘要",))
    constraints_lines = section_lines(sections, ("商业硬约束",))
    milestones_lines = section_lines(sections, ("里程碑时间线",))
    facts_lines = section_lines(sections, ("已知事实",))
    questions_lines = section_lines(sections, ("开放问题",))
    risks_lines = section_lines(sections, ("风险",))
    actions_lines = section_lines(sections, ("下一步动作",))
    dependencies_lines = section_lines(sections, ("依赖项",))

    # 里程碑表
    _, milestone_rows = parse_tables(milestones_lines)

    return {
        "name": bullet_field(summary_lines, "项目名称") or card_path.parent.parent.name,
        "phase": bullet_field(summary_lines, "当前阶段"),
        "go_live": bullet_field(summary_lines, "目标上市日期"),
        "channel": bullet_field(summary_lines, "销售渠道"),
        "budget": bullet_field(constraints_lines, "预算上限"),
        "moq": bullet_field(constraints_lines, "MOQ") or bullet_field(constraints_lines, "首发批量"),
        "hard_deadline": bullet_field(constraints_lines, "硬截止日期"),
        "milestones": milestone_rows,
        "facts": list_items(facts_lines, limit=6),
        "questions": list_items(questions_lines, limit=6, skip_resolved=True),
        "risks": list_items(risks_lines, limit=6, skip_resolved=True),
        "actions": list_items(actions_lines, limit=6),
        "dependencies_done": [
            d for d in list_items(dependencies_lines, limit=12)
            if "✅" in d or "已完成" in d
        ],
        "dependencies_blocked": [
            d for d in list_items(dependencies_lines, limit=12)
            if "❌" in d or "未回复" in d or "待确认" in d
        ],
    }


def build_tracker(data: dict) -> str:
    """根据项目卡数据生成 tracker 内容。"""
    name = data["name"]
    phase = data["phase"] or "未检测到"
    today = date.today().isoformat()
    lines: list[str] = []
    lines.append(f"# 包装项目推进表 — {name}")
    lines.append("")
    lines.append("> 此文件由 sync-project 自动从 project-memory-card.md 同步。如需手工补充，请加在 `## 备注` 区块下，避免被覆盖。")
    lines.append(f"> 最近同步：{today}")
    lines.append("")
    lines.append("## 当前阶段")
    lines.append(f"- {phase}")
    lines.append("")

    # 里程碑表
    lines.append("## 关键里程碑")
    if data["milestones"]:
        # 取表头
        sample = data["milestones"][0]
        headers = list(sample.keys())
        lines.append("| " + " | ".join(headers) + " |")
        lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
        for row in data["milestones"]:
            cells = [row.get(h, "") for h in headers]
            lines.append("| " + " | ".join(cells) + " |")
    else:
        lines.append("_项目卡未提供里程碑时间线_")
    lines.append("")

    # 任务清单（从 actions 提取）
    lines.append("## 任务清单")
    if data["actions"]:
        lines.append("| 任务 | 来源 |")
        lines.append("| --- | --- |")
        for action in data["actions"]:
            # 去掉已完成的标记
            cleaned = re.sub(r"~~.*?~~", "", action).strip()
            cleaned = re.sub(r"^✅\s*", "", cleaned)
            if cleaned:
                lines.append(f"| {cleaned} | 项目卡下一步动作 |")
    else:
        lines.append("_项目卡未提供下一步动作_")
    lines.append("")

    # 关键路径（从依赖项推断）
    lines.append("## 关键路径")
    blocked = data["dependencies_blocked"]
    if blocked:
        lines.append("**当前阻塞项：**")
        for b in blocked:
            lines.append(f"- {b}")
    else:
        lines.append("_无阻塞项_")
    lines.append("")

    # 风险节点
    lines.append("## 风险节点")
    if data["risks"]:
        for r in data["risks"]:
            lines.append(f"- {r}")
    else:
        lines.append("_无风险项_")
    lines.append("")

    # 开放问题
    lines.append("## 开放问题")
    if data["questions"]:
        for q in data["questions"]:
            lines.append(f"- {q}")
    else:
        lines.append("_无开放问题_")
    lines.append("")

    # 备注（用户手工区）
    lines.append("## 备注")
    lines.append("")
    lines.append("<!-- 在此添加手工补充内容，sync-project 不会覆盖本区块以外的内容 -->")
    lines.append("")

    return "\n".join(lines) + "\n"


def preserve_manual_notes(old_tracker: Path, new_content: str) -> str:
    """保留旧 tracker 里 ## 备注 区块下的手工内容。"""
    if not old_tracker.exists():
        return new_content
    old_text = read_text(old_tracker)
    # 抓取旧的备注区块内容
    m = re.search(r"## 备注\s*\n(.*?)(?:\n##\s|\Z)", old_text, re.DOTALL)
    if not m:
        return new_content
    manual_notes = m.group(1).strip()
    if not manual_notes or manual_notes.startswith("<!--"):
        return new_content
    # 替换新内容里的备注区块
    return re.sub(
        r"(## 备注\s*\n)(.*?)(<!--|\Z)",
        lambda m: m.group(1) + manual_notes + "\n\n" + m.group(3),
        new_content,
        count=1,
        flags=re.DOTALL,
    )


def detect_structural_decisions(card_path: Path) -> list[str]:
    """检查项目卡本次更新是否含结构性决策，返回需要追加到 decision-log 的提示。"""
    text = read_text(card_path)
    sections = split_sections(text)
    update_lines = section_lines(sections, ("本次更新",))
    if not update_lines:
        return []
    joined = "\n".join(update_lines)
    hits: list[str] = []
    for kw in STRUCTURAL_DECISION_KEYWORDS:
        if kw in joined:
            # 抽取该关键词所在的 bullet
            for line in update_lines:
                if kw in line and line.strip().startswith(("-", "*")):
                    hits.append(clean_text(line))
                    break
    return hits


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync project status from project-memory-card.md")
    parser.add_argument("--root", default=None, help="Packaging OS root")
    parser.add_argument("--project", required=True, help="Project folder name (or substring)")
    args = parser.parse_args()

    root = Path(args.root).resolve() if args.root else Path(__file__).resolve().parents[4]
    try:
        project_dir = find_project_dir(root, args.project)
    except (FileNotFoundError, ValueError) as e:
        print(f"[error] {e}", file=sys.stderr)
        return 1

    card_path = project_dir / "00_Project_Control" / "project-memory-card.md"
    if not card_path.exists():
        print(f"[error] 项目卡不存在：{card_path}", file=sys.stderr)
        return 1

    print(f"[sync] {project_dir.name}")
    print(f"  源：{card_path.relative_to(root)}")

    # 1. 刷新 tracker
    tracker_path = project_dir / "00_Project_Control" / "project-tracker.md"
    data = extract_card_data(card_path)
    new_tracker = build_tracker(data)
    new_tracker = preserve_manual_notes(tracker_path, new_tracker)
    write_text(tracker_path, new_tracker)
    print(f"  ✓ tracker 已同步：{tracker_path.relative_to(root)}")

    # 2. 检测结构性决策
    decisions = detect_structural_decisions(card_path)
    if decisions:
        print(f"")
        print(f"  ⚠ 项目卡「本次更新」含结构性决策，请人工追加到 decision-log.md：")
        for d in decisions:
            print(f"    - {d}")

    print(f"[done] {project_dir.name} 同步完成")
    return 0


if __name__ == "__main__":
    sys.exit(main())
