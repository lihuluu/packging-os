---
name: knowledge-synthesizer
description: 扫描项目总卡、阶段产出、复盘文档和关键沟通记录，把零散工作产出提炼成可复用的结构化知识，并回写到共享知识库。适用于用户想把项目经验回写成共享规则、维护跨项目知识库、批量盘点项目沉淀覆盖率，或定期整理 Claude Code 工作结果的场景。常见触发说法包括：把这个项目的工作产出沉淀成知识库、帮我总结这些项目里重复出现的经验、把零散经验整理成可复用规则、更新共享知识库、把这次复盘回写到系统知识、盘点所有项目的知识沉淀覆盖率。不适用于项目级复盘本身；项目复盘应先交给 `project-retrospective`。
---

# Knowledge Synthesizer

## 概述

这是给 Claude Code 用的“知识沉淀入口”。

它不替代项目复盘，而是在项目复盘之后，或在跨项目整理时，把文档、决策、问题和结论抽成未来还能复用的知识。

重点不是堆积摘要，而是把经验写成你能快速扫读、Claude 也能继续维护的规则、风险信号、流程更新和品类洞察。

V2 开始，这个 skill 还负责批量盘点项目沉淀覆盖率，维护工作区级知识汇总。
V3 开始，这个 skill 还要求产出固定的“会话包 + 历史日志”，让 Claude Code 每次都按同一流程执行。
V4 开始，这个 skill 支持一键启动会话，把覆盖表、收件箱、会话包和日志草稿自动准备好。

把它理解成 3 个递进层：
- 项目级知识沉淀：把单项目经验整理成 `knowledge-synthesis.md`
- 跨项目知识回写：把可复用规则更新进 `Workspace/Knowledge/Library/`
- 批量治理与会话启动：先做覆盖盘点，再准备本轮工作区级会话包

## 典型触发句

- 把这个项目的工作产出沉淀成知识库。
- 帮我把这些项目里重复出现的经验整理成规则。
- 把这次复盘回写到系统知识。
- 我想让 Claude Code 定期整理我的项目产出，形成可复用知识。
- 帮我把这些零散经验变成结构化知识卡。
- 更新共享知识库，把这次项目的经验补进去。
- 这些产出里哪些值得沉淀成 SOP 或判断规则？
- 启动本轮知识整理会话，并自动更新覆盖表、收件箱和日志草稿。

## 使用流程

1. 读取目标范围内的项目总卡、关键阶段文档、复盘文档和重要沟通结论。
2. 先判断当前任务属于：`项目级沉淀`、`跨项目回写` 还是 `批量治理/会话启动`。
3. 需要批量整理时，先参考 [batch-scan-rules.md](./references/batch-scan-rules.md)，并优先使用 [`./scripts/get_knowledge_coverage.py`](./scripts/get_knowledge_coverage.py) 盘点项目覆盖率。
4. 使用 [knowledge-framework.md](./references/knowledge-framework.md) 提取 `决策规则`、`风险信号`、`流程更新`、`品类洞察` 和 `待验证假设`。
5. 去掉纯流水账内容，只保留对未来项目有复用价值的结论。
6. 项目级任务先更新 `knowledge-synthesis.md`；只有可跨项目复用的结论，才继续回写到 `Workspace/Knowledge/`。
7. 更新共享知识时，先保证人读层可读：优先维护 `Workspace/Knowledge/Library/knowledge-dashboard.md`、`Workspace/Knowledge/Library/workspace-knowledge-digest.md` 和分类表格页。
8. V4 优先运行 [`./scripts/start_knowledge_review_session.py`](./scripts/start_knowledge_review_session.py)，自动准备 `Workspace/Knowledge/Operations/` 下的 `coverage/`、`queue/`、`current/` 和 `history/` 所需文件。
9. 如果不走一键启动，批量模式下再运行 [`./scripts/build_knowledge_review_packet.py`](./scripts/build_knowledge_review_packet.py)，生成 `current/current-review-session.md`。
10. 更新 `workspace-knowledge-digest.md` 和项目级 `knowledge-synthesis.md`。
11. 把本轮结果记入 `Workspace/Knowledge/Operations/history/`。
12. 如果已有共享知识与本次结论冲突，标出冲突来源，而不是强行合并。
13. 共享知识与工作区级运行文件写入时，必须使用安全写入流程；成功后清理对应 `.tmp.*`，失败时保留临时文件并报错。

## 合成规则

- 只沉淀未来还能复用的结论，不复制项目过程记录。
- 每条知识都要写清楚：何时适用、为什么、应采取什么动作。
- 区分 `已验证知识`、`低置信假设` 和 `冲突待验证项`。
- 单项目观察可以沉淀，但必须标记证据强度。
- 能落到清单、模板、审批点或目录规则的知识，优先落地成这些形式。
- 知识页默认优先使用表格和一页摘要，避免长段式 AI 说明文。
- 批量模式先做“覆盖盘点”，再做“知识抽取”，不要直接跳到共享规则。
- 没有 `knowledge-synthesis.md` 的项目先进入待处理队列，不要假装已沉淀完成。
- 每轮批量整理都应留下可复盘的会话记录。
- 会话启动阶段的重复整理工作，优先让脚本完成。
- 会话准备脚本只负责准备范围和骨架，不替代知识判断与结论归纳。
- 批量扫描和会话包应忽略 `.tmp.*`、`.DS_Store` 等临时或运行噪音文件。
- 状态盘点时，`knowledge-synthesis.md` 已创建但项目仍在推进的项目，标记为 `Synthesis Created`，不要直接视为 `Done`。

## 输出要求

- 输出 `项目摘要`、`来源文档`、`已知事实`、`关键假设`、`风险`、`开放问题`、`结论沉淀` 和 `下一步动作`。
- 项目级文档必须列出来源文档。
- 共享知识库更新时，优先更新 `Workspace/Knowledge/Library/knowledge-dashboard.md` 和 `Workspace/Knowledge/Library/workspace-knowledge-digest.md`，再更新对应分类文件和索引。
- 如果发现某条经验更适合回写到已有 skill 的模板或规则，要明确指出目标文件。
- 批量模式必须额外输出 `覆盖状态`、`待处理项目` 和 `本轮工作区级结论`。
- V3 还必须输出 `当前会话包` 和 `历史日志入口`。

## 输出前检查

1. 确认目标目录已存在；不存在时先创建。
2. 工作区级文件写入必须使用安全写入流程：先写 `.tmp.*`，成功后再替换正式文件。
3. 正式写入成功后，立即清理对应目录下遗留的 `.tmp.*`。
4. 如果写入失败，保留临时文件并明确报错，不要静默吞掉异常。

## 默认归档位置

- 项目级目录：`05_Retrospective`
- 项目级推荐文件名：`knowledge-synthesis.md`
- 系统级目录：`Workspace/Knowledge/`
- 工作区级文件：
- `Library/knowledge-dashboard.md`
- `Library/workspace-knowledge-digest.md`
- `Library/decision-rules.md`
- `Library/risk-signals.md`
- `Library/process-updates.md`
- `Library/category-insights.md`
- `Library/knowledge-index.md`
- `Operations/coverage/project-knowledge-coverage.md`
- `Operations/coverage/knowledge-coverage-report.md`
- `Operations/queue/knowledge-capture-inbox.md`
- `Operations/current/current-review-session.md`
- `Operations/current/current-review-log-draft.md`
- `Operations/history/`
- 归档规则：项目级沉淀独立归档；跨项目知识应进入共享知识库，不进入 `04_Final`

## 参考资料

阅读 [knowledge-framework.md](./references/knowledge-framework.md) 查看知识分类、字段结构和回写规则。
阅读 [../../references/shared-field-glossary.md](../../references/shared-field-glossary.md) 统一项目卡、复盘和知识沉淀的公共字段词表。
阅读 [batch-scan-rules.md](./references/batch-scan-rules.md) 查看多项目扫描顺序和覆盖规则。
阅读 [review-session-playbook.md](./references/review-session-playbook.md) 查看固定执行会话的顺序。
阅读 [session-bootstrap-rules.md](./references/session-bootstrap-rules.md) 查看一键启动会话的范围和边界。
当需要项目级知识沉淀模板时，使用 [knowledge-synthesis-template.md](./assets/knowledge-synthesis-template.md)。
当需要工作区级汇总模板时，使用 [workspace-knowledge-digest-template.md](./assets/workspace-knowledge-digest-template.md)。
当需要历史记录模板时，使用 [knowledge-review-log-template.md](./assets/knowledge-review-log-template.md)。
当需要会话日志草稿模板时，使用 [current-review-log-draft-template.md](./assets/current-review-log-draft-template.md)。
处理工作区级文件写入时，优先复用 [`./scripts/knowledge_file_utils.py`](./scripts/knowledge_file_utils.py)；需要清理历史遗留临时文件时，使用 [`./scripts/cleanup-temp-files.sh`](./scripts/cleanup-temp-files.sh)。
