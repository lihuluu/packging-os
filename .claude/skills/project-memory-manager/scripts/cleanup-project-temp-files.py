#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""清理项目目录下的临时文件和系统垃圾文件（跨平台）.

清理对象：
  - .DS_Store / Thumbs.db / desktop.ini
  - Office 临时锁文件 ~$*
  - *.tmp / *.tmp.* / *.bak / *.log
  - 空的 .gitkeep
  - __pycache__ 目录

默认 dry-run，需要 --execute 才真正删除。
"""
from __future__ import annotations

import argparse
import io
import sys
from pathlib import Path


if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf-8-sig"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
if sys.stderr.encoding and sys.stderr.encoding.lower() not in ("utf-8", "utf-8-sig"):
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")


JUNK_FILE_NAMES = {".DS_Store", "Thumbs.db", "desktop.ini"}
JUNK_FILE_SUFFIXES = (".tmp", ".bak", ".log")
JUNK_FILE_PATTERNS = (".tmp.",)  # 文件名中间含 .tmp.
JUNK_DIRS = {"__pycache__"}


def is_junk(path: Path) -> bool:
    name = path.name
    if path.is_dir():
        return name in JUNK_DIRS
    if name in JUNK_FILE_NAMES:
        return True
    if name.startswith("~$"):
        return True
    if name.endswith(JUNK_FILE_SUFFIXES):
        return True
    if any(pat in name for pat in JUNK_FILE_PATTERNS):
        return True
    if name == ".gitkeep":
        try:
            return path.stat().st_size == 0
        except OSError:
            return False
    return False


def find_junk(root: Path) -> list[Path]:
    items: list[Path] = []
    for path in root.rglob("*"):
        # 跳过 .git, .obsidian, node_modules 等
        if any(part in {".git", ".obsidian", "node_modules"} for part in path.parts):
            continue
        if path.is_symlink():
            continue
        try:
            if is_junk(path):
                items.append(path)
        except OSError:
            continue
    return items


def main() -> int:
    parser = argparse.ArgumentParser(description="Clean project temp files (cross-platform).")
    parser.add_argument("--root", default=None, help="Packaging OS root (defaults to script's parents[4])")
    parser.add_argument("--execute", action="store_true", help="Actually delete files (default: dry-run)")
    parser.add_argument("--quiet", action="store_true", help="Suppress per-file output")
    args = parser.parse_args()

    root = Path(args.root).resolve() if args.root else Path(__file__).resolve().parents[4]
    projects_dir = root / "Workspace" / "Projects"
    if not projects_dir.exists():
        print(f"[error] Workspace/Projects not found under {root}", file=sys.stderr)
        return 1

    # 同时扫知识库、.claude 全域、docs、Templates
    scan_dirs = [
        projects_dir,
        root / "Workspace" / "Knowledge",
        root / "Workspace" / "Templates",
        root / ".claude",
        root / "docs",
        root,  # 根目录的零散 .tmp 文件
    ]

    junk: list[Path] = []
    for scan_dir in scan_dirs:
        if scan_dir.exists():
            junk.extend(find_junk(scan_dir))

    # 去重并排序（目录要在文件之后删，避免删到目录里的文件再报错）
    junk = sorted(set(junk), key=lambda p: (p.is_file(), str(p)))

    if not junk:
        if not args.quiet:
            print("[clean] 未发现临时文件，工作区干净。")
        return 0

    mode = "EXECUTE" if args.execute else "DRY-RUN"
    if not args.quiet:
        print(f"[clean] 模式：{mode}")
        print(f"[clean] 发现 {len(junk)} 个临时文件/目录：")

    deleted = 0
    failed: list[tuple[Path, str]] = []
    for path in junk:
        rel = path.relative_to(root) if path.is_relative_to(root) else path
        if args.execute:
            try:
                if path.is_dir():
                    # 目录先清空再删
                    for child in path.rglob("*"):
                        if child.is_file():
                            child.unlink()
                    path.rmdir()
                else:
                    path.unlink()
                deleted += 1
                if not args.quiet:
                    print(f"  ✓ 删除 {rel}")
            except OSError as exc:
                failed.append((path, str(exc)))
                if not args.quiet:
                    print(f"  ✗ 失败 {rel}: {exc}", file=sys.stderr)
        else:
            if not args.quiet:
                print(f"  · 待删 {rel}")

    if args.execute:
        print(f"[done] 已删除 {deleted} 个，失败 {len(failed)} 个")
    else:
        print(f"[done] dry-run 发现 {len(junk)} 个，加 --execute 真正删除")

    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
