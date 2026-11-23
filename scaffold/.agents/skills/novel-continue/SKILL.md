---
name: novel-continue
description: Continue or revise a Git-versioned long-form novel safely. Use whenever asked to write the next 30 chapters, resume an interrupted writing session, update character/plot/foreshadowing state, maintain GitHub Issues, prepare cumulative handoffs, audit continuity, or review each 300 chapters. Follow workflow.md gates before any publication.
---
# Novel Continue：统一执行入口（必须读 workflow）

读取 `AGENTS.md`、`workflow.md`、`state/current.md`、最近 `handoffs/`、本批 `outline` 与相关 `bible`/`state` 台账。先探测工作区是否存在未完成草稿或 `sync_pending`；严禁盲目从最后章节号直接续写。

## 场景路由
- 尚未 Gate A/B：调用 `novel-init`/`novel-outline`，不要写正文。
- 正式续写：从 `last_published_chapter+1` 起连续 30 章。按章执行 contract→草稿→质检→事实提取→更新角色/线索/Issue；批次 Gate C 通过才发布。
- 中断恢复：先对比工作区文件、Git 状态、最新 handoff 和 Issue 同步日志，确定哪些是正式发布、哪些只是草稿。
- 修订：找出受影响事实与下游章节，回滚/重算状态，不仅修改一句话。
- 累计达到 300 的倍数：在当前30章发布前完成 Gate D 全量审查，重大偏航先获作者确认。

## 必须履行的文件和记录
- 章节：`chapters/0001-0030/0001.md` …… `0030.md`；每章目标约2000汉字，按 `scripts/validate_novel.py` 的规则计数。
- 状态：`state/current.md`、`state/foreshadowing.md`、`state/relationships.md`、`state/knowledge.md`、`state/timeline.md` 及角色/剧情卡。
- GitHub Issue：按 `docs/issue-model.md` 用稳定ID做双向关联；写入变更证据、情绪/关系/位置/任务状态；失败时挂 `sync_pending` 并阻塞发布。
- Handoff：`handoffs/0001-0030.md` 等，必须继承前一份累计 handoff + 本次正文事实；下一轮可以直接依赖它导航，但遇矛盾需核对正文。
- 发布：本批30章字数/连续性/Issue同步全通过，再提交一次批次 commit/push，输出 SHA、Issue结果、handoff路径；未通过不说“完成”。
- 达到300的倍数追加 `reviews/0001-0300.md` 等。

## 自检 / 有雾
- 运行 `python3 scripts/validate_novel.py --mode structure`（结构）。
- 准备开写先运行 `python3 scripts/validate_novel.py --mode gate`（100章门禁）。
- 写完30章后运行 `python3 scripts/validate_novel.py --mode batch --start N`（编号、篇幅、交接、同步）。
- **工具校验仅覆盖可机器判断的断言**；剧情审稿和人格连续性必须读 `references/chapter-audit.md`。
- 凡核心未决、设定冲突、人物重大变更，请依 `docs/grilling.md` grilling 并停在受影响章节前。

## 失败恢复
GitHub Issues 和 Git push 不构成原子事务。先做本地校验，再 Issue 同步对账，最后推送批次；若任何一步失败，保留证据和同步队列，不作虚假成功承诺。详见 `references/issue-sync.md`。

### GitHub 同步（V0.2）
每批发布前读取 `docs/github-automation.md`，维护 `state/github-issues.json`，执行 `python3 scripts/github_sync.py reconcile` 与 `sync`；核验双向链接和远端状态。该脚本只同步标题与正文，不负责章节证据、状态转换或 PR；这些仍由 Agent 按 `workflow.md` 执行，失败不得通过 Gate C。
