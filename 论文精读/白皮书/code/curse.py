#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
curse.py —— 维度灾难计算器（讲 03 / 第零章 0.4 的数字都由它现场复算）
============================================================================
三个问题：
  Q1 N 个点均匀撒进 d 维盒子，每个方向摊到几个点？  → per_axis = N ** (1/d)
  Q2 想让每轴至少 t 个点，需要多少样本？            → need = t ** d
  Q3 高维立方体里随机取点，它离边界有多近、离邻居有多远？（蒙特卡洛实证）

用法： python3 code/curse.py            # 跑自检并打印
      python3 code/curse.py --n 1000 --dims 1,3,8,74,100 --t 10
"""
from __future__ import annotations

import argparse
import math
import random


def per_axis(n: float, d: int) -> float:
    return n ** (1.0 / d)


def need_samples(d: int, t: float) -> float:
    return t ** d


def edge_stats(d: int, trials: int = 4000, seed: int = 7):
    """单位立方体 [0,1]^d 内均匀取点：统计到最近边界的距离（取各坐标 min(x,1-x) 的最小值）
    以及到最近邻居的距离。返回两个均值。"""
    rng = random.Random(seed)
    pts = [[rng.random() for _ in range(d)] for _ in range(trials)]
    edge = min(min(min(x, 1 - x) for x in p) for p in pts[:trials])
    edge_mean = sum(min(min(x, 1 - x) for x in p) for p in pts) / trials
    nn = []
    for i in range(120):
        best = float("inf")
        for j in range(120):
            if i == j:
                continue
            best = min(best, math.dist(pts[i], pts[j]))
        nn.append(best)
    return edge_mean, sum(nn) / len(nn), edge


def report(n: float, dims: list[int], t: float) -> str:
    lines = [f"固定样本量 N = {n:g}，要求每轴 ≥ {t:g} 个点", "",
             f"{'维度 d':>8} | {'每轴点数 N^(1/d)':>16} | {'所需样本 t^d':>18} | {'缺口倍数':>12}",
             "-" * 74]
    for d in dims:
        pa = per_axis(n, d)
        need = need_samples(d, t)
        gap = need / n
        lines.append(f"{d:>8} | {pa:>16.3f} | {need:>18.3g} | {gap:>12.3g}")
    lines.append("")
    lines.append("高维几何实证（单位立方体，均匀随机点，4000 次）：")
    for d in (2, 8, 74):
        e, nn, emin = edge_stats(d)
        lines.append(f"  d={d:>3}：点到最近边界的平均距离 {e:.4f}（全场最小 {emin:.4f}），"
                     f"120 点互找最近邻的平均距离 {nn:.4f} → 比值 {nn / e if e else float('nan'):.2f}")
    lines.append("")
    lines.append("结论：d 一大，样本数与边界距离同时坍缩，而邻居距离几乎不变 —— "
                 "「数据永远在边缘」不是比喻，是算术。")
    return "\n".join(lines)


def selftest() -> int:
    ok = True
    if abs(per_axis(1000, 3) - 10.0) > 1e-9:
        print("FAIL: per_axis(1000,3) 应为 10.0"); ok = False
    if abs(per_axis(1000, 74) - 10 ** (3 / 74)) > 1e-6:
        print("FAIL: per_axis(1000,74) 应约 1.10"); ok = False
    if need_samples(8, 10) != 1e8:
        print("FAIL: need_samples(8,10) 应为 1e8"); ok = False
    if need_samples(1, 10) != 10:
        print("FAIL: need_samples(1,10) 应为 10"); ok = False
    e8, nn8, _ = edge_stats(8)
    if not (0.0 < e8 < 0.5):
        print("FAIL: 8 维边界距离应在 (0,0.5)"); ok = False
    print("selftest:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=float, default=1000)
    ap.add_argument("--dims", default="1,3,8,74,100")
    ap.add_argument("--t", type=float, default=10)
    a = ap.parse_args()
    print(report(a.n, [int(x) for x in a.dims.split(",")], a.t))
    print()
    raise SystemExit(selftest())
