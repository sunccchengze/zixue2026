---
name: memory-system
description: 参照小龙虾 6 大核心记忆架构（self-improving-agent, three-layer-memory, memory-entropy, memory-evaluator, precedent-memory, learning-system-skill）为孙承泽大创项目量身定制的永久跨会话记忆与无缝接力系统。确保新 Session 的 Agent 能 100% 继承历史教训、用户偏好、物理金标准与未完成战役。
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
metadata:
  memory_root: .learnings/
  structure:
    - .learnings/LEARNINGS.md (用户偏好与物理金标准)
    - .learnings/ERRORS.md (判例式负向记忆与红线禁区)
    - .learnings/FEATURE_REQUESTS.md (四大战役待办任务表)
    - HANDOFF.md (交接总账本)
    - 14_DAYS_MASTER_PLAN.md (14天作战大纲)
---

# 6 阶全栈智能体记忆系统 (Memory System for Wind Farm Viz)

> **核心目标**：实现跨 Session、跨 Agent 实例的**“零损耗无缝接力”**。
> 新 Session 启动时，第一步读取 `.learnings/` 与 `HANDOFF.md`，瞬间唤醒全部上下文记忆与行为红线。

---

## 一、 6 大记忆引擎矩阵

1. **`self-improving-agent` (自演化更新引擎)**：
   - 每次交互产生的认知突破自动写入 `.learnings/LEARNINGS.md`；
2. **`three-layer-memory` (三层记忆架构)**：
   - **L1 工作记忆 (Working Memory)**：当前 Session 正在处理的临时变量与代码调试；
   - **L2 情景判例记忆 (Episodic Precedent Memory)**：用户批评与踩坑教训（`.learnings/ERRORS.md`）；
   - **L3 语义长期记忆 (Semantic Long-term Memory)**：物理机理公式、实验金数据与代码契约（`HANDOFF.md`）；
3. **`memory-entropy` (记忆熵评估与降噪)**：
   - 剔除无用的中间报错与过时调试日志，保持 `.learnings/` 极其精炼、高数据密度；
4. **`memory-evaluator` (记忆评估器)**：
   - 每次输出前对照 `.learnings/ERRORS.md` 进行拦截自查；
5. **`precedent-memory` (判例法红线库)**：
   - 将用户过去的所有严厉批评转化为绝对不可再犯的铁律；
6. **`learning-system-skill` (学习系统总控)**：
   - 调度全部记忆读写，确保跨 Session 风格 100% 保持一致。

---

## 二、 新 Session 接入协议（Next Agent Handover Protocol）

后继 Session 的 Agent 必须在开局执行以下动作：
1. **自动读取记忆核心**：首先阅读 `.learnings/LEARNINGS.md`、`.learnings/ERRORS.md` 与 `HANDOFF.md`；
2. **开篇声明规程**：首行必须声明调度的大师与调用的 SKILL；
3. **严格遵从四大禁区**：
   - 绝不改动 `site/` 莫兰迪浅色与视频背景基线；
   - 绝不在 PPT 中使用 Emoji 或悬浮圆角白卡片；
   - 绝不使用 `present_file` 弹出查看器打扰用户；
   - 坚持用第一性原理与差评式大白话深入浅出讲解。
