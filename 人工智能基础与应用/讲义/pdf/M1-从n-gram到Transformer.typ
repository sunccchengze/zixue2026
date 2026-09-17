
// ══ 讲义排版模板（由 md2typst.py 生成，请勿手改）══
#set document(title: "M1 · 从 n-gram 到 Transformer", author: "孙承泽 · 能动强基2501 · 西安交通大学")

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
    #text(font: SANS, size: 27pt, weight: "bold", fill: ACCENT)[M1 · 从 n-gram 到 Transformer]
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


= 讲义 M1 · 从 n-gram 到 Transformer

#block(width: 100%, above: 9pt, below: 9pt, inset: (left: 12pt, right: 8pt, y: 6pt), stroke: (left: 3pt + luma(180)), fill: luma(252))[
#text(size: 9.8pt)[
对应课题：#strong[课题02（W2）前半]｜模块：M1｜预计 1 个时段 对标材料：李沐 d2l ch8–ch10（RNN → 注意力）· CS336 lecture 01（概览）· 《Attention Is All You Need》原文（走论文精读） #strong[为什么讲这段]：不理解 attention 之前的世界，就不知道它在解决什么问题—— 而"知道它在解决什么问题"，是你将来能判断"某个新架构值不值得看"的唯一依据。
]
]

== 〇、本讲要回答的 5 个问题

+ n-gram 语言模型为什么必然失败？它的失败方式是什么？
+ 困惑度（perplexity）为什么能当指标？它和 M0 的交叉熵什么关系？
+ RNN/LSTM 解决了什么，又为什么被淘汰？
+ seq2seq + attention（2014）与 Transformer（2017）的关键差别在哪？
+ 为什么说"并行性"是 Transformer 取胜的主因，而不是"注意力更聪明"？

#v(4pt)
#line(length: 100%, stroke: 0.6pt + luma(200))
#v(4pt)

== 一、n-gram：用计数做语言模型

#strong[链式法则]：$P(w_(1)dots.h w_T) = product_t P(w_t ∣ w_(<t))$。 #strong[n-gram 的近似]：只依赖前 $n-1$ 个词，$P(w_t∣ w_(t-n+1)dots.h w_(t-1))$，用#strong[语料计数]估计： $ P(w_t∣ w_(t-1)) = frac(c(w_(t-1)w_t), c(w_(t-1))) $

#strong[两个死穴]（这就是"为什么历史必然翻篇"）：

#block(width: 100%, above: 8pt, below: 10pt)[
#text(size: 9pt)[
  #table(
    columns: (0.290fr, 0.710fr),
    inset: (x: 7pt, y: 5pt),
    align: left + top,
    stroke: (x, y) => (bottom: if y == 0 { 0.9pt + luma(105) } else { 0.25pt + luma(220) }),
    table.header([死穴], [具体表现]),
    [#strong[稀疏]], [没见过的组合概率为 0 → 平滑（add-k / 回退 / Kneser-Ney）只是打补丁],
    [#strong[上下文太短]], [$n=5$ 时也只能看 4 个词；而"这句话的主语是谁"可能要跨 50 个词],
  )
]
]

#strong[评价指标]：困惑度 $"PPL"=exp(-frac(1, T)sum_t log P(w_t∣ w_(<t)))$ —— 正是 M0 里交叉熵取指数。#strong[PPL 越低，模型对下一个词越不"惊讶"。] 这个指标一路沿用到今天（bpb 是它的分词器无关版本）。

#v(4pt)
#line(length: 100%, stroke: 0.6pt + luma(200))
#v(4pt)

== 二、词向量：从 one-hot 到分布式表示

#strong[one-hot 的问题]：任意两词的内积都是 0——"猫"和"狗"的距离与"猫"和"民主"一样远。语义无从谈起。

#strong[word2vec（skip-gram + 负采样）]：用一个"给定中心词预测上下文词"的浅层网络， 训练出的#strong[中间层权重]就是词向量。结果是著名的#strong[向量算术]：$arrow(k i n g)-arrow(m a n)+arrow(w o m a n)≈arrow(q u e e n)$。

#strong[关键转折]：人们发现"预测下一个词"这个任务逼着模型学出#strong[语义结构]。 这正是后来 GPT 路线的思想雏形：#strong[语言建模本身就是最好的自监督任务。]

#v(4pt)
#line(length: 100%, stroke: 0.6pt + luma(200))
#v(4pt)

== 三、RNN / LSTM：把"历史"压进一个向量

#strong[RNN]：$h_t = tanh(W_h h_(t-1) + W_x x_t)$，用 $h_(t-1)$ 携带历史。 #strong[LSTM]：加门控（遗忘门、输入门、输出门）让信息可以"长期保留"。

#strong[为什么被淘汰（两个根因，都是工程性的）]：

+ #strong[梯度消失/爆炸]：BPTT 要对时间展开求导，梯度是 $product_t frac(∂ h_t, ∂ h_(t-1))$ 的连乘。 连乘里每个 Jacobian 的谱半径 \<1 → 指数衰减；\>1 → 爆炸。#strong[这是结构性问题，不是调参能解决的。]
+ #strong[无法并行]：$h_t$ 依赖 $h_(t-1)$，#strong[必须按时间顺序串行计算]。 GPU 有上万核心却只能一次算一步 —— 训练吞吐被"时间"卡死。

#block(width: 100%, above: 9pt, below: 9pt, inset: (left: 12pt, right: 8pt, y: 6pt), stroke: (left: 3pt + luma(180)), fill: luma(252))[
#text(size: 9.8pt)[
#strong[这是本讲最重要的一句话]：深度学习的历史不是"模型更聪明"的历史， 而是"#strong[让更多算力能有效地作用于更多数据]"的历史。Transformer 赢在#strong[能并行]。
]
]

#v(4pt)
#line(length: 100%, stroke: 0.6pt + luma(200))
#v(4pt)

== 四、seq2seq 与注意力（2014）：注意力的真正起源

#strong[seq2seq 结构]：一个 RNN 把源句编码成一个#strong[固定长度]向量，另一个 RNN 从它解码出目标句。

#strong[瓶颈]：整句信息被压进一个向量 —— 句子越长，丢得越多。

#strong[Bahdanau 注意力（2014）的解法]：解码每一步时，#strong[回头扫描编码器的所有隐状态]， 算出"当前该关注哪几个位置"，加权求和作为当前步的上下文。 → 这就是 #strong[QKV 的雏形]（解码器状态＝Query，编码器隐状态＝Key/Value）。

#strong[关键历史结论]：#strong[注意力最初是给 RNN 打补丁的]，不是 Transformer 的胜利品。 Transformer 的贡献是：#strong["既然注意力这么好用，那还要 RNN 干什么？"]—— 把 RNN 整个删掉，只用注意力 + 前馈层，于是#strong[整段序列可以并行计算]。

#strong[路径长度对比]（理解"为什么更快"的关键）：

#block(width: 100%, above: 8pt, below: 10pt)[
#text(size: 9pt)[
  #table(
    columns: (0.387fr, 0.401fr, 0.212fr),
    inset: (x: 7pt, y: 5pt),
    align: left + top,
    stroke: (x, y) => (bottom: if y == 0 { 0.9pt + luma(105) } else { 0.25pt + luma(220) }),
    table.header([架构], [任意两位置的依赖路径], [并行性]),
    [RNN], [$O(L)$（要穿过 L 步）], [✘ 串行],
    [#strong[Transformer]], [#strong[$O(1)$]（一步直达）], [✔ 全并行],
  )
]
]

代价是注意力本身 $O(L^2)$ 的计算量——这是"用算力换并行"的经典交易， 也是后来 flash attention、稀疏注意力、线性注意力等一整条研究线的起点。

#v(4pt)
#line(length: 100%, stroke: 0.6pt + luma(200))
#v(4pt)

== 五、常见误解

#block(width: 100%, above: 8pt, below: 10pt)[
#text(size: 9pt)[
  #table(
    columns: (0.410fr, 0.590fr),
    inset: (x: 7pt, y: 5pt),
    align: left + top,
    stroke: (x, y) => (bottom: if y == 0 { 0.9pt + luma(105) } else { 0.25pt + luma(220) }),
    table.header([误解], [更正]),
    ["注意力是 Transformer 发明的"], [2014 年 Bahdanau 就用于 seq2seq；2017 只是#strong[去掉 RNN] 并改成 self-attention],
    ["self-attention 与 attention 是两回事"], [同一机制，只是 Q/K/V 都来自同一序列],
    ["RNN 不行是因为效果差"], [在长依赖上确实差，但#strong[致命的并行性]才是被淘汰主因],
    ["PPL 越低模型越强"], [只在#strong[同分词器、同数据]下可比（见 M2）],
  )
]
]

#v(4pt)
#line(length: 100%, stroke: 0.6pt + luma(200))
#v(4pt)

== 六、能立刻跑的实验

#block(width: 100%, above: 9pt, below: 9pt, inset: (x: 10pt, y: 8pt), radius: (right: 4pt), fill: luma(248), stroke: (left: 2.5pt + luma(165)))[
  #raw("# 用 n-gram 的视角感受\"上下文长度\"的代价：统计 bigram 的稀疏程度
环境/.venv/bin/python - <<'PY'
import collections, re
text = open(\"上游/assignment1-basics/tests/fixtures/tinystories_sample.txt\", encoding=\"utf-8\").read().lower()
words = re.findall(r\"[a-z']+\", text)
uni = collections.Counter(words)
bi  = collections.Counter(zip(words, words[1:]))
print(f\"词数={len(words)}  不同词={len(uni)}  不同的相邻词对={len(bi)}\")
print(f\"→ 光是一个小语料，二元组就已经接近词数的 {len(bi)/len(uni):.1f} 倍；三/四元组的稀疏会爆掉\")
print(\"→ 换成长度更大的语料，这个比值会继续上升（稀疏问题的定量感受）\")
PY", block: true, lang: "bash")
]

#v(4pt)
#line(length: 100%, stroke: 0.6pt + luma(200))
#v(4pt)

== 七、代码级提问（3–5 道）

+ #strong[【推导】] 为什么 BPTT 的梯度是 Jacobian 连乘？写出两步的式子，并说明"谱半径 \<1 就衰减"的含义。
+ #strong[【对比】] 用一句话说清：Transformer 相比 RNN，#strong[用掉了什么、换来了什么]？
+ #strong[【判断】] 如果有一天硬件变成"串行极快、并行极慢"，Transformer 还会是主流吗？说理由。
+ #strong[【联系】] d2l 里 attention 的示意图和 M3 讲的 $Q K^(⊤)$ 是一回事吗？把两者对应起来。
+ #strong[【指标】] 你的 n-gram 模型 PPL=120，另一个模型 PPL=80，但用的是不同分词器。能说后者更强吗？

#v(4pt)
#line(length: 100%, stroke: 0.6pt + luma(200))
#v(4pt)

== 八、记忆锚

- #strong[隐喻]：RNN = #strong["传话游戏"]——一句话传到第 50 个人已经面目全非； 注意力 = #strong["所有人同时看着原始白板"]——谁离得远都不影响看清原文。
- #strong[口诀]：#strong["n-gram 死于稀疏、RNN 死于串行、注意力先治 RNN、Transformer 删掉串行"]
- #strong[符号位置法]：把 $O(L)$ 与 $O(1)$ 并排写在卡片上—— #strong[左边是"要走 L 步"，右边是"一步直达"]；下面是代价 $O(L^2)$，提醒你注意力不是免费的。
