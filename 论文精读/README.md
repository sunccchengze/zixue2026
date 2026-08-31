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
| 出处 | Progress in Aerospace Sciences **134** (2022) 100849 · DOI 10.1016/j.paerosci.2022.100849 · arXiv 2202.07141 |
| 全文文本 | `materials/论文全文-提取文本.md`（PyMuPDF 提取，按页打标记，供检索） |
| 章节页码 | `资料映射.md`（由 PDF 书签直读，**与上游指南目录有 4 处出入，已纠正**） |

## 二、文件地图

```
论文精读/
├── README.md                      ← 你在这里
├── 12篇论文总规划.md               P01 综述 + P02–P12（按被引次数客观排序，含 DOI）
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
├── 大师天团/                       与他 turbine 仓库现有 13 大师内阁对齐（见该目录）
└── 论文01-ML气动外形优化/
    ├── 精读路线图.md               12 次会话计划（按真实章节页码重排）
    ├── 开题简报.md                 背景 / 研究问题 / 攻关线索 / 里程碑 / 交付物
    └── 会话01-全景扫描/            每次会话一个文件夹
```

## 三、上游指南已修好（2026-08-31 第 2 次核对）

第一次核对时我发现上游 `-SKILL-` 的 `track-paper-aso/README.md` 目录与 PDF 实物有 **4 处不符**，
并据此重排了 12 会话。上游随后自己修了：

- 最新提交 `4cbe659`「Rewrite paper study track based on actual PDF content」（2026-08-31 04:33 UTC）；
- `README.md` 升到 **v2.0（基于 PDF 实际内容重写）**，并新增 `paper.pdf`；
- 我核过：上游那份 `paper.pdf` 与本仓库 `materials/` 里的 PDF **sha256 完全一致**
  （`1a97b96b2b001928a5ac5a5878554ec70e74870660b195782d4ac3bb1e4d1052`，5,337,421 字节）；
- v2.0 的章节页码与我从 PDF 书签读出的 45 条书签**逐条吻合**。

**所以 4 处冲突已全部消除。** 差异记录保留在 `资料映射.md` §三 与 `memory/ERRORS.md` J2，
作为"引用外部资料前必须核一手材料"的判例，不删。

## 三之二、用户背景已一手核实（原"待核实"作废）

原 README §三 第 3 条把用户背景标为"矛盾、待核实"，**这个判断是错的**（判例 `memory/ERRORS.md` J1）：

| 项 | 核实结果 | 一手来源 |
|---|---|---|
| 姓名 | 孙承泽 | `turbine-blade-ai-platform/HANDOFF.md` §1；`wind_farm_viz` 组会 PPT 文件名 |
| 身份 | 西安交大能动学院 **能动强基 2501 班 本科**（大一升大二），**不是研究生** | 同上 |
| 方向 | 燃气轮机与航空发动机"两机"、气动热力学、MDO | 同上 |
| 导师 | 郭振东 副教授（班主任）、宋立明 教授（叶轮机械研究所副所长） | 同上 |
| 项目 | **turbine-blade-ai-platform 真实存在**，NASA Rotor 37 / PLAID 1000 样本 / 74 维 / 残差代理 / NSGA-II / MC Dropout UQ / SU2 / ONNX-WASM 前端 | 分支 `arena/019ffee7-...`（2026-08-15 提交 `a8d0fe1a`，**比 main 新 7 天**） |
| 目标 | 直博两机重大专项 → 大三海外访学 → 发 ASME Turbo Expo / J. Turbomachinery | `学习路.md` |

"高中/大一水平"和"自研平台"**不矛盾**：他是刚读完大一的强基生，工程实践远超同龄，
但正式数学/流体力学课还没上。→ 讲课口径是**深入浅出但不减深度**（六层阶梯），不是降低难度。
完整画像与讲课硬规则 A0–A7 见 `memory/LEARNINGS.md`。

## 三之三、这不只是 1 篇论文

用户要求"这 12 篇论文我要彻底吃透"。规划见 **`12篇论文总规划.md`**：
P01 = 本综述（12 次会话），P02–P12 = 从本综述参考文献里按**被引次数客观排序**选出的 11 篇
（含 DOI），共 51 次会话。其中我也实测了本综述的覆盖盲区：**FNO / DeepONet / Transformer /
扩散模型 / SINDy 在 528 条参考文献里 0 命中**，需另补。

## 四、开局协议（照抄总纲 §0）

1. 读仓库根 `AGENTS.md`（回合级 push 是最高优先级）；
2. 读 `论文精读/memory/HANDOFF.md`；
3. 扫 `memory/LEARNINGS.md` + `memory/ERRORS.md`；
4. 查 `memory/PROGRESS.md` 与 `memory/drill-ledger/index.md`，**先清到期卡**；
5. 从 HANDOFF 的"下一句该问什么"继续，不重新自我介绍。
