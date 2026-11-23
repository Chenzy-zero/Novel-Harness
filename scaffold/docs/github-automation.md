# GitHub 自动化 V0.2

GitHub API 操作通过 `scripts/github_sync.py` 共享，三个 Skill 只负责决定何时调用，不复制 API 逻辑。

## 准备
- Python 3.9+、git、可访问 GitHub API。
- `gh auth login` 或设置 `GH_TOKEN` / `GITHUB_TOKEN`，令牌需有目标仓库 Issues 写权限。
- 默认从 `origin` 推断 `owner/repo`；必要时设置 `NOVEL_GITHUB_REPO`。

## 操作
```bash
python3 scripts/github_sync.py bootstrap --dry-run
python3 scripts/github_sync.py bootstrap
python3 scripts/github_sync.py reconcile
python3 scripts/github_sync.py sync --dry-run
python3 scripts/github_sync.py sync
```

`bootstrap` 仅创建缺失的 `novel:arc/beat/char/thread/audit` Labels；Issue 表单由仓库的 `.github/ISSUE_TEMPLATE/` 提供。
`sync` 从 `state/github-issues.json` 读取记录；每条记录必须含 `id`、`title`、`path`，可选 `description`。稳定 ID 格式 `ARC-xxx` 等。通过 Issue 正文隐藏标记匹配远端 Issue，重复运行不会重复创建；远端重复 ID 会拒绝执行。删除记录**不会删除远端 Issue**。

示例：
```json
[
  {"id":"ARC-001","title":"第一卷主线","path":"outline/arcs/arc-001.md","description":"规划中的剧情弧"}
]
```

**限制与安全边界：** V0.2 仅做 Label 初始化和 Issue 标题/正文同步，不自动维护文档中的反向 URL、不自动设置 GitHub Projects、Milestones、子 Issue，也不自动合并 PR。远端 Issue 正文由同步器管理，人工补充内容应写在仓库 canonical 文档中；若人工直接编辑 Issue 正文，下一次同步可能覆盖修改。发布前须人工确认 `reconcile` 和双向链接，且不能把此工具当作完整 Gate C。API 失败会以非零状态退出，不得清空 `pending_issue_sync`。
