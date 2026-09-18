
// ══ 讲义排版模板（由 md2typst.py 生成，请勿手改）══
#set document(title: "课题10-长程Agent", author: "孙承泽 · 能动强基2501 · 西安交通大学")

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
    #text(font: SANS, size: 27pt, weight: "bold", fill: ACCENT)[课题10-长程Agent]
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


= 课题10 开题简报 · 长程 Agent 与 self-judge

#block(width: 100%, above: 9pt, below: 9pt, inset: (left: 12pt, right: 8pt, y: 6pt), stroke: (left: 3pt + luma(180)), fill: luma(252))[
#text(size: 9.8pt)[
模块：#strong[M8] ｜ 周次：#strong[W14（12-14→12-20）] ｜ 算力：#strong[T2 Kaggle 2×T4，计划 8 GPU·小时] 唐杰作业对应：#strong[⑤ 训长程 Agent，鼓励 self-judge loop] ｜ 判分来源：#strong[自建]（消融实验 + 轨迹日志） 手写：#strong[R10（self-judge 协议设计）]
]
]

== 一、研究背景

从"回答问题"到"完成任务"的跨越，靠的是 #strong[harness（外壳）]：工具调用、上下文管理、失败重试、自我评估。 Karpathy 与李宏毅都专讲 #strong[context engineering]；nanochat 里 #raw("execution.py") 就是一个最小的"能执行代码的 Agent 外壳"。 本课题的落点是#strong[长程任务]：多步串联后误差累积，以及#strong[self-judge（自我评判）到底有没有用]。

== 二、研究问题

#block(width: 100%, above: 9pt, below: 9pt, inset: (left: 12pt, right: 8pt, y: 6pt), stroke: (left: 3pt + luma(180)), fill: luma(252))[
#text(size: 9.8pt)[
#strong[多步任务中，失败主要来自模型能力还是来自 harness 设计？加上 self-judge loop 后成功率提升多少——还是反而下降？]
]
]

== 三、攻关线索

+ #strong[最小 ReAct]：不用任何框架，手写 #raw("Thought → Action → Observation") 循环（三四十行就能跑）
+ #strong[工具设计]：先给两个工具（计算器 / 受限代码执行）。#strong[工具接口的清晰度往往比模型智力更决定成败]
+ #strong[长程任务构造]：把课题09 的题改造成"需要 3–5 步"的复合任务（如：先算 → 再验 → 再格式化）
+ #strong[失败分类]：格式错 / 工具调错 / 目标漂移（忘了原始要求）/ 循环打转 / 提前放弃
+ #strong[self-judge 的两种形态]：
  - #strong[自评重试]：模型给自己打分，低于阈值就重做（rasbt ch5 的 self-refinement）
  - #strong[自评过滤]：生成多个候选，自己挑最好的（best-of-N 的变体）
+ #strong[关键实验（消融）]：同样的任务集，三组对照 = 无 self-judge / 自评重试 / 自评过滤
+ #strong[警惕]：self-judge #strong[会放大原有错误]（模型判不出自己错在哪，反而确信）→ 必须留失败案例

== 四、里程碑

- □ M1 手写最小 ReAct 循环（无框架），跑通单步任务
- □ M2 加入第二个工具 + 多步任务集（≥30 个任务）
- □ M3 #strong[轨迹记录规范]：每步的 thought/action/observation 落盘（可复现）
- □ M4 基线成功率 + #strong[失败五分类]（每类给 2 个真实案例）
- □ M5 #strong[self-judge 消融]：三组对照，给出成功率差与误差棒
- □ M6 #strong[反例收集]：找出 ≥3 个"self-judge 导致更差"的案例并解释机制
- □ M7 一页报告 + 知识卡

== 五、交付物

#block(width: 100%, above: 8pt, below: 10pt)[
#text(size: 9pt)[
  #table(
    columns: (0.283fr, 0.339fr, 0.378fr),
    inset: (x: 7pt, y: 5pt),
    align: left + top,
    stroke: (x, y) => (bottom: if y == 0 { 0.9pt + luma(105) } else { 0.25pt + luma(220) }),
    table.header([交付物], [位置], [验收]),
    [ReAct 循环], [#raw("手写/")], [可跑通多步任务],
    [self-judge 协议], [#raw("手写/")（R10）], [有明确的判定时机与阈值设计说明],
    [轨迹日志], [#raw("证据/trajectories/")], [每任务一份，含步数与结果],
    [消融数据], [#raw("证据/")], [三组成功率 + 误差棒],
    [报告], [#raw("报告.md")], [必须回答"何时 self-judge 有害"],
  )
]
]

== 六、讲课锚点

- #strong[讲义]：#raw("M8-智能体.md")（W13 展开）
- #strong[对标]：#strong[李宏毅《Context Engineering》专讲]（Agent 时代的关键技术）· Berkeley LLM Agents MOOC（ReAct 原始论文那讲）· HF Agents Course（三框架对照 + 观测性/评测 bonus unit）· #strong[rasbt ch5（self-refinement）] · #raw("nanochat/execution.py")+#raw("tests/test_execution.py")（#strong[沙箱执行的最小实现]，可读接口不可抄实现）
- #strong[搭桥]：M5 的 KV cache（长上下文的显存代价）→ 为什么长程 Agent 必须做#strong[上下文压缩]

== 七、代码级提问示例

+ 长程任务失败率随步数指数上升。#strong[分解]：是每步错误率问题，还是错误会累积传播？
+ self-judge 什么时候#strong[一定]无效？（提示：当模型无法区分"看起来对"和"真的对"时）
+ 上下文压缩（截断/摘要）会引入什么新失败模式？
+ 为什么"工具返回值要结构化"能显著提升成功率？（从 token 分布角度解释）
+ #strong[【下注】] 预测 self-judge 在简单任务 vs 困难任务上的效果差异，先写再测。

== 八、风险与提醒

- ❗ #strong[不要用框架起步]：手写一遍 ReAct 再去看 LangGraph/smolagents，否则学不到 harness 的本质。
- ⚠ self-judge 会显著增加 token 消耗与时间 → 算力预算要写进实验卡。
- ⚠ 轨迹日志可能很大 → 只保留结构化摘要（thought 截断 + 结果），避免污染仓库体积。
