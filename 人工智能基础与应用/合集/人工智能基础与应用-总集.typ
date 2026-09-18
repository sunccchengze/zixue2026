
// ══ 讲义排版模板（由 md2typst.py 生成，请勿手改）══
#set document(title: "人工智能基础与应用-总集", author: "孙承泽 · 能动强基2501 · 西安交通大学")

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
    #text(font: SANS, size: 27pt, weight: "bold", fill: ACCENT)[人工智能基础与应用-总集]
    #v(0.5cm)
    #text(font: SANS, size: 12.5pt, fill: ACCENT2)[人工智能基础与应用 · 大模型实训]
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

= 人工智能基础与应用 I · 学科 README（课程轨 + 实训轨 双轨合一）

#block(width: 100%, above: 9pt, below: 9pt, inset: (left: 12pt, right: 8pt, y: 6pt), stroke: (left: 3pt + luma(180)), fill: luma(252))[
#text(size: 9.8pt)[
2026-09-17 立（由"任务型轻工作台"升级为#strong[双轨标准骨架]，升级条件由本 README 旧版预留）。 本文件夹同时承载三件事： #strong[① 课程轨]——CORE100299 的课堂事务（考勤、随堂作业、大论文 70%）； #strong[② 实训轨]——把唐杰 2026 秋季作业清单（7 条）与 CS336 五份作业在#strong[零预算]下走完的 11 个课题； #strong[③ 知识轨]——大语言模型 M0–M9 全景知识地图，知行合一。

两条轨共用一套 memory、一套证据规范、一套判分器——#strong[同一份劳动产出两种成绩]（课程大论文 = 实训中期的技术报告）。
]
]

== 必读顺序（新会话照此开局，不许跳）

+ 仓库根 #raw("AGENTS.md")（回合级 commit+push 是全仓库最高优先级）
+ #raw("_开局指令-给新会话Agent.md")（本学科唯一入口）
+ #raw("memory/HANDOFF.md")（现在卡在哪、下一句该问什么）
+ #raw("章程与地图/造轮子边界.md")（★ 谁写代码——本学科最易出事故处）
+ #raw("章程与地图/知行合一规程.md")（★ 什么叫"学过"）
+ 其余按需：#raw("知识地图-大模型全景.md")（学什么）/ #raw("实训路线图.md")（何时学）/ #raw("对标教学资源清单.md")（跟谁学）/ #raw("算力与成本预算.md")（花多少）/ #raw("判分与验收标准.md")（怎么算过）/ #raw("AI使用红线.md")（我能不能写）/ #raw("上游锁定清单.md")（依赖哪个版本）

== 课程档案（CORE100299，2026-09-16 首课）

- #strong[推荐教材]：辛景民、武佳懿、郑南宁主编《人工智能概论》，清华大学出版社，2025
- #strong[考核]：课程大论文 #strong[70%] + 平时 #strong[30%]（随堂作业 + 考勤）；#strong[无期末笔试]
- #strong[时间]：1–8 周，周三 9–10 节 + 周五 9–10 节，东1东-328（陈炜煌）
- #strong[大纲六板块]：绪论 / 搜索求解 / 知识表示 / 机器学习 / 智能体 / 大语言模型
- 详见 #raw("资料原件/首课信息-20260916.md")

== 目录地图

#block(width: 100%, above: 9pt, below: 9pt, inset: (x: 10pt, y: 8pt), radius: (right: 4pt), fill: luma(248), stroke: (left: 2.5pt + luma(165)))[
  #raw("人工智能基础与应用/
├── README.md                    本文件（双轨导游图）
├── _开局指令-给新会话Agent.md     唯一入口
├── 章程与地图/                   本学科\"宪法层\"
│   ├── 知识地图-大模型全景.md  ⭐  M0–M9：学什么（四件咬合：问题/对标/实验/证据）
│   ├── 对标教学资源清单.md    ⭐  跟谁学（22 项已核实资源 + 8 条坑）
│   ├── 知行合一规程.md        ⭐  什么叫学过（四件咬合 + 代码级提问 + 三条硬标准）
│   ├── 实训路线图.md              何时学（16 周 × 11 课题 × 唐杰7条 × CS336 + 知识讲解锚点）
│   ├── 造轮子边界.md          ⭐  谁写代码（手写 R1–R10 / 代写 B1–B8 / 协作 C1–C4）
│   ├── AI使用红线.md              双轨制下 Agent 的红线与例外
│   ├── 算力与成本预算.md      ⭐  零预算编排（Kaggle 30h/周 ×2×T4 + 实验卡制度 + 配额账本）
│   ├── 判分与验收标准.md          三层判分 + 每课题通过证据
│   └── 上游锁定清单.md        ⭐  repo + commit + 许可 + 只用哪些路径
├── 讲义/                    ⭐私有  知识讲解主库（三师制中\"我\"那一腿）
│   ├── pdf/                       📕 PDF 成品：全书 23 页 + 单讲分册（下载即可读）
│   ├── README.md                  使用方法 + 讲义规范（8 件套）+ 展开状态表 + PDF 下载
│   ├── M0-数学与机器学习地基.md     自动微分/熵与bpb/算力显存记账/数值稳定性/排查顺序
│   ├── M1-从n-gram到Transformer.md n-gram/词向量/RNN/seq2seq+注意力/并行性
│   ├── M2-分词与表示.md            压缩视角/字节起步/算法复杂度/编码回放/接口与内存
│   ├── M3-Transformer内部机制.md   注意力与缩放/多头/GQA/RoPE/RMSNorm/SwiGLU/参数量/KV cache
│   └── M4-M9-待展开大纲.md         M4–M9 骨架大纲 + 展开时机表
├── 课程轨/                      课堂事务（本学科私有目录，已登记）
│   ├── 课程进度.md               8 周 × 16 次课的进度锚点 + 作业/考勤台账
│   └── 大论文/                   选题 → 提纲 → 初稿 → 终稿（70% 成绩）
├── 资料原件/ 资料文本/           首课信息、活动留档、教材章节索引、讲义提取文本
├── 环境/                  ⭐私有  脚手架区（已实跑验证）
│   ├── bootstrap_cpu.sh          T0 环境（轻量档 9 秒；--with-torch 可选）
│   ├── 预检.md                   会话门禁（P100 一票否决）+ 实验卡制度
│   ├── judge/                    CS336 官方判分器接入（test_*.py 未改一字）+ tiktoken 离线词表
│   ├── 归档/make_run.py          证据归档：run.yaml（commit/预测/预算/产物哈希）
│   ├── 报告模板/                 一页四段（中文）+ NeurIPS 骨架（英文）
│   └── pdf/                      📕 讲义排版链：md2typst.py + 一键脚本 + 字体（详见其 README）
├── memory/                      记忆系统六件 + drill-ledger
├── 知识卡/                       （可选，量大时启用）知识卡索引 → 见知行合一规程 §二
└── 课题01-BPE分词器/ … 课题11-结项/   作战单元（**11 份开题简报已全部就位**）", block: true)
]

#strong[私有目录登记]（依 #raw("仓库使用手册.md") §二）：#raw("课程轨/")、#raw("环境/")、#raw("知识卡/")，以及各课题下的 #raw("手写/")、#raw("脚手架/")、#raw("证据/") 三个子目录，均为本学科私有约定，已在此登记。

== 课题单元形态

#block(width: 100%, above: 9pt, below: 9pt, inset: (x: 10pt, y: 8pt), radius: (right: 4pt), fill: luma(248), stroke: (left: 2.5pt + luma(165)))[
  #raw("课题NN-名称/
├── 开题简报.md      背景 → 研究问题 → 攻关线索 → 里程碑 → 交付物
├── 手写/            ⭐ 学习目标代码；Agent 只读禁写（见 造轮子边界.md）
├── 脚手架/          ⭐ Agent 全权负责：编排/日志/绘图/判分/归档
├── 证据/            ⭐ run.yaml + 日志 + 曲线 + 产物哈希 + 结论与反证（no-go 不擦除）
├── 报告.md          一页四段（问题-动机-方法-结果）
└── 判卷记录.md      自动判分结果 + 导师审稿 3–5 条 + 费曼收口记录", block: true)
]

== 当前状态（只改这一行，细节进 memory）

● #strong[2026-09-17 可开课，教材已可下载]：三轨骨架 + 9 份章程 + 讲义库（M0/M1/M2/M3 全文 + M4–M9 大纲）

- #strong[11 份课题开题简报全部就位] + 判分器实跑接通 + 证据归档工具 + #strong[讲义 PDF 全书 23 页 / 章程合订 28 页]；

下一步 = #strong[课题01 开题（BPE 分词器，纯 CPU，0 算力）]，同步启动课程大论文选题。

📕 #strong[想读 PDF]：#raw("讲义/pdf/大模型实训讲义-全书.pdf")（首选）· #raw("章程与地图/pdf/章程与地图-全书.pdf")

== 一课两用（本学科最大红利）

#block(width: 100%, above: 8pt, below: 10pt)[
#text(size: 9pt)[
  #table(
    columns: (0.302fr, 0.219fr, 0.479fr),
    inset: (x: 7pt, y: 5pt),
    align: left + top,
    stroke: (x, y) => (bottom: if y == 0 { 0.9pt + luma(105) } else { 0.25pt + luma(220) }),
    table.header([课程要求], [实训轨对应], [复用方式]),
    [大论文 70%（第 8 周结课前）], [课题01–05 的成果], [大论文 = 实训前五课题的#strong[中文技术报告]（选题可联动 #raw("turbine-blade-ai-platform")）],
    [随堂作业 30%], [每课题的判分记录 / 知识卡], [直接取用，零额外劳动],
    [六板块（搜索/知识表示/机器学习/智能体/LLM）], [M0–M9 知识地图], [见《知识地图》末尾的板块映射表],
  )
]
]

== 与其它学科联动

- #raw("probability/")：RL 的期望/方差/条件期望地基已建成 → 讲 GRPO 时直接搭桥，不重讲
- #raw("论文精读/")：Chinchilla / DPO / GRPO / ReAct / SWE-agent 等论文走论文精读流程
- #raw("turbine-blade-ai-platform")（用户真实项目）：大论文与结项报告的应用案例来源

#pagebreak()

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

#pagebreak()

= 知识地图 · 大语言模型全景（M0–M9）

#block(width: 100%, above: 9pt, below: 9pt, inset: (left: 12pt, right: 8pt, y: 6pt), stroke: (left: 3pt + luma(180)), fill: luma(252))[
#text(size: 9.8pt)[
立图 2026-09-17。#strong[本文件回答一个问题：要把大语言模型"彻底搞懂"，到底要懂哪些东西。] 每个模块都是"#strong[四个咬合件]"：核心问题 → 对标材料 → 亲手实验 → 判分证据。 只讲不做 = 没学（见《知行合一规程.md》）；只做不讲 = 学歪。

用法：模块不是线性章节，但#strong[顺序有依赖]（M0→M1→M2→M3→M4→M5→M6→M7→M8→M9）。 每周讲哪个模块，见《实训路线图.md》的"知识讲解锚点"列。
]
]

== 判断"真的懂了"的三条硬标准（本学科通用）

+ #strong[能讲清]：不用术语、用大白话讲给外行听，且能回答"为什么不是别的做法"。
+ #strong[能指出代码位置]：说出这个概念在本仓 #raw("手写/") 或上游 nanochat/CS336 里#strong[具体是哪个函数、哪几行]。
+ #strong[能改坏并修好]：故意改坏（去掉 mask、换掉归一化、打乱位置编码）→ #strong[预测]现象 → 跑实验验证 → 修回。 （第 3 条是"知"与"行"的分界线；只会背定义的人在第三步一定翻车。）

#v(4pt)
#line(length: 100%, stroke: 0.6pt + luma(200))
#v(4pt)

== M0 · 数学与机器学习地基

- #strong[核心问题]：梯度到底怎么传过 100 层？为什么归一化能让训练稳下来？交叉熵、困惑度、bpb 三者的关系是什么？参数量/FLOPs/显存怎么估？
- #strong[关键概念]：链式法则与计算图、雅可比、损失函数（MSE/交叉熵）、梯度下降族、正则化、数值稳定性、信息量与熵、复杂度记账（6ND 公式）
- #strong[对标]：李沐《动手学深度学习》ch2–ch5、ch11（优化算法）；Karpathy micrograd 视频；概率论课题01–08（已建成，直接搭桥）
- #strong[亲手实验]：手写 micrograd（标量自动微分，200 行内）→ 手写 MLP 在 MNIST 子集上训到 \>95%
- #strong[判分证据]：与 PyTorch autograd 的数值梯度对照表（误差 \< 1e-6）+ 参数量/FLOPs 估算脚本实测偏差
- #strong[常见误解]：把 loss 当"正确率"；以为"梯度消失"是 bug 而不是结构性质；以为 d2l 的 MXNet 代码不用改

== M1 · 语言模型史与前 Transformer 时代

- #strong[核心问题]：Transformer 解决了什么前人的痛点？为什么 attention 取代了 RNN？"语言模型"这个词 20 年里的含义变化？
- #strong[关键概念]：n-gram 与平滑、词袋、word2vec/GloVe、RNN/LSTM/GRU、seq2seq + 注意力、Bahdanau/Luong attention、并行化的动机
- #strong[对标]：李沐 d2l ch8–ch10（RNN → 注意力）；CS336 lecture 01（概览与分词）；《Attention Is All You Need》原文（入论文精读）
- #strong[亲手实验]：手写 bigram/trigram 语言模型算困惑度 → 手写一个最小 RNN LM → 对比同参数量的单层 Transformer
- #strong[判分证据]：三者在同一语料上的 bpb 对照表 + "RNN 为什么慢"的显式计时（逐步 vs 并行）
- #strong[常见误解]：以为"注意力=Transformer"；以为 attention 是 2017 才发明的（其实 2014 就有）

== M2 · 分词与表示

- #strong[核心问题]：为什么不用字符？为什么不用整词？词表大小怎么权衡？中文/代码/数学符号怎么处理？
- #strong[关键概念]：BPE（训练循环、merge 规则、特殊 token、bytes 回退）、WordPiece、Unigram、词表大小 ↔ 序列长度 ↔ 参数量的三方权衡、压缩率
- #strong[对标]：CS336 A1 tokenizer 部分；nanochat #raw("tokenizer.py")；HF LLM Course ch2（"Implement BPE/WordPiece/Unigram from the ground up"）
- #strong[亲手实验]：手写 BPE（训练 + 编码 + 流式编解码往返）→ 在 TinyStories 与中文语料上各训一个词表 → 测压缩率
- #strong[判分证据]：#raw("tests/test_tokenizer.py")、#raw("test_train_bpe.py") 全绿 + 压缩率表（中英文分别）+ 往返一致性
- #strong[常见误解]：以为 token 就是"词"；忽略中文一个汉字可能被切成 2–3 个 byte token 导致实际序列变长

== M3 · Transformer 架构与内部机制

- #strong[核心问题]：attention 到底在算什么？为什么需要多头？位置编码为什么从正弦换成 RoPE？RMSNorm 凭什么比 LayerNorm 更常用？残差在防什么？
- #strong[关键概念]：QKV 与缩放点积、因果 mask、多头与 GQA/MQA、RoPE（含外推）、RMSNorm、pre-norm vs post-norm、FFN/SwiGLU、权重共享、初始化与 QK-norm、参数量分解
- #strong[对标]：CS336 lecture 03–04 + A1 model 部分；rasbt《LLMs-from-scratch》ch3–ch4（含 MoE/GQA/MLA/SWA 附录）；李宏毅 GenAI-ML；nanochat #raw("gpt.py")
- #strong[亲手实验]：手写完整 Transformer 层（含 RoPE/RMSNorm/SwiGLU）→ 形状测试 → #strong[改坏实验]：去掉因果 mask、把 RoPE 换成可学习位置嵌入、去掉残差，各跑一次看现象
- #strong[判分证据]：#raw("tests/test_model.py")、#raw("test_nn_utils.py") 全绿 + 三组"改坏"实验的 loss 曲线与现象记录（进 #raw("证据/")）
- #strong[常见误解]：以为 attention 是"可解释的检索"；以为参数越多越好；忽略 pre-norm 对稳定性的决定性作用

== M4 · 训练：数据、优化、系统

- #strong[核心问题]：为什么同样的模型有人训得动有人训崩？Scaling law 怎么指导算力分配？多卡为什么不是线性加速？
- #strong[关键概念]：预训练目标与数据配比、去重与过滤、AdamW（解耦权重衰减）、Muon、LR schedule（warmup+cosine）、梯度裁剪、混合精度（bf16/fp16/fp32 与 GradScaler）、梯度累积、DDP/FSDP/TP/PP、通信开销与扩展效率、Chinchilla 与 compute-optimal、#raw("--target_flops")
- #strong[对标]：CS336 A2/A3 + lecture 05–11；nanochat #raw("optim.py")/#raw("base_train.py")/#raw("runs/scaling_laws.sh")；HF Ultra-Scale Playbook（分布式，待核）；李沐 d2l ch11–ch12
- #strong[亲手实验]：手写 AdamW 与 LR 调度 → 单卡固定算力下的 depth sweep（d4/d6/d8/d10）→ 拟合幂律外推 d12 → #strong[用真实 d12 训练验证预测（打脸链路）] → 双卡 DDP 测扩展效率
- #strong[判分证据]：#raw("tests/test_optimizer.py") 全绿；sweep 原始数据 + 拟合图 + 外推预测存档（#strong[预测先写死再跑]）；扩展效率曲线 + 通信占比
- #strong[常见误解]：以为"loss 不降就是数据问题"；把显存不足当成硬件不够（其实是批大小/精度/累积没调）；把 DDP 当免费加速

== M5 · 推理与部署

- #strong[核心问题]：为什么生成是逐个 token 的？KV cache 省了什么、代价是什么？量化会掉多少点？吞吐与延迟怎么权衡？
- #strong[关键概念]：自回归解码、KV cache、批处理与 continuous batching、PagedAttention、采样策略（temperature/top-p/top-k）、量化（int8/int4/GPTQ/AWQ）、投机解码、显存占用分解、token 成本
- #strong[对标]：nanochat #raw("engine.py")（KV cache 实现）+ #raw("infer_bench.py")；CS336 lecture 10（Inference）；rasbt ch2（生成与 KV caching）
- #strong[亲手实验]：从零写 KV cache 的自回归生成 → 对比有无 cache 的耗时/显存 → 手写一个贪心 vs top-p 采样对照 → 测不同 batch size 的吞吐
- #strong[判分证据]：#raw("tests/test_engine.py") 全绿 + 延迟/吞吐/显存三张图 + "cache 换来多少倍加速"的实测数字
- #strong[常见误解]：以为推理慢是因为"模型太大"（常是没批处理/没 cache）；以为量化无损

== M6 · 后训练：从"会说话"到"会做事"

- #strong[核心问题]：SFT、DPO、RLVR 各自在补什么能力？为什么 RLVR 能提升数学/代码却可能伤害通用能力？reward hacking 长什么样？
- #strong[关键概念]：指令微调与 chat template、损失掩码（只算 answer 部分）、奖励模型、PPO、DPO 的隐式奖励、GRPO 的组内归一化优势、可验证奖励（verifiable reward）、拒绝采样、蒸馏、合成数据、KL 正则与过度优化
- #strong[对标]：CS336 A5（含 #raw("test_grpo.py")、GSPO/MaxRL）；#strong[rasbt《Reasoning from Scratch》ch3–ch8]（先建评测→推理时扩展→self-refinement→GRPO→改进 GRPO→蒸馏）；Nathan Lambert《RLHF Book》（免费在线，17 章）；HF LLM Course ch11–12；minimind #raw("train_dpo/train_grpo.py")；nano-aha-moment（单文件单卡）
- #strong[亲手实验]：同一基座上做 SFT / DPO / GRPO 三变体 → #strong[同一评测口径]下对照 → 手写 GRPO 损失并逐项注释（advantage 从哪来、为什么要除标准差）→ 制造一次 reward hacking 并记录现象
- #strong[判分证据]：#raw("tests/test_grpo.py") 全绿 + 三方对照表（同基座/同评测/同种子策略）+ reward 曲线与失败样本分析
- #strong[常见误解]：以为 DPO 不用 reward model 就"更简单"；以为 RL 一定比 SFT 强；把训练 reward 上升当成能力提升（不做 held-out 评测就是自欺）

== M7 · 评测：把"感觉变好了"变成"确实变好了"

- #strong[核心问题]：benchmark 分数可信吗？污染怎么判断？为什么必须固定口径？评测方差有多大？
- #strong[关键概念]：bpb / perplexity / CORE / 下游基准（GSM8K/MATH-500/MMLU/HumanEval）、pass\@k、评测污染、few-shot 与 prompt 敏感性、方差与置信区间、LLM-as-judge 的偏置、可验证奖励 vs 学习型奖励
- #strong[对标]：#strong[rasbt《Reasoning from Scratch》ch3（先建评测再上技术，全书教学法基石）]；nanochat #raw("core_eval.py")（单文件 CORE）；CS336 lecture 12；Berkeley Agentic AI MOOC "Agent Evaluation"；lm-evaluation-harness
- #strong[亲手实验]：写一个"数学题判定器"（解析 + 数值比对 + 容错）→ 测它在 200 道题上的准确率与假阳性 → 给自己的两个模型跑同一套评测并给误差棒
- #strong[判分证据]：判定器的单测 + 假阳性/假阴性样例分析 + 带误差棒的对照表（#strong[不许只报均值]）
- #strong[常见误解]：只看一个 benchmark 下结论；忽略 prompt 格式带来的巨大差异；把测试集当验证集反复调

== M8 · 智能体：工具、记忆、harness、长程任务

- #strong[核心问题]：LLM 从"回答问题"到"完成任务"缺什么？harness 为什么比模型本身更能决定成败？self-judge 什么时候有效、什么时候是自欺？
- #strong[关键概念]：工具调用/函数调用、ReAct 循环、context engineering（Karpathy/李宏毅都专讲）、记忆与压缩、harness 设计（沙箱、权限、反馈信号）、长程任务的误差累积、多智能体、self-judge / self-refine 的边界条件、可验证环境
- #strong[对标]：李宏毅 GenAI-ML《Context Engineering》专讲；Berkeley LLM Agents MOOC + Agentic AI MOOC（含 "Post-Training Verifiable Agents"）；HF Agents Course（三大框架 + 排行榜）；rasbt《Reasoning from Scratch》ch5（self-refinement）；#raw("PrimeIntellect-ai/verifiers")、terminal-bench、SWE-bench
- #strong[亲手实验]：手写最小 ReAct 循环（不用框架）→ 给它 2 个工具（计算器 + 代码执行）→ 记录失败轨迹分类 → 加 self-judge 再跑，做消融
- #strong[判分证据]：轨迹日志（成功/失败分类）+ self-judge 有无的成功率差 + "什么时候 self-judge 有害"的案例
- #strong[常见误解]：以为 Agent 的瓶颈在模型智力（常在你的工具接口与反馈信号）；以为 self-judge 免费提升（它会放大原有错误）

== M9 · 前沿与安全（持续跟进区，不是一次性学完）

- #strong[核心问题]：MoE/长上下文/多模态改变了什么？对齐与安全是"加一层"还是"改训练目标"？持续学习与"AI 训 AI"可行到什么程度？
- #strong[关键概念]：MoE 稀疏激活、长上下文外推与记忆、多模态对齐、可解释性、红队与越狱、幻觉的成因、评测式安全保障、合成数据闭环、self-play、灾难性遗忘、模型合并
- #strong[对标]：CS336 lecture 04（MoE）+ 论文精读清单；Berkeley Agentic AI MOOC（安全与红队）；#raw("opendilab/awesome-RLVR")；#raw("LeapLabTHU/limit-of-RLVR")
- #strong[亲手实验（选题制）]：从"合成数据自训练一轮" / "拒绝采样提升数学" / "self-play 生成题目"三者中选一个，做最小闭环 + 反证
- #strong[判分证据]：小实验 + 明确写出"这个方向的 no-go 是什么"（负结果不许擦除）
- #strong[常见误解]：把"前沿"当成必须立刻掌握（正确姿势是保持索引能力 + 每季度更新一次本模块）

#v(4pt)
#line(length: 100%, stroke: 0.6pt + luma(200))
#v(4pt)

== 模块 ↔ 课题 ↔ 周次 对照

#block(width: 100%, above: 8pt, below: 10pt)[
#text(size: 9pt)[
  #table(
    columns: (0.058fr, 0.140fr, 0.115fr, 0.256fr, 0.237fr, 0.194fr),
    inset: (x: 7pt, y: 5pt),
    align: left + top,
    stroke: (x, y) => (bottom: if y == 0 { 0.9pt + luma(105) } else { 0.25pt + luma(220) }),
    table.header([模块], [主课题], [周次], [讲（对标）], [做（手写区）], [证（判分/证据）]),
    [M0], [前置/贯穿], [W1], [d2l ch2–5], [micrograd + MLP], [数值梯度对照],
    [M1], [课题02], [W2], [d2l ch8–10], [bigram → RNN → Transformer], [bpb 对照表],
    [M2], [课题01], [W1], [CS336 A1 + HF ch2], [手写 BPE], [pytest 全绿 + 压缩率],
    [M3], [课题02], [W2–W3], [CS336 lec03–04 + rasbt ch3–4], [手写 Transformer], [pytest + 改坏实验],
    [M4], [课题03/04/06], [W3–W9], [CS336 A2/A3 + nanochat], [AdamW + sweep + DDP], [拟合图 + 扩展效率],
    [M5], [课题04/05], [W5–W8], [nanochat engine + CS336 lec10], [KV cache + Triton kernel], [三图 + 实测数字],
    [M6], [课题08], [W10–W12], [理由书 ch3–8 + RLHF Book], [SFT/DPO/GRPO 对照], [test\_grpo 全绿 + 对照表],
    [M7], [课题07/08], [W9–W12], [Reasoning ch3 + CS336 lec12], [判定器 + 评测], [假阳性分析 + 误差棒],
    [M8], [课题09/10], [W13–W14], [李宏毅 Context Eng. + Agents MOOC], [最小 ReAct + self-judge], [轨迹分类 + 消融],
    [M9], [课题11（选题）], [W15–W16], [论文精读 + MOOC], [选题小实验], [no-go 记录],
  )
]
]

== 与课程（CORE100299）六板块的映射

#block(width: 100%, above: 8pt, below: 10pt)[
#text(size: 9pt)[
  #table(
    columns: (0.322fr, 0.301fr, 0.377fr),
    inset: (x: 7pt, y: 5pt),
    align: left + top,
    stroke: (x, y) => (bottom: if y == 0 { 0.9pt + luma(105) } else { 0.25pt + luma(220) }),
    table.header([课程板块], [对应本图模块], [课程大论文可用素材]),
    [绪论], [M1], [语言模型史一页],
    [搜索求解], [M8（Agent 的搜索/规划）], [ReAct 与树搜索对照],
    [知识表示], [M8（记忆/工具）], [context engineering 案例],
    [机器学习（监督/深度/强化/无监督）], [M0/M3/M4/M6], [预训练+后训练全链路],
    [智能体], [M8], [最小 ReAct + self-judge 消融],
    [大语言模型], [M2–M7], [0.1B 端到端 + scaling law],
  )
]
]

#pagebreak()

= 对标教学资源清单（2026-09-17 核实）

#block(width: 100%, above: 9pt, below: 9pt, inset: (left: 12pt, right: 8pt, y: 6pt), stroke: (left: 3pt + luma(180)), fill: luma(252))[
#text(size: 9.8pt)[
目的：#strong[给"讲"这条腿找最好的老师]。每个知识点都指定一份对标材料， 由导师讲解 + 你复述 + 你动手，形成"三师制"：#strong[对标名师讲概念 / 我讲你的具体卡点 / 判分器讲对错]。

核实纪律（承仓库铁律"引用任何数字先复现"）： 本表"核实"列标 ✔ 的，是我在 2026-09-17 当日通过 #raw("gh api") 或官网页面#strong[实际打开确认]的； 标 ◷ 的表示尚未亲自核实，#strong[不许作为唯一依据]，用前先核。 标 ⚠ 的是已知坑（过时/收费/不可达）。
]
]

== 一、主线三件套（工程 + 判分，本学科骨架）

#block(width: 100%, above: 8pt, below: 10pt)[
#text(size: 9pt)[
  #table(
    columns: (0.027fr, 0.319fr, 0.109fr, 0.039fr, 0.089fr, 0.149fr, 0.270fr),
    inset: (x: 7pt, y: 5pt),
    align: left + top,
    stroke: (x, y) => (bottom: if y == 0 { 0.9pt + luma(105) } else { 0.25pt + luma(220) }),
    table.header([\#], [资源], [类型], [语言], [覆盖模块], [核实], [为什么选它]),
    [1], [#strong[Stanford CS336]（#raw("stanford-cs336/lectures") + #raw("assignment1-basics")…#raw("assignment5-alignment")）], [课程 + 可执行判分器], [英], [M2–M7], [✔ commit 已锁], [唯一把「从零写」做成#strong[自动判分]的课程；2026 版 A5 已含 GRPO/GSPO/MaxRL],
    [2], [#strong[karpathy/nanochat]（58,087★, MIT）], [全链路工程], [英], [M2–M5, M7], [✔ commit #raw("92d63d4e8bb4")], [20 个文件覆盖 tokenizer→预训练→SFT→RL→评测→推理引擎→工具执行；单旋钮 #raw("--depth")；支持 CPU/MPS],
    [3], [#strong[jingyaogong/minimind]（61,450★, Apache-2.0）], [中文全链路 + RL 脚本], [中], [M2–M6], [✔], [中文文档 + #raw("train_grpo/ppo/dpo/agent.py")；单卡 3090 上"3 块钱 2 小时"；适合读代码学中文术语],
  )
]
]

== 二、理论线的"对标名师"（补"讲"的深度）

#block(width: 100%, above: 8pt, below: 10pt)[
#text(size: 9pt)[
  #table(
    columns: (0.033fr, 0.295fr, 0.100fr, 0.060fr, 0.088fr, 0.075fr, 0.349fr),
    inset: (x: 7pt, y: 5pt),
    align: left + top,
    stroke: (x, y) => (bottom: if y == 0 { 0.9pt + luma(105) } else { 0.25pt + luma(220) }),
    table.header([\#], [资源], [类型], [语言], [覆盖模块], [核实], [怎么用]),
    [4], [#strong[rasbt《Build a Reasoning Model (From Scratch)》] + #raw("rasbt/reasoning-from-scratch")（5,000+★, Apache-2.0）], [书 + 逐章 notebook], [英], [#strong[M6/M7/M8]], [✔], [#strong[教学法范本]：ch3 先建评测再上任何技术（"so every later improvement is measured rather than asserted"）；ch5 self-refinement；ch6 GRPO 从零；ch2–4 可 CPU 跑，只有 RL 章需要 GPU],
    [5], [#strong[Nathan Lambert《Reinforcement Learning from Human Feedback》]（rlhfbook.com，免费在线，2026 版）], [书（免费）], [英], [#strong[M6/M7]], [✔], [后训练理论主线：指令微调/奖励模型/PPO/DPO/RLVR/拒绝采样/合成数据/过度优化/评测，17 章],
    [6], [#strong[李宏毅（台大）GenAI-ML 2025 Fall / 机器学习 2026 Spring]], [视频 + 讲义 PDF], [#strong[中]], [M3/M6/M8], [✔ 站点已核], [中文讲得最清楚的一手：含《Context Engineering》专讲（Agent 时代的核心）],
    [7], [#strong[李沐《动手学深度学习》(zh.d2l.ai，B站 236 集)]], [书 + 视频（免费）], [#strong[中]], [M0/M1/M3/M5], [✔], ["不是通过幻灯片讲解，而是通过解读代码、动手调参跑实验来学习"——#strong[中文知行合一的原典]],
    [8], [#strong[rasbt《Build a Large Language Model (From Scratch)》] + #raw("rasbt/LLMs-from-scratch")（105,140★，2026-09-17 仍在更新）], [书 + notebook], [英], [M2–M4, M6], [✔], [代码级最细；附录含 GQA/MLA/SWA/MoE/KV cache/FLOPs 分析/LoRA，正好是 M3/M5 的补充读物],
    [9], [#strong[HF LLM Course]（13 章，ch11–12 含 LoRA/SFT/GRPO）], [课程（免费）], [英], [M2/M6], [✔], [由 transformers/TRL 库作者写，ch8「调试训练流水线」是别处没有的],
    [10], [#strong[HF Agents Course]（4 units + 最终项目排行榜 + function-calling 微调 bonus）], [课程（免费，有证书）], [英], [#strong[M8]], [✔], [三个框架并学（smolagents/LlamaIndex/LangGraph），最后提交到公开排行榜——#strong[自带客观验收]],
    [11], [#strong[Berkeley LLM Agents MOOC / Agentic AI MOOC]（rdi.berkeley.edu、agenticai-learning.org）], [公开课录像 + slides], [英], [#strong[M8/M9]], [✔], [有一讲就叫 "Post-Training Verifiable Agents"、一讲 "Agent Evaluation"——正是唐杰作业⑤的前沿坐标],
    [12], [#strong[Karpathy《Neural Networks: Zero to Hero》]（micrograd/makemore/nanoGPT）], [视频], [英], [M0/M1/M3], [✔ 系列存在性已核], [直觉地基；micrograd 是 M0 手写实验的模板（但#strong[你要自己写]）],
    [13], [#strong[3Blue1Brown 神经网络系列]], [动画视频], [英（有中字）], [M0/M3], [◷], [视觉直觉；用来预热 attention/反向传播],
    [14], [#strong[HF Ultra-Scale Playbook]], [长文（免费）], [英], [M4], [◷], [分布式训练（DDP/FSDP/TP/PP）的工程全景，W9 前核实],
    [15], [#strong[《大规模语言模型：从理论到实践》（复旦 张奇等）]], [书], [#strong[中]], [M2–M6], [◷], [中文教材备选；与 minimind 配套读],
  )
]
]

== 三、评测与环境类（M7/M8 的判分件）

#block(width: 100%, above: 8pt, below: 10pt)[
#text(size: 9pt)[
  #table(
    columns: (0.050fr, 0.336fr, 0.083fr, 0.217fr, 0.315fr),
    inset: (x: 7pt, y: 5pt),
    align: left + top,
    stroke: (x, y) => (bottom: if y == 0 { 0.9pt + luma(105) } else { 0.25pt + luma(220) }),
    table.header([\#], [资源], [覆盖], [核实], [用途]),
    [16], [#raw("harbor-framework/terminal-bench")（+ 冻结版 #raw("terminal-bench-1")）], [M8], [✔], [长程 Agent 的连续基准（v2 新仓，v1 已冻结改名）],
    [17], [#raw("SWE-bench/SWE-bench")、#raw("SWE-bench/SWE-smith")], [M7/M8], [✔], [代码任务评测 / 合成可验证环境],
    [18], [GSM8K / MATH-500], [M7], [✔（在 rasbt ch3 用作 verifier 对象）], [数学可验证奖励的标准件],
    [19], [#raw("PrimeIntellect-ai/verifiers")（4,626★, MIT）], [M7/M8], [✔ commit 已锁], [RL 环境 + 评测的抽象层，做课题09 的参照],
    [20], [#raw("EleutherAI/lm-evaluation-harness")、#raw("UKGovernmentBEIS/inspect_ai")], [M7], [✔], [学术评测标准件 / harness 设计参考],
    [21], [#raw("walkinglabs/hands-on-modern-rl")（4,395★，中文）], [M6], [✔], [RL→RLVR→Agentic RL 中文教材，#strong[实验标注 CPU/xGPU 且挂免费在线 Notebook]],
    [22], [#raw("McGill-NLP/nano-aha-moment")], [M6], [✔], [单文件单卡从零 GRPO（阅读用，不宜作依赖）],
  )
]
]

== 四、明确标注的坑（用前必读）

#block(width: 100%, above: 8pt, below: 10pt)[
#text(size: 9pt)[
  #table(
    columns: (0.346fr, 0.654fr),
    inset: (x: 7pt, y: 5pt),
    align: left + top,
    stroke: (x, y) => (bottom: if y == 0 { 0.9pt + luma(105) } else { 0.25pt + luma(220) }),
    table.header([资源], [坑]),
    [CS336 #strong[A3]], [需要 #raw("A3_API_KEY") = 8 位学号，#strong[非斯坦福在校生拿不到] → 本学科用自建 sweep 替代（课题03 已按此设计）],
    [CS336 #strong[A2]], [#raw("flash-attn") 安装特殊：#raw("uv sync --no-install-package flash-attn") 再 #raw("uv sync")],
    [CS336 #strong[A5]], [2026 版换成 Olmo-2-1B \@ GSM8K，且用 Modal 云函数 → 显存要求最高，放在 W12 且用双 T4],
    [#strong[Kaggle P100]], [若分配到 P100（SM60），#strong[Triton 不可用]（需 CC≥7.0）→ 课题05 必须重开会话直到拿到 T4],
    [#raw("karpathy/nanoGPT")、#raw("build-nanogpt")、#raw("llm.c")], [已被 nanochat 取代或停滞，#strong[只作历史读物]],
    [#raw("karpathy/LLM101n")], [#strong[已归档（archived）]，且 Eureka Labs 至今未完整发布 → 只当索引，别当路线],
    [HuggingFace #strong[FineWeb]], [我用 #raw("gh api") 查 #raw("HuggingFaceFW/fineweb")、#raw("huggingface/fineweb") 均 404 → #strong[不要写这两个路径]，语料走 TinyStories / #raw("stanford-cs336/owt-sample") / dolma],
    [#raw("terminal-bench")], [已改名分仓（v1 → #raw("terminal-bench-1")，v2 → 新仓），旧链接会 404],
  )
]
]

== 五、三师制使用方法（每个知识点的标准动作）

#block(width: 100%, above: 9pt, below: 9pt, inset: (x: 10pt, y: 8pt), radius: (right: 4pt), fill: luma(248), stroke: (left: 2.5pt + luma(165)))[
  #raw("① 先读对标材料的那一节（不超过 25 分钟，带着\"我要回答哪 3 个问题\"去读）
② 合上材料，用自己的话讲给我听（我按 M0–M9 的\"核心问题\"追问，专挑你含糊的地方）
③ 我讲你的卡点（只讲你卡住的那一层，不重讲整章）
④ 上手写（手写区任务，最小可运行）
⑤ 跑判分（pytest / 自建判定器）→ 出证据
⑥ 改坏它 → 预测 → 验证 → 修好（第 3 条硬标准）", block: true)
]

#strong[分工原则]：对标名师负责"标准讲法"，我负责"你的卡点 + 判分 + 记忆归档"， #strong[任何一方都不替代你动手]（见《造轮子边界.md》）。

#pagebreak()

= 知行合一规程（本学科教学法核心）

#block(width: 100%, above: 9pt, below: 9pt, inset: (left: 12pt, right: 8pt, y: 6pt), stroke: (left: 3pt + luma(180)), fill: luma(252))[
#text(size: 9.8pt)[
立规 2026-09-17。缘起：用户指出"实操性够强，但知识讲解偏少"，并明确要求#strong[把知行合一贯穿全流程]。 本规程定义：什么算"学过"，什么算"学会"，以及每一层怎么被强制咬合。

一句话：#strong[本学科没有"听懂了"这个状态，只有在代码里被验证过的"懂了"。]
]
]

#v(4pt)
#line(length: 100%, stroke: 0.6pt + luma(200))
#v(4pt)

== 一、把"知行合一"变成可执行的四件咬合

#block(width: 100%, above: 8pt, below: 10pt)[
#text(size: 9pt)[
  #table(
    columns: (0.112fr, 0.228fr, 0.343fr, 0.317fr),
    inset: (x: 7pt, y: 5pt),
    align: left + top,
    stroke: (x, y) => (bottom: if y == 0 { 0.9pt + luma(105) } else { 0.25pt + luma(220) }),
    table.header([咬合件], [名称], [谁的活], [不通过的后果]),
    [讲], [导师讲 + 对标名师], [我（≤20 分钟一块，≤150 字一个概念块）], [讲完必须立刻出"代码级提问"],
    [做], [手写区最小可运行], [你], [没跑起来 = 这一课不算上],
    [证], [判分器 / 实验证据], [我搭台，你跑], [无证据的结论一律不采纳],
    [反], [改坏实验 + 打脸记录], [你预测，你验证], [只会正确写法的人，遇到 bug 一定卡死],
  )
]
]

#strong[四件缺一 → 本知识点标 ◐ 未通过，不进 PROGRESS 的 ✔。]

#v(4pt)
#line(length: 100%, stroke: 0.6pt + luma(200))
#v(4pt)

== 二、知识卡规范（每个知识点一张，落 #raw("知识卡/") 或课题目录）

#block(width: 100%, above: 9pt, below: 9pt, inset: (x: 10pt, y: 8pt), radius: (right: 4pt), fill: luma(248), stroke: (left: 2.5pt + luma(165)))[
  #raw("# 知识卡 · <知识点名>（模块 M?）
- 一句话定义：
- 直觉（给别人讲会用的话）：
- 公式/伪代码骨架（手写，不许贴代码）：
- 对标出处：<材料名 + 章节>
- 上手写实验：<文件路径 + 判分命令>
- 判分证据：<pytest 名 / 图 / 数字>
- 改坏实验：改哪里 → 你预测的现象 → 实测现象
- 常见误解：
- 记忆锚（隐喻+口诀+符号位置）：
- 间隔重复卡号：", block: true, lang: "markdown")
]

#block(width: 100%, above: 9pt, below: 9pt, inset: (left: 12pt, right: 8pt, y: 6pt), stroke: (left: 3pt + luma(180)), fill: luma(252))[
#text(size: 9.8pt)[
知识卡#strong[由你口述、我整理]（你说我写），但"直觉""改坏实验的预测"两栏必须是你自己的话。 若某栏你说不出来 → 这节课没上完。
]
]

#v(4pt)
#line(length: 100%, stroke: 0.6pt + luma(200))
#v(4pt)

== 三、讲课节拍（每周两个时段，各 1.5–3h）

#block(width: 100%, above: 9pt, below: 9pt, inset: (x: 10pt, y: 8pt), radius: (right: 4pt), fill: luma(248), stroke: (left: 2.5pt + luma(165)))[
  #raw("时段 A（理论）：讲（≤20min 一块）→ 你复述 → 我挑含糊处追问 → 你写知识卡 → 出代码级提问
时段 B（实验）：读对标材料对应节 → 你写手写区 → 跑判分 → 记录证据 → 改坏实验 → 归档", block: true)
]

#strong[硬纪律]：

- 一次讲透，不挤牙膏（沿用你已定的节奏：你多讲、我多写；批量 3–5 个关键问题）。
- 每个概念块 ≤150 字，讲完必须配一个"#strong[立刻能跑的最小实验]"。
- 讲课时#strong[不许给手写区代码]（见《造轮子边界.md》）；给的是"该去哪里找、该测什么"。

#v(4pt)
#line(length: 100%, stroke: 0.6pt + luma(200))
#v(4pt)

== 四、代码级提问（"知"与"行"的咬合点，本学科独创）

每讲完一块，我出 #strong[3–5 道代码级提问]，形式固定为"#strong[改坏它 / 预测现象 / 给出诊断]"：

#block(width: 100%, above: 8pt, below: 10pt)[
#text(size: 9pt)[
  #table(
    columns: (0.193fr, 0.807fr),
    inset: (x: 7pt, y: 5pt),
    align: left + top,
    stroke: (x, y) => (bottom: if y == 0 { 0.9pt + luma(105) } else { 0.25pt + luma(220) }),
    table.header([类型], [例子]),
    [改坏预测], ["把 attention 的因果 mask 注释掉，loss 会怎样？训练 100 步内你会看到什么现象？"],
    [放大器], ["把 RoPE 换成可学习位置嵌入，在训练/外推两种场景下各自会怎么退化？"],
    [诊断], ["你观察到 loss 在第 400 步突然变 NaN，请按顺序列出你会检查的 5 个量。"],
    [代价], ["把词表从 32k 扩到 128k，参数量、序列长度、每 token 成本各变多少？（估数量级）"],
    [反事实], ["如果 DDP 改成 FSDP，同样的 batch，显存和速度分别会怎么动？为什么？"],
  )
]
]

#strong[判分标准]：预测错不算失败（#strong[预测错 + 跑实验打脸 = 最高质量的学习]）， 但"没有预测就跑"算失败，因为那等于放弃了知行之间的连接。

#v(4pt)
#line(length: 100%, stroke: 0.6pt + luma(200))
#v(4pt)

== 五、"真的懂了"的三条硬标准（与《知识地图》一致，此处为验收动作）

+ #strong[能讲清] → 你对着外行话讲一遍，我专门装不懂追问三层（Why → Why not → What if）。
+ #strong[能指出代码位置] → 你在我画出的 #raw("手写/") 或上游代码里，#strong[不搜索]直接指出对应函数/行号区间。
+ #strong[能改坏并修好] → 我在你没看过的地方埋一个 bug（或你自己改坏），你在#strong[不看不该看的代码]的前提下， 用实验定位并修好；修好过程必须留日志进 #raw("证据/")。

#block(width: 100%, above: 9pt, below: 9pt, inset: (left: 12pt, right: 8pt, y: 6pt), stroke: (left: 3pt + luma(180)), fill: luma(252))[
#text(size: 9.8pt)[
三条全过才写 ✔；只过第 1 条 = 会考试，不会干活。
]
]

#v(4pt)
#line(length: 100%, stroke: 0.6pt + luma(200))
#v(4pt)

== 六、反讲机制（费曼 + 红队）

- 每模块收口：#strong[你当老师，我当刺头学生]，我只问"为什么"，不纠正、只追问，直到你卡住或讲穿。
- 卡住的地方#strong[就是下一个知识点的入口]，直接写进 #raw("HANDOFF.md") 的"下一步"。
- 结项前：你来当评审，对着自己的报告做 3 条自我攻击（"这个结论最可能错在哪？"）， 与导师审稿意见并列存档 → 这就是唐杰作业⑦"问题/动机/方法/结果一项都不能糊"的本地化实现。

#v(4pt)
#line(length: 100%, stroke: 0.6pt + luma(200))
#v(4pt)

== 七、与其它章程的关系

- 谁写代码 → 《造轮子边界.md》（R1–R10 手写 / B1–B8 代写 / C 协作）
- 讲什么、讲多深 → 《知识地图-大模型全景.md》（M0–M9 四件咬合件）
- 用哪份材料讲 → 《对标教学资源清单.md》（三师制）
- 怎么算过 → 《判分与验收标准.md》（三层判分 + 每课题通过证据）
- 什么时候讲 → 《实训路线图.md》"知识讲解锚点"列

#pagebreak()

= 实训路线图 · 16 周 × 11 课题 × 唐杰 7 条 × CS336 映射

#block(width: 100%, above: 9pt, below: 9pt, inset: (left: 12pt, right: 8pt, y: 6pt), stroke: (left: 3pt + luma(180)), fill: luma(252))[
#text(size: 9.8pt)[
#strong[2026-09-17 并入 #raw("人工智能基础与应用/")（实训轨）]：本学科三轨合一—— #strong[课程轨]（CORE100299 课堂事务，见 #raw("../课程轨/课程进度.md")）、 #strong[实训轨]（本文件 + 11 个课题）、#strong[知识轨]（#raw("知识地图-大模型全景.md") M0–M9）。 配套：《对标教学资源清单.md》（跟谁学）、《知行合一规程.md》（什么叫学过）、 《造轮子边界.md》（谁写代码）、《算力与成本预算.md》（花多少）、《判分与验收标准.md》（怎么算过）。

立图 2026-09-17。基准：#strong[第 1 教学周 = 2026-09-14]（与校历、与唐杰清华开课同周）。 节奏：16 周跟课（每周 5–6h，约 2 个学习时段）。预算：#strong[零现金]，只用免费算力（见《算力与成本预算.md》）。
]
]

== 一、目标（一句话）

#strong[用零现金预算，把唐杰 2026 秋季作业清单一条不落地走完]，每一环都留下可复现证据、可执行判分与一页报告； 最终产出一份 NeurIPS 格式的英文技术报告 + 一个可现场 demo 的作品。

== 二、唐杰 7 条 ↔ 本学科课题 ↔ 判分来源（主映射表）

#block(width: 100%, above: 8pt, below: 10pt)[
#text(size: 9pt)[
  #table(
    columns: (0.365fr, 0.158fr, 0.347fr, 0.130fr),
    inset: (x: 7pt, y: 5pt),
    align: left + top,
    stroke: (x, y) => (bottom: if y == 0 { 0.9pt + luma(105) } else { 0.25pt + luma(220) }),
    table.header([唐杰作业条目], [对应课题], [官方规格 / 判分器], [算力档]),
    [① 从零写 Tokenizer + Transformer，端到端训 0.1B], [课题01、02、04], [CS336 A1（#raw("tests/")）], [T0 → T2],
    [② 手写 Triton attention kernel，测多卡训练/推理增益], [课题05、06], [CS336 A2], [T1 / T2],
    [③ raw dump 洗语料，拟合 scaling law 再外推], [课题07、03], [CS336 A4 + A3（A3 需自建替代）], [T0 / T1],
    [④ 同一基座做 SFT / DPO / RLVR 对照], [课题08], [CS336 A5（含 #raw("tests/test_grpo.py")）], [T2],
    [⑤ 可验证环境 + harness，训长程 Agent，鼓励 self-judge loop], [课题09、10], [无官方判分器（前沿区）→ verifiers / terminal-bench 思路], [T2],
    [⑥ 2–3 人组队，英文 NeurIPS 格式，W16 现场 demo], [课题11], [本仓库报告协议 + LaTeX 模板], [—],
    [⑦ 作业 40% / 大项目 60%；问题/动机/方法/结果一项都不能糊], [全学科判分口径], [《判分与验收标准.md》], [—],
  )
]
]

== 三、16 周课表（周次 / 课题 / 交付物 / GPU 需求）

#block(width: 100%, above: 8pt, below: 10pt)[
#text(size: 9pt)[
  #table(
    columns: (0.074fr, 0.152fr, 0.244fr, 0.379fr, 0.152fr),
    inset: (x: 7pt, y: 5pt),
    align: left + top,
    stroke: (x, y) => (bottom: if y == 0 { 0.9pt + luma(105) } else { 0.25pt + luma(220) }),
    table.header([周], [日期], [课题], [本周交付物（硬指标）], [GPU]),
    [W1], [09-14→09-20], [课题01 BPE 分词器], [手写 BPE + #raw("test_tokenizer.py")/#raw("test_train_bpe.py") 全绿 + 压缩率表], [0],
    [W2], [09-21→09-27], [课题02 Transformer 骨架], [attention/MLP/RoPE/RMSNorm 手写 + 形状与数值测试过], [0],
    [W3], [09-28→10-04], [课题02 收口（国庆周，减半）], [训练循环 + AdamW + 序列化测试过；loss 稳定下降曲线], [0],
    [W4], [10-05→10-11], [课题03 Scaling Law 预演], [5 点小规模 sweep + 拟合 + 外推预测 + 打脸记录], [0（CPU）],
    [W5], [10-12→10-18], [课题04 0.1B 端到端（上）], [数据管线 + 双 T4 冒烟 + 首轮训练启动（断点续训可用）], [6–9h（2×T4）],
    [W6], [10-19→10-25], [课题04 收口], [bpb/CORE 指标 + 采样样本 + 实测成本账单 vs 估算], [6–12h（2×T4）],
    [W7], [10-26→11-01], [课题05 Triton kernel（上）], [naive 实现 → 分块实现，正确性对齐], [4h（1×T4）],
    [W8], [11-02→11-08], [课题05 收口 + 课题06 开题], [speedup / 显存 / profiling 三张图（含硬件口径声明）], [6h（2×T4）],
    [W9], [11-09→11-15], [课题06 多卡与分布式], [DDP vs FSDP 对照 + 扩展效率曲线 + 通信占比分析], [8h（2×T4）],
    [W10], [11-16→11-22], [课题07 数据清洗与去重], [过滤/去重规则 + 有无清洗的对照组 loss 对比], [6h（1×T4）],
    [W11], [11-23→11-29], [课题08 SFT], [SFT 基线 + 与基座对照], [8h（2×T4）],
    [W12], [11-30→12-06], [课题08 DPO + RLVR], [#strong[SFT / DPO / GRPO 三方对照表]（同基座、同评测口径）], [10h（2×T4）],
    [W13], [12-07→12-13], [课题09 可验证环境 + harness], [1 个自建可验证环境 + rollout 成功率 + 判定逻辑单测], [6h（2×T4）],
    [W14], [12-14→12-20], [课题10 长程 Agent + self-judge], [多步任务串联 + self-judge 有无的消融], [8h（2×T4）],
    [W15], [12-21→12-27], [蓄水周], [补跑欠账 + 英文报告初稿], [4h（弹性）],
    [W16], [12-28→01-03], [课题11 结项], [NeurIPS 格式英文报告 + 现场 demo + 总复盘], [4h（弹性）],
  )
]
]

#strong[GPU 总需求 ≈ 97 小时]，免费额度可用 #strong[≈480 小时]（Kaggle 30h/周 × 16 周）→ 安全系数约 #strong[5×]（见预算章程）。

=== 附：知识讲解锚点（每周讲哪个模块——补上"讲"这条腿，2026-09-17 新增）

#block(width: 100%, above: 9pt, below: 9pt, inset: (left: 12pt, right: 8pt, y: 6pt), stroke: (left: 3pt + luma(180)), fill: luma(252))[
#text(size: 9.8pt)[
每个知识点的"四件咬合"（讲/做/证/反）见《知行合一规程.md》；模块内容见《知识地图-大模型全景.md》； 对标材料见《对标教学资源清单.md》。
]
]

#block(width: 100%, above: 8pt, below: 10pt)[
#text(size: 9pt)[
  #table(
    columns: (0.107fr, 0.184fr, 0.366fr, 0.344fr),
    inset: (x: 7pt, y: 5pt),
    align: left + top,
    stroke: (x, y) => (bottom: if y == 0 { 0.9pt + luma(105) } else { 0.25pt + luma(220) }),
    table.header([周], [讲解模块], [本周要讲透的核心问题（≤5 个）], [配套材料]),
    [W1], [#strong[M0 + M2]], [计算图与链式法则；熵/交叉熵/困惑度；BPE 为什么字节起步], [d2l ch2–5；CS336 A1 handout],
    [W2], [#strong[M1 + M3（上）]], [从 n-gram 到 attention 的动机；attention 在算什么；为什么多头], [d2l ch8–10；CS336 lec01/03],
    [W3], [#strong[M3（下）]], [RoPE vs 可学习位置；RMSNorm/pre-norm 为何关键；残差防什么], [CS336 lec03–04；rasbt ch3–4],
    [W4], [#strong[M4（上）]], [优化器与 LR 调度；混合精度；scaling law 如何指导算力分配], [CS336 lec09/11；nanochat #raw("optim.py")],
    [W5], [#strong[M4（下）+ M5（上）]], [数据配比与去重；吞吐/显存/FLOPs 记账], [CS336 lec05/13–14；nanochat #raw("base_train.py")],
    [W6], [#strong[M5（下）]], [KV cache 省了什么；采样策略；bpb/CORE 指标口径], [nanochat #raw("engine.py")/#raw("core_eval.py")；CS336 lec10/12],
    [W7], [#strong[M5（续·kernel）]], [GPU 内存层级；Triton 编程模型；flash attention 的分块与 online softmax], [CS336 lec05–06；triton 官方教程],
    [W8], [#strong[M4（续·并行）]], [DDP/FSDP/TP/PP 的取舍；为什么不是线性加速], [CS336 lec07–08；nanochat #raw("optim.py")],
    [W9], [#strong[M7（上）]], [评测口径、污染、方差、误差棒；"变好了"如何被证明], [rasbt ch3；CS336 lec12],
    [W10], [#strong[M7（下）+ M6（上）]], [过滤/去重的判定规则；指令微调与损失掩码], [CS336 A4；《RLHF Book》ch4],
    [W11], [#strong[M6（中）]], [偏好数据、奖励模型、DPO 的隐式奖励], [《RLHF Book》ch5/8/11；CS336 A5],
    [W12], [#strong[M6（下）]], [GRPO 的组内优势、KL 正则、reward hacking、过度优化], [rasbt ch6–7；《RLHF Book》ch6/7/14],
    [W13], [#strong[M8（上）]], [工具调用/ReAct/context engineering；harness 为什么决定成败], [李宏毅《Context Engineering》；Agents MOOC],
    [W14], [#strong[M8（下）]], [长程任务的误差累积；self-judge 何时有效、何时有害], [rasbt ch5；Berkeley Agentic AI MOOC],
    [W15–16], [#strong[M9（选题）]], [前沿采样：MoE/长上下文/合成数据闭环；no-go 的写法], [论文精读清单；awesome-RLVR],
  )
]
]

== 四、11 课题总表（手写要点 / 判分来源 / 通过证据）

#block(width: 100%, above: 8pt, below: 10pt)[
#text(size: 9pt)[
  #table(
    columns: (0.061fr, 0.186fr, 0.239fr, 0.298fr, 0.216fr),
    inset: (x: 7pt, y: 5pt),
    align: left + top,
    stroke: (x, y) => (bottom: if y == 0 { 0.9pt + luma(105) } else { 0.25pt + luma(220) }),
    table.header([\#], [课题], [手写区核心（不可代写）], [判分来源], [通过证据]),
    [01], [BPE 分词器], [merge 循环、特殊 token、bytes 回退、流式编码], [CS336 A1 #raw("tests/test_tokenizer.py")、#raw("test_train_bpe.py")], [pytest 全绿 + 压缩率表],
    [02], [Transformer 骨架], [attention、RoPE、RMSNorm、SwiGLU、残差、初始化], [CS336 A1 #raw("test_model.py")、#raw("test_nn_utils.py")], [pytest 全绿 + 参数量核对],
    [02b], [训练循环与优化器], [AdamW/Muon 更新式、LR schedule、梯度裁剪、精度管理], [CS336 A1 #raw("test_optimizer.py")、#raw("test_serialization.py")], [pytest 全绿 + loss 曲线],
    [03], [Scaling Law], [数据采集脚本口径、拟合、外推、#strong[打脸记录]], [自建判分：预测 vs 实测偏差], [5 点 sweep 数据 + 拟合图 + 外推预测存档],
    [04], [0.1B 端到端], [（复用 01/02 产物）预训练编排、断点续训判断], [自建判分：loss/bpb 达标 + 采样可读], [bpb/CORE + 采样样本 + 成本账单],
    [05], [Triton attention kernel], [#strong[kernel 本体]（分块、online softmax）], [CS336 A2 + 正确性对齐参考实现], [三图（speedup/显存/profile）+ 数值误差记录],
    [06], [多卡与分布式], [并行策略选择、通信原语、扩展效率分析], [CS336 A2 分布式部分 + 自建 benchmark], [扩展效率曲线 + 通信占比],
    [07], [数据清洗与去重], [#strong[过滤/去重规则的判定逻辑]], [CS336 A4 + 自建消融], [规则清单 + 对照组 loss 差],
    [08], [SFT / DPO / RLVR], [#strong[损失函数与优势估计]（A/group norm/重要性比）], [CS336 A5 #raw("tests/test_grpo.py") + 自建对照], [三方对照表（同口径）],
    [09], [可验证环境], [#strong[判定逻辑（verifier/reward）]], [自建单测 + rollout 成功率], [判定逻辑测试 + 成功率 + 失败样本分析],
    [10], [长程 Agent], [#strong[self-judge 协议设计]], [自建消融], [有无 self-judge 的成功率差 + 案例],
    [11], [结项], [报告骨架与结论判断], [报告协议 + 导师审稿], [英文报告 + demo],
  )
]
]

== 五、规模三档（零预算版）

#block(width: 100%, above: 8pt, below: 10pt)[
#text(size: 9pt)[
  #table(
    columns: (0.113fr, 0.270fr, 0.142fr, 0.275fr, 0.201fr),
    inset: (x: 7pt, y: 5pt),
    align: left + top,
    stroke: (x, y) => (bottom: if y == 0 { 0.9pt + luma(105) } else { 0.25pt + luma(220) }),
    table.header([档], [硬件], [模型规模], [数据], [用途]),
    [#strong[T0]], [沙箱 CPU（2 vCPU/3GB）或 Colab CPU], [1–10M], [TinyStories 子集 / owt-sample 采样], [课题01–03 的全部正确性与判分],
    [#strong[T1]], [Kaggle 1×T4 16GB], [0.03–0.1B], [TinyStories 全量 + 子集], [课题05/07 的单卡实验],
    [#strong[T2]], [Kaggle 2×T4（32GB 合计）], [0.1B], [同上 + 合成任务数据], [课题04/06/08/09/10],
  )
]
]

#strong[规模下探是主动取舍，不是妥协]：把"0.1B"从口号变成每次会话都能真跑的实验， 代价是学不到万卡级工程；收益是 16 周内全链路闭环。前沿规模直觉另走 #raw("论文精读/") 补齐。

== 六、跨学科搭桥（讲课时主动用）

- RL 的目标函数 → #raw("probability/") 的期望、方差、条件期望（REINFORCE = 用样本估期望）
- 语言模型的困惑度/交叉熵 → #raw("probability/") 的信息量直觉
- scaling law 的幂律拟合 → #raw("probability/") 的最小二乘与回归
- 结项报告 → #raw("论文精读/") 的论文写作规范；demo → #raw("人工智能基础与应用/") 的大论文素材

#pagebreak()

= 造轮子边界 · 谁写代码（本学科最高契约）

#block(width: 100%, above: 9pt, below: 9pt, inset: (left: 12pt, right: 8pt, y: 6pt), stroke: (left: 3pt + luma(180)), fill: luma(252))[
#text(size: 9.8pt)[
立约 2026-09-17，用户拍板口径："#strong[分层双轨]"。 本学科同时要求两件互相冲突的事：① 唐杰作业要求"不会动手、只会调 API 的先下去"； ② 你的时间是稀缺资源，16 周内跑完全链路。#strong[解决办法不是折中，而是划死边界]： 学习目标必须你手写；非学习目标必须我代写。边界之下，任何一方越界都算事故。
]
]

== 一、三条铁律

+ #strong[手写区（#raw("课题NN/手写/")）：Agent 禁止写入任何文件。] 不得给代码、不得给伪代码、 不得把第三方实现（含 nanochat / CS336 参考实现 / GitHub 上的答案库）当答案指给你。 允许的动作只有五类：解释报错、解释概念、审查你已写的 diff、建议 sanity check / toy example / profiler 检查、指路官方文档与讲义。
+ #strong[脚手架区（#raw("课题NN/脚手架/")、#raw("环境/")）：Agent 全权负责且必须主动完成]，不等你催。 这部分写一遍就够，重复劳动零学习收益。
+ #strong[越界的正确姿势]：你说"给我看答案"→ 走提示阶梯（五级）→ 到第五级给答案后， #strong[必须挂近迁移重考卡片]（隔 1–3 天、无提示、换场景再考）。给了答案不挂卡片 = 违规。

== 二、手写清单（学习目标，共 10 项）

#block(width: 100%, above: 8pt, below: 10pt)[
#text(size: 9pt)[
  #table(
    columns: (0.110fr, 0.568fr, 0.322fr),
    inset: (x: 7pt, y: 5pt),
    align: left + top,
    stroke: (x, y) => (bottom: if y == 0 { 0.9pt + luma(105) } else { 0.25pt + luma(220) }),
    table.header([编号], [手写内容], [为什么必须亲手写]),
    [R1], [BPE 训练与编码算法（merge 循环、特殊 token、bytes 回退、流式编码）], [分词决定了模型看到的世界；面试/科研高频],
    [R2], [Transformer 全部组件（attention、RoPE、RMSNorm、SwiGLU、残差、初始化）], [梯度与形状直觉只从亲手写里长出来],
    [R3], [训练循环与优化器（AdamW/Muon 更新式、LR schedule、梯度裁剪、精度管理）], [训练不收敛时，只有写过的人会 debug],
    [R4], [反向传播验证（gradient check、数值梯度对照）], [这是"我懂了"与"我能跑"的分界线],
    [R5], [#strong[Triton attention kernel 本体]（分块、online softmax）], [唐杰作业②的核心；性能直觉的唯一来源],
    [R6], [Scaling law 拟合与外推（数据采集口径、拟合、预测、打脸记录）], [这是"科研判断力"的训练区，不能外包],
    [R7], [SFT / DPO / RLVR 的#strong[损失函数与优势估计]（含 group normalization、重要性比）], [后训练是 2026 的重心；抄公式等于没学],
    [R8], [数据过滤/去重的#strong[判定规则]（启发式规则设计）], [数据决定上限；规则设计的品味靠自己做],
    [R9], [可验证环境的#strong[判定逻辑]（verifier / reward function）], [唐杰作业⑤的技术核心],
    [R10], [self-judge loop 的#strong[协议设计]（何时判、判什么、如何防退化）], [唐杰课明确鼓励的方向；前沿无标准答案],
  )
]
]

== 三、代写清单（脚手架，Agent 负责，共 8 项）

#block(width: 100%, above: 8pt, below: 10pt)[
#text(size: 9pt)[
  #table(
    columns: (0.097fr, 0.474fr, 0.429fr),
    inset: (x: 7pt, y: 5pt),
    align: left + top,
    stroke: (x, y) => (bottom: if y == 0 { 0.9pt + luma(105) } else { 0.25pt + luma(220) }),
    table.header([编号], [代写内容], [交付形态]),
    [B1], [环境与依赖（uv / CUDA / 镜像 / 引导脚本）], [#raw("环境/bootstrap*.sh") + #raw("uv.lock")],
    [B2], [数据下载/解压/分片/上传（含 Kaggle Dataset 打包）], [#raw("环境/数据/") 脚本 + 清单],
    [B3], [日志、曲线绘图、实验编排、#strong[断点续训封装]], [#raw("课题NN/脚手架/") 脚本],
    [B4], [判分脚本（拉取 CS336 官方 #raw("tests/") 并接入适配器）], [#raw("环境/judge/") + #raw("judge.sh")],
    [B5], [证据带自动归档（run.yaml / 日志 / 曲线 / 产物哈希）], [#raw("课题NN/证据/") 由脚本生成],
    [B6], [报告模板与排版（Markdown + LaTeX/NeurIPS 模板）], [#raw("环境/报告模板/")],
    [B7], [配额与超时治理（会话预检、超时自停、配额账本）], [#raw("环境/预检.md") + 脚本],
    [B8], [checkpoint 上传/下载与版本管理], [#raw("课题NN/脚手架/ckpt_*.sh")],
  )
]
]

== 四、协作区（一起定，你拍板）

#block(width: 100%, above: 8pt, below: 10pt)[
#text(size: 9pt)[
  #table(
    columns: (0.109fr, 0.474fr, 0.417fr),
    inset: (x: 7pt, y: 5pt),
    align: left + top,
    stroke: (x, y) => (bottom: if y == 0 { 0.9pt + luma(105) } else { 0.25pt + luma(220) }),
    table.header([编号], [事项], [分工]),
    [C1], [架构与底座选型、上游引入范围], [Agent 出方案与证据 → 你拍板],
    [C2], [超参搜索空间、指标口径（bpb / CORE / 通过率）], [Agent 出方案 → 你定口径],
    [C3], [实验优先级与是否值得重跑], [Agent 给成本估算 → 你决定],
    [C4], [可验证环境的题目设计], [你出设计意图 → Agent 评估可行性与成本],
  )
]
]

== 五、违规示例（判例，会长大）

- #strong[E-01（预防性记录）]：Agent 往 #raw("手写/") 里写入实现文件 —— 即使内容正确也算违规， 必须改为"审查意见 + 测试建议"落到 #raw("判卷记录.md")。
- #strong[E-02（预防性记录）]：Agent 说"你可以参考 nanochat 的 #raw("flash_attention.py") 第 30 行" —— 违规。 正确做法：说明该文件#strong[在整体架构中的位置与接口契约]，指出官方 Triton 教程与 CS336 A2 handout 的对应章节。
- #strong[E-03（预防性记录）]：Agent 帮你把实验卡写好之后直接开始烧 GPU 时间 —— 违规。 实验卡必须由你确认（哪怕只是回一句"跑"）。

== 六、边界自检（每次动手前问一遍）

+ 我现在要写的这个文件，属于 R1–R10 还是 B1–B8？
+ 如果是 R 类 → 我只能读、只能评论，不能写。
+ 如果是 B 类 → 我必须写，且要写完整（不留 TODO 给用户）。
+ 如果两边都不是 → 进协作区，先出方案再动手。

#pagebreak()

= AI 使用红线（本学科版）

#block(width: 100%, above: 9pt, below: 9pt, inset: (left: 12pt, right: 8pt, y: 6pt), stroke: (left: 3pt + luma(180)), fill: luma(252))[
#text(size: 9.8pt)[
改编自 #strong[Stanford CS336 官方 #raw("AGENTS.md")]（#raw("stanford-cs336/assignment1-basics")，2026-09-17 读取原文）， 按用户的"#strong[分层双轨]"口径改写。CS336 原文的立场是"Teaching Assistant, Not Solution Generator"， 本学科的立场是"#strong[学习目标区=TA，基建区=工程师]"。
]
]

== 一、最高原则

#block(width: 100%, above: 9pt, below: 9pt, inset: (left: 12pt, right: 8pt, y: 6pt), stroke: (left: 3pt + luma(180)), fill: luma(252))[
#text(size: 9.8pt)[
#strong[学习目标（R1–R10）必须由用户亲手完成；非学习目标（B1–B8）必须由 Agent 完成。] 边界见《造轮子边界.md》。任何一端的越界都算事故，写进 #raw("memory/ERRORS.md")。
]
]

== 二、手写区：Agent 应当做（SHOULD）

- 解释概念：#strong[只讲用户卡住的那一层]，不重讲整章；用一个反例或一个玩具例子收尾。
- 指路：指出对应讲义章节（CS336 / d2l / 李宏毅 / rasbt / RLHF Book 的#strong[具体哪一节]）与官方文档。
- 审查用户代码：提 3–5 条意见，#strong[指向"哪个不变量可能被破坏""哪个边界情况没测"]，不直接给修好的代码。
- 帮助 debug：#strong[问引导性问题]（"你检查过 mask 施加在 softmax 之前还是之后吗？"），而不是给修复。
- 解释报错：Python / PyTorch / CUDA / Triton / 分布式栈的报错含义与排查顺序。
- 建议验证手段：形状断言、玩具输入、profiler 检查、消融、梯度检查（数值对照）。

== 三、手写区：Agent 禁止做（SHOULD NOT，照抄 CS336 并加严）

- ✘ 写任何 Python 或伪代码
- ✘ 给出问题的解法或思路解法
- ✘ 完成手写区里的 TODO
- ✘ 编辑用户仓库里的手写区文件
- ✘ 大段重构用户代码变成"成品答案"
- ✘ 把作业要求直接翻译成可运行代码
- ✘ 替用户实现核心组件（tokenizer、transformer 块、优化器、训练循环、Triton kernel、 分布式逻辑、scaling law 管线、数据过滤/去重、对齐/RL 方法）
- ✘ #strong[把第三方实现当答案指路]（CS336 原文：课程材料自包含）——本仓加严：包括 nanochat / minimind / GitHub 上的作业答案库。可以指出"该功能在架构中的#strong[位置与接口契约]"，但不得指出"去抄哪几行"。

== 四、脚手架区：Agent 应当做（且必须做完）

- ✔ #raw("环境/")：依赖锁、引导脚本、会话预检、报告模板、数据打包
- ✔ #raw("脚手架/")：实验编排、日志、曲线绘图、断点续训、checkpoint 管理、判分脚本、证据归档
- ✔ #raw("课程轨/")：课程进度台账、大论文模板与格式整理
- ✔ #raw("memory/")：HANDOFF / PROGRESS / ERRORS / LEARNINGS / MEMORY / drill-ledger 的维护

#strong[判据]：脚手架代码里#strong[不允许留 TODO 给用户]——那是把学习目标混进了基建。

== 五、例外与补偿（本学科特有，CS336 没有）

#block(width: 100%, above: 8pt, below: 10pt)[
#text(size: 9pt)[
  #table(
    columns: (0.239fr, 0.387fr, 0.375fr),
    inset: (x: 7pt, y: 5pt),
    align: left + top,
    stroke: (x, y) => (bottom: if y == 0 { 0.9pt + luma(105) } else { 0.25pt + luma(220) }),
    table.header([情形], [允许], [补偿动作]),
    [用户明说"卡死了，给我看答案"], [走提示阶梯五级，第 5 级给答案], [#strong[必须]挂"近迁移重考"卡（隔 1–3 天、无提示、换场景复考）],
    [用户连续 2 轮在同一处打转], [由我提议"降档"：给一个#strong[更小的可跑通示例]（不是我写他的目标代码）], [记录到 #raw("ERRORS.md")，下一课换讲法],
    [环境/工具链阻塞（非学习目标）], [直接由我修好，不占用用户时间], [记入 #raw("证据/") 的环境变更],
  )
]
]

== 六、教学法提示（照抄 CS336 的方法论，本学科已内化）

用户求助时，按此顺序：①问澄清问题（试过什么/期望什么/发生了什么）→ ②引用讲义概念而非直接回答 → ③建议下一步而不是替他做 → ④审查代码并指出#strong[可能 bug/缺失检查]的方向性提示 → ⑤解释"为什么"而不只是"怎么做" → ⑥#strong[优先用测试与不变量而非修复]。

== 七、学术诚信与"知行合一"的关系（本学科的立场）

CS336：AI 只能用于低层次编程问题与高层次概念问题，不得直接解题； "我们强烈建议在完成作业时关掉 AI 自动补全（Cursor Tab / Copilot）——我们发现它让人更难深入内容。"

#strong[本学科采纳这条建议的一半]：动手写 R1–R10 时，#strong[手写区文件的编辑器内 AI 自动补全也要关] （或在 #raw("脚手架/") 里明确标注禁止生成手写区文件）。理由：本学科的验收标准是"#strong[能改坏并修好]"—— 如果代码是补全出来的，你就没有能力在它坏掉时诊断它。

== 八、越界举报（自检清单，每轮自问）

+ 我这一轮写的文件，属于 R 类还是 B 类？
+ 我给的是"问题"还是"答案"？（给答案前是否走了阶梯、是否挂了重考卡？）
+ 我有没有指路第三方实现？
+ 用户这一轮有没有"预测 → 验证"的环节？没有的话，我是不是又变成讲解器了？

#pagebreak()

= 算力与成本预算（零预算版）

#block(width: 100%, above: 9pt, below: 9pt, inset: (left: 12pt, right: 8pt, y: 6pt), stroke: (left: 3pt + luma(180)), fill: luma(252))[
#text(size: 9.8pt)[
立规 2026-09-17。用户拍板：#strong[零现金预算]，但要求#strong[全量对标唐杰 7 条]（含多卡与长程 Agent）。 本文件证明这个组合可行，并定义它的代价与纪律。
]
]

== 一、免费资源池（2026-09-17 核实）

#block(width: 100%, above: 8pt, below: 10pt)[
#text(size: 9pt)[
  #table(
    columns: (0.132fr, 0.198fr, 0.152fr, 0.146fr, 0.139fr, 0.080fr, 0.152fr),
    inset: (x: 7pt, y: 5pt),
    align: left + top,
    stroke: (x, y) => (bottom: if y == 0 { 0.9pt + luma(105) } else { 0.25pt + luma(220) }),
    table.header([平台], [免费额度], [硬件], [会话上限], [持久存储], [卡要求], [角色]),
    [#strong[Kaggle]], [#strong[30 GPU·小时/周]（每周重置）], [#strong[2×T4（32GB 合计）] 或 1×P100], [9–12h（支持后台运行、每 5 分钟自动存档）], [20GB #raw("/kaggle/working")], [无需], [#strong[主战场]（唯一能做"多卡"的免费档）],
    [Google Colab 免费], [\~15–30 GPU·h/周（未公布，随需求波动）], [1×T4 16GB], [12h，可能提前断], [Google Drive（易失）], [无需], [备用（短实验、CPU 实验）],
    [沙箱 CPU（本仓）], [无限], [2 vCPU / 3GB RAM], [—], [仓库（注意体积纪律）], [无需], [#strong[T0 全部课题的正确性与判分]],
    [Lightning AI 免费档], [约 15 credits/月], [T4/A10G 等], [\~3–4h 重启], [50GB], [无需], [备用（额度与 GPU 型号#strong[未核实]，用前先验）],
    [SageMaker Studio Lab], [4h/次、4h/24h], [1×T4], [4h], [15GB], [需账号], [极端备用],
    [Modal], [$3 0/月 免 费 额 度（C S 3 3 6 赞 助 商，B 2 0 0$6.25/h ≈ 4.8h/月）], [B200], [按任务], [卷], [需国际支付/网络], [#strong[可选升级]，非计划内],
  )
]
]

#strong[结论]：16 周可用 #strong[≈480 GPU·小时]（Kaggle 30h × 16 周），本学科计划只用 #strong[≈97 小时] → #strong[安全系数约 5×]。

== 二、三档规模（零预算下的能力边界）

#block(width: 100%, above: 8pt, below: 10pt)[
#text(size: 9pt)[
  #table(
    columns: (0.128fr, 0.235fr, 0.161fr, 0.360fr, 0.116fr),
    inset: (x: 7pt, y: 5pt),
    align: left + top,
    stroke: (x, y) => (bottom: if y == 0 { 0.9pt + luma(105) } else { 0.25pt + luma(220) }),
    table.header([档], [硬件], [模型规模], [典型任务], [单次时长]),
    [#strong[T0]], [沙箱 CPU / Colab CPU], [1–10M], [课题01–03 全部、判分器、知识卡实验], [分钟级],
    [#strong[T1]], [Kaggle 1×T4 16GB], [0.03–0.1B], [课题05 Triton bench、课题07 数据消融], [1–4h],
    [#strong[T2]], [Kaggle 2×T4 32GB], [0.1B], [课题04 端到端、课题06 DDP、课题08 RL、课题09/10 Agent], [6–12h],
  )
]
]

== 三、成本估算（#strong[标记为估算，必须在课题04 用实测替换]）

- 参考点（实测自 nanochat 公开文档）：#strong[d12 ≈ GPT-1 量级 ≈ 0.1B]，在 8×H100 上约 #strong[6 分钟]。
- T4 是 #strong[SM75，无 bf16]（nanochat 自动退化 fp32，需手动 fp16 + GradScaler 才能提速）； 等效算力约为 H100 的 1/15–1/25。
- #strong[估算]：单 T4 约 12–20h，双 T4 DDP 约 #strong[7–12h]（扩展效率按 60–80% 估）。
- #strong[执行方式]：拆成两个 9h 会话（Kaggle 会话上限 9–12h），中间用 #raw("/kaggle/working") 的 checkpoint 续训。
- ⚠ 这个数字#strong[不许照抄进报告]：课题04 结束后，用实测耗时替换，并在报告里写明"估算 vs 实测"的偏差。

== 四、每周配额分配（16 周）

#block(width: 100%, above: 8pt, below: 10pt)[
#text(size: 9pt)[
  #table(
    columns: (0.161fr, 0.253fr, 0.262fr, 0.324fr),
    inset: (x: 7pt, y: 5pt),
    align: left + top,
    stroke: (x, y) => (bottom: if y == 0 { 0.9pt + luma(105) } else { 0.25pt + luma(220) }),
    table.header([周], [课题], [计划 GPU 用量], [备注]),
    [W1–W4], [课题01–03], [#strong[0 h]], [纯 CPU，零消耗期（先把正确性做对）],
    [W5], [课题04（上）], [6–9 h], [数据管线 + 双 T4 冒烟 + 首轮训练],
    [W6], [课题04（下）], [6–12 h], [收口 + 采样 + 成本账单],
    [W7], [课题05（上）], [4 h], [单 T4（#strong[必须是 T4，P100 不可用]）],
    [W8], [课题05（下）+ 课题06 开题], [6 h], [Triton bench 三图],
    [W9], [课题06], [8 h], [双 T4 DDP/FSDP 对照],
    [W10], [课题07], [6 h], [单 T4 数据消融],
    [W11], [课题08（SFT）], [8 h], [双 T4],
    [W12], [课题08（DPO+RLVR）], [10 h], [双 T4，最贵的一周],
    [W13], [课题09], [6 h], [双 T4 rollout],
    [W14], [课题10], [8 h], [双 T4],
    [W15–W16], [蓄水/补跑/结项], [4+4 h], [弹性],
    [#strong[合计]], [], [#strong[≈97 h / 480 h]], [余量用于重跑与失败实验],
  )
]
]

== 五、硬纪律（出过事故的领域）

+ #strong[实验卡制度]：上 GPU 前必须先写实验卡，经用户确认才开跑。模板：

#block(width: 100%, above: 9pt, below: 9pt, inset: (x: 10pt, y: 8pt), radius: (right: 4pt), fill: luma(248), stroke: (left: 2.5pt + luma(165)))[
  #raw("   ### 实验卡 #NN（课题NN / 模块 M?）
   - 假设（一句话，可被证伪）：
   - 命令（完整可复制）：
   - 预算上限：≤ ? GPU·小时（默认 3）
   - 停止条件：loss 不降 / 超过预算 / 出现 NaN → 立即停
   - 成功判据（跑之前先写死）：
   - 预期现象（**先写预测**，跑完对照——这是知行合一的咬合点）：
   - 产物归档：证据/run.yaml + 日志 + 曲线 + 哈希", block: true, lang: "markdown")
]

+ #strong[会话预检]（每次开 Kaggle 先跑）：#raw("nvidia-smi") 看型号 → #strong[T4 或 2×T4 才继续；P100 立即重开会话]（SM60，Triton 不可用，课题05 会在上面白烧配额）。
+ #strong[断点续训是强制项]：Kaggle 会话随时可能断；每 N 步写 checkpoint 到 #raw("/kaggle/working")（20GB 持久）。
+ #strong[超时自停]：脚本内自带 wall-clock 上限（默认 3h），到点保存退出，不靠人盯。
+ #strong[配额账本]：跑完立刻在 #raw("memory/PROGRESS.md") 记：日期 / 平台 / GPU 型号 / 实际耗时 / 累计消耗 / 本周余量。
+ #strong[不做无判据的实验]：没有"成功判据"就不许开跑——这是防止"烧配额摸鱼"的唯一有效办法。

== 六、可选升级路径（仅在零预算实在卡住时启动，需用户拍板）

#block(width: 100%, above: 8pt, below: 10pt)[
#text(size: 9pt)[
  #table(
    columns: (0.212fr, 0.388fr, 0.400fr),
    inset: (x: 7pt, y: 5pt),
    align: left + top,
    stroke: (x, y) => (bottom: if y == 0 { 0.9pt + luma(105) } else { 0.25pt + luma(220) }),
    table.header([方案], [价格（2026 公开比价，#strong[下单前以平台现价为准]）], [何时值得]),
    [国内云 4090 按量], [¥1.45–2.0/小时（AutoDL / 恒源云 / 智星云等）], [双 T4 跑不动 0.1B RL（W12）时；约 ¥30 可买 15h],
    [Modal 免费额度], [\$30/月（≈4.8h B200）], [需要 bf16 + 快迭代时（需国际支付）],
    [Colab Pro], [订阅制], [不建议（免费档足够本学科用量）],
  )
]
]

#block(width: 100%, above: 9pt, below: 9pt, inset: (left: 12pt, right: 8pt, y: 6pt), stroke: (left: 3pt + luma(180)), fill: luma(252))[
#text(size: 9.8pt)[
诚实声明：本学科的设计前提是"#strong[免费额度足够]"，依据是 §三 的估算与 §四 的配额表。 若课题04 实测发现双 T4 需要 \>20h，则触发"规模下探一级"（d12 → d10，或语料减半）， #strong[而不是]自动升级付费；升级必须由用户单独拍板。
]
]

#pagebreak()

= 判分与验收标准

#block(width: 100%, above: 9pt, below: 9pt, inset: (left: 12pt, right: 8pt, y: 6pt), stroke: (left: 3pt + luma(180)), fill: luma(252))[
#text(size: 9.8pt)[
立标 2026-09-17。继承仓库总纲 #raw("skills/科研式学习导师/SKILL.md") §5a《命题与判卷纪律》， 并按本学科"可执行判分"的特性做加法。#strong[与总纲冲突处，以本文件的更严条款为准。]
]
]

== 一、三层判分（每一层都必须留下原始输出）

#block(width: 100%, above: 8pt, below: 10pt)[
#text(size: 9pt)[
  #table(
    columns: (0.169fr, 0.254fr, 0.310fr, 0.266fr),
    inset: (x: 7pt, y: 5pt),
    align: left + top,
    stroke: (x, y) => (bottom: if y == 0 { 0.9pt + luma(105) } else { 0.25pt + luma(220) }),
    table.header([层], [谁判], [判据], [归档]),
    [#strong[L1 自动判分]], [判分器（pytest / 自建 script）], [通过 / 失败 / 覆盖率 / 指标数字], [#raw("判卷记录.md") 贴#strong[原始输出]（不许转述）],
    [#strong[L2 导师审稿]], [我], [3–5 条：必考项 / 要记住 / 预告项（含"哪里可能在自欺"）], [#raw("判卷记录.md")],
    [#strong[L3 费曼收口]], [你讲 + 我追问], [三条硬标准（讲清 / 指代码 / 改坏修好）], [#raw("判卷记录.md") + #raw("知识卡")],
  )
]
]

#strong[L1 不通过 → 不进 L2/L3]；L3 不通过 → 课题不标 ✔，写进 HANDOFF 的"下一句"。

== 二、通用红线（继承总纲 + 本学科加严）

+ #strong[结果对 ≠ 满分]：本学科分数按"证据链"给，逻辑链完整才满分（总纲 §5a 第 5 条）。
+ #strong[没有预测的实验不算实验]：跑之前必须先写"预期现象"（见实验卡），否则 L1 直接判不合格。
+ #strong[无证据的结论不采纳]：曲线要原始日志/repro 命令；截图要能追溯到 run.yaml。
+ #strong[no-go 不擦除]：失败的实验、被推翻的假设全部留在 #raw("证据/")，并在报告里如实呈现。
+ #strong[口径统一]：跨模型比较必须同数据集、同 token 化、同评测脚本；指标优先用#strong[词表无关]的 bpb。
+ #strong[不许自创指标]：新增指标必须给出定义 + 为什么已有的不管用 + 与已有指标的相关性。
+ #strong[误差棒是必填项]：任何"变好了"的结论都要给多次运行的范围（至少 2 个种子）。
+ #strong[不许把测试集当验证集反复调]（M7 常见自欺）。
+ #strong[掌握的定义]（总纲 §5a 第 8 条原文）：当次对 + #strong[隔 1–3 天无提示再对] + 能讲清为什么。
+ #strong[宣布"通过"必须附证据引用]：哪份判分输出、哪个数字、哪些 leech 已清零。

== 三、每课题的"通过证据"清单（缺一不可）

#block(width: 100%, above: 8pt, below: 10pt)[
#text(size: 9pt)[
  #table(
    columns: (0.046fr, 0.133fr, 0.250fr, 0.179fr, 0.175fr, 0.217fr),
    inset: (x: 7pt, y: 5pt),
    align: left + top,
    stroke: (x, y) => (bottom: if y == 0 { 0.9pt + luma(105) } else { 0.25pt + luma(220) }),
    table.header([\#], [课题], [L1 自动判分], [L2 审稿关注], [L3 收口动作], [额外证据]),
    [01], [BPE 分词器], [#raw("test_tokenizer.py") + #raw("test_train_bpe.py") 全绿], [边界：空串、单字节、中文、emoji、往返], [手写一段中文的编码过程并解释], [压缩率表（中/英）+ 往返一致性],
    [02], [Transformer 骨架], [#raw("test_model.py")、#raw("test_nn_utils.py") 全绿], [形状/初始化/数值稳定性], [白板上画出一次前向的数据流], [#strong[三组改坏实验]（去 mask / 换位置编码 / 去残差）曲线],
    [03], [Scaling Law], [自建：拟合优度 + 外推误差], [数据点是否同口径、是否外推过远], [复述"为什么用幂律而不是线性"], [5 点 sweep 原始数据 + #strong[预测先写死再跑]的记录],
    [04], [0.1B 端到端], [自建：loss/bpb 达标 + 采样可读性], [是否过拟合/是否记住了测试集], [讲清"这个模型会什么、不会什么"], [采样样本 + #strong[实测成本 vs 估算偏差]],
    [05], [Triton kernel], [CS336 A2 正确性对齐（误差 \< 容差）], [数值稳定性、边界 block、dtype], [讲清 online softmax 为什么必要], [speedup/显存/profile 三图 + #strong[硬件口径声明]],
    [06], [多卡与分布式], [扩展效率数据 + 梯度一致性检查], [通信占比是否解释得通], [讲清"为什么不是 2 倍"], [扩展曲线 + 通信时间分解],
    [07], [数据清洗去重], [自建：规则单测 + 对照组], [规则是否过严（伤数据）或过松], [讲清每条规则的代价], [规则清单 + 有/无清洗的对照],
    [08], [SFT/DPO/RLVR], [#raw("test_grpo.py") 全绿 + 三方对照], [是否 reward hacking、是否能力回退], [逐项解释 GRPO 损失每一项], [三方对照表（同口径）+ 失败样本分析],
    [09], [可验证环境], [判定逻辑单测 + rollout 脚本], [假阳性/假阴性样例], [讲清"什么算完成"的判定], [成功率 + 失败轨迹分类],
    [10], [长程 Agent], [消融数据 + 轨迹日志], [self-judge 是否在放大错误], [讲清"什么时候 self-judge 有害"], [有无 self-judge 的成功率差],
    [11], [结项], [报告格式审查（NeurIPS）+ demo 可运行], [结论是否超出证据范围], [自我攻击 3 条 + 现场答疑], [英文报告 + demo + 总复盘],
  )
]
]

== 四、成绩口径（对齐唐杰作业的 40% / 60%）

#block(width: 100%, above: 8pt, below: 10pt)[
#text(size: 9pt)[
  #table(
    columns: (0.109fr, 0.148fr, 0.432fr, 0.311fr),
    inset: (x: 7pt, y: 5pt),
    align: left + top,
    stroke: (x, y) => (bottom: if y == 0 { 0.9pt + luma(105) } else { 0.25pt + luma(220) }),
    table.header([项], [权重], [内容], [判据]),
    [平时作业], [#strong[40%]], [课题01–09 的 L1+L2+L3], [每课题等权，未过者按比例扣],
    [大项目], [#strong[60%]], [课题04+08+10+11 构成的整机（端到端模型 + 对照实验 + Agent 尾巴 + 报告）], [#strong[问题、动机、方法、结果一项都不能糊]（唐杰原话）],
  )
]
]

#block(width: 100%, above: 9pt, below: 9pt, inset: (left: 12pt, right: 8pt, y: 6pt), stroke: (left: 3pt + luma(180)), fill: luma(252))[
#text(size: 9.8pt)[
注意：课程轨（CORE100299）的成绩由#strong[老师]给，本表只用来自我标定； 但#strong[课程大论文（70%）直接取用实训轨 W8 前的成果]，所以两份成绩是同一份劳动的两个出口。
]
]

== 五、自欺自查清单（结项前必过）

+ 我报的每个数字，#strong[能在 #raw("证据/") 里找到原始日志]吗？
+ 我的"变好了"，有没有可能是评测口径变了 / 提示词变了 / 只挑了好种子？
+ 我有没有把#strong[训练集上的表现]当成了能力？
+ 我写下的每个"因为…所以…"，有没有#strong[反事实检验]（去掉这个因素会怎样）？
+ 我的图，#strong[坐标轴和误差棒]都标了吗？有没有截断坐标轴让差距显得很大？
+ 我的结论，#strong[最强的反方论点]是什么？写进报告了吗？

#pagebreak()

= 上游锁定清单（本学科只读依赖）

#block(width: 100%, above: 9pt, below: 9pt, inset: (left: 12pt, right: 8pt, y: 6pt), stroke: (left: 3pt + luma(180)), fill: luma(252))[
#text(size: 9.8pt)[
立单 2026-09-17。纪律：#strong[只记 commit + 用途 + 只引哪些路径]，不整仓复制（仓库有体积上限）。 换机器恢复的方式写在"复现命令"里。#strong[引入日期一律记当日，半年后重审一次]。
]
]

== 一、骨架依赖（必须锁，判分与训练都靠它）

#block(width: 100%, above: 8pt, below: 10pt)[
#text(size: 9pt)[
  #table(
    columns: (0.211fr, 0.122fr, 0.101fr, 0.112fr, 0.214fr, 0.240fr),
    inset: (x: 7pt, y: 5pt),
    align: left + top,
    stroke: (x, y) => (bottom: if y == 0 { 0.9pt + luma(105) } else { 0.25pt + luma(220) }),
    table.header([仓库], [commit], [引入日], [许可], [用途], [只用哪些路径]),
    [#raw("stanford-cs336/assignment1-basics")], [#raw("a158843b2010")], [2026-09-17], [MIT], [课题01/02 判分器 + handout], [#raw("tests/")、#raw("cs336_basics/")（仅接口）、PDF],
    [#raw("stanford-cs336/assignment2-systems")], [#raw("ca8bc81a59b7")], [2026-09-17], [MIT], [课题05/06 判分器], [#raw("tests/")、#raw("cs336_systems/")（空壳）、PDF],
    [#raw("stanford-cs336/assignment3-scaling")], [#raw("03e9372992e9")], [2026-09-17], [MIT], [课题03 规格参考（#strong[API 不可用，只读设计]）], [PDF、#raw("cs336_scaling/")],
    [#raw("stanford-cs336/assignment4-data")], [#raw("0555bea66369")], [2026-09-17], [MIT], [课题07 过滤/去重规格], [#raw("tests/")、#raw("configs/")、PDF],
    [#raw("stanford-cs336/assignment5-alignment")], [#raw("c2734a263087")], [2026-09-17], [⚠ 未声明（用前确认）], [课题08 判分器（#raw("tests/test_grpo.py")）], [#raw("tests/")、#raw("data/")、PDF],
    [#raw("stanford-cs336/lectures")], [#raw("de53a9f979a6")], [2026-09-17], [⚠ 未声明], [讲义（#raw("lecture_01.py")…#raw("lecture_17.py")、PDF）], [全仓可读（文本量小）],
    [#raw("karpathy/nanochat")], [#raw("92d63d4e8bb4")], [2026-09-17], [MIT], [课题04/05/06 的工程底座与对照实现], [#raw("nanochat/")、#raw("scripts/")、#raw("runs/")、#raw("tasks/")、#raw("tests/")],
  )
]
]

#strong[复现命令（换机器照抄）]：

#block(width: 100%, above: 9pt, below: 9pt, inset: (x: 10pt, y: 8pt), radius: (right: 4pt), fill: luma(248), stroke: (left: 2.5pt + luma(165)))[
  #raw("mkdir -p 上游 && cd 上游
for r in stanford-cs336/assignment1-basics stanford-cs336/assignment2-systems \\
         stanford-cs336/assignment5-alignment karpathy/nanochat; do
  n=$(basename $r); git clone --depth 1 https://github.com/$r $n
done
cd assignment1-basics && git fetch --depth 1 origin a158843b2010 && git checkout a158843b2010", block: true, lang: "bash")
]

== 二、知识线依赖（只读，不入仓）

#block(width: 100%, above: 8pt, below: 10pt)[
#text(size: 9pt)[
  #table(
    columns: (0.210fr, 0.184fr, 0.109fr, 0.141fr, 0.115fr, 0.240fr),
    inset: (x: 7pt, y: 5pt),
    align: left + top,
    stroke: (x, y) => (bottom: if y == 0 { 0.9pt + luma(105) } else { 0.25pt + luma(220) }),
    table.header([仓库 / 站点], [commit / 版本], [引入日], [许可], [对标模块], [用法]),
    [#raw("rasbt/reasoning-from-scratch")], [#raw("b2e0841ee8be")], [2026-09-17], [Apache-2.0], [M6/M7/M8], [#strong[教学法范本]（ch3 先建评测）；ch2–4 可 CPU 跑],
    [#raw("rasbt/LLMs-from-scratch")], [#raw("ace7c08802b5")], [2026-09-17], [见仓库（NOASSERTION）], [M2–M4], [代码级最细的对照读物（附录 GQA/MoE/KV cache）],
    [#raw("huggingface/agents-course")], [#raw("b3946b1d09d2")], [2026-09-17], [Apache-2.0], [M8], [Agent 三框架 + 最终项目排行榜],
    [#raw("harbor-framework/terminal-bench")], [#raw("7a337a834bff")], [2026-09-17], [Apache-2.0], [M8], [长程 Agent 基准（v2；v1 已冻结为 #raw("terminal-bench-1")）],
    [#raw("PrimeIntellect-ai/verifiers")], [#raw("ff3b8dc551ba")], [2026-09-17], [MIT], [M7/M8], [可验证环境抽象（课题09 参照，不引入代码）],
    [#raw("jingyaogong/minimind")], [#raw("7a9137d2e902")], [2026-09-17], [Apache-2.0], [M2–M6], [中文术语与 RL 脚本对照（读，不抄进手写区）],
    [#raw("walkinglabs/hands-on-modern-rl")], [#raw("9f6e429c6894")], [2026-09-17], [⚠ NOASSERTION], [M6], [中文 RL→RLVR 教材（含免费在线 Notebook）],
    [#raw("McGill-NLP/nano-aha-moment")], [#raw("5314e6f8fc60")], [2026-09-17], [MIT], [M6], [单文件 GRPO（阅读；已停更，不作依赖）],
    [#raw("THUDM/slime")], [#raw("4c193f1f3750")], [2026-09-17], [Apache-2.0], [M8/M9], [智谱自家 Agentic RL 基建（W14 后的进阶读物）],
    [#raw("KellerJordan/modded-nanogpt")], [#raw("ecbb586296d3")], [2026-09-17], [MIT], [M4], [单卡 speedrun 思路；#strong[注意其验证指标口径争议]],
    [#raw("datajuicer/data-juicer")], [#raw("1e9720d01610")], [2026-09-17], [Apache-2.0], [M4/M7], [课题07 数据清洗的规则参考],
    [#raw("d2l-ai/d2l-zh")], [#raw("e6b18ccea714")（2023-08-18）], [2026-09-17], [Apache-2.0], [M0/M1/M3/M5], [中文地基读物；⚠ #strong[仓库 2023 后基本停更]，内容仍有效但别等更新],
  )
]
]

== 三、许可与合规注意

+ #raw("stanford-cs336/assignment5-alignment") 与 #raw("lectures") 仓库#strong[未声明 SPDX 许可]： #strong[只做本地学习与对照，不复制进本仓、不再分发]。
+ #raw("walkinglabs/hands-on-modern-rl") 为 NOASSERTION：同样只读、不复制。
+ 所有上游代码#strong[一律不进本仓 git]（体积 + 许可双理由）；本仓只保留 commit 记录与引用的路径清单。
+ 数据：只用 TinyStories（公开）、#raw("stanford-cs336/owt-sample")（课程公开样本）、以及自己清洗的小语料； ⚠ 不要引用 #raw("HuggingFaceFW/fineweb") / #raw("huggingface/fineweb")（2026-09-17 实测均 404）。

== 四、重审机制

- 每学期期初（下一次：2027-02）重跑一遍 #raw("gh api") 检查：上游是否改名/归档/换许可；
- CS336 每年改 handout（A5 已从 Qwen-2.5-Math 换为 Olmo-2-1B，新增 GSPO/MaxRL）， #strong[重审时必须重新读 CHANGELOG]，否则会拿着旧讲义做新作业。

#pagebreak()

= 课题01 开题简报 · BPE 分词器

#block(width: 100%, above: 9pt, below: 9pt, inset: (left: 12pt, right: 8pt, y: 6pt), stroke: (left: 3pt + luma(180)), fill: luma(252))[
#text(size: 9.8pt)[
模块：#strong[M2 分词与表示] ｜ 周次：#strong[W1（09-14→09-20）] ｜ 算力：#strong[T0 纯 CPU，0 GPU·小时] 唐杰作业对应：#strong[① 从零写 Tokenizer] 的前半 ｜ 判分来源：#strong[CS336 A1 #raw("tests/test_tokenizer.py") + #raw("test_train_bpe.py")] 手写/代写：本课题#strong[全部核心代码属手写区 R1]（见《造轮子边界.md》）
]
]

#v(4pt)
#line(length: 100%, stroke: 0.6pt + luma(200))
#v(4pt)

== 一、研究背景（这个问题历史上卡过谁）

- 2017 年前的 NLP 用整词表，未登录词（OOV）是死穴；字符级建模又让序列变得极长。
- BPE 从 2016（Sennrich 等）的#strong[机器翻译子词切分]技术，被 GPT-2（2019）引入到#strong[字节级]， 从此成为大模型的事实标准（GPT-2/3/4、LLaMA、Qwen、GLM 都是 BPE 系）。
- 关键洞察：#strong[词表不是"词汇表"，而是一个可学习的压缩算法]——它同时决定了 ①模型的输入长度 ②嵌入层参数量 ③模型能见到的最小语义单元 ④多语言/代码/数学的公平性。

== 二、研究问题（一句话，开放问题）

#block(width: 100%, above: 9pt, below: 9pt, inset: (left: 12pt, right: 8pt, y: 6pt), stroke: (left: 3pt + luma(180)), fill: luma(252))[
#text(size: 9.8pt)[
#strong[在固定词表预算下，如何设计一个训练-编码两阶段都正确、且对中文/英文/代码都公平的子词分词器？] ——并回答：为什么"字节起步"是零预算下唯一不会翻车的选择？
]
]

== 三、攻关线索（路标，不是答案）

+ #strong[压缩视角]：如果词表大小为 V，BPE 训练在最大化什么？把它写成"每一步减少多少 token 数"。
+ #strong[字节起步的理由]：从 Unicode 字符起步会在哪些具体输入上崩？（想 3 个真实例子再往下走）
+ #strong[训练算法]：朴素实现为什么是 O(n²)？哪些数据结构能把它压到近似线性？（提示方向：不要用字符串拼接）
+ #strong[并列与终止]：最高频并列时怎么办？什么时候停止合并？特殊 token（#raw("<|endoftext|>")）为什么不能参与合并？
+ #strong[编码与解码]：encode 的时候，遇到未在 merge 表里的相邻对怎么处理？为什么必须保证 #raw("decode(encode(x)) == x")（往返一致性）？
+ #strong[多语言公平性]：同一段中文，字节级 BPE 的 token 数为什么比英文多？这对模型的"中文成本"意味着什么？

== 四、里程碑（可勾选，3–6 个）

- □ #strong[M1 手写 BPE 训练]：能从语料统计词频、迭代合并、输出 merge 表与词表，并#strong[打印出前 10 个 merge 及其频次]
- □ #strong[M2 手写编码器]：支持特殊 token、未登录字节回退、往返一致性（自测 5 类边界：空串/单字节/中文/emoji/控制字符）
- □ #strong[M3 通过官方判分]：#raw("test_tokenizer.py") 与 #raw("test_train_bpe.py") 全绿（原始输出贴 #raw("判卷记录.md")）
- □ #strong[M4 压缩率对照]：在 TinyStories（英）与中文小语料上各训一个 32k 词表，出压缩率表 + 与你的下注对照
- □ #strong[M5 改坏实验（必做）]：①禁用 bytes 回退 ②不处理特殊 token ③停止条件改成"合并到只剩 1 个词" ——每个先写#strong[预测]，再跑，再记录现象
- □ #strong[M6 一页报告 + 知识卡]：报告按一页四段；知识卡 ≥3 张进 drill-ledger

== 五、交付物要求

#block(width: 100%, above: 8pt, below: 10pt)[
#text(size: 9pt)[
  #table(
    columns: (0.157fr, 0.373fr, 0.470fr),
    inset: (x: 7pt, y: 5pt),
    align: left + top,
    stroke: (x, y) => (bottom: if y == 0 { 0.9pt + luma(105) } else { 0.25pt + luma(220) }),
    table.header([交付物], [位置], [验收]),
    [实现代码], [#raw("手写/")（你写）], [通过 M3],
    [判分原始输出], [#raw("判卷记录.md")], [粘贴 #raw("证据/judge-*.log") 原文（不许转述）],
    [证据], [#raw("证据/")], [#raw("run.yaml")（commit/时间/命令）+ 日志 + 压缩率表 + 改坏实验记录],
    [报告], [#raw("报告.md")], [一页四段：问题-动机-方法-结果],
    [知识卡], [#raw("memory/drill-ledger/topics/")], [≥3 张（bytes 回退 / merge 规则 / 压缩率权衡）],
  )
]
]

== 五之二、官方判分标准（2026-09-17 实跑探明，#strong[先知道标准再动手]）

判分器已接通：#raw("环境/judge/judge.sh 01")。实跑探明 #strong[28 个测试]（27 项 + 1 项 xfail），要求如下：

=== 接口契约（你唯一需要遵守的外部形状）

#block(width: 100%, above: 9pt, below: 9pt, inset: (x: 10pt, y: 8pt), radius: (right: 4pt), fill: luma(248), stroke: (left: 2.5pt + luma(165)))[
  #raw("# 手写/bpe.py 必须提供：
def train_bpe(input_path, vocab_size, special_tokens, **kwargs) -> tuple[dict[int, bytes], list[tuple[bytes, bytes]]]
class Tokenizer:
    def __init__(self, vocab, merges, special_tokens=None): ...
    def encode(self, text: str) -> list[int]: ...
    def decode(self, ids: list[int]) -> str: ...
    def encode_iterable(self, iterable) -> Iterator[int]: ...   # ← 隐藏要求，见下", block: true, lang: "python")
]

=== 三条硬门槛（都会挂人）

#block(width: 100%, above: 8pt, below: 10pt)[
#text(size: 9pt)[
  #table(
    columns: (0.041fr, 0.291fr, 0.410fr, 0.258fr),
    inset: (x: 7pt, y: 5pt),
    align: left + top,
    stroke: (x, y) => (bottom: if y == 0 { 0.9pt + luma(105) } else { 0.25pt + luma(220) }),
    table.header([\#], [测试], [门槛], [说明]),
    [1], [#raw("test_train_bpe_speed")], [corpus.en + vocab 500 #strong[\< 1.5 秒]], [官方参考 0.38s；"玩具实现"约 3s 会挂],
    [2], [#raw("test_train_bpe")], [merges #strong[逐项等于]参考 merges；vocab 键值集合一致], [意味着预处理与#strong[并列打破规则]都要与参考一致],
    [3], [#raw("test_encode_iterable_memory_usage")], [用 #raw("encode_iterable") 流式读 #strong[5MB] 语料，额外内存 #strong[≤ 1MB]（#raw("RLIMIT_AS") 实测）], [#strong[必须有真正的流式实现]，不能先 read() 全部],
  )
]
]

=== 一个官方"故意让分"的测试（别被骗）

- #raw("test_encode_memory_usage") 被官方标记 #strong[#raw("xfail")]，理由原话： #emph["Tokenizer.encode is expected to take more memory than allotted (1MB)"]。 → 也就是说：#strong[#raw("encode()") 超内存是允许的，#raw("encode_iterable()") 超内存是不允许的]。 这个 xfail 恰好是本课题"接口设计决定内存上界"的活教材（见知识地图 M5 的同类问题）。

=== 对齐口径的隐含要求

- 与 #strong[tiktoken 的 GPT-2] 逐 id 对齐 → 编码时必须#strong[严格按 merges 的 rank 顺序]合并， 而不是"最长匹配优先"；且需处理 #raw("allowed_special") 与重叠特殊 token（#raw("test_overlapping_special_tokens")）。
- 往返一致性覆盖：空串 / 单字符 / Unicode / 多行 / 特殊 token 尾随换行 / 地址文本 / 德语 / TinyStories。

== 六、开题批（开场直接发给用户，3–5 题）

#block(width: 100%, above: 9pt, below: 9pt, inset: (left: 12pt, right: 8pt, y: 6pt), stroke: (left: 3pt + luma(180)), fill: luma(252))[
#text(size: 9.8pt)[
见 #raw("../memory/HANDOFF.md") 的"课题01 开题批"五题（下注题 / 概念题 / 手算题 / 权衡题 / 工程题）。 #strong[第 1 题（中文 token 倍数）必须先存档预测]，它是本学科第一条"预测→打脸"链路。
]
]

== 七、讲课锚点（知行合一的"讲"这一腿）

- #strong[讲什么]：M2 的五个核心问题（压缩视角 → 字节起步 → 训练算法 → 编码与往返 → 多语言成本）
- #strong[对标材料]（三师制）：
  - 主线：#strong[CS336 A1 handout] 的 tokenizer 章节（英文，规格权威）
  - 中文：#strong[李沐 d2l ch14.6 子词嵌入]；或 #strong[minimind 的 #raw("train_tokenizer.py") 中文注释]（只读，不得抄进手写区）
  - 补充：#strong[HF LLM Course ch2]（"Implement BPE/WordPiece/Unigram from the ground up"）
- #strong[讲完必出代码级提问（3–5 道，示例）]：
  + 把 merge 循环里"统计相邻对频次"改成"只统计出现次数 \>1 的对"，词表会变得更好还是更差？预测并说明。
  + 你的 encode 如果按"最长匹配优先"而不是"按 merge 顺序"，往返一致性还成立吗？
  + 词表里如果混入一个#strong[重复的 token]，哪一步会先崩溃？

== 八、参考实现（#strong[只准用于对照，不准抄]）

- #raw("karpathy/nanochat") 的 #raw("nanochat/tokenizer.py")（接口设计与特殊 token 处理）
- #raw("rasbt/LLMs-from-scratch") ch2 附带的 "BPE From Scratch"
- ⚠ 纪律：GS=看接口与设计思路，#strong[不看实现细节]；你的代码必须自己写。 判据：M5 的改坏实验能不能被你解释——抄来的人在这里一定卡住。

#pagebreak()

= 判卷记录 · 课题01 BPE 分词器

#block(width: 100%, above: 9pt, below: 9pt, inset: (left: 12pt, right: 8pt, y: 6pt), stroke: (left: 3pt + luma(180)), fill: luma(252))[
#text(size: 9.8pt)[
判分器：#raw("环境/judge/judge.sh 01")（CS336 官方 2026 测试，锁 commit #raw("a158843b2010")，test\_#emph[.py 未改一字） 归档规则：只贴]#emph[原始输出]\*，不做美化、不做转述（《判分与验收标准.md》§二-3）。
]
]

#v(4pt)
#line(length: 100%, stroke: 0.6pt + luma(200))
#v(4pt)

== L1 · 基线（2026-09-17 立科时实跑）

#block(width: 100%, above: 8pt, below: 10pt)[
#text(size: 9pt)[
  #table(
    columns: (0.209fr, 0.791fr),
    inset: (x: 7pt, y: 5pt),
    align: left + top,
    stroke: (x, y) => (bottom: if y == 0 { 0.9pt + luma(105) } else { 0.25pt + luma(220) }),
    table.header([项], [结果]),
    [命令], [#raw("环境/judge/judge.sh 01")],
    [结果], [#strong[27 failed, 1 xfailed]],
    [失败原因], [#strong[全部同一原因]：#raw("FileNotFoundError: 手写区还没有实现文件")（接线层主动抛出的友好提示）],
    [判分器状态], [✔ 管线已验证可执行（28 个测试全部被收集并运行，非网络/环境错误）],
    [结论], [这是#strong[正确的初始状态]：判分器就位，只差 #raw("手写/bpe.py")],
  )
]
]

#strong[当初实跑的关键片段]（完整输出会由脚本落到 #raw("证据/judge-*.log")）：

#block(width: 100%, above: 9pt, below: 9pt, inset: (x: 10pt, y: 8pt), radius: (right: 4pt), fill: luma(248), stroke: (left: 2.5pt + luma(165)))[
  #raw("FAILED tests/test_train_bpe.py::test_train_bpe_speed - FileNotFoundError
FAILED tests/test_train_bpe.py::test_train_bpe - FileNotFoundError
FAILED tests/test_train_bpe.py::test_train_bpe_special_tokens - FileNotFoundError
FAILED tests/test_tokenizer.py::... （24 项，含 test_encode_iterable_memory_usage）
======================== 27 failed, 1 xfailed in 3.67s =========================", block: true)
]

#block(width: 100%, above: 9pt, below: 9pt, inset: (left: 12pt, right: 8pt, y: 6pt), stroke: (left: 3pt + luma(180)), fill: luma(252))[
#text(size: 9.8pt)[
注：#raw("1 xfailed") 不是缺陷——它是官方#strong[故意标记]的 #raw("test_encode_memory_usage") （理由："encode 预期会超过 1MB 配额"）。详见 #raw("开题简报.md") §五之二。
]
]

== L2 · 导师审稿意见

◷ 待用户提交首次实现后填写（3–5 条：必考项 / 要记住 / 预告项）。

== L3 · 费曼收口

⬜ 未开始。收口动作：你对着"完全不懂分词的人"讲清 BPE，我装不懂连问三层 （Why → Why not → What if），再抽 1 次"改坏实验"复述。

#v(4pt)
#line(length: 100%, stroke: 0.6pt + luma(200))
#v(4pt)

== 本课题的判分环境坑（已解决，记录备查）

#block(width: 100%, above: 8pt, below: 10pt)[
#text(size: 9pt)[
  #table(
    columns: (0.190fr, 0.373fr, 0.438fr),
    inset: (x: 7pt, y: 5pt),
    align: left + top,
    stroke: (x, y) => (bottom: if y == 0 { 0.9pt + luma(105) } else { 0.25pt + luma(220) }),
    table.header([坑], [现象], [处置]),
    [官方 conftest 需 Python ≥3.12], [官方 #raw("pyproject.toml"): #raw("requires-python = \">=3.12,<3.14\"")；conftest 用 PEP 695 泛型语法，3.11 无法解析], [3.11 下自动改用#strong[等价轻量 conftest]（同一 #raw("snapshot") 夹具语义），并在日志头部如实声明；升到 3.12+ 后自动切回官方原文],
    [tiktoken 需联网下载 GPT-2 词表], [无外网时 #raw("SSLError") 挂掉 12 项对齐测试], [新增 #raw("环境/judge/prefetch_tiktoken.py")：用官方 fixture #strong[离线构造] tiktoken 缓存（encoder.json 哈希与 tiktoken 内置期望一致，已验证 n\_vocab=50257）],
    [PyTorch CPU 专用源不可达], [#raw("download.pytorch.org") SSL 被拦], [bootstrap 改为：默认不装 torch（课题01 不需要）；#raw("--with-torch") 时先试 CPU 源、失败退回 PyPI],
  )
]
]

#pagebreak()

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

#pagebreak()

= 课题03 开题简报 · Scaling Law 预演与打脸链路

#block(width: 100%, above: 9pt, below: 9pt, inset: (left: 12pt, right: 8pt, y: 6pt), stroke: (left: 3pt + luma(180)), fill: luma(252))[
#text(size: 9.8pt)[
模块：#strong[M4] ｜ 周次：#strong[W4（10-05→10-11）] ｜ 算力：#strong[T0 纯 CPU（极小规模 sweep）] 唐杰作业对应：#strong[③ 拟合 scaling law 再外推] ｜ 判分来源：#strong[无官方判分器]（CS336 A3 需 8 位学号 API key，不可得）→ #strong[自建判分：预测 vs 实测的偏差] 手写：#strong[R6（拟合与外推）]
]
]

#v(4pt)
#line(length: 100%, stroke: 0.6pt + luma(200))
#v(4pt)

== 一、研究背景

Kaplan 等（2020）与 Chinchilla（2022）发现：loss 随参数量 $N$ 与数据量 $D$ 呈#strong[幂律下降]， 且存在一个#strong[算力最优配比]。这条规律是"为什么敢花几千万训一次大模型"的全部依据。 但初学者最常见的错误是：#strong[把外推当预言]，不做回溯验证就把曲线画到天上去。

本课题的核心不是"拟合出一条漂亮的线"，而是#strong[建立"预测 → 验证 → 承认偏差"的科研习惯]。 这也是本学科"预测—打脸日志"（#raw("memory/MEMORY.md")）的主要产地。

== 二、研究问题（一句话）

#block(width: 100%, above: 9pt, below: 9pt, inset: (left: 12pt, right: 8pt, y: 6pt), stroke: (left: 3pt + luma(180)), fill: luma(252))[
#text(size: 9.8pt)[
#strong[在极小规模（我的 CPU 能承受的范围内）跑 4–5 个点，能否外推出更大模型的 loss？外推误差有多大、什么时候会崩？]
]
]

== 三、攻关线索

+ #strong[口径]：横轴用什么？参数量 $N$？token 数 $D$？（提示：固定预算时，$N$ 与 $D$ 不能同时变）
+ #strong[记账]：用 M0 的 $6 N D$ 估算每一次跑的算力，#strong[确保不同点是在"同样算力预算"下比较]（否则曲线无意义）
+ #strong[拟合]：幂律 $L = a N^(-alpha) + c$ 的形式里，那个常数项 $c$ 代表什么？它会不会让外推失效？
+ #strong[外推]：拟合完先#strong[把预测写死在文件里]（带日期），再去跑验证点 —— 顺序不能反
+ #strong[偏差来源]：小规模数据是否"无限数据区"？学习率是否随规模重新调过？#strong[这些都是外推失准的技术原因]

== 四、里程碑

- □ M1 设计 sweep：4–5 个规模点（如 d4/d6/d8/d10），预算固定、口径统一
- □ M2 跑完 sweep，记录每个点的最终 loss/bpb 与耗时（CPU 上即可，分钟级）
- □ M3 拟合幂律并画图（含数据点、拟合线、坐标轴标注）
- □ M4 #strong[先写死外推预测]（例如 d12 的 bpb 预测值 + 置信区间），归档到 #raw("证据/")
- □ M5 跑验证点，计算偏差，并#strong[解释偏差的方向与原因]
- □ M6 一页报告：包含"预测 vs 实测"对照表（#strong[这一条是验收硬指标]）

== 五、交付物

#block(width: 100%, above: 8pt, below: 10pt)[
#text(size: 9pt)[
  #table(
    columns: (0.282fr, 0.353fr, 0.365fr),
    inset: (x: 7pt, y: 5pt),
    align: left + top,
    stroke: (x, y) => (bottom: if y == 0 { 0.9pt + luma(105) } else { 0.25pt + luma(220) }),
    table.header([交付物], [位置], [验收]),
    [sweep 原始数据], [#raw("证据/sweep.csv")], [含配置、loss、耗时、算力估算],
    [拟合脚本与图], [#raw("脚手架/") + #raw("证据/")], [图有坐标轴、有拟合优度],
    [#strong[外推预测存档]], [#raw("证据/预测-<日期>.md")], [跑验证点#strong[之前]的文件时间戳],
    [报告], [#raw("报告.md")], [预测 vs 实测对照表],
  )
]
]

== 六、讲课锚点

- #strong[讲义]：#raw("讲义/M4-M9-待展开大纲.md") 的 M4 部分（W3 展开为完整版 #raw("M4-训练.md")）
- #strong[对标]：CS336 lecture 09/11（scaling laws）· #raw("nanochat/runs/scaling_laws.sh") 与其 miniseries 文档 · d2l 的线性回归/最小二乘（拟合的数学基础）
- #strong[搭桥]：#raw("probability/") 的方差与回归 —— 拟合优度、残差分析直接可用

== 七、代码级提问示例

+ 为什么横轴常画 #strong[FLOPs] 而不是参数量？（提示：Chinchilla 的核心结论是什么）
+ 你拟合出的 $c$（常数项）为负，说明了什么？还能外推吗？
+ 如果两个规模点用了不同的学习率，曲线还能一起拟合吗？为什么？
+ #strong[【下注】] 你预测 d12 的 bpb 会比你拟合线的预测值偏高还是偏低？先写下答案再跑。

== 八、风险与提醒

- ⚠ #strong[不要为了"好看"调学习率]：每个点的超参策略必须写进 #raw("证据/")，否则外推无意义。
- ⚠ 极小规模会出现"学习率不敏感/过于敏感"的异常区间 —— 这本身就是很好的报告素材（no-go 不擦除）。
- ⚠ 本课题#strong[不花 GPU]；如发现 CPU 太慢，优先"缩小语料/减步数"，不要上 Kaggle（配额留给课题04）。

#pagebreak()

= 课题04 开题简报 · 0.1B 端到端预训练（#strong[首次上机]）

#block(width: 100%, above: 9pt, below: 9pt, inset: (left: 12pt, right: 8pt, y: 6pt), stroke: (left: 3pt + luma(180)), fill: luma(252))[
#text(size: 9.8pt)[
模块：#strong[M4/M5] ｜ 周次：#strong[W5–W6（10-12→10-25）] ｜ 算力：#strong[T2 Kaggle 2×T4，计划 12–21 GPU·小时] 唐杰作业对应：#strong[① 端到端训一个 0.1B] ｜ 判分来源：#strong[自建]（loss/bpb 达标 + 采样可读性）+ #raw("nanochat/core_eval.py") 的 CORE 手写：复用课题01/02 的产物（tokenizer + 模型 + 优化器），本课题新增#strong[数据管线与训练编排的判断]
]
]

#v(4pt)
#line(length: 100%, stroke: 0.6pt + luma(200))
#v(4pt)

== 一、研究背景

"0.1B" 是唐杰作业里的数字，也是#strong[单卡/双卡免费算力下的上限]。参考点：nanochat 的 d12 约等于 GPT-1 量级 （官方讨论区原话："d12 是我最喜欢的模型，它是 GPT-1 的大小，约 6 分钟训完"——那是在 8×H100 上）。 #strong[本课题的核心不是刷指标，而是把"训练一次完整模型"的每个环节亲自走通并记账。]

== 二、研究问题（一句话）

#block(width: 100%, above: 9pt, below: 9pt, inset: (left: 12pt, right: 8pt, y: 6pt), stroke: (left: 3pt + luma(180)), fill: luma(252))[
#text(size: 9.8pt)[
#strong[在 2×T4、20 GPU·小时的预算内，我能不能从零训出一个"能生成连贯英文、并在 CORE 上有非零分"的 0.1B 模型？实测成本与估算差多少？]
]
]

== 三、攻关线索

+ #strong[数据]：TinyStories（全量）+ owt-sample 采样。#strong[先算一遍]：词表大小 × 语料字节 → token 数 → 需要的步数
+ #strong[规模选择]：nanochat 用单一旋钮 #raw("--depth")；在 T4 上 16GB 显存能放多深？（用 M0 的显存公式先估）
+ #strong[精度]：#strong[T4 是 SM75，没有 bf16] → 必须 fp16 + GradScaler（或用 nanochat 的 #raw("NANOCHAT_DTYPE=float16")）
+ #strong[断点续训]：Kaggle 会话 9–12h 会断 → checkpoint 必须写 #raw("/kaggle/working")（20GB 持久）
+ #strong[超时自停]：脚本内置 wall-clock 上限，防止忘记关会话
+ #strong[指标]：训练看 bpb（词表无关），最终跑 CORE（22 数据集合成，#raw("core_eval.py") 单文件）

== 四、里程碑

- □ M1 #strong[实验卡获批]：写清假设/命令/预算上限/停止条件/成功判据（见《算力与成本预算.md》§五）
- □ M2 #strong[会话预检]：#raw("nvidia-smi") 确认 2×T4（#strong[若是 P100 立即重开会话]）
- □ M3 #strong[冒烟]：#raw("--depth=4")、100 步，确认能跑、能存、能续训（≤10 分钟）
- □ M4 首次正式训练：双 T4 + DDP，跑到预算上限或 loss 平台
- □ M5 续训一次（验证 checkpoint 真的可用 —— 这一条最容易翻车）
- □ M6 评测：bpb + CORE + #strong[采样 20 条样本]（人工判断"是否连贯"）
- □ M7 #strong[成本账单]：实测耗时 vs 估算（M0 的 6ND + T4 折算），逐项解释偏差
- □ M8 一页报告 + 知识卡（含"我最意外的三个现象"）

== 五、交付物

#block(width: 100%, above: 8pt, below: 10pt)[
#text(size: 9pt)[
  #table(
    columns: (0.280fr, 0.292fr, 0.428fr),
    inset: (x: 7pt, y: 5pt),
    align: left + top,
    stroke: (x, y) => (bottom: if y == 0 { 0.9pt + luma(105) } else { 0.25pt + luma(220) }),
    table.header([交付物], [位置], [验收]),
    [实验卡], [#raw("证据/实验卡-NN.md")], [经用户确认],
    [run.yaml + 日志], [#raw("证据/")], [含 commit、配置、随机种子、耗时],
    [曲线], [#raw("证据/")], [loss/bpb vs FLOPs 与 vs 时间 两张],
    [采样样本], [#raw("证据/样本.md")], [≥20 条，标注"通顺/不通顺"],
    [#strong[成本账单]], [#raw("报告.md")], [实测 vs 估算偏差 ≤ 2× 或给出解释],
    [checkpoint], [Kaggle 持久盘], [不进程（体积原因）；只在 #raw("证据/") 留哈希与路径],
  )
]
]

== 六、讲课锚点

- #strong[讲义]：#raw("M4-训练.md")（W3 展开）
- #strong[对标]：#raw("nanochat/README.md") 与 #raw("runs/speedrun.sh")（读它怎么组织全流程）· CS336 lecture 05/13–14
- #strong[搭桥]：课题03 的 scaling 结论在这里第一次被"真跑"检验

== 七、代码级提问示例

+ 双 T4 跑 d12，为何#strong[不是] 2 倍加速？先预测扩展效率（50%？80%？），再测。
+ T4 上 fp16 与 fp32，谁更快？谁更稳？GradScaler 在解决什么？
+ 你的 loss 在第 2000 步开始上升。按 M0 §五 的顺序，你的前三个动作是什么？
+ 若把语料从 TinyStories 换成中文语料（词表不变），loss 会怎么变？#strong[bpb 呢？]

== 八、风险与提醒

- ❗ #strong[P100 陷阱]：本课题如果拿到 P100，训练慢 3–5 倍且后续课题05 直接不可用 → #strong[宁可等 T4 时段]。
- ❗ #strong[配额]：本课题占全学期约 1/5 的配额，实验卡必须写实；#strong[冒烟不通过不许开正式训练]。
- ⚠ 0.1B 在 T4 上大概率需要"降 batch + 梯度累积"，这会改变有效 batch size → #strong[要写进 run.yaml]。
- ⚠ Kaggle 会话到期会杀进程：#strong[每 500 步存一次]是硬要求。

#pagebreak()

= 课题05 开题简报 · 手写 Triton attention kernel

#block(width: 100%, above: 9pt, below: 9pt, inset: (left: 12pt, right: 8pt, y: 6pt), stroke: (left: 3pt + luma(180)), fill: luma(252))[
#text(size: 9.8pt)[
模块：#strong[M5] ｜ 周次：#strong[W7–W8（10-26→11-08）] ｜ 算力：#strong[T1 Kaggle 1×T4，计划 10 GPU·小时] 唐杰作业对应：#strong[② 手写 Triton attention kernel，测多卡训练与推理增益] ｜ 判分来源：#strong[CS336 A2]（正确性对齐）+ 自建性能对照 手写：#strong[R5（kernel 本体：分块 + online softmax）]
]
]

#v(4pt)
#line(length: 100%, stroke: 0.6pt + luma(200))
#v(4pt)

== 一、研究背景

朴素注意力要把 $L× L$ 的注意力矩阵#strong[整个写进显存]：$L=8 1 9 2$ 时单头就是 64M 个元素。 FlashAttention（2022）的核心洞察：#strong[根本不需要把矩阵写出来] —— 分块计算、在线维护 softmax 的 最大值与归一化因子，就能得到数学上完全等价的结果。它把注意力的显存从 $O(L^2)$ 降到 $O(L)$。

Triton 让这件事对非 CUDA 专家也可做：用 Python 风格的 DSL 写"块级"程序。 #strong[本课题的目标不是写出最快的 kernel，而是亲手经历"数值等价 + 显存下降 + 速度提升"这三件事的因果链。]

== 二、研究问题（一句话）

#block(width: 100%, above: 9pt, below: 9pt, inset: (left: 12pt, right: 8pt, y: 6pt), stroke: (left: 3pt + luma(180)), fill: luma(252))[
#text(size: 9.8pt)[
#strong[一个分块 + online softmax 的手写 kernel，能否在数值上等价于朴素实现，并把显存从 O(L²) 降到 O(L)、速度提升若干倍？提升来自哪里（算术减少？访存减少？）]
]
]

== 三、攻关线索

+ #strong[先量化瓶颈]：朴素实现在 L=2k/8k 时的显存、耗时（用 profiler 看是 compute-bound 还是 memory-bound）
+ #strong[online softmax 的递推]：维护 running max $m$ 与 running sum $ℓ$， 新块的贡献要按 $e^(m_("old")-m_("new"))$ 缩放 —— #strong[这正是 M0 §四 logsumexp 的应用]
+ #strong[分块维度]：按 query 分块、沿 key 方向扫描 → 每个块只需常驻 SRAM
+ #strong[数值容差]：与 PyTorch SDPA 对照，相对误差应在 1e-2\~1e-3（fp16）；#strong[先写容差，再判定]
+ #strong[多卡/推理增益]：训练侧测吞吐（tokens/s），推理侧测 decode 显存与延迟 —— 这是唐杰作业②要求的"增益"

== 四、里程碑

- □ M1 基线：朴素注意力的显存与耗时（L=2k/4k/8k 三点）
- □ M2 #strong[正确性]：手写 kernel 与 SDPA 的数值对照（max abs error 记录在案）
- □ M3 #strong[显存]：证明峰值显存随 L 近似线性（对比朴素实现的 O(L²)）
- □ M4 #strong[速度]：给出 speedup 曲线（含 L 与 block size 两个维度）
- □ M5 #strong[profiling]：用 profiler 说明"提升来自哪里"（访存 vs 算术，给出数字）
- □ M6 #strong[增益测量]：训练吞吐（tokens/s）与推理（融合进 attention 后）的实测对比
- □ M7 一页报告 + 知识卡（online softmax 递推必须能徒手推）

== 五、交付物

#block(width: 100%, above: 8pt, below: 10pt)[
#text(size: 9pt)[
  #table(
    columns: (0.197fr, 0.246fr, 0.558fr),
    inset: (x: 7pt, y: 5pt),
    align: left + top,
    stroke: (x, y) => (bottom: if y == 0 { 0.9pt + luma(105) } else { 0.25pt + luma(220) }),
    table.header([交付物], [位置], [验收]),
    [kernel], [#raw("手写/")（你写）], [M2 数值对照通过],
    [三张图], [#raw("证据/")], [speedup / 显存 / profile（#strong[坐标轴与硬件口径必须标注]）],
    [数值误差记录], [#raw("证据/")], [含容差设定与依据],
    [报告], [#raw("报告.md")], [必须回答"提升来自哪里"],
  )
]
]

== 六、讲课锚点

- #strong[讲义]：#raw("讲义/M5-推理.md")（W5 展开）中"GPU 内存层级与 Triton 编程模型"一节
- #strong[对标]：CS336 lecture 05–06（GPUs / Kernels & Triton）+ A2 handout（#strong[flash-attn 需两步安装]： #raw("uv sync --no-install-package flash-attn") 再 #raw("uv sync")）· Triton 官方 FlashAttention 教程
- #strong[搭桥]：M0 §四 的 logsumexp —— 你会亲手把它写进 kernel

== 七、代码级提问示例

+ online softmax 里，为什么新块要乘 $e^(m_("old")-m_("new"))$？不乘会怎样？
+ block size 从 64 增到 256：显存、速度、数值误差各往哪走？
+ 为什么 L 很大时，朴素实现容易 OOM 而 kernel 不会？（用 $O(L^2)$ vs $O(L)$ 说清）
+ #strong[【下注】] 你预测 speedup 在 L=2k 时是多少倍？先写，再测。

== 八、风险与提醒

- ❗ #strong[P100 不可用于本课题]：Triton 要求计算能力 ≥7.0，P100 是 6.0 → #strong[开跑前必须验明是 T4]。
- ⚠ 正确性优先于速度：#strong[数值对照不过，速度数字一律不算数]。
- ⚠ 硬件口径陷阱：任何 speedup 数字必须写明"对比对象（PyTorch SDPA / 朴素实现）"与"硬件（T4）"， 否则曲线毫无意义（这一条写进报告硬要求）。
- ⚠ 若 T4 上 kernel 因共享内存不够而失败，#strong[先降 block size，不要放弃]（这本身就是教学素材）。

#pagebreak()

= 课题06 开题简报 · 多卡与分布式训练

#block(width: 100%, above: 9pt, below: 9pt, inset: (left: 12pt, right: 8pt, y: 6pt), stroke: (left: 3pt + luma(180)), fill: luma(252))[
#text(size: 9.8pt)[
模块：#strong[M4] ｜ 周次：#strong[W9（11-09→11-15）] ｜ 算力：#strong[T2 Kaggle 2×T4，计划 8 GPU·小时] 唐杰作业对应：#strong[② 的"多卡训练增益"部分] ｜ 判分来源：#strong[CS336 A2 分布式部分 + 自建 benchmark] 手写：#strong[R3 的延伸（并行策略选择与通信原语判断）]
]
]

== 一、研究背景

数据并行（DDP）把同一模型复制到每张卡、各自算一个微批、再#strong[同步梯度]； 当模型放不下单卡时，才有 FSDP/ZeRO（切分参数、梯度、优化器状态）、张量并行（切层内矩阵）、流水线并行（切层）。 #strong[Kaggle 免费档给的是 2×T4，且走 PCIe 而非 NVLink] —— 这恰好是"观察通信成为瓶颈"的最佳实验台。

== 二、研究问题

#block(width: 100%, above: 9pt, below: 9pt, inset: (left: 12pt, right: 8pt, y: 6pt), stroke: (left: 3pt + luma(180)), fill: luma(252))[
#text(size: 9.8pt)[
#strong[在弱互联（PCIe）的 2×T4 上，DDP 的扩展效率是多少？瓶颈是计算还是通信？FSDP 在什么规模才开始划算？]
]
]

== 三、攻关线索

+ #strong[先对齐正确性]：DDP 后的梯度应与单卡（同等效批大小）#strong[数值一致]，先验证再谈性能
+ #strong[批大小语义]：2 卡 × 每卡 batch = 等效批大小；若显存受限要#strong[同步调整学习率]（线性/平方根缩放）
+ #strong[计时口径]：#raw("step time") 要区分"纯计算时间"与"含 all-reduce 的时间"；用 #raw("torch.profiler") 或手写计时
+ #strong[扩展效率]：$E = frac(T_1, 2 thin T_2)$。#strong[先预测]（PCIe 下 0.6–0.8？）再测
+ #strong[通信占比]：梯度同步量与参数量成正比（$2 N$ 字节/步，all-reduce 近似）；序列长/批小时通信占比更高
+ #strong[FSDP 的代价]：切分带来额外通信（all-gather + reduce-scatter），#strong[小模型上往往更慢]

== 四、里程碑

- □ M1 DDP 梯度一致性验证（与单卡同等效批）→ 记录最大误差
- □ M2 单卡 vs 双卡 的 #raw("step time")、#raw("tokens/s") 对照（同模型、同等效批）
- □ M3 #strong[扩展效率曲线]（至少 3 个配置点：不同 batch/序列长度）
- □ M4 #strong[通信占比分解]：计算 / all-reduce / 数据加载 三段计时
- □ M5 一次 FSDP 实验并解释"为什么（不）划算"
- □ M6 #strong[先写预测再实测]：预测扩展效率，跑完对照（进 #raw("memory/MEMORY.md") 打脸日志）
- □ M7 一页报告

== 五、交付物

#block(width: 100%, above: 8pt, below: 10pt)[
#text(size: 9pt)[
  #table(
    columns: (0.199fr, 0.416fr, 0.385fr),
    inset: (x: 7pt, y: 5pt),
    align: left + top,
    stroke: (x, y) => (bottom: if y == 0 { 0.9pt + luma(105) } else { 0.25pt + luma(220) }),
    table.header([交付物], [位置], [验收]),
    [分布式脚本], [#raw("手写/") 或 #raw("脚手架/")（按 B3 分类）], [可复跑],
    [计时原始数据], [#raw("证据/bench.csv")], [含每配置 3 次重复],
    [扩展效率曲线], [#raw("证据/")], [标注硬件（2×T4 PCIe）与对比基准],
    [报告], [#raw("报告.md")], [解释"为什么不是 2 倍"],
  )
]
]

== 六、讲课锚点

- #strong[讲义]：#raw("M4-训练.md")（W3 展开）中并行一节
- #strong[对标]：CS336 lecture 07–08（Parallelism）· #raw("nanochat/optim.py")（分布式优化器实现）· HF Ultra-Scale Playbook（用前先核）
- #strong[搭桥]：M0 的"梯度累加"→ DDP 就是#strong[跨卡的梯度累加]

== 七、代码级提问示例

+ 2×T4 上 DDP 只快了 1.4 倍，列出三个最可能的原因。
+ 把每卡 batch 减半、用梯度累积补回等效批，通信量会怎么变？
+ 什么情况下 FSDP 会#strong[比 DDP 慢]？（用通信量解释）
+ all-reduce 的通信量是多少字节/步？用参数量 $N$ 表示。

== 八、风险与提醒

- ⚠ Kaggle 双 T4 会话#strong[不稳定]（可能只给一张）：预检时确认 #raw("torch.cuda.device_count()==2")。
- ⚠ 不要在本课题纠缠"调到最快"——#strong[目标是理解扩展效率的成因]，配额要留给课题08。

#pagebreak()

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

#pagebreak()

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

#pagebreak()

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

#pagebreak()

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

#pagebreak()

= 课题11 开题简报 · 结项（NeurIPS 报告 + 现场 demo）

#block(width: 100%, above: 9pt, below: 9pt, inset: (left: 12pt, right: 8pt, y: 6pt), stroke: (left: 3pt + luma(180)), fill: luma(252))[
#text(size: 9.8pt)[
模块：#strong[M9] ｜ 周次：#strong[W15–W16（12-21→2027-01-03）] ｜ 算力：#strong[弹性 ≤4 GPU·小时] 唐杰作业对应：#strong[⑥ 英文 NeurIPS 格式 + W16 现场 demo]、#strong[⑦ 作业 40% / 大项目 60%] ｜ 判分来源：#strong[报告协议 + 导师审稿 + 自我攻击]
]
]

== 一、研究背景

唐杰的原话是"#strong[问题、动机、方法、结果，一项都不能糊]"。 这恰好也是本学科九份章程反复强调的：#strong[没有证据的结论不采纳、no-go 不擦除、误差棒必填]。 结项不是"写一篇总结"，而是#strong[把 11 个课题的证据链组装成一份可被审稿的作品]。

== 二、研究问题（结项版）

#block(width: 100%, above: 9pt, below: 9pt, inset: (left: 12pt, right: 8pt, y: 6pt), stroke: (left: 3pt + luma(180)), fill: luma(252))[
#text(size: 9.8pt)[
#strong[我能不能用一份英文技术报告 + 一个可运行的 demo，证明我独立完成了大模型全链路，并且知道自己的结论在哪里不成立？]
]
]

== 三、攻关线索

+ #strong[报告骨架]（NeurIPS 风格，8–10 页）：Abstract / Introduction / Related Work / Method / Experiments / Results / Discussion & Limitations / Conclusion
+ #strong[只写有证据的结论]：每个数字都能指回 #raw("证据/") 中的原始日志
+ #strong[Limitations 必须诚实]：规模受限（0.1B vs 前沿）、算力受限（免费档）、评测口径的局限
+ #strong[Demo 设计]：现场演示要#strong[可在 3 分钟内跑完]（预生成 checkpoint，不现场训练）
+ #strong[自我攻击 3 条]：主动写出"我的结论最可能错在哪"
+ #strong[一稿多用]：这份报告同时作为课程大论文（70%）与唐杰作业⑦的交付物

== 四、里程碑

- □ M1 证据清点：11 个课题的 #raw("证据/") 全部齐备，缺的补齐（这是一次"审计"）
- □ M2 英文报告初稿（Abstract + Method + Experiments 先写）
- □ M3 图表规范化：所有图有坐标轴、单位、误差棒、样本数
- □ M4 #strong[自我攻击 3 条] + 导师审稿 3–5 条 → 修订
- □ M5 Demo 准备：脚本 + 预生成模型 + 3 分钟演练
- □ M6 总复盘：写进 #raw("memory/LEARNINGS.md")（哪些讲法有效、哪些坑最贵）
- □ M7 课程大论文定稿并提交（署名直填：孙承泽 / 2253710052 / 能动强基2501）

== 五、交付物

#block(width: 100%, above: 8pt, below: 10pt)[
#text(size: 9pt)[
  #table(
    columns: (0.187fr, 0.554fr, 0.259fr),
    inset: (x: 7pt, y: 5pt),
    align: left + top,
    stroke: (x, y) => (bottom: if y == 0 { 0.9pt + luma(105) } else { 0.25pt + luma(220) }),
    table.header([交付物], [位置], [验收]),
    [英文报告], [#raw("课题11-结项/report-en.md")（+ PDF）], [格式合规、结论有据],
    [中文大论文], [#raw("课程轨/大论文/")], [课程要求格式],
    [Demo], [#raw("课题11-结项/脚手架/demo.sh")], [3 分钟内可跑],
    [复盘], [#raw("memory/LEARNINGS.md") + #raw("HANDOFF.md")], [可被下一任直接接续],
  )
]
]

== 六、讲课锚点

- #strong[讲义]：#raw("M9-前沿.md")（W15 展开）
- #strong[对标]：#strong[rasbt ch3 的"先建评测"精神]贯穿全文 · CS336 报告规范 · #raw("论文精读/") 的英文写作规范
- #strong[搭桥]：#raw("turbine-blade-ai-platform")（应用章节）；#raw("人工智能基础与应用/课程轨/大论文")（一稿两用）

== 七、自检清单（结项前必过，抄自《判分与验收标准》§五）

+ 每个数字都能在 #raw("证据/") 找到原始日志吗？
+ "变好了"有没有可能是口径变了 / 只挑了好种子？
+ 有没有把#strong[训练集表现]当能力？
+ 每个"因为…所以…"有没有反事实检验？
+ 图表的坐标轴与误差棒都标了吗？
+ 我写下的最强反方论点是什么？

== 八、风险与提醒

- ⚠ 报告最易犯的错是#strong[夸大]：规模受限就要说受限，这反而是可信度来源。
- ⚠ 不要为了"好看"删掉 no-go 记录——用户明确要求"负结果不许擦除"。
- ⚠ W16 现场 demo 必须有#strong[失败预案]（预生成结果 + 录屏），不依赖现场网络与算力。
