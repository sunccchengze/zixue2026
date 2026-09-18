
// ══ 讲义排版模板（由 md2typst.py 生成，请勿手改）══
#set document(title: "大模型实训讲义 · 全书", author: "孙承泽 · 能动强基2501 · 西安交通大学")

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
    #text(font: SANS, size: 27pt, weight: "bold", fill: ACCENT)[大模型实训讲义 · 全书]
    #v(0.5cm)
    #text(font: SANS, size: 12.5pt, fill: ACCENT2)[从零实现大模型：M0–M9 知识主干]
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

#[
  = 目录
  #show outline.entry.where(level: 1): set text(weight: "bold", size: 11pt, fill: ACCENT)
  #show outline.entry.where(level: 2): set text(size: 9.8pt, fill: luma(60))
  #outline(title: none, depth: 2, indent: 1.15em)
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
    [#strong[#raw("讲义/pdf/大模型实训讲义-全书.pdf")]], [24], [★ #strong[首选]：封面 + 版权说明 + 目录 + M0–M3 + 大纲],
    [#raw("讲义/pdf/M0…M3.pdf") 等单讲分册], [2–5], [手机上读、单讲打印、发给同学],
    [#raw("章程与地图/pdf/章程与地图-全书.pdf")], [28], [九份章程合订（学什么/跟谁学/什么叫学过/何时学/谁写代码）],
  )
]
]

#strong[排版与验收]：正文思源宋体、标题黑体、代码等宽；全书 24 页里 99 条去重公式已#strong[逐条单独编译验证]过， 每讲章节也做了齐备性自检（防排版吞内容）。重生成与维护见 #raw("环境/pdf/README.md")。

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

#pagebreak()

= 讲义 M0 · 数学与机器学习地基

#block(width: 100%, above: 9pt, below: 9pt, inset: (left: 12pt, right: 8pt, y: 6pt), stroke: (left: 3pt + luma(180)), fill: luma(252))[
#text(size: 9.8pt)[
对应：#strong[贯穿全程，W1 起]｜前置讲义，不单独占周次，随用随补 对标材料：李沐 d2l ch2–ch5 + ch11（优化）· Karpathy micrograd 视频 · #raw("probability/") 课题01–08（已建成，直接搭桥） #strong[为什么先讲这个]：后面所有的"为什么训练崩了""为什么显存不够""为什么换分词器 loss 不能比"， 答案都在这一讲里。#strong[它不是复习，是工具箱。]
]
]

== 〇、本讲要回答的 5 个问题

+ 梯度是怎么穿过 100 层网络的？为什么反向传播只要一遍？
+ 交叉熵、困惑度、bpb 三者的关系是什么？为什么跨模型只能比 bpb？
+ 训练一个 N 参数的模型，显存和算力到底怎么估？
+ 为什么 softmax 要先减最大值？不这样做会怎样？
+ "loss 不降"时，我该按什么顺序怀疑？

#v(4pt)
#line(length: 100%, stroke: 0.6pt + luma(200))
#v(4pt)

== 一、自动微分：为什么反向传播只要一遍

#strong[计算图]：把 $f(x_1,dots.h,x_n)$ 表示为有向无环图，每个节点是一次基本运算。 #strong[链式法则]：若 $y = f(g(x))$，则 $frac(d y, d x) = frac(d y, d g)⋅frac(d g, d x)$。

两种方向的差别（这是本讲的#strong[第一个关键直觉]）：

#block(width: 100%, above: 8pt, below: 10pt)[
#text(size: 9pt)[
  #table(
    columns: (0.193fr, 0.206fr, 0.292fr, 0.310fr),
    inset: (x: 7pt, y: 5pt),
    align: left + top,
    stroke: (x, y) => (bottom: if y == 0 { 0.9pt + luma(105) } else { 0.25pt + luma(220) }),
    table.header([模式], [做法], [成本], [适合]),
    [前向模式], [从输入往输出推导数], [每个输入要一遍 → #strong[n 遍]], [输入少、输出多],
    [#strong[反向模式]], [从输出往输入推导数], [#strong[一遍]拿到全部输入的偏导], [#strong[输入多、输出少 ← 我们的情况]],
  )
]
]

我们的情况是"几亿个参数（输入多）→ 一个标量 loss（输出少）"， 所以#strong[反向模式（就是我们说的反向传播）]是天选：#strong[1 次前向 + 1 次反向 = 全部梯度]。

#strong[梯度累加的工程含义]：反向时每个节点把上游梯度#strong[相加]。这解释了两个常见现象： ①同一个张量被用了两次（如权重共享），梯度会累加； ②既然梯度是"累加"的，就能#strong[梯度累积]（gradient accumulation）——多个小批次的梯度加起来等价于大批次， 这是后来显存不够时的核心手段（课题04 会用到）。

#strong[在代码里长什么样]：

- #raw("手写/") 里会有一个 #raw("Value") 类（或等价的张量自动微分），核心是 #raw(".backward()")： 按#strong[拓扑逆序]遍历，每个节点用局部导数乘上游梯度累加到父节点。
- 上游对照：#raw("nanochat/optim.py") 里参数更新前的 #raw("p.grad") 就是这一机制的产物；CS336 A1 的 #raw("run_gradient_clipping") 则是#strong[在使用]梯度（先要能算出来）。

#v(4pt)
#line(length: 100%, stroke: 0.6pt + luma(200))
#v(4pt)

== 二、信息量、交叉熵、困惑度、bpb（#strong[跨分词器可比性]的根源）

#strong[信息量]：一个概率为 $p$ 的事件携带的信息是 $-log p$（nats，底为 $e$；若底为 2 则单位是 bit）。

#strong[熵]：随机变量的平均信息量 $H(p) = -sum_x p(x)log p(x)$。 直觉：#strong["平均每个符号有多难猜"]。

#strong[交叉熵]：用模型分布 $q$ 去编码真实分布 $p$ 的代价 $ H(p,q) = -sum_x p(x)log q(x) $ 语言模型里 $p$ 是"真实下一个 token"，$q$ 是模型输出 —— #strong[这正好就是训练 loss]。

#strong[困惑度]：$"PPL" = exp(H(p,q))$（nats 为底时）。 直觉最有用的一句话：#strong["模型平均在多少个等概率选项里犯迷糊。"] PPL=10 相当于"平均 10 选 1"。

#strong[bpb（bits per byte）]： $ "bpb" = frac(H(p,q)thin"[nats]", ln 2 × overline(hash"bytes per token")) $ 分母是"平均每个 token 对应多少字节"。

#block(width: 100%, above: 9pt, below: 9pt, inset: (left: 12pt, right: 8pt, y: 6pt), stroke: (left: 3pt + luma(180)), fill: luma(252))[
#text(size: 9.8pt)[
#strong[为什么必须用 bpb 跨模型比较]：交叉熵的单位是"每 token"，而 token 的大小随分词器变化—— 词表越大 token 越"大"，同样文本的 token 数越少，单 token 交叉熵天然越高。 #strong[除以"每 token 字节数"就把记账单位统一到"每个字节"上，于是与分词器无关。] 这也解释了 M2 讲义的结论：换词表后 loss 不可比，bpb 可比。
]
]

#strong[在代码里长什么样]：#raw("nanochat/loss_eval.py") 专门做 bpb（而不是 loss）的评估； #raw("nanochat/core_eval.py") 则是另一类指标（CORE，由 22 个数据集的准确率合成）。 #strong[你在课题01 的压缩率表，其实是在预演 bpb 的分母]——先感受"每 token 多少字节"。

#v(4pt)
#line(length: 100%, stroke: 0.6pt + luma(200))
#v(4pt)

== 三、算力与显存记账（#strong[估数量级]是核心能力）

#strong[参数量]（Transformer 主项，细节见 M3）：

- 每层注意力 $4 d^2$（Q/K/V/O 四个 $d× d$），MLP 约 $8 d^2$（SwiGLU 的等价形式）→ #strong[每层 ≈ $1 2 d^2$]
- 词嵌入 $V⋅ d$（权重共享时 1 份）

#strong[算力（训练）]：业界通用估算 $ "总 FLOPs" ≈ 6 × N × D $ 其中 $N$ 是#strong[非嵌入参数量]，$D$ 是训练 token 数。拆解：每个参数在前向贡献 2 FLOPs（乘+加）， 反向是前向的 2 倍 → 合计 6。注意力部分另有 $1 2 L h q t$ 项（序列长度相关，短序列时可忽略）。

#block(width: 100%, above: 9pt, below: 9pt, inset: (left: 12pt, right: 8pt, y: 6pt), stroke: (left: 3pt + luma(180)), fill: luma(252))[
#text(size: 9.8pt)[
Karpathy 在 nanochat 文档里给的就是这个公式，并特别注明"与 Chinchilla 略有 1% 差异，因为不计嵌入与 softmax"。
]
]

#strong[显存（训练）]：粗算每参数

#block(width: 100%, above: 8pt, below: 10pt)[
#text(size: 9pt)[
  #table(
    columns: (0.667fr, 0.333fr),
    inset: (x: 7pt, y: 5pt),
    align: left + top,
    stroke: (x, y) => (bottom: if y == 0 { 0.9pt + luma(105) } else { 0.25pt + luma(220) }),
    table.header([项], [字节数]),
    [参数（bf16）], [2],
    [梯度（bf16）], [2],
    [Adam 一阶动量（fp32）], [4],
    [Adam 二阶动量（fp32）], [4],
    [#strong[小计（不含激活、不含 fp32 主权重）]], [#strong[≈ 12–16]],
    [激活（随 batch × 序列长度增长，可用 checkpointing 换）], [视配置],
  )
]
]

#strong[练习式直觉]：0.1B 参数 × 16 字节 ≈ 1.6GB（优化器+梯度+权重）； 剩下的全是激活与临时张量 —— #strong[这就是为什么 16GB 的 T4 训 0.1B 要精打细算]（课题04 的真实约束）。

#strong[在代码里长什么样]：#raw("nanochat/gpt.py") 里有 #raw("estimate_flops()") 与 #raw("num_scaling_params()") 两个方法， 正是上面两段公式的代码化。#strong[课题03 的 scaling law 就是靠这两个函数把"跑多大"换算成"花多少算力"的。]

#v(4pt)
#line(length: 100%, stroke: 0.6pt + luma(200))
#v(4pt)

== 四、数值稳定性：softmax 与 logsumexp

#strong[问题]：$"softmax"(x)_i = e^(x_i)/sum_j e^(x_j)$。若某个 $x_i = 1 0 0 0$，$e^(1 0 0 0)$ 直接溢出成 #raw("inf")。

#strong[解法]：分子分母同乘 $e^(-m)$（$m=max_j x_j$）： $ "softmax"(x)_i = frac(e^(x_i-m), sum_j e^(x_j-m)) $ 数值上完全等价，但最大指数变成 $e^0=1$，永不溢出。#strong["减最大值"不是技巧，是恒等变形。]

#strong[logsumexp 技巧]：$log sum_j e^(x_j) = m + log sum_j e^(x_j - m)$， 这是所有"用 log 概率做加法"的算法（交叉熵、CTC、HMM、flash attention 的 online softmax）的共同基础。

#strong[为什么这很重要]：课题05 的 #strong[online softmax] 就是"分块计算时如何边算边保持数值稳定"， 其思想内核与这里的减最大值完全一致——#strong[你在 M0 学的东西，会在 Triton kernel 里原样再出现一次。]

#v(4pt)
#line(length: 100%, stroke: 0.6pt + luma(200))
#v(4pt)

== 五、"loss 不降"的排查顺序（把知识变成动作）

+ #strong[数据]：label 与输入错位了吗？分词是否正常（看打印出来的样本）？
+ #strong[初始化]：全零/全同初始化会让对称性无法打破；检查 std 与层数是否匹配
+ #strong[学习率]：太大 → loss 震荡/NaN；太小 → 曲线是平的。先用小数据#strong[能否过拟合一条样本]自检
+ #strong[形状与 mask]：mask 是否在 softmax 之前施加？是否广播到正确维度？
+ #strong[数值]：是否出现 #raw("inf/nan")？打开梯度范数监控
+ #strong[数值精度]：bf16 在小模型/小梯度上可能不够（T4 没有 bf16，课题04 要用 fp16 + GradScaler）

#block(width: 100%, above: 9pt, below: 9pt, inset: (left: 12pt, right: 8pt, y: 6pt), stroke: (left: 3pt + luma(180)), fill: luma(252))[
#text(size: 9.8pt)[
这份顺序本身就是"知行合一"：#strong[它会成为课题04 的排查清单]，而不是一段可背诵的文字。
]
]

#v(4pt)
#line(length: 100%, stroke: 0.6pt + luma(200))
#v(4pt)

== 六、能立刻跑的实验

#block(width: 100%, above: 9pt, below: 9pt, inset: (x: 10pt, y: 8pt), radius: (right: 4pt), fill: luma(248), stroke: (left: 2.5pt + luma(165)))[
  #raw("# ① 手算 bpb 的换算（先自己推，再看输出对不对）
环境/.venv/bin/python - <<'PY'
import math
# 假设某模型：每 token 交叉熵 2.0 nats，平均每个 token 对应 4 个字节
loss_nats, bytes_per_token = 2.0, 4.0
ppl = math.exp(loss_nats)
bpb = loss_nats / math.log(2) / bytes_per_token
print(f\"loss={loss_nats} nats → PPL={ppl:.2f}, bpb={bpb:.3f}\")
print(\"→ 再推一遍：若词表翻倍使 bytes/token 变成 6，bpb 会怎么变？loss 呢？\")
PY

# ② 验证\"减最大值\"是恒等变形（含极端值）
环境/.venv/bin/python - <<'PY'
import numpy as np
x = np.array([0.0, 1000.0, 1000.0])
naive = np.exp(x) / np.exp(x).sum()      # 溢出
stable = np.exp(x - x.max()) / np.exp(x - x.max()).sum()
print(\"naive :\", naive, \" ← 溢出成 nan\")
print(\"stable:\", stable, \" ← 正确\")
PY", block: true, lang: "bash")
]

#v(4pt)
#line(length: 100%, stroke: 0.6pt + luma(200))
#v(4pt)

== 七、代码级提问（3–5 道）

+ #strong[【推导】] 用 $e^(-m)$ 的恒等变形，证明"减最大值"不改变 softmax 的输出（写出两步）。
+ #strong[【估算】] 一个 0.1B 参数模型用 Adam 训练（bf16 参数 + fp32 优化器状态）： ①权重+梯度+优化器状态占多少 GB？②若 T4 只有 16GB，留给激活的预算是多少？
+ #strong[【预测】] 训练中把 loss 从 fp32 计算改成 fp16 计算：训练会更快还是更慢？会出现什么新故障？ （提示：T4 无 bf16；GradScaler 是干什么的）
+ #strong[【联系】] #raw("probability/") 里学过的"期望"和这里的"交叉熵"是同一个东西的两种说法吗？ 试着用期望的符号把交叉熵写出来。
+ #strong[【诊断】] 曲线在 400 步突然 NaN。按本讲 §五 的顺序，你会先看哪三个量？

#v(4pt)
#line(length: 100%, stroke: 0.6pt + luma(200))
#v(4pt)

== 八、记忆锚

- #strong[隐喻]：反向传播 = #strong["责任回溯"]——loss 是最终事故，每个参数按"它贡献了多少"分摊责任； 责任可以累加，所以梯度能攒（梯度累积）。
- #strong[口诀]：#strong["一遍反向、六倍算力、十六字节、先减最大值"] （反向传播一遍 / 6ND / 每参数约 16 字节 / softmax 稳定性）
- #strong[符号位置法]：把 $"bpb" = frac(H, ln 2 ⋅ B)$ 写在卡片中央， #strong[分子 H 是"每 token 的惊讶"，分母 B 是"每 token 的字节"]， 中间一条分数线＝"把单位从 token 换成 byte"——这条线就是跨分词器比较的桥。

#pagebreak()

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

#pagebreak()

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

#pagebreak()

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

#pagebreak()

= 讲义 M4–M9 · 展开大纲（按周写完整版）

#block(width: 100%, above: 9pt, below: 9pt, inset: (left: 12pt, right: 8pt, y: 6pt), stroke: (left: 3pt + luma(180)), fill: luma(252))[
#text(size: 9.8pt)[
说明：本文件是 M4–M9 的#strong[骨架大纲]（核心问题 + 关键概念 + 必读 + 实验 + 坑）， #strong[每周讲课前我会把当周讲义展开成完整版]（新增 #raw("M4-训练.md") 等文件），不留空讲义占位。 这样做的理由：这些模块严重依赖课题04 起的#strong[真实实验数据]，提前写死会出现"讲义与实测不符"。
]
]

#v(4pt)
#line(length: 100%, stroke: 0.6pt + luma(200))
#v(4pt)

== M4 · 训练：数据、优化、系统（W3–W9）

#strong[要回答的问题]：为什么同一个模型有人训得动有人训崩？scaling law 怎么指导算力分配？多卡为什么不是线性加速？

#strong[关键概念]：预训练目标与数据配比 | 过滤与去重 | AdamW（解耦权重衰减的意义）| Muon | LR schedule（warmup + cosine）| 梯度裁剪 | 混合精度（bf16 vs fp16 vs fp32，GradScaler 何时必需）| 梯度累积 | DDP / FSDP / TP / PP | Chinchilla 的 compute-optimal | #raw("--target_flops") 与"固定算力预算下的最优 (N, D)"

#strong[必读]：CS336 lecture 05–11 + A2/A3 handout · #raw("nanochat/optim.py")、#raw("base_train.py")、#raw("runs/scaling_laws.sh") · d2l ch11–ch12

#strong[实验]：手写 AdamW 与调度 → 单卡固定算力下的 depth sweep（d4/d6/d8/d10）→ 拟合幂律 → #strong[先写死外推预测] → 跑 d12 验证（打脸链路）

#strong[坑]：把"loss 不降"当数据问题（常是 LR/初始化/精度）| 把 DDP 当免费加速（PCIe 下扩展效率可能只有 1.3–1.5×）| T4 无 bf16（必须 fp16 + GradScaler）| 显存不足先怀疑 batch 与精度，再怀疑硬件

#v(4pt)
#line(length: 100%, stroke: 0.6pt + luma(200))
#v(4pt)

== M5 · 推理与部署（W5–W8）

#strong[要回答的问题]：为什么生成必须逐 token？KV cache 省了什么、代价是什么？量化掉多少点？吞吐与延迟的取舍？

#strong[关键概念]：自回归解码 | #strong[KV cache（显存公式见 M3 §五）] | continuous batching | PagedAttention | 采样策略（temperature / top-p / top-k / repetition penalty）| 量化（int8/int4/GPTQ/AWQ）| 投机解码 | 每 token 成本

#strong[必读]：#raw("nanochat/engine.py")（KV cache 实现）+ #raw("infer_bench.py") · CS336 lecture 10 · rasbt《Reasoning》ch2

#strong[实验]：从零写带 KV cache 的生成 → 测有/无 cache 的耗时与显存 → 贪心 vs top-p 对照 → batch size 对吞吐的影响

#strong[坑]：以为"慢是因为模型大"（常是没批处理/没 cache）| 以为量化无损 | 忽略 prefill 与 decode 两个阶段特性完全不同（前者算力密集，后者显存带宽密集）

#v(4pt)
#line(length: 100%, stroke: 0.6pt + luma(200))
#v(4pt)

== M6 · 后训练：从"会说话"到"会做事"（W10–W12）

#strong[要回答的问题]：SFT / DPO / RLVR 各补什么能力？为什么 RLVR 提数学/代码却可能伤通用能力？reward hacking 长什么样？

#strong[关键概念]：指令微调与 chat template | #strong[损失掩码（只算 answer 部分）] | 奖励模型 | PPO 的四个模型 | DPO 的隐式奖励（推导：为什么可以不要 reward model）| #strong[GRPO 的组内归一化优势] | KL 正则 | 拒绝采样 | 蒸馏与合成数据 | 过度优化（over-optimization）

#strong[必读]：CS336 A5（含 #raw("tests/test_grpo.py")、GSPO/MaxRL）· #strong[rasbt《Reasoning from Scratch》ch3–ch8] · #strong[Nathan Lambert《RLHF Book》]（免费在线，17 章）· #raw("minimind/trainer/train_grpo.py") · #raw("nano-aha-moment")（单文件）

#strong[实验]：同基座做 SFT / DPO / GRPO 三变体 → 同一评测口径对照 → 手写 GRPO 损失并逐项注释 → #strong[制造一次 reward hacking 并记录]

#strong[坑]：以为 DPO"更简单所以更好"| 以为 RL 一定比 SFT 强 | #strong[把训练 reward 上升当能力提升]（不做 held-out 评测就是自欺）| KL 系数设错导致模型"复读训练集答案"

#v(4pt)
#line(length: 100%, stroke: 0.6pt + luma(200))
#v(4pt)

== M7 · 评测：把"感觉变好了"变成"确实变好了"（W9–W12）

#strong[要回答的问题]：benchmark 分数可信吗？污染怎么判断？为什么必须固定口径？方差有多大？

#strong[关键概念]：bpb / PPL / CORE | 下游基准（GSM8K / MATH-500 / MMLU / HumanEval）| pass\@k | 评测污染 | few-shot 与 prompt 敏感性 | #strong[方差与误差棒] | LLM-as-judge 的偏置 | 可验证奖励 vs 学习型奖励

#strong[必读]：#strong[rasbt ch3（先建评测再上技术——全书教学法基石）] · #raw("nanochat/core_eval.py")（单文件 CORE）· CS336 lecture 12 · Berkeley Agentic AI MOOC 的 "Agent Evaluation" 讲

#strong[实验]：写一个数学题判定器（解析 + 数值比对 + 容错）→ 测它在 200 题上的准确率与#strong[假阳性] → 给两个模型跑同一套评测并给误差棒

#strong[坑]：只看一个 benchmark 下结论 | 忽略 prompt 格式造成的巨大差异 | 把测试集当验证集反复调 | 只报均值不报方差

#v(4pt)
#line(length: 100%, stroke: 0.6pt + luma(200))
#v(4pt)

== M8 · 智能体：工具、记忆、harness、长程任务（W13–W14）

#strong[要回答的问题]：从"回答问题"到"完成任务"缺什么？为什么 harness 比模型本身更决定成败？self-judge 何时有效、何时自欺？

#strong[关键概念]：工具/函数调用 | ReAct 循环（Thought-Action-Observation）| #strong[context engineering]（李宏毅与 Karpathy 都专讲）| 记忆与压缩 | harness 设计（沙箱、权限、反馈信号）| 长程任务的误差累积 | 多智能体 | self-judge / self-refine 的边界 | 可验证环境

#strong[必读]：李宏毅《Context Engineering》专讲 · Berkeley LLM Agents / Agentic AI MOOC（含 "Post-Training Verifiable Agents"）· HF Agents Course（三框架 + 公开排行榜）· rasbt ch5（self-refinement）· #raw("PrimeIntellect-ai/verifiers") · terminal-bench

#strong[实验]：手写最小 ReAct 循环（不用框架）→ 给两个工具（计算器 + 代码执行）→ 记录失败轨迹并分类 → 加 self-judge 做消融

#strong[坑]：以为瓶颈在模型智力（常在你的工具接口与反馈信号）| 以为 self-judge 免费提升（#strong[它会放大原有错误]）| 上下文不做压缩导致长任务后段"忘记目标"

#v(4pt)
#line(length: 100%, stroke: 0.6pt + luma(200))
#v(4pt)

== M9 · 前沿与安全（W15–W16 选题制）

#strong[要回答的问题]：MoE / 长上下文 / 多模态改变了什么？对齐与安全是"加一层"还是"改训练目标"？"AI 训 AI"可行到什么程度？

#strong[关键概念]：MoE 稀疏激活（总参数 vs 激活参数）| 长上下文外推 | 多模态对齐 | 可解释性 | 红队与越狱 | 幻觉的成因 | 合成数据闭环 | self-play | 灾难性遗忘 | 模型合并

#strong[必读]：CS336 lecture 04（MoE）· #raw("opendilab/awesome-RLVR") · #raw("LeapLabTHU/limit-of-RLVR") · 论文精读清单联动

#strong[实验（三选一）]：合成数据自训练一轮 / 拒绝采样提升数学 / self-play 生成题目 → 做最小闭环 + #strong[明确写出这个方向的 no-go]

#strong[坑]：把"前沿"当必须立刻掌握（正确姿势是#strong[保持索引能力 + 每季度更新一次本模块]）| 只看结论不看评测口径 | 把"能跑通"当成"有结论"

#v(4pt)
#line(length: 100%, stroke: 0.6pt + luma(200))
#v(4pt)

== 展开时机表

#block(width: 100%, above: 8pt, below: 10pt)[
#text(size: 9pt)[
  #table(
    columns: (0.322fr, 0.447fr, 0.231fr),
    inset: (x: 7pt, y: 5pt),
    align: left + top,
    stroke: (x, y) => (bottom: if y == 0 { 0.9pt + luma(105) } else { 0.25pt + luma(220) }),
    table.header([讲义文件], [需要先有], [预计展开时间]),
    [#raw("M4-训练.md")], [课题02 收口（能算 FLOPs/显存）], [W3],
    [#raw("M5-推理.md")], [课题04 首轮训练成功（有模型可推理）], [W5],
    [#raw("M7-评测.md")], [有第一个模型输出], [W9],
    [#raw("M6-后训练.md")], [课题07 数据管线 + 评测口径固定], [W10],
    [#raw("M8-智能体.md")], [有 SFT 后的模型], [W13],
    [#raw("M9-前沿.md")], [全部证据齐备], [W15],
  )
]
]
