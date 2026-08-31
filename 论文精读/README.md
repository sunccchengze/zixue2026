# 论文精读 · 学科入口

> 2026-08-31 开设的新学科。不同于 `probability/` 那种"教材制"学科，本学科是**论文制**：
> 一次只啃一篇论文，逐节读透，产物是可复述的理解、可批判的判断、可执行的改进清单。
>
> 方法论来源（两处，已合流）：
> 1. 本仓库教学法总纲 `skills/科研式学习导师/SKILL.md`（批量提问/打脸链路/记忆系统/大师天团/一页报告）；
> 2. 用户 `-SKILL-` 仓库 `arena/01a048e7-skill` 分支
>    `skills/core/zixue2026-expanded/references/tracks/track-paper-aso/`（12 会话论文精读计划 + 论文精读导师开局指令）。
>
> **冲突时以本仓库 `AGENTS.md` 与总纲为准**（回合级 push、批量提问、跳过逐篇审阅等硬规则）。

---

## 一、当前在啃的论文

| 项 | 内容（**均已核对 PDF 实物**） |
|---|---|
| 标题 | Machine Learning in Aerodynamic Shape Optimization |
| 作者 | Jichao Li (NUS 机械系)、Xiaosong Du、Joaquim R. R. A. Martins (U Michigan 航空航天系) |
| 文件 | `materials/Machine learning in aerodynamic shape optimization.pdf` |
| 页数 | **103 页**（正文 1–68，参考文献 69–103） |
| 图数 | **47 幅**（索引见 `materials/图表索引.md`） |
| 版本 | LaTeX 预印本，creationDate 2022-12-05；上游称 arXiv:2202.07141 |
| 全文文本 | `materials/论文全文-提取文本.md`（PyMuPDF 提取，按页打标记，供检索） |
| 章节页码 | `资料映射.md`（由 PDF 书签直读，**与上游指南目录有 4 处出入，已纠正**） |

## 二、文件地图

```
论文精读/
├── README.md                      ← 你在这里
├── _开局指令-给新会话Agent.md      新会话第一步读这个
├── 论文精读方法论.md               打脸链路五步 / 提问与解释策略 / 验收五项 / 一页报告
├── 资料映射.md                     章节 ↔ PDF页 ↔ 会话（含与上游指南的差异表）
├── materials/
│   ├── *.pdf                      唯一权威资料源
│   ├── 论文全文-提取文本.md         检索用（34万字符）
│   └── 图表索引.md                 47 幅图的图号↔页码↔图题↔所属会话
├── memory/
│   ├── MEMORY_SYSTEM.md            记忆架构 + 开局协议
│   ├── HANDOFF.md                  交接总账本（永远最新，含"下一句该问什么"）
│   ├── MEMORY.md                   论文理解主账本（预测/打脸/修正三段式）
│   ├── LEARNINGS.md                本学科学习画像
│   ├── ERRORS.md                   判例库 + 导师红线
│   ├── PROGRESS.md                 12 会话台账
│   └── drill-ledger/index.md       间隔重复账本（术语卡）
├── 大师天团/                       多视角提问（候选人已列，待用户确认后蒸馏）
└── 论文01-ML气动外形优化/
    ├── 精读路线图.md               12 次会话计划（按真实章节页码重排）
    ├── 开题简报.md                 背景 / 研究问题 / 攻关线索 / 里程碑 / 交付物
    └── 会话01-全景扫描/            每次会话一个文件夹
```

## 三、和上游指南的三个关键差异（诚实记账）

1. **目录不符**：上游 `track-paper-aso/README.md` 写的"§2.2 Parameterization / §2.3 Aerodynamic Analysis /
   §2.4 Optimization"在本 PDF 中**不存在**——§2 只有 2.1 General Process 和 2.2 Existing Challenges。
   参数化实际在 §4.1.1，气动分析在 §4.2，优化在 §4.3。会话计划已按实物重排。
2. **神经网络位置不符**：上游把 CNN/RNN/LSTM/传统代理模型都塞进"§3.1 监督学习"；
   实物 §3.1 只有 KNN/SVM/决策树与随机森林/传统代理模型，**神经网络全部在 §3.5**（含 CNN/RNN/AE/GAN/SOM/PINN）。
3. **用户背景待核**：上游 `agent-opening.md` 断言用户是"西安交通大学风电方向研究生，
   在做 turbine-blade-ai-platform（PyTorch 残差代理 + NSGA-II + NASA Rotor 37 + 74 维设计空间）"；
   本仓库 `probability/memory/LEARNINGS.md` 记录的是"数学底子偏基础（高中/大一水平）"。
   **两者矛盾，尚未向用户核实。** 会话01 的校准访谈第一问就是问这个。核实前，
   所有"连接你的项目"环节一律以**假设**标注，不写进 MEMORY.md 当事实。

## 四、开局协议（照抄总纲 §0）

1. 读仓库根 `AGENTS.md`（回合级 push 是最高优先级）；
2. 读 `论文精读/memory/HANDOFF.md`；
3. 扫 `memory/LEARNINGS.md` + `memory/ERRORS.md`；
4. 查 `memory/PROGRESS.md` 与 `memory/drill-ledger/index.md`，**先清到期卡**；
5. 从 HANDOFF 的"下一句该问什么"继续，不重新自我介绍。
