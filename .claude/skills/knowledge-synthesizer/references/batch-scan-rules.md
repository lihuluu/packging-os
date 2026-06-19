# 批量知识扫描规则

## 目标

让 Claude Code 在不依赖数据库的前提下，稳定完成多项目知识沉淀。

## 推荐扫描顺序

1. 运行 `.claude/skills/knowledge-synthesizer/scripts/get_knowledge_coverage.py`
2. 更新 `Workspace/Knowledge/Operations/coverage/project-knowledge-coverage.md`
3. 把缺少沉淀的项目写入 `Workspace/Knowledge/Operations/queue/knowledge-capture-inbox.md`
4. 优先处理：
   - 已有 `project-retrospective.md` 但没有 `knowledge-synthesis.md` 的项目
   - 已有 `knowledge-synthesis.md` 但仍在推进、需要后续补证据的项目
   - 最近更新过的项目
   - 高复用或高风险品类
5. 处理完项目级沉淀后，再更新共享知识文件和 `workspace-knowledge-digest.md`
6. 盘点时忽略 `.tmp.*`、`.DS_Store` 等临时或运行噪音文件。

## 项目状态判定

### Ready

满足以下条件之一：
- 有 `project-retrospective.md`
- 有多份阶段产出，且项目已经进入后期

### Missing Synthesis

有足够项目产出，但没有 `knowledge-synthesis.md`

### Synthesis Created

已有 `knowledge-synthesis.md`，但项目仍在推进、缺复盘或还会继续补证据

### Low Signal

只有少量文档，还不足以提炼稳定知识

### Done

已有 `knowledge-synthesis.md`，且共享知识已完成回写

## 工作区级输出

批量扫描时至少维护三个文件：
- `project-knowledge-coverage.md`
- `knowledge-capture-inbox.md`
- `workspace-knowledge-digest.md`

## 更新原则

- 先记录覆盖状态，再抽取知识
- 收件箱只保留真正待处理项
- 工作区级汇总只写本轮新增或变化明显的结论
- 同一轮不要重复回写同一条共享知识
