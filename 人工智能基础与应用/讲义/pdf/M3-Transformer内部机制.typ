
// ══ 讲义排版模板（由 md2typst.py 生成，请勿手改）══
#set document(title: "M3 · Transformer 内部机制", author: "孙承泽 · 能动强基2501 · 西安交通大学")

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
    #text(font: SANS, size: 27pt, weight: "bold", fill: ACCENT)[M3 · Transformer 内部机制]
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


= 讲义 M3 · Transformer 内部机制

#block(width: 100%, above: 9pt, below: 9pt, inset: (left: 12pt, right: 8pt, y: 6pt), stroke: (left: 3pt + luma(180)), fill: luma(252))[
#text(size: 9.8pt)[
对应课题：#strong[课题02 Transformer 骨架（W2–W3）]｜模块：M3｜预计 2–3 个时段 对标材料：CS336 lecture 03–04 + A1 handout（模型部分）· rasbt《LLMs-from-scratch》ch3–ch4（附录含 GQA/MLA/MoE） 这是全学科#strong[最核心的一讲]：唐杰作业①的"从零写 Transformer"就落在这里。
]
]

== 〇、本讲要回答的 5 个问题

+ 注意力到底在算什么？为什么缩放因子是 $1/sqrt(d_k)$？
+ 为什么要多头？多头比单头强在哪、代价是什么？
+ RoPE 凭什么比可学习位置嵌入更能外推？
+ RMSNorm 凭什么能替代 LayerNorm？pre-norm 与 post-norm 差在哪？
+ 一个 $d$ 宽、$L$ 层、词表 $V$ 的 Transformer 有多少参数？KV cache 有多大？

#v(4pt)
#line(length: 100%, stroke: 0.6pt + luma(200))
#v(4pt)

== 一、注意力：加权检索 + 为什么缩放 $1/sqrt(d_k)$

#strong[计算式]（先记住形状，再看含义）： $ "Attn"(Q,K,V) = "softmax"lr((frac(Q K^(⊤), sqrt(d_k)) + M))V $ 其中 $Q,K,V ∈ bb(R)^(L× d_k)$，$M$ 是因果掩码（下三角为 0、其余 $-∞$）。

#strong[含义]：每个位置发出一个查询 $q$，去和所有位置的键 $k$ 做#strong[内积]（相似度）， softmax 归一化成权重，再对值 $v$ 做加权平均。#strong[它就是"按相似度检索并汇总"]。

#strong[为什么除以 $sqrt(d_k)$]：设 $q,k$ 各分量独立、均值 0 方差 1，则内积 $q⋅ k = sum_(i=1)^(d_k) q_i k_i$ 的 方差是 $d_k$（方差可加）。$d_k$ 越大，内积的#strong[取值范围越宽] → softmax 越容易"饱和" （一个位置拿走几乎全部权重）→ 梯度趋近 0 → 训练不动。 除以 $sqrt(d_k)$ 把内积的方差重新拉回 1 量级。#strong[这是"训练稳定性"的第一课。]

#strong[因果掩码]：语言模型不能看未来。做法是#strong[在 softmax 之前]给未来位置加 $-∞$（实现上常用 $-1 0^9$ 之类的大负数， 而不是 0）——因为在 softmax 之后置零会#strong[改变概率归一化]（等价于把已分配的概率丢掉，剩下的位置没有重新归一）。

#strong[在代码里长什么样]：#raw("手写/") 里会有 #raw("scaled_dot_product_attention") 与 #raw("multihead_self_attention")（含 causal 与 RoPE 两个变体）；上游对照 #raw("nanochat/gpt.py") 的 #raw("CausalSelfAttention")。#strong[注意接口而非实现]：CS336 的 #raw("tests/adapters.py") 规定了你要暴露的函数签名。

#v(4pt)
#line(length: 100%, stroke: 0.6pt + luma(200))
#v(4pt)

== 二、多头：拆开看不同关系，但总算力不变

#strong[做法]：把 $d$ 维拆成 $h$ 份、每份 $d_k = d/h$，各自独立做注意力，再拼回来过一个输出投影 $W_O$。

#strong[关键理解（常被误解）]：多头#strong[不增加]注意力的总计算量—— 单个头用满 $d$ 维时，$Q K^(⊤)$ 是 $L^2 d$；$h$ 个头各 $d/h$ 维合计仍是 $L^2 d$。 多头的收益在于#strong[归纳偏置]：不同的头可以在不同子空间里学不同的关系 （有的学"上一个词是谁"，有的学"括号配对"，有的学"句子边界"），比单一头更灵活。

#strong[变体（现代模型常用）]：

#block(width: 100%, above: 8pt, below: 10pt)[
#text(size: 9pt)[
  #table(
    columns: (0.211fr, 0.365fr, 0.424fr),
    inset: (x: 7pt, y: 5pt),
    align: left + top,
    stroke: (x, y) => (bottom: if y == 0 { 0.9pt + luma(105) } else { 0.25pt + luma(220) }),
    table.header([变体], [做法], [动机]),
    [MQA], [所有头#strong[共享一份] K/V], [KV cache 减小 h 倍，但质量略降],
    [#strong[GQA]], [头分组，组内共享 K/V（如 8 组）], [折中：cache 减小、质量几乎不掉 ← 现代主流],
    [MLA], [把 K/V 压成低维潜变量再解压], [更激进，DeepSeek 系],
  )
]
]

#block(width: 100%, above: 9pt, below: 9pt, inset: (left: 12pt, right: 8pt, y: 6pt), stroke: (left: 3pt + luma(180)), fill: luma(252))[
#text(size: 9.8pt)[
#strong[为什么都在动 K/V]：推理时的瓶颈是 #strong[KV cache 的显存]（见 §五）， 它随 #raw("层数 × 序列长度 × 头数") 线性增长，与"生成速度"直接相关。这是"架构为推理服务"的典型例子。
]
]

#v(4pt)
#line(length: 100%, stroke: 0.6pt + luma(200))
#v(4pt)

== 三、位置编码：从"贴标签"到"转角度"

#strong[问题]：注意力的内积是#strong[置换不变]的——把 token 顺序打乱，结果不变。所以必须注入位置信息。

#strong[三代方案]：

#block(width: 100%, above: 8pt, below: 10pt)[
#text(size: 9pt)[
  #table(
    columns: (0.246fr, 0.395fr, 0.359fr),
    inset: (x: 7pt, y: 5pt),
    align: left + top,
    stroke: (x, y) => (bottom: if y == 0 { 0.9pt + luma(105) } else { 0.25pt + luma(220) }),
    table.header([方案], [做法], [缺陷]),
    [可学习绝对嵌入], [学一个 $L_(max)× d$ 的查表], [#strong[不能外推]：训练 2048，推理 4096 时后一半没学过],
    [正弦绝对编码（原论文）], [$sin/cos$ 固定频率], [可外推性弱，实践中被 RoPE 取代],
    [#strong[RoPE（旋转位置编码）]], [把 $q,k$ 按#strong[二维子空间]旋转角度 $theta⋅ m$], [内积只依赖#strong[相对距离] $m-n$；外推性好],
  )
]
]

#strong[RoPE 的核心恒等式]（这是它存在的全部理由）： $ ⟨ R_m q,thin R_n k⟩ = ⟨ q,thin R_(n-m) k⟩ $ 即：#strong[在内积里只出现"位置差"]，绝对位置被"旋转"吸收掉了。 推导要点：旋转矩阵是正交阵，$R_m^(⊤) R_n = R_(n-m)$。

#strong[频率分配]：第 $i$ 对维度的角频率 $theta_i = 1 0 0 0 0^(-2 i/d)$—— 低维（$i$ 小）转得快（管近距离），高维转得慢（管远距离）。 #strong["10000"这个底数是"能覆盖多长上下文"的旋钮]，这就是所谓 YaRN / NTK 插值等长上下文外推技巧的入口。

#strong[在代码里长什么样]：#raw("手写/") 的 #raw("rope") 与前缀 #raw("rope") 的多头注意力； CS336 有单独的 #raw("run_rope") 测试点。

#v(4pt)
#line(length: 100%, stroke: 0.6pt + luma(200))
#v(4pt)

== 四、归一化与残差：让 100 层能训起来的两件套

#strong[LayerNorm]：对每个 token 的 $d$ 维向量做 $(x-mu)/sqrt(sigma^2+epsilon)$，再缩放和平移。 #strong[RMSNorm]：只做 $x/sqrt("mean"(x^2)+epsilon)$，再乘一个可学缩放 $g$。

- 省掉了#strong[减均值]与#strong[平移]：更便宜（少一次归约、少一组参数）
- 效果相当：真正起作用的是#strong[尺度不变性]（分母归一化），而中心化贡献有限
- 现代模型（LLaMA/Qwen/GLM 系）默认 RMSNorm

#strong[残差连接]：$x ← x + f("norm"(x))$（pre-norm）。 #strong[它防的是梯度消失]：反向传播时，加法的 Jacobian 是单位阵， 于是梯度有一条#strong[恒等通路]可以直达浅层。没有它，几十层的网络基本训不动。

#strong[pre-norm vs post-norm]（原论文是 post-norm）：

#block(width: 100%, above: 8pt, below: 10pt)[
#text(size: 9pt)[
  #table(
    columns: (0.252fr, 0.378fr, 0.370fr),
    inset: (x: 7pt, y: 5pt),
    align: left + top,
    stroke: (x, y) => (bottom: if y == 0 { 0.9pt + luma(105) } else { 0.25pt + luma(220) }),
    table.header([], [形式], [性质]),
    [post-norm], [$"norm"(x + f(x))$], [原版；深了需要小心 warmup，容易发散],
    [#strong[pre-norm]], [$x + f("norm"(x))$], [训练稳，是现代默认；代价是"深度"的表示能力稍弱],
  )
]
]

#block(width: 100%, above: 9pt, below: 9pt, inset: (left: 12pt, right: 8pt, y: 6pt), stroke: (left: 3pt + luma(180)), fill: luma(252))[
#text(size: 9.8pt)[
课题02 会做"去掉残差"的改坏实验：你会亲眼看到 loss 从"平稳下降"变成"几乎不动"。
]
]

#v(4pt)
#line(length: 100%, stroke: 0.6pt + luma(200))
#v(4pt)

== 五、FFN、参数量与 KV cache（#strong[把结构换算成资源]）

#strong[FFN 的演化]：两层线性 + 激活。原版 $d_(f f) = 4 d$ 配 ReLU。 #strong[SwiGLU] 用三个矩阵：$"Swish"(x W_1)⊙(x W_3)$ 再过 $W_2$； 为保持参数量不变，取 $d_(f f) ≈ frac(8, 3)d$（3 个矩阵 × 8/3 ≈ 4 个矩阵 × d 的等价参数量）。

#strong[单层参数量]（$d$ 宽，标准 MHA）：

- 注意力：$W_Q,W_K,W_V,W_O$ 各 $d× d$ → $4 d^2$
- MLP（SwiGLU，$d_(f f)=frac(8, 3)d$）：$3⋅ d⋅ frac(8, 3)d = 8 d^2$
- 两处 RMSNorm 缩放：$2 d$（可忽略）
- #strong[合计 ≈ $1 2 d^2$ 每层] → 全模型 ≈ $1 2 thin L thin d^2 + V d$（权重共享时）

#strong[验算习惯]：拿到任何模型的配置（如 #raw("d=768, L=12, V=50257")）， 先心算 $1 2×1 2×7 6 8^2 ≈ 8 5"M"$，加嵌入 $5 0 2 5 7×7 6 8≈3 9"M"$（共享则算 1 份） ≈ 124M —— #strong[与 GPT-2 的 124M 吻合]。这种"能不能心算"是 M3 的验收标志之一。

#strong[KV cache 显存]（推理，重点）： $ "bytes" = 2 × L_("layers") × L_("seq") × n_(k v) × d_k × "bytes/elem" $ （乘 2 是因为 K 和 V）。用 GQA 后 $n_(k v)$ 从 $h$ 降到组数， #strong[cache 直接按比例缩小]——这就是 GQA 流行的真正原因。 课题05 会实测这个数字。

#v(4pt)
#line(length: 100%, stroke: 0.6pt + luma(200))
#v(4pt)

== 六、常见误解（每条配反例）

#block(width: 100%, above: 8pt, below: 10pt)[
#text(size: 9pt)[
  #table(
    columns: (0.432fr, 0.568fr),
    inset: (x: 7pt, y: 5pt),
    align: left + top,
    stroke: (x, y) => (bottom: if y == 0 { 0.9pt + luma(105) } else { 0.25pt + luma(220) }),
    table.header([误解], [反例 / 更正]),
    ["注意力=可解释的检索"], [注意力权重高 ≠ 因果重要（已有大量反例）；它是#strong[加权平均的权重]，别过度解读],
    ["多头=多算"], [总 FLOPs 不变（§二），只是分成子空间],
    ["位置编码只是加个向量"], [RoPE 是#strong[旋转 Q/K]，不是加到输入上；且它只影响内积的相位],
    ["RMSNorm 是 LayerNorm 的近似"], [它#strong[省略]了中心化，不是近似；在很多模型上效果更好且更省],
    ["参数量大就一定强"], [同样算力下，参数与数据要按 scaling law 配比（课题03 的正题）],
    ["因果 mask 随便加个大负数就行"], [必须#strong[在 softmax 之前]；加在之后会破坏归一化],
  )
]
]

#v(4pt)
#line(length: 100%, stroke: 0.6pt + luma(200))
#v(4pt)

== 七、能立刻跑的实验与改坏实验（课题02 的里程碑）

#strong[基础验证]（跑通即达里程碑 M1–M3）：

#block(width: 100%, above: 9pt, below: 9pt, inset: (x: 10pt, y: 8pt), radius: (right: 4pt), fill: luma(248), stroke: (left: 2.5pt + luma(165)))[
  #raw("bash 环境/bootstrap_cpu.sh --with-torch      # 课题02 起需要 torch
环境/judge/judge.sh 02 --quick               # 形状与数值测试（判分器按需接入）", block: true, lang: "bash")
]

#strong[三组改坏实验（先写预测，再跑，再记录——这是本讲的核心作业）]：

#block(width: 100%, above: 8pt, below: 10pt)[
#text(size: 9pt)[
  #table(
    columns: (0.053fr, 0.276fr, 0.387fr, 0.284fr),
    inset: (x: 7pt, y: 5pt),
    align: left + top,
    stroke: (x, y) => (bottom: if y == 0 { 0.9pt + luma(105) } else { 0.25pt + luma(220) }),
    table.header([\#], [改哪里], [先预测什么], [预期观察（跑完记得回来对照）]),
    [1], [去掉因果 mask（让所有位置互相可见）], [#strong[训练 loss 会大幅下降]，但采样出来的文本"语法很好、内容胡说"], [典型"作弊"：loss 好看，能力为零],
    [2], [RoPE 换成可学习绝对嵌入], [训练集内正常，#strong[超出训练长度立刻崩]], [外推性丧失；正是课程要"用实验看见"的性质],
    [3], [去掉残差连接], [浅层（≤4 层）还能训，#strong[深了就完全不收敛]], [梯度消失的实证],
  )
]
]

#block(width: 100%, above: 9pt, below: 9pt, inset: (left: 12pt, right: 8pt, y: 6pt), stroke: (left: 3pt + luma(180)), fill: luma(252))[
#text(size: 9.8pt)[
#strong[记录要求]：每条都要有"预测 → 现象 → 解释"三段，落进 #raw("课题02/证据/")。预测错是资产，不是污点。
]
]

#v(4pt)
#line(length: 100%, stroke: 0.6pt + luma(200))
#v(4pt)

== 八、代码级提问（3–5 道）

+ #strong[【推导】] 用"方差可加"说明：$q⋅ k$ 的方差是 $d_k$，并解释为何要除以 $sqrt(d_k)$ 而不是 $d_k$。
+ #strong[【心算】] 配置 $d=1 0 2 4,thin L=2 4,thin V=1 0 0 0 0 0$，权重共享。估算参数量（结果用 G/M 表示），并拆出嵌入层占比。
+ #strong[【改坏预测】] 把 causal mask 从"softmax 之前"挪到"softmax 之后"（对已归一化权重置零）， 训练会发生什么？给出两个可能的现象并说明理由。
+ #strong[【联系】] 用 M0 的 logsumexp 解释：为什么 flash attention 的分块计算能保持数值稳定？
+ #strong[【代价】] 序列长度从 2k 增到 32k：①注意力计算量变几倍 ②KV cache 变几倍 ③哪个先撞墙？

#v(4pt)
#line(length: 100%, stroke: 0.6pt + luma(200))
#v(4pt)

== 九、记忆锚

- #strong[隐喻]：注意力 = #strong["会议室里的自由讨论"]——每人（query）挑自己关心的话题（key）， 按关心程度（softmax 权重）听别人（value）说话；因果 mask = "不许听后面发言的人"； 多头 = 同时开 h 个并行分会场；RoPE = 每个人的座位号刻在#strong[朝向]上，所以只关心"相隔几个座位"。
- #strong[口诀]：#strong["缩放防饱和、掩码在软前、多头不减算、旋转只认距、残差是命脉、归一挑 RMS"]
- #strong[符号位置法]：$frac(Q K^(⊤), sqrt(d_k))$ —— 把 $sqrt(d_k)$ 写在分数线下方， 心里念"#strong[维度越高，内积越炸，除以根号拉回来]"。
