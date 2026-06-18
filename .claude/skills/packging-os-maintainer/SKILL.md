---
name: packging-os-maintainer
description: 维护 Packging OS 这套 Claude Code 系统的治理一致性、skill 路由、模板字段、测试样例和共享脚本。适用于新增或修改 `.claude/skills/`、`CLAUDE.md`、`README.md`、`.claude/references/skills-test-cases.md`、共享模板、共享字段词表或 `packging-os-maintainer/scripts/validate-packging-os.cmd` / `validate-packging-os.sh` / `validate-packging-os.ps1` / `validate-packging-os.py` 之后的巡检、补同步和回归检查场景。常见触发说法包括：帮我检查这套 Claude Code 系统有没有漂、我刚改了几个 skill 顺手把文档和路由补齐、给 Packging OS 做一次治理巡检、我新增了一个 skill 帮我把 README 和测试补上、跑一遍 Packging OS 验证并告诉我还缺什么。不适用于具体包装项目的业务判断。
---

# Packging OS Maintainer

## 概述

把这个 skill 当成 Packging OS 的系统治理入口，而不是包装项目业务入口。
它的职责是保证这套 Claude Code 系统在你持续迭代时仍然一致、可发现、可验证：

- skill 新增或收边后，相关文档是否同步
- 路由变化后，`packging-os` 和测试样例是否跟上
- 模板或词表变化后，共享字段是否漂移
- 共享脚本是否仍然能跑
- 临时文件、废弃命名和旧路径残留能否被自动发现

如果用户在做具体包装项目判断，回到对应业务 skill；不要用这个 skill 代替包装分析。

## 使用流程

1. 先判断这次变更属于哪一类：`skill 新增/修改`、`路由调整`、`模板/词表调整`、`治理文档调整`、`共享脚本调整`。
2. 只读取和本次变更直接相关的文件；必要时再补读 `CLAUDE.md`、`README.md`、`.claude/references/skills-test-cases.md`、`packging-os`。
3. 如果本次修改了包装业务 skill，按 [`governance-checklist.md`](./references/governance-checklist.md) 检查 description 边界、引用路径、README 技能表、`packging-os` 路由和回归样例是否同步。
4. 如果本次修改了项目卡、复盘或知识沉淀模板，检查 [`../../references/shared-field-glossary.md`](../../references/shared-field-glossary.md) 以及相关模板是否仍然一致。
5. 如果本次修改了共享脚本或验证规则，优先回读脚本引用路径，并实际运行 Windows 入口 [`validate-packging-os.cmd`](./scripts/validate-packging-os.cmd) 或 Mac/Linux 入口 [`validate-packging-os.sh`](./scripts/validate-packging-os.sh)。
6. 在宣布完成前，至少跑一次治理校验；Windows 默认跑 `./scripts/validate-packging-os.cmd`，Mac/Linux 默认跑 `sh ./scripts/validate-packging-os.sh`。如果变更影响了脚本本身，先修脚本再继续其他同步。
7. 输出时使用 [`governance-review-template.md`](./assets/governance-review-template.md) 的结构，明确写出已同步项、未完成项、验证结果和下一步动作。
8. 如果这次变更涉及命名规范或文件治理，额外检查是否出现 `.DS_Store`、`*.tmp.*`、废弃文件名和旧路径引用。

## 必查项

- 新增 skill 时：
  - `README.md` 技能表是否新增条目
  - 如果是包装工作流叶子 skill，`packging-os`、`workflow-map.md`、`output-routing.md` 是否需要同步
  - `.claude/references/skills-test-cases.md` 是否补了核心样例和边界样例
- 修改现有 skill 边界时：
  - frontmatter `description` 是否同时写清适用场景和不适用场景
  - 现有测试样例是否要改预期
- 修改模板或共享字段时：
  - `project-memory-manager`、`project-retrospective`、`knowledge-synthesizer` 三类模板是否仍一致
  - `packging-os/references/output-templates.md` 是否跟上
- 修改治理文档时：
  - `CLAUDE.md`、`README.md`、相关 skill 是否互不冲突
  - 文档引用的本地文件是否存在
- 修改共享脚本或清理规则时：
  - 清理脚本和治理校验脚本的匹配范围是否一致
  - 是否覆盖 `.DS_Store`、`*.tmp.*`、废弃文件名和旧路径引用

## 输出规则

- 先写 `本次变更范围`，不要直接跳到结论。
- 写清 `已同步文件` 和 `仍待同步文件`，避免只说“已经检查过”。
- 如果验证失败，直接列出失败项和受影响文件，不要模糊描述。
- 如果本次只做分析、不改文件，也要明确给出推荐的同步清单。
- 结尾必须写 `下一步动作`；如果还有明确后续治理任务，推荐继续使用 `packging-os-maintainer`。

## 参考资料

阅读 [governance-checklist.md](./references/governance-checklist.md) 查看不同变更类型对应的同步矩阵和最小验证要求。
当变更涉及共享字段时，阅读 [../../references/shared-field-glossary.md](../../references/shared-field-glossary.md)。
输出治理结果时，优先使用 [governance-review-template.md](./assets/governance-review-template.md)。

## 脚本入口

- 一键治理校验（Windows 原生，不依赖 Python）：[validate-packging-os.cmd](./scripts/validate-packging-os.cmd)
- 一键治理校验（Mac/Linux，自动选择 python3、python 或 pwsh）：[validate-packging-os.sh](./scripts/validate-packging-os.sh)
- 底层治理校验（PowerShell，Windows 原生）：[validate-packging-os.ps1](./scripts/validate-packging-os.ps1)
- 底层治理校验（Python，Mac/Linux 首选）：[validate-packging-os.py](./scripts/validate-packging-os.py)
- 共享验证配置（标题定义）：[validation-config.json](./scripts/validation-config.json)
- 日常治理总入口（Windows）：[daily-governance-check.cmd](./scripts/daily-governance-check.cmd)
- 日常治理总入口（Mac/Linux）：[daily-governance-check.sh](./scripts/daily-governance-check.sh)
- 新建标准项目目录（Windows）：[init-project.cmd](./scripts/init-project.cmd)
- 新建标准项目目录（Mac/Linux）：[init-project.sh](./scripts/init-project.sh)
- 新建标准项目目录（PowerShell 底层脚本）：[init-project.ps1](./scripts/init-project.ps1)
- 新建标准项目目录（Python 底层脚本）：[init-project.py](./scripts/init-project.py)
- 项目目录临时文件清理（Windows）：[`../project-memory-manager/scripts/cleanup-project-temp-files.cmd`](../project-memory-manager/scripts/cleanup-project-temp-files.cmd)
- 项目目录临时文件清理（Mac/Linux）：[`../project-memory-manager/scripts/cleanup-project-temp-files.sh`](../project-memory-manager/scripts/cleanup-project-temp-files.sh)
- 知识库临时文件清理：[`../knowledge-synthesizer/scripts/cleanup-temp-files.sh`](../knowledge-synthesizer/scripts/cleanup-temp-files.sh)

`.cmd` 和 `.sh` 是跨平台入口，负责选择合适运行时；`.ps1` 和 `.py` 是底层校验器，共享 `validation-config.json` 中的标题定义。Windows 上优先用 `validate-packging-os.cmd`，Mac/Linux 上优先用 `sh validate-packging-os.sh`。
