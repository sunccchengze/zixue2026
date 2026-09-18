
// ══ 讲义排版模板（由 md2typst.py 生成，请勿手改）══
#set document(title: "课题03-Scaling-Law", author: "孙承泽 · 能动强基2501 · 西安交通大学")

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
    #text(font: SANS, size: 27pt, weight: "bold", fill: ACCENT)[课题03-Scaling-Law]
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


= 课题03 开题简报 · Scaling Law 预演与打脸链路

#block(width: 100%, above: 9pt, below: 9pt, inset: (left: 12pt, right: 8pt, y: 6pt), stroke: (left: 3pt + luma(180)), fill: luma(252))[
#text(size: 9.8pt)[
模块：#strong[M4] ｜ 周次：#strong[W4（10-05→10-11）] ｜ 算力：#strong[T0 纯 CPU（极小规模 sweep）] 唐杰作业对应：#strong[③ 拟合 scaling law 再外推] ｜ 判分来源：#strong[无官方判分器]（CS336 A3 需 8 位学号 API key，不可得）→ #strong[自建判分：预测 vs 实测的偏差] 手写：#strong[R6（拟合与外推）]
]
]

#v(4pt)
#line(length: 100%, stroke: 0.6pt + luma(200))
#v(4pt)

== 一、研究背景

Kaplan 等（2020）与 Chinchilla（2022）发现：loss 随参数量 $N$ 与数据量 $D$ 呈#strong[幂律下降]， 且存在一个#strong[算力最优配比]。这条规律是"为什么敢花几千万训一次大模型"的全部依据。 但初学者最常见的错误是：#strong[把外推当预言]，不做回溯验证就把曲线画到天上去。

本课题的核心不是"拟合出一条漂亮的线"，而是#strong[建立"预测 → 验证 → 承认偏差"的科研习惯]。 这也是本学科"预测—打脸日志"（#raw("memory/MEMORY.md")）的主要产地。

== 二、研究问题（一句话）

#block(width: 100%, above: 9pt, below: 9pt, inset: (left: 12pt, right: 8pt, y: 6pt), stroke: (left: 3pt + luma(180)), fill: luma(252))[
#text(size: 9.8pt)[
#strong[在极小规模（我的 CPU 能承受的范围内）跑 4–5 个点，能否外推出更大模型的 loss？外推误差有多大、什么时候会崩？]
]
]

== 三、攻关线索

+ #strong[口径]：横轴用什么？参数量 $N$？token 数 $D$？（提示：固定预算时，$N$ 与 $D$ 不能同时变）
+ #strong[记账]：用 M0 的 $6 N D$ 估算每一次跑的算力，#strong[确保不同点是在"同样算力预算"下比较]（否则曲线无意义）
+ #strong[拟合]：幂律 $L = a N^(-alpha) + c$ 的形式里，那个常数项 $c$ 代表什么？它会不会让外推失效？
+ #strong[外推]：拟合完先#strong[把预测写死在文件里]（带日期），再去跑验证点 —— 顺序不能反
+ #strong[偏差来源]：小规模数据是否"无限数据区"？学习率是否随规模重新调过？#strong[这些都是外推失准的技术原因]

== 四、里程碑

- □ M1 设计 sweep：4–5 个规模点（如 d4/d6/d8/d10），预算固定、口径统一
- □ M2 跑完 sweep，记录每个点的最终 loss/bpb 与耗时（CPU 上即可，分钟级）
- □ M3 拟合幂律并画图（含数据点、拟合线、坐标轴标注）
- □ M4 #strong[先写死外推预测]（例如 d12 的 bpb 预测值 + 置信区间），归档到 #raw("证据/")
- □ M5 跑验证点，计算偏差，并#strong[解释偏差的方向与原因]
- □ M6 一页报告：包含"预测 vs 实测"对照表（#strong[这一条是验收硬指标]）

== 五、交付物

#block(width: 100%, above: 8pt, below: 10pt)[
#text(size: 9pt)[
  #table(
    columns: (0.282fr, 0.353fr, 0.365fr),
    inset: (x: 7pt, y: 5pt),
    align: left + top,
    stroke: (x, y) => (bottom: if y == 0 { 0.9pt + luma(105) } else { 0.25pt + luma(220) }),
    table.header([交付物], [位置], [验收]),
    [sweep 原始数据], [#raw("证据/sweep.csv")], [含配置、loss、耗时、算力估算],
    [拟合脚本与图], [#raw("脚手架/") + #raw("证据/")], [图有坐标轴、有拟合优度],
    [#strong[外推预测存档]], [#raw("证据/预测-<日期>.md")], [跑验证点#strong[之前]的文件时间戳],
    [报告], [#raw("报告.md")], [预测 vs 实测对照表],
  )
]
]

== 六、讲课锚点

- #strong[讲义]：#raw("讲义/M4-M9-待展开大纲.md") 的 M4 部分（W3 展开为完整版 #raw("M4-训练.md")）
- #strong[对标]：CS336 lecture 09/11（scaling laws）· #raw("nanochat/runs/scaling_laws.sh") 与其 miniseries 文档 · d2l 的线性回归/最小二乘（拟合的数学基础）
- #strong[搭桥]：#raw("probability/") 的方差与回归 —— 拟合优度、残差分析直接可用

== 七、代码级提问示例

+ 为什么横轴常画 #strong[FLOPs] 而不是参数量？（提示：Chinchilla 的核心结论是什么）
+ 你拟合出的 $c$（常数项）为负，说明了什么？还能外推吗？
+ 如果两个规模点用了不同的学习率，曲线还能一起拟合吗？为什么？
+ #strong[【下注】] 你预测 d12 的 bpb 会比你拟合线的预测值偏高还是偏低？先写下答案再跑。

== 八、风险与提醒

- ⚠ #strong[不要为了"好看"调学习率]：每个点的超参策略必须写进 #raw("证据/")，否则外推无意义。
- ⚠ 极小规模会出现"学习率不敏感/过于敏感"的异常区间 —— 这本身就是很好的报告素材（no-go 不擦除）。
- ⚠ 本课题#strong[不花 GPU]；如发现 CPU 太慢，优先"缩小语料/减步数"，不要上 Kaggle（配额留给课题04）。
