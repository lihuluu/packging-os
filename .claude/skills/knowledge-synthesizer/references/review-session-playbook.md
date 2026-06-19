# 知识整理会话操作手册

## 目标

把一次 Claude Code 的批量知识整理，固定成可重复执行的会话，而不是临时拼凑动作。

## 推荐会话顺序

1. 运行 `.claude/skills/knowledge-synthesizer/scripts/get_knowledge_coverage.py`
2. 运行 `.claude/skills/knowledge-synthesizer/scripts/build_knowledge_review_packet.py`
3. 阅读 `Workspace/Knowledge/Operations/current/current-review-session.md`
4. 根据优先级处理项目级 `knowledge-synthesis.md`
5. 更新：
- `Workspace/Knowledge/Operations/coverage/project-knowledge-coverage.md`
- `Workspace/Knowledge/Operations/queue/knowledge-capture-inbox.md`
- `Workspace/Knowledge/Library/workspace-knowledge-digest.md`
6. 把本轮结果记入 `Workspace/Knowledge/Operations/history/`

## 会话产物

每轮至少应有：
- 一个当前会话包：`current/current-review-session.md`
- 一个工作区汇总：`workspace-knowledge-digest.md`
- 一个历史记录：`history/YYYY-MM-DD-knowledge-review.md`

## 优先级规则

- `P1`：已有复盘但没有知识沉淀
- `P2`：文档完整，适合开始沉淀，或已有 `knowledge-synthesis.md` 但仍需补证据
- `P3`：低信号，先观察
- `Done`：已完成，只在有重大变化时重开

## 扫描边界

- 会话包只推荐正式项目文档，不列出 `.tmp.*`、`.DS_Store` 等临时或运行噪音文件。

## 会话结束前检查

- 覆盖表是否更新
- 收件箱是否移除已处理项目
- 工作区汇总是否只保留本轮变化
- 是否记录了下一轮建议
