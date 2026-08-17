# 记忆系统 · 复变函数与积分变换 科研式学习项目

> 参照 `skills/科研式学习导师/SKILL.md`（教学法总纲）与概率论项目的成熟骨架，为**这个项目**
> 量身定制。新会话的我，开局第一步必须读完这个文件夹，才能做到"零损耗接力"——
> 不用用户重新交代一遍背景。

## 目录结构

```
复变函数与积分变换/memory/
├── MEMORY_SYSTEM.md      本文件：架构说明 + 新会话接入协议
├── HANDOFF.md            交接总账本：现在进展到哪一步、下一步做什么（最重要，永远最新）
├── LEARNINGS.md          本学科学习画像（用户全科画像单点维护于 probability/memory/LEARNINGS.md）
├── ERRORS.md             判例库：通用红线 + 本学科用户判例（每条带红线）
├── PROGRESS.md           14课题进度台账：每个课题的状态（未开始/攻关中/已验收）
└── drill-ledger/         drill-me式间隔重复卡片账本（一个课题一个文件）
    ├── index.md
    └── topics/
```

## 新会话接入协议（下一个我必须做的事）

1. 先读本学科 `_开局指令-给新会话Agent.md`（若有），再读 `HANDOFF.md`——了解上次卡在哪、下一步该问什么。
2. 扫一眼 `LEARNINGS.md`、`ERRORS.md` 与 `probability/memory/LEARNINGS.md`（用户画像单点）——
   避免用已经验证"没用"的讲法，避免踩踩过的坑。
3. 查 `PROGRESS.md`——知道现在在14课题地图的第几站。
4. 查 `drill-ledger/index.md`——看有没有"到期该复习"的旧知识点，优先处理（间隔重复的核心原则：
   欠账的记忆优先，新内容其次）。
5. 开场不用重新自我介绍或者重复讲过的规则，直接从"接着上次"的地方问问题。

## 六个引擎在这里怎么落地

| 引擎 | 在复变项目里的落地 |
|---|---|
| self-improving-agent | 每次用户被问倒/纠正讲法，写入 `LEARNINGS.md`（复变专属节）并回写概率论总画像 |
| three-layer-memory | L1=当前对话临时上下文；L2=`ERRORS.md`判例；L3=`PROGRESS.md`+`drill-ledger`长期知识状态 |
| memory-entropy | 定期（每5-8次对话）清理 `LEARNINGS.md` 里过时条目，保持精炼 |
| memory-evaluator | 每次审报告前，先对照 `ERRORS.md` 自查——旧坑不能让他义正词严掉第二次 |
| precedent-memory | `ERRORS.md` 里的每条"误区"就是判例，之后遇到同类问题直接引用判例名 |
| learning-system-skill | 本文件——调度以上5个文件的读写时机 |

## 记忆熵降噪规则（防止文件无限膨胀）

- `LEARNINGS.md` / `ERRORS.md` 单文件超过约150行时，做一次合并（同根因的条目合并成一条，
  参考"伯乐原则"——先搜有没有同根因的旧条目，别重复记）。
- 只记录**可迁移的模式**，不记流水账。

## 与 drill-me 间隔重复账本的关系

`drill-ledger/` 是**知识点级**的细粒度记忆（哪个概念哪天该复习），
`PROGRESS.md` 是**课题级**的粗粒度记忆（14课题走到哪了），
两者一细一粗，共同构成"你到底掌握到什么程度"的完整画像。
