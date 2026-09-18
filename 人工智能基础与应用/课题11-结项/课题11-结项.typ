
// ══ 讲义排版模板（由 md2typst.py 生成，请勿手改）══
#set document(title: "课题11-结项", author: "孙承泽 · 能动强基2501 · 西安交通大学")

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
    #text(font: SANS, size: 27pt, weight: "bold", fill: ACCENT)[课题11-结项]
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


= 课题11 开题简报 · 结项（NeurIPS 报告 + 现场 demo）

#block(width: 100%, above: 9pt, below: 9pt, inset: (left: 12pt, right: 8pt, y: 6pt), stroke: (left: 3pt + luma(180)), fill: luma(252))[
#text(size: 9.8pt)[
模块：#strong[M9] ｜ 周次：#strong[W15–W16（12-21→2027-01-03）] ｜ 算力：#strong[弹性 ≤4 GPU·小时] 唐杰作业对应：#strong[⑥ 英文 NeurIPS 格式 + W16 现场 demo]、#strong[⑦ 作业 40% / 大项目 60%] ｜ 判分来源：#strong[报告协议 + 导师审稿 + 自我攻击]
]
]

== 一、研究背景

唐杰的原话是"#strong[问题、动机、方法、结果，一项都不能糊]"。 这恰好也是本学科九份章程反复强调的：#strong[没有证据的结论不采纳、no-go 不擦除、误差棒必填]。 结项不是"写一篇总结"，而是#strong[把 11 个课题的证据链组装成一份可被审稿的作品]。

== 二、研究问题（结项版）

#block(width: 100%, above: 9pt, below: 9pt, inset: (left: 12pt, right: 8pt, y: 6pt), stroke: (left: 3pt + luma(180)), fill: luma(252))[
#text(size: 9.8pt)[
#strong[我能不能用一份英文技术报告 + 一个可运行的 demo，证明我独立完成了大模型全链路，并且知道自己的结论在哪里不成立？]
]
]

== 三、攻关线索

+ #strong[报告骨架]（NeurIPS 风格，8–10 页）：Abstract / Introduction / Related Work / Method / Experiments / Results / Discussion & Limitations / Conclusion
+ #strong[只写有证据的结论]：每个数字都能指回 #raw("证据/") 中的原始日志
+ #strong[Limitations 必须诚实]：规模受限（0.1B vs 前沿）、算力受限（免费档）、评测口径的局限
+ #strong[Demo 设计]：现场演示要#strong[可在 3 分钟内跑完]（预生成 checkpoint，不现场训练）
+ #strong[自我攻击 3 条]：主动写出"我的结论最可能错在哪"
+ #strong[一稿多用]：这份报告同时作为课程大论文（70%）与唐杰作业⑦的交付物

== 四、里程碑

- □ M1 证据清点：11 个课题的 #raw("证据/") 全部齐备，缺的补齐（这是一次"审计"）
- □ M2 英文报告初稿（Abstract + Method + Experiments 先写）
- □ M3 图表规范化：所有图有坐标轴、单位、误差棒、样本数
- □ M4 #strong[自我攻击 3 条] + 导师审稿 3–5 条 → 修订
- □ M5 Demo 准备：脚本 + 预生成模型 + 3 分钟演练
- □ M6 总复盘：写进 #raw("memory/LEARNINGS.md")（哪些讲法有效、哪些坑最贵）
- □ M7 课程大论文定稿并提交（署名直填：孙承泽 / 2253710052 / 能动强基2501）

== 五、交付物

#block(width: 100%, above: 8pt, below: 10pt)[
#text(size: 9pt)[
  #table(
    columns: (0.187fr, 0.554fr, 0.259fr),
    inset: (x: 7pt, y: 5pt),
    align: left + top,
    stroke: (x, y) => (bottom: if y == 0 { 0.9pt + luma(105) } else { 0.25pt + luma(220) }),
    table.header([交付物], [位置], [验收]),
    [英文报告], [#raw("课题11-结项/report-en.md")（+ PDF）], [格式合规、结论有据],
    [中文大论文], [#raw("课程轨/大论文/")], [课程要求格式],
    [Demo], [#raw("课题11-结项/脚手架/demo.sh")], [3 分钟内可跑],
    [复盘], [#raw("memory/LEARNINGS.md") + #raw("HANDOFF.md")], [可被下一任直接接续],
  )
]
]

== 六、讲课锚点

- #strong[讲义]：#raw("M9-前沿.md")（W15 展开）
- #strong[对标]：#strong[rasbt ch3 的"先建评测"精神]贯穿全文 · CS336 报告规范 · #raw("论文精读/") 的英文写作规范
- #strong[搭桥]：#raw("turbine-blade-ai-platform")（应用章节）；#raw("人工智能基础与应用/课程轨/大论文")（一稿两用）

== 七、自检清单（结项前必过，抄自《判分与验收标准》§五）

+ 每个数字都能在 #raw("证据/") 找到原始日志吗？
+ "变好了"有没有可能是口径变了 / 只挑了好种子？
+ 有没有把#strong[训练集表现]当能力？
+ 每个"因为…所以…"有没有反事实检验？
+ 图表的坐标轴与误差棒都标了吗？
+ 我写下的最强反方论点是什么？

== 八、风险与提醒

- ⚠ 报告最易犯的错是#strong[夸大]：规模受限就要说受限，这反而是可信度来源。
- ⚠ 不要为了"好看"删掉 no-go 记录——用户明确要求"负结果不许擦除"。
- ⚠ W16 现场 demo 必须有#strong[失败预案]（预生成结果 + 录屏），不依赖现场网络与算力。
