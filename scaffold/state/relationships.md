# 人物关系图（有向边 / 知情差 / 情感状态）

## 建模
每条关系设 `REL-xxx`；`from_character` → `to_character`、态度（敌对/友好/利用/依赖/爱慕/未知，可多值）、信任度变化、公开/隐秘、关键事件、章节锚点。
关系**通常不单独开 Issue**；合并到人物卡的 `relationships` / GitHub CHAR Issue。只有跨篇章的重要关系转折才升格为独立 BEAT / THREAD Issue。

| REL ID | A | B | A对B态度 | B对A态度 | 最新变化章节 | 证据 |
|---|---|---|---|---|---|---|
