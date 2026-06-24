#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check-memory-drift.py — 项目卡漂移检查脚本

用法：
    python3 .claude/skills/project-memory-manager/scripts/check-memory-drift.py

功能：
    扫描 Workspace/Projects/ 下的所有项目，
    检查每个项目的 project-memory-card.md 是否落后于该项目下的最新文件。
    输出汇总表，并对落后超过阈值的项目发出警告。

选项：
    --root PATH         手动指定仓库根目录（默认自动推断，取脚本所在位置上 4 级）
    --threshold DAYS    项目卡落后超过多少天才报警（默认 7 天）
    --all               同时列出未漂移的项目（默认只列问题项目）
"""
import argparse
import io
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Tuple

# Windows 终端编码兼容
if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf-8-sig"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
if sys.stderr.encoding and sys.stderr.encoding.lower() not in ("utf-8", "utf-8-sig"):
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

CARD_FILENAME = "project-memory-card.md"
CARD_RELATIVE = f"00_Project_Control/{CARD_FILENAME}"

# 忽略这些目录/文件（不影响漂移判断）
SKIP_DIRS = {"00_Project_Control"}
SKIP_SUFFIXES = {".tmp", ".bak", ".log", ".DS_Store"}
SKIP_NAMES = {"Thumbs.db", "desktop.ini", ".gitkeep", ".gitignore"}


def get_mtime(path: Path) -> datetime:
    return datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)


def latest_mtime_excluding_card(project_dir: Path) -> Tuple[Optional[datetime], Optional[Path]]:
    """返回项目目录中（排除 00_Project_Control 下的文件后）最新修改文件的时间和路径。"""
    latest_time: Optional[datetime] = None
    latest_path: Optional[Path] = None

    for f in project_dir.rglob("*"):
        if not f.is_file():
            continue
        # 跳过 00_Project_Control 目录
        try:
            parts = f.relative_to(project_dir).parts
        except ValueError:
            continue
        if parts[0] in SKIP_DIRS:
            continue
        if f.suffix.lower() in SKIP_SUFFIXES:
            continue
        if f.name in SKIP_NAMES:
            continue

        mtime = get_mtime(f)
        if latest_time is None or mtime > latest_time:
            latest_time = mtime
            latest_path = f

    return latest_time, latest_path


def fmt_dt(dt: Optional[datetime]) -> str:
    if dt is None:
        return "（无文件）"
    return dt.strftime("%Y-%m-%d %H:%M")


def main() -> int:
    parser = argparse.ArgumentParser(description="检查项目卡是否落后于最新产出。")
    parser.add_argument("--root", default=None, help="仓库根目录（默认自动推断）")
    parser.add_argument(
        "--threshold", type=int, default=7, metavar="DAYS",
        help="项目卡落后超过多少天才标记为漂移（默认 7 天）"
    )
    parser.add_argument("--all", action="store_true", help="同时显示未漂移的项目")
    args = parser.parse_args()

    script_path = Path(__file__).resolve()
    root = Path(args.root).resolve() if args.root else script_path.parents[4]

    projects_dir = root / "Workspace" / "Projects"
    if not projects_dir.exists():
        print(f"错误：找不到 Workspace/Projects/ 目录（在 {root}）", file=sys.stderr)
        return 1

    project_dirs = sorted(
        [d for d in projects_dir.iterdir() if d.is_dir() and not d.name.startswith(".")]
    )

    if not project_dirs:
        print("Workspace/Projects/ 下没有找到任何项目目录。")
        return 0

    drift_projects: list[tuple[str, str, str, int, str]] = []  # name, card_time, latest_time, days, latest_file
    ok_projects: list[tuple[str, str, str]] = []  # name, card_time, latest_time
    no_card_projects: list[str] = []
    no_other_files_projects: list[str] = []

    for project_dir in project_dirs:
        name = project_dir.name
        card_path = project_dir / CARD_RELATIVE

        if not card_path.exists():
            no_card_projects.append(name)
            continue

        card_mtime = get_mtime(card_path)
        latest_mtime, latest_file = latest_mtime_excluding_card(project_dir)

        if latest_mtime is None:
            no_other_files_projects.append(name)
            continue

        delta_seconds = (latest_mtime - card_mtime).total_seconds()
        delta_days = int(delta_seconds / 86400)

        if delta_days >= args.threshold:
            rel_latest = latest_file.relative_to(project_dir).as_posix() if latest_file else "?"
            drift_projects.append((name, fmt_dt(card_mtime), fmt_dt(latest_mtime), delta_days, rel_latest))
        else:
            ok_projects.append((name, fmt_dt(card_mtime), fmt_dt(latest_mtime)))

    # ── 输出 ────────────────────────────────────────────────────────────────
    print(f"Packaging OS — 项目卡漂移检查")
    print(f"扫描目录：{projects_dir}")
    print(f"漂移阈值：{args.threshold} 天")
    print(f"扫描时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print()

    if drift_projects:
        print(f"⚠️  需要更新项目卡（{len(drift_projects)} 个项目）")
        print()
        col_w = max(len(r[0]) for r in drift_projects) + 2
        header = f"{'项目名称':<{col_w}}  {'项目卡更新':<17}  {'最新产出':<17}  {'落后天数':>6}  最新文件"
        print(header)
        print("-" * len(header))
        for name, card_t, latest_t, days, latest_f in drift_projects:
            print(f"{name:<{col_w}}  {card_t:<17}  {latest_t:<17}  {days:>6} 天  {latest_f}")
        print()
    else:
        print("✅  没有漂移项目（所有项目卡均在阈值内）。")
        print()

    if args.all and ok_projects:
        print(f"✅  项目卡已更新（{len(ok_projects)} 个项目）")
        col_w = max(len(r[0]) for r in ok_projects) + 2
        header = f"{'项目名称':<{col_w}}  {'项目卡更新':<17}  {'最新产出':<17}"
        print(header)
        print("-" * len(header))
        for name, card_t, latest_t in ok_projects:
            print(f"{name:<{col_w}}  {card_t:<17}  {latest_t:<17}")
        print()

    if no_card_projects:
        print(f"⚠️  缺少项目卡（{len(no_card_projects)} 个项目）")
        for name in no_card_projects:
            print(f"  - {name}  →  缺少 {CARD_RELATIVE}")
        print()

    if no_other_files_projects:
        print(f"ℹ️  仅有项目卡、尚无其他产出（{len(no_other_files_projects)} 个项目）")
        for name in no_other_files_projects:
            print(f"  - {name}")
        print()

    total_checked = len(drift_projects) + len(ok_projects) + len(no_card_projects) + len(no_other_files_projects)
    print(f"共扫描 {total_checked} 个项目，其中 {len(drift_projects)} 个需要更新项目卡。")

    return 1 if drift_projects or no_card_projects else 0


if __name__ == "__main__":
    sys.exit(main())
