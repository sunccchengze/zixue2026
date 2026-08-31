# MEMORY_SYSTEM · 数理方程科研式学习

> 参照概率论项目记忆系统（6引擎架构）为本学科定制。新会话开局必读本文件夹。

## 目录结构

```
数理方程/
├── memory/
│   ├── MEMORY_SYSTEM.md   本文件：架构+接入协议
│   ├── HANDOFF.md         交接总账本（永远最新：进展/下一句/判卷预案/会话记录）
│   ├── LEARNINGS.md       学习画像：偏好|卡点|有效讲法|知识背景
│   ├── ERRORS.md          判例库：通用红线+本学科判例
│   ├── PROGRESS.md        课题台账（⬜/🟡/✅）
│   └── drill-ledger/      间隔重复账本：index.md + topics/topicNN-*.md
├── 大师天团/              思维视角蒸馏（诚实声明）
├── 科研式学习路线图.md    12课题地图
├── 资料映射.md            课题 ↔ 教材页码/习题
├── 科研式学习方法论.md    验收标准/报告结构
└── 课题NN-*/              每课题开题简报+报告+公式卡PNG
```

## 新会话接入协议

1. 读 `HANDOFF.md` → 知道卡在哪、下一句问什么
2. 扫 `LEARNINGS.md` + `ERRORS.md` → 避免踩旧坑、复用有效讲法
3. 查 `PROGRESS.md` + `drill-ledger/index.md` → 课题进度+到期卡片，到期卡优先
4. 开场不重复自我介绍，直接从HANDOFF下一句继续

## 6引擎落地

| 引擎 | 落地 |
|---|---|
| self-improving-agent | 被用户纠正/新有效讲法 → 写 LEARNINGS.md |
| three-layer-memory | L1=对话临时；L2=ERRORS判例；L3=PROGRESS+drill长期 |
| memory-entropy | 每5-8轮合并LEARNINGS同根因条目，>150行清理 |
| memory-evaluator | 审报告前查ERRORS，旧坑预警 |
| precedent-memory | ERRORS每条带红线方法 |
| learning-system-skill | 本文件总调度 |

## 账本卡片表（简化FSRS）

`| # | concept | S | D | last | due | flags | history |`

- 新卡：Again S=1.0 / Hard 1.5 / Good 3.0 / Easy 6.0，初始 D=3
- 复习：Hard 1.4 / Good 2.2 / Easy 3.0 微调；Again → S=max(1.0,S×0.3) 且 D+1；flags: cw=自信错, leech=4次Again需换角度重教
- 单次新卡 ≤7张，到期卡优先
- 会话内重考隔3轮换表面形式，最终档为准

## 与总纲关系

本文件为 `skills/科研式学习导师/SKILL.md` §3 的学科化实现，服从用户硬偏好（批量提问/跳过审阅/生图PNG/手写公式卡/提速/语音容错/发现式学习）。
