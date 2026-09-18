
// ══ 讲义排版模板（由 md2typst.py 生成，请勿手改）══
#set document(title: "课题05-Triton-attention-kernel", author: "孙承泽 · 能动强基2501 · 西安交通大学")

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
    #text(font: SANS, size: 27pt, weight: "bold", fill: ACCENT)[课题05-Triton-attention-kernel]
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


= 课题05 开题简报 · 手写 Triton attention kernel

#block(width: 100%, above: 9pt, below: 9pt, inset: (left: 12pt, right: 8pt, y: 6pt), stroke: (left: 3pt + luma(180)), fill: luma(252))[
#text(size: 9.8pt)[
模块：#strong[M5] ｜ 周次：#strong[W7–W8（10-26→11-08）] ｜ 算力：#strong[T1 Kaggle 1×T4，计划 10 GPU·小时] 唐杰作业对应：#strong[② 手写 Triton attention kernel，测多卡训练与推理增益] ｜ 判分来源：#strong[CS336 A2]（正确性对齐）+ 自建性能对照 手写：#strong[R5（kernel 本体：分块 + online softmax）]
]
]

#v(4pt)
#line(length: 100%, stroke: 0.6pt + luma(200))
#v(4pt)

== 一、研究背景

朴素注意力要把 $L× L$ 的注意力矩阵#strong[整个写进显存]：$L=8 1 9 2$ 时单头就是 64M 个元素。 FlashAttention（2022）的核心洞察：#strong[根本不需要把矩阵写出来] —— 分块计算、在线维护 softmax 的 最大值与归一化因子，就能得到数学上完全等价的结果。它把注意力的显存从 $O(L^2)$ 降到 $O(L)$。

Triton 让这件事对非 CUDA 专家也可做：用 Python 风格的 DSL 写"块级"程序。 #strong[本课题的目标不是写出最快的 kernel，而是亲手经历"数值等价 + 显存下降 + 速度提升"这三件事的因果链。]

== 二、研究问题（一句话）

#block(width: 100%, above: 9pt, below: 9pt, inset: (left: 12pt, right: 8pt, y: 6pt), stroke: (left: 3pt + luma(180)), fill: luma(252))[
#text(size: 9.8pt)[
#strong[一个分块 + online softmax 的手写 kernel，能否在数值上等价于朴素实现，并把显存从 O(L²) 降到 O(L)、速度提升若干倍？提升来自哪里（算术减少？访存减少？）]
]
]

== 三、攻关线索

+ #strong[先量化瓶颈]：朴素实现在 L=2k/8k 时的显存、耗时（用 profiler 看是 compute-bound 还是 memory-bound）
+ #strong[online softmax 的递推]：维护 running max $m$ 与 running sum $ℓ$， 新块的贡献要按 $e^(m_("old")-m_("new"))$ 缩放 —— #strong[这正是 M0 §四 logsumexp 的应用]
+ #strong[分块维度]：按 query 分块、沿 key 方向扫描 → 每个块只需常驻 SRAM
+ #strong[数值容差]：与 PyTorch SDPA 对照，相对误差应在 1e-2\~1e-3（fp16）；#strong[先写容差，再判定]
+ #strong[多卡/推理增益]：训练侧测吞吐（tokens/s），推理侧测 decode 显存与延迟 —— 这是唐杰作业②要求的"增益"

== 四、里程碑

- □ M1 基线：朴素注意力的显存与耗时（L=2k/4k/8k 三点）
- □ M2 #strong[正确性]：手写 kernel 与 SDPA 的数值对照（max abs error 记录在案）
- □ M3 #strong[显存]：证明峰值显存随 L 近似线性（对比朴素实现的 O(L²)）
- □ M4 #strong[速度]：给出 speedup 曲线（含 L 与 block size 两个维度）
- □ M5 #strong[profiling]：用 profiler 说明"提升来自哪里"（访存 vs 算术，给出数字）
- □ M6 #strong[增益测量]：训练吞吐（tokens/s）与推理（融合进 attention 后）的实测对比
- □ M7 一页报告 + 知识卡（online softmax 递推必须能徒手推）

== 五、交付物

#block(width: 100%, above: 8pt, below: 10pt)[
#text(size: 9pt)[
  #table(
    columns: (0.197fr, 0.246fr, 0.558fr),
    inset: (x: 7pt, y: 5pt),
    align: left + top,
    stroke: (x, y) => (bottom: if y == 0 { 0.9pt + luma(105) } else { 0.25pt + luma(220) }),
    table.header([交付物], [位置], [验收]),
    [kernel], [#raw("手写/")（你写）], [M2 数值对照通过],
    [三张图], [#raw("证据/")], [speedup / 显存 / profile（#strong[坐标轴与硬件口径必须标注]）],
    [数值误差记录], [#raw("证据/")], [含容差设定与依据],
    [报告], [#raw("报告.md")], [必须回答"提升来自哪里"],
  )
]
]

== 六、讲课锚点

- #strong[讲义]：#raw("讲义/M5-推理.md")（W5 展开）中"GPU 内存层级与 Triton 编程模型"一节
- #strong[对标]：CS336 lecture 05–06（GPUs / Kernels & Triton）+ A2 handout（#strong[flash-attn 需两步安装]： #raw("uv sync --no-install-package flash-attn") 再 #raw("uv sync")）· Triton 官方 FlashAttention 教程
- #strong[搭桥]：M0 §四 的 logsumexp —— 你会亲手把它写进 kernel

== 七、代码级提问示例

+ online softmax 里，为什么新块要乘 $e^(m_("old")-m_("new"))$？不乘会怎样？
+ block size 从 64 增到 256：显存、速度、数值误差各往哪走？
+ 为什么 L 很大时，朴素实现容易 OOM 而 kernel 不会？（用 $O(L^2)$ vs $O(L)$ 说清）
+ #strong[【下注】] 你预测 speedup 在 L=2k 时是多少倍？先写，再测。

== 八、风险与提醒

- ❗ #strong[P100 不可用于本课题]：Triton 要求计算能力 ≥7.0，P100 是 6.0 → #strong[开跑前必须验明是 T4]。
- ⚠ 正确性优先于速度：#strong[数值对照不过，速度数字一律不算数]。
- ⚠ 硬件口径陷阱：任何 speedup 数字必须写明"对比对象（PyTorch SDPA / 朴素实现）"与"硬件（T4）"， 否则曲线毫无意义（这一条写进报告硬要求）。
- ⚠ 若 T4 上 kernel 因共享内存不够而失败，#strong[先降 block size，不要放弃]（这本身就是教学素材）。
