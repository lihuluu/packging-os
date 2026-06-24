#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PostToolUse hook：监听对 project-memory-card.md 的 Edit/Write，
自动调用 sync-project.py 刷新 tracker 和 dashboard。

stdin 收到 Claude Code 的 hook JSON：
{
  "tool_name": "Edit" | "Write" | "MultiEdit",
  "tool_input": { "file_path": "...", ... },
  ...
}

只要 file_path 含 project-memory-card.md，就提取项目目录名，
异步调用 sync-project.py（不阻塞 Claude 主流程）。
"""
from __future__ import annotations

import io
import json
import os
import subprocess
import sys
from pathlib import Path

# Windows GBK 终端兼容：print 含中文项目名/路径（如 HGT235_特级高山绿茶）会 UnicodeEncodeError。
# 非 UTF-8 终端时把 stderr 包成 utf-8(errors=replace)；Mac/Linux 已是 UTF-8，零影响。
if sys.stderr.encoding and sys.stderr.encoding.lower() not in ("utf-8", "utf-8-sig"):
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")


HOOK_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = HOOK_DIR.parent.parent  # .claude/hooks -> root
SYNC_SCRIPT = PROJECT_ROOT / ".claude" / "skills" / "project-memory-manager" / "scripts" / "sync-project.py"
PROJECTS_DIR = PROJECT_ROOT / "Workspace" / "Projects"


def find_python() -> str | None:
    for candidate in (sys.executable, "python", "python3"):
        if not candidate:
            continue
        try:
            result = subprocess.run(
                [candidate, "--version"],
                capture_output=True, text=True, timeout=5,
            )
            if result.returncode == 0:
                return candidate
        except (FileNotFoundError, subprocess.TimeoutExpired):
            continue
    return None


def extract_project_name(file_path: str) -> str | None:
    """从 file_path 提取项目目录名。路径里必须含 Workspace/Projects/<项目>/00_Project_Control/project-memory-card.md"""
    p = Path(file_path)
    parts = p.parts
    # 找 Workspace/Projects/<项目名>/00_Project_Control/...
    for i, part in enumerate(parts):
        if part == "Projects" and i > 0 and parts[i - 1] == "Workspace" and i + 1 < len(parts):
            return parts[i + 1]
    # 兜底：直接取 00_Project_Control 的父目录名
    if "00_Project_Control" in parts:
        idx = parts.index("00_Project_Control")
        if idx > 0:
            return parts[idx - 1]
    return None


def main() -> int:
    # 安静模式：hook 输出会显示给用户，所以默认不打印任何东西
    debug = os.environ.get("PACKAGING_OS_HOOK_DEBUG") == "1"

    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0  # hook 失败不能阻塞工具

    tool_name = payload.get("tool_name", "")
    if tool_name not in ("Edit", "Write", "MultiEdit", "NotebookEdit"):
        return 0

    tool_input = payload.get("tool_input", {}) or {}
    file_path = tool_input.get("file_path", "")
    if not file_path:
        return 0

    # 路径归一化（Windows 反斜杠 / Mac 正斜杠 都接受）
    normalized = str(file_path).replace("\\", "/")
    if "project-memory-card.md" not in normalized:
        return 0

    project_name = extract_project_name(normalized)
    if not project_name:
        if debug:
            print(f"[auto-sync] 无法从路径提取项目名：{file_path}", file=sys.stderr)
        return 0

    # 校验项目目录真的存在
    project_dir = PROJECTS_DIR / project_name
    if not project_dir.is_dir():
        if debug:
            print(f"[auto-sync] 项目目录不存在：{project_dir}", file=sys.stderr)
        return 0

    # 找 Python
    python = find_python()
    if not python:
        if debug:
            print("[auto-sync] 找不到 Python，跳过", file=sys.stderr)
        return 0

    # 异步调用 sync-project.py（DETACHED_PROCESS on Windows / nohup style on Unix）
    try:
        if os.name == "nt":
            # Windows: 用 CREATE_NEW_PROCESS_GROUP + DETACHED_PROCESS 让子进程独立
            subprocess.Popen(
                [python, str(SYNC_SCRIPT), "--root", str(PROJECT_ROOT), "--project", project_name],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                stdin=subprocess.DEVNULL,
                creationflags=0x00000008 | 0x00000200,  # DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP
            )
        else:
            # Mac/Linux: 用 start_new_session 让子进程脱离父进程
            subprocess.Popen(
                [python, str(SYNC_SCRIPT), "--root", str(PROJECT_ROOT), "--project", project_name],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                stdin=subprocess.DEVNULL,
                start_new_session=True,
            )
        if debug:
            print(f"[auto-sync] 已触发后台同步：{project_name}", file=sys.stderr)
    except OSError as exc:
        if debug:
            print(f"[auto-sync] 启动失败：{exc}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())
