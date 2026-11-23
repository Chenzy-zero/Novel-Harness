# GitHub Issues 补偿式同步

Git commit 与 GitHub Issue PATCH 不保证原子性。每次状态事件拥有稳定 `event_id`（例如 `CH-0032-CHAR-004-1`），保证重复执行不会重复加同一事实。该事件写在对应人物卡事件日志，并写入 Issue 正文审计段落。

1. 写本地草稿与 event log，校验状态前后合法。
2. 读取 Issue 最新内容/更新时间，按 stable ID 核对路径，计算变更。
3. 补写相应 Issue 字段/日志；尽可能写 `event_id` 防止重试重复。
4. 重新读 Issue，确认 event_id 和最终状态一致。
5. 修改本地 `state/current.md` 的 `pending_issue_sync` 队列并留同步时间。
6. 冲突/限流/权限失败：记录异常和远端当前值，禁止自行覆盖作者/他人编辑；将事件转入 `sync_pending`；批次 Gate C 阻塞。
7. 若需要撤销已写 Issue 的草稿事务，以补偿事件注明原因并重算，而不是抹去历史。
8. 发布时再对账：角色、剧情弧、伏笔所有当前 Issue 状态必须与本地状态镜像一致；没访问权限不代表验证通过。
