---
name: novel-outline
description: Develop and validate a novel's master outline, volume arcs, plot beats, foreshadowing plans, character arcs, and chapter-by-chapter plans for the first 100 chapters. Use before drafting a novel, whenever plotting or restructuring, or when an author asks for sufficient material to sustain 100 chapters.
---
# Novel Outline：大纲/前100章规划

先读取 `AGENTS.md`、`workflow.md`、`project/brief.md`、`project/decisions.md`、`bible/world.md`、`outline/master.md` 以及已确认的角色设定；严格执行 Gate B。

1. 根据用户确认的创作契约提出全书主线、每卷驱动力、主角成长与代价、反派动机、阶段悬念。说明不同线路的利弊，重大选择先 grilling。
2. 为主要弧线创建 ARC 卡（`outline/arcs/`），拆分到带完成条件的 BEAT 卡（`outline/beats/`）；关联 CHAR/THREAD/知识差与预计章节窗口。
3. 建立 1–100 章的独立简纲：目标、障碍、推进事件、因果结果、角色、对应 ID、伏笔、章尾钩子。每10章小目标、每30章阶段转折。
4. 对 1–30 章逐章细化 Chapter Contract（参见 `templates/chapter-contract.md`），不写正式正文。
5. 检查100章中主线推进/支线回报比、人物设定一致性、规则成本、伏笔铺设及回收计划；不要用“100章占位”充数。
6. 文件与 GitHub ARC/BEAT/THREAD/CHAR Issues 对账，`sync_pending` 禁止通过 Gate B。
7. 把 Gate B 审核结果与阻塞问题清单给作者；**只有作者批准、且 `project/brief.md` 的 `planning_status: APPROVED` 与 `outline/first-100.md` 的 `coverage: 100/100` 同时满足，才能交付正式开写**。
8. 如需要变更主线、重要人物命运或能力边界，先记录候选并向作者 grilling，再改动获批的计划。

在回复中区分“已确认”“提案”“未决”，不会把小说大纲当成已发布事实。

### GitHub 追踪（V0.2）
需追踪的 ARC、BEAT、CHAR、THREAD 先写 canonical 文档，再更新 `state/github-issues.json`（稳定 ID、标题、相对路径、描述），按 `docs/github-automation.md` 运行 `reconcile` 与 `sync`。当前工具不自动回填 Issue URL，必须手工核对双向链接。未完成对账不可宣称 GitHub 同步完成。
