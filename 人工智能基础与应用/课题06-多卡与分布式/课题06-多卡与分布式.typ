
// ══ 讲义排版模板（由 md2typst.py 生成，请勿手改）══
#set document(title: "课题06-多卡与分布式", author: "孙承泽 · 能动强基2501 · 西安交通大学")

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
    #text(font: SANS, size: 27pt, weight: "bold", fill: ACCENT)[课题06-多卡与分布式]
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


= 课题06 开题简报 · 多卡与分布式训练

#block(width: 100%, above: 9pt, below: 9pt, inset: (left: 12pt, right: 8pt, y: 6pt), stroke: (left: 3pt + luma(180)), fill: luma(252))[
#text(size: 9.8pt)[
模块：#strong[M4] ｜ 周次：#strong[W9（11-09→11-15）] ｜ 算力：#strong[T2 Kaggle 2×T4，计划 8 GPU·小时] 唐杰作业对应：#strong[② 的"多卡训练增益"部分] ｜ 判分来源：#strong[CS336 A2 分布式部分 + 自建 benchmark] 手写：#strong[R3 的延伸（并行策略选择与通信原语判断）]
]
]

== 一、研究背景

数据并行（DDP）把同一模型复制到每张卡、各自算一个微批、再#strong[同步梯度]； 当模型放不下单卡时，才有 FSDP/ZeRO（切分参数、梯度、优化器状态）、张量并行（切层内矩阵）、流水线并行（切层）。 #strong[Kaggle 免费档给的是 2×T4，且走 PCIe 而非 NVLink] —— 这恰好是"观察通信成为瓶颈"的最佳实验台。

== 二、研究问题

#block(width: 100%, above: 9pt, below: 9pt, inset: (left: 12pt, right: 8pt, y: 6pt), stroke: (left: 3pt + luma(180)), fill: luma(252))[
#text(size: 9.8pt)[
#strong[在弱互联（PCIe）的 2×T4 上，DDP 的扩展效率是多少？瓶颈是计算还是通信？FSDP 在什么规模才开始划算？]
]
]

== 三、攻关线索

+ #strong[先对齐正确性]：DDP 后的梯度应与单卡（同等效批大小）#strong[数值一致]，先验证再谈性能
+ #strong[批大小语义]：2 卡 × 每卡 batch = 等效批大小；若显存受限要#strong[同步调整学习率]（线性/平方根缩放）
+ #strong[计时口径]：#raw("step time") 要区分"纯计算时间"与"含 all-reduce 的时间"；用 #raw("torch.profiler") 或手写计时
+ #strong[扩展效率]：$E = frac(T_1, 2 thin T_2)$。#strong[先预测]（PCIe 下 0.6–0.8？）再测
+ #strong[通信占比]：梯度同步量与参数量成正比（$2 N$ 字节/步，all-reduce 近似）；序列长/批小时通信占比更高
+ #strong[FSDP 的代价]：切分带来额外通信（all-gather + reduce-scatter），#strong[小模型上往往更慢]

== 四、里程碑

- □ M1 DDP 梯度一致性验证（与单卡同等效批）→ 记录最大误差
- □ M2 单卡 vs 双卡 的 #raw("step time")、#raw("tokens/s") 对照（同模型、同等效批）
- □ M3 #strong[扩展效率曲线]（至少 3 个配置点：不同 batch/序列长度）
- □ M4 #strong[通信占比分解]：计算 / all-reduce / 数据加载 三段计时
- □ M5 一次 FSDP 实验并解释"为什么（不）划算"
- □ M6 #strong[先写预测再实测]：预测扩展效率，跑完对照（进 #raw("memory/MEMORY.md") 打脸日志）
- □ M7 一页报告

== 五、交付物

#block(width: 100%, above: 8pt, below: 10pt)[
#text(size: 9pt)[
  #table(
    columns: (0.199fr, 0.416fr, 0.385fr),
    inset: (x: 7pt, y: 5pt),
    align: left + top,
    stroke: (x, y) => (bottom: if y == 0 { 0.9pt + luma(105) } else { 0.25pt + luma(220) }),
    table.header([交付物], [位置], [验收]),
    [分布式脚本], [#raw("手写/") 或 #raw("脚手架/")（按 B3 分类）], [可复跑],
    [计时原始数据], [#raw("证据/bench.csv")], [含每配置 3 次重复],
    [扩展效率曲线], [#raw("证据/")], [标注硬件（2×T4 PCIe）与对比基准],
    [报告], [#raw("报告.md")], [解释"为什么不是 2 倍"],
  )
]
]

== 六、讲课锚点

- #strong[讲义]：#raw("M4-训练.md")（W3 展开）中并行一节
- #strong[对标]：CS336 lecture 07–08（Parallelism）· #raw("nanochat/optim.py")（分布式优化器实现）· HF Ultra-Scale Playbook（用前先核）
- #strong[搭桥]：M0 的"梯度累加"→ DDP 就是#strong[跨卡的梯度累加]

== 七、代码级提问示例

+ 2×T4 上 DDP 只快了 1.4 倍，列出三个最可能的原因。
+ 把每卡 batch 减半、用梯度累积补回等效批，通信量会怎么变？
+ 什么情况下 FSDP 会#strong[比 DDP 慢]？（用通信量解释）
+ all-reduce 的通信量是多少字节/步？用参数量 $N$ 表示。

== 八、风险与提醒

- ⚠ Kaggle 双 T4 会话#strong[不稳定]（可能只给一张）：预检时确认 #raw("torch.cuda.device_count()==2")。
- ⚠ 不要在本课题纠缠"调到最快"——#strong[目标是理解扩展效率的成因]，配额要留给课题08。
