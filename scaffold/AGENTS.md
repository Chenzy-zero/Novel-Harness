# AGENTS.md — 小说创作 Agent 入口

本文件适用于 Codex / Claude Code / OpenCode 等可读取仓库文件的 Agent。

## 优先级
用户本轮明确要求 > 已确认的 `project/brief.md` > `workflow.md` > `bible/` 和 `outline/` 的已批准正史 > `state/` / 最近 handoff > GitHub Issues 当前镜像 > Agent 的推测。

任何冲突：**停止改动受影响范围**，列出矛盾、证据路径、最小修复选项，向作者 grilling。不得“合理脑补”为既成事实。

## 每次开始工作都必须执行
1. 从仓库根目录读取 `workflow.md` 和 `project/brief.md`。
2. 读取 `state/current.md`；按编号查找最近一期 `handoffs/`（若不存在，应确认是新项目）。
3. 定位当前任务涉及的 `bible/`、`outline/` 和相关人物 / 伏笔 / 知识台账。
4. 如有 GitHub 凭据，查询相应 GitHub Issues；无凭据时进入 ISSUE_SYNC_BLOCKED，需记录阻塞，不谎称同步完成。
5. 区分：已确认 / 草案 / 推断 / 未决。对重要未决选择先 grilling。

## 禁止行为
- 不在准备阶段写正文，不绕过前100章门禁。
- 不把总结文件或 Issue 视为事实真相；关键事实必须有正文/作者批准的证据锚点。
- 不因为模型上下文装不下而遗忘已经出现的角色、地点、规则、伏笔。
- 不未经作者批准修改核心设定、主线目的、主要人物命运、重大转折。
- 不每写一章就向 `main` 推送；正式批次完成30章、审核、同步、handoff后一次 push/PR。
- 不进行破坏性 git 操作来掩盖冲突，不替作者作开放结局的重大决策。

## 文件与状态
- 稳定标识：`CHAR-001` / `ARC-001` / `BEAT-001` / `THREAD-001` / `RULE-001`；不依赖 issue number。
- 新出场的重要 NPC 必须在其章节进入 canon **之前**建卡；在该章提交前将卡、状态、Issue 镜像同步。
- 人物卡包含动机、情绪、关系、当前地点、已知事实、正在推进的任务、状态变更史。
- 章节引用的时间、地理、组织、能力、物品必须与台账一致；有意不一致须标记为叙事误导而非遗忘。

## 必须使用的 Skills
- 初始化/核对设定：`.agents/skills/novel-init/SKILL.md`
- 总纲 / 30-100章规划：`.agents/skills/novel-outline/SKILL.md`
- 任何续写/回顾/状态更新：`.agents/skills/novel-continue/SKILL.md`

## 交付
列明章节区间、字数、校验结果、角色与伏笔状态变动、commit SHA、Issue 同步结果、handoff 路径和所有仍未解决的 blocker。没验证的步骤必须写“未完成”。
