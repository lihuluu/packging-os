#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""knowledge_file_utils.py — 知识库脚本共享工具（跨平台，Packging OS）。

等价于原 knowledge-file-utils.ps1 的原子写能力，并把原 ps1 在
get-knowledge-coverage / build-knowledge-review-packet / start-knowledge-review-session
三处重复的「项目扫描 + 状态判定 + 优先级映射」逻辑下沉为纯函数（行为不变）。

被 get_knowledge_coverage.py / build_knowledge_review_packet.py /
start_knowledge_review_session.py 通过同目录平铺 import。
"""
from __future__ import annotations

import io
import os
import re
import sys
import time
from pathlib import Path

# Windows 终端编码兼容（与 sync-project.py / check-memory-drift.py 一致）
if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf-8-sig"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
if sys.stderr.encoding and sys.stderr.encoding.lower() not in ("utf-8", "utf-8-sig"):
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# 临时文件后缀正则：.tmp.{pid}.{ms}，等价 ps1 的 "\.tmp\.\d+\.\d+$"
_TMP_SUFFIX_RE = re.compile(r"\.tmp\.\d+\.\d+$")

# 项目内关键文件相对路径（用 pathlib 的 /，不拼字符串，跨平台安全）
CARD_RELATIVE = "00_Project_Control/project-memory-card.md"
RETRO_RELATIVE = "05_Retrospective/project-retrospective.md"
SYNTHESIS_RELATIVE = "05_Retrospective/knowledge-synthesis.md"

# 状态 → 优先级（与 ps1 Get-Priority 一致；default = Done）
PRIORITY_MAP = {
    "Missing Synthesis": "P1",
    "Synthesis Created": "P2",
    "Ready": "P2",
    "Low Signal": "P3",
}
PRIORITY_ORDER = {"P1": 1, "P2": 2, "P3": 3, "Done": 4}


def get_knowledge_temp_path(path: Path) -> Path:
    """生成原子写用的临时路径：{path}.tmp.{pid}.{毫秒时间戳}。"""
    return Path(f"{path}.tmp.{os.getpid()}.{int(time.time() * 1000)}")


def remove_knowledge_temp_files(target_path: Path) -> None:
    """清理 target 同目录下同名文件的 .tmp.* 残留。"""
    directory = target_path.parent
    if not directory.is_dir():
        return
    for f in directory.glob(f"{target_path.name}.tmp.*"):
        try:
            f.unlink()
        except OSError:
            continue


def write_knowledge_file_atomic(path: Path, lines: list[str]) -> None:
    """原子写：建父目录 → 写 .tmp → os.replace 替换正式文件 → 清理残留。

    失败时保留 .tmp 并抛出异常（与 ps1 Write-KnowledgeFileAtomic 一致）。
    行尾用 LF；原 ps1 用 CRLF，迁移后统一为 LF，markdown 渲染无差异。
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = get_knowledge_temp_path(path)
    try:
        content = "\n".join(lines)
        if lines:
            content += "\n"
        tmp.write_text(content, encoding="utf-8")
        os.replace(tmp, path)  # 跨平台原子 rename + 覆盖，等价 Move-Item -Force；同目录同卷
        remove_knowledge_temp_files(path)
    except OSError:
        if tmp.exists():
            print(f"[knowledge] 临时文件保留待查：{tmp}", file=sys.stderr)
        raise


def is_operational_noise(file_path: Path) -> bool:
    """判断是否为运行噪音文件（.DS_Store 或 .tmp.{pid}.{ms} 残留）。"""
    name = file_path.name
    if name == ".DS_Store":
        return True
    return bool(_TMP_SUFFIX_RE.search(name))


def scan_project_files(project_dir: Path) -> list[Path]:
    """递归列出项目内非噪音文件（过滤 .DS_Store / .tmp.N.N）。"""
    files: list[Path] = []
    for f in project_dir.rglob("*"):
        if f.is_file() and not is_operational_noise(f):
            files.append(f)
    return files


def classify_project_status(project_dir: Path, files: list[Path]) -> str:
    """判定项目知识沉淀状态（与 ps1 Get-ProjectStatus 的 if-elseif 链等价）。"""
    synthesis = project_dir / SYNTHESIS_RELATIVE
    retro = project_dir / RETRO_RELATIVE
    memory = project_dir / CARD_RELATIVE
    doc_count = len(files)

    if synthesis.exists():
        if retro.exists():
            return "Done"
        return "Synthesis Created"
    if retro.exists():
        return "Missing Synthesis"
    if doc_count >= 4 and memory.exists():
        return "Ready"
    return "Low Signal"


def status_to_priority(status: str) -> str:
    """状态 → 优先级；未知状态归 Done（与 ps1 default 一致）。"""
    return PRIORITY_MAP.get(status, "Done")


def format_mtime(mtime: float) -> str:
    """mtime（epoch 秒）→ 'yyyy-MM-dd HH:mm' 本地时间（与 ps1 LastWriteTime 格式一致）。"""
    return time.strftime("%Y-%m-%d %H:%M", time.localtime(mtime))
