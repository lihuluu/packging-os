---
name: visual-direction-validator
description: Validate packaging visual directions before design execution or AI draft generation. Use when the user wants quick packaging design image validation, visual route comparison, packaging illustration or artwork direction, AI concept draft prompts, or to process AI concept asset tasks from a visual direction sheet. Triggers include packaging visual validation, 包装视觉方向验证, 包装出图快速验证, 包装插画, 标签插画, AI 草案, AI 概念素材, 主视觉草案, 底纹草案, 辅助图形, and visual direction validation. Default domain is tea packaging; for clearly non-tea categories, state that the category-specific module is not yet specialized and use the generic packaging framework.
---

# Packaging Visual Direction Validator

Use this skill to turn a packaging visual idea into a fast validation package. The goal is to decide whether a visual direction is worth design execution, not to produce final assets.

Default posture:
- Validate first.
- Generate prompts second.
- Generate images only when explicitly requested.
- Treat all AI images as draft references, never as final production assets.

## Boundary

Use `visual-system-builder` when the user needs a full packaging visual system: commercial communication goal, information hierarchy, layout rules, SKU rules, and visual direction sheet.

Use this skill when the user needs to validate or execute the image/artwork part of a visual direction:
- compare several image or artwork routes
- decide whether to use plant, product, pattern, seal, landscape, or abstract graphics
- create a designer-readable reference package
- create AI prompts for concept drafts
- generate or register AI concept drafts after the user confirms image generation

If a visual direction sheet already contains `AI 概念素材任务`, treat those tasks as the input contract.

## Operating Modes

### 1. Direction Validation Mode

Use by default. Do not create images.

Output:
- direction cards
- designer reference brief
- prompt package, if useful
- screening notes template
- next-step recommendation

### 2. Project Integrated Mode

Use when the request includes a project path, a task ID, or comes from `visual-direction.md`.

Default output structure:

```text
Workspace/Projects/{project}/03_Design/02_Assets/AI_Concepts/{task-id}/
├── ai-concept-brief.md
├── prompts/
│   └── prompt.md
├── variants/
└── selection-notes.md
```

Also remind the user to update:

```text
Workspace/Projects/{project}/03_Design/02_Assets/asset-register.md
```

Default asset status:

```text
AI 生成草案 / 仅参考 / 不可直接终稿
```

### 3. Draft Generation Mode

Use only when one of these is true:
- the user explicitly asks to generate images, 出图, 做几版草案, or variants
- an existing `AI 概念素材任务` asks for generated draft variants
- the user has selected a direction and asks to validate it through images

When generating images, keep the same project structure. Never write results to `04_Final`.

## Input Check

Extract or infer these fields:

| Field | Purpose |
| --- | --- |
| product | category, SKU, name, or short description |
| pack type | box, pouch, can, label, wrapper, bag, sachet, gift box, or other |
| key face | front, back, side, top, wraparound, e-commerce thumbnail |
| positioning | premium, daily value, heritage, natural, modern, gift, functional, playful |
| channel | shelf, e-commerce, gift, wholesale, internal sample, proposal |
| visual job | attract, explain, prove quality, create memory, add texture, unify SKU |
| constraints | fixed logo, color, material, printing, legal, forbidden motifs, reference style |

Ask at most one focused question only if a missing field blocks the validation.

## Validation Workflow

### Step 1. Read Context

If a project path is available, read the most relevant files before judging:

- `00_Project_Control/project-memory-card.md`
- `01_Brief/packaging-brief.md`
- `02_Research/positioning-summary.md`
- `03_Design/03_Presentation/visual-direction.md`
- `03_Design/02_Assets/asset-register.md`

Do not read every project file. Prefer current-state and visual-context files.

### Step 2. Build 3 Direction Cards

Create 2-3 clearly different visual direction cards. Each card must include:

- **Name**: short route name
- **Visual hypothesis**: what this route is trying to prove
- **Subject**: what appears visually
- **Composition**: where it lives on the packaging
- **Style**: how it is rendered
- **Best test surface**: where to test it fastest
- **Keep signal**: what would make this direction worth continuing
- **Kill signal**: what would make this direction not worth continuing
- **Production caution**: print, material, rights, or compliance risk

Use the reference library only as needed:

- `references/subjects/{subject}.md`
- `references/compositions/{composition}.md`
- `references/styles/{style}.md`
- `references/analysis-framework.md`

### Step 3. Choose Recommendation

Recommend one route as the next test. Explain why in packaging terms:

- real buying scene
- recognition at first glance
- fit with price and channel
- fit with structure and print
- risk of over-design or misleading evidence

### Step 4. Produce Designer Reference Package

For the selected route, write a compact reference package:

- design intent
- visual elements
- layout placement
- color and texture direction
- material or print assumptions
- forbidden content
- handoff note for designer redraw/vectorization

State clearly when the package is only for reference.

### Step 5. Produce Prompt Package

When prompt output is useful or requested, create a bilingual prompt package:

- Chinese version for project discussion
- English version for image tools
- negative prompt
- packaging context
- no text inside the image
- no logo, certification mark, fake origin proof, watermark, or competitor element

Use `references/base-prompt.md` as the base template.

### Step 6. Generate Drafts Only If Confirmed

If image generation is confirmed:

1. Check existing `variants/` files and continue numbering.
2. Generate drafts with the selected prompt.
3. Save outputs under the task folder.
4. Update or instruct updating `selection-notes.md`.
5. Keep status as draft reference until designer redraw, vectorization, authorization, and prepress review happen.

## Output Templates

### Direction Validation Summary

```markdown
# 视觉方向快速验证

## 输入判断
- 产品/品类：
- 包装形态：
- 关键展示面：
- 当前目标：

## 方向卡

### A. {route name}
- 验证假设：
- 视觉主题：
- 构图方式：
- 风格手法：
- 最快测试位置：
- 保留信号：
- 淘汰信号：
- 生产/授权风险：

## 推荐下一步
- 推荐路线：
- 原因：
- 下一步动作：
```

### Selection Notes

```markdown
# AI 概念素材筛选记录

## {task-id}
- 任务目的：
- 已生成/待生成版本：
- 保留版本：
- 淘汰版本：
- 采用方式：仅参考 / 设计师重绘 / 矢量化 / 淘汰
- 授权状态：AI 生成草案 / 仅参考 / 不可直接终稿
- 下一步：
```

## Rules

- Never present AI output as final artwork.
- Never place AI drafts in `04_Final`.
- Never claim commercial-use rights unless the tool, license, company policy, and asset status are confirmed.
- Never create logos, certification marks, legal proof, real-origin evidence, or fake process evidence with AI.
- Do not let a pretty image override packaging logic. Test the route against channel, structure, information hierarchy, print, and buyer recognition.
- If a project has explicitly abandoned AI image generation, do not generate drafts; provide designer reference and validation notes only.

