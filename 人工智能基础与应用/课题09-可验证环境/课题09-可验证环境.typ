
// ══ 讲义排版模板（由 md2typst.py 生成，请勿手改）══
#set document(title: "课题09-可验证环境", author: "孙承泽 · 能动强基2501 · 西安交通大学")

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
    #text(font: SANS, size: 27pt, weight: "bold", fill: ACCENT)[课题09-可验证环境]
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


= 课题09 开题简报 · 可验证环境 + harness

#block(width: 100%, above: 9pt, below: 9pt, inset: (left: 12pt, right: 8pt, y: 6pt), stroke: (left: 3pt + luma(180)), fill: luma(252))[
#text(size: 9.8pt)[
模块：#strong[M7/M8] ｜ 周次：#strong[W13（12-07→12-13）] ｜ 算力：#strong[T2 Kaggle 2×T4，计划 6 GPU·小时] 唐杰作业对应：#strong[⑤ 搭可验证环境 + harness] ｜ 判分来源：#strong[自建]（判定逻辑单测 + rollout 成功率） 手写：#strong[R9（判定逻辑 / verifier）]
]
]

== 一、研究背景

2026 年的关键词是"#strong[可验证奖励]"：与其训练一个会拍马屁的奖励模型，不如#strong[造一个能判定对错的环境]。 CS336 没有这一环，Berkeley Agentic AI MOOC 专门有一讲叫 "Post-Training Verifiable Agents"， #raw("PrimeIntellect-ai/verifiers") 把它抽象成库。唐杰作业⑤要求"搭可验证环境 + harness"正是这个方向。

#strong["可验证"的三要素]：①任务是可判定的（不是主观好坏）②环境能给出稳定反馈 ③harness 能重复运行并复现。

== 二、研究问题

#block(width: 100%, above: 9pt, below: 9pt, inset: (left: 12pt, right: 8pt, y: 6pt), stroke: (left: 3pt + luma(180)), fill: luma(252))[
#text(size: 9.8pt)[
#strong[我能为一个小模型设计一个"可自动判定"的任务环境吗？判定逻辑的假阳性/假阴性有多高？模型在这个环境里的成功率是多少？]
]
]

== 三、攻关线索

+ #strong[选题]：从三个里选一个（按成本从低到高）
  - ①#strong[数学题解答]（用数值比对 + 容错；MATH-500 风格）
  - ②#strong[函数补全]（隐藏单元测试；本质是迷你 HumanEval）
  - ③#strong[格式约束生成]（如严格 JSON / 表格填充，规则判定）
+ #strong[判定逻辑的三大坑]：等价但不相同（#raw("1/2") vs #raw("0.5")）、解析失败当错、#strong[边界用例漏判]
+ #strong[假阳性检测]：人为构造"错误但能骗过判定器"的答案 → 测出#strong[假阳性率]（这是质量的核心指标）
+ #strong[harness 设计]：任务装载 → 模型生成 → 判定 → 记录轨迹 → 复现（固定种子）
+ #strong[可重复性]：同一批任务跑两次，成功率波动多大？（#strong[误差棒思维]，M7 讲过）
+ #strong[对照]：可验证奖励 vs 规则弱判定（如只看格式），用同一模型比成功率差异

== 四、里程碑

- □ M1 选定任务类型，写 30–100 道题的#strong[题集]（含标准答案与判定规则）
- □ M2 #strong[判定逻辑单测]：等价形式、边界、异常输入（≥10 个用例）
- □ M3 #strong[假阳性实验]：构造 10 个"错误但可能蒙混"的答案，测出漏判率
- □ M4 harness 跑通：给基座模型跑一遍，得成功率 + 失败样本
- □ M5 失败分类：把失败归成 3–5 类（格式错 / 计算错 / 中途放弃 / 判定器误杀）
- □ M6 一页报告：#strong[判定器质量 + 模型表现 两个都要报]

== 五、交付物

#block(width: 100%, above: 8pt, below: 10pt)[
#text(size: 9pt)[
  #table(
    columns: (0.312fr, 0.376fr, 0.312fr),
    inset: (x: 7pt, y: 5pt),
    align: left + top,
    stroke: (x, y) => (bottom: if y == 0 { 0.9pt + luma(105) } else { 0.25pt + luma(220) }),
    table.header([交付物], [位置], [验收]),
    [题集与判定器], [#raw("手写/")（判定逻辑 R9）], [M2 单测通过],
    [harness 脚本], [#raw("脚手架/")（B3）], [固定种子可复跑],
    [失败样本], [#raw("证据/")], [≥20 条，分类标注],
    [假阳性报告], [#raw("报告.md")], [含漏判率与典型案例],
  )
]
]

== 六、讲课锚点

- #strong[讲义]：#raw("M8-智能体.md")（W13 展开）
- #strong[对标]：Berkeley Agentic AI MOOC 的 "Post-Training Verifiable Agents" 与 "Agent Evaluation" 讲 · #raw("PrimeIntellect-ai/verifiers")（#strong[只读概念，不引入代码]）· #raw("harbor-framework/terminal-bench") 的任务设计思路 · #strong[rasbt ch3]（评测器设计：解析 + verifier + 基准式检查）

== 七、代码级提问示例

+ 你的判定器把 #raw("1/2") 判错、把 #raw("0.50") 判对——这属于哪一类错误？如何系统性避免？
+ 假阳性率高会导致 RL 训练出现什么后果？（联系课题08 的 reward hacking）
+ 同一批任务两次运行成功率差 8%。你会先怀疑模型还是 harness？怎么验证？
+ 为什么"用 LLM 当裁判"在可验证任务上通常是#strong[退步]？

== 八、风险与提醒

- ⚠ #strong[判定器本身也要被评测]：只报模型成功率不报判定器质量，是不完整的实验。
- ⚠ 题集不要抄公开 benchmark（污染问题），#strong[自己出题 + 自己判定]才是本课题的价值。
- ⚠ 配额有限：优先"题集质量高、任务简单"，不要一上来做代码执行沙箱（那是课题10 的事）。
