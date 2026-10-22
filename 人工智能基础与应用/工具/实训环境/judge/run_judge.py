#!/usr/bin/env python3
"""判分器接线脚本（脚手架区 B4）· Agent 维护，用户不需要改。

职责：
  1. 确保上游判分器已就位（缺失则克隆，并锁定 commit）
  2. 把官方 tests/ 原样复制到 .build/（**绝不修改 test_*.py**）
  3. 注入接线文件 tests/adapters.py：把 手写/bpe.py 接到官方测试期望的接口上
  4. 选择 conftest：Python≥3.12 用官方原文；否则用**等价轻量版**（并在日志里如实声明）
  5. 运行 pytest，原始输出打印 + 落盘归档

用法：
    python run_judge.py 01 [--quick] [--selftest] [--no-archive] [--keep]
环境变量：
    SCZ_HANDWRITTEN_FILE  覆盖手写文件路径（自测用）
    SCZ_SELF_WIRE=1       保留官方 adapters.py 模板，由用户自己接线
"""
from __future__ import annotations

import argparse
import datetime as dt
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SUBJECT = HERE.parent.parent                      # 人工智能基础与应用/
UPSTREAM = SUBJECT / "上游"
BUILD_ROOT = HERE / ".build"

LABS: dict[str, dict] = {
    "01": {
        "name": "BPE 分词器",
        "repo": "stanford-cs336/assignment1-basics",
        "commit": "a158843b2010",
        "tests": ["tests/test_train_bpe.py", "tests/test_tokenizer.py"],
        "handwritten": "课题01-BPE分词器/手写/bpe.py",
        "evidence_dir": "课题01-BPE分词器/证据",
        "adapter": "tokenizer",
    },
}

ADAPTER_TOKENIZER = '''\
"""自动生成：CS336 官方测试 → 手写/bpe.py 的接线层。
生成者：环境/judge/run_judge.py；请勿手改（下次判分会覆盖）。
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

_USER_FILE = Path(r"{user_file}")
_CACHE = {{}}


def _user():
    if "mod" in _CACHE:
        return _CACHE["mod"]
    if not _USER_FILE.exists():
        raise FileNotFoundError(
            "手写区还没有实现文件：\\n  " + str(_USER_FILE) +
            "\\n这是本课题的初始状态——先在 手写/bpe.py 写出 train_bpe 与 Tokenizer，再回来判分。"
        )
    spec = importlib.util.spec_from_file_location("scz_handwritten_bpe", _USER_FILE)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    _CACHE["mod"] = mod
    return mod


# --- 官方 adapters.py 要求的两个入口（签名原样照抄）---------------------
def get_tokenizer(vocab, merges, special_tokens=None):
    return _user().Tokenizer(vocab, merges, special_tokens)


def run_train_bpe(input_path, vocab_size, special_tokens, **kwargs):
    return _user().train_bpe(input_path, vocab_size, special_tokens, **kwargs)
'''

# 等价轻量 conftest：只提供 snapshot 夹具（官方语义一致），去掉 torch 与 PEP 695 依赖
CONFTEST_MINIMAL = '''\
"""轻量 conftest（由 环境/judge/run_judge.py 生成）
为什么不是官方原文：
  1) 官方 tests/conftest.py 使用 PEP 695 泛型语法（`def f[T](...)`/`class C[T]`），
     需要 Python >= 3.12（官方 pyproject: requires-python = ">=3.12,<3.14"）；
     当前解释器为 {pyver}，无法解析。
  2) 官方 conftest 其余夹具是为课题02 的模型测试准备的（依赖 torch）。
本文件只保留课题01 需要的 `snapshot` 夹具，语义与官方 Snapshot.assert_match 一致（pickle 逐键比较）。
⚠️ 官方两个测试文件 test_train_bpe.py / test_tokenizer.py 未被修改一字。
"""
import os
import pickle
from pathlib import Path

import pytest


class DEFAULT:
    pass


class Snapshot:
    def __init__(self, snapshot_dir="tests/_snapshots", default_force_update=False, default_test_name=None):
        self.snapshot_dir = Path(snapshot_dir)
        os.makedirs(self.snapshot_dir, exist_ok=True)
        self.default_force_update = default_force_update
        self.default_test_name = default_test_name

    def _get_snapshot_path(self, test_name: str) -> Path:
        return self.snapshot_dir / f"{{test_name}}.pkl"

    def assert_match(self, actual, test_name=DEFAULT, force_update=DEFAULT):
        if force_update is DEFAULT:
            force_update = self.default_force_update
        if test_name is DEFAULT:
            assert self.default_test_name is not None, "Test name must be provided or set as default"
            test_name = self.default_test_name
        with open(self._get_snapshot_path(test_name), "rb") as f:
            expected_data = pickle.load(f)
        if isinstance(actual, dict):
            for key in actual:
                if key not in expected_data:
                    raise AssertionError(f"Key '{{key}}' not found in snapshot for {{test_name}}")
                assert actual[key] == expected_data[key], (
                    f"Data for key '{{key}}' does not match snapshot for {{test_name}}"
                )
        else:
            assert actual == expected_data, f"Data does not match snapshot for {{test_name}}"


def pytest_addoption(parser):
    # 官方 conftest 支持该选项（供 numpy_snapshot 使用）；此处仅为兼容性保留
    parser.addoption("--snapshot-exact", action="store_true", default=False, help="Use exact matching for numpy snapshots")


@pytest.fixture
def snapshot(request):
    return Snapshot(default_force_update=False, default_test_name=request.node.name)
'''


def log(msg: str) -> None:
    print(msg, flush=True)


def ensure_upstream(cfg: dict) -> Path:
    dest = UPSTREAM / cfg["repo"].split("/")[-1]
    if not dest.exists():
        log(f"→ 克隆上游判分器：{cfg['repo']}")
        UPSTREAM.mkdir(parents=True, exist_ok=True)
        subprocess.run(["git", "clone", "--depth", "1", f"https://github.com/{cfg['repo']}.git", str(dest)], check=True)
    else:
        log(f"✅ 上游已就位：{dest.relative_to(SUBJECT)}")
    return dest


def build_workspace(cfg: dict, upstream: Path) -> tuple[Path, str]:
    """复制官方 tests/，注入接线文件与 conftest。返回 (build_dir, conftest_mode)。"""
    build = BUILD_ROOT / f"lab{cfg['lab']}"
    if build.exists():
        shutil.rmtree(build)
    build.mkdir(parents=True)
    shutil.copytree(upstream / "tests", build / "tests")

    user_file = Path(os.environ.get("SCZ_HANDWRITTEN_FILE") or (SUBJECT / cfg["handwritten"]))
    adapter = build / "tests" / "adapters.py"
    if os.environ.get("SCZ_SELF_WIRE") == "1":
        mode_adapter = "官方 adapters.py 原文（用户自行接线）"
    else:
        adapter.write_text(ADAPTER_TOKENIZER.format(user_file=user_file), encoding="utf-8")
        mode_adapter = f"接线层 → {user_file}"

    py = sys.version_info
    official_conftest = py >= (3, 12) and os.environ.get("SCZ_MINIMAL_CONFTEST") != "1"
    if official_conftest:
        conftest_mode = f"官方 conftest 原文（Python {py.major}.{py.minor} ≥ 3.12 ✅）"
    else:
        (build / "tests" / "conftest.py").write_text(
            CONFTEST_MINIMAL.format(pyver=f"{py.major}.{py.minor}.{py.micro}"), encoding="utf-8"
        )
        conftest_mode = (
            f"等价轻量 conftest（Python {py.major}.{py.minor} < 3.12，官方原文用 PEP 695 语法无法解析；"
            "已保留同一 snapshot 夹具语义）"
        )

    log(f"→ 工作区：{build.relative_to(SUBJECT)}｜官方 test_*.py 未改动")
    log(f"→ adapters：{mode_adapter}")
    log(f"→ conftest：{conftest_mode}")
    return build, conftest_mode


def run_pytest(build: Path, cfg: dict, quick: bool) -> tuple[int, str]:
    tests = list(cfg["tests"])
    if quick:
        tests = ["tests/test_train_bpe.py",
                 "tests/test_tokenizer.py::test_roundtrip_empty",
                 "tests/test_tokenizer.py::test_roundtrip_ascii_string"]
    venv_py = HERE.parent / ".venv" / "bin" / "python"
    py = str(venv_py) if venv_py.exists() else sys.executable
    cmd = [py, "-m", "pytest", "-v", "--tb=short", "-p", "no:cacheprovider", *tests]
    log("\n" + "=" * 70)
    log("官方判分器运行中：" + " ".join(tests))
    log("=" * 70)
    proc = subprocess.run(cmd, cwd=build, capture_output=True, text=True)
    out = proc.stdout + proc.stderr
    print(out, flush=True)
    return proc.returncode, out


def archive(cfg: dict, raw: str, code: int, conftest_mode: str, selftest: bool) -> Path:
    ev = SUBJECT / cfg["evidence_dir"]
    ev.mkdir(parents=True, exist_ok=True)
    ts = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    tag = "SELFTEST-" if selftest else ""
    path = ev / f"judge-{tag}{ts}.log"
    passed = len(re.findall(r"\bPASSED\b", raw))
    failed = len(re.findall(r"\bFAILED\b", raw))
    header = (
        f"# 判分原始输出（课题{cfg['lab']} · {cfg['name']}）\n"
        f"- 时间：{dt.datetime.now().isoformat(timespec='seconds')}\n"
        f"- 判分器：CS336 官方测试（锁定 commit {cfg['commit']}），**test_*.py 未修改一字**\n"
        f"- conftest：{conftest_mode}\n"
        f"- 结果：exit={code}  PASSED={passed}  FAILED={failed}\n"
        f"- 说明：本文件由 环境/judge/run_judge.py 自动生成；原文照录，不做美化\n\n"
        f"```\n{raw}\n```\n"
    )
    path.write_text(header, encoding="utf-8")
    log(f"\n→ 原始输出已归档：{path.relative_to(SUBJECT)}")
    return path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("lab", choices=sorted(LABS))
    ap.add_argument("--quick", action="store_true", help="只跑关键几项，频繁自测用")
    ap.add_argument("--selftest", action="store_true", help="Agent 自测判分管线（不污染证据目录）")
    ap.add_argument("--no-archive", action="store_true", help="不写归档文件")
    ap.add_argument("--keep", action="store_true", help="保留 .build 工作区")
    a = ap.parse_args()

    cfg = dict(LABS[a.lab], lab=a.lab)
    log("=" * 70)
    log(f" 判分 · 课题{a.lab} {cfg['name']}" + ("（自测模式）" if a.selftest else ""))
    log("=" * 70)
    upstream = ensure_upstream(cfg)
    build, conftest_mode = build_workspace(cfg, upstream)
    code, out = run_pytest(build, cfg, a.quick)

    if not (a.no_archive or a.selftest):
        archive(cfg, out, code, conftest_mode, a.selftest)
    if not a.keep:
        shutil.rmtree(build, ignore_errors=True)

    log("\n" + "-" * 70)
    if a.selftest:
        log(f"自测完成：exit={code}（用于验证判分管线可执行；不代表任何成绩）")
    elif code == 0:
        log("✅ 判分通过。把 证据/judge-*.log 的原文贴进 判卷记录.md，再补 L2 审稿意见。")
    else:
        log("❌ 判分未通过。按《知行合一规程》§四：先写预测 → 再改代码 → 再回来看这里。")
    log("-" * 70)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
