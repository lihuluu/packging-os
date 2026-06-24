# Packaging OS 输出归档规则

## 目录
- 目标
- 推荐项目结构
- Skill 到目录映射
- 命名规则
- 归档规则

## 目标

这份规则用于解决“skill 已生成交付物，但没有归档到正确目录”的问题。

使用原则：
- 子 skill 负责生成内容
- `packaging-os` 负责判断当前阶段并推荐归档位置
- 所有过程文档、控制文档和最终交付分开存放

## 推荐项目结构

在现有项目目录上，推荐至少补齐这两个目录：

```text
00_Project_Control
01_Brief
02_Research
03_Design
04_Final
05_Retrospective
```

共享知识建议单独维护在：

```text
Workspace/Knowledge
```

说明：
- `00_Project_Control`：仅存放 `project-memory-card.md`（单一事实源）
- `01_Brief`：客户原始资料、brief 拆解稿
- `02_Research`：竞品分析、定位总结、策略判断
- `03_Design`：概念、视觉、结构、材质、供应商沟通、打样等核心工作区
- `04_Final`：只放最终交付
- `05_Retrospective`：复盘与 SOP 更新

初始化脚本也必须遵循这套归档路径：`project-tracker.md` 写入 `00_Project_Control`，`supplier-brief.md` 写入 `03_Design/04_Production`。

如果项目仍沿用旧结构，建议优先新增：
- `00_Project_Control`
- `05_Retrospective`

## Skill 到目录映射

| Skill | 默认交付物 | 默认目录 | 推荐文件名 |
| --- | --- | --- | --- |
| `project-memory-manager` | 项目总卡 | `00_Project_Control` | `project-memory-card.md` |
| `brief-decomposer` | brief 拆解表 + 正式任务书 | `01_Brief` | `brief-decomposition.md` + `packaging-brief.md` |
| `research-analyzer` | 定位总结/研究结论 | `02_Research` | `positioning-summary.md` |
| `concept-generator` | 概念方向卡 | `03_Design/03_Presentation` | `concept-directions.md` |
| `structure-selector` | 结构决策表 | `03_Design/04_Production` | `structure-decision.md` |
| `visual-system-builder` | 视觉方向单 | `03_Design/03_Presentation` | `visual-direction.md` |
| `visual-system-builder` | 素材授权登记 | `03_Design/02_Assets` | `asset-register.md` |
| `visual-system-builder` / `visual-direction-validator` | AI 概念素材任务 + 草案资产 | `03_Design/02_Assets/AI_Concepts/{task-id}` | `ai-concept-brief.md` / `prompts/prompt.md` / `variants/variant-01.png` / `selection-notes.md` |
| `visual-direction-validator` | 方向验证卡 + 设计师参考包 + 提示词 + 可选草案 | `03_Design/02_Assets` | `direction-validation.md` / `designer-reference.md` / `prompts/prompt.md` / `variants/variant-01.png` |
| `material-finishing-advisor` | 材质工艺建议单 | `03_Design/04_Production` | `material-finishing-plan.md` |
| `supplier-brief-writer` | 供应商 brief | `03_Design/04_Production` | `supplier-brief.md` |
| `quotation-comparator` | 报价对比表 | `03_Design/04_Production` | `quotation-comparison.md` |
| （项目负责人填写） | 包装成本明细 | `03_Design/04_Production` | `packaging-cost-summary.md` |
| `project-tracker` | 项目推进表 | `00_Project_Control` | `project-tracker.md` |
| `proposal-builder` | 提案大纲/讲解备注 | `03_Design/03_Presentation` | `proposal-outline.md` |
| `prepress-checker` | 印前检查/打样诊断 | `03_Design/06_Proof_Record` | `prepress-review.md` |
| `prepress-checker` | 合规复核记录 | `03_Design/06_Proof_Record` | `compliance-review.md` |
| `prepress-checker` | 样品与大货验收记录 | `03_Design/06_Proof_Record` | `sample-acceptance-record.md` |
| `project-retrospective` | 项目复盘 | `05_Retrospective` | `project-retrospective.md` |
| `knowledge-synthesizer` | 项目知识沉淀 + 共享知识回写 | `05_Retrospective` + `Workspace/Knowledge` | `knowledge-synthesis.md` |
| `design-version-tracker` | 决策日志 | `03_Design/01_Working` | `decision-log.md` |

## 命名规则

### 默认规则

- skill id 与 skill 目录统一使用 `kebab-case`
- 项目文档、知识文档、模板产物统一使用 `kebab-case`
- 控制层常驻文档优先使用固定名：
  - `project-memory-card.md`（单一事实源）
- 阶段性交付可使用固定名或版本名：
  - `concept-directions-v1.md`
  - `structure-decision-v2.md`
  - `prepress-review-2025-11-08.md`

### 版本建议

- 持续更新型文档：覆盖更新为主
  - 项目总卡
  - 项目推进表
  - 供应商 brief
- 评审型文档：保留版本更好
  - 概念方向卡
  - 结构决策表
  - 材质工艺建议单
  - 印前检查记录
  - 合规复核记录
  - 样品与大货验收记录
  - 项目复盘

### 废弃命名

以下命名只允许作为历史兼容对象存在，不再作为新产物推荐名：

- `project_tracker.md`
- `structure-selection.md`

如果在旧项目中沿用了这些文件名：

- 新生成文档仍按标准名输出
- 在文档头部或说明中标注“推荐正式归档位置”和标准文件名
- 后续迁移时统一改回标准名，不继续扩散旧名

## 归档规则

### Final 目录规则

- `04_Final` 只放真正最终交付物
- 不要把以下文档放进 `04_Final`：
  - 项目总卡
  - 报价比较
  - 推进表
  - brief 拆解
  - 研究结论
  - 过程版概念卡
  - 打样问题诊断

### 控制层规则

- `00_Project_Control` 存放 `project-memory-card.md`（单一事实源）和 `project-tracker.md`（项目推进表）；不放其他阶段文档
- 供应商 brief、报价对比等生产沟通文档放进 `03_Design/04_Production`
- 项目推进表与项目卡保持在同一控制层：`00_Project_Control`
- 不和 AI 源文件、效果图、刀模源文件混放

### 知识层规则

- 项目级知识沉淀放 `05_Retrospective/knowledge-synthesis.md`
- 跨项目可复用规则放 `Workspace/Knowledge/Library/`
- 共享知识更新时，先改索引，再改分类文件
- 批量模式下，同时维护：
- `Workspace/Knowledge/Operations/coverage/project-knowledge-coverage.md`
- `Workspace/Knowledge/Operations/queue/knowledge-capture-inbox.md`
- `Workspace/Knowledge/Library/workspace-knowledge-digest.md`
- `Workspace/Knowledge/Operations/current/current-review-session.md`
- `Workspace/Knowledge/Operations/history/`
- `Workspace/Knowledge/Operations/current/current-review-log-draft.md`

### 设计层规则

- 提案型文档放 `03_Design/03_Presentation`
- 字体、图片、插画、AI 图、品牌资产授权记录放 `03_Design/02_Assets`
- AI 生成的图像/图形草案放 `03_Design/02_Assets/AI_Concepts/{task-id}`，默认只作为概念素材，不直接进入 `04_Final`
- 生产与结构型文档放 `03_Design/04_Production`
- 打样、验收、合规复核与印前记录放 `03_Design/06_Proof_Record`
- 结构文档标准名固定为 `structure-decision.md`，不再新建 `structure-selection.md`

### 如果目录不存在

- 不要把文档随意塞进已有目录
- 优先建议补建目标目录
- 如果必须临时兼容旧项目结构，至少在文档开头写清“推荐正式归档位置”
