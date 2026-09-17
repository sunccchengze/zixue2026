# 判分器接入（脚手架区 B4）· 用户不需要改这里的任何文件

> 目标：**判分标准由斯坦福 CS336 官方测试定义，一字不改**；我们的工作只是把它接到你的手写实现上。
> 你唯一要做的事，是让 `课题NN/手写/` 里的文件符合下面的**接口契约**。

## 一、课题01（BPE）的接口契约

你的 `课题01-BPE分词器/手写/bpe.py` 必须提供两样东西（签名照 CS336 handout 原样）：

```python
# 1) 训练
def train_bpe(
    input_path: str | os.PathLike,
    vocab_size: int,
    special_tokens: list[str],
    **kwargs,
) -> tuple[dict[int, bytes], list[tuple[bytes, bytes]]]:
    """返回 (vocab, merges)
    vocab : {token_id: token_bytes}  含 256 个基础字节 + 合并产物 + 特殊 token
    merges: [(bytes1, bytes2), ...]  按创建顺序排列
    注意：特殊 token 绝不参与合并，且不得出现在其他 token 的字节里。
    """

# 2) 分词器对象
class Tokenizer:
    def __init__(self, vocab: dict[int, bytes], merges: list[tuple[bytes, bytes]],
                 special_tokens: list[str] | None = None): ...
    def encode(self, text: str) -> list[int]: ...
    def decode(self, ids: list[int]) -> str: ...
```

> ⚠️ 这里的接口**不是我给你定的**，是 CS336 官方 `tests/adapters.py` 要求的（我读的是上游原文）。
> 你可以自己决定内部怎么组织，但这两个签名不能变——否则判分器的接线会断。

## 二、判分器怎么工作（三步，全自动）

```bash
环境/judge/judge.sh 01        # 判课题01
```

1. **拉取官方判分器**：把 `stanford-cs336/assignment1-basics` 克隆到 `上游/`（已存在则复用），
   锁定 commit（见 `章程与地图/上游锁定清单.md`）。
2. **接线**：把上游的 `tests/` 原样复制到 `.build/`（**不改一行测试**），
   只替换 `tests/adapters.py` 为我们的**接线文件**——它把你 `手写/bpe.py` 里的 `train_bpe` /
   `Tokenizer` 接到官方测试期望的 `run_train_bpe` / `get_tokenizer` 上。
3. **跑分**：执行 `pytest tests/test_train_bpe.py tests/test_tokenizer.py`，
   **原始输出**同时打印到屏幕并落进 `课题NN/证据/judge-<时间戳>.log`。

## 三、为什么 adapters.py 由我写（透明说明）

CS336 官方流程里，`tests/adapters.py` 是学生自己填的——但那是**纯接线**（把函数名对上），
不含任何 BPE 算法知识。按本学科《造轮子边界.md》，接线属 **B2 类脚手架**，
由我写完整、不留 TODO；你只写真正需要学的算法本身。

> 如果你希望自己接线（更贴近官方流程），删掉 `.build/` 后设置 `SCZ_SELF_WIRE=1` 再跑
> `judge.sh 01`，脚本会把官方 `adapters.py` 原样给你，你去填。

## 四、课题01 的官方判分门槛（先知道标准，再动手）

| 测试 | 判什么 | 门槛 |
|---|---|---|
| `test_train_bpe_speed` | 训练效率 | corpus.en + vocab 500 **必须 < 1.5 秒**（官方参考实现 0.38s；"玩具实现"约 3s 会挂） |
| `test_train_bpe` | 正确性 | 你的 merges **逐个比对**官方参考 merges；vocab 的键与值集合必须一致 |
| `test_train_bpe_special_tokens` | 特殊 token | 特殊 token 不进合并、且不得以 `b"<|"` 形式泄漏进其他 token |
| `test_tokenizer.py`（16+ 项） | 编码/解码 | 空串、单字符、Unicode、多行、特殊 token 边界、往返一致性，并与 **tiktoken(GPT-2)** 逐 id 对齐 |

**几个关键推论**（这些是解题线索，不是答案）：
- 有**速度门槛** → 朴素 O(n²) 字符串拼接实现会挂 → 数据结构选择是本题核心难点之一。
- 要**逐 id 对齐 tiktoken** → 编码时的合并顺序必须严格按 merges 的顺序（不能按最长匹配）。
- 有**内存上限**测试（用 `resource.RLIMIT_AS`）→ 不能把整个语料读进内存再暴力展开。

## 五、后续课题的判分器（待接入）

| 课题 | 上游判分器 | 备注 |
|---|---|---|
| 02 | `assignment1-basics/tests/test_model.py`、`test_nn_utils.py`、`test_optimizer.py`、`test_serialization.py` | 需要 torch（已装） |
| 05/06 | `assignment2-systems/tests/` | ⚠️ flash-attn 需两步安装；Triton 需 GPU（T4 及以上） |
| 07 | `assignment4-data/tests/` | 数据管线 |
| 08 | `assignment5-alignment/tests/test_grpo.py` | ⚠️ 需确认该仓许可（见上游锁定清单） |
| 03 | **无**（A3 需学号 API key） | 自建判分：拟合优度 + 外推误差，脚本在 `环境/judge/` 一并提供 |
