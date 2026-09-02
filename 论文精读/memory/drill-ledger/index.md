# DRILL LEDGER · 间隔重复账本（论文精读）

> 简化 FSRS。规则见 `../MEMORY_SYSTEM.md` §三。
> **到期卡优先于新内容**；单次新卡 ≤7；术语卡必带记忆锚三件套与页码。

## 卡片总表

| # | concept | p. | S(days) | D(1-5) | last | due | flags | history |
|---|---|---|---|---|---|---|---|---|
| — | （账本为空，等会话01 判卷后建第一批卡） | — | — | — | — | — | — | — |

## 到期队列

（无）

## 计划中的第一批卡（会话01–02 判卷后建，≤7 张）

| 候选术语 | 页码 | 为什么值得建卡 |
|---|---|---|
| ASO（气动外形优化） | p3 | 全篇主语 |
| adjoint method（伴随方法） | p3 | 理解"为什么还需要 ML"的前提 |
| design variable / parameterization | p4–5 | 高维问题的根源 |
| surrogate model（代理模型 / metamodel） | p4 | ML 介入的主要入口 |
| XDSM（扩展设计结构矩阵） | p5 | Fig.1 的读图法，读不懂图就读不懂流程 |
| two compounding challenges（两个复合挑战） | p5 | 高计算成本 × 高维设计空间 |
| PINN（物理信息神经网络） | p4, §3.5.8 | 作者的最终押注方向 |

## flags 说明

- `cw` = confident-wrong：自信却错（黄金教学点）
- `leech` = 累计 4 次 Again：换角度重教，不再重考

---
*最后更新：2026-08-31*
