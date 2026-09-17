
// ══ 讲义排版模板（由 md2typst.py 生成，请勿手改）══
#set document(title: "库 · 使用方法（三师制里的\"我\"那一腿）", author: "孙承泽 · 能动强基2501 · 西安交通大学")

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
    #text(font: SANS, size: 27pt, weight: "bold", fill: ACCENT)[库 · 使用方法（三师制里的"我"那一腿）]
    #v(0.5cm)
    #text(font: SANS, size: 12.5pt, fill: ACCENT2)[从零实现大模型：M0–M9 知识主干（16 周 / 11 课题 / 零预算）]
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


= 讲义库 · 使用方法（三师制里的"我"那一腿）

#block(width: 100%, above: 9pt, below: 9pt, inset: (left: 12pt, right: 8pt, y: 6pt), stroke: (left: 3pt + luma(180)), fill: luma(252))[
#text(size: 9.8pt)[
立库 2026-09-17。#strong[为什么要有这个库]：用户指出"实操性够强，但知识讲解偏少"。 《知识地图》回答"学什么"，《对标资源清单》回答"跟谁学"， #strong[本库回答"此刻这一讲到底讲了什么"]——由我按你的水平写的#strong[主讲义]。

三者关系不是替代，是分工：

- #strong[对标名师]（Raschka / 李沐 / 李宏毅 / CS336）＝ 权威原始讲法，读它打地基
- #strong[本库讲义] ＝ 为你量身写的浓缩主干 + 与代码的对应 + 常见误解（省你时间）
- #strong[我（对话里）] ＝ 只讲你卡住的那一层，出代码级提问，判你的理解
]
]

== 讲义规范（每讲必含 8 件）

#block(width: 100%, above: 8pt, below: 10pt)[
#text(size: 9pt)[
  #table(
    columns: (0.072fr, 0.362fr, 0.567fr),
    inset: (x: 7pt, y: 5pt),
    align: left + top,
    stroke: (x, y) => (bottom: if y == 0 { 0.9pt + luma(105) } else { 0.25pt + luma(220) }),
    table.header([\#], [部件], [作用]),
    [1], [本讲要回答的 3–5 个问题], [带着问题读，读完能答才算过],
    [2], [主干讲解（≤150 字/概念块）], [一次讲透，不挤牙膏],
    [3], [公式/伪代码骨架], [这是"手写区"的地图，#strong[不是答案]],
    [4], [#strong[在代码里长什么样]], [指向 #raw("手写/") 或上游 nanochat 的#strong[函数与接口]（不给行号、不给实现）],
    [5], [常见误解（每条配一个反例）], [抄自历届踩坑与官方测试的隐含要求],
    [6], [能立刻跑的实验], [讲完就跑，知行咬合点],
    [7], [代码级提问（3–5 道）], [改坏它/预测现象/给出诊断],
    [8], [记忆锚（隐喻 + 口诀 + 符号位置）], [进 drill-ledger],
  )
]
]

== 📕 下载 PDF（离线阅读 / 打印用）

不用看屏幕读 Markdown——#strong[讲义已排成 PDF]，直接下载：

#block(width: 100%, above: 8pt, below: 10pt)[
#text(size: 9pt)[
  #table(
    columns: (0.405fr, 0.121fr, 0.474fr),
    inset: (x: 7pt, y: 5pt),
    align: left + top,
    stroke: (x, y) => (bottom: if y == 0 { 0.9pt + luma(105) } else { 0.25pt + luma(220) }),
    table.header([下载这个], [页数], [说明]),
    [#strong[#raw("讲义/pdf/大模型实训讲义-全书.pdf")]], [23], [★ #strong[首选]：封面 + 版权说明 + 目录 + M0–M3 + 大纲],
    [#raw("讲义/pdf/M0…M3.pdf") 等单讲分册], [2–5], [手机上读、单讲打印、发给同学],
    [#raw("章程与地图/pdf/章程与地图-全书.pdf")], [28], [九份章程合订（学什么/跟谁学/什么叫学过/何时学/谁写代码）],
  )
]
]

#strong[排版与验收]：正文思源宋体、标题黑体、代码等宽；全书 23 页里 99 条去重公式已#strong[逐条单独编译验证]过， 每讲章节也做了齐备性自检（防排版吞内容）。重生成与维护见 #raw("环境/pdf/README.md")。

#block(width: 100%, above: 9pt, below: 9pt, inset: (x: 10pt, y: 8pt), radius: (right: 4pt), fill: luma(248), stroke: (left: 2.5pt + luma(165)))[
  #raw("cd 人工智能基础与应用 && 环境/pdf/生成讲义PDF.sh        # 每讲 + 全书
cd 人工智能基础与应用 && 环境/pdf/生成讲义PDF.sh --charter   # 章程分册", block: true, lang: "bash")
]

#block(width: 100%, above: 9pt, below: 9pt, inset: (left: 12pt, right: 8pt, y: 6pt), stroke: (left: 3pt + luma(180)), fill: luma(252))[
#text(size: 9.8pt)[
铁律：#strong[母版是这里的 #raw(".md")，PDF 是派生物]。改了讲义必须重跑一次生成脚本。
]
]

== 目录与状态

#block(width: 100%, above: 8pt, below: 10pt)[
#text(size: 9pt)[
  #table(
    columns: (0.317fr, 0.125fr, 0.229fr, 0.203fr, 0.125fr),
    inset: (x: 7pt, y: 5pt),
    align: left + top,
    stroke: (x, y) => (bottom: if y == 0 { 0.9pt + luma(105) } else { 0.25pt + luma(220) }),
    table.header([讲义], [模块], [对应课题/周次], [状态], [PDF]),
    [#raw("M0-数学与机器学习地基.md")], [M0], [贯穿，W1 起], [✔ 已写], [✔ 5 页],
    [#raw("M1-从n-gram到Transformer.md")], [M1], [课题02，W2], [✔ 已写], [✔ 4 页],
    [#raw("M2-分词与表示.md")], [M2], [#strong[课题01，W1（当前）]], [✔ 已写], [✔ 5 页],
    [#raw("M3-Transformer内部机制.md")], [M3], [课题02，W2–W3], [✔ 已写], [✔ 5 页],
    [#raw("M4-M9-待展开大纲.md")], [M4–M9], [W4–W16], [◐ 大纲已就位，按周展开], [✔ 4 页],
  )
]
]

#block(width: 100%, above: 9pt, below: 9pt, inset: (left: 12pt, right: 8pt, y: 6pt), stroke: (left: 3pt + luma(180)), fill: luma(252))[
#text(size: 9.8pt)[
PDF 生成日期：2026-09-17（母版有改动就要重跑 #raw("环境/pdf/生成讲义PDF.sh")）。
]
]

#block(width: 100%, above: 9pt, below: 9pt, inset: (left: 12pt, right: 8pt, y: 6pt), stroke: (left: 3pt + luma(180)), fill: luma(252))[
#text(size: 9.8pt)[
展开节奏：#strong[每周讲之前，我把当周讲义写完整]（不留空讲义占位）；本文件表格同步更新状态。
]
]

== 使用流程（照做）

#block(width: 100%, above: 9pt, below: 9pt, inset: (x: 10pt, y: 8pt), radius: (right: 4pt), fill: luma(248), stroke: (left: 2.5pt + luma(165)))[
  #raw("① 预习：读本讲\"要回答的问题\"（2 分钟）
② 读对标材料对应章节（≤25 分钟，带着问题读）
③ 读本库讲义（≤15 分钟，看主干与\"代码里长什么样\"）
④ 合上讲义，用自己的话讲给我听 → 我专挑含糊处追问
⑤ 进手写区（R 类任务）→ 跑判分
⑥ 做\"改坏实验\"→ 先预测 → 再跑 → 修好
⑦ 我出代码级提问，你作答 → 进 drill-ledger 建卡", block: true)
]

#strong[纪律]：讲义里#strong[不含可直接粘贴到 #raw("手写/") 的实现]（见《造轮子边界.md》）。 讲义给的是"坐标系 + 陷阱 + 判据"，代码必须你自己长出来。
