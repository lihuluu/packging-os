# 包装 Skills 测试样例库

维护目标：作为这套包装 skills 的长期回归样例库，供后续修改 `SKILL.md`、调整路由规则、增加新 skill、收窄边界或扩展新品类模块时复用。

更新时间：2026-05-19

## 使用说明

- 这不是 Claude Code 运行时的真实自动触发结果，而是设计级代理测试样例。
- 每次调整 skill 触发文案、总控路由或新增 skill 后，都应回看这份样例库。
- 如果某条问法的预期主 skill 发生变化，应记录变更原因，而不是直接覆盖。
- 当前默认业务域是茶叶包装设计；非茶叶品类样例用于检测“通用工作流可用，但不能强套茶叶专用规则”的边界。

## 判定规则

- `清晰命中`：问法应稳定落到一个主 skill。
- `总控接管`：问法跨多个阶段时，优先由 `packaging-os` 接手再分发。
- `边界可控`：存在次优候选，但通过当前文案和路由规则仍可判断。
- `模糊样例`：故意保留的冲突问法，用于检测系统是否需要进一步收窄边界。

## 核心样例

| ID | 用户问法 | 预期主 skill | 次优候选 | 判定 | 说明 |
| --- | --- | --- | --- | --- | --- |
| C01 | 这个包装项目该从哪一步开始做？ | `packaging-os` | `project-memory-manager` | 清晰命中 | 典型总控入口 |
| C02 | 先帮我整理一下这个项目现状，再告诉我下一步。 | `packaging-os` | `project-memory-manager` | 总控接管 | 先整理状态，再决定分流 |
| C03 | 现在是先做结构还是先做视觉？ | `packaging-os` | `structure-selector` / `visual-system-builder` | 清晰命中 | 典型路由题 |
| C04 | 帮我拆一下这个包装 brief。 | `brief-decomposer` | `project-memory-manager` | 清晰命中 | 直接需求澄清 |
| C05 | 客户只给了一句话，你帮我整理成正式需求。 | `brief-decomposer` | `packaging-os` | 清晰命中 | 模糊需求 -> brief |
| C06 | 这些会议纪要帮我提炼成能开工的包装 brief。 | `brief-decomposer` | `project-memory-manager` | 清晰命中 | 会议纪要转任务书 |
| C06B | 客户只说要做一款高端茶礼盒，其他都没定，先帮我整理 brief。 | `brief-decomposer` | `packaging-os` | 边界可控 | 应输出原始需求/可推进状态，保留待确认项，不脑补成本、MOQ、结构、供应商、验收责任人和成功指标 |
| C06C | 前期 brief 里没有 MOQ、供应商和验收负责人，要不要先补齐？ | `brief-decomposer` | `project-memory-manager` / `supplier-brief-writer` | 边界可控 | brief 只判断这些是否阻塞下一步；默认作为后续移交项，不要求开案一次性填满 |
| C07 | 帮我分析一下这几个竞品包装的共性和机会点。 | `research-analyzer` | `concept-generator` | 清晰命中 | 竞品研究明确 |
| C08 | 这个赛道的包装还有什么空白点？ | `research-analyzer` | `packaging-os` | 清晰命中 | 定位/赛道研究 |
| C09 | 这组参考图能看出什么定位机会？ | `research-analyzer` | `visual-system-builder` | 边界可控 | 若参考图被定义为竞品样本，应偏研究 |
| C10 | 给我 3 个可提案的包装概念方向。 | `concept-generator` | `visual-system-builder` | 清晰命中 | 方向生成明确 |
| C11 | 帮这个产品想几个包装创意和命名方向。 | `concept-generator` | `research-analyzer` | 清晰命中 | 概念与命名 |
| C12 | 这个产品包装故事怎么讲？ | `concept-generator` | `visual-system-builder` | 清晰命中 | 叙事导向明显 |
| C13 | 这个礼盒适合天地盖还是抽屉盒？ | `structure-selector` | `material-finishing-advisor` | 清晰命中 | 结构选择明确 |
| C14 | 这个结构适不适合电商运输？ | `structure-selector` | `prepress-checker` | 清晰命中 | 结构与物流判断 |
| C15 | 帮我比较几个盒型，再给打样建议。 | `structure-selector` | `project-tracker` | 清晰命中 | 结构 + 打样规划 |
| C16 | 这个包装正面第一眼应该看到什么？ | `visual-system-builder` | `concept-generator` | 清晰命中 | 信息层级问题 |
| C17 | 帮我把这个概念落成版式和视觉规则。 | `visual-system-builder` | `concept-generator` | 清晰命中 | 概念 -> 视觉规则 |
| C18 | 这个系列包装的 SKU 怎么统一？ | `visual-system-builder` | `concept-generator` | 清晰命中 | 系列化视觉系统 |
| C19 | 这个盒子用什么纸和工艺比较合适？ | `material-finishing-advisor` | `prepress-checker` | 清晰命中 | 材质工艺明确 |
| C20 | 我想做高级感但预算有限，工艺怎么选？ | `material-finishing-advisor` | `structure-selector` | 清晰命中 | 材质工艺取舍 |
| C21 | 这个方案在环保和成本上怎么平衡？ | `material-finishing-advisor` | `packaging-os` | 清晰命中 | 材料层判断 |
| C21B | 这个概念落到什么材质会更对？ | `material-finishing-advisor` | `visual-system-builder` | 清晰命中 | 概念到材质翻译 |
| C22 | 帮我把这套方案整理成发给工厂的打样说明。 | `supplier-brief-writer` | `project-tracker` | 清晰命中 | 供应商沟通明确 |
| C23 | 我要发给工厂询价，你帮我写需求。 | `supplier-brief-writer` | `brief-decomposer` | 清晰命中 | 询价 brief |
| C24 | 帮我列出需要供应商确认的关键问题。 | `supplier-brief-writer` | `quotation-comparator` | 清晰命中 | 沟通清单 |
| C25 | 帮我比较这三家工厂报价，看哪家更稳。 | `quotation-comparator` | `supplier-brief-writer` | 清晰命中 | 报价对比明确 |
| C26 | 这几份报价是不是一个口径？ | `quotation-comparator` | `supplier-brief-writer` | 清晰命中 | 口径校对 |
| C27 | 这个报价为什么便宜这么多？ | `quotation-comparator` | `material-finishing-advisor` | 清晰命中 | 价格陷阱识别 |
| C28 | 帮我把这个项目拆成时间线、责任人和下一步动作。 | `project-tracker` | `packaging-os` | 清晰命中 | 项目推进明确 |
| C29 | 这个包装项目现在卡在哪个节点？ | `project-tracker` | `packaging-os` | 清晰命中 | 执行节点判断 |
| C30 | 现在最该推进哪一步？ | `project-tracker` | `packaging-os` | 边界可控 | 若强调执行推进，偏 tracker |
| C31 | 帮我整理一下这个包装项目当前状态。 | `project-memory-manager` | `packaging-os` | 清晰命中 | 项目卡维护 |
| C32 | 把这些零散信息整理成一个项目总卡。 | `project-memory-manager` | `packaging-os` | 清晰命中 | 状态汇总 |
| C33 | 这个项目现在已经确认了哪些事？ | `project-memory-manager` | `packaging-os` | 清晰命中 | 已确认事项汇总 |
| C34 | 这个包装 PDF 现在可以发厂了吗？ | `prepress-checker` | `supplier-brief-writer` | 清晰命中 | 印前判断明确 |
| C35 | 打样出来有色差和爆线，帮我分析一下原因。 | `prepress-checker` | `material-finishing-advisor` | 清晰命中 | 打样问题诊断 |
| C36 | 帮我审核这个包装文件有没有量产风险。 | `prepress-checker` | `packaging-os` | 清晰命中 | 印前风险检查 |
| C36B | 这个方向要不要先做概念测试？ | `packaging-os` | `concept-generator` | 边界可控 | 属于概念层后的桥接判断，应由总控决定是否插入验证节点 |
| C36C | 这个礼盒概念已经定了，能不能直接进材质方案？ | `packaging-os` | `material-finishing-advisor` | 边界可控 | 应先判断是否需要桥接节点，再决定能否直接进入材料层 |
| C36D | 这个项目已经做到白样了，这几个桥接节点哪些还要补，哪些已经被现有文档覆盖了？ | `packaging-os` | `project-memory-manager` | 边界可控 | 进行中项目的桥接复核，应支持 `待插入 / 已覆盖 / 可跳过` 判断 |
| C37 | 帮我复盘一下这个包装项目。 | `project-retrospective` | `project-memory-manager` | 清晰命中 | 复盘明确 |
| C38 | 这次包装上市后反馈一般，帮我总结问题和原因。 | `project-retrospective` | `project-memory-manager` | 清晰命中 | 上市后复盘 |
| C39 | 帮我把这次经验整理成 SOP 更新项。 | `project-retrospective` | `packaging-os` | 清晰命中 | 经验沉淀 |
| C40 | 把这个项目的工作产出沉淀成知识库。 | `knowledge-synthesizer` | `project-retrospective` | 清晰命中 | 项目级知识回写 |
| C41 | 帮我总结这些项目里重复出现的经验，整理成共享规则。 | `knowledge-synthesizer` | `packaging-os` | 清晰命中 | 跨项目知识整理 |
| C42 | 更新共享知识库，把这次复盘里的结论补进去。 | `knowledge-synthesizer` | `project-retrospective` | 清晰命中 | 复盘后回写系统知识 |
| C43 | 盘点所有项目的知识沉淀覆盖率，并更新工作区知识汇总。 | `knowledge-synthesizer` | `packaging-os` | 清晰命中 | 批量知识整理 |
| C44 | 生成本轮知识整理会话包，并给我按优先级开始处理。 | `knowledge-synthesizer` | `packaging-os` | 清晰命中 | 固定执行会话入口 |
| C45 | 启动本轮知识整理会话，并自动更新覆盖表、收件箱和日志草稿。 | `knowledge-synthesizer` | `packaging-os` | 清晰命中 | 一键启动入口 |
| C46 | 帮我整理这个包装提案逻辑，按汇报页序写出来。 | `proposal-builder` | `packaging-os` | 清晰命中 | 提案页序整理 |
| C47 | 这套包装方案怎么讲给客户听更顺？ | `proposal-builder` | `concept-generator` | 清晰命中 | 提案讲解备注 |
| C48 | 我需要先发供应商询价，再比较报价并排一下项目推进顺序。 | `packaging-os` | `supplier-brief-writer` / `quotation-comparator` / `project-tracker` | 总控接管 | 协作层组合任务应由总控排顺序 |
| C49 | 帮我把工厂 brief、报价判断和提案逻辑一起梳理一下。 | `packaging-os` | `supplier-brief-writer` / `quotation-comparator` / `proposal-builder` | 总控接管 | 多个协作子任务同时命中 |
| C50 | 我刚改了几个 skill，帮我检查这套 Claude Code 系统有没有漂。 | `packaging-os-maintainer` | `packaging-os` | 清晰命中 | 系统治理巡检 |
| C51 | 我新增了一个 skill，顺手把 README、路由和测试补齐。 | `packaging-os-maintainer` | `packaging-os` | 清晰命中 | 新增 skill 后的补同步 |
| C52 | 跑一遍 Packaging OS 验证，并告诉我还缺什么。 | `packaging-os-maintainer` | `packaging-os` | 清晰命中 | 验证脚本与治理汇总 |
| C53 | 帮我检查哪些项目的项目卡已经落后于最新产出。 | `project-memory-manager` | `packaging-os-maintainer` | 清晰命中 | 项目状态漂移诊断 |
| C53B | 最近哪些项目动过？ | `packaging-os` | `project-memory-manager` | 总控接管 | 按 `Workspace/Projects/` 目录修改时间排序，读各项目 `project-memory-card.md` |
| C53C | 继续推进猴王五年陈茯茶，先帮我看现在到哪了。 | `packaging-os` | `project-memory-manager` | 总控接管 | 应先读工作区总览和单项目项目卡，再决定下一步 skill |
| C54 | 帮我把新包装项目目录模板接进系统，并补一个初始化脚本。 | `packaging-os-maintainer` | `packaging-os` | 清晰命中 | 属于系统治理，不是单个包装项目分析 |
| C55 | 帮这个有机绿茶做一张包装插画。 | `visual-direction-validator` | `visual-system-builder` | 清晰命中 | 先输出方向验证和设计师参考包；只有用户明确要出图时才生成 AI 草案 |
| C56 | 这款精酿啤酒的包装插画应该用什么风格？ | `packaging-os` | `visual-direction-validator` | 边界可控 | 非默认垂类，应先标注缺少啤酒品类模块，再决定是否用通用视觉验证框架 |
| C57 | 给我一个适合这款茶礼盒包装的插画提示词。 | `visual-direction-validator` | `concept-generator` | 清晰命中 | 明确需要提示词，且命中默认茶叶垂类；提示词前应先说明验证假设 |
| C58 | 这个包装该用植物插画还是产品插画？ | `visual-direction-validator` | `visual-system-builder` | 清晰命中 | 主题选择属于视觉方向验证入口 |
| C59 | 帮我记一下这次变更的理由。 | `design-version-tracker` | `project-memory-manager` | 清晰命中 | 决策日志追加 |
| C60 | 这个设计为什么改成这样？ | `design-version-tracker` | `project-memory-manager` | 清晰命中 | 决策追溯 |
| C61 | 这个工艺为什么从烫金改成UV？ | `design-version-tracker` | `material-finishing-advisor` | 清晰命中 | 工艺决策追溯 |
| C62 | 记录一下客户这次的反馈和对应的修改。 | `design-version-tracker` | `project-memory-manager` | 清晰命中 | 客户反馈驱动决策记录 |
| C66 | 这个项目还没到供应商阶段，但结构可能很贵，要不要先问工厂？ | `packaging-os` → `supplier-brief-writer`（粗可行性确认模式） | `structure-selector` / `packaging-os` | 边界可控 | 横向商业检查点允许在结构层提前触发供应商可行性确认；系统不应因"还没到第 7 层"而推迟协作判断 |
| C67 | 概念方向很好，但依赖特种纸和压凸，能不能直接做视觉？ | `concept-generator` + 提示桥接：概念到材质翻译 / 供应商可行性确认 | `visual-system-builder` / `material-finishing-advisor` | 边界可控 | 概念层商业检查点要求标注供应链依赖；不能跳过验证直接进视觉层 |
| C68 | 中秋档期很紧，现在先做视觉还是先排供应商时间？ | `project-tracker` | `packaging-os` / `supplier-brief-writer` | 清晰命中 | 档期硬截止为最高优先级风险；应建议先排关键路径确认供应商交期，再做视觉 |
| C69 | 协作层是不是第 7 步才用？ | `packaging-os` | — | 清晰命中 | 系统应解释"商业交付层"新定位；横向商业检查点意味着每层都有商业检查 |
| C70 | 客户还没确认 MOQ，可以发正式报价吗？ | `supplier-brief-writer`（粗可行性确认模式） | `packaging-os` / `quotation-comparator` | 边界可控 | 系统应建议先发粗可行性确认 brief 而非正式询价；MOQ 未确认时正式报价可能无效 |
| C71 | "我只看了小罐茶的官网，其他竞品还没来得及看，先帮我做定位分析" | `research-analyzer` | `packaging-os` / `brief-decomposer` | 边界可控 | 竞品 < 3，应输出快速假设版，所有结论标 [E1]，尾部标注"建议补充竞品样本" |
| C72 | "我有 5 个竞品实物 + 2 个电商截图 + 1 份渠道走访笔记" | `research-analyzer` | — | 清晰命中 | 应输出证据支撑版；实物标 [E4]，截图标 [E2]，走访标 [E3]；附竞品样本矩阵 |
| C73 | "观夏算竞品吗？它是做香氛的" | `research-analyzer` | `concept-generator` | 边界可控 | 应分类为"审美参考 + 跨品类借鉴"，不归入"直接竞品"；可分析其设计方法论但不应作为定位依据 |
| C74 | 快速假设版研究直接进入概念层 | `concept-generator` | `packaging-os` / `research-analyzer` | 边界可控 | concept-generator 应触发接收检查警告"研究证据不足"；概念方向限制为 2 个 + 标注"基于 E1 假设" |
| C75 | 山隐项目定位回顾（回归测试） | `research-analyzer` | `concept-generator` | 边界可控 | 小罐茶/tea'stone/观夏/精品咖啡应按样本分类 + 证据等级重新标注；观夏改为审美参考；开箱体验降级为 [E1]；人群偏好标为待验证假设；风味标签标注跨品类借鉴 [E1] |
| C76 | "这个方案大概多少钱？" | `packaging-os` / 当前所在 skill | `supplier-brief-writer` | 边界可控 | 不报价；要求成本依据；只能输出成本风险和询价清单 [C0] |
| C77 | "留白是不是更省钱？" | `research-analyzer` / `material-finishing-advisor` | — | 边界可控 | 必须标为 [C0] 推断；改为"留白可能降低印刷复杂度，但真实成本仍取决于纸材、结构、工艺、MOQ 和供应商报价" |
| C78 | "30 元/盒能不能做高端？" | `packaging-os` | `material-finishing-advisor` / `supplier-brief-writer` | 边界可控 | 标为 [C1] 预算压力判断；只能判断是否存在预算压力，不能判断真实成本 |
| C79 | "抽屉盒是不是比天地盖贵？" | `structure-selector` | — | 边界可控 | 只能判断复杂度差异（装配人工/材料用量/刀模），不能判断真实单价；标为 [C0] |
| C80 | "没有 MOQ 能不能估成本？" | `packaging-os` / `material-finishing-advisor` | `brief-decomposer` | 边界可控 | MOQ 是成本阻塞项；没有 MOQ 不能估成本，只能列出成本变量和待确认项 |
| C81 | "这家便宜很多能不能选？" | `quotation-comparator` | `supplier-brief-writer` | 边界可控 | 先检查税/运/打样/刀模/版费/损耗/外协/工艺缺项；没有同口径时必须输出"当前报价不可直接比较" |
| C82 | "客户只有预算，没有供应商报价" | `packaging-os` | `supplier-brief-writer`（粗可行性确认） | 清晰命中 | 只能输出成本风险和询价清单；标为 [C1]；建议先发粗可行性确认 |
| C83 | "视觉方向单里的正面和背面信息层级不准确，会影响后续设计稿，怎么改？" | `visual-system-builder` | `proposal-builder` / `prepress-checker` | 清晰命中 | 应先补商业沟通目标、包装面任务分配、阅读顺序和低保真结构，再调整视觉规则 |
| C84 | "这份视觉方向单太长了，客户看起来会烦，能不能优化成主文档加附录？" | `visual-system-builder` | `proposal-builder` | 清晰命中 | 视觉方向单应主文档短、执行细节进附录；不是提案页序问题 |
| C85 | "视觉方向已经定了，还需要加情绪板节点吗？" | `visual-system-builder` | `concept-generator` | 边界可控 | 方向已定时不新增独立情绪板节点；可保留轻量视觉锚点或参考基准 |
| C86 | "这套包装用了网上找的山水图，可以直接进终稿吗？" | `visual-system-builder` | `prepress-checker` | 边界可控 | 必须检查素材来源和商用授权；权利不明只能标为仅参考/不可用，不能进入 `04_Final` |
| C87 | "这个茶叶包装背标信息还没让品控看，可以发厂吗？" | `prepress-checker` | `packaging-os` | 清晰命中 | 标签/法规信息未复核应列为阻塞项，不能标记 ready to release |
| C88 | "AI 生成的包装插画能不能直接商用？" | `visual-system-builder` | `visual-direction-validator` | 边界可控 | 应要求记录生成工具、提示词、企业内部使用规则和授权状态，不直接默认可商用 |
| C89 | "白样结构还没验收，能不能先做大货？" | `prepress-checker` | `project-tracker` | 清晰命中 | 白样未通过或未验收，不应进入大货；输出样品验收状态和下一步动作 |
| C90 | "彩样颜色和签样不一致，但供应商说大货会好，可以过吗？" | `prepress-checker` | `supplier-brief-writer` | 边界可控 | 应按彩样/合同样验收记录处理；不能只凭口头承诺放行 |
| C91 | "帮我写打样 brief，顺便把白样和彩样验收标准写进去。" | `supplier-brief-writer` | `prepress-checker` | 清晰命中 | 供应商 brief 必须包含白样、彩样/合同样和大货首件/抽检验收重点 |
| C92 | "视觉方向单里的图像和图形这部分交给 AI 做，怎么落地？" | `visual-system-builder` | `visual-direction-validator` | 清晰命中 | 应先拆成 AI 概念素材任务，再交给 visual-direction-validator 生成项目内草案资产，不直接进入 Final |
| C93 | "根据这份视觉方向单生成 3 版主视觉和底纹草案。" | `visual-direction-validator` | `visual-system-builder` | 边界可控 | 若方向单已明确任务，可直接进入项目集成模式，输出到 `03_Design/02_Assets/AI_Concepts/{task-id}/` 并提示更新 asset-register |
| C94 | "我要给铝箔袋供应商写 brief，这个袋子的印刷→复合→成型工序比较多，我担心对位出问题。" | `supplier-brief-writer` | `prepress-checker` | 清晰命中 | 多工序软包装必须量化各工序公差（印刷套准、复合偏移、成型收缩），要求供应商提供累计上限，写入验收标准 |
## 边界样例

这些样例不是错误，而是用来长期监测 skill 边界是否开始漂移。

| ID | 用户问法 | 当前预期 | 冲突 skill | 备注 |
| --- | --- | --- | --- | --- |
| B01 | 这个包装应该长什么样？ | `concept-generator` 或 `visual-system-builder` | 两者互相冲突 | 要看用户是在问方向，还是在问版式落地 |
| B02 | 这个项目现在卡在哪？ | `packaging-os` 或 `project-tracker` | 两者互相冲突 | 若问整体瓶颈偏总控，若问执行节点偏 tracker |
| B03 | 帮我把 brief 转成包装方向。 | `concept-generator` | `research-analyzer` | 若定位未清，可能应先做研究 |
| B04 | 这些参考图能看出什么？ | `research-analyzer` | `visual-system-builder` | 要看参考图是竞品图还是风格图 |
| B05 | 我要发供应商询价，但需求还不够清楚。 | `packaging-os` | `supplier-brief-writer` / `brief-decomposer` | 总控应先补需求，再进入供应商沟通 |
| B06 | 帮我做一个提案，是该走 `proposal-builder` 还是 `project-tracker`？ | `proposal-builder` | `project-tracker` | 如果重点是页序和讲法，应稳定落到 `proposal-builder` |
| B07 | 帮我记录一下这个项目接下来要做什么。 | `project-tracker` 或 `project-memory-manager` | `design-version-tracker` | "接下来要做什么"是推进/状态维护，不是决策追溯；版本追踪只记录"为什么改了" |
| B08 | 这个包装项目当前版本是什么状态？ | `project-memory-manager` | `design-version-tracker` | 若问项目整体状态偏项目卡，若问版本冻结状态偏版本追踪 |
| B09 | 我接了一个咖啡包装项目，能不能也用这套系统？ | `packaging-os` | `brief-decomposer` / `research-analyzer` | 应使用通用工作流，但提示当前缺少咖啡品类模块，不应套用茶叶标签和茶礼盒规则 |

## 治理层回归样例

| ID | 检查点 | 预期结果 | 说明 |
| --- | --- | --- | --- |
| G01 | `CLAUDE.md` 是否引用不存在的治理文件 | 不应引用不存在文件 | 避免 Claude Code 遇到无法满足的上位规则 |
| G02 | README、`packaging-os`、`workflow-map.md` 的工作流层数是否一致 | 统一为 9 层 | 防止总纲与 skill 路由冲突 |
| G03 | README 技能表与 `.claude/skills/` 实际目录是否一致 | 应一致 | 防止新增 skill 后文档失真 |
| G04 | `packaging-os` 是否覆盖所有叶子 skill | 应覆盖 | 防止出现空路由 |
| G05 | `knowledge-synthesizer` 是否明确不替代 `project-retrospective` | 应明确 | 防止知识沉淀吞掉项目复盘 |
| G06 | 项目卡、复盘、知识沉淀是否统一使用共享字段词表 | 应统一 | 防止公共字段继续同义漂移 |
| G07 | 修改系统文件时，是否优先路由到 `packaging-os-maintainer` | 应优先路由 | 防止系统治理任务误落到业务 skill |
| G08 | 项目初始化脚本、README 和 `Workspace/Projects/README.md` 的目录结构是否一致 | 应一致 | 防止项目目录规范再次分裂 |
| G09 | 治理校验脚本是否能发现 `.DS_Store` 和 `*.tmp.*` | 应能发现 | 防止临时文件重新进入仓库 |
| G10 | 项目目录里是否还残留废弃文件名或旧路径引用 | 不应残留 | 防止 `project_tracker.md`、`structure-selection.md`、`03_Design/02_Structure/` 回流 |
| G11 | 开案必查项是否在项目卡模板、输出模板和项目卡框架里一致 | 应一致 | 防止开案约束只写在单一文件里 |
| G12 | 概念到材质翻译是否在材料层 framework、asset 和 workflow-map 中同时出现 | 应一致 | 防止桥接节点只存在于复盘结论里 |
| G13 | 桥接节点是否有“必须 / 建议 / 可跳过”的触发条件表 | 应明确 | 防止总控知道要桥接，但不知道何时必须插入 |
| G14 | 叶子 skill 是否显式引用统一的桥接节点规则文件 | 应明确 | 防止桥接逻辑只停在总控层，不下沉到执行 skill |
| G15 | 对进行中的真实项目复核桥接节点时，是否支持 `待插入 / 已覆盖 / 可跳过` 执行状态 | 应支持 | 防止既有项目被迫重复执行已被现有产物覆盖的桥接动作 |
| G16 | 日常治理入口是否同时覆盖系统校验、项目临时文件 dry-run 和项目卡漂移检查 | 应覆盖 | 防止治理命令重新分散成多个入口 |
| G18 | decision-log 模板是否包含共享字段 | 应包含 | 防止版本管理文档脱离共享字段体系 |
| G20 | 工作区项目驾驶舱是否按最近活跃排序，并排除临时文件和生成文件 | 应支持 | 防止 dashboard 被临时文件污染 |
| G20A | 决策日志"追加 only"是否仅限 `## 决策记录` 表行，共享字段块允许更新 | 应明确 | 防止"追加 only"与共享字段更新自相矛盾 |
| G21 | `file-naming-standard.md` 是否位于共享 references 目录 | 应位于 `.claude/references/` | 防止跨 skill 公共规范锁定在单一 skill 内部 |
| G23 | `decision-log.md` 决策序号是否统一使用 `D-NNN` | 应统一 | 防止快照冻结项无法稳定引用决策 |
| G25 | `CLAUDE.md`、README、`packaging-os` 和测试样例是否一致表达“通用工作室骨架 + 茶叶默认垂类 + 未来品类模块” | 应一致 | 防止系统被改死成茶叶专用，或重新漂回无边界泛包装 |
| G26 | 合规与素材授权标准是否被 `visual-system-builder`、`prepress-checker`、`packaging-os` 和 README 同步引用 | 应一致 | 防止授权机制只停留在共享文档，业务 skill 不触发 |
| G27 | 样品与大货验收标准是否被 `supplier-brief-writer`、`prepress-checker`、`project-tracker` 和项目卡模板同步引用 | 应一致 | 防止验收标准只在发厂后才出现 |
| G28 | 新项目初始化是否生成 `asset-register.md`、`compliance-review.md` 和 `sample-acceptance-record.md` | 应生成 | 防止新项目缺少合规/授权/验收机制入口 |
| G29 | `brief-decomposer` 是否只生成最低可推进 brief，不把 MOQ、供应商、合规负责人、素材授权和样品验收强塞为开案必填 | 应明确 | 防止 brief 重新膨胀成理想化生产任务书 |
| G30 | AI 概念素材是否归档到 `03_Design/02_Assets/AI_Concepts/{task-id}/` 并登记为草案状态 | 应明确 | 防止 AI 图像/图形草案被误放入 `04_Final` 或被默认视为可生产资产 |

## 回归检查点

每次修改 skills 后，优先检查这些项目：

1. `packaging-os` 是否仍然优先接管跨阶段问题。
2. `project-memory-manager` 是否只处理项目状态，不吞掉总控路由。
3. `project-tracker` 是否聚焦执行节点，而不是泛化成项目总控。
4. `concept-generator` 和 `visual-system-builder` 的边界是否仍然清楚。
5. `quotation-comparator` 是否只在“已有多家报价”前提下触发。
6. `supplier-brief-writer` 是否只处理供应商沟通，不提前吞掉需求澄清。
7. `knowledge-synthesizer` 是否只处理知识沉淀，不吞掉项目级复盘。
8. `knowledge-synthesizer` 在批量模式下是否先做覆盖盘点，再做知识抽取。
9. `knowledge-synthesizer` 是否能把批量整理收敛到固定会话包和历史日志。
10. `knowledge-synthesizer` 是否能把会话准备阶段自动化，但不越权替代知识判断。
11. `proposal-builder` 是否只处理提案页序和讲法，不吞掉概念生成或项目排期。
12. `.claude/skills/packaging-os-maintainer/scripts/validate-packaging-os.py 是否能发现缺失 skill、失效引用和 README 技能表漂移。
13. 项目卡、复盘、知识沉淀三类模板是否统一使用 `项目摘要 / 来源文档 / 已知事实 / 关键假设 / 风险 / 开放问题 / 结论沉淀 / 下一步动作` 这套公共词表。
14. 修改 `.claude/skills/`、`README.md`、`CLAUDE.md` 或共享模板时，是否会优先进入 `packaging-os-maintainer` 并运行治理检查。
15. 治理校验脚本是否能发现 `.DS_Store`、`*.tmp.*` 等系统或临时文件。
16. 项目目录中是否还残留 `project_tracker.md`、`structure-selection.md` 或 `03_Design/02_Structure/` 这类废弃命名与旧路径。
17. `daily-governance-check` 是否仍能串起系统校验、项目临时文件 dry-run 和项目卡漂移检查。
18. AI 概念素材任务是否保持 `visual-system-builder` 负责编排、`visual-direction-validator` 负责验证方向和生成草案、`asset-register.md` 负责授权状态沉淀。

## 追加模板

后续新增样例时，按下面格式追加：

| ID | 用户问法 | 预期主 skill | 次优候选 | 判定 | 说明 |
| --- | --- | --- | --- | --- | --- |
| N01 |  |  |  |  |  |

## 维护建议

- 不要只追加“清晰样例”，要保留一定数量的边界样例。
- 如果某条样例从 `清晰命中` 退化为 `边界可控`，应优先检查对应 skill 的 `description` 和典型触发句。
- 如果新增 skill，应先补 3 到 5 条核心样例，再补 1 到 2 条边界样例。
