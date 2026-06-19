#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""project_file_utils.py — 项目文档安全写入工具（跨平台，Packging OS）。

等价于原 project-file-utils.ps1。提供原子写：先写同目录 .tmp.{pid}.{ms}，
再 os.replace 替换正式文件，最后清理残留 .tmp.*；失败时保留临时文件并抛出异常。
供 project-memory-manager 下需要批量写入项目文档的脚本复用（与 knowledge_file_utils.py
的原子写部分同构，分属两个 skill 各自的写入工具库，避免跨 skill 耦合）。
"""
from __future__ import annotations

import io
import os
import re
import sys
import time
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf-8-sig"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
if sys.stderr.encoding and sys.stderr.encoding.lower() not in ("utf-8", "utf-8-sig"):
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

_TMP_SUFFIX_RE = re.compile(r"\.tmp\.\d+\.\d+$")


def get_project_temp_path(path: Path) -> Path:
    """生成原子写用的临时路径：{path}.tmp.{pid}.{毫秒时间戳}。"""
    return Path(f"{path}.tmp.{os.getpid()}.{int(time.time() * 1000)}")


def remove_project_temp_files(target_path: Path) -> None:
    """清理 target 同目录下同名文件的 .tmp.* 残留。"""
    directory = target_path.parent
    if not directory.is_dir():
        return
    for f in directory.glob(f"{target_path.name}.tmp.*"):
        try:
            f.unlink()
        except OSError:
            continue


def write_project_file_atomic(path: Path, lines: list[str]) -> None:
    """原子写：建父目录 → 写 .tmp → os.replace 替换正式文件 → 清理残留。

    失败时保留 .tmp 并抛出异常（与 ps1 Write-ProjectFileAtomic 一致）。
    行尾用 LF（原 ps1 用 CRLF，迁移后统一为 LF，markdown 渲染无差异）。
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = get_project_temp_path(path)
    try:
        content = "\n".join(lines)
        if lines:
            content += "\n"
        tmp.write_text(content, encoding="utf-8")
        os.replace(tmp, path)  # 跨平台原子 rename + 覆盖，等价 Move-Item -Force；同目录同卷
        remove_project_temp_files(path)
    except OSError:
        if tmp.exists():
            print(f"[project] 临时文件保留待查：{tmp}", file=sys.stderr)
        raise
