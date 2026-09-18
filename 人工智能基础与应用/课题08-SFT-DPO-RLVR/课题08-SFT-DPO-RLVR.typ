
// ══ 讲义排版模板（由 md2typst.py 生成，请勿手改）══
#set document(title: "课题08-SFT-DPO-RLVR", author: "孙承泽 · 能动强基2501 · 西安交通大学")

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
    #text(font: SANS, size: 27pt, weight: "bold", fill: ACCENT)[课题08-SFT-DPO-RLVR]
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


= 课题08 开题简报 · SFT / DPO / RLVR 三方对照

#block(width: 100%, above: 9pt, below: 9pt, inset: (left: 12pt, right: 8pt, y: 6pt), stroke: (left: 3pt + luma(180)), fill: luma(252))[
#text(size: 9.8pt)[
模块：#strong[M6/M7] ｜ 周次：#strong[W11–W12（11-23→12-06）] ｜ 算力：#strong[T2 Kaggle 2×T4，计划 18 GPU·小时（全学期最贵）] 唐杰作业对应：#strong[④ 同一基座上把 SFT、DPO、RLVR 做对照] ｜ 判分来源：#strong[CS336 A5 #raw("tests/test_grpo.py")] + 自建三方对照 手写：#strong[R7（损失函数与优势估计）]
]
]

== 一、研究背景

预训练给"知识"，后训练给"行为"。三条主流路线：

#block(width: 100%, above: 8pt, below: 10pt)[
#text(size: 9pt)[
  #table(
    columns: (0.228fr, 0.356fr, 0.417fr),
    inset: (x: 7pt, y: 5pt),
    align: left + top,
    stroke: (x, y) => (bottom: if y == 0 { 0.9pt + luma(105) } else { 0.25pt + luma(220) }),
    table.header([方法], [需要什么], [优化什么]),
    [#strong[SFT]], [(指令, 回答) 对], [最大似然（只对回答部分算 loss）],
    [#strong[DPO]], [(指令, 好回答, 坏回答) 偏好对], [隐式奖励差（无需显式 reward model）],
    [#strong[RLVR]], [可判对错的答案 + 验证器], [期望可验证奖励（GRPO 用组内相对优势）],
  )
]
]

#strong[本课题的教学价值极高]：它是课程大纲"机器学习（强化学习）"与唐杰作业④的交点， 也是"知识讲解"最能发挥的地方——#strong[GRPO 的每一项都能在概率论里找到根]（期望、方差、条件期望）。

== 二、研究问题

#block(width: 100%, above: 9pt, below: 9pt, inset: (left: 12pt, right: 8pt, y: 6pt), stroke: (left: 3pt + luma(180)), fill: luma(252))[
#text(size: 9.8pt)[
#strong[同一个基座、同一套评测，SFT / DPO / RLVR 各自把什么能力提升了、把什么能力损害了？训练奖励的上升，有多少是真的能力提升？]
]
]

== 三、攻关线索

+ #strong[基座与数据]：基座用课题04 的模型（或 0.1B 级开源小模型）；任务是#strong[可验证]的（数学题/格式约束/单元测试）
+ #strong[SFT 的损失掩码]：#strong[只对回答部分算 loss]，指令部分不算 —— 这是个高频错误点
+ #strong[DPO 的推导]：为什么 $sigma(beta log frac(pi(y_w), pi_(r e f)(y_w)) - beta log frac(pi(y_l), pi_(r e f)(y_l)))$ 能等价于"隐式奖励"？
+ #strong[GRPO 的四步]：采样一组输出 $G$ 个 → 打分 → #strong[组内归一化得优势] $A_i = frac(r_i - "mean"(r), "std"(r))$ → 加权策略梯度 + KL 惩罚
+ #strong[KL 惩罚的作用]：防止策略跑离参考模型太远（对应 RLHF Book 的"过度优化"章）
+ #strong[评测口径]：#strong[训练奖励 ≠ 能力]。必须在 held-out 题集上评，并且给误差棒
+ #strong[制造一次 reward hacking]：例如让模型学到"输出格式对了但答案是瞎猜"，记录现象（这是本课题最好的素材）

== 四、里程碑

- □ M1 SFT 基线（含损失掩码正确性验证：打印一条样本的 mask）
- □ M2 DPO 跑通 + 与 SFT 的对照（held-out）
- □ M3 手写 GRPO 损失并#strong[逐项注释]（优势从哪来、为什么要除标准差）
- □ M4 #raw("tests/test_grpo.py") 通过（判分器接入后）
- □ M5 #strong[三方对照表]（同基座、同评测、同种子策略，带误差棒）
- □ M6 #strong[reward hacking 实验]：故意设计一个"可被钻空子"的奖励，观察并记录
- □ M7 一页报告 + 知识卡（GRPO 递推必须能徒手推）

== 五、交付物

#block(width: 100%, above: 8pt, below: 10pt)[
#text(size: 9pt)[
  #table(
    columns: (0.320fr, 0.330fr, 0.350fr),
    inset: (x: 7pt, y: 5pt),
    align: left + top,
    stroke: (x, y) => (bottom: if y == 0 { 0.9pt + luma(105) } else { 0.25pt + luma(220) }),
    table.header([交付物], [位置], [验收]),
    [三个训练脚本], [#raw("手写/")（损失与优势估计属 R7）], [可复跑],
    [判分输出], [#raw("判卷记录.md")], [#raw("test_grpo.py") 原文],
    [对照表], [#raw("证据/")], [含误差棒与评测口径说明],
    [reward hacking 记录], [#raw("证据/")], [现象 + 机制解释],
    [报告], [#raw("报告.md")], ["能力提升 vs 训练奖励"必须分开讨论],
  )
]
]

== 六、讲课锚点

- #strong[讲义]：#raw("M6-后训练.md")（W10 展开）
- #strong[对标]：#strong[rasbt《Reasoning from Scratch》ch3（先建评测）+ ch6–ch7（GRPO）] · #strong[《RLHF Book》ch4/6/8/14] · CS336 A5 + lecture 15–17 · #raw("minimind/trainer/train_grpo.py")（中文工程实现）· #raw("nano-aha-moment")（单文件）
- #strong[搭桥（重点）]：#raw("probability/") 的#strong[期望、方差、条件期望]——GRPO 的优势归一化就是"标准化"， KL 惩罚就是"分布差异"，REINFORCE 就是"用样本均值估期望"

== 七、代码级提问示例

+ 为什么 SFT 只对回答部分算 loss？若指令部分也算，会发生什么？
+ GRPO 里为什么要除以组内标准差？如果一组所有奖励#strong[完全相同]，优势是多少？这时梯度会怎样？
+ DPO 不需要 reward model，那它的"奖励"藏在哪？（用对数比写出来）
+ 训练奖励从 0.3 涨到 0.8，held-out 准确率却从 40% 掉到 35%。列出三个可能原因。
+ #strong[【下注】] 预测三方在 held-out 上的排序，先写再测。

== 八、风险与提醒

- ❗ #strong[最贵的一周]：18 GPU·小时是全学期 1/5，#strong[三个方法各只跑一次正式实验]，其余用小规模调试。
- ❗ #strong[不做 held-out 评测就等于自欺]：训练奖励必须与独立评测同时报（写进报告硬要求）。
- ⚠ A5 官方仓库#strong[未声明 SPDX 许可] → 只做本地学习对照，不复制进仓（见《上游锁定清单》§三）。
- ⚠ Kaggle 会话上限 9–12h：RL 训练务必支持#strong[断点续训]，否则一次会话跑不完。
