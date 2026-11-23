# GitHub Issues 数据模型 / 状态协议

## 为什么不把每个对象都建 Issue？
1000章可能出现成百上千个背景物件、路人、对话和小情绪。全都建单会淹没关键事件。
建议 **5类主要 Issue**（以标题前缀与表单区分）：

| 类别 | ID | 对应文件 | 何时创建 | 关闭时机 |
|---|---|---|---|---|
| 剧情弧（Epic） | ARC | `outline/arcs/ARC-xxx.md` | 主/重要支线正式列入大纲 | 弧线在 canon 中完结 |
| 剧情节点（Story/Task） | BEAT | `outline/beats/BEAT-xxx.md` | 有独立目标、完成条件、会改变状态 | 已兑现或经作者取消 |
| 重要角色（Entity） | CHAR | `bible/characters/CHAR-xxx.md` | 主角、重要NPC、反复登场的角色 | 离场且无后续义务；死亡不等于关闭 |
| 暗线/伏笔（Promise） | THREAD | `state/foreshadowing.md`，复杂项可单文件 | 对读者有承诺、需跨章追踪 | 兑现，或作者批准取消 |
| 审计/设定冲突（Audit） | AUDIT | `reviews/` 或 `project/questions.md` | 发现漏洞、全量复盘和重大风险 | 证据确认且复核通过 |

世界规则 `RULE`、势力 `FACTION`、关系 `REL`、事实 `FACT` 默认写文件不独立开 Issue；当它们触发跨章节风险/变更时新开 AUDIT/BEAT。

## GitHub层级关系
- **EPIC/ARC → STORY/BEAT**：用 GitHub 原生 sub-issues（客户端有权限则用）；否则使用正文 `parent: #号`、`tracked-by: #号` 的文本链接，禁止假称已建立原生父子关系。
- `BEAT` 可依赖其他 `BEAT`，用 `depends_on` 及 Issue URL。
- `CHAR`、`THREAD` 与 ARC/BEAT **横向链接**，不纳入父子，以免人物被单一剧情归属。
- 大规模使用 GitHub Projects 自定义 status / 当前章数可以作为可选可视化面板；它不是事实源。
- 推荐标签：`type:arc`、`type:beat`、`type:character`、`type:thread`、`type:audit`、`sync:pending`、`needs:author`。首次需确认 GitHub labels 已创建，否则不可声称标签生效。

## 状态域（两层分开）
GitHub Issue `open/closed` **仅**表达是否需继续追踪。
文件与 Issue 正文中独立维护业务状态：
- ARC：`proposed / planned / active / paused / completed / cancelled`
- BEAT：`planned / ready / in-progress / completed / blocked / cancelled`
- CHAR：`planned / active / offstage / missing / deceased / retired`；另有 `emotional_state`、`life_state`、`current_objectives`
- THREAD：`proposed / open / progressing / paid / deferred / cancelled`
- AUDIT：`open / investigating / resolved / waived`
不得以“关闭 Issue”自动推断死亡、反目或伏笔兑现。

## 关联字段与更新协议
每个 Issue 正文**必须**包含稳定 ID、`canonical_file`（仓库内相对路径 + GitHub 浏览链接）、当前业务状态、关联 ID、`last_changed_chapter`、最新事件证据/批准记录、下一个动作。对应文件保留 `issue` URL。台账中引用稳定ID。

更新动作顺序：
1. 生成拟议事实变更和正文证据，检测冲突、确认重大内容已经授权。
2. 更新本地对应正史/状态/台账；追加 event log（谁、章节、前/后状态、证据、变更批次）。
3. 更新 GitHub Issue body，并核对读取回执；记录成功时间或存 `sync_pending` 队列。
4. 重新读取双向链接和关键字段，对账；有未同步条目不得把批次合并到 main。
5. Issues 的实时更新时间只是镜像写入时间，**不是剧情时间**。回溯修订需重算受影响章节之后的状态。

## GitHub API 限制
- connector 若仅支持普通 Issue 创建/更新，原生 sub-issue 绑定与自定义字段不一定可操作：应退化为可靠的 `#issue` 文本关系，绝不能“假同步”。
- Issue 与 git commit 不是跨系统原子事务，应用“先本地审查、后远端对账、失败保留 `sync_pending` 并阻塞”的补偿模式。
- 一次性路人不创建 Issue；后续升格重要 NPC 才补卡并按首次出场章补历史。
- 新重要角色在新章节正式发布前，必须建卡、建立 Issue、更新当前状态与关系。
