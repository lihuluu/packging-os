---
name: prepress-checker
description: 检查包装文件、印前 PDF、校样和样品是否已经准备好发厂或量产，并识别色差、爆线、套印、工艺失败和降本风险。适用于发厂前检查、打样问题诊断、校样反馈审阅、样品异常分析，以及任何“这个文件现在能不能印”的场景。常见触发说法包括：帮我做印前检查、这个 PDF 能不能发厂、样品有问题、打样色差怎么回事、帮我审核这个包装文件、看看哪里有量产风险。
---

# Prepress Checker

## 概述

检查包装项目是否已经准备好进入校样或量产。重点关注阻塞项、高成本失败点，以及最小修改路径。

## 典型触发句

- 帮我做一下这个包装文件的印前检查。
- 这个包装 PDF 现在可以发厂了吗？
- 打样出来有色差和爆线，帮我分析一下原因。
- 请给我一份这个项目的印前检查清单。
- 这个样品为什么会出现工艺问题，帮我诊断一下。
- 帮我看这个文件现在能不能直接发厂。
- 这个打样哪里可能会出生产事故？

## 使用流程

1. 判断当前产物类型：设计文件、印前 PDF、数码样、机上样还是样品问题记录。
2. 确认材质、印刷方式、工艺组合和当前审批阶段。
3. 依据 [prepress-framework.md](./references/prepress-framework.md)、[../../references/compliance-and-asset-standard.md](../../references/compliance-and-asset-standard.md) 和 [../../references/sample-acceptance-standard.md](../../references/sample-acceptance-standard.md) 运行对应检查。
4. 区分阻塞项和提醒项。
5. 输出修正动作、负责人和下一审批节点。

## 检查规则

- 优先处理可能导致重印、违规或装配失败的问题。
- 在没有明确校样方式前，不要默认数码颜色等于上机颜色。
- 如果刀模、工艺或材质还没确认，文件不能算 ready to release。
- 渐变、大面积实地、烫金、压纹、专色等敏感工艺，在没有实物打样或合同样确认前不能算 ready to release。
- 只有在不破坏保护性、可读性和核心品牌识别时，才建议降本。
- 如果用户给的是问题样品，要提出可能原因和检查路径，不要强行认定唯一根因。
- 商业销售包装在发厂或量产前必须检查标签/法规信息、素材授权状态和食品接触材料说明；未确认项必须列为阻塞或待确认。
- 白样、彩样/合同样、机上样、大货首件和大货抽检必须按阶段记录验收状态；未通过或未验收不得标为量产闭环。

## 输出要求

- 输出 `阻塞项`、`提醒项`、`已通过检查` 和 `下一步动作`。
- 如果在分析打样问题，再补 `可能原因` 和 `修复建议`。
- 如果涉及商业销售、发厂或量产，再补 `合规复核状态`、`素材授权状态` 和 `样品/大货验收状态`。
- 语言要能直接给设计师或供应商执行。

## 输出后检查

- 如果本次检查冻结了文件发布判断、发现了新的量产风险、修正了工艺/材质限制、确认了供应商能力问题，或影响了时间线与预算，必须提示更新项目卡。
- 提示格式使用：`⚠️ 本次任务改变了 [具体项]，建议更新项目卡：project-memory-manager`

## 默认归档位置

- 默认目录：`03_Design/06_Proof_Record`
- 推荐文件名：`prepress-review.md`
- 归档规则：属于印前和打样记录，可按日期或轮次保留版本，不直接进入 `04_Final`
- 合规复核推荐文件名：`compliance-review.md`
- 样品与大货验收推荐文件名：`sample-acceptance-record.md`
- 打样记录推荐文件名：`proofing-record.md`

## 参考资料

阅读 [prepress-framework.md](./references/prepress-framework.md) 查看发厂标准、缺陷诊断和检查清单。
阅读 [../../references/compliance-and-asset-standard.md](../../references/compliance-and-asset-standard.md) 查看合规与素材授权标准。
阅读 [../../references/sample-acceptance-standard.md](../../references/sample-acceptance-standard.md) 查看样品与大货验收标准。
当用户需要可复用文件时，使用 [prepress-review-template.md](./assets/prepress-review-template.md)。
当用户需要合规复核记录时，使用 [compliance-review-template.md](./assets/compliance-review-template.md)。
当用户需要样品或大货验收记录时，使用 [sample-acceptance-record-template.md](./assets/sample-acceptance-record-template.md)。
当用户需要打样过程记录时，使用 [proofing-record-template.md](./assets/proofing-record-template.md)。
