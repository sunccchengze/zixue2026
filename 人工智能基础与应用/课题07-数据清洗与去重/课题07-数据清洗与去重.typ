
// ══ 讲义排版模板（由 md2typst.py 生成，请勿手改）══
#set document(title: "课题07-数据清洗与去重", author: "孙承泽 · 能动强基2501 · 西安交通大学")

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
    #text(font: SANS, size: 27pt, weight: "bold", fill: ACCENT)[课题07-数据清洗与去重]
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


= 课题07 开题简报 · 数据清洗与去重

#block(width: 100%, above: 9pt, below: 9pt, inset: (left: 12pt, right: 8pt, y: 6pt), stroke: (left: 3pt + luma(180)), fill: luma(252))[
#text(size: 9.8pt)[
模块：#strong[M7/M4] ｜ 周次：#strong[W10（11-16→11-22）] ｜ 算力：#strong[T1 Kaggle 1×T4，计划 6 GPU·小时] 唐杰作业对应：#strong[③ 从 raw dump 洗语料] ｜ 判分来源：#strong[CS336 A4]（过滤/去重规格）+ 自建消融 手写：#strong[R8（过滤/去重的判定规则设计）]
]
]

== 一、研究背景

"数据决定上限"已是共识：C4/FineWeb/Dolma 等工作的主要贡献#strong[不是模型而是数据管线]。 典型手段：语言识别、质量启发式（重复度、符号比、平均行长）、有毒内容过滤、#strong[近似去重（MinHash/LSH）]。 最有教学价值的现象：#strong[清洗规则过严会伤害模型]（把有价值的长尾数据也删了）。

== 二、研究问题

#block(width: 100%, above: 9pt, below: 9pt, inset: (left: 12pt, right: 8pt, y: 6pt), stroke: (left: 3pt + luma(180)), fill: luma(252))[
#text(size: 9.8pt)[
#strong[在固定算力下，"清洗 + 去重"能把同样规模模型的下游表现提升多少？每条规则的收益与代价各是多少？]
]
]

== 三、攻关线索

+ #strong[基线优先]：先训一个"未清洗"的基线（可与课题04 的结果复用）—— #strong[没有对照就无法声称"清洗有效"]
+ #strong[规则设计]：至少三条可解释规则（如：短行比例、符号-词比、n-gram 重复率），每条要能说清"它在拦什么"
+ #strong[去重量级]：精确去重（哈希）与近似去重（MinHash + LSH）的成本差异；文档级 vs 段落级
+ #strong[消融]：逐条关掉规则各跑一次（小规模即可），得"每条规则的边际贡献"表
+ #strong[口径]：所有对照必须#strong[同 token 预算、同分词器、同评测]（否则结论无效）
+ #strong[常用工具对照]：#raw("datajuicer/data-juicer")（Apache-2.0，活跃）与 #raw("allenai/dolma") 的规则集可作参考

== 四、里程碑

- □ M1 数据来源与规模确定（用 owt-sample / TinyStories 扩样，或小规模 CC 采样）
- □ M2 手写 3 条启发式规则 + 1 个去重算法（精确哈希起步，有余力再上 MinHash）
- □ M3 规则单元测试（#strong[含假阳性样例]：被误删的好数据长什么样）
- □ M4 训练对照：未清洗 vs 全部清洗 vs 逐条消融（≥4 组跑）
- □ M5 结果表：每组的下游指标 + #strong[数据保留率]（这是被忽略的关键列）
- □ M6 一页报告：必须回答"哪条规则最值钱、哪条可能有害"

== 五、交付物

#block(width: 100%, above: 8pt, below: 10pt)[
#text(size: 9pt)[
  #table(
    columns: (0.256fr, 0.328fr, 0.417fr),
    inset: (x: 7pt, y: 5pt),
    align: left + top,
    stroke: (x, y) => (bottom: if y == 0 { 0.9pt + luma(105) } else { 0.25pt + luma(220) }),
    table.header([交付物], [位置], [验收]),
    [过滤/去重实现], [#raw("手写/")], [M3 单测通过],
    [规则清单与理由], [#raw("报告.md")], [每条规则说明"拦什么、代价是什么"],
    [对照实验数据], [#raw("证据/对照.csv")], [含保留率与指标],
    [假阳性样例], [#raw("证据/")], [≥5 条被误删的好数据],
  )
]
]

== 六、讲课锚点

- #strong[讲义]：#raw("M7-评测.md")（W9 展开）中"数据质量与评测的关系"
- #strong[对标]：CS336 lecture 13–14（Data）+ A4 handout · #raw("datajuicer/data-juicer") 规则文档 · Dolma 论文
- #strong[搭桥]：概率论的#strong[采样与分布] —— 过滤本质是"改变训练分布"，会引入选择偏差

== 七、代码级提问示例

+ 过滤掉"短行"能提分，但会不会系统性删掉对话/代码类数据？怎么检测这种偏差？
+ 精确去重 vs 近似去重：各自漏掉什么、误杀什么？
+ 数据保留率从 90% 降到 50%，你如何判断"这是提纯还是阉割"？
+ #strong[【下注】] 预测"全部清洗"相对"未清洗"的提升幅度，先写再测。

== 八、风险与提醒

- ⚠ 磁盘：本课题可能涉及较大语料，#strong[大文件绝不进 git]（见学科 #raw(".gitignore")）。
- ⚠ 不要一开始就上 MinHash 集群版：#strong[先精确去重跑通闭环]，再考虑近似。
- ⚠ 4 组对照训练会吃掉配额：#strong[用小模型 + 短序列]，保证口径一致即可。
