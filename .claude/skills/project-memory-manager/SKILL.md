---
name: project-memory-manager
description: 维护包装项目的统一项目卡，持续整理已确认事项、冻结项、开放问题、关键假设、风险和下一步动作，避免多轮协作里上下文丢失。适用于项目刚开案、阶段切换、多人协作、会议后整理、评审后更新状态，或任何“先帮我整理项目现状”的场景。常见触发说法包括：整理这个包装项目现状、更新项目卡、把会议纪要写进项目状态、当前哪些信息已经定了、帮我汇总风险和待确认项、把零散信息归到一个总表里。不适用于排执行时间线、写提案页序或比较报价。
---

# Project Memory Manager

## 概述

把包装项目中的零散信息整理成一份可持续更新的项目总卡。重点不是重复写总结，而是让后续任一 skill 都能基于同一份状态继续工作。

## 典型触发句

- 帮我整理一下这个包装项目当前状态。
- 请把这次会议纪要更新进项目卡。
- 这个项目现在已经确认了哪些事？
- 帮我汇总当前的风险、待定项和下一步动作。
- 我想要一份可以持续维护的包装项目总表。
- 先帮我把项目现状梳理出来。
- 把这些零散信息整理成一个项目总卡。

## 使用流程

1. 从 brief、会议纪要、聊天记录、阶段产出和供应商反馈里提取已确认信息。
2. 区分 `已确认`、`待确认`、`假设` 和 `冲突信息`。
3. 开案或阶段切换时，优先补齐实物规格、MOQ 预估、环保优先级、当前供应商状态、合规/标签负责人、素材授权责任人和样品验收负责人。
4. 使用统一结构汇总项目背景、冻结项、风险、依赖和下一步动作。
5. 标出自上次更新以来新增、变更或失效的信息。
6. 同步刷新 `project-tracker.md` 和 `decision-log.md`（见维护规则）。
7. 结尾提示当前最适合衔接的下一个 skill 或评审节点。

## 维护规则

- 不要把推测写成已确认事实。
- 用户或附件里互相矛盾的信息要直接标出来，不要自行合并。
- 冻结项要写清变更代价，例如影响结构、成本、交期还是法规。
- 只保留能影响后续判断的信息，避免把项目卡写成流水账。
- 任何跨阶段传递的重要结论，都应该进入项目卡。
- 如果供应商能力、MOQ、环保优先级或实物规格还不清楚，要明确写进 `开放问题` 或 `关键假设`，不要空着不提。
- 如果合规/标签信息、素材授权、食品接触材料或样品验收状态还不清楚，要写进 `开放问题` 或 `风险`，不要默认可进入最终交付。
- 每次**写入或更新** `project-memory-card.md` 后，**必须**同步刷新以下两个文件：
  1. `00_Project_Control/project-tracker.md`（从项目卡中提取当前阶段、里程碑、开放问题、风险和下一步动作，同步到推进表）
  2. `03_Design/01_Working/decision-log.md`（如果本次更新产生了新的结构性决策——如概念锁定、结构选型、视觉方向变更、材质工艺变更、跳过阶段等——在决策记录表追加一行；不覆盖已有行）

## 时间记录规则

- 项目摘要中的时间必须使用**绝对日期**（如 2026-06-21），不使用相对时间（如"距今日 59 天"）。相对时间在下次读取时必然失效。
- 每个项目卡必须包含 **里程碑时间线** 表格，记录每个关键节点的计划日期和实际日期。
- 里程碑时间线在以下时机更新：
  - **开案时**：根据 Brief 排出计划日期列
  - **阶段完成时**：填写该里程碑的实际日期
  - **发生偏差时**：在备注列写明偏差原因
- 里程碑列表可根据项目实际情况增减行，但不得删除以下标准节点：开案、Brief 确认、概念方向锁定、结构选型确认、视觉方向锁定、材质工艺确认、供应商回复、设计稿交付、印前确认、白样验收、彩样签收、大货交付、上市。
- 偏差 = 实际 - 计划。正数表示提前，负数表示延迟。

## 输出要求

- 输出 `项目摘要`、`商业硬约束`、`合规、授权与验收状态`、`里程碑时间线`、`已知事实`、`开放问题`、`关键假设`、`风险`、`依赖项` 和 `下一步动作`。
- 只要信息可得，就优先写明 `实物规格 / 内容物`、`MOQ 预估`、`环保优先级`、`当前供应商状态`、`合规/标签负责人`、`素材授权状态` 和 `样品验收状态`。
- 项目摘要中的时间一律用绝对日期，不用"距今日 X 天"。
- 每次更新时检查里程碑时间线，补填已完成的实际日期。
- 如果有历史版本差异，再补 `本次更新`。
- 语言要能被设计、供应商和项目管理角色共同理解。

## 输出后检查

- 如果本次整理确认了新的冻结项、风险、供应商/MOQ 信息、时间线/预算变化、法规/环保约束、素材授权状态或样品验收状态，必须直接写进项目卡，不要只停留在正文分析里。
- 如果发现上下游文档已明显晚于项目卡，必须在 `风险` 或 `下一步动作` 中标记状态漂移。
- 如果通过脚本批量写入或更新项目文档，应使用 `project_file_utils.py` 的原子写入流程；手工/Agent 写入后，日常治理必须通过 `validate-packaging-os` 检查是否残留 `.tmp.*`。
- 项目级 `project-dashboard.md` 已退役（不再生成），跨项目浏览请直接看各项目 `00_Project_Control/project-memory-card.md` + `project-tracker.md`。
- 同步刷新 `00_Project_Control/project-tracker.md`：从项目卡提取当前阶段、里程碑时间线、开放问题、风险和下一步动作，覆盖写入推进表。推进表的里程碑行应与项目卡一致。
- 同步刷新 `03_Design/01_Working/decision-log.md`：检查本次更新是否产生了新的结构性决策（概念方向锁定、结构选型、视觉方向变更、材质工艺变更、阶段跳过、客户确认等）。如果有，在 `## 决策记录` 表格追加新行（编号递增），不覆盖历史行。其余字段块（已知事实、关键假设、风险、开放问题、结论沉淀、下一步动作）允许覆盖更新。

## 默认归档位置

- 默认目录：`00_Project_Control`
- 推荐文件名：`project-memory-card.md`
- 归档规则：属于持续更新文档，应覆盖更新，不进入 `04_Final`

## 参考资料

阅读 [memory-framework.md](./references/memory-framework.md) 查看项目卡字段、更新规则和风险信号。
阅读 [../../references/shared-field-glossary.md](../../references/shared-field-glossary.md) 统一项目卡、复盘和知识沉淀的公共字段词表。
阅读 [../../references/compliance-and-asset-standard.md](../../references/compliance-and-asset-standard.md) 查看合规与素材授权状态字段。
阅读 [../../references/sample-acceptance-standard.md](../../references/sample-acceptance-standard.md) 查看样品与大货验收状态字段。
当需要项目卡模板时，使用 [project-memory-card-template.md](./assets/project-memory-card-template.md)。

## 脚本入口

- 批量检查项目卡是否落后于最新产出（Windows）：[check-memory-drift.cmd](./scripts/check-memory-drift.cmd)
- 批量检查项目卡是否落后于最新产出（Mac/Linux）：[check-memory-drift.sh](./scripts/check-memory-drift.sh)
- 批量检查项目卡是否落后于最新产出（Python 底层脚本）：[check-memory-drift.py](./scripts/check-memory-drift.py)
- 项目状态一键同步：[sync-project.py](./scripts/sync-project.py) / [sync-project.cmd](./scripts/sync-project.cmd) / [sync-project.sh](./scripts/sync-project.sh)（写完项目卡后同步追踪表和决策日志）
- 项目文档安全写入工具：[project_file_utils.py](./scripts/project_file_utils.py)
- 清理项目目录下的临时文件（Windows，默认 dry-run）：[cleanup-project-temp-files.cmd](./scripts/cleanup-project-temp-files.cmd)
- 清理项目目录下的临时文件（Mac/Linux，默认 dry-run）：[cleanup-project-temp-files.sh](./scripts/cleanup-project-temp-files.sh)
