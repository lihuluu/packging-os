# 会话启动规则

## 目标

用一条 Claude Code 可调用的脚本，把批量知识整理前的重复准备动作自动完成。

## 自动准备范围

启动会话时，脚本应自动更新：
- `coverage/project-knowledge-coverage.md`
- `queue/knowledge-capture-inbox.md`
- `current/current-review-session.md`
- `current/current-review-log-draft.md`

脚本只读取正式项目文档，不读取 `.tmp.*`、`.DS_Store` 等临时或运行噪音文件。

## 不自动处理的部分

以下内容仍保留给 Claude 或用户判断：
- 项目级 `knowledge-synthesis.md` 的具体结论
- 共享知识的去重、冲突判断和合并
- 工作区级 `workspace-knowledge-digest.md` 的最终内容
- 正式历史日志的结案版本

## 优先级输出要求

- `Missing Synthesis` -> `P1`
- `Synthesis Created` -> `P2`
- `Ready` -> `P2`
- `Low Signal` -> `P3`
- `Done` 不进入待处理队列

## 启动后的人类动作

1. 阅读 `current/current-review-session.md`
2. 从 `queue/knowledge-capture-inbox.md` 顶部项目开始
3. 处理完后更新 `workspace-knowledge-digest.md`
4. 把 `current/current-review-log-draft.md` 结转成正式历史日志到 `history/`
