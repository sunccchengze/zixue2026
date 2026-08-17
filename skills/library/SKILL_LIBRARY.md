# 技能库索引 SKILL_LIBRARY

> 来源：用户 `-SKILL-` 仓库 `arena/01a0095c-skill` 分支（GitHub 开源技能 + 用户蒸馏产物）。
> 已精选与"科研式学习"最相关的 12 个技能放入本仓库 `skills/library/`。
> **所有学科 Agent 开局必读本索引**，按需调用对应技能。
> 完整上游（2千+技能）仍在原仓库，需要更多时用
> `gh api "repos/sunccchengze/-SKILL-/contents/skills/community/...?ref=arena/01a0095c-skill"` 检索。

## 调用方式总则

每个技能的使用方法 = **打开对应 SKILL.md 文件，照它说的做**。分两类：

- **方法类**（纯方法论，无依赖）：读 SKILL.md → 按其中流程/模板执行。所有学科通用。
- **工具类**（需安装运行时）：先读 SKILL.md 确认依赖 → 按需安装 → 再执行。安装前征得用户同意。

## 方法类技能（随时可用）

| 技能 | 路径 | 用途 | 何时调用 |
|---|---|---|---|
| 科研式学习导师（本仓库自产总纲） | `skills/科研式学习导师/SKILL.md` | 课题制教学全流程（批量提问/打脸链路/记忆系统/大师团/报告协议） | **所有学科主引擎，永远优先** |
| DeepTutor（教学法） | `skills/library/DeepTutor/SKILL.md` | 交互式学习平台的教学设计（deep_solve/deep_question/visualize 等能力的设计思路） | 设计"深解/出题/可视化"类教学环节时借鉴其能力划分 |
| DeepTutor 内置文档技能 | `skills/library/DeepTutor/builtin-pdf.md` `builtin-docx.md` `builtin-pptx.md` | PDF/docx/pptx 的**读取、批注、编辑方法论** | 处理学科资料（讲义/真题/课件）时 |
| PDF 处理 | `skills/library/pdf-handling/SKILL.md` | 通用 PDF 读写合并方法论 | 同上，资料预处理 |
| 文档转 Markdown | `skills/library/doc-to-markdown/SKILL.md` | 任意文档 → Markdown 的转换流程 | 把 PPT/PDF 转成可检索笔记时 |
| nuwa 女娲造人（人物蒸馏） | `skills/library/nuwa-skill/SKILL.md` | 蒸馏真实人物思维框架（快速档：公开资料→心智模型→诚实声明） | 各学科建"大师天团"时（每学科开局第七步） |
| manim 数学动画 | `skills/library/manim-video/SKILL.md` | 数学概念动画（manim 视频）方法论 | 需要动态可视化抽象概念时（如中心极限定理、波动传播） |
| mermaid 图表 | `skills/library/mermaid-diagrams/SKILL.md` | Mermaid 流程图/时序图/状态图规范 | 画流程、路线图、状态机（如"解题决策工作流"） |
| LaTeX 公式/海报 | `skills/library/latex-posters/SKILL.md` | LaTeX 规范（含海报排版） | 写报告公式排版、生成公式图时参考 |

## 工具类技能（需运行时，可选安装）

| 技能 | 路径 | 依赖 | 何时调用 |
|---|---|---|---|
| DeepTutor CLI | `skills/library/DeepTutor/SKILL.md`（下半部分） | `pip install deeptutor-cli`（Python 3.11+），可另配 LLM | 用户明确想要"独立学习平台"（聊天/深解/出题/知识库）时，**先问用户是否安装** |

> 备注：DeepTutor 是一个完整的交互式学习平台（CLI/Web），能力包括 deep_solve、deep_question、
> deep_research、visualize、math_animator、mastery_path 等。**本项目默认用自产总纲教学，
> DeepTutor 作为教学法参考与可选的进阶工具**，不替代导师 Agent 本身。

## 已内置于总纲、无需单独调用的上游技能（历史记录）

- drill-me（间隔重复+提取练习）→ 已内化进 `科研式学习导师` §2/§3
- memory-system（六引擎记忆架构）→ 已内化进 §3
- growth-log（成长日志三原则）→ 已内化进 §3
- rules-distill（跨技能铁律蒸馏）→ 已内化进 §6
- self-improving-agent（学习记录自演化）→ 已落地为 LEARNINGS/ERRORS 双文件

## 使用纪律

1. 读 SKILL.md 时**渐进加载**：先 SKILL.md，再它引用的 reference；只跑当前任务需要的部分；
2. 工具类技能安装/联网前先征得用户同意；
3. 两个技能冲突时，服从用户指令与本项目总纲（`科研式学习导师`）；
4. 用完不写回技能库——技能库只读；所有学习产物写进对应学科文件夹。
