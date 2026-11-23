# Novel Harness｜AI 长篇小说创作工程框架

> 一套面向 AI Agent 的长篇小说创作 Harness：将**设定共创、大纲规划、批量续写、人物与伏笔追踪、跨会话恢复、质量检查**组织成可复用的工作流。

**项目定位：** Novel Harness 是安装到小说仓库中的创作工程框架，而不是一本小说，也不是单纯的“一键生成小说”提示词。它参考软件工程中的需求基线、状态追踪、版本管理与质量门禁，让 Agent 在长篇创作过程中尽可能保持人物、剧情和世界规则的一致性。

> **当前状态：早期预览版。** 已有三个 Agent Skills、小说项目模板、Python 安装器、结构检查及基础 GitHub Issue 同步脚本。自动连续创作 30 章、Issue 双向状态同步、失败恢复与每 300 章审计尚未完成端到端验收；请勿将其视为成熟的无人值守创作系统。

## 目录

- [一、它解决什么问题](#一它解决什么问题)
- [二、工作原理](#二工作原理)
- [三、安装与快速开始](#三安装与快速开始)
- [四、从零开始写一本小说](#四从零开始写一本小说)
- [五、三个 Skill 的职责](#五三个-skill-的职责)
- [六、GitHub Issues 如何使用](#六github-issues-如何使用)
- [七、项目目录说明](#七项目目录说明)
- [八、校验、更新与注意事项](#八校验更新与注意事项)
- [九、当前实现情况与路线图](#九当前实现情况与路线图)

## 一、它解决什么问题

长篇小说不只是“不断生成下一章”。当作品达到数百章时，AI 容易出现：

- **设定漂移**：世界规则、能力上限或人物经历前后矛盾。
- **角色失忆**：忘记配角的身份、关系、情绪、目标及其已知信息。
- **剧情失控**：主线偏离、重要人物消失、伏笔迟迟不兑现。
- **跨会话断层**：换模型、换设备或重新打开会话后，无法可靠恢复进度。
- **交付不可追踪**：不知道某个设定是谁批准的、哪一章改变了角色状态。

Novel Harness 的思路是：**将小说事实、创作计划和任务状态持久化到仓库，并在每次创作时按需读取、更新和校验。**

## 二、工作原理

```text
作者提出创作目标 / 审批重大决策
              │
              ▼
        AI Agent（调度）
              │
     ┌────────┼─────────┐
     ▼        ▼         ▼
 novel-init  novel-outline  novel-continue
     │        │         │
     └────────┼─────────┘
              ▼
        小说 Git 仓库
   ┌──────────┼─────────────┐
   ▼          ▼             ▼
  bible/    outline/       state/
  正史设定   剧情规划        当前状态
   │          │             │
   └──────────┼─────────────┘
              ▼
   GitHub Issues（可选联网同步）
              │
              ▼
   校验 / handoff / Git 提交
```

**事实优先级：** 作者批准的设定与正式发布正文是权威依据；`state/` 是当前状态快照；`handoffs/` 是跨会话摘要；GitHub Issues 负责追踪任务与状态，不能擅自覆盖正史。详情参见安装到小说项目后的 `workflow.md`。

### 四个关键门禁

| 门禁 | 触发阶段 | 核心要求 |
| --- | --- | --- |
| Gate A | 初始化 | 与作者讨论并确认核心设定，未确认内容不得擅自写成正史 |
| Gate B | 正式开写前 | 前 100 章逐章简纲、前 30 章详细规划、主要人物与伏笔档案齐备 |
| Gate C | 每批 30 章 | 正文数量与字数、连续性、handoff、Issue 对账及交付检查 |
| Gate D | 每累计 300 章 | 全量检查主线、人物、时间线、伏笔、设定冲突和遗留问题 |

默认目标为**每章约 2000 汉字、每批 30 章**。这属于创作工作流约定，不代表现有版本已经具备稳定无人值守的批量写作执行器。

## 三、安装与快速开始

### 3.1 环境要求

- Git：用于克隆框架和管理小说仓库。
- Python 3.9 或更新版本：运行安装与校验脚本。
- 支持读取 Agent Skills 的 AI 编程/创作 Agent（如具备相应能力的 Codex、Claude Code 等）。不同工具的技能发现方式可能不同，请确认它能够读取小说仓库中的 `.agents/skills/`。
- **可选**：GitHub 账号、`gh` CLI 或 `GH_TOKEN` / `GITHUB_TOKEN`，用于 GitHub Issues 同步。

### 3.2 下载框架

目前代码位于开发分支 `feat/initial-harness`，在 PR 合并前需要显式切换：

```bash
git clone https://github.com/Chenzy-zero/Novel-Harness.git
cd Novel-Harness
git checkout feat/initial-harness
```

### 3.3 初始化一本新小说

将 `/path/to/my-novel` 替换成你的目标目录：

```bash
# 先查看会安装哪些文件，不实际写入
python3 scripts/install.py /path/to/my-novel --dry-run

# 确认后执行安装
python3 scripts/install.py /path/to/my-novel
```

安装器会将 `scaffold/` 中的目录和文件复制到目标位置；目标文件已经存在时，**默认跳过，不覆盖**。安装器不会自动执行 `git init`、创建远端仓库或调用 GitHub API。

### 3.4 将小说目录作为 Git 仓库

```bash
cd /path/to/my-novel

# 仅在该目录尚未初始化 Git 时执行
git init

# 验证模板结构
python3 scripts/validate_novel.py --mode structure
```

如要同步到 GitHub，请先自行创建小说仓库并配置 `origin` 远程地址。

### 3.5 在 Agent 中启动

使用 AI Agent 打开**小说仓库目录**，而不是 Novel-Harness 工具仓库，然后输入：

> 请阅读 AGENTS.md 和 workflow.md，使用 novel-init 初始化这本小说。先与我讨论题材、世界观、主角、故事冲突和篇幅，不要直接写正文。

如果 Agent 没有自动识别 Skill，可明确让它读取 `.agents/skills/novel-init/SKILL.md`。Skill 是否能够自动触发，取决于使用的 Agent 环境。

## 四、从零开始写一本小说

### 第一步：共创设定（novel-init）

Agent 会询问题材、读者定位、叙事视角、世界规则、主角目标、冲突、结局方向等，必要时给出多个方案及优缺点。

**你需要做的事：** 讨论、选择、修改并明确批准重要设定。

**主要产物：** `project/brief.md`、`project/decisions.md`、`project/questions.md`、`bible/` 中的世界与人物资料。

### 第二步：制定大纲（novel-outline）

Agent 根据已批准设定，拆解主线、分卷、剧情弧、关键事件，准备前 100 章逐章简纲和前 30 章详细章节契约。

**你需要做的事：** 审核主线方向、核心人物命运和重大反转。

**主要产物：** `outline/master.md`、`outline/first-100.md`、剧情弧与章节契约。

### 第三步：正式写作（novel-continue）

在完成 Gate B 后，可以要求：

> 继续写下一批 30 章。严格按照 workflow.md 执行，每章更新人物、关系、伏笔和事件状态，结束时生成累计 handoff 并检查 GitHub Issues。

设计中的每章流程是：**恢复上下文 → 读取章节契约 → 写草稿 → 校验因果与设定 → 更新状态 → 进入下一章**。

**重要：** 当前版本提供工作流规范与部分机械校验，不保证 Agent 能在单次会话中稳定完成 30 章，也不保证所有状态都能自动同步。

### 第四步：跨会话恢复

下次打开小说仓库时，让 Agent 读取 `state/current.md`、最新 `handoffs/`、相关人物和剧情资料，以及必要的正文证据，再继续写作。不要只依赖聊天历史。

### 第五步：周期性复盘

每累计 300 章，按照 Gate D 对主线偏离、角色状态、伏笔、知识差、时间线与设定一致性进行全量审计；涉及重大剧情修改时，先征求作者批准。

## 五、三个 Skill 的职责

| Skill | 什么时候使用 | 负责什么 |
| --- | --- | --- |
| `novel-init` | 新建小说、讨论设定 | 初始化创作资料、Grilling、作者审批、GitHub 基础配置 |
| `novel-outline` | 准备或调整大纲 | 主线规划、前 100 章、章节契约、剧情追踪 |
| `novel-continue` | 正式续写 | 逐章创作、状态更新、批次检查、handoff、复盘 |

三个 Skill 共同遵循 `workflow.md`。GitHub API 的具体操作由共享脚本处理，避免三个 Skill 各自重复实现。

## 六、GitHub Issues 如何使用

GitHub Issues 用于追踪**需要跨章节持续管理**的对象，而不是把每句话都变成 Issue。

| 类型 | 含义 | 例子 |
| --- | --- | --- |
| ARC | 剧情弧 | 第一卷的核心冲突 |
| BEAT | 关键剧情节点 | 主角首次发现某个秘密 |
| CHAR | 重要角色 | 配角的目标、关系与状态变化 |
| THREAD | 伏笔或悬而未决的线索 | 某个神秘物品的来历 |
| AUDIT | 审计与问题 | 第 300 章连续性复盘 |

### GitHub 初始化

在小说仓库中，完成 GitHub 登录并配置远端后：

```bash
# 预览需要创建的 Labels
python3 scripts/github_sync.py bootstrap --dry-run

# 创建缺失的 Labels
python3 scripts/github_sync.py bootstrap
```

### Issue 同步

将需要追踪的记录维护在 `state/github-issues.json`，每条记录包含稳定 ID、标题和对应的仓库文档路径。对应文件必须先存在。

```bash
# 只查看差异
python3 scripts/github_sync.py reconcile

# 预览写入
python3 scripts/github_sync.py sync --dry-run

# 实际创建或更新 Issue
python3 scripts/github_sync.py sync
```

同步器通过稳定 ID 查找已有 Issue，避免重复创建。**当前仅覆盖基础 Label 初始化和 Issue 标题/正文同步**；自动反向链接、完整状态迁移、冲突保护和可靠的失败重试仍待完善。同步失败时不能宣称发布门禁已通过。

更详细的说明位于 `scaffold/docs/github-automation.md`。

## 七、项目目录说明

### Novel-Harness 工具仓库

```text
Novel-Harness/
├── README.md                    # 本文档
├── scripts/
│   └── install.py               # 将框架安装到小说目录
├── tests/
│   └── test_install.py          # 安装器测试
├── scaffold/                    # 安装到小说仓库的模板
│   ├── AGENTS.md                # Agent 工作入口
│   ├── workflow.md              # 创作工作流和质量门禁
│   ├── .agents/skills/          # 三个小说 Skill
│   ├── project/                # 创作需求、决策与待决问题
│   ├── bible/                  # 世界观、角色、势力正史
│   ├── outline/                # 主线、分卷、章节规划
│   ├── state/                  # 当前状态、关系、知识、伏笔
│   ├── handoffs/               # 跨批次、跨会话交接
│   ├── reviews/                # 周期性全量复盘
│   ├── templates/              # 章节契约等模板
│   ├── scripts/                # 校验和 GitHub 同步工具
│   └── .github/                # Issue 表单等配置
└── .github/workflows/          # 框架自身的 CI
```

### 每本小说自己的仓库

安装完成后，每本小说维护独立的 `bible/`、`outline/`、`state/`、`chapters/`、`handoffs/` 和 Git 历史。

**不要把小说正文写进 Novel-Harness 工具仓库。** 这样框架可以独立升级，也不会把不同小说的世界观和人物状态混在一起。

## 八、校验、更新与注意事项

### 运行测试

在 Novel-Harness 工具仓库中：

```bash
python3 -m unittest discover -s tests -v
python3 scaffold/scripts/validate_novel.py --mode structure
```

在具体小说仓库中：

```bash
python3 scripts/validate_novel.py --mode structure
```

校验器还提供 `--mode gate` 和 `--mode batch --start 1`，但目前主要验证文件、审批标记、章节字数和部分状态字段，**不能代替人工剧情审查或远端 Issue 对账**。

### 更新已有小说项目

```bash
cd /path/to/Novel-Harness
git pull

python3 scripts/install.py /path/to/my-novel --dry-run
python3 scripts/install.py /path/to/my-novel
```

默认不会覆盖已有文件，因此适合首次安装，但**不是完整的版本升级或迁移机制**。对于已安装的旧版 Skill、脚本和模板，需要人工比较差异并合并。

`--force` 可以覆盖目标文件，但可能破坏小说仓库中的个性化配置和创作数据，使用前必须备份或提交 Git。

### 安全与使用边界

- 不要将 GitHub Token、账号密码等凭据提交到小说仓库。
- GitHub Issues 是追踪视图，不是覆盖正文或作者决策的权威数据源。
- 不要把未经作者批准的重大设定自动标记为 APPROVED。
- 网络失败、Issue 同步失败或章节不完整时，应保留进度并明确报告，不得虚报完成。
- 安装器不会自动创建 GitHub 仓库、发布 Release 或安装全局 CLI。

## 九、当前实现情况与路线图

| 能力 | 当前状态 |
| --- | --- |
| 三个 Agent Skills | 已提供 |
| 可复用小说模板 | 已提供 |
| Python 安装器 | 已提交，待完整验收 |
| 结构校验 | 已提供 |
| GitHub Label / Issue 基础同步 | 已提供，待真实联调 |
| 自动检查 100 章有效规划 | 待增强 |
| 稳定执行 30 章批次 | 待端到端验证 |
| Issue 双向状态和证据同步 | 待实现 |
| 中断恢复与可靠重试 | 待完善 |
| 每 300 章全量审计 | 已有规范，待验证 |
| 一键 CLI / `npx novel-harness init` | 规划中，尚不可用 |
| 自动版本升级与模板迁移 | 规划中 |

### 长期目标

让使用者只需要：

1. 安装 Novel Harness；
2. 在新小说仓库中运行初始化；
3. 与 Agent 确认设定和大纲；
4. 用“继续写下一批 30 章”驱动创作；
5. 由框架负责持久化、状态追踪、检查和可恢复交付。

**设计原则：作者决定故事，Agent 执行创作，仓库保存事实，工作流保证可追踪。**

---

本项目仍在开发中，欢迎通过 GitHub Issues 记录功能需求、缺陷和工程验收事项。
