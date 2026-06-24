# Packaging OS 待提交变更清单

> 用途：记录已写入工作区但**暂未 git commit / push** 的变更，便于跨会话追溯。
> 提交完成后请删除本文件，或把对应条目移到 `reviews/` 下的治理快照。

---

## 当前状态（截至 2026-06-22）

- 分支：`main`
- 领先 `origin/main`：**9 个 commit**（已 commit，未 push）
- 工作区未提交修改：**1 个文件**
- 治理校验：`validate-packaging-os` passed

---

## 一、未提交修改（工作区）

### `.claude/hooks/check-project-memory-drift.py`

**变更类型**：bugfix / 兼容性补丁

**修改内容**（diff 摘要）：

```python
+import io
 import sys
 from pathlib import Path
 from datetime import datetime

+# Windows 终端编码兼容（避免中文项目名输出成 GBK 乱码）
+if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf-8-sig"):
+    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
+if sys.stderr.encoding and sys.stderr.encoding.lower() not in ("utf-8", "utf-8-sig"):
+    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")
```

**根因**：
- Windows 中文终端默认 GBK 编码，`print()` 含中文项目名（如 `HT2385_猴王·手筑茯茶五年陈950克`、`岁藏天尖`、`茶+康养调味茶系列`）时会抛 `UnicodeEncodeError` 或输出乱码。
- 该 hook 由 `UserPromptSubmit` 触发，崩溃会让用户每次提交 prompt 都看到栈追溯。

**风险评估**：
- Mac/Linux 已是 UTF-8 环境，`if` 条件不成立，零影响。
- Windows GBK 终端：`errors="replace"` 保证不再崩溃；中文输出改为 UTF-8 字节，部分老终端可能仍显示乱码，但现代 Windows Terminal / VSCode 终端默认 UTF-8 已无问题。
- 不影响 hook 退出码逻辑。

**建议 commit message**：

```
fix(hook): force utf-8 stdout/stderr in memory-drift checker

Windows GBK terminals crash on UnicodeEncodeError when the checker
prints Chinese project names. Wrap stdout/stderr in TextIOWrapper
only when the active encoding is not UTF-8, so Mac/Linux behavior
is unchanged.
```

---

## 二、未推送 commit（本地 main 领先 origin/main 共 9 个）

整组 commit 主题：**PowerShell zero-out + 跨平台 Python 化**

| # | hash | message | 说明 |
|---|------|---------|------|
| 1 | `7a00b79` | fix(hook): make UserPromptSubmit cross-platform (python + public settings.json) | 把 UserPromptSubmit hook 从 .ps1 迁到 python，settings.json 同步 |
| 2 | `d9c1c40` | feat(knowledge-synthesizer): add cross-platform python scripts + thin-shell entries | knowledge-synthesizer 新增 py 脚本 + 跨平台壳 |
| 3 | `18ff2a6` | chore(knowledge-synthesizer): remove migrated PowerShell scripts | 清掉已迁走的 ps1 |
| 4 | `4d0a53b` | chore(project-memory-manager): migrate project-file-utils.ps1 -> python | project_file_utils 改为 py |
| 5 | `71b74a3` | refactor(scripts): drop PowerShell from entry-point .sh/.cmd (call .py directly) | 入口 .sh/.cmd 直接调 py，不再绕一层 ps1 |
| 6 | `afd903d` | chore(scripts): remove last 4 PowerShell scripts + sync docs (ps1 zero) | 清掉最后 4 个 ps1，同步文档 |
| 7 | `7302846` | docs: drop stale .ps1 references after PowerShell zero-out | 清掉文档里残留的 .ps1 引用 |
| 8 | `557fffb` | chore: remove unused blender template (tea_tiandi_gift_box.py) | 删一个没用过的 blender 模板 |
| 9 | `d5b4647` | fix(hooks): prefer python3 over python in hook commands (avoid Mac stderr noise) | hook 命令改为 `python3 ... || python ...`，避开 Mac 上 python → python3 警告 |

**关联性**：1–7 是同一主题（PowerShell zero-out），8 是顺手清理，9 是 1 的 Mac 端打磨。
**风险**：本地 `validate-packaging-os.cmd` 已通过；临时文件、漂移、ps1 残留均为 0。

---

## 三、待用户决策的动作

- [ ] 是否提交未提交的 hook 编码补丁（合并到 #9 之后作为 #10）
- [ ] 是否 `git push origin main` 把本地 9–10 个 commit 推到远端
- [ ] 推送完成后删除本文件（或迁移到 `reviews/2026-06-22.md` 做历史快照）

---

## 四、下次治理检查时的对照动作

1. 跑 `git status`：若本文件列出的未提交修改仍在 → 提示用户决策。
2. 跑 `git log origin/main..HEAD`：若未推送 commit 数仍为 9（或+1）→ 提示用户 push。
3. 若上述两项均已清空，但本文件仍存在 → 视为遗留垃圾，可删除或转为历史治理快照。
