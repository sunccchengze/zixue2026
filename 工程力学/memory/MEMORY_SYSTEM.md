# 记忆系统 · 工程力学科研式学习项目

> 参照共享总纲 `skills/科研式学习导师/SKILL.md` §3 的固定结构，为本学科定制。
> 新会话的我，开局第一步必须读完这个文件夹，才能做到"零损耗接力"。

## 目录结构

```
工程力学/memory/
├── MEMORY_SYSTEM.md      本文件：架构说明 + 新会话接入协议
├── HANDOFF.md            交接总账本：现在进展到哪一步、下一步做什么（最重要，永远最新）
├── LEARNINGS.md          本学科学到的：用户卡点、有效讲法（通用硬偏好在 probability/memory/LEARNINGS.md 单点维护）
├── ERRORS.md             判例库：通用红线（继承）+ 本学科用户判例
├── MEMORY.md             当前理解主账本：核心直觉+预测→打脸→修正日志
├── PROGRESS.md           课题台账：每个课题的状态（⬜/🟡/✅）
└── drill-ledger/         drill-me 间隔重复卡片账本
    ├── index.md
    └── topics/
```

## 新会话接入协议（下一个我必须做的事）

1. 先读本学科 `_开局指令-给新会话Agent.md`（唯一入口，含必读清单与第一问）；
2. 读 `memory/HANDOFF.md`——了解上次卡在哪、下一步该问什么；
3. 扫共享 `probability/memory/LEARNINGS.md`（用户画像单点维护）+ 本学科 `memory/LEARNINGS.md`；
4. 读 `probability/memory/ERRORS.md` 的"通用红线"节 + 本学科 `memory/ERRORS.md` 用户判例；
5. 查 `memory/PROGRESS.md` 与 `memory/drill-ledger/index.md`（到期卡优先）；
6. 开场不重新自我介绍、不重讲规则，直接从 HANDOFF 的"下一句"继续。

## 六个引擎在这里怎么落地

| 引擎 | 落地 |
|---|---|
| self-improving-agent | 每次你被我问倒/纠正我的讲法，写入本学科 `LEARNINGS.md`；通用偏好写回共享 LEARNINGS |
| three-layer-memory | L1=当前对话；L2=`ERRORS.md` 判例；L3=`PROGRESS.md`+`drill-ledger` |
| memory-entropy | 定期（每 5-8 次会话）清理过时条目，同根因合并 |
| memory-evaluator | 审报告前先对照 `ERRORS.md` 自查：旧坑不能让你再掉 |
| precedent-memory | 每条误区即判例，之后直接引用判例名 |
| learning-system-skill | 本文件——调度以上文件的读写时机 |

## 记忆熵降噪规则

- 单文件超过约 150 行做一次合并（同根因合并，伯乐原则）；
- 只记**可迁移模式**，不记流水账。
