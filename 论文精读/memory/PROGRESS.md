# PROGRESS · 论文精读台账

> **总规划：12 篇论文 / 51 次会话**，见 `../12篇论文总规划.md`。
> 当前：P01《Machine Learning in Aerodynamic Shape Optimization》（Li, Du, Martins）· 103 页 · 47 图
> P01 详细计划见 `../论文01-ML气动外形优化/精读路线图.md`

## 12 篇论文总台账

| # | 论文 | 被引 | 会话数 | 状态 |
|---|---|---|---|---|
| P01 | Li/Du/Martins, ML in ASO, Prog. Aerosp. Sci. 134 (2022) 100849 | — | 12 | 🔄 会话01 进行中 |
| P02 | Kenway et al., Effective adjoint approaches for CFD, Prog. Aerosp. Sci. 110 (2019) 100542 | ×5 | 4 | ⬜ |
| P03 | Lyu et al., ASO of the CRM wing benchmark, AIAA J. 53 (2015) 968–985 | ×9 | 3 | ⬜ |
| P04 | Queipo et al., Surrogate-based analysis and optimization, Prog. Aerosp. Sci. 41 (2005) 1–28 | ×4 | 3 | ⬜ |
| P05 | Li/Bouhlel/Martins, Data-based fast airfoil analysis and optimization, AIAA J. 57 (2019) 581–596 | ×19 | 4 | ⬜ |
| P06 | Du/He/Martins, NN-based parameterization and surrogate modeling, AST 113 (2021) 106701 | ×11 | 4 | ⬜ |
| P07 | Bouhlel/He/Martins, Scalable gradient-enhanced ANN (subsonic+transonic), SMO 61 (2020) 1363–1376 | ×6 | 3 | ⬜ |
| P08 | Li/Zhang, Deep-learning-based geometric filtering in ASO, AST 112 (2021) 106603 | ×8 | 3 | ⬜ |
| P09 | Li/Zhang, Adjoint-free ASO of the CRM wing, AIAA J. 59 (2021) 1990–2000 | ×10 | 4 | ⬜ |
| P10 | Li/Zhang/Chen, Supercritical airfoils via deep RL, AIAA J. 59 (2021) 3988–4001 | ×5 | 3 | ⬜ |
| P11 | Thuerey et al., DL for RANS simulations of airfoil flows, AIAA J. 58 (2020) 25–36 | ×6 | 4 | ⬜ |
| P12 | Cai/Mao/Wang/Yin/Karniadakis, PINNs for fluid mechanics: a review, Acta Mech. Sin. 37 (2021) 1727–1738 | §3.5.8 | 4 | ⬜ |
| 补 | FNO / DeepONet（本综述 0 命中，题录待核） | — | 待定 | ⬜ |

**总进度：0 / 51 会话**

## 会话台账

| 会话 | 内容 | PDF页 | 状态 | 完成日期 | 备注 |
|---|---|---|---|---|---|
| 01 | 全景扫描（Abstract + §1） | 1–3 | 🔄 进行中 | - | 2026-08-31 开题；第 1 轮已按用户真实画像**重发**（先认词2+预测6+规划3），**待答** |
| 02 | 传统 ASO 与六个挑战（§2） | 4–7 | ⬜ | - | 含 Fig.1 XDSM 读图 |
| 03 | 传统代理模型（§3.1） | 7–16 | ⬜ | - | Kriging 家族，Fig.2–16 |
| 04 | 无监督学习与降维（§3.2） | 17–25 | ⬜ | - | 连概率论协方差/数理方程特征值 |
| 05 | 半监督 + 强化学习（§3.3–3.4） | 26–32 | ⬜ | - | |
| 06 | 神经网络全家桶（§3.5） | 32–40 | ⬜ | - | 含 PINN（§3.5.8） |
| 07 | 几何设计空间（§4.1） | 41–46 | ⬜ | - | Fig.42–44 |
| 08 | 气动评估（§4.2）⭐⭐ | 47–57 | ⬜ | - | 全篇最重要 |
| 09 | 优化架构（§4.3） | 58–67 | ⬜ | - | Fig.46–47 |
| 10 | 结论与展望（§5） | 68 | ⬜ | - | |
| 11 | 批判性阅读 | 1–103 | ⬜ | - | 含参考文献抽样 |
| 12 | 知识整合 | — | ⬜ | - | 一页四段报告 + 审稿意见 |

**状态**：⬜ 未开始 · 🔄 进行中 · ✅ 已完成 · 🔶 需复习

## 统计

- P01 已完成：0 / 12（0%）
- 全规划已完成：0 / 51（0%）
- 开始日期：2026-08-31
- 预计完成：12 次会话（约 12–14 小时纯阅读 + 答题）

## 里程碑台账（开题简报 §四）

| # | 里程碑 | 状态 | 达成会话 |
|---|---|---|---|
| M1 | 画出 CFD-based ASO 标准工作流（Fig.1）并指出时间瓶颈 | ⬜ | - |
| M2 | 列出 §2.2 六个挑战（≥4）并映射到 §4 小节 | ⬜ | - |
| M3 | 写出 Kriging 预测式结构，解释 f 与 R 的角色 | ⬜ | - |
| M4 | 解释 PCA / AE 降维本质差别与各自丢失什么 | ⬜ | - |
| M5 | 说明系数建模 vs 流场建模取舍并给理由 | ⬜ | - |
| M6 | 解释 PINN 损失函数组成及为何少用数据 | ⬜ | - |
| M7 | 指出综述 ≥3 处局限（带页码） | ⬜ | - |
| M8 | 交付一页四段报告含"存疑"节 | ⬜ | - |

## 复习队列

| 卡片 | 上次 | 建议复习 |
|---|---|---|
| （暂无，等会话01 判卷后建卡） | - | - |

---
*最后更新：2026-08-31*
