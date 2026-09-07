<!-- v2 -->
> **10 分钟读法**：时间紧就只读 **6.2 六个软肋** 与 **6.3 六个选题**；
> 要横向对比全书再读 6.1 矩阵表；6.4 是本书的公示制度（错过的数字都挂在那儿），6.5 是全书收口。

![全书概念地图：流程与瓶颈 → 工具箱 → 战场 → 架构 → 三笔账](./images/back_concept_map_zh.png)

## 6.1 全景对比矩阵（把 12 讲压成一张表）

> **怎么读**：先竖读「代价 / 失效条件」那一列，再横读你关心的那一讲。
> 先竖读代价，是因为收益可以吹，代价很难藏。

> 这张表是**替论文 §5 补的那张总表**（讲 10 §5）。三列硬指标里，"代价"一列论文全文没给，
> 我们给的也不是估计值，而是**口径 + 出处**：凡标〔原文 P##〕的可回溯，凡标「本白皮书复算」的可由 `code/` 跑出。

| 讲 | 解决什么 | 核心操作（一句话） | 关键数字（含口径） | 代价 / 失效条件 |
| :---: | :--- | :--- | :--- | :--- |
| 01 流程与瓶颈 | 看清 ASO 的模块与最贵环节 | 画 XDSM：对角线模块、非对角线数据 | 二维翼型几十个、三维机翼几百个设计变量〔原文 P5〕〔原文 P5 "tens of design variables are required"〕 | CFD 每次数小时；畸形外形直接不收敛〔原文 P6〕〔原文 P6 "abnormal shapes, such as wavy airfoil surfaces"〕 |
| 02 Kriging 家族 | 少花 CFD 拿到可信预测 | 趋势 + 相关表 → μ、σ；θ 用极大似然 | 10^5 训练点以上不适合〔原文 P50〕〔原文 P50 "not suitable for handling a large volume of train-"〕；最高 100 维（PLS 方向法）〔原文 P48〕〔原文 P48 "partial least squares method"〕 | 高维下 R → I，退化成"只有趋势"（本白皮书复算：`code/curse.py`） |
| 03 降维 | 把 d 变小 | 中心化 → 协方差 → 特征分解；按累计方差选 k | 叶片几何 100 → 15〔原文 P44〕〔原文 P44 "from 100 to 15"〕；Rotor 37：1,734 样本、8 模态、+0.25% 效率〔原文 P45〕〔原文 P45 "extract eight PCA modes of the NASA Rotor 37 blade from 1,734 samples"〕 | 线性模态抓不住弯曲流形；无真实库 → 模态本身畸形〔原文 P45〕 |
| 04 半监督 / RL | 标签不够或没有标签 | 伪标签回填 / (s,a,r) 三件套 | 无气动专用数字（综述仅给通用原理） | 伪标签自我强化；RL 训练成本高〔原文 P59〕〔原文 P59 "concerns of rl-based aso include the high training cost"〕 |
| 05 神经网络全家桶 | 从拟合数到场 | 前向 + 反传；式 (64) 平方损失 | 未见翼型上场预测平均相对误差 < 3%（U-Net）〔原文 P54〕〔原文 P54 "less than 3% in tests on unseen airfoils"〕 | 梯度消失（sigmoid 0.25^9 ≈ 4×10⁻⁶）；PINN 换边界要重训〔原文 P41〕〔原文 P41 "the original PINN was set up under a fixed set of initial and boundary conditions"〕 |
| 06 几何设计空间 | 让采样"只落在合法流形上" | 模态参数化 + 合法性约束 S_valid ≥ s_min | 下界约 0.7 不误伤创新外形〔原文 P47〕〔原文 P47 "a lower bound of ∼0.7"〕 | 阈值不可跨对象照搬（本白皮书判断） |
| 07 气动评估 | 决定替代哪一步 | 系数建模 vs 流场建模选型决策树 | 135,108 样本、60 变量、C_L/C_D/C_M 平均相对误差 ≤ 0.4%（47,967 未见机翼）〔原文 P62〕〔原文 P62 "135,108"〕 | 插值型模型 + 高维 ⇒ 外推失准〔原文 P47〕〔原文 P47 "may not ensure accuracy in extrapolations"〕 |
| 08 加速与约束 | 让"验证"这一步也变便宜 | CNN 给初场 / 数据驱动离散 / 分离传感器替代经验式 | 加速 1.9–7.4×〔原文 P56〕〔原文 P56 "accelerated the simulations by up to a factor of 1.9 to 7.4"〕；粗 4–8× 网格同级精度〔原文 P56〕〔原文 P56 "4 to 8 × coarser than standard"〕 | 代理再准也可能达不到所需保真度 ⇒ 仍需 CFD〔原文 P56〕〔原文 P56 "may not meet the required"〕 |
| 09 优化架构 | 换掉整个循环 | 序贯加点 / 在线交互 / RL 策略 / 条件生成 | ≤17 维用 Kriging、30 维转 ANN（Table 4，`code/ego.py` 演示 EI）；4,000× 加速〔原文 P61〕〔原文 P61 "4,000"〕 | 代理式不随维度良好扩展〔原文 P60〕〔原文 P60 "does not scale well with the dimensionality"〕；生成式最优点可偏离真最优〔原文 P59〕〔原文 P59 "could be distinct from the true optimum"〕 |
| 10 结论 | 给出验收标准 | "收益 + 前提"三句式 | 训练成本高是大规模应用的拦路石〔原文 P1〕〔原文 P1 "practical large-scale design optimizations remain"〕 | 很多模型未与传统 ASO 对比〔原文 P68〕〔原文 P68 "many ML models are applied to less challenging ASO"〕 |
![十二讲按三笔账着色：维度账 / 精度账 / 成本账](./images/part6v2_s1_matrix_map_zh.png)

| 11 批判 | 划出综述国境线 | 被引计数 + 0 命中检索 | 826 处编号标记 / 513 篇不同文献 / 书目 528 条（`tools/scan_corpus.py` 实测） | 结论章零图零表（本白皮书补 6.1） |

## 6.2 横向批判：这 12 讲共享的六个软肋

1. **精度口径不统一**：R²、平均相对误差、counts、MAE 四种口径混用，综述未给换算表 →
   任何人跨工作比较都在犯 category error（讲 07 §6）。
   → **怎么补**：一律四件套报数（留出集 MAE + 平均相对误差 + 样本量 + 划分方式）。
2. **训练成本全程隐身**：Abstract 承认"ML 训练成本高"〔原文 P1 "practical large-scale design optimizations remain"〕，
   但正文每一处成功案例都只报推理精度，**没有一处报"造这个模型花了多少核时"**（讲 09 §6、讲 10 §5）。
   → **怎么补**：把一次训练账（样本 × 机时 + 网络训练核时）写成表，放进论文正文而不是附录。
3. **外推风险只有定性警告**：无一处"外推距离—误差"曲线（讲 07、讲 10）。
   → **怎么补**：用最近邻距离 d(x) 做门控，报**外推子集**上的误差，而不是只报留出集。
4. **合法性阈值不可迁移**：0.7 是在翼型 + 特定跨声速机翼上定的（讲 06）；换到叶栅/端壁/涡轮没有任何依据。
   → **怎么补**：换对象就重定阈值，用 ROC 报出标定样本数与错判率。
5. **基线缺失**：作者自己在结论里点名的"未与传统 ASO 对比"（讲 10）——这是全领域通病，也是本白皮书作者的选题富矿。
   → **怎么补**：同预算下与传统方法并排跑，报 counts 与收敛率。
6. **编排割裂**：方法（§3）与应用（§4）相隔 30 页，同一技术（ME、Isomap、POD/DMD）两地分述（讲 11 §6），
   首次阅读者极易把"工具箱"和"战场"当成两件事——本白皮书用"每讲 §7 承前启后"专门对抗这条。
   → **怎么补**：本白皮书用每讲「承前启后」对抗；你读任何综述时也自己补一张方法↔应用对照表。

![六个软肋 → 六个选题：一条软肋正好长出一个题目](./images/part6v2_s2_six_weakspots_zh.png)

## 6.3 前瞻选题：六个软肋直接长出来的六个题目

| 软肋 | 可做的题 | 为什么你（孙承泽）能做 | 最小可行实验 |
| :--- | :--- | :--- | :--- |
| ①口径 | "统一评估协议：ASO 代理模型的四件套报告规范" | 你有真实平台与留出集，别人多在演示数据上 | 把 6 个公开/自有代理模型按同一四件套重报，做成技术报告 |
| ②成本 | "训练账本：ML-ASO 的摊销模型" | 你能拿到 SU2 机时与代理训练时间两个数 | 用 `code/curse.py` 的样本需求 × 单次 CFD 机时 → 画"第几次开始回本"曲线 |
| ③外推 | "最近邻距离门控：让交互式平台知道自己什么时候不可信" | 你已有 17.4 vs 6.1 的实测信号 | 给前端加 d(x) 计算（KD-tree）+ 阈值 + 拒答策略，测用户是否会误用 |
| ④阈值 | "跨对象合法性：把判别器搬到涡轮叶栅" | 你的叶栅数据是别人没有的 | 用翼型训的 CNN 在叶栅上量 FP/FN，重定 s_min（ROC，FPR ≤ 1%） |
| ⑤基线 | "200 次 CFD 预算内：NSGA-II+代理 vs SLSQP+伴随 vs Co-Kriging" | 三条你都能跑 | 同一初始样本、同一预算、报 counts 与收敛率 |
| ⑥盲区 | "综述 0 命中的那一格：FNO/DeepONet 能否替 Rotor 37 的 74→场" | 数据形状天然适合算子 | 先把输出从 3 标量升级成沿叶高分布，再对比 U-Net 与 FNO |

## 6.4 装配中改掉的旧说法（公示，避免复现）

> 学 Mr.GUO 仓库的"已删除虚构数字公示"制度：凡本书早期版本写错、已被推翻的数字，一律公示并写明判据。

| 旧说法 | 现状 | 判据 |
| :--- | :--- | :--- |
| 「降维把 d 从 74 打到 8，每维点数从 1.10 涨到 **10^0.875 ≈ 7.5**」 | **已改为 1000^(1/8) = 2.37（约 2.2 倍）** | 算式 N^(1/d) 由 `code/curse.py` 复算；10^0.875 是把"样本数 1000 = 10^3"错当成"指数 3 → 7.5"的脑补 |
| 「本综述正文有 870 个引用标记 / 529 条不同文献」（见 `../章程与地图/12篇论文总规划.md`） | 本次实测 **826 / 513**（书目 528 条与规划一致） | `tools/scan_corpus.py` 用固定正则与页区间（p3–68）计数；差异来自"区间式 `[1-4]` 是否展开"与页边界判定，脚本口径已在文件头写明，可复现 |
| 「图号最大 47、表号最大 5」 | 保留 | 与 `../资料原件/图表索引.md` 一致，并由 `tools/verify_all.py` B 项逐处核对 |
| 「每多一阶导数信息 ≈ 样本数减半」（文献里对 s=1 间接 GEK 的经验说法，本书讲稿初稿顺手带过） | **本白皮书不复现该说法**：`code/gek.py` 在 6 个随机设计上平均只换来 **1.13×**，n=10 时反而更差（0.93×）；讲 02 §4 已改为"稳定但有限 + 两个前提" | 判据是脚本输出（表 4 行、±sd 同表）；差异来源写在正文：虚拟点用一阶泰勒，Δ ∈ [0.10, 0.24] 的截断误差本身就是噪声 |
| 「图注/图上标注 每维 1.03 个点」（`L06_s4_shrink_and_gate_zh.png` 第一版） | **重画并改为 1.41**（1000^(1/20)），同时把图内"20 维 → 8 维"改成与 `code/modal.py` 一致的 **20 → 6（99% 能量线）** | 1.03 是我口算失误（把 1000^(1/100)=1.07 记串了）；正解由 `python3 -c "print(1000**(1/20))"` 与本仓 `code/curse.py` 双向核对 |

## 6.5 全书收口：一句话版

**这本白皮书只教了一件事：把"我要用机器学习做气动设计"翻译成三笔可核对的账——**

1. **维度账**：d 从多少降到多少？`code/curse.py` 里每轴点数变了多少？
2. **精度账**：留出集与**外推子集**的 MAE 各是多少？口径写了没有？
3. **成本账**：省下的 CFD 机时，够不够抵训练花掉的机时？什么时候开始回本？

> 三笔账都能报出数字的人，才算读完这篇 103 页的综述；
> 而能不能在组会上把**第四件事**说清楚——「这篇综述的国境线在哪、我要往哪一格补数据」——
> 决定你是这篇论文的**读者**，还是它的**下一个作者**。

**本白皮书自身的存疑清单（不设"已解决"，只设"何时能验"）**

| 存疑 | 计划验证方式 |
| :--- | :--- |
| 「统计特征参数化」是否真的无法反算几何（本白皮书讲 06 判断） | 找你的特征生成代码逐行确认；若能反算，本讲 §8 第一行作废 |
| 0.4% 相对误差 ↔ R² 的换算量级（讲 07 §3(b)） | 在你自己的 1,000 组数据上同时报两种口径，做一次实测标定 |
| 「s_min 保守取 0.5」是否比 0.7 更适配叶栅（讲 06 §8） | 用 ROC 曲线在 50 张人工标注合法新构型上定阈值 |
| EI 在 74 维上是否还有效（讲 09 §3(a)） | 先在 8 维模态空间上跑 `code/ego.py` 的同款实验，再逐级加维 |

---

## 6.6 附录 B2：全书认词总表（81 条，按首次定义排序）

> 用法：读到后面某一讲遇到没定义的词，回这张表查"首义于讲 N"，再去那一讲看它的操作定义。
> 表由脚本把 12 讲每讲开头的认词表自动合并生成，讲稿一改、重跑装配即同步。

| 词 | 英文 | 首义于 |
| :--- | :--- | :---: |
| 设计变量 | design variables | 讲 01 |
| 目标函数 | objective function | 讲 01 |
| 气动外形参数化 | geometric parameterization | 讲 01 |
| FFD | Free-Form Deformation，自由变形：Free 自由、Form 外形、Deformation 变形 | 讲 01 |
| 网格变形 | mesh deformation | 讲 01 |
| 伴随求解器 | adjoint solver | 讲 01 |
| XDSM | eXtended Design Structure Matrix，扩展设计结构矩阵 | 讲 01 |
| SLSQP / SNOPT | 两种梯度优化算法 | 讲 01 |
| 基函数 / 趋势函数 | basis / trend function f(x) | 讲 02 |
| 相关函数 | correlation function R(x, x′) | 讲 02 |
| 相关矩阵 | correlation matrix R | 讲 02 |
| 超参数 | hyperparameters θ | 讲 02 |
| 置信区间 | predictive confidence interval | 讲 02 |
| 梯度增强 Kriging | GEK = Gradient-Enhanced Kriging | 讲 02 |
| 协同克里金 | Co-Kriging / cokriging | 讲 02 |
| 多项式混沌展开 | PCE = Polynomial Chaos Expansion | 讲 02 |
| EGO | Efficient Global Optimization | 讲 02 |
| 聚类 | clustering | 讲 03 |
| k-means | k 均值：k 是堆数、means 是各堆的中心 | 讲 03 |
| 高斯混合模型 | GMM = Gaussian Mixture Model | 讲 03 |
| 主成分分析 | PCA = Principal Component Analysis | 讲 03 |
| 快照 | snapshot | 讲 03 |
| DMD | Dynamic Mode Decomposition，动态模态分解：Dynamic 动态、Mode 模态、Decomposition 分解 | 讲 03 |
| 流形学习 | manifold learning（Isomap / LLE 等） | 讲 03 |
| 降维/参数化 | dimensionality reduction | 讲 03 |
| 核 PCA | kernel PCA | 讲 03 |
| 低秩 | low-rank | 讲 03 |
| 伪标签 | pseudo label | 讲 04 |
| 受限玻尔兹曼机 | RBM = restricted Boltzmann machine（restricted 受限：层内不相连） | 讲 04 |
| 对比散度 | CD = contrastive divergence | 讲 04 |
| 深度信念网络 | DBN = deep belief network | 讲 04 |
| 强化学习 | RL = reinforcement learning（reinforcement 强化、learning 学习） | 讲 04 |
| 状态 / 动作 / 奖励 | state / action / reward | 讲 04 |
| Q 值 | Q(s,a) | 讲 04 |
| DQN | Deep Q-Network | 讲 04 |
| 策略梯度 | policy gradient（确定性策略梯度 DPG 直接把状态映射到最优动作）[^L04-13] | 讲 04 |
| 前向传播 / 反向传播 | forward pass / backpropagation | 讲 05 |
| 激活函数 | activation function | 讲 05 |
| 损失函数 | loss function | 讲 05 |
| 梯度消失 | vanishing gradient | 讲 05 |
| 过拟合 | overfitting | 讲 05 |
| 转置卷积 | transposed convolution | 讲 05 |
| 瓶颈层 | bottleneck layer | 讲 05 |
| 模态崩塌 | mode collapse | 讲 05 |
| 拓扑保持 | topology preservation | 讲 05 |
| 参数化 | parameterization | 讲 06 |
| CST | Class-Shape Transformation | 讲 06 |
| Hicks–Henne | 凸度函数叠加 | 讲 06 |
| 模态参数化 | modal parameterization | 讲 06 |
| ASM | Aerodynamic Shape Modes，气动外形模态：从**气动量**（而非几何坐标）里抽模态 | 讲 06 |
| 几何过滤 | geometric filtering | 讲 06 |
| 合法性得分 | validity score | 讲 06 |
| 最优采样 | deep-learning-based optimal sampling | 讲 06 |
| 响应面法 | polynomial response surface | 讲 07 |
| 混合专家 | ME = Mixture of Experts | 讲 07 |
| RMTS | regularized minimal-energy tensor-product splines | 讲 07 |
| 降阶模型 | ROM = reduced-order model | 讲 07 |
| 配点 | collocation points | 讲 07 |
| 计数 | drag counts | 讲 07 |
| 平均绝对误差 | MAE = mean absolute error | 讲 07 |
| 外推 | extrapolation | 讲 07 |
| 初场 | initial field / initial guess | 讲 08 |
| 保真度 | fidelity | 讲 08 |
| 模态多网格 | mode multigrid | 讲 08 |
| 数据驱动离散化 | data-driven discretization | 讲 08 |
| 湍流闭合 | turbulence closure | 讲 08 |
| 分离传感器 | separation sensor | 讲 08 |
| 离设计点 | off-design | 讲 08 |
| 隐式约束 | implicit constraint | 讲 08 |
| 加点准则 | infill criterion / acquisition | 讲 09 |
| 序贯优化 | sequential / iterative refinement | 讲 09 |
| SEGOMOE | Super-Efficient GO + Mixture Of Experts | 讲 09 |
| 弱/强学习者 | weak / strong learner | 讲 09 |
| 泛化性 | generalizability | 讲 09 |
| 经验知识来源 | empirical knowledge | 讲 10 |
| 插值型 | interpolative | 讲 10 |
| 外推能力 | extrapolation ability | 讲 10 |
| 覆盖盲区 | coverage gap | 讲 11 |
| 口径 | metric definition | 讲 11 |
| 可复现性 | reproducibility | 讲 11 |
| 被引次数 | citation count（本仓特指：在本综述正文 p3–68 内 `[N]` 标记出现次数） | 讲 11 |


---

## 6.7 附录 B3：十二讲 × 3 个数速查

> 用法：组会前扫一眼这 12 行；任何一个数你说不出页码与口径，就回原讲补。

| 讲 | 三个数 |
| :---: | :--- |
| 1 XDSM 与六个挑战：传统气 | 5 模块；六挑战 = 3 + 3；200 vs 1 |
| 2 Kriging 及其亲戚：一 | 1.13×；100,000；1.96σ |
| 3 降维的本质：把一整个流场压成 | 2.37；99%；100% |
| 4 标签不够与没有标签：半监督、 | 0.0180 vs 0.0205；λ = 0.1–0.3；100 × 200 |
| 5 神经网络全家桶：从 ANN  | 0.25^9 ≈ 4 × 10⁻⁶；523,011；0.678 → 0.0075 |
| 6 几何设计空间：模态参数化与几 | 100 → 15；s_min ≈ 0.7；1.41 → 3.16 |
| 7 气动评估：预测三个系数，还是 | 135,108；47,967；≤ 0.4% |
| 8 别让 CFD 从零起跑：加速 | 1.9–7.4×；40–80×；4% |
| 9 优化架构：代理式、交互式、R | 17 / 30；4,000×；5 步 |
| 10 作者的三条结论与一句自我批评 | 66 个数量级；1.10；0.04 / 2.5 counts |
| 11 批判性阅读：一篇 103 页 | 826；18；5 × 0 |
| 12 知识整合：一页报告、验收抽问 | 1.10 → 2.3；≤ 3 倍；≤ 0.5 |


---

## 6.8 附录 B4：平台修复清单总清算（13 项三栏）

> 三栏口径：**只省钱** = 不改模型也能做；**改模型** = 要动网络或加模块；**改流程** = 改的是规矩与验收方式。

| # | 项 | 做什么 | 类别 | 出自 |
| :---: | :--- | :--- | :---: | :---: |
| #1 | 插几何合法性判别器 | （输入 74 维向量 → 输出 0–1 分数，代价是一次性训练一个 CNN）——不改模型，只省钱。 | 改模型 | 讲 01 |
| #2 | Kriging/GEK 基线对打 | 同样 1000×74 数据、同样留出集，量 R² 与 95% 区间覆盖率，和 MC Dropout 的 65% 对质。 | 改模型 | 讲 02 |
| #3 | 先修 140k 粗网格收敛，再谈 Co-Kriging 融合 | （红线：未收敛的解不许进低精度层）。 | 改流程 | 讲 02 |
| #4 | 先 PCA 再喂代理 | 把 74 维压到 8–20 维（按累计方差 ≥ 99% 定 k）， | 改流程 | 讲 03 |
| #5 | 未收敛算例登记为无标签集 | 给 relrms = −3.39 那批数据打上"未收敛"标记， | 改流程 | 讲 04 |
| #6 | 残差代理 PINN 化（路线二） | 在现有损失上加一项物理残差 | 改模型 | 讲 05 |
| #7 | 拆通道 | 74 维统计特征降级为中间表征， | 只省钱 | 讲 06 |
| #8 | 预优化采样抽模态 | 按 Duan et al. 的路子攒 1,000–2,000 个"好形状"， | 只省钱 | 讲 06 |
| #9 | 上 CNN 合法性门禁 | 正样本用历史 1,000 组、负样本用随机 FFD 扰动， | 改模型 | 讲 06 |
| #10 | 报误差必须报外推子集口径 | 随机留出与"按 Ω/P 分组留出"两个 R² 一起报； | 改流程 | 讲 07 |
| #11 | 你的 SU2 初场可用 CNN 代理给初值 | 先把 140k 粗网格跑到收敛立起 baseline， | 改模型 | 讲 08 |
| #12 | 交互平台加"拒答阈值" | 前端在到训练集最近邻距离超过阈值时（你的实测：前沿 17.4 对内部 6.1）， | 只省钱 | 讲 09 |
| #13 | 选题⑥：从境外五城里挑一座建桥 | 。五城 = FNO / DeepONet / Transformer / 扩散模型 / SINDy， | 改模型 | 讲 11 |

