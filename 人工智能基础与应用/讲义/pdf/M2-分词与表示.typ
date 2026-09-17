
// ══ 讲义排版模板（由 md2typst.py 生成，请勿手改）══
#set document(title: "M2 · 分词与表示", author: "孙承泽 · 能动强基2501 · 西安交通大学")

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
    #text(font: SANS, size: 27pt, weight: "bold", fill: ACCENT)[M2 · 分词与表示]
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


= 讲义 M2 · 分词与表示

#block(width: 100%, above: 9pt, below: 9pt, inset: (left: 12pt, right: 8pt, y: 6pt), stroke: (left: 3pt + luma(180)), fill: luma(252))[
#text(size: 9.8pt)[
对应课题：#strong[课题01 BPE 分词器（W1）]｜模块：M2｜预计 2 个时段（3–5 小时） 对标材料：CS336 A1 handout（规格权威）· 李沐 d2l ch14.6 子词嵌入（中文）· HF LLM Course ch2 #strong[读法]：先读下面的"要回答的问题"，再读对标材料，最后回来看本讲义主干。
]
]

== 〇、本讲要回答的 5 个问题

+ BPE 训练究竟在优化什么？为什么说它"不是词汇表，而是压缩器"？
+ 为什么必须从#strong[字节]起步？代价是什么？
+ 训练算法为什么容易写成 O(n²)？如何做到官方要求的 \<1.5 秒？
+ 编码时为什么必须"回放合并历史"，而不能"最长匹配优先"？
+ 同一个模型，换分词器后 loss 不可比——那该用什么指标？

#v(4pt)
#line(length: 100%, stroke: 0.6pt + luma(200))
#v(4pt)

== 一、压缩视角：BPE 到底在做什么

#strong[一句话]：给定词表预算 V，BPE 反复执行"找出当前出现次数最多的相邻 token 对 → 合并成一个新 token"。每合并一次，语料的总 token 数减少一点，直到词表填满 V。

形式化：把语料看成一串字节 $b_1 b_2 dots.h b_n$。定义当前切分下相邻对 $(x,y)$ 的频次 $c(x,y)$。每步选 $ (x^(*), y^(*)) = arg max_((x,y)) c(x,y) $ 把语料中所有该对合并为新 token $x y$，并把 $(x,y)$ 记入 merges 列表（顺序即"资历"）。

#strong[关键推论 A（压缩率）]：合并的收益可以直接量化——每合并一处，总 token 数减 1。所以"BPE 训练过程"就是"贪心压缩过程"，merges 列表本质是#strong[一本压缩字典，且按收益从大到小排序]。

#strong[关键推论 B（为什么 loss 不可跨分词器比较）]：token 越少 → 每个 token 承载信息越多 → 单 token 的交叉熵必然更高。这是记账单位问题，不是模型好坏。所以跨分词器比较必须换成#strong[与切分无关]的单位：bits-per-byte（bpb）。

#block(width: 100%, above: 9pt, below: 9pt, inset: (left: 12pt, right: 8pt, y: 6pt), stroke: (left: 3pt + luma(180)), fill: luma(252))[
#text(size: 9.8pt)[
#strong[这条是新课标里最重要的一条]：nanochat 全程用 bpb 而不是 loss 来跨模型比较，课题03（scaling law）和课题08（RL 对照）都会回到这里。
]
]

#v(4pt)
#line(length: 100%, stroke: 0.6pt + luma(200))
#v(4pt)

== 二、为什么必须字节起步（以及代价）

从 #strong[Unicode 字符]起步的三个具体麻烦：

#block(width: 100%, above: 8pt, below: 10pt)[
#text(size: 9pt)[
  #table(
    columns: (0.224fr, 0.410fr, 0.365fr),
    inset: (x: 7pt, y: 5pt),
    align: left + top,
    stroke: (x, y) => (bottom: if y == 0 { 0.9pt + luma(105) } else { 0.25pt + luma(220) }),
    table.header([麻烦], [具体例子], [后果]),
    [词表爆炸且长尾], [仅 CJK 就有 9 万余字符，常用仅数千], [大部分字符训练不充分，嵌入近乎随机],
    [永远有未登录], [新 emoji（每年新增）、生僻字、方言字], [无兜底机制 → OOV，直接崩],
    [失去字节级共享], ["妈"与"吗"共享部首但完全不同字符], [学不到字形/字节层面的结构],
  )
]
]

从#strong[字节]起步：任何文本 → UTF-8 → 0–255 的字节序列 → 这 256 个 token 永远在词表里。 #strong[所以字节级 BPE 永远不存在"无法表示的输入"，只可能被切得更碎。] 这就是"零风险"的含义。

#strong[代价（必须知道，因为它是第 1 题的答案关键）]：

- 汉字 UTF-8 占 #strong[3 字节]；英文常用词常被合并成 1 token，而中文常需 1.5–2 个 token 表示 1 个汉字 （取决于词表大小与语料配比）→ #strong[中文的"每字成本"高于英文]
- 序列变长 → 注意力计算量（O(L²)）上升 → 中文推理成本更高

#v(4pt)
#line(length: 100%, stroke: 0.6pt + luma(200))
#v(4pt)

== 三、训练算法：从 O(n²) 到官方要求的 \<1.5 秒

#strong[朴素想法的三个陷阱]（都会导致超时或超内存）：

+ #strong[每步重扫全语料]统计相邻对 → O(V · n)，V=500、n≈百万级就是灾难
+ #strong[用字符串做合并]（#raw("text.replace(\"ab\",\"ab_new\")")）→ 每次 O(n) 拷贝 + 无法区分"新合并的 token"与"原始字符"
+ #strong[把语料整体读入内存再展开成 token 列表] → 5MB 语料 + 1MB 配额的内存测试必挂

#strong[正确方向的三个要点]（方向，不是实现）：

- #strong[词频级统计而非字符级]：同一种"词"（如 #raw(" the")）在语料里重复百万次，只需统计一次它的结构，再按词频加权
- #strong[增量更新]：一次合并只影响"包含该对的相邻位置"，其余的对频次不变 → 只需局部更新
- #strong[优先队列/堆]：快速取出当前最高频的对，而不是每步全量排序

#block(width: 100%, above: 9pt, below: 9pt, inset: (left: 12pt, right: 8pt, y: 6pt), stroke: (left: 3pt + luma(180)), fill: luma(252))[
#text(size: 9.8pt)[
官方参考实现 0.38 秒，"玩具实现"约 3 秒——#strong[这 8 倍差距就在上面三点里]。
]
]

#v(4pt)
#line(length: 100%, stroke: 0.6pt + luma(200))
#v(4pt)

== 四、编码：回放合并历史，而不是最长匹配

编码时我们#strong[没有语料统计]，只有 merges 列表（一个有序的"合并历史"）。正确做法：

#block(width: 100%, above: 9pt, below: 9pt, inset: (x: 10pt, y: 8pt), radius: (right: 4pt), fill: luma(248), stroke: (left: 2.5pt + luma(165)))[
  #raw("把文本按 UTF-8 切成字节数组
loop:
    找出当前序列中所有相邻对里，在 merges 中\"排名最靠前\"（资历最老）的那一对
    合并它
    直到没有任何相邻对出现在 merges 中", block: true)
]

#strong[为什么不是"最长匹配优先"？] 因为训练时每一次合并都遵循"最老优先"的规则； 若编码用另一套规则，同一个子串在不同上下文会被切成不同 token， #strong[与 tiktoken/GPT-2 的逐 id 对齐测试必然失败]。BPE 的编码本质是#strong[回放训练时的决策序列]。

#strong[特殊 token 是另一套优先级]：它们#strong[不参与合并]，且在编码时#strong[先于普通文本被匹配]。 注意两个官方测试点名的情况：#strong[重叠]的特殊 token（如 #raw("a") 与 #raw("ab") 同时存在）与 #strong[尾随换行]（#raw("<|endoftext|>\\n")）——这类边界的处理顺序会直接决定对错。

#v(4pt)
#line(length: 100%, stroke: 0.6pt + luma(200))
#v(4pt)

== 五、接口设计决定内存上界（#raw("encode") vs #raw("encode_iterable")）

官方测试里有一个耐人寻味的设置：

#block(width: 100%, above: 8pt, below: 10pt)[
#text(size: 9pt)[
  #table(
    columns: (0.419fr, 0.581fr),
    inset: (x: 7pt, y: 5pt),
    align: left + top,
    stroke: (x, y) => (bottom: if y == 0 { 0.9pt + luma(105) } else { 0.25pt + luma(220) }),
    table.header([方法], [官方态度]),
    [#raw("encode(text)")], [被 #raw("xfail") 标记：#emph["encode 预期会超过 1MB 配额"] —— #strong[超了也原谅]],
    [#raw("encode_iterable(iterable)")], [用 #raw("RLIMIT_AS") 硬限 1MB，读 5MB 语料 —— #strong[超了就失败]],
  )
]
]

#strong[为什么这不是双标]：接口的#strong[输入形态]决定了它的内存下界。 #raw("encode(str)") 的输入本身就是一整段字符串，它已经在内存里了——上界由输入决定，实现者无能为力。 #raw("encode_iterable(iterable)") 的契约是#strong[流式]：输入是迭代器，实现就必须逐块处理、边读边 yield。 任何 #raw("list(iterable)") / #raw("\"\".join(iterable)") / 先聚合再编码的写法，都违背了接口语义。

#block(width: 100%, above: 9pt, below: 9pt, inset: (left: 12pt, right: 8pt, y: 6pt), stroke: (left: 3pt + luma(180)), fill: luma(252))[
#text(size: 9.8pt)[
这是#strong[软件工程里最漂亮的一课]：接口不只是名字，它是#strong[约束]。 同一个算法，换个接口，内存上界就从"输入大小"降到"块大小"。这个思想在课题05（KV cache）、 课题07（数据流式清洗）、课题10（长程 Agent 的记忆压缩）都会反复出现。
]
]

#v(4pt)
#line(length: 100%, stroke: 0.6pt + luma(200))
#v(4pt)

== 六、词表大小的三方权衡（第 1、4 题的答案框架）

词表从 V 扩到 4V，同时影响三件事：

#block(width: 100%, above: 8pt, below: 10pt)[
#text(size: 9pt)[
  #table(
    columns: (0.319fr, 0.241fr, 0.440fr),
    inset: (x: 7pt, y: 5pt),
    align: left + top,
    stroke: (x, y) => (bottom: if y == 0 { 0.9pt + luma(105) } else { 0.25pt + luma(220) }),
    table.header([受影响项], [方向], [机理]),
    [嵌入/输出层参数量], [↑ 约 4 倍], [参数 ∝ V·d（若权重共享则 1 份，否则 2 份）],
    [同文本序列长度 L], [↓], [更多常见片段被合并 → token 数下降],
    [每 token 的注意力计算], [↓ 约 L² 下降], [注意力是 O(L²·d)],
    [罕见 token 的训练充分度], [↓], [长尾 token 出现次数少，嵌入学不好],
  )
]
]

净效果#strong[不是单调的]：太小 → 序列太长、算力烧在长度上；太大 → 参数浪费 + 长尾欠训练。 经验上 32k–128k 是常见区间（GPT-2 用 50257，现代模型多在 100k 量级，且对多语言友好）。

#strong[中文特例]：词表若中文覆盖不足，一个汉字可能被拆成 3 个字节 token， #strong[中文成本直接翻 2–3 倍]——这是国产模型普遍重视中文词表预算的原因。

#v(4pt)
#line(length: 100%, stroke: 0.6pt + luma(200))
#v(4pt)

== 七、常见误解（每条配反例）

#block(width: 100%, above: 8pt, below: 10pt)[
#text(size: 9pt)[
  #table(
    columns: (0.340fr, 0.660fr),
    inset: (x: 7pt, y: 5pt),
    align: left + top,
    stroke: (x, y) => (bottom: if y == 0 { 0.9pt + luma(105) } else { 0.25pt + luma(220) }),
    table.header([误解], [反例]),
    ["一个 token 就是一个词"], [#raw("▁transformer") 可能是 1 个 token，#raw("妈") 可能是 3 个 token（UTF-8 三字节）],
    ["分词只是预处理，不影响模型能力"], [词表决定序列长度 → 决定有效上下文与算力分配 → 直接影响能学到什么],
    ["编码用最长匹配更聪明"], [会与训练决策不一致 → 与 tiktoken 逐 id 对齐测试直接失败],
    ["词表越大越好"], [长尾 token 训练不足 + 嵌入层参数浪费；存在经验最优],
    ["decode 一定无损"], [只有在#strong[完整 utf-8 序列]上才无损；单 token 解码可能是半个字符（#raw("�")）],
  )
]
]

#v(4pt)
#line(length: 100%, stroke: 0.6pt + luma(200))
#v(4pt)

== 八、能立刻跑的实验（讲完就做，知行咬合点）

#block(width: 100%, above: 9pt, below: 9pt, inset: (x: 10pt, y: 8pt), radius: (right: 4pt), fill: luma(248), stroke: (left: 2.5pt + luma(165)))[
  #raw("# ① 跑判分基线（现在应当是 27 failed + 1 xfailed，全部因缺手写文件）
环境/judge/judge.sh 01 --quick

# ② 看官方参考 merges 长什么样（前 20 条）——体会\"资历顺序\"的直觉
head -20 上游/assignment1-basics/tests/fixtures/train-bpe-reference-merges.txt

# ③ 亲眼看字节：一个汉字到底占几个 token（用官方 fixture 的 GPT-2 词表）
环境/.venv/bin/python - <<'PY'
import tiktoken, os
os.environ[\"TIKTOKEN_CACHE_DIR\"] = \"环境/tiktoken-cache\"
enc = tiktoken.get_encoding(\"gpt2\")
for s in [\"hello world\", \"你好\", \"你好，世界！\", \"🦙\"]:
    ids = enc.encode(s)
    print(f\"{s!r:16} → {len(ids)} 个 token  {[enc.decode([i]) for i in ids]}\")
print(\"→ 汉字/emoji 被切成多个字节 token 的现象，一眼可见\")
PY", block: true, lang: "bash")
]

#v(4pt)
#line(length: 100%, stroke: 0.6pt + luma(200))
#v(4pt)

== 九、代码级提问（3–5 道，先写预测再动手）

+ #strong[【改坏预测】] 把训练里"并列最高频时任意取一个"改成"取字节序最小的一对"， #raw("test_train_bpe") 会过吗？#raw("test_train_bpe_speed") 呢？#strong[先写预测和理由。]
+ #strong[【诊断】] 你的实现通过了往返一致性测试，但 #raw("test_train_bpe") 的 merges 比对失败。 请按顺序列出你会检查的 4 件事（提示方向：预处理、并列规则、特殊 token、词表初值）。
+ #strong[【代价估算】] 同一句话，词表从 32k 换到 128k： ①嵌入参数量变几倍 ②序列长度大致变几成 ③#strong[bpb 会变吗？为什么？]
+ #strong[【接口】] 若把 #raw("encode_iterable") 写成"先 #raw("list(iterable)") 再拼接"， 哪个测试会挂？#strong[挂的形式是断言失败，还是进程被直接杀掉？]（想清楚 #raw("RLIMIT_AS") 的作用方式）
+ #strong[【迁移】] 课题05 要写 KV cache，它会遇到和"#raw("encode") vs #raw("encode_iterable")"#strong[同构]的内存问题吗？ 说说你的类比。

#v(4pt)
#line(length: 100%, stroke: 0.6pt + luma(200))
#v(4pt)

== 十、记忆锚

- #strong[隐喻]：BPE = #strong["贪心的拼音缩写机"]——不停找最常一起出现的两段，把它们缩成一个新记号， 缩到最后词表满了；字典按先来后到排资历。
- #strong[口诀]：#strong["字节兜底、频次贪心、老手优先、流式省内存"]（对应：字节起步 / 训练目标 / 编码回放 / 接口约束）
- #strong[符号位置法]：$V$（词表）在上，撑着两件事：下面是 #strong[参数量 ∝ V·d]，右边是 #strong[序列长度 L ↓]； 三者写成一个三角形，随时能想起"扩词表 = 拿参数换长度"。

#v(4pt)
#line(length: 100%, stroke: 0.6pt + luma(200))
#v(4pt)

== 十一、本讲与后续的接口（预告）

- #strong[M3]：序列长度 L 怎么进入注意力计算量（O(L²)）——词表选择的代价在这一讲兑现
- #strong[M4]：bpb 作为跨规模比较单位——scaling law 的纵轴
- #strong[M5]：#raw("encode_iterable") 的流式思想 → KV cache 的"不重算历史"
- #strong[课程板块]：本讲直接对应课程大纲的"大语言模型"入门，也是大论文"方法"章的第一段素材
