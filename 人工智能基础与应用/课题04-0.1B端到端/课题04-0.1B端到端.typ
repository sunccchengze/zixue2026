
// ══ 讲义排版模板（由 md2typst.py 生成，请勿手改）══
#set document(title: "课题04-0.1B端到端", author: "孙承泽 · 能动强基2501 · 西安交通大学")

// 字体回退链：CJK → 拉丁兜底 → 单色 emoji（讲义里偶尔出现 emoji 或方块字符）
#let SERIF = ("Noto Serif SC", "DejaVu Sans", "Noto Emoji")
#let SANS  = ("Noto Sans SC", "DejaVu Sans", "Noto Emoji")
#let MONO  = ("DejaVu Sans Mono", "Noto Sans SC", "Noto Emoji")
#let ACCENT = rgb("#1d4e6b")
#let ACCENT2 = rgb("#2c6f92")

#set page(
  paper: "a4",
  margin: (x: 1.95cm, top: 2.05cm, bottom: 2.0cm),
  header-ascent: 1em,
  header: context {
    let h = query(selector(heading.where(level: 1)).before(here()))
    if h.len() > 0 and here().page() > 1 {
      set text(size: 8pt, fill: luma(140), font: SANS)
      align(right)[#h.last().body]
      v(-0.6em)
      line(length: 100%, stroke: 0.4pt + luma(215))
    }
  },
  footer: context {
    set text(size: 8.5pt, fill: luma(130), font: SANS)
    align(center)[— #counter(page).display() —]
  },
)

#set text(font: SERIF, size: 10.5pt, lang: "zh", region: "cn", hyphenate: false)
#set par(justify: true, leading: 1.02em, spacing: 0.95em, first-line-indent: 0em)
#set raw(tab-size: 2)
#show raw: set text(font: MONO, size: 8.3pt, fill: luma(35))
#show link: set text(fill: ACCENT2)

#show heading: set text(font: SANS, weight: "bold", fill: ACCENT)
#show heading.where(level: 1): it => {
  pagebreak(weak: true)
  v(0.25em)
  block(width: 100%)[
    #text(size: 19.5pt, fill: ACCENT)[#it.body]
    #v(3pt)
    #line(length: 100%, stroke: 1.3pt + ACCENT)
  ]
  v(0.8em)
}
#show heading.where(level: 2): it => block(above: 1.25em, below: 0.55em, width: 100%)[
  #text(size: 13.5pt, fill: ACCENT2)[#it.body]
]
#show heading.where(level: 3): it => block(above: 1.0em, below: 0.45em)[
  #text(size: 11.5pt, fill: rgb("#33566b"))[#it.body]
]
#show heading.where(level: 4): it => block(above: 0.9em, below: 0.4em)[
  #text(size: 10.5pt, fill: rgb("#33566b"))[#it.body]
]

#[
  #set page(header: none, footer: none)
  #v(3.0cm)
  #align(center)[
    #text(font: SANS, size: 12pt, fill: luma(110), tracking: 0.15em)[人工智能基础与应用 · 大模型实训]
    #v(1.4cm)
    #text(font: SANS, size: 27pt, weight: "bold", fill: ACCENT)[课题04-0.1B端到端]
    #v(0.5cm)
    #text(font: SANS, size: 12.5pt, fill: ACCENT2)[开题简报 · 交付要求 · 判卷记录]
    #v(1.0cm)
    #line(length: 45%, stroke: 0.8pt + luma(150))
    #v(1.0cm)
    #text(size: 11pt, fill: luma(70))[孙承泽 · 能动强基2501 · 西安交通大学]
    #v(0.25cm)
    #text(size: 9.5pt, fill: luma(130))[2026-09-17 生成　·　版本 v1.0]
  ]
  #v(4.4cm)
  #align(center)[
    #text(size: 8.5pt, fill: luma(150), font: SANS)[Markdown 母版：人工智能基础与应用/讲义/ 下的 .md 文件　·　配套上游：CS336 A1–A5 · nanochat · minimind]
  ]
  #pagebreak()
]


= 课题04 开题简报 · 0.1B 端到端预训练（#strong[首次上机]）

#block(width: 100%, above: 9pt, below: 9pt, inset: (left: 12pt, right: 8pt, y: 6pt), stroke: (left: 3pt + luma(180)), fill: luma(252))[
#text(size: 9.8pt)[
模块：#strong[M4/M5] ｜ 周次：#strong[W5–W6（10-12→10-25）] ｜ 算力：#strong[T2 Kaggle 2×T4，计划 12–21 GPU·小时] 唐杰作业对应：#strong[① 端到端训一个 0.1B] ｜ 判分来源：#strong[自建]（loss/bpb 达标 + 采样可读性）+ #raw("nanochat/core_eval.py") 的 CORE 手写：复用课题01/02 的产物（tokenizer + 模型 + 优化器），本课题新增#strong[数据管线与训练编排的判断]
]
]

#v(4pt)
#line(length: 100%, stroke: 0.6pt + luma(200))
#v(4pt)

== 一、研究背景

"0.1B" 是唐杰作业里的数字，也是#strong[单卡/双卡免费算力下的上限]。参考点：nanochat 的 d12 约等于 GPT-1 量级 （官方讨论区原话："d12 是我最喜欢的模型，它是 GPT-1 的大小，约 6 分钟训完"——那是在 8×H100 上）。 #strong[本课题的核心不是刷指标，而是把"训练一次完整模型"的每个环节亲自走通并记账。]

== 二、研究问题（一句话）

#block(width: 100%, above: 9pt, below: 9pt, inset: (left: 12pt, right: 8pt, y: 6pt), stroke: (left: 3pt + luma(180)), fill: luma(252))[
#text(size: 9.8pt)[
#strong[在 2×T4、20 GPU·小时的预算内，我能不能从零训出一个"能生成连贯英文、并在 CORE 上有非零分"的 0.1B 模型？实测成本与估算差多少？]
]
]

== 三、攻关线索

+ #strong[数据]：TinyStories（全量）+ owt-sample 采样。#strong[先算一遍]：词表大小 × 语料字节 → token 数 → 需要的步数
+ #strong[规模选择]：nanochat 用单一旋钮 #raw("--depth")；在 T4 上 16GB 显存能放多深？（用 M0 的显存公式先估）
+ #strong[精度]：#strong[T4 是 SM75，没有 bf16] → 必须 fp16 + GradScaler（或用 nanochat 的 #raw("NANOCHAT_DTYPE=float16")）
+ #strong[断点续训]：Kaggle 会话 9–12h 会断 → checkpoint 必须写 #raw("/kaggle/working")（20GB 持久）
+ #strong[超时自停]：脚本内置 wall-clock 上限，防止忘记关会话
+ #strong[指标]：训练看 bpb（词表无关），最终跑 CORE（22 数据集合成，#raw("core_eval.py") 单文件）

== 四、里程碑

- □ M1 #strong[实验卡获批]：写清假设/命令/预算上限/停止条件/成功判据（见《算力与成本预算.md》§五）
- □ M2 #strong[会话预检]：#raw("nvidia-smi") 确认 2×T4（#strong[若是 P100 立即重开会话]）
- □ M3 #strong[冒烟]：#raw("--depth=4")、100 步，确认能跑、能存、能续训（≤10 分钟）
- □ M4 首次正式训练：双 T4 + DDP，跑到预算上限或 loss 平台
- □ M5 续训一次（验证 checkpoint 真的可用 —— 这一条最容易翻车）
- □ M6 评测：bpb + CORE + #strong[采样 20 条样本]（人工判断"是否连贯"）
- □ M7 #strong[成本账单]：实测耗时 vs 估算（M0 的 6ND + T4 折算），逐项解释偏差
- □ M8 一页报告 + 知识卡（含"我最意外的三个现象"）

== 五、交付物

#block(width: 100%, above: 8pt, below: 10pt)[
#text(size: 9pt)[
  #table(
    columns: (0.280fr, 0.292fr, 0.428fr),
    inset: (x: 7pt, y: 5pt),
    align: left + top,
    stroke: (x, y) => (bottom: if y == 0 { 0.9pt + luma(105) } else { 0.25pt + luma(220) }),
    table.header([交付物], [位置], [验收]),
    [实验卡], [#raw("证据/实验卡-NN.md")], [经用户确认],
    [run.yaml + 日志], [#raw("证据/")], [含 commit、配置、随机种子、耗时],
    [曲线], [#raw("证据/")], [loss/bpb vs FLOPs 与 vs 时间 两张],
    [采样样本], [#raw("证据/样本.md")], [≥20 条，标注"通顺/不通顺"],
    [#strong[成本账单]], [#raw("报告.md")], [实测 vs 估算偏差 ≤ 2× 或给出解释],
    [checkpoint], [Kaggle 持久盘], [不进程（体积原因）；只在 #raw("证据/") 留哈希与路径],
  )
]
]

== 六、讲课锚点

- #strong[讲义]：#raw("M4-训练.md")（W3 展开）
- #strong[对标]：#raw("nanochat/README.md") 与 #raw("runs/speedrun.sh")（读它怎么组织全流程）· CS336 lecture 05/13–14
- #strong[搭桥]：课题03 的 scaling 结论在这里第一次被"真跑"检验

== 七、代码级提问示例

+ 双 T4 跑 d12，为何#strong[不是] 2 倍加速？先预测扩展效率（50%？80%？），再测。
+ T4 上 fp16 与 fp32，谁更快？谁更稳？GradScaler 在解决什么？
+ 你的 loss 在第 2000 步开始上升。按 M0 §五 的顺序，你的前三个动作是什么？
+ 若把语料从 TinyStories 换成中文语料（词表不变），loss 会怎么变？#strong[bpb 呢？]

== 八、风险与提醒

- ❗ #strong[P100 陷阱]：本课题如果拿到 P100，训练慢 3–5 倍且后续课题05 直接不可用 → #strong[宁可等 T4 时段]。
- ❗ #strong[配额]：本课题占全学期约 1/5 的配额，实验卡必须写实；#strong[冒烟不通过不许开正式训练]。
- ⚠ 0.1B 在 T4 上大概率需要"降 batch + 梯度累积"，这会改变有效 batch size → #strong[要写进 run.yaml]。
- ⚠ Kaggle 会话到期会杀进程：#strong[每 500 步存一次]是硬要求。
