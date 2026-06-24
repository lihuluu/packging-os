# Packaging OS 治理检查清单

## 1. skill 新增

适用场景：
- 新增 `.claude/skills/<skill-name>/`
- 给现有系统补一个全新叶子 skill 或系统治理 skill

最小同步项：
- `README.md` 的完整技能列表
- 如果是包装工作流叶子 skill：
  - `.claude/skills/packaging-os/SKILL.md`
  - `.claude/skills/packaging-os/references/workflow-map.md`
  - `.claude/skills/packaging-os/references/output-routing.md`
  - 如有通用输出模板变化，再看 `output-templates.md`
- `.claude/references/skills-test-cases.md`：
  - 至少补 1 到 3 条核心样例
  - 至少补 1 条边界或治理样例

验证：
- skill 内 `SKILL.md` 存在
- `SKILL.md` 引用的本地文件存在
- Windows：`.claude\skills\packaging-os-maintainer\scripts\validate-packaging-os.cmd`
- Mac/Linux：`sh .claude/skills/packaging-os-maintainer/scripts/validate-packaging-os.sh`

## 2. skill 边界收紧或放宽

重点检查：
- frontmatter `description` 是否写清：
  - 它处理什么
  - 什么时候触发
  - 什么场景不优先使用
- 相关边界样例是否需要改预期
- 如果路由判断发生变化，`packaging-os` 是否同步

高风险信号：
- 只改了正文，没改 frontmatter `description`
- skill 已经开始吞掉相邻阶段任务
- README 描述和 skill description 不一致

## 3. 模板或共享字段变更

重点文件：
- `.claude/references/shared-field-glossary.md`
- `project-memory-manager`
- `project-retrospective`
- `knowledge-synthesizer`
- `packaging-os/references/output-templates.md`

最小检查：
- 三类模板是否仍使用统一公共字段
- 词表变化是否反映到 framework 和 asset 模板
- 没有把同义字段重新写回去
- 如果变更会通过脚本写入项目级文档，必须复用 `project-memory-manager/scripts/project_file_utils.py` 或等价的原子写入流程，并确保失败后临时文件会被治理校验发现

## 4. 治理文档变更

适用文件：
- `CLAUDE.md`
- `README.md`
- `.claude/references/skills-test-cases.md`

最小检查：
- `CLAUDE.md` 是上位规则，不得和 README 或 skill 指令冲突
- README 负责给人看，不能替代 skill 路由本体
- `.claude/references/skills-test-cases.md` 要覆盖新路由或新边界

## 5. 共享脚本或验证脚本变更

适用文件：
- `.claude/skills/packaging-os-maintainer/scripts/validate-packaging-os.py`
- 被多个 skill 共用的脚本

最小检查：
- 脚本路径和被引用位置一致
- 真正运行一次脚本，不只做静态阅读
- 如果脚本用于治理检查，失败输出要能定位到文件或规则
- 如果脚本负责清理临时文件，匹配范围要覆盖 `.DS_Store`、`Thumbs.db`、`desktop.ini`、`~$*`、`*.tmp`、`*.tmp.*`、`*.bak`、`*.log`、空 `.gitkeep` 和 `__pycache__/`
- 如果脚本负责治理校验，至少要能发现临时文件 / 临时目录、废弃文件名和旧路径引用
- 如果新增项目级写入脚本，必须说明安全写入策略：先写同目录临时文件，再原子替换目标文件，最后清理同目标名的 `.tmp.*` 残留

高风险信号：
- 清理脚本和校验脚本的匹配范围不一致
- 只会报“有问题”，但不能指出具体文件
- 旧命名已经在 README 标为废弃，但校验脚本仍无法发现

## 6. 推荐输出格式

建议固定输出这些段落：

1. `本次变更范围`
2. `已同步文件`
3. `验证结果`
4. `风险与遗留`
5. `下一步动作`

不要只写“已检查完毕”或“没有问题”，而不说明检查了什么。

