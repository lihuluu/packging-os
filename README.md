# Packging OS — 包装设计工作室工作流系统

> 一套面向独立包装设计工作室的全流程系统，基于 Claude Skills 构建，覆盖从需求到量产，以及复盘后的知识沉淀。
> `README.md` 面向人读，负责说明系统怎么用；`CLAUDE.md` 是当前唯一的 Claude 执行总纲，负责约束行为和输出。

当前默认业务域是**茶叶包装设计**：茶叶 SKU、茶礼盒、茶叶标签、打样、供应商、报价、印前、版本追踪和项目复盘。系统底层保留通用包装工作流，未来扩展其他品类时，应新增品类模块，而不是推翻现有 9 层骨架。

品类策略详见 `.claude/references/domain-strategy.md`。

---

## 快速开始

如果你是第一次进入这个仓库，先看本文档理解系统结构和使用方式；如果你是在配置 Claude 的执行行为，看 `CLAUDE.md`。

### 推荐入口：项目总览

如果你是回来继续推进工作，按 `Workspace/Projects/` 下各项目目录的修改时间排序，依次阅读各项目的 `00_Project_Control/project-memory-card.md`（项目事实来源）和 `00_Project_Control/project-tracker.md`（项目推进表）。

项目事实仍以各项目的 `00_Project_Control/project-memory-card.md` 为准；推进表负责跟踪执行状态。

### 方式一：从总控进入（推荐）

如果你不确定从哪一步开始，直接说：

```
"帮我梳理一下这个茉莉花茶礼盒项目"
"这个茶叶 SKU 该从哪一步开始做？"
"现在是先做茶礼盒结构还是先做视觉？"
```

系统会自动判断项目阶段并给出建议。

### 方式二：直接进入具体阶段

如果你已经明确需求：

| 你的需求             | 对应指令                                                   |
| -------------------- | ---------------------------------------------------------- |
| 整理混乱的需求       | "拆解这个茶叶包装 brief"                                   |
| 分析竞品             | "分析这组茶礼盒竞品的包装机会"                             |
| 获取创意方向         | "给我 3 个茶叶包装概念方向"                                |
| 选择盒型             | "这个茶礼盒适合天地盖还是抽屉盒？"                         |
| 定义视觉系统         | "创建这个茶叶系列包装视觉系统"                             |
| 快速验证包装视觉方向 | "这个包装方向先帮我快速验证" / "给我茶叶包装插画提示词"   |
| 选择材质工艺         | "推荐这款茶礼盒的纸材和工艺"                               |
| 检查文件             | "检查这个茶叶包装文件能否量产"                             |
| 发给工厂             | "写一份茶叶包装供应商 brief"                               |
| 对比报价             | "对比这几家茶礼盒供应商报价"                               |
| 项目排期             | "制定这个茶叶包装项目推进时间线"                           |
| 整理提案逻辑         | "帮我整理这个茶叶包装提案逻辑"                             |
| 更新状态             | "更新项目状态"                                             |
| 项目复盘             | "复盘这个项目"                                             |
| 沉淀知识             | "把这个项目的工作产出沉淀成知识库"                         |
| 批量整理知识         | "盘点所有项目的知识沉淀覆盖率，并更新工作区知识汇总"       |
| 启动一次知识整理会话 | "生成本轮知识整理会话包，并给我按优先级开始处理"           |
| 一键启动知识整理     | "启动本轮知识整理会话，并自动更新覆盖表、收件箱和日志草稿" |

### 方式三：维护这套 Claude Code 系统

如果你是在迭代 Packging OS 本身，而不是在推进某个包装项目，直接说：

```
"我刚改了几个 skill，帮我检查这套 Claude Code 系统有没有漂"
"我新增了一个 skill，顺手把 README、路由和测试补齐"
"跑一遍 Packging OS 验证，并告诉我还缺什么"
"帮我检查哪些项目的项目卡已经落后于最新产出"
"清理 Workspace/Projects 里的临时文件"
"清理 Workspace/Knowledge 里的临时文件"
```

这类请求应优先使用 `packging-os-maintainer`，先做治理巡检，再做必要同步。

常用治理脚本入口：

- 项目卡状态漂移检查：`.claude/skills/project-memory-manager/scripts/check-memory-drift.py`
- 项目目录临时文件清理（Windows）：`.claude/skills/project-memory-manager/scripts/cleanup-project-temp-files.cmd`
- 项目目录临时文件清理（Mac/Linux）：`.claude/skills/project-memory-manager/scripts/cleanup-project-temp-files.sh`
- 知识库临时文件清理：`.claude/skills/knowledge-synthesizer/scripts/cleanup-temp-files.sh`

### 常用维护命令

如果你已经在仓库根目录，可以直接运行：

```bash
# 1) 跑一遍系统治理校验
# Windows 原生入口（不依赖系统 Python）
.claude\skills\packging-os-maintainer\scripts\validate-packging-os.cmd

# Mac / Linux 入口（自动选择 python3、python 或 pwsh）
sh .claude/skills/packging-os-maintainer/scripts/validate-packging-os.sh

（项目级 dashboard 已退役，直接用 project-memory-card.md + project-tracker.md）

# 1.5) 预览项目目录临时文件（默认不删除）
.claude\skills\project-memory-manager\scripts\cleanup-project-temp-files.cmd
sh .claude/skills/project-memory-manager/scripts/cleanup-project-temp-files.sh

# 2) 检查哪些项目的项目卡已经落后
python3 .claude/skills/project-memory-manager/scripts/check-memory-drift.py --all

# 3) 清理知识库临时文件
sh .claude/skills/knowledge-synthesizer/scripts/cleanup-temp-files.sh
```

推荐把这些命令理解成 Claude Code 的治理入口：

- 想检查系统有没有漂：Windows 运行 `validate-packging-os.cmd`，Mac/Linux 运行 `validate-packging-os.sh`
- 想看项目状态有没有落后：运行 `check-memory-drift.py`
- 想清理工作区噪音：先运行项目清理脚本 dry-run 看清单，再决定是否执行删除
- 想让 Claude Code 代你做这些动作：直接说“跑一遍治理检查”、“检查项目卡漂移”或“清理临时文件”

---

## 系统架构

Packging OS 使用 **9 层工作流**，每层有明确的输入、输出和交付标准：

```
┌─────────────────────────────────────────────────────────────┐
│                           9层工作流                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  0. 状态层 ───────── 项目记忆：现在在哪？                      │
│       ↓                                                      │
│  1. 洞察层 ───────── 拆解需求 + 证据化研究（快速假设版/证据支撑版） │
│       ↓                                                      │
│  2. 概念层 ───────── 生成创意概念方向                          │
│       ↓                                                      │
│  3. 结构层 ───────── 选择盒型结构                              │
│       ↓                                                      │
│  4. 视觉层 ───────── 定义视觉系统 + AI 概念素材草案              │
│       ↓                                                      │
│  5. 材料层 ───────── 材质与工艺方案                            │
│       ↓                                                      │
│  6. 印前层 ───────── 印前检查                                  │
│       ↓                                                      │
│  7. 商业交付层 ───── 供应商 brief + 报价 + 排期 + 提案 + 审批   │
│       ↓                                                      │
│  8. 复盘层 ───────── 项目复盘与经验沉淀                        │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 启动新项目

### 第一步：创建项目目录

推荐直接运行初始化脚本：

```bash
python3 .claude/skills/packging-os-maintainer/scripts/init-project.py "项目名称"
```

脚本会创建标准顶层目录，同时在 `03_Design/` 保留你更贴近真实执行的工作分层。
当前版本还会一并生成“项目启动模板包”，默认写入：

- `00_Project_Control/project-memory-card.md`
- `03_Design/01_Working/project-tracker.md`
- `03_Design/02_Assets/asset-register.md`
- `03_Design/02_Assets/AI_Concepts/`（AI 概念素材草案，不直接进入 Final）
- `03_Design/04_Production/supplier-brief.md`
- `03_Design/06_Proof_Record/compliance-review.md`
- `03_Design/06_Proof_Record/sample-acceptance-record.md`
- `01_Brief/brief-decomposition.md`
- `01_Brief/packaging-brief.md`

如需手动创建，目录建议如下：

```bash
mkdir -p "Workspace/Projects/项目名称"/{00_Project_Control,01_Brief,02_Research,03_Design/{01_Working,02_Assets/AI_Concepts,03_Presentation,04_Production,05_Renders,06_Proof_Record},04_Final/{01_Print_Files,02_Source_Files,03_Assets,04_Previews,05_Dielines},05_Retrospective}
```

### 第二步：启动项目

告诉 Claude：

```
"帮我启动一个新项目：
- 货号 / 产品名称：xxx
- 茶类 / 工艺：xxx
- 规格 / 净含量：xxx
- 包装形态：xxx
- 价格带：xxx
- 目标用户：xxx
- 销售渠道：xxx
- 目标档期：xxx"
```

系统会自动：

1. 创建项目总卡
2. 判断项目阶段
3. 生成下一步动作

---

## 项目目录结构

```
项目名称/
├── 00_Project_Control/          ← 项目控制文档
│   └── project-memory-card.md   ← 项目总卡（必须）
├── 01_Brief/                    ← 需求文档
│   ├── brief-decomposition.md
│   └── packaging-brief.md
├── 02_Research/                 ← 研究分析
│   └── positioning-summary.md
├── 03_Design/                   ← 设计工作区
│   ├── 01_Working/              ← 过程稿、版本迭代、设计日志
│   │   └── project-tracker.md   ← 项目推进表
│   ├── 02_Assets/               ← 字体、插画、图片、图标、样机源素材
│   │   └── asset-register.md    ← 素材来源与授权状态登记
│   ├── 03_Presentation/         ← 提案文档
│   │   ├── concept-directions.md
│   │   ├── proposal-outline.md
│   │   └── visual-direction.md
│   ├── 04_Production/           ← 生产文档
│   │   ├── supplier-brief.md
│   │   ├── quotation-comparison.md
│   │   ├── structure-decision.md
│   │   └── material-finishing-plan.md
│   ├── 05_Renders/              ← 效果图与预览图工作文件
│   └── 06_Proof_Record/         ← 打样记录
│       ├── prepress-review.md
│       ├── compliance-review.md
│       └── sample-acceptance-record.md
├── 04_Final/                    ← 最终交付物（只放终版）
│   ├── 01_Print_Files/          ← 印刷终稿
│   ├── 02_Source_Files/         ← 可交付源文件
│   ├── 03_Assets/               ← 最终交付素材
│   ├── 04_Previews/             ← 最终预览图
│   └── 05_Dielines/             ← 刀模线终稿
└── 05_Retrospective/            ← 项目复盘
    ├── project-retrospective.md
    └── knowledge-synthesis.md
```

### 命名约定

为了让 Claude Code 的路由、归档和校验稳定工作，仓库内统一采用下面这套命名规则：

- skill 目录名和 skill id 使用 `kebab-case`
- 项目文档、知识文档、模板产物文件名使用 `kebab-case`
- 项目目录名可保留中文、品牌名或日期前缀，但单个文档文件名不要混用下划线和连字符

当前固定文件名如下：

```text
project-memory-card.md
project-tracker.md
supplier-brief.md
quotation-comparison.md
packaging-brief.md
brief-decomposition.md
positioning-summary.md
concept-directions.md
visual-direction.md
structure-decision.md
material-finishing-plan.md
prepress-review.md
proposal-outline.md
asset-register.md
compliance-review.md
sample-acceptance-record.md
proofing-record.md
project-retrospective.md
knowledge-synthesis.md
```

废弃命名：

- `project_tracker.md`
- `structure-selection.md`

这是一套“顶层标准化 + 执行层顺手”的混合模板：

- 顶层目录固定，方便路由、脚本检查和跨项目治理
- `03_Design/` 沿用真实设计执行逻辑，减少你切目录的摩擦
- `04_Final/` 再细分交付类型，降低误放过程文件或串项目文件的风险

共享知识库位于 `Workspace/Knowledge/`。
其中：

- `Workspace/Knowledge/Library/` 放给你读的结构化知识页
- `Workspace/Knowledge/Operations/` 放给 Claude Code 和脚本维护的运行文件
  第二版还加入了工作区级文件：覆盖表、待处理收件箱和知识汇总。
  第三版补了固定执行会话：当前会话包和历史日志。
  第四版补了一键启动脚本：会话准备阶段的重复文书由脚本先做。

---

## Skill 目录约定

`.claude/skills/` 只放 skill 目录，不再把 Claude 专用脚本散放在仓库根目录。

跨 skill 共用的校验或治理脚本，优先放在最贴近职责的治理 skill 的 `scripts/` 下，并由对应 skill 维护引用。

每个 skill 推荐使用下面的结构：

```text
.claude/skills/skill-name/
├── SKILL.md
├── references/
├── assets/
└── scripts/
```

- `SKILL.md`：触发说明、使用流程、输入输出规则
- `references/`：只在需要时加载的框架、规则、参考资料
- `assets/`：模板、表单、可复用输出文件
- `scripts/`：只服务这个 skill 的自动化脚本

放置规则：

- 只被单个 skill 使用的脚本，放进该 skill 的 `scripts/`
- 被多个 skill 共用的脚本，才考虑放公共层
- 更新脚本位置后，必须同步更新对应 `SKILL.md` 和系统文档中的路径引用

---

## 完整技能列表

| 技能                             | 功能         | 典型场景                                         |
| -------------------------------- | ------------ | ------------------------------------------------ |
| `packging-os`              | 系统总控     | 不确定从哪开始时                                 |
| `packging-os-maintainer`   | 系统治理     | 修改 skill、路由、模板或治理文档后做巡检与补同步 |
| `project-memory-manager`    | 维护项目总卡 | 更新状态、同步信息                               |
| `brief-decomposer`          | 拆解需求     | 需求混乱时                                       |
| `research-analyzer`         | 研究分析     | 寻找差异化                                       |
| `concept-generator`         | 生成概念     | 头脑风暴阶段                                     |
| `structure-selector`        | 选择结构     | 确定盒型                                         |
| `visual-system-builder`     | 视觉系统     | 定义视觉语言，并拆解 AI 概念素材任务             |
| `design-version-tracker`    | 版本追踪     | 记录设计变更决策和追溯变更理由                   |
| `visual-direction-validator`| 视觉验证出图 | 快速验证包装视觉方向，生成设计师参考包、提示词和可选 AI 草案 |
| `material-finishing-advisor`| 材质顾问     | 选材定工艺                                       |
| `prepress-checker`          | 印前检查     | 发厂前检查                                       |
| `supplier-brief-writer`     | 供应商 brief | 工厂沟通                                         |
| `quotation-comparator`      | 对比报价     | 决策时                                           |
| `project-tracker`           | 项目追踪     | 项目管理                                         |
| `proposal-builder`          | 提案整理     | 汇报逻辑、页序和讲解备注                         |
| `project-retrospective`     | 项目复盘     | 项目结束后                                       |
| `knowledge-synthesizer`     | 知识沉淀     | 把项目经验回写到共享知识库                       |

---

## 核心原则

### 1. 阶段交接规则

- **定位不清 → 不进入概念**
- **结构未定 → 不进入视觉**
- **材质未测 → 不进入量产**

### 1.1 Brief 逐步成熟

前期 brief 不要求一次性填满。系统先判断 brief 状态，再决定输出粒度：

| 状态 | 用法 |
|------|------|
| 原始需求 | 记录客户原话、已知事实和关键缺口，不用推测补满 |
| 可推进 | 已能支持下一步动作；用 `brief-decomposition.md` 承载假设、风险、缺口和移交项，`packaging-brief.md` 只同步已确认事实和待确认边界 |
| 已确认 | 入口层信息已确认，可移交研究、概念、结构、视觉、供应商沟通或印前处理 |

brief 不是一次性填满的正式生产任务书。成本拆分、MOQ、材料克重、供应商状态、验收负责人、素材授权负责人、合规负责人和成功指标，默认由后续对应 skill 承接；除非用户或项目资料明确提供，否则不写成 brief 已确认事实。

### 1.5 横向商业检查点

供应商沟通、成本意识和排期风险不是第 7 层才开始的。每层都要检查：

| 层级 | 商业检查点 | 成本依据等级 |
|------|-----------|-------------|
| 0. 状态层 | MOQ、供应商状态、审批人、硬截止、合规/授权/验收状态是否已记录 | 预算上限标注 [C1]？ |
| 1. 洞察层 | 渠道、预算、批量、上市时间、供应商是否已定；标签/合规阻塞是否已识别 | 预算/成本上限的证据等级？ |
| 2. 概念层 | 用户共鸣、货架/电商表现、供应链依赖是否验证 | 成本变量已识别 [C0]？ |
| 3. 结构层 | 装箱效率、打样周期、供应商能力、结构成本 | 成本压力来源已拆解 [C0-C2]？ |
| 4. 视觉层 | 电商缩略图、货架远视、印刷适配、法规信息区、AI 概念草案状态、素材授权 | 印刷复杂度成本压力 [C0]？ |
| 5. 材料层 | MOQ、纸材稳定性、工艺良率、成本/交期、食品接触材料状态 | 供应商报价 [C3+] 或成本压力 [C0]？ |
| 6. 印前层 | 校样审批、色差、文件责任边界、合规复核、样品验收 | 最终成本已确认 [C4-C5]？ |
| 8. 复盘层 | 哪些商业风险应前置进下一次开案 | 成本估算与实际偏差？ |

### 2. 单一事实来源

项目总卡是单一事实来源，每个阶段完成后必须更新。
如果怀疑项目卡已落后于下游产出，可运行 `.claude/skills/project-memory-manager/scripts/check-memory-drift.py` 做批量检查。

同时，`README.md` 是这套系统对外公开的命名规范源头；如果某个 skill、模板或脚本引用了不同文件名，应以本文档为准并回补同步。

### 2.5 合规与素材授权

包装用于商业销售前，必须显式检查法规/标签信息和素材授权状态。

- 字体、图片、插画、AI 生成图、认证标志和合作方 Logo 都要记录来源与授权状态
- AI 生成的主视觉、辅助图形、底纹、印章或图标默认是概念草案，归档到 `03_Design/02_Assets/AI_Concepts/{task-id}/`，不得直接进入 `04_Final`
- 茶叶包装的标签信息、食品接触材料、条码、生产信息和宣传边界必须有内部法规/品控或供应商依据
- 视觉方向可以提出合规信息区和授权风险，但最终合规结论不得由设计推断替代
- 推荐归档：`03_Design/02_Assets/asset-register.md`、`03_Design/06_Proof_Record/compliance-review.md`

### 3. 冻结项管理

一旦标记"冻结"，变更必须记录原因和影响。

### 4. 样品与大货验收

真实项目的完成标准不是效果图好看，而是白样、彩样和大货能被共同验收。

- 白样重点看结构、尺寸、开合、内托、装箱和运输风险
- 彩样/合同样重点看色差、纸张、工艺、覆膜、烫金、压纹和信息可读性
- 大货首件和抽检重点看与签样一致性、批量缺陷、数量和批次状态
- 推荐归档：`03_Design/06_Proof_Record/sample-acceptance-record.md`

### 5. 风险优先

每个阶段必须显式列出风险和假设。

### 6. 知识回写

项目复盘不是终点。对未来项目有复用价值的经验，应继续回写到 `Workspace/Knowledge/Library/`，同时让运行文件留在 `Workspace/Knowledge/Operations/`。

### 7. 批量整理

当项目变多后，不再逐个手工检查。让 Claude Code 先盘点项目沉淀覆盖率，再处理缺口项目和工作区级总结。

### 8. 固定会话

批量整理不再依赖临场组织。让 Claude Code 先生成 `Operations/current/current-review-session.md`，再按统一顺序处理，并把结果写入 `Operations/history/`。

### 9. 一键启动

第四版开始，可以先运行一条脚本，把覆盖表、收件箱、会话包和日志草稿一次准备好，再开始判断具体知识。

---

## 系统文档

| 文档                                                                              | 说明                                                             |
| --------------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| `README.md`                                                                       | 本文档，系统入口与人读说明                                       |
| `CLAUDE.md`                                                                       | Claude 执行规则总纲（当前唯一主版本，中文）                      |
| `.claude/references/skills-test-cases.md`                                          | 技能测试用例                                                     |
| `Workspace/Knowledge/`                                                            | Claude Code 共享知识库根目录                                     |
| `.claude/skills/packging-os-maintainer/SKILL.md`                                    | Claude Code 系统治理入口：检查 skill、路由、模板和文档同步       |
| `.claude/skills/knowledge-synthesizer/scripts/get_knowledge_coverage.py`         | Claude Code 批量盘点项目沉淀覆盖率                               |
| `.claude/skills/knowledge-synthesizer/scripts/build_knowledge_review_packet.py`  | Claude Code 生成本轮知识整理会话包                               |
| `.claude/skills/knowledge-synthesizer/scripts/start_knowledge_review_session.py` | Claude Code 一键启动本轮知识整理会话                             |
| `.claude/skills/packging-os-maintainer/scripts/validate-packging-os.cmd`              | Windows 一键治理校验入口：调用系统自带 Windows PowerShell，不依赖 Python |
| `.claude/skills/packging-os-maintainer/scripts/validate-packging-os.sh`               | Mac/Linux 一键治理校验入口：自动选择 `python3`、`python` 或 `pwsh` |
| `.claude/skills/packging-os-maintainer/scripts/validate-packging-os.ps1`              | PowerShell 版最小一致性检查：适合 Windows 或已安装 `pwsh` 的环境 |
| `.claude/skills/packging-os-maintainer/scripts/validate-packging-os.py`               | Python 版最小一致性检查：适合 Mac、Cloud Code 或无 `pwsh` 的环境 |
| `.claude/skills/project-memory-manager/scripts/project-file-utils.ps1`                | 项目文档安全写入工具：同目录临时文件 + 原子替换 + 残留清理 |
| `.claude/skills/project-memory-manager/scripts/cleanup-project-temp-files.cmd`       | Windows 项目临时文件清理入口，默认 dry-run，传 `-Execute` 才删除 |
| `.claude/skills/project-memory-manager/scripts/cleanup-project-temp-files.sh`        | Mac/Linux 项目临时文件清理入口，默认 dry-run，传 `--execute` 才删除 |

### 文档分工

- `README.md`：解释这套系统是什么、什么时候用、怎么开始。
- `CLAUDE.md`：规定 Claude 在这个仓库里必须如何路由、输出、验证和归档。
- `SKILL.md`：定义每个具体阶段的触发条件、工作流和交付规则。

### 治理校验环境

如果你同时在 Windows 和 Mac 上维护这套系统，推荐把治理校验统一成“双入口”：

- Windows：运行 `.claude\skills\packging-os-maintainer\scripts\validate-packging-os.cmd`，它调用 Windows 自带 PowerShell 5.1+，不依赖系统 Python。
- Mac / Linux：运行 `sh .claude/skills/packging-os-maintainer/scripts/validate-packging-os.sh`，它会按顺序寻找 `python3`、`python`、`pwsh`。
- 高级用法：如果你明确想指定运行时，也可以直接运行底层 `validate-packging-os.ps1` 或 `validate-packging-os.py`。

最小自检命令：

```bash
# Windows
.claude\skills\packging-os-maintainer\scripts\validate-packging-os.cmd

# Mac / Linux
sh .claude/skills/packging-os-maintainer/scripts/validate-packging-os.sh
```

说明：

- `.cmd` 和 `.sh` 是入口脚本，负责选择合适运行时；`.ps1` 和 `.py` 是底层校验器，覆盖同一组核心治理检查。
- Windows 默认走 `.cmd`，避免因为没装 Python 导致治理脚本变成摆设。
- Mac 如果没有 Python 3，可安装 Python 3，或安装 PowerShell 7 后让 `.sh` 自动走 `pwsh`。
- 日常治理顺序建议固定为：先跑 `validate-packging-os`，如果出现 `[temp-file]` 或 `[temp-dir]`，先用项目清理脚本 dry-run 看清单，再执行删除。
- 后续凡是脚本批量写入项目级 Markdown，优先复用 `project-file-utils.ps1` 的安全写入流程，避免半写入文件长期留在项目目录里。

---

## 演示案例

查看 `Workspace/Projects/山隐_东方高端茶/` 了解当前在用的项目目录结构和阶段产出：

- 从 brief 到材料层方案的完整文档链
- `00_Project_Control/project-memory-card.md` 是单一信息源，覆盖项目摘要、里程碑时间线、桥接节点状态

---

_Packging OS — 秩序不是终点，是让创造力得以生长的土壤_
