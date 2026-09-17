#!/usr/bin/env python3
"""tiktoken 词表离线预热（脚手架区 B1 附属）· Agent 维护

为什么需要它：
  CS336 的 `tests/test_tokenizer.py` 要用 tiktoken 的 GPT-2 编码器做**逐 id 对齐**校验，
  而 tiktoken 首次使用时会联网下载 vocab.bpe / encoder.json。在无外网或外网受限的环境
  （本仓沙箱、部分校园网、Kaggle 断网会话）会直接 SSLError 挂掉。

本脚本做两件事：
  1. 优先尝试真实下载（有外网时走这条路，最正统）；
  2. 下载不通时，用 CS336 官方 fixture（`上游/assignment1-basics/tests/fixtures/gpt2_*.json/txt`）
     在本地**构造** tiktoken 缓存：
       - encoder.json ← gpt2_vocab.json（sha256 与 tiktoken 内置期望完全一致，可验证）
       - vocab.bpe    ← "#version: 0.2\\n" + gpt2_merges.txt（tiktoken 解析时会跳过首行）
     已验证：tiktoken 对 gpt2 不传 expected_hash，因此构造出的缓存可用；
     构造后本脚本仍会**实际加载一次**确认 n_vocab=50257。

用法：
    python 环境/judge/prefetch_tiktoken.py
产物：环境/tiktoken-cache/（已 gitignore，可随时重建）
"""
from __future__ import annotations

import hashlib
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SUBJECT = HERE.parent.parent
CACHE = SUBJECT / "环境" / "tiktoken-cache"
FIXTURES = SUBJECT / "上游" / "assignment1-basics" / "tests" / "fixtures"

GPT2_VOCAB_BPE_URL = "https://openaipublic.blob.core.windows.net/gpt-2/encodings/main/vocab.bpe"
GPT2_ENCODER_JSON_URL = "https://openaipublic.blob.core.windows.net/gpt-2/encodings/main/encoder.json"
ENCODER_JSON_SHA256 = "196139668be63f3b5d6574427317ae82f612a97c5d1cdaf36ed2256dbf636783"


def cache_path(url: str) -> Path:
    return CACHE / hashlib.sha1(url.encode()).hexdigest()


def try_real_download() -> bool:
    """有外网时直接让 tiktoken 自己下载（最正统）。"""
    os.environ["TIKTOKEN_CACHE_DIR"] = str(CACHE)
    try:
        import tiktoken

        enc = tiktoken.get_encoding("gpt2")
        print(f"✅ 真实下载成功：gpt2 n_vocab={enc.n_vocab}")
        return True
    except Exception as exc:  # noqa: BLE001
        print(f"⚠️  联网下载不可用（{type(exc).__name__}）→ 改用官方 fixture 离线构造")
        return False


def build_from_fixtures() -> None:
    vocab_json = FIXTURES / "gpt2_vocab.json"
    merges_txt = FIXTURES / "gpt2_merges.txt"
    if not vocab_json.exists() or not merges_txt.exists():
        sys.exit(
            "❌ 找不到官方 fixture。请先跑一次判分器（它会克隆上游）：\n"
            "   环境/judge/judge.sh 01 --quick    # 目的是触发上游克隆\n"
            f"   期望路径：{FIXTURES}"
        )

    encoder_bytes = vocab_json.read_bytes()
    got = hashlib.sha256(encoder_bytes).hexdigest()
    if got != ENCODER_JSON_SHA256:
        print(f"⚠️  encoder.json 哈希不一致（期望 {ENCODER_JSON_SHA256[:12]}… 实际 {got[:12]}…），仍继续（tiktoken 不校验）")
    else:
        print("✅ encoder.json 哈希与 tiktoken 内置期望一致")

    merges_text = merges_txt.read_text(encoding="utf-8")
    if not merges_text.endswith("\n"):
        merges_text += "\n"
    # tiktoken 解析第一行为版本头并丢弃（split("\n")[1:-1]）
    vocab_bpe_bytes = ("#version: 0.2\n" + merges_text).encode("utf-8")

    CACHE.mkdir(parents=True, exist_ok=True)
    cache_path(GPT2_ENCODER_JSON_URL).write_bytes(encoder_bytes)
    cache_path(GPT2_VOCAB_BPE_URL).write_bytes(vocab_bpe_bytes)
    print(f"→ 已写入缓存：{CACHE.relative_to(SUBJECT)}（{len(list(CACHE.iterdir()))} 个文件）")


def verify() -> None:
    os.environ["TIKTOKEN_CACHE_DIR"] = str(CACHE)
    import tiktoken

    enc = tiktoken.get_encoding("gpt2")
    assert enc.n_vocab == 50257, f"n_vocab 异常：{enc.n_vocab}"
    sample = "hello world 你好，世界！"
    ids = enc.encode(sample)
    assert enc.decode(ids) == sample, "往返一致性失败"
    print(f"✅ 离线缓存可用：n_vocab={enc.n_vocab}，示例 '{sample}' → {len(ids)} 个 id，往返一致")


if __name__ == "__main__":
    print("=" * 60)
    print(" tiktoken GPT-2 词表预热")
    print("=" * 60)
    if not try_real_download():
        build_from_fixtures()
        verify()
    print("\n下一步：环境/judge/judge.sh 01 （judge.sh 会自动设置 TIKTOKEN_CACHE_DIR）")
