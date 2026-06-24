# 待修复：UserPromptSubmit hook 报 `powershell.exe: command not found`（Mac）

- 日期：2026-06-19
- 状态：✅ **已执行（2026-06-19）**——新 `.py` 已建、`settings.json` 已加 UserPromptSubmit、`settings.local.json` 已删 UserPromptSubmit
- 方案：**python 化 + 提升到公开 `settings.json`**（照搬现有 SessionStart / PostToolUse 两个 hook 的写法）
- 前提确认：**Windows 已装 Python** ✅（2026-06-19 用户确认）
- 方案演进：最初考虑"留在 local + `$CLAUDE_PROJECT_DIR`"，已优化为"**提升到公开 `settings.json`**"——彻底绕开 Dropbox 同步 `settings.local.json` 的坑

---

## 1. 症状

每次提交 prompt 都出现 non-blocking hook 错误：

```
UserPromptSubmit hook error
Failed with non-blocking status code: /bin/sh: powershell.exe: command not found
```

## 2. 根因

`.claude/settings.local.json` 的 `UserPromptSubmit` hook 调用：

```
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "D:\Dropbox\Packaging_OS\.claude\hooks\check-project-memory-drift.ps1"
```

两个问题：① `powershell.exe` 在 Mac 不存在；② 路径是 Windows 的 `D:\`。配置是 Windows 机器遗留（`settings.local.json` 在 Dropbox 同步）。

## 3. 这个 hook 在做什么（有用，别删）

扫 `Workspace/Projects/` 所有项目，比较记忆卡 `project-memory-card.md` 和最新产出文件的修改时间，落后超过 1 分钟就注入 `<packaging-os-reminder>` 提醒；没落后就 `exit 0` 静默。逻辑详见 `.claude/hooks/check-project-memory-drift.ps1`。

## 4. 当前系统所有 hook（2026-06-19 盘点）

| Hook 事件 | 来源配置 | command 写法 | Mac 状态 |
|----------|---------|-------------|---------|
| SessionStart | `settings.json`（公开） | `python ...py \|\| python3 ...py` + 相对路径 | ✅ 正常 |
| PostToolUse (Edit\|Write\|…) | `settings.json`（公开） | `python ...py \|\| python3 ...py` + 相对路径 | ✅ 正常 |
| **UserPromptSubmit** | `settings.local.json`（本地） | `powershell.exe` + `D:\` 绝对路径 | ❌ **报错** |

**关键观察**：前两个在公开配置 + 跨平台写法 → 正常；第三个在本地配置 + Windows 写死 → 挂。**第三个照搬前两个的写法即可。**

## 5. 修复方案（已定）

### 核心三步

1. **新建** `.claude/hooks/check-project-memory-drift.py`（跨平台 python，草稿见下）
2. **`settings.json` 加** `UserPromptSubmit` 段（和现有 SessionStart/PostToolUse 并列）
3. **`settings.local.json` 删掉** `UserPromptSubmit`（已移到公开配置，本地不再需要）

### `settings.json` 要加的段

```json
"UserPromptSubmit": [
  {
    "matcher": "",
    "hooks": [
      {
        "type": "command",
        "command": "python .claude/hooks/check-project-memory-drift.py || python3 .claude/hooks/check-project-memory-drift.py"
      }
    ]
  }
]
```

### `.claude/hooks/check-project-memory-drift.py` 草稿（跨平台，等价 .ps1，直接可用）

```python
#!/usr/bin/env python3
"""Cross-platform equivalent of check-project-memory-drift.ps1.
Scans Workspace/Projects; flags project memory cards that lag behind the latest
project files. Silent exit when nothing is stale. Works on Mac and Windows."""
import sys
from pathlib import Path
from datetime import datetime

root = Path(__file__).resolve().parent.parent.parent  # .claude/hooks -> repo root
projects_root = root / "Workspace" / "Projects"

if not projects_root.exists():
    sys.exit(0)

IGNORED = {".DS_Store", "Thumbs.db", "desktop.ini", ".gitkeep", ".gitignore"}
drifted = []

for project in sorted(p for p in projects_root.iterdir() if p.is_dir()):
    card = project / "00_Project_Control" / "project-memory-card.md"

    latest = None  # (path, mtime)
    for f in project.rglob("*"):
        if not f.is_file():
            continue
        if "00_Project_Control" in f.relative_to(project).parts:
            continue
        if ".tmp." in f.name or f.name in IGNORED:
            continue
        m = f.stat().st_mtime
        if latest is None or m > latest[1]:
            latest = (f, m)

    if latest is None:
        continue

    latest_file, latest_mtime = latest
    fmt = lambda t: datetime.fromtimestamp(t).strftime("%Y-%m-%d %H:%M")

    if not card.exists():
        drifted.append((project.name, "missing card", "", fmt(latest_mtime),
                        str(latest_file.relative_to(project))))
        continue

    card_mtime = card.stat().st_mtime
    if latest_mtime > card_mtime + 60:  # 1 分钟
        drifted.append((project.name, "card may be stale", fmt(card_mtime),
                        fmt(latest_mtime), str(latest_file.relative_to(project))))

if not drifted:
    sys.exit(0)

print("<packaging-os-reminder>")
print("Some project memory cards may be behind the latest project files. If the user "
      "request touches project status, project memory, dashboards, or handoff state, "
      "consider reminding them or updating the relevant card explicitly.")
for name, status, card_t, latest_t, latest_f in drifted[:5]:
    print(f"- {name}: {status}; card={card_t}; latest={latest_t}; latest_file={latest_f}")
if len(drifted) > 5:
    print(f"- ... plus {len(drifted) - 5} more project(s).")
print("</packaging-os-reminder>")
sys.exit(0)
```

> 备选方案 B（不推荐）：直接删 UserPromptSubmit，失去自动检查，手动跑 `check-memory-drift.py --all`。

## 6. 跨机器情况（已解决）

- Windows Python 已确认装了 ✅
- 提升到公开 `settings.json` 后，hook **随仓库共享**，Mac / Windows 都从仓库读 → 不再依赖 Dropbox 同步 `settings.local.json`
- `settings.local.json` 删掉 UserPromptSubmit 后只剩本地项（permissions/env/token），Dropbox 同步它也无害

## 7. 关键诊断信息（执行时用）

- 要改的文件：
  - `settings.json`（公开，**无 token，可 Read/Edit**）
  - `settings.local.json`（**含 token，只能用 jq 改，不要 Read 整个文件**）
- 从 `settings.local.json` 删 UserPromptSubmit 的 jq 命令：
  ```bash
  f=".claude/settings.local.json"
  jq 'del(.hooks.UserPromptSubmit)' "$f" > "$f.tmp" && mv "$f.tmp" "$f"
  ```
- Windows 源脚本：`.claude/hooks/check-project-memory-drift.ps1`（逻辑见第 3 节，修复后可保留作备份或删除）

## 8. 执行清单（2026-06-19 已落地）

- [x] 创建 `.claude/hooks/check-project-memory-drift.py`（第 5 节草稿）✅
- [x] `settings.json` 加 `UserPromptSubmit` 段（第 5 节 JSON）✅
- [x] `settings.local.json` 删 `UserPromptSubmit`（第 7 节 jq 命令，别 Read）✅
- [x] 脚本单独运行验证：`python3 …/check-project-memory-drift.py` → `EXIT=0` 无异常；两个 JSON 均合法 ✅
- [ ] 提交一个测试 prompt，确认不再报 `powershell.exe: command not found`（**待用户下一条 prompt 自然验证**）
- [ ] （可选）commit `settings.json` + 新 `.py` 到仓库（让 Windows 机器也自动受益）
