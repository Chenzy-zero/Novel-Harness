# 小说项目起步说明

本目录是 Novel Harness Project Starter。压缩包解压后，这份文件会出现在小说仓库根目录。

## 快速开始

1. 在支持 Agent Skills 的 Agent 中打开本仓库。
2. 让 Agent 读取 `AGENTS.md` 和 `workflow.md`，然后使用 `novel-init`。
3. 如果 Agent 没有自动发现 Skill，请让它读取 `.agents/skills/novel-init/SKILL.md`。
4. 先与作者讨论并确认设定；Gate B 通过前不要写正式正文。

三个 Skill 位于 `.agents/skills/`。模板路径均相对于本仓库根目录；本项目不需要运行 Novel-Harness 工具仓库里的 `install.py`。

## 放入已有仓库

如果目标仓库已有文件，请先把压缩包解压到临时目录，再逐项合并缺少的文件；遇到同名文件时保留目标仓库版本并人工比较。不要直接覆盖已有小说内容或设定。

`chapters/` 用于正式章节。开始写正文前先完成 Gate B，并依据 `templates/chapter-contract.md` 维护章节契约。
