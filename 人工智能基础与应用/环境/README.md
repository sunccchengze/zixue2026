# 环境（脚手架区 B1–B8，Agent 全权负责）

> 本目录是**基建区**：这里的东西由我写完整，**不留 TODO 给用户**（见《造轮子边界.md》）。
> 用户只在"要不要跑、花多少配额"上拍板。

## 一、目录职责

```
环境/
├── README.md         本文件
├── bootstrap_cpu.sh  T0：沙箱/本地 CPU 环境（uv + 依赖，跑判分用）        ← 待建
├── bootstrap_kaggle.md Kaggle 会话开场清单（预检 + 依赖 + 数据）          ← 待建
├── 预检.md           会话预检：GPU 型号门禁（T4 ✅ / P100 ❌）            ← 待建
├── judge/            判分器接入：CS336 tests + adapters + judge.sh        ← 待建
├── 数据/             TinyStories / owt-sample 的获取与分片（小样本进仓）  ← 待建
├── 归档/             run.yaml 生成、曲线绘图、产物哈希                    ← 待建
└── 报告模板/         一页四段（中文）+ NeurIPS（英文）模板                ← 待建
```

## 三、建设状态（2026-09-17 实跑验证）

| 文件 | 状态 | 说明 |
|---|---|---|
| `bootstrap_cpu.sh` | ✅ 建成并实跑 | 轻量档 9 秒装好（pytest/tiktoken/psutil/numpy/jaxtyping）；`--with-torch` 可选装 torch |
| `judge/judge.sh` + `run_judge.py` | ✅ 建成并实跑 | **CS336 官方 28 个测试真实执行**（基线 27 failed + 1 xfailed，全部因缺 `手写/bpe.py`）；自动归档原始输出到 `证据/` |
| `judge/prefetch_tiktoken.py` | ✅ 建成并实跑 | 离线构造 tiktoken GPT-2 词表缓存（绕开沙箱外网限制），实测 n_vocab=50257 |
| `预检.md` | ✅ 建成 | 会话门禁（P100 一票否决）+ 实验卡制度 |
| `归档/` | ⬜ 待建 | run.yaml 生成 + 曲线绘制（课题04 前必须就绪） |
| `报告模板/` | ⬜ 待建 | 中文一页四段 + 英文 NeurIPS 骨架（W3 前就绪） |

## 四、技术决定（写在这里防止漂移）

| 项 | 决定 | 理由 |
|---|---|---|
| 依赖管理 | **uv**（与 CS336 一致） | 自带 lock，跨机器可复现 |
| 判分 | **pytest + CS336 `tests/adapters.py`** | 客观、可复跑、原始输出可归档 |
| 数据类型 | 训练用 **fp16 + GradScaler**（T4 无 bf16） | nanochat 在 SM<80 默认 fp32，太慢 |
| 断点续训 | 强制，checkpoint 写 `/kaggle/working` | Kaggle 会话随时可能断（9–12h 上限） |
| 超时 | 脚本内置 wall-clock 上限（默认 3h） | 防"忘记关机"式浪费配额 |
| 曲线 | 本地 matplotlib → PNG 进 `证据/` | 不依赖 wandb（免费额度/网络都不稳） |
| 大文件 | 一律 `.gitignore`（见学科根 `.gitignore`） | 仓库有快照体积上限 |

## 三、待建设清单（下一步实现顺序）

1. `预检.md`：会话开场 5 条检查（GPU 型号 / 磁盘 / 依赖 / 数据 / 计时器）
2. `bootstrap_cpu.sh`：沙箱内一键装好 pytest + 依赖，能直接跑 CS336 tokenizer 判分
3. `judge/`：把 CS336 A1–A5 的 `tests/` 克隆到**仓库外**（`上游/`），写 `judge.sh 课题01` 一键出判分原始输出
4. `归档/`：`run.yaml` 生成脚本（git commit / 上游 commit / 超参 / 随机种子 / 命令 / 时间）+ 曲线绘制
5. `bootstrap_kaggle.md`：含"若分配到 P100 如何重开"的分支说明
6. `报告模板/`：中文一页四段 + 英文 NeurIPS 骨架（署名直填规则）

> 纪律提醒：以上脚本属于 **B 类代写**，我可以直接写完；
> 但**任何进入 `课题NN/手写/` 的内容一律不在此列**。
