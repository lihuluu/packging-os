#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
init-project.py — Packaging OS 项目目录初始化脚本

用法：
    python3 .claude/skills/packaging-os-maintainer/scripts/init-project.py "项目名称"

功能：
    在 Workspace/Projects/<项目名称>/ 下创建标准目录结构，
    并写入一组项目启动模板包。

选项：
    --root PATH     手动指定仓库根目录（默认自动推断，取脚本所在位置上 4 级）
    --dry-run       只打印将要创建的路径，不实际创建
"""
import argparse
import io
import sys
from pathlib import Path

# Windows 终端编码兼容
if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf-8-sig"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
if sys.stderr.encoding and sys.stderr.encoding.lower() not in ("utf-8", "utf-8-sig"):
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")


DIRS = [
    "00_Project_Control",
    "01_Brief",
    "02_Research",
    "03_Design/01_Working",
    "03_Design/02_Assets",
    "03_Design/02_Assets/AI_Concepts",
    "03_Design/03_Presentation",
    "03_Design/04_Production",
    "03_Design/05_Renders",
    "03_Design/06_Proof_Record",
    "04_Final/01_Print_Files",
    "04_Final/02_Source_Files",
    "04_Final/03_Assets",
    "04_Final/04_Previews",
    "04_Final/05_Dielines",
    "05_Retrospective",
]

STARTER_FILES = [
    (
        ".claude/skills/project-memory-manager/assets/project-memory-card-template.md",
        "00_Project_Control/project-memory-card.md",
    ),
    (
        ".claude/skills/project-tracker/assets/project-tracker-template.md",
        "00_Project_Control/project-tracker.md",
    ),
    (
        ".claude/skills/visual-system-builder/assets/asset-register-template.md",
        "03_Design/02_Assets/asset-register.md",
    ),
    (
        ".claude/skills/supplier-brief-writer/assets/supplier-brief-template.md",
        "03_Design/04_Production/supplier-brief.md",
    ),
    (
        ".claude/skills/prepress-checker/assets/compliance-review-template.md",
        "03_Design/06_Proof_Record/compliance-review.md",
    ),
    (
        ".claude/skills/prepress-checker/assets/sample-acceptance-record-template.md",
        "03_Design/06_Proof_Record/sample-acceptance-record.md",
    ),
    (
        ".claude/skills/prepress-checker/assets/proofing-record-template.md",
        "03_Design/06_Proof_Record/proofing-record.md",
    ),
    (
        ".claude/skills/brief-decomposer/assets/brief-decomposition-template.md",
        "01_Brief/brief-decomposition.md",
    ),
    (
        ".claude/skills/brief-decomposer/assets/packaging-brief-template.md",
        "01_Brief/packaging-brief.md",
    ),
    (
        ".claude/skills/design-version-tracker/assets/decision-log-template.md",
        "03_Design/01_Working/decision-log.md",
    ),
]
FALLBACK_TEMPLATES = {
    ".claude/skills/project-memory-manager/assets/project-memory-card-template.md": """\
# 包装项目总卡

## 项目摘要
- 项目名称：
- 产品/品类：
- 当前阶段：
- 目标上市时间：
- 销售渠道：
- 目标价格带：

## 商业硬约束
- 预算上限（单 SKU 包装成本）：
- MOQ 预估：
- 首发批量：
- 供应商状态：未触达 / 初步接触 / 已确认能力 / 已报价
- 审批人：
- 硬截止日期：
- 当前最大商业风险：

## 合规、授权与验收状态
- 标签/法规信息状态：未开始 / 待确认 / 已复核
- 素材授权状态：未开始 / 待确认 / 已登记 / 存在不可用素材
- 食品接触材料状态：不适用 / 待供应商确认 / 已确认
- 白样验收状态：未开始 / 待验收 / 通过 / 有条件通过 / 不通过
- 彩样/合同样验收状态：未开始 / 待验收 / 通过 / 有条件通过 / 不通过
- 大货首件/抽检状态：未开始 / 待验收 / 通过 / 有条件通过 / 不通过 / 不适用

## 已知事实
### 产品与商业约束
- 实物规格 / 内容物：
- 目标用户：
- 环保优先级：

### 供应商与量产前提
- 当前供应商状态：
- 已确认供应商能力：
- MOQ 预估：

## 冻结项
 -

## 开放问题
 -

## 关键假设
 -

## 风险
 -

## 依赖项
 -

## 下一步动作
1.
2.
3.

## 本次更新
- 新增：
- 变更：
- 失效：
""",
    ".claude/skills/project-tracker/assets/project-tracker-template.md": """\
# 包装项目推进表

## 当前阶段
-

## 关键里程碑
| 里程碑 | 目标时间 | 负责人 | 依赖项 | 状态 |
| --- | --- | --- | --- | --- |
| Brief 确认 |  |  |  |  |
| 概念确认 |  |  |  |  |
| 结构确认 |  |  |  |  |
| 材质工艺确认 |  |  |  |  |
| 合规/标签复核 |  |  |  |  |
| 素材授权确认 |  |  |  |  |
| 打样 |  |  |  |  |
| 白样验收 |  |  |  |  |
| 彩样/合同样验收 |  |  |  |  |
| 大货首件/抽检 |  |  |  |  |
| 发厂 |  |  |  |  |

## 任务清单
| 任务 | 优先级 | 负责人 | 前置条件 | 状态 |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

## 风险节点
-

## 合规/授权/验收节点
| 节点 | 负责人 | 依赖项 | 状态 | 下一步 |
| --- | --- | --- | --- | --- |
| 合规/标签复核 |  |  |  |  |
| 素材授权登记 |  |  |  |  |
| 白样验收 |  |  |  |  |
| 彩样/合同样验收 |  |  |  |  |
| 大货首件/抽检 |  |  |  |  |

## 下一周动作
1.
2.
3.
""",
    ".claude/skills/supplier-brief-writer/assets/supplier-brief-template.md": """\
# 供应商 Brief

## 项目背景
- 项目名称：
- 产品/品类：
- 目标渠道：
- 目标价格带：

## 需求规格
- 结构形式：
- 尺寸：
- 预计数量：
- 材质：
- 印刷：
- 后道工艺：

## 本次目标
- [ ] 询价
- [ ] 打样
- [ ] 可行性确认
- [ ] 交期确认

## 必须确认项
1.
2.
3.

## 交付要求
- 需要提供：
- 回复截止时间：
- 打样验收重点：

## 合规/材料文件需求
- 食品接触材料或内包材说明：
- 材料规格/克重/厚度：
- 工艺外协情况：
- 条码或可变信息印刷风险：
- 大货批次/留样方式：

## 样品与大货验收标准
- 白样验收重点：
- 彩样/合同样验收重点：
- 机上样验收重点（如适用）：
- 大货首件验收重点：
- 大货抽检标准：

## 供应商回复清单
- 单价：
- MOQ：
- 打样费：
- 刀模费/版费：
- 交期：
- 风险说明：
""",
    ".claude/skills/visual-system-builder/assets/asset-register-template.md": """\
# 素材授权登记表

## 项目摘要
- 项目名称：
- 产品/品类：
- 当前版本：
- 登记日期：
- 负责人：

## 素材授权清单
| 编号 | 素材类型 | 素材名称/描述 | 使用位置 | 来源 | 授权状态 | 授权范围/限制 | 需要确认人 | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A-001 | 字体 / 图片 / 插画 / AI 图 / Logo / 认证标志 | | | | 已确认 / 内部资产 / 待确认 / 仅参考 / 不可用 | | | |

## 不能进入最终交付的素材
| 素材 | 原因 | 替代动作 |
| --- | --- | --- |
| | | |
""",
    ".claude/skills/prepress-checker/assets/compliance-review-template.md": """\
# 合规复核记录

## 项目摘要
- 项目名称：
- 产品/品类：
- 销售渠道/地区：
- 当前版本：
- 复核日期：
- 复核人/责任部门：

## 标签与法规信息检查
| 项目 | 状态 | 来源/确认人 | 备注 |
| --- | --- | --- | --- |
| 品名 | 已确认 / 待确认 / 不适用 | | |
| 规格/净含量 | 已确认 / 待确认 / 不适用 | | |
| 生产商/委托方 | 已确认 / 待确认 / 不适用 | | |
| 执行标准 | 已确认 / 待确认 / 不适用 | | |
| 生产许可/SC | 已确认 / 待确认 / 不适用 | | |
| 条码 | 已确认 / 待确认 / 不适用 | | |
| 食品接触材料说明 | 已确认 / 待确认 / 不适用 | | |
""",
    ".claude/skills/prepress-checker/assets/sample-acceptance-record-template.md": """\
# 样品与大货验收记录

## 项目摘要
- 项目名称：
- 产品/品类：
- 供应商：
- 样品阶段：白样 / 数码样 / 彩样/合同样 / 机上样 / 大货首件 / 大货抽检
- 样品版本/批次：
- 验收日期：
- 验收人：

## 验收检查表
| 维度 | 检查项 | 状态 | 问题描述 | 处理建议 |
| --- | --- | --- | --- | --- |
| 结构 | 尺寸、折线、开合、内托、装箱 | 通过 / 有条件通过 / 不通过 / 不适用 | | |
| 外观 | 色差、污点、擦花、压痕、毛边、溢胶 | 通过 / 有条件通过 / 不通过 / 不适用 | | |
| 印刷 | 套印、糊字、断线、实地、条码可读性 | 通过 / 有条件通过 / 不通过 / 不适用 | | |
| 工艺 | 烫金、UV、压凸压凹、模切偏移 | 通过 / 有条件通过 / 不通过 / 不适用 | | |

## 验收结论
- [ ] 通过
- [ ] 有条件通过
- [ ] 不通过
""",
    ".claude/skills/prepress-checker/assets/proofing-record-template.md": """\
# 打样记录

## 项目摘要
- 项目名称：
- 产品/品类：
- 供应商：
- 负责人：
- 创建日期：

## 打样进度总览

| 轮次 | 打样类型 | 状态 | 发出日期 | 回收日期 | 关联验收 |
| --- | --- | --- | --- | --- | --- |
| R-001 | 白样 / 数码样 / 彩色数码样 / 色样/合同样 / 机上样 | 进行中 / 已回收 / 已签样 / 不通过 |  |  | S-___（见 sample-acceptance-record.md） |

## R-001 — [打样类型]

### 打样参数
- 打样类型：白样 / 数码样 / 彩色数码样 / 色样/合同样 / 机上样
- 供应商：
- 打样数量：
- 刀模/版费：
- 打样费用：
- 预计周期：
- 发出日期：
- 回收日期：

### 打样规格
- 材质：
- 克重/厚度：
- 印刷方式：
- 工艺：
- 色彩标准 / 对照签样：

### 供应商沟通记录
| 日期 | 沟通内容 | 负责人 |
| --- | --- | --- |
|  |  |  |

### 回收反馈
- 结构评价：
- 色彩评价：
- 工艺评价：
- 材料评价：
- 信息/文案评价：
- 总体结论：通过 / 有条件通过 / 不通过

### 问题与调整
| 编号 | 问题 | 调整动作 | 责任方 | 截止时间 | 状态 |
| --- | --- | --- | --- | --- | --- |
| P-001 |  |  |  |  | 待处理 / 已完成 |

### 本轮结论
- 是否需要下一轮打样：
- 下一轮类型：
- 备注：

## 打样时间线

| 节点 | 计划日期 | 实际日期 | 偏差 | 原因 |
| --- | --- | --- | --- | --- |
| 白样发出 |  |  |  |  |
| 白样回收 |  |  |  |  |
| 色样发出 |  |  |  |  |
| 色样回收 |  |  |  |  |
| 合同样签定 |  |  |  |  |
| 大货首件 |  |  |  |  |

## 打样费用汇总

| 轮次 | 类型 | 供应商 | 费用 | 是否计入大货 | 备注 |
| --- | --- | --- | --- | --- | --- |
| R-001 |  |  |  | 是 / 否 |  |
| **合计** | | | | | |

## 关联文档
- 印前检查：prepress-review.md（同目录）
- 合规复核：compliance-review.md（同目录）
- 样品验收：sample-acceptance-record.md（同目录）
- 供应商 Brief：supplier-brief.md（../04_Production/）

## 风险
-

## 开放问题
-

## 下一步动作
1.
2.
3.
""",
    ".claude/skills/brief-decomposer/assets/brief-decomposition-template.md": """\
# 项目 Brief 拆解表

## Brief 状态

| 字段 | 内容 |
|------|------|
| 当前状态 | 原始需求 / 工作中 / 已确认 |
| 信息来源 | 客户原话 / 会议纪要 / 销售转述 / 项目卡 / 其他 |
| 本轮目标 | 澄清需求 / 形成工作版 / 进入确认版 / 进入下一阶段 |
| 最后更新 |  |

## 已知事实

| 维度 | 内容 | 来源/确定性 |
|------|------|-------------|
| 项目名称 |  | 已确认 / 待确认 |
| 产品 |  | 已确认 / 待确认 |
| 品类 |  | 已确认 / 待确认 |
| 价格带 |  | 已确认 / 待确认 |
| 渠道 |  | 已确认 / 待确认 |
| 时间线 |  | 已确认 / 待确认 |

## 工作假设

| 假设 | 依据 | 影响 | 验证方式 |
|------|------|------|----------|
|  |  |  |  |

## 缺失信息

| 缺失项 | 为什么重要 | 阻塞级别 | 下一步确认方式 |
|--------|------------|----------|----------------|
|  |  | 商业阻塞 / 发厂前阻塞 / 可后补 |  |

## 目标

| 类型 | 内容 | 状态 |
|------|------|------|
| 商业目标 |  | 已确认 / 待确认 / 工作假设 |
| 包装目标 |  | 已确认 / 待确认 / 工作假设 |
| 成功标准 |  | 已确认 / 待确认 / 工作假设 |

## 约束条件

| 类型 | 内容 | 状态 |
|------|------|------|
| 尺寸与物流 |  | 已确认 / 待确认 / 工作假设 |
| 法规 |  | 已确认 / 待确认 / 工作假设 |
| 预算 |  | 已确认 / 待确认 / 工作假设 |
| 品牌资产 |  | 已确认 / 待确认 / 工作假设 |

## 开案商业必查
- 销售渠道（是否已定）：
- 包装预算（单 SKU 成本上限）：
- 首发批量预估：
- 上市硬截止日期：
- 供应商是否已定：
- 审批人：
- 合规/标签负责人：
- 素材授权负责人：
- 样品验收负责人：

## 发厂/上市前阻塞项
- 标签/法规信息：
- 素材授权：
- 食品接触材料：
- 白样/彩样/大货验收：

## 风险

| 风险 | 触发条件 | 影响 | 当前处理 |
|------|----------|------|----------|
|  |  |  |  |

## 下一步问题
1.
2.
3.

## 建议下一步
-
""",
    ".claude/skills/design-version-tracker/assets/decision-log-template.md": """\
# 设计决策日志

## 项目摘要
- 产品名称：
- 业务域：茶叶包装 / 其他
- 茶类/工艺：
- 规格/净含量：
- 项目目录：

## 已知事实

### 影响决策的约束条件
-

## 决策记录

| 编号 | 变更内容 | 触发来源 | 决策理由 | 日期 |
|------|---------|---------|---------|------|
| D-___ | | | | |

> 编号：使用 `D-001`、`D-002` 等三位编号，同项目内全局递增。

## 关键假设
-

## 风险
-

## 开放问题
-

## 结论沉淀
-

## 下一步动作
1.
2.
3.
""",
    ".claude/skills/brief-decomposer/assets/packaging-brief-template.md": """\
# 包装设计任务书

> 本文件是任务书快照，不用于承载内部推理。未确认信息保留为「待确认」，工作假设请写入 `brief-decomposition.md`。

## Brief 状态

| 字段 | 内容 |
|------|------|
| 当前状态 | 原始需求 / 工作中 / 已确认 |
| 信息口径 | 仅已确认事实 / 含待确认边界 / 已冻结执行口径 |
| 信息来源 | 客户原话 / 会议纪要 / 销售转述 / 项目卡 / 其他 |
| 最后更新 |  |
| 确认人/确认方式 | 待确认 |

## 项目概览

| 字段 | 内容 |
|------|------|
| 项目名称 |  |
| 负责人 |  |
| 创建日期 |  |
| 目标上市 |  |

## 产品信息

| 字段 | 内容 | 状态 |
|------|------|------|
| 品牌名 |  | 已确认 / 待确认 |
| 品牌一句话 |  | 已确认 / 待确认 |
| 业务域 | 茶叶包装 / 其他 | 已确认 / 待确认 |
| 产品/SKU |  | 已确认 / 待确认 |
| 茶类/工艺 |  | 已确认 / 待确认 |
| 规格/净含量 |  | 已确认 / 待确认 |
| 包装形态 |  | 已确认 / 待确认 |
| 价格带 |  | 已确认 / 待确认 |

## 市场定位

| 字段 | 内容 | 状态 |
|------|------|------|
| 目标人群 | 待确认 | 已确认 / 待确认 |
| 销售渠道 | 待确认 | 已确认 / 待确认 |
| 竞品参考 | 待确认 | 已确认 / 待确认 |

## 项目目标

| 类型 | 内容 | 状态 |
|------|------|------|
| 商业目标 | 待确认 | 已确认 / 待确认 |
| 包装目标 | 待确认 | 已确认 / 待确认 |
| 成功指标 | 待确认 | 已确认 / 待确认 |

## 品牌调性

| 字段 | 内容 | 状态 |
|------|------|------|
| 关键词 | 待确认 | 已确认 / 待确认 |
| 喜欢的方向 | 待确认 | 已确认 / 待确认 |
| 不喜欢的方向 | 待确认 | 已确认 / 待确认 |

## 设计范围

1.
2.
3.

## 必须项

| 项目 | 内容 | 状态 |
|------|------|------|
| 必须出现的文案 | 待确认 | 已确认 / 待确认 |
| 固定结构 | 待确认 | 已确认 / 待确认 |
| 合规 | 待确认 | 已确认 / 待确认 |
| 素材授权要求 | 待确认 | 已确认 / 待确认 |
| 样品验收要求 | 待确认 | 已确认 / 待确认 |

## 预算与时间线

| 项目 | 内容 |
|------|------|
| 包装预算 |  |
| 礼盒预算 |  |
| 单 SKU 成本上限 |  |
| 首发批量预估 |  |
| 供应商状态 | 未触达 / 初步接触 / 已确认能力 / 已报价 |
| 目标上市 |  |

## 合规、授权与验收责任

| 项目 | 负责人/状态 |
|------|-------------|
| 合规/标签负责人 |  |
| 素材授权负责人 |  |
| 样品验收负责人 |  |
| 食品接触材料状态 | 不适用 / 待供应商确认 / 已确认 |
| 白样验收状态 | 未开始 / 待验收 / 通过 / 有条件通过 / 不通过 |
| 彩样/合同样验收状态 | 未开始 / 待验收 / 通过 / 有条件通过 / 不通过 |

## 风险

| 风险 | 说明 |
|------|------|
|  |  |

## 待确认问题

| 问题 | 影响 | 负责人/来源 |
|------|------|-------------|
|  |  |  |
""",
}


def read_template(root: Path, rootless_path: str) -> str:
    template = root / rootless_path
    if template.exists():
        return template.read_text(encoding="utf-8-sig")
    return FALLBACK_TEMPLATES[rootless_path]


def inject_project_name(content: str, project_name: str) -> str:
    """把模板中的项目名称占位行替换为实际名称。"""
    updated = content.replace("- 项目名称：", f"- 项目名称：{project_name}", 1)
    if updated != content:
        return updated
    return content.replace("| 项目名称 |  |", f"| 项目名称 | {project_name} |", 1)


def seed_file(root: Path, project_dir: Path, project_name: str, template_path: str, destination: str, dry_run: bool) -> None:
    target = project_dir / destination
    content = read_template(root, template_path)
    seeded = inject_project_name(content, project_name)
    print(f"  写入文件  {target.relative_to(root)}")
    if not dry_run:
        target.write_text(seeded, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="初始化 Packaging OS 标准项目目录。")
    parser.add_argument("project_name", help="项目名称，将作为目录名使用")
    parser.add_argument("--root", default=None, help="仓库根目录（默认自动推断）")
    parser.add_argument("--dry-run", action="store_true", help="只打印路径，不实际创建")
    args = parser.parse_args()

    script_path = Path(__file__).resolve()
    root = Path(args.root).resolve() if args.root else script_path.parents[4]

    project_dir = root / "Workspace" / "Projects" / args.project_name

    if project_dir.exists():
        print(f"错误：目录已存在 → {project_dir}", file=sys.stderr)
        print("如需重新初始化，请先手动删除或重命名现有目录。", file=sys.stderr)
        return 1

    print(f"项目根目录：{project_dir}")
    print(f"模式：{'dry-run（不创建文件）' if args.dry_run else '实际创建'}")
    print()

    # 创建目录
    for rel in DIRS:
        target = project_dir / rel
        print(f"  创建目录  {target.relative_to(root)}")
        if not args.dry_run:
            target.mkdir(parents=True, exist_ok=True)

    # 写入项目启动模板包
    for template_path, destination in STARTER_FILES:
        seed_file(root, project_dir, args.project_name, template_path, destination, args.dry_run)

    print()
    if args.dry_run:
        print("dry-run 完成，未实际创建任何文件。")
    else:
        print(f"项目初始化完成：{args.project_name}")
        print("已生成项目启动模板包：")
        print("- 00_Project_Control/project-memory-card.md")
        print("- 00_Project_Control/project-tracker.md")
        print("- 03_Design/02_Assets/asset-register.md")
        print("- 03_Design/02_Assets/AI_Concepts/")
        print("- 03_Design/04_Production/supplier-brief.md")
        print("- 03_Design/06_Proof_Record/compliance-review.md")
        print("- 03_Design/06_Proof_Record/sample-acceptance-record.md")
        print("- 03_Design/06_Proof_Record/proofing-record.md")
        print("- 03_Design/01_Working/decision-log.md")
        print("- 01_Brief/brief-decomposition.md")
        print("- 01_Brief/packaging-brief.md")
        print("下一步：先补项目卡和 brief，再运行 packaging-os 开始项目。")

    return 0


if __name__ == "__main__":
    sys.exit(main())
