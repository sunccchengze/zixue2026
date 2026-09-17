
// ══ 讲义排版模板（由 md2typst.py 生成，请勿手改）══
#set document(title: "M0 · 数学与机器学习地基", author: "孙承泽 · 能动强基2501 · 西安交通大学")

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
    #text(font: SANS, size: 27pt, weight: "bold", fill: ACCENT)[M0 · 数学与机器学习地基]
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
