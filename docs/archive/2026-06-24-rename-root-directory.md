# 根目录改名操作指南：Packging_OS → Packaging_OS

> 日期：2026-06-24
> 状态：**待执行**（系统内部 Packging→Packaging 改名已完成，本指南是「根目录」这一最后保留项的操作步骤）

## 背景

2026-06-24 系统级改名 `Packging` → `Packaging` 已完成（文档、skill ID、脚本名、memory 索引全部对齐，治理校验通过）。当时**刻意保留**了两项外部标识：

- GitHub remote URL `lihuluu/packaging-os.git`
- 本地仓库根目录 `Packging_OS`

保留原因是它们有跨系统副作用（Dropbox 同步、Claude Code memory bucket、IDE workspace、cc-connect、已分享链接）。本指南处理**本地根目录**这一项。GitHub remote 改名另议。

详见 `CHANGELOG.md` 的 `[Unreleased] - Rename Packging → Packaging` 段落。

---

## 硬约束（动手前必读）

1. **当前 Claude 会话就跑在该目录里** —— 改名会让当前会话的工作目录当场失效、后续操作全部断掉。**改名必须在 Claude 会话之外、在终端手动执行**。
2. **memory bucket 必须先迁移** —— Claude Code 的 memory 按工作目录绝对路径编码成 bucket 名（`/` 和 `_` 都替换成 `-`）。目录一改，bucket 名就变，旧 bucket 里的 memory 会失联。**4 条 memory**（cc-connect 代理、settings token 规则、脚本规范、改名记录）会全部不加载。
3. **两端（Mac + Windows）bucket 各自独立** —— bucket 在各自机器的 `~/.claude/projects/`（Mac）/ `%USERPROFILE%\.claude\projects\`（Windows），**不在 Dropbox 里，不会自动同步**。两端要各自迁各自的 bucket。
4. **Dropbox 会全量重同步** —— 把改名当成「删旧 + 建新」，整个仓库（含 `.git` 全部历史）重新上传下载。**`.git` 被 Dropbox 重同步有损坏风险**，同步期间任何一端都不要开 git 操作。

## 不受影响（已验证）

- **git 历史 / remote / 分支**：`core.worktree` 未设，不依赖父目录名。
- **所有脚本**：用 `Path(__file__).resolve().parents[4]` 推断 root，不写死目录名（见 `validate-packaging-os.py`、`init-project.py` 等）。
- **治理校验 `validate-packaging-os.sh`**：跨平台，不引用根目录名。

---

## 完整流程（按时序）

```
① 两端准备：关闭占用 Packging_OS 路径的程序
② Mac 端：迁 bucket + 改目录名
③ Dropbox 同步：Windows 的目录名自动跟着变
④ Windows 端：迁 Windows 的 bucket
⑤ 两端各改 IDE workspace；Mac 另改 cc-connect work_dir
⑥ 两端在新路径启动 Claude，确认 memory 还在 → 跑 validate
```

### ① 两端准备

两端都做：
- 退出所有 Claude Code 会话（避免工作目录变动）
- 关闭 IDE / 编辑器里打开该项目的 workspace（避免 Dropbox 生成冲突副本）
- **Windows 端无 cc-connect**，跳过 cc-connect 相关；Mac 端有 cc-connect，第 ⑤ 步要改其 work_dir。

### ② Mac 端（在 Mac 终端执行）

```bash
# 2a. 先迁 memory bucket（bucket 名已确认：下划线编码成连字符）
mv "/Users/ethan/.claude/projects/-Users-ethan-Library-CloudStorage-Dropbox-Packging-OS" \
   "/Users/ethan/.claude/projects/-Users-ethan-Library-CloudStorage-Dropbox-Packaging-OS"

# 2b. 改根目录名
mv "/Users/ethan/Library/CloudStorage/Dropbox/Packging_OS" \
   "/Users/ethan/Library/CloudStorage/Dropbox/Packaging_OS"
```

### ③ 等 Dropbox 同步

- Mac 端改名后，Dropbox 上传到云端，Windows 端 Dropbox 客户端会把 `D:\Dropbox\Packging_OS` 自动重命名为 `Packaging_OS`。
- **等 Dropbox 同步完成（托盘图标停止转圈）再进下一步。**
- 同步期间两端都**不要**开 git 操作（避免 `.git` 损坏）。

### ④ Windows 端（PowerShell，等同步完后）

Windows bucket 的编码（盘符 `D:\`、用户名）无法从 Mac 端确认。用「启动新会话建新 bucket → 复制旧 memory」最稳，不靠猜名字：

```powershell
# 4a. 先在 D:\Dropbox\Packaging_OS 启动一次 Claude Code，让它建好新 bucket，然后退出

# 4b. 查看现有 bucket（会列出旧 Packging bucket 和新 Packaging bucket 两个）
Get-ChildItem $env:USERPROFILE\.claude\projects\ -Directory | Where-Object Name -like "*Pack*"

# 4c. 把旧 bucket 的 memory 复制到新 bucket（替换 <旧> <新> 为上一步查到的实际名字）
Copy-Item "$env:USERPROFILE\.claude\projects\<旧Packging-bucket>\*" `
          "$env:USERPROFILE\.claude\projects\<新Packaging-bucket>\" -Recurse
```

> 如果两端 memory 内容不一致（各自独立积累），复制前先看一眼旧 bucket 的 `MEMORY.md`，决定保留哪些 / 是否合并。

### ⑤ IDE workspace 与 cc-connect

- **两端**：IDE / 编辑器的 workspace 路径改成新的（`.../Packaging_OS` → `.../Packaging_OS`；Windows 同理）。
- **仅 Mac**：cc-connect 的 work_dir 改成 `/Users/ethan/Library/CloudStorage/Dropbox/Packaging_OS`。
- **Windows**：无 cc-connect，跳过。

### ⑥ 验证（两端各自）

```bash
# Mac：在新路径启动 Claude，检查 memory 是否还在
cd ~/Library/CloudStorage/Dropbox/Packaging_OS
claude
# 进入后应能看到 cc_connect_proxy / packaging-os-cross-platform-scripts 等 memory

# 跑治理校验
sh .claude/skills/packaging-os-maintainer/scripts/validate-packaging-os.sh
# 期望输出：Packaging OS validation passed.
```

Windows 端同理，在新路径 `D:\Dropbox\Packaging_OS` 启动并跑 `validate-packaging-os.cmd`。

---

## 风险与回滚

| 风险 | 应对 |
|---|---|
| memory bucket 名拼错，新会话读不到 memory | Mac bucket 名已确认可直接 mv；Windows 用「启动新会话建新 bucket → 复制」法绕过猜名 |
| Dropbox 同步损坏 `.git` | 同步期间不开 git；万一损坏，从 GitHub remote 重新 clone（`lihuluu/packaging-os.git`） |
| 改名后想反悔 | `mv` 改回 `Packging_OS` + bucket 改回旧名即可，完全可逆 |

## 改完后要更新的文档（改完目录名再做）

1. `CHANGELOG.md`：把 `Packging_OS` / `D:\Dropbox\Packging_OS` 从 `[Unreleased]` 的 **Kept As-Is** 段挪到 **Renamed** 段，注明两端已改 + Dropbox 已同步。
2. memory `cc_connect_proxy.md` 第 26 行：work_dir 路径 `Packging_OS` → `Packaging_OS`。
3. 跑一遍 `validate-packaging-os.sh` 确认新路径下全绿。

> GitHub remote URL `lihuluu/packaging-os.git` 改名是**独立的公开仓库操作**（涉及已分享链接、clone 地址、CI），不在本指南范围，单独决策。
