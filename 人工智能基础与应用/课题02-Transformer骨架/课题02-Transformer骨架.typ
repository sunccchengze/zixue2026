
// ══ 讲义排版模板（由 md2typst.py 生成，请勿手改）══
#set document(title: "课题02-Transformer骨架", author: "孙承泽 · 能动强基2501 · 西安交通大学")

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
    #text(font: SANS, size: 27pt, weight: "bold", fill: ACCENT)[课题02-Transformer骨架]
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


= 课题02 开题简报 · Transformer 骨架与训练循环

#block(width: 100%, above: 9pt, below: 9pt, inset: (left: 12pt, right: 8pt, y: 6pt), stroke: (left: 3pt + luma(180)), fill: luma(252))[
#text(size: 9.8pt)[
模块：#strong[M0/M1/M3] ｜ 周次：#strong[W2–W3（09-21→10-04）] ｜ 算力：#strong[T0 纯 CPU，0 GPU·小时] 唐杰作业对应：#strong[① 从零写 Transformer] 的后半 ｜ 判分来源：#strong[CS336 A1 #raw("tests/test_model.py")、#raw("test_nn_utils.py")、#raw("test_optimizer.py")、#raw("test_serialization.py")] 手写：#strong[R2（Transformer 全部组件）+ R3（训练循环与优化器）+ R4（反向传播验证）]
]
]

#v(4pt)
#line(length: 100%, stroke: 0.6pt + luma(200))
#v(4pt)

== 一、研究背景

2017 年《Attention Is All You Need》删掉 RNN，用自注意力 + 前馈层实现 #strong[O(1) 依赖路径 + 全并行]。 此后所有主流大模型都是它的变体，但#strong[细节已经换了一轮]：正弦位置编码 → RoPE；LayerNorm → RMSNorm； post-norm → pre-norm；ReLU MLP → SwiGLU；MHA → GQA。#strong[本课题要求你把现代版写出来，而不是复刻 2017 版。]

== 二、研究问题（一句话）

#block(width: 100%, above: 9pt, below: 9pt, inset: (left: 12pt, right: 8pt, y: 6pt), stroke: (left: 3pt + luma(180)), fill: luma(252))[
#text(size: 9.8pt)[
#strong[一个"能从零训起来"的现代 Transformer 层，最少需要哪几个组件？每个组件去掉之后，训练会以什么方式失败？]
]
]

== 三、攻关线索

+ #strong[形状先行]：写下每一步的张量形状（含 batch、序列、头数），#strong[先能在纸上跑通]，再写代码。
+ #strong[注意力的三个动作]：投影出 Q/K/V → 缩放点积 + 因果掩码 → softmax 加权求和并输出投影。哪一步最容易错？为什么？
+ #strong[位置信息]：RoPE 为什么是"旋转 Q/K"而不是"加到输入上"？（讲义 M3 §三给了恒等式）
+ #strong[归一化与残差]：为什么 pre-norm 比 post-norm 好训？残差提供了什么"通路"？
+ #strong[优化器]：AdamW 里"解耦权重衰减"解耦的是什么？为什么它比 L2 正则更常用？
+ #strong[稳定性]：梯度裁剪在什么情况下救命？fp16 vs bf16 的差别如何影响 loss 曲线？

== 四、里程碑

- □ M1 手写全部组件：注意力（含因果 mask 与 RoPE）、RMSNorm、SwiGLU FFN、残差堆叠、初始化
- □ M2 形状与数值判分通过：#raw("test_model.py") / #raw("test_nn_utils.py") 全绿
- □ M3 手写训练循环 + AdamW + LR 调度 + 梯度裁剪 → #raw("test_optimizer.py") / #raw("test_serialization.py") 全绿
- □ M4 端到端：#strong[CPU 上训一个极小模型（d4–d8），loss 稳定下降]，并保存/加载 checkpoint 续训成功
- □ M5 #strong[R4 反向传播验证]：与 PyTorch autograd 的数值梯度对照（相对误差 \< 1e-6）
- □ M6 #strong[三组改坏实验]（去 mask / 换位置编码 / 去残差）：每组先写预测，再跑，再记录
- □ M7 一页报告 + 知识卡 ≥3 张

== 五、交付物

#block(width: 100%, above: 8pt, below: 10pt)[
#text(size: 9pt)[
  #table(
    columns: (0.245fr, 0.330fr, 0.425fr),
    inset: (x: 7pt, y: 5pt),
    align: left + top,
    stroke: (x, y) => (bottom: if y == 0 { 0.9pt + luma(105) } else { 0.25pt + luma(220) }),
    table.header([交付物], [位置], [验收]),
    [实现], [#raw("手写/")（你写）], [M2/M3 判分全绿],
    [判分输出], [#raw("判卷记录.md")], [#raw("证据/judge-*.log") 原文],
    [改坏实验记录], [#raw("证据/改坏实验.md")], [预测→现象→解释 三段齐全],
    [loss 曲线], [#raw("证据/")], [训练日志 + 图（含坐标轴与步数）],
    [报告], [#raw("报告.md")], [一页四段],
  )
]
]

== 六、讲课锚点（讲义 M3 + 对标）

- #strong[讲义]：#raw("讲义/M3-Transformer内部机制.md")（主干）+ #raw("讲义/M0-数学与机器学习地基.md")（§一 自动微分、§五 排查顺序）
- #strong[对标]：CS336 lecture 03–04 · rasbt ch3–ch4 · 李沐 d2l ch10–ch11
- #strong[必备工具链]：#raw("bash 环境/bootstrap_cpu.sh --with-torch")（本课题起需要 torch）

== 七、代码级提问示例（讲课中出，先预测后验证）

+ 把因果 mask 从 softmax #strong[之前]挪到#strong[之后]，训练现象会怎样？
+ 去掉残差后，4 层还能训、12 层完全不动——请用梯度路径解释。
+ 你把 RoPE 的最大频率底数从 10000 改成 100：短文训练会受影响吗？长上下文外推呢？
+ AdamW 的 #raw("weight_decay") 若改成"直接加到梯度上"（即 L2），在大学习率下会出现什么差异？

== 八、风险与提醒

- ⚠ #strong[CPU 训练极慢]：本课题#strong[只要能训起来、loss 下降]即可，不追求指标（真训练在课题04）。
- ⚠ 形状错误是最高频故障：#strong[先写形状注释再写实现]，可省一半时间。
- ⚠ 判分器需要 torch；#raw("bootstrap --with-torch") 首次约 555MB（沙箱网络受限时可能失败，届时改用 Kaggle CPU 会话）。
