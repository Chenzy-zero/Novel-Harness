---
name: novel-init
description: Initialize and collaboratively define a new long-form novel project. Use this whenever a user wants to start a novel, discuss premise, worldbuilding, genre, protagonist, tone, characters, world rules, or create a reusable fiction repository; grill the author before writing canonical facts or any chapters.
---
# Novel Init：初始化与作者共创

从仓库根目录读取 `AGENTS.md`、`workflow.md`、`project/brief.md`、`project/questions.md`、`docs/grilling.md`，严格遵循 Gate A。

1. 读取已有作者确认信息与决策，不重复提问、不从仓库名称猜题材。
2. 标记所有内容为 APPROVED / PROPOSED / DRAFT / BLOCKED。列出主题、主角、目标、障碍、代价、规则、视角、语气、预计篇幅、结局方向的缺口。
3. 先提 2–4 个重要的、彼此相关的问题；每个重要悬而未决问题给出选择、读者吸引点、创作成本和建议，不擅自选定。
4. 作者明确批准后才填 `project/brief.md`、`bible/world.md`、角色/势力卡、`project/decisions.md`；每个角色应有稳定ID、基本生平、性格驱动、关系、状态/情绪、知识/任务状态。
5. 对跨章节需要追踪的 ARC、CHAR、THREAD 建 GitHub Issue，包含文档路径并反向链接；若暂时没有 API 权限，记录阻塞，不伪称成功。
6. 输出：“目前确定的创作契约”“候选设定”“待作者决策”“距离 Gate B 还欠什么”。
7. 在 Gate B 获批前禁止写任何正式正文；调用 `novel-outline` 继续规划。

### 兼容
本 Skill 为 Agent Skills 标准文档，可在其他小说仓库重用；所有路径相对小说仓库根目录，不硬编码仓库名。无 GitHub 权限时可做讨论与草稿，但不可声称已经同步 Issue。

### GitHub 初始化（V0.2）
在作者允许使用 GitHub 且仓库已经配置 origin 后，先阅读 `docs/github-automation.md`，执行 `python3 scripts/github_sync.py bootstrap --dry-run` 预检，再执行 `python3 scripts/github_sync.py bootstrap` 创建缺失 Labels。Issue 模板已由 `.github/ISSUE_TEMPLATE/` 提供。初始化创作资料后，将需追踪的 ARC、CHAR、THREAD 等条目以稳定 ID 写入 `state/github-issues.json`，对应文件必须先存在；执行 `reconcile` 检查差异，确认后执行 `sync`。任何失败必须报告并记录 `sync_pending`，不得称 GitHub 已同步。不要将 Issue 的创建当作作者对剧情的批准。
