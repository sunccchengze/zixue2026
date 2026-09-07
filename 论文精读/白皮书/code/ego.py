#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ego.py —— 加点准则（EI / LCB / UCB）与序贯全局优化（讲 02 §3(e)、讲 09 §3(a) 的实盘）
============================================================================
三条准则，全部只依赖代理模型给出的 (μ, σ) 与当前最优 ξ：

  EI(x) = (ξ − μ)·Φ(z) + σ·φ(z)，  z = (ξ − μ)/σ     （最大化"期望改善"，最小化问题）
  LCB(x) = μ(x) − κ·σ(x)                             （乐观地看下界；论文 §4.3.1 提到"最小化置信下界"这一族准则）
  UCB(x) = μ(x) + κ·σ(x)                             （最大化时用；这里只给对照）

三件必须亲眼看见的事（本模块的自检就是把它们跑出来）：
  T1 手算例：μ/σ 已知时 EI 的数值（讲 02 §3(e) 那两个点，误差 < 0.02）
  T2 数值病：z ≪ −40 时 φ(z) 下溢 ⇒ EI ≡ 0 ⇒ 序贯优化僵住（讲 02 讲的"z 的两个极端"的算术版本）
  T3 端到端：在可手算的二次函数上跑 12 步 EGO，20 次昂贵评估内逼近真最优

只用标准库（numpy 都不需要）。用法：
    python3 code/ego.py                    # 三项自检 + 端到端 EGO
    python3 code/ego.py --demo-ei          # 只跑 T1
    python3 code/ego.py --criterion lcb    # 端到端换 LCB（默认 ei）
"""
from __future__ import annotations

import argparse
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kriging import Kriging  # noqa: E402


def Phi(z: float) -> float:
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))


def phi(z: float) -> float:
    return math.exp(-0.5 * z * z) / math.sqrt(2.0 * math.pi)


def ei_min(mu: float, sd: float, xi: float) -> tuple[float, float]:
    """返回 (EI, z)。最小化问题专用；σ→0 时 EI→0（已采样点没有信息量）。"""
    if sd <= 1e-12:
        return 0.0, float("inf")
    z = (xi - mu) / sd
    return (xi - mu) * Phi(z) + sd * phi(z), z


def lcb(mu: float, sd: float, kappa: float = 1.96) -> float:
    return mu - kappa * sd


def ucb(mu: float, sd: float, kappa: float = 1.96) -> float:
    return mu + kappa * sd


# ---------------------------------------------------------------- T1 / T2 自检
def demo_ei(verbose: bool = True) -> tuple[bool, float, float]:
    rows = [(0.90, 0.10, "A"), (1.10, 0.60, "B")]
    vals, ok = [], True
    if verbose:
        print("T1 讲 02 手算例复算（最小化，ξ = 1.00）")
        print(f"{'点':>4} {'μ':>6} {'σ':>6} {'z':>8} {'EI':>8}  类型")
    for mu, sd, tag in rows:
        v, z = ei_min(mu, sd, 1.00)
        vals.append(v)
        if verbose:
            print(f"{tag:>4} {mu:>6.2f} {sd:>6.2f} {z:>8.4f} {v:>8.4f}  "
                  + ("偏开发(z>0)" if z > 0 else "偏探索(z≤0)"))
    ok &= vals[1] > vals[0] and abs(vals[0] - 0.108) < 0.01 and abs(vals[1] - 0.185) < 0.02
    if verbose:
        print("    ⇒ 预测更差的 B 反而 EI 更大：σ 是「万一更好」的期权费。")
        print("T2 数值病演示（z ≪ 0 时 φ 下溢）")
        for z in (-3.0, -10.0, -38.0, -40.0):
            v, _ = ei_min(0.0, 1.0, z)
            print(f"    z = {z:>6.1f} → EI = {v:.3e}（φ(z) = {phi(z):.3e}）")
        v40, _ = ei_min(0.0, 1.0, -40.0)
        print("    ⇒ z ≤ −40 时 EI 数值上等于 0，序贯优化会僵在「没信息可算」的地方。")
    return ok, vals[0], vals[1]


# ------------------------------------------------------------------ T3 端到端
def stratified(n: int, lo: float, hi: float, seed: int = 20260907) -> list[float]:
    rng = random.Random(seed)
    strata = n * 4
    return [lo + (hi - lo) * (i + 0.5) / strata for i in sorted(rng.sample(range(strata), n))]


def sequential(f, lo: float, hi: float, steps: int = 12, n_grid: int = 800,
               n_init: int = 6, criterion: str = "ei", kappa: float = 1.96):
    xs = stratified(n_init, lo, hi)
    ys = [f(x) for x in xs]
    hist, dead = [], 0
    for _ in range(steps):
        m = Kriging(theta_grid=(0.1, 0.25, 0.5, 1.0, 2.0, 4.0, 8.0, 16.0, 32.0),
                    ).fit([[x] for x in xs], ys)
        xi = min(ys)
        scored = []
        for g in range(n_grid):
            x = lo + (hi - lo) * g / (n_grid - 1)
            mu, sd = m.predict([x])
            if sd <= 1e-6:                      # 已采样点：σ≈0 ⇒ 白烧一次昂贵评估，标准做法是排除
                continue
            v, z = ei_min(mu, sd, xi)
            score = v if criterion == "ei" else lcb(mu, sd, kappa)
            scored.append((score, x, z, v, sd))
        if not scored:
            break
        if criterion == "ei" and max(t[0] for t in scored) <= 1e-12:
            dead += 1
        best = max(scored) if criterion == "ei" else min(scored)
        _, x_new, z_new, v_new, sd_new = best
        xs.append(x_new)
        ys.append(f(x_new))
        hist.append((len(hist) + 1, x_new, ys[-1], z_new, v_new, sd_new, min(ys)))
    return hist, dead


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--steps", type=int, default=12)
    ap.add_argument("--criterion", choices=["ei", "lcb"], default="ei")
    ap.add_argument("--kappa", type=float, default=1.96)
    ap.add_argument("--demo-ei", action="store_true")
    a = ap.parse_args()

    ok, vA, vB = demo_ei(verbose=True)
    if a.demo_ei:
        print("selftest:", "PASS" if ok else "FAIL")
        return 0 if ok else 1

    # T3：可手算的二次函数（讲 02/09 的"能当场验"原则）
    f = lambda x: (x - 4.0) ** 2 - 1.0          # noqa: E731  真最优 x*=4.0, f*=−1.0
    print(f"\nT3 端到端 EGO：min (x−4)² − 1 on [0, 10]，真最优 f* = −1.0（x* = 4.0）")
    print(f"准则 {a.criterion.upper()}" + (f"（κ = {a.kappa}）" if a.criterion == "lcb" else "")
          + f"；初点 6 个（分层随机）；步数 {a.steps} ⇒ 昂贵评估共 {a.steps + 6} 次")
    hist, dead = sequential(f, 0.0, 10.0, steps=a.steps, criterion=a.criterion, kappa=a.kappa)
    print(f"{'步':>3} {'新点 x':>8} {'f(x)':>9} {'z':>9} {'打分 EI':>9} {'σ':>7} {'当前最优':>9}")
    for it, x, y, z, v, sd, cur in hist:
        zs = f"{z:>9.3f}" if math.isfinite(z) else f"{'inf':>9}"
        print(f"{it:>3} {x:>8.4f} {y:>9.4f} {zs} {v:>9.4f} {sd:>7.4f} {cur:>9.4f}")
    err = abs(hist[-1][6] + 1.0)
    print(f"\n|x̂ − x*| = {abs(hist[-1][1] - 4.0) if err < 0.5 else float('nan'):.4f}"
          f"；f 误差 = {err:.4f}；EI 僵住步数 = {dead}/{len(hist)}")
    print("读法：EI 连续为 0（见 T2）时换 LCB 立刻能动 —— 这就是论文 §4.3.1 里"
          "「最大化 EI」与「最小化置信下界」两族准则并存的工程理由。")
    ok = ok and err < 0.05
    print("selftest:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
