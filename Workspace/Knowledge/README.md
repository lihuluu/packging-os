# Knowledge

这个目录现在只做两件事：

- `Library/`：给你看的知识库，强调摘要、规则和结构化阅读。
- `Operations/`：给 Claude Code 和脚本维护的运行文件，强调覆盖率、队列、会话和日志。

## 你平时看哪里

优先看 `Library/`：

1. `Library/knowledge-dashboard.md`
2. `Library/workspace-knowledge-digest.md`
3. `Library/decision-rules.md`
4. `Library/risk-signals.md`
5. `Library/process-updates.md`
6. `Library/category-insights.md`

## Claude Code 主要写哪里

主要写 `Operations/`：

- `Operations/coverage/project-knowledge-coverage.md`
- `Operations/queue/knowledge-capture-inbox.md`
- `Operations/current/current-review-session.md`
- `Operations/current/current-review-log-draft.md`
- `Operations/history/`

## Operations 分层

- `coverage/`：长期维护的覆盖状态与覆盖率快照。
- `queue/`：待处理知识沉淀队列。
- `current/`：当前这轮知识整理会话的工作文件。
- `history/`：已经完成的历史日志，只存归档结果。

## 使用原则

- 项目级沉淀先写在项目自己的 `05_Retrospective/knowledge-synthesis.md`。
- 跨项目可复用结论回写到 `Library/`。
- 会话准备、覆盖盘点、待处理队列和日志草稿由脚本维护在 `Operations/` 对应子目录下。
