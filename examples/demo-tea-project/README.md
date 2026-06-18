# 山隐·东方高端茶 — 模板化示例项目（Demo Project）

> ⚠️ 这是一个**模板化示例项目**。它展示 Packging OS 一个完整茶包装项目从 brief 到复盘的 **9 层目录骨架**与**标准产出文件**。
> 目录里的每个文件都是**空白模板**（含字段结构、占位符、填写说明），**不含真实业务内容**。
> 用法：复制本目录到真实项目，按层逐项填写。

## 项目标识（示例占位）

| 字段 | 示例占位 |
|------|---------|
| 项目名 | 山隐·东方高端茶 |
| 品牌 | 山隐（示例） |
| 类型 | 东方高端茶礼盒（示例定位） |
| 状态 | 模板，待填写 |

## 9 层目录与标准产出文件

```
demo-tea-project/
├── 00_Project_Control/          ← Layer 0 单一事实源
│   ├── project-memory-card.md
│   ├── project-tracker.md
│   └── decision-log.md
├── 01_Brief/                    ← Layer 1 需求
│   ├── packaging-brief.md
│   └── brief-decomposition.md
├── 02_Research/                 ← Layer 2 研究/定位
│   └── positioning-summary.md
├── 03_Design/                   ← Layer 3-6 设计/生产
│   ├── 01_Working/
│   │   ├── concept-directions.md      ← Layer 2 概念
│   │   ├── structure-decision.md      ← Layer 3 结构
│   │   └── visual-direction.md        ← Layer 4 视觉
│   ├── 02_Assets/
│   │   └── asset-register.md
│   ├── 03_Presentation/
│   │   └── proposal-outline.md        ← Layer 7 提案
│   ├── 04_Production/
│   │   ├── material-finishing-plan.md ← Layer 5 材质工艺
│   │   ├── supplier-brief.md          ← Layer 7 供应商
│   │   ├── quotation-comparison.md    ← Layer 7 报价
│   │   └── packaging-cost-summary.md
│   └── 06_Proof_Record/               ← Layer 6 印前/样品
│       ├── prepress-review.md
│       ├── compliance-review.md
│       ├── sample-acceptance-record.md
│       └── proofing-record.md
└── 05_Retrospective/            ← Layer 8 复盘
    └── project-retrospective.md
```

## 模板使用指引

**占位符约定**
- `<必填>` 必填占位
- `[选项A / 选项B]` 可选项
- `{{字段}}` 待替换变量

**成本证据等级（强制）**
- 所有成本/价格结论标注 `[C0]`-`[C5]`，详见 `.claude/references/cost-evidence-standard.md`
- 无 `[C3]`+ 证据，不得输出真实价格、单价或"可控制在 ¥XX 内"

**合规 / 资产 / 样品（强制）**
- 涉及视觉素材、AI 草案、标签内容、供应商文件、样品、量产的文件，必须填写授权 / 验收状态
- 字体、图片、插画、AI 生成图、认证标志、合作品牌 logo，未记录授权状态前一律不得标记为"可交付"

**输出规范**
- 每份决策性文件区分：已知事实 / 假设 / 建议 / 风险 / 下一步
- 比较类内容（概念、结构、材质、供应商、报价、排期、风险）用表格

## 注意

- 本目录为**公开示例**，不含真实客户、供应商、报价、电话邮箱、生产文件
- 真实项目数据位于 `Workspace/Projects/`，已被 `.gitignore` 排除，不入此仓库
- 本目录内容是模板，不是真实项目记录
