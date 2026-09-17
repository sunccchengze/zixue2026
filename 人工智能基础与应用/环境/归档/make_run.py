#!/usr/bin/env python3
"""证据归档 · run.yaml 生成器（脚手架区 B5）· Agent 维护

目的：让每一次实验都自动留下**可追溯的身份证**——这是本学科"无证据的结论不采纳"的落地工具。

用法示例：
  python 环境/归档/make_run.py --lab 04 --hypothesis "双T4 跑 d12 可在 9h 内到 bpb<1.0" \
      --cmd "torchrun --nproc_per_node=2 -m scripts.base_train --depth=12" \
      --gpu "2xT4" --hours 9.0 --seed 1337 --tag smoke

产物：课题NN-*/证据/run-<时间戳>.yaml（+ 可选对产物目录做 sha256 清单）
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import platform
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SUBJECT = HERE.parent.parent
REPO = SUBJECT.parent

LAB_DIRS = {
    "01": "课题01-BPE分词器", "02": "课题02-Transformer骨架", "03": "课题03-Scaling-Law",
    "04": "课题04-0.1B端到端", "05": "课题05-Triton-attention-kernel", "06": "课题06-多卡与分布式",
    "07": "课题07-数据清洗与去重", "08": "课题08-SFT-DPO-RLVR", "09": "课题09-可验证环境",
    "10": "课题10-长程Agent", "11": "课题11-结项",
}


def sh(cmd: list[str], cwd: Path | None = None) -> str:
    try:
        return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=20).stdout.strip()
    except Exception as exc:  # noqa: BLE001
        return f"<err: {exc}>"


def git_info() -> dict:
    return {
        "branch": sh(["git", "rev-parse", "--abbrev-ref", "HEAD"], REPO),
        "commit": sh(["git", "rev-parse", "--short", "HEAD"], REPO),
        "dirty": bool(sh(["git", "status", "--porcelain"], REPO)),
    }


def gpu_info() -> dict:
    if not shutil_which("nvidia-smi"):
        return {"available": False, "note": "本机无 nvidia-smi（CPU 实验或云端未预检）"}
    q = "name,memory.total,compute_cap"
    out = sh(["nvidia-smi", f"--query-gpu={q}", "--format=csv,noheader"])
    return {"available": True, "raw": out, "count": len(out.splitlines()) if out else 0}


def shutil_which(name: str) -> str | None:
    from shutil import which

    return which(name)


def hash_artifacts(paths: list[str]) -> list[dict]:
    out = []
    for p in paths:
        path = Path(p)
        if not path.exists():
            out.append({"path": p, "status": "missing"})
            continue
        if path.is_file():
            h = hashlib.sha256(path.read_bytes()).hexdigest()
            out.append({"path": p, "bytes": path.stat().st_size, "sha256": h})
        else:
            files = [f for f in path.rglob("*") if f.is_file()]
            total = sum(f.stat().st_size for f in files)
            digest = hashlib.sha256()
            for f in sorted(files):
                digest.update(hashlib.sha256(f.read_bytes()).digest())
            out.append({"path": p, "files": len(files), "bytes": total, "sha256_tree": digest.hexdigest()})
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lab", required=True, choices=sorted(LAB_DIRS))
    ap.add_argument("--hypothesis", required=True, help="一句话假设（必须可被证伪）")
    ap.add_argument("--cmd", required=True, help="完整可复制的命令")
    ap.add_argument("--prediction", default="", help="**先写下的预测**（知行合一的咬合点）")
    ap.add_argument("--stop-condition", default="loss 不降 / 超预算 / 出现 NaN → 立即停")
    ap.add_argument("--success", default="", help="成功判据（跑之前先写死）")
    ap.add_argument("--gpu", default="cpu", help="如 2xT4 / 1xT4 / cpu")
    ap.add_argument("--hours", type=float, default=0.0, help="实际耗时（GPU·小时）")
    ap.add_argument("--seed", default="")
    ap.add_argument("--tag", default="")
    ap.add_argument("--artifact", action="append", default=[], help="要哈希的产物路径（可多次）")
    ap.add_argument("--notes", default="")
    a = ap.parse_args()

    ev = SUBJECT / LAB_DIRS[a.lab] / "证据"
    ev.mkdir(parents=True, exist_ok=True)
    ts = dt.datetime.now()
    name = f"run-{ts.strftime('%Y%m%d-%H%M%S')}" + (f"-{a.tag}" if a.tag else "")
    path = ev / f"{name}.yaml"

    data = {
        "lab": a.lab,
        "lab_dir": LAB_DIRS[a.lab],
        "created_at": ts.isoformat(timespec="seconds"),
        "hypothesis": a.hypothesis,
        "prediction_written_before_run": a.prediction or "<未写——本次不计入预测-打脸链路>",
        "command": a.cmd,
        "stop_condition": a.stop_condition,
        "success_criteria": a.success or "<未写>",
        "compute": {"device": a.gpu, "actual_gpu_hours": a.hours, "gpu_probe": gpu_info()},
        "seed": a.seed,
        "repo": git_info(),
        "runtime": {"python": sys.version.split()[0], "platform": platform.platform()},
        "upstream_locked": {
            # 与 章程与地图/上游锁定清单.md 同步；此处只记当前实际 HEAD，供事后核对
            "cs336_a1": sh(["git", "-C", str(SUBJECT / "上游" / "assignment1-basics"), "rev-parse", "--short", "HEAD"]),
        },
        "artifacts": hash_artifacts(a.artifact),
        "notes": a.notes,
        "archive_rule": "本文件是证据链的一部分；no-go 与失败结果同样保留，不删除",
    }

    # 手写 YAML（避免引入 pyyaml 依赖）
    def dump(obj, indent=0) -> str:
        pad = "  " * indent
        lines = []
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    lines.append(f"{pad}{k}:")
                    lines.append(dump(v, indent + 1))
                else:
                    lines.append(f"{pad}{k}: {json.dumps(v, ensure_ascii=False)}")
        elif isinstance(obj, list):
            for item in obj:
                if isinstance(item, (dict, list)):
                    lines.append(f"{pad}-")
                    lines.append(dump(item, indent + 1))
                else:
                    lines.append(f"{pad}- {json.dumps(item, ensure_ascii=False)}")
        return "\n".join(lines)

    path.write_text(dump(data) + "\n", encoding="utf-8")
    print(f"✅ 证据已归档：{path.relative_to(SUBJECT)}")
    if not a.prediction:
        print("⚠️  提醒：本次没有预先写下的预测——按《知行合一规程》§四，这不计入'预测-打脸'链路。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
