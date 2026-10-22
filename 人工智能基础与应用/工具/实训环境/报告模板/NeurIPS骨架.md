# 报告模板 · 英文技术报告骨架（NeurIPS 风格，结项与唐杰作业⑥用）

> 用途：课题11 结项报告 / 课程大论文英文版。建议 8–10 页（含图表）。
> 纪律：**每一节都问自己"这里的每个数字有证据吗"**；Limitations 不许敷衍。

## 元信息

- **Title**：From Scratch to a 0.1B Language Model and a Long-Horizon Agent: A Zero-Budget Full-Stack Reproduction
- **Author**：Sun Chengze (孙承泽) · Student ID 2253710052 · Class 能动强基2501
- **Affiliation**：Xi'an Jiaotong University · School of Energy and Power Engineering
- **Date**：Auto-generated (`环境/报告模板` 支持直接填署名，不留占位符)

---

## 1. Abstract（150–200 词）

四句结构：①做了什么（一句话）②怎么做的（规模 + 算力约束）③主要结果（**带数字**）④局限（一句话诚实声明）。
**禁止出现**："取得了显著效果""达到了先进水平"这类无证据表述。

## 2. Introduction

- 动机：为什么"从零走全链路"仍然值得做（唐杰作业清单的 7 条要求 → 本文的组织方式）
- 约束：零预算（免费 GPU）、0.1B 规模（主动选择而非妥协）
- 贡献：三条（例：①完整可复现流程与证据规范 ②×与 × 的对照实验 ③一套可验证环境与 harness）

## 3. Related Work

按"教材/课程/框架/论文"四类分组，**每条都要说明与本工作的关系**（借用？对照？区别？）：
CS336 · nanochat · minimind · rasbt《Reasoning from Scratch》· RLHF Book · verifiers / terminal-bench

## 4. Method

分四块，每块**对应一个课题**并给证据索引：
1. **Tokenizer & Model**（课题01/02）：BPE 设计选择、Transformer 组件、参数量核算
2. **Training**（课题03/04/06）：数据、优化器、scaling 预测与验证、并行策略
3. **Post-training**（课题08）：SFT / DPO / RLVR 的设置与对照口径
4. **Agent & Env**（课题09/10）：可验证环境设计、harness、self-judge 协议

## 5. Experiments

- 硬件与预算表（设备、GPU·小时、实测耗时）
- 评测口径说明（**同口径对照**；bpb 与 CORE 的定义）
- 每个实验：假设 → 命令（可复现）→ 指标 → 证据文件路径

## 6. Results

- 主表：各课题关键指标（**带误差棒/重复次数**）
- **预测 vs 实测**表（本工作的特色：把"打脸"写进正文，而不是藏起来）
- 图：loss/bpb 曲线、scaling 拟合与外推验证、扩展效率、三方对照、Agent 成功率消融

## 7. Discussion & Limitations（**必写，重点**）

- 规模限制：0.1B 学不到涌现行为与前沿工程（MoE/万卡/多模态）
- 算力限制：免费档的会话中断与配额约束如何影响结论强度
- 口径限制：自建评分器的假阳性率；T4 无 bf16 带来的精度差异
- **最强反方论点**：如果我的结论是错的，最可能是因为什么？

## 8. Conclusion

- 三条结论（与 Abstract 呼应，但不重复措辞）
- 一句"下一步"（具体动作，不写空话）

## References

按 NeurIPS 引用格式；**所有上游仓库都要带 commit hash 与访问日期**（见《上游锁定清单》）。

## Appendix（可选，建议必附其一）

- A. 完整超参与命令（可直接复跑）
- B. **失败与 no-go 记录**（本工作的诚实性证明）
- C. 自建评分器的判定规则与假阳性分析

---

## 排版说明

- 目前用 Markdown 起草（便于版本管理与 diff）；**定稿时可转 LaTeX**：
  模板可参考 `skills/library/latex-posters/SKILL.md` 的 LaTeX 规范，或直接向导师要会议模板。
- 图表规范：坐标轴标注单位、误差棒、样本数；**禁止截断坐标轴夸大差异**。
- 写作时同步填 `课题11-结项/证据/自检清单.md`（抄自《判分与验收标准》§五）。
