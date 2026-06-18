---
name: packging-os
description: 包装设计工作室总控与路由 skill，用于先判断项目现在处于哪一步，再决定该先做 brief、研究定位、概念、结构、视觉、材质、供应商沟通、提案准备、印前检查还是复盘。当前默认业务域是茶叶包装设计；当用户未说明品类时，按茶叶 SKU、茶礼盒、茶叶标签或茶叶包装版本项目理解。适用于用户不知道先做什么、一个请求跨多个阶段、需要先整理项目状态，或想把包装项目从 0 到落地梳理成完整流程的场景。遇到明确非茶叶品类时，保留通用工作流，但必须提示当前缺少该品类专用规则。当用户已经明确指定单一环节交付物时，不优先使用本 skill，应直接交给对应子 skill。
---

# Packging OS

## 概述

把这个 skill 当成包装设计工作室的总控系统。它的职责不是直接替你做某一个单点任务，而是判断当前阶段、只追问真正关键的问题，并输出可以继续推进项目的结构化交付物。

优先把它当成“路由器 + 项目总卡入口”，而不是某个具体环节的替代者。

当前默认业务域是茶叶包装设计。茶叶是第一套成熟垂类，不是系统唯一未来方向；通用工作流骨架必须保留，品类细节按 [domain-strategy.md](../../references/domain-strategy.md) 处理。

## 典型触发句

- 帮我把这个茶叶包装项目从 brief 到提案梳理成完整流程。
- 我现在有一个茶礼盒需求，但不知道应该先做定位、结构还是视觉。
- 这个项目同时涉及概念、盒型和材质，你帮我排一下优先级。
- 请按包装设计完整流程，告诉我现在这个茶叶项目卡在哪一步。
- 我想把这个茶叶包装需求拆成阶段任务和对应交付物。
- 帮我整理一下这个包装项目当前状态，再告诉我下一步该做什么。
- 这个茶叶包装项目现在适合先找供应商、先做打样，还是先补策略？
- 这个茶叶 SKU 包装该从哪一步开始做？
- 茶礼盒先做盒型还是先做视觉比较合理？

## 使用流程

1. 先检查是否已有统一项目状态；如果没有，优先走 `project-memory-manager` 整理项目卡。
2. 当用户问继续推进、当前进度、最近哪些项目动过、项目状态，但没有点名单一阶段时，按 `Workspace/Projects/` 下各项目目录的修改时间排序，依次读相关项目的 `00_Project_Control/project-memory-card.md` 和 `00_Project_Control/project-tracker.md`，再决定下一步 skill。
3. 根据用户请求、附件、项目卡或当前产物类型，识别项目所处阶段。
4. 如果阶段不清晰，只追问 intake 清单里那些会阻塞判断的问题。
5. 依据 [workflow-map.md](./references/workflow-map.md) 选择对应工作流层，并明确应该调用哪个子 skill。
6. 如果当前阶段切换风险高，按 [bridge-node-rules.md](./references/bridge-node-rules.md) 先决定是否插入 `概念测试`、`货架模拟`、`开箱测试`、`概念到材质翻译` 或 `供应商可行性确认`。
7. 结合 [output-templates.md](./references/output-templates.md) 输出一个明确交付物。
8. 依据 [output-routing.md](./references/output-routing.md) 为该交付物指定默认归档位置、推荐文件名和是否应进入 `Final`。
9. 结尾必须补充：已知事实、假设、风险、下一步动作，以及建议衔接的下一个 skill。

命名约束：
- skill id 与 skill 目录统一使用 `kebab-case`
- 项目文档与知识文档文件名统一使用 `kebab-case`
- 产物命名以 `output-routing.md` 为准，不继续新增 `project_tracker.md`、`structure-selection.md` 这类旧名

## Intake 清单

在做不可逆建议前，优先确认这些约束：
- 产品 / SKU 与品类；未说明品类时默认按茶叶包装理解
- 茶叶项目优先补充：货号、茶类/工艺、规格/净含量、包装形态、目标档期
- 目标用户
- 价格带
- 销售渠道
- 哪些品牌资产已固定，哪些还开放
- 尺寸、运输、陈列或法规限制
- 预算与时间线
- 合规/标签信息负责人、素材授权状态、样品验收状态
- 当前最优先的目标：货架表现、礼赠感、电商安全、成本、环保还是量产稳定性

用户或附件已经回答过的问题不要重复追问。

## 路由规则

- 如果用户在问“现在项目到哪了、确认了什么、还缺什么”，先走状态层，优先调用 `project-memory-manager`。
- 当用户只有模糊 brief、开案需求或还没进入执行阶段时，先走洞察层。
- 竞品分析、消费者理解、机会点判断、包装定位，走洞察层。
- 命名、故事、创意方向、关键词、情绪板，走概念层。
- 盒型、开合方式、刀模限制、打样验证、运输逻辑，走结构层。
- 信息层级、字体、色彩、版式、效果图、视觉语言，走视觉层。
- 视觉方向单里的图像/图形需要交给 AI 生成草案时，先走 `visual-system-builder` 拆成 `AI 概念素材任务`，再交给 `visual-direction-validator` 输出项目内概念素材包。
- 字体、图片、插画、AI 生成图、认证标志、合作方 Logo 的来源和授权状态，走视觉层并建议维护 `asset-register.md`。
- 包装视觉方向快速验证、包装插画/图形方向、提示词、主题×构图×风格组合推荐、AI 草案生成，优先调用 `visual-direction-validator`。如果来自视觉方向单或项目资产任务，应输出到 `03_Design/02_Assets/AI_Concepts/{task-id}/`；如果只是独立探索，应先输出方向验证卡和设计师参考包，只有用户明确要求出图时才生成草案。当前默认按茶叶包装视觉判断；明确非茶叶品类时先标注缺少该品类模块。
- 纸材、印刷、后道工艺、法规与环保，走材料层。
- 印前文件、校色、打样问题、合规复核、白样/彩样/大货验收、量产风险、成本优化，走印前层。
- 供应商 brief、询价、报价比较、项目推进、提案准备，走商业交付层。
- 如果一个请求同时包含 `供应商 brief`、`报价比较`、`项目推进`、`提案准备` 中两项或以上，按协作层组合任务处理：先判断已经走到哪一步，再按 `supplier-brief-writer -> quotation-comparator -> project-tracker -> proposal-builder` 的顺序给出分步建议。
- 上市后反馈、问题归因、流程修正、知识沉淀，走复盘层。
- 如果用户明确在问“把项目经验回写成共享知识库”或“把零散产出整理成可复用规则”，优先调用 `knowledge-synthesizer`。
- 如果用户明确在问“批量盘点所有项目的沉淀状态”或“更新工作区级知识汇总”，仍走复盘层，优先调用 `knowledge-synthesizer`。
- 如果用户明确在问“启动本轮知识整理会话”或“给我本轮优先处理队列”，仍走复盘层，优先调用 `knowledge-synthesizer`。
- 如果用户明确在问”自动准备本轮知识整理”或”自动更新覆盖表和收件箱”，仍走复盘层，优先调用 `knowledge-synthesizer`。
- 如果用户在问”这个设计为什么改成这样”、”帮我追溯决策”、”记录变更理由”，优先调用 `design-version-tracker`。
- 如果用户明确提出非茶叶品类，先按通用工作流判断阶段，再列出该品类缺失的专用事实；不要把茶叶标签、茶礼盒结构或茶叶供应商口径强套上去。

如果一个请求跨多个阶段，先解决当前最卡住的瓶颈，并明确写出下一个阶段该做什么。

## 路由优先级

当一个请求同时命中多个层时，按下面顺序判断：

1. 先看是否缺项目状态；如果缺，先补 `project-memory-manager`。
2. 再看是否存在阻塞性问题；如果有，先处理最阻塞的那个阶段。
3. 如果方向未定，不进入执行层。
4. 如果供应商、报价、时间线已经成为主要问题，优先转入商业交付层。
5. 如果用户直接指定一个明确环节，优先交给对应子 skill，而不是在 `packging-os` 内泛化处理。
6. 如果阶段切换返工成本高，优先判断是否应插入桥接节点，而不是直接推进到下一层。

## 桥接节点规则

- `必须插入`、`建议插入`、`可跳过` 的判定统一以 [bridge-node-rules.md](./references/bridge-node-rules.md) 为准。
- 如果桥接节点被插入，输出中必须明确：
  - 为什么现在不能直接进下一层
  - 这次桥接动作的完成标准
  - 完成后应该回到哪一个子 skill

## 商业交付层组合任务

- 当用户一次性要求“写 brief + 看报价 + 排期 + 做提案”中的多项任务时，不要让用户自己拆 skill。
- 先判断当前协作状态：
  - 还没统一询价或打样口径：先 `supplier-brief-writer`
  - 已收到两家或以上报价：再 `quotation-comparator`
  - 已进入执行推进或需要排关键路径：再 `project-tracker`
  - 已有阶段结论且准备汇报：最后 `proposal-builder`
- 输出时必须明确 `当前建议先做哪一步`、`为什么不是别的一步`、`做完后下一步接哪个协作 skill`。

## 决策规则

- 电商优先的产品，先保证运输安全和装箱效率。
- 新品牌且预算有限时，先保识别度和记忆点，不先堆装饰工艺。
- 高客单礼赠产品，优先考虑开箱节奏和结构手感。
- 当成本有压力时，先减结构复杂度，再削减品牌核心识别。
- 茶叶包装项目必须尽早确认规格/净含量、茶类/工艺、执行标准、SC、生产商、产地、贮存条件、条码、内袋食品接触和标签信息区。
- 非茶叶受监管品类必须先补齐该品类法规、阻隔性、标签和材料安全要求，再给生产敏感建议。
- 在没确认供应商能力、MOQ 和公差前，不要贸然推荐复杂工艺。
- 涉及成本、预算、报价、工艺单价、结构成本、量产可行性时，必须引用成本证据等级 [C0]-[C5]；没有 C3 及以上证据时，不得输出真实成本判断；没有 MOQ、数量区间、材质规格、工艺口径时，不得比较供应商价格。详见 [cost-evidence-standard.md](../../references/cost-evidence-standard.md)。
- 商业销售包装进入最终交付前，必须显式检查合规/标签信息、素材授权状态和样品验收状态；缺项时只能标为风险或待确认，不能默认通过。详见 [compliance-and-asset-standard.md](../../references/compliance-and-asset-standard.md) 与 [sample-acceptance-standard.md](../../references/sample-acceptance-standard.md)。

## 输出规则

- 输出必须是结构化交付物，不要只给泛泛 brainstorm。
- 区分已知事实、假设和建议。
- 只要建议会影响量产、成本或合规，就必须附风险清单。
- 涉及字体、图片、插画、AI 图、认证标志、合作方 Logo 或最终文件交付时，必须说明素材授权状态。
- 涉及打样、发厂或量产时，必须说明白样、彩样、机上样、大货首件或抽检的验收状态。
- 写出下一个评审节点或审批动作。
- 对概念、结构、材质、供应商的比较，优先用表格。
- 如果缺统一项目状态，输出中必须提示先建立或更新项目卡。
- 如果建议进入下一层，必须点名推荐下一个子 skill。
- 如果产出了结构化文档，必须同时写出默认归档目录和推荐文件名。
- 如果当前项目目录缺少目标归档位置，必须明确建议新增目录，而不是随意塞进 `Final`。
- 如果当前请求本质上已经是单一叶子任务，直接交给对应子 skill，不要重复包一层总控分析。
- 如果发现历史旧文件名，输出中要明确标注“历史命名”，新产物一律按标准名落档。

## 拆分规则

当某类任务高频且足够独立时，直接交给专门的子 skill。当前子 skill 包括：`project-memory-manager`、`brief-decomposer`、`research-analyzer`、`concept-generator`、`structure-selector`、`visual-system-builder`、`visual-direction-validator`、`material-finishing-advisor`、`supplier-brief-writer`、`quotation-comparator`、`project-tracker`、`proposal-builder`、`prepress-checker`、`project-retrospective` 和 `knowledge-synthesizer`。

推荐拆分方式：
- 项目状态整理 -> `project-memory-manager`
- 模糊需求澄清 -> `brief-decomposer`
- 研究和定位 -> `research-analyzer`
- 创意方向 -> `concept-generator`
- 结构选择 -> `structure-selector`
- 视觉规则 -> `visual-system-builder`
- 包装视觉方向验证 / 包装插画与 AI 草案 -> `visual-direction-validator`
- 材质工艺 -> `material-finishing-advisor`
- 供应商沟通 -> `supplier-brief-writer`
- 报价比较 -> `quotation-comparator`
- 时间线和责任推进 -> `project-tracker`
- 提案页序和讲解逻辑 -> `proposal-builder`
- 印前与打样问题 -> `prepress-checker`
- 复盘沉淀 -> `project-retrospective`
- 跨项目知识沉淀 -> `knowledge-synthesizer`
- 版本决策追溯 -> `design-version-tracker`

## 参考资料

阅读 [workflow-map.md](./references/workflow-map.md) 了解状态层、9 层工作流、节点路由和阶段交接规则。
阅读 [bridge-node-rules.md](./references/bridge-node-rules.md) 了解桥接节点的触发条件、顺序和跳过规则。
阅读 [output-templates.md](./references/output-templates.md) 查看常用交付物模板。
阅读 [output-routing.md](./references/output-routing.md) 查看不同 skill 的默认归档目录和命名规则。
阅读 [domain-strategy.md](../../references/domain-strategy.md) 了解通用工作流、茶叶默认垂类和未来品类模块的边界。
阅读 [cost-evidence-standard.md](../../references/cost-evidence-standard.md) 了解成本证据等级和禁止/推荐表达。
阅读 [compliance-and-asset-standard.md](../../references/compliance-and-asset-standard.md) 了解商业包装合规与素材授权检查。
阅读 [sample-acceptance-standard.md](../../references/sample-acceptance-standard.md) 了解白样、彩样和大货验收标准。
当用户需要可直接填写的文件时，优先使用对应子 skill 自己的 `assets/` 模板；只有跨阶段打样跟踪这类共享模板，才使用 [`./assets/templates/`](./assets/templates/) 下的文件。
