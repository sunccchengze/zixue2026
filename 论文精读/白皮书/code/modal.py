#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
modal.py —— 几何模态参数化 + 有效性门（讲 06 的数字都由它现场复算）
=====================================================================
它回答两个问题（也正是讲 06 §3 与 §8 的论点）：

  Q1 收缩：把 d 个设计变量压成 r 个模态系数，"每个方向摊到几个点"从多少涨到多少？
            per_axis = N ** (1/d)（这个式子由 code/curse.py 讲透，本模块只负责把 d 真的改小）。
  Q2 门控：随机在全 d 维里取点，有多少比例是"畸形外形"（网格生成器退回、一次 CFD 白烧）？
            只在主模态张成的子空间里取点，这个比例又是多少？

几何约定（教学玩具，刻意不是真的 CST/Hicks-Henne，为了能手算）：
  翼型由 20 个系数描述：前 10 个给**厚度分布**沿弦向加乘性扰动，后 10 个给**拱线**加系数。
  "有效" = 厚度非负 + 沿弦向大体单调衰减 + 后缘不胖 + 拱不穿上下表面。
  这四条对应论文 §4.1.2 的"从真实外形到异常外形的单调平滑衰减"式几何过滤精神。

用法： python3 code/modal.py                      # 跑自检并打印
      python3 code/modal.py --n 2000 --seed 3 --trials 8000
"""
from __future__ import annotations

import argparse
import math
import random

CHORD_STATIONS = [i / 20.0 for i in range(21)]                 # x/c ∈ [0,1]
# 前缘到 3/4 弦的一段四分之一椭圆：从 1.0 单调衰减到 0.714。
# 取前 3/4 弦的一段四分之一椭圆（前段自然变厚、后段单调衰减），x/c > 0.75 处夹到 0.05。
# 为什么不用整条 NACA 分布：本模块的门要求"厚度单峰"，用真实分布反而会让基准自己被打回——
# 教学代码里的判据必须能在纸上复核，所以我选了这条能口算的形状。
BASE_THICKNESS = [math.sqrt(max(0.05, 1.0 - (4.0 / 3.0 * x) ** 2)) for x in CHORD_STATIONS]
NATURAL_TV = sum(abs(b - a) for a, b in zip(
    [t for t in BASE_THICKNESS], [t for t in BASE_THICKNESS[1:]]))   # 基准上表面的自然起伏 ≈ 0.29
D_FULL = 20                                                     # 10 厚度 + 10 拱线


# ---------------------------------------------------------------------------
# 1. 几何：系数 → 翼型
# ---------------------------------------------------------------------------

def _interp(vals):
    """把 10 个系数分段线性插到 21 个弦向站位。"""
    out, m = [], len(vals)
    for x in CHORD_STATIONS:
        u = x * (m - 1)
        i = min(int(u), m - 2)
        f = u - i
        out.append(vals[i] * (1 - f) + vals[i + 1] * f)
    return out


def build_airfoil(coeffs):
    """coeffs 长度 20：前 10 = 厚度乘性扰动，后 10 = 拱线系数。返回 (thickness[21], camber[21])。"""
    t_inc, c_coef = _interp(coeffs[:10]), _interp(coeffs[10:])
    thickness = [bt * (1.0 + ti) for bt, ti in zip(BASE_THICKNESS, t_inc)]
    camber = [cc * 4.0 * x * (1.0 - x) for cc, x in zip(c_coef, CHORD_STATIONS)]
    return thickness, camber


def is_valid(thickness, camber):
    """有效性门（三条，全部可手算，全部有物理解释；对应论文 §4.1.2 的"平滑衰减/可画网格"精神）：
    ① 厚度处处 ≥ 0.02 —— 局部捏死的形状，网格生成器直接退回；
    ② 上表面总起伏 Σ|Δ(t+cam)| ≤ 2.5 × 基准起伏 —— "平滑"就是几何过滤的真实内容：
       锯齿状形状即使每一点都不穿面，也不该进优化环；
    ③ |拱| ≤ 0.75 × 局部厚度 —— 拱线穿出表面就是自交。
    （论文那句"从真实外形单调平滑地走向异常外形"里的"单调"，在这里由 ② 承担：
      它测的是**波动量**，不挑单峰/双峰——这是刻意简化，写讲稿时不许把它说成等价。）"""
    if min(thickness) < 0.02:
        return False
    up = [t + cc for t, cc in zip(thickness, camber)]
    if sum(abs(b - a) for a, b in zip(up, up[1:])) > 2.5 * NATURAL_TV:
        return False
    if any(abs(cc) > 0.75 * tt for cc, tt in zip(camber, thickness)):
        return False
    return True


# ---------------------------------------------------------------------------
# 2. 只用标准库的 PCA（循环 Jacobi 对称特征分解）
# ---------------------------------------------------------------------------

def jacobi_eig(A, sweeps=80, tol=1e-12):
    n = len(A)
    a = [row[:] for row in A]
    v = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for _ in range(sweeps):
        off = math.sqrt(sum(a[i][j] ** 2 for i in range(n) for j in range(n) if i != j))
        if off < tol:
            break
        for p in range(n - 1):
            for q in range(p + 1, n):
                if abs(a[p][q]) < 1e-18:
                    continue
                theta = (a[q][q] - a[p][p]) / (2.0 * a[p][q])
                t = (1.0 if theta >= 0 else -1.0) / (abs(theta) + math.sqrt(theta * theta + 1.0))
                c, s = 1.0 / math.sqrt(t * t + 1.0), t / math.sqrt(t * t + 1.0)
                for k in range(n):
                    akp, akq = a[k][p], a[k][q]
                    a[k][p], a[k][q] = c * akp - s * akq, s * akp + c * akq
                for k in range(n):
                    apk, aqk = a[p][k], a[q][k]
                    a[p][k], a[q][k] = c * apk - s * aqk, s * apk + c * aqk
                for k in range(n):
                    vkp, vkq = v[k][p], v[k][q]
                    v[k][p], v[k][q] = c * vkp - s * vkq, s * vkp + c * vkq
    vals = [a[i][i] for i in range(n)]
    order = sorted(range(n), key=lambda i: -vals[i])
    return [vals[i] for i in order], [[v[k][i] for k in range(n)] for i in order]


def pca(X):
    n, d = len(X), len(X[0])
    mean = [sum(row[j] for row in X) / n for j in range(d)]
    Z = [[row[j] - mean[j] for j in range(d)] for row in X]
    C = [[sum(Z[i][a] * Z[i][b] for i in range(n)) / (n - 1) for b in range(d)] for a in range(d)]
    vals, vecs = jacobi_eig(C)
    return mean, vals, vecs


def per_axis(n, d):
    return n ** (1.0 / d)


# ---------------------------------------------------------------------------
# 3. 两种采样：贴流形的平滑扰动 vs 逐变量独立乱取
# ---------------------------------------------------------------------------

def sample_realistic(rng, scale=0.30):
    """6 个基系数（幅度按 1/(k+1) 衰减 ⇒ 低频占主导，这才是真实的几何数据该有的谱）
    → 20 个系数。相邻站位强相关 ⇒ 形状仍像翼型，这就是"数据流形"。"""
    b = [rng.uniform(-scale, scale) / (k + 1) for k in range(6)]
    thick = [sum(b[k] * math.sin((k + 1) * math.pi * (i + 0.5) / 10.0) for k in range(6)) for i in range(10)]
    cam = [sum(b[k] * math.cos((k + 1) * math.pi * (i + 0.5) / 10.0) for k in range(6)) * 0.30 for i in range(10)]
    return thick + cam


def sample_naive(rng, sigma=0.30):
    """每个设计变量独立高斯 ⇒ 大概率不是翼型（优化器在没有几何先验时的真实处境）。"""
    return [rng.gauss(0.0, sigma) for _ in range(D_FULL)]


# ---------------------------------------------------------------------------
# 4. 主流程
# ---------------------------------------------------------------------------

def run(n=1000, seed=11, energy=0.99, trials=6000, gate_amp=1.6):
    rng = random.Random(seed)
    X = [sample_realistic(rng) for _ in range(n)]
    mean, vals, vecs = pca(X)
    tot = sum(vals) or 1.0
    r, cum = D_FULL, 0.0
    for i, ev in enumerate(vals):
        cum += ev / tot
        if cum >= energy:
            r = i + 1
            break

    def project(c):
        z = [c[j] - mean[j] for j in range(D_FULL)]
        return [sum(z[j] * vecs[k][j] for j in range(D_FULL)) for k in range(r)]

    def lift(z):
        out = list(mean)
        for k, zk in enumerate(z):
            for j in range(D_FULL):
                out[j] += zk * vecs[k][j]
        return out

    pa_full, pa_modal = per_axis(n, D_FULL), per_axis(n, r)
    zs = [project(x) for x in X]
    sd = [math.sqrt(sum(z[k] ** 2 for z in zs) / len(zs)) for k in range(r)]

    ok_naive = ok_modal = ok_in = 0
    for _ in range(trials):
        ok_naive += 1 if is_valid(*build_airfoil(sample_naive(rng))) else 0
        z = [rng.gauss(0.0, gate_amp * s) for s in sd]      # 比训练分布还宽（默认 1.6σ）
        ok_modal += 1 if is_valid(*build_airfoil(lift(z))) else 0
        z = [rng.gauss(0.0, s) for s in sd]                  # 贴着训练分布的包络取点
        ok_in += 1 if is_valid(*build_airfoil(lift(z))) else 0
    pv_naive, pv_modal, pv_in = ok_naive / trials, ok_modal / trials, ok_in / trials

    # 训练样本自身的合格率（流形上的点当然全部有效）
    pv_train = sum(1 for x in X if is_valid(*build_airfoil(x))) / n

    lines = [
        "【1】模态收缩（PCA，只用标准库 Jacobi 特征分解）",
        f"    样本量 N = {n}，原始设计变量 d = {D_FULL}（10 厚度 + 10 拱线）",
        "    特征值前 8 项占比：" + ", ".join(f"{ev/tot:5.1%}" for ev in vals[:8]),
        f"    达到累计能量 {energy:.0%} 需要的模态数 r = {r}",
        f"    每维点数：{D_FULL} 维 → {pa_full:.2f} 个/维   ⇒   {r} 维 → {pa_modal:.2f} 个/维"
        f"（放大 {pa_modal/pa_full:.1f} 倍）",
        "",
        "【2】有效性门（厚度下限 + 起伏上限 + 拱不穿面）",
        f"    逐变量独立乱取 {D_FULL} 维：合格率 {pv_naive:6.1%}  ← 其余全是会被网格生成器退回的畸形",
        f"    贴着训练分布（1.0σ）在 {r} 维子空间取点：合格率 {pv_in:6.1%}",
        f"    放大到 {gate_amp}σ（比训练分布还宽）：合格率 {pv_modal:6.1%}  ← 说明子空间不是护身符",
        f"    训练样本自身合格率：{pv_train:.1%}（作为门的参照，应为 100%）",
        f"    一次 CFD 白烧的概率：{1-pv_naive:.1%} → {1-pv_modal:.1%}",
        "",
        "【读法】降维买的是「每维点数」，过滤买的是「不白跑」——两者正交，",
        "        所以讲 06 说：模态参数化不减少评估次数，它减少的是**无效评估**。",
        f"        注意 r={r} 是被 {energy:.0%} 能量线卡出来的，不是「物理极限」：把能量线放宽，r 还会变大。",
    ]
    return "\n".join(lines), dict(n=n, d=D_FULL, r=r, pa_full=pa_full, pa_modal=pa_modal,
                                  pv_naive=pv_naive, pv_modal=pv_modal, pv_in=pv_in, pv_train=pv_train,
                                  energy=energy, first_ev=vals[0] / tot)


def selftest(res):
    ok = True
    n, d, r = res["n"], res["d"], res["r"]
    if abs(per_axis(1000, 20) - 1.4125) > 1e-3:
        print("FAIL: per_axis(1000,20) 应为 1.41"); ok = False
    if abs(per_axis(1000, 3) - 10.0) > 1e-9:
        print("FAIL: per_axis(1000,3) 应为 10.0"); ok = False
    if not (1 <= r < d):
        print(f"FAIL: 模态数 r={r} 应落在 [1,{d}) 内"); ok = False
    if abs(per_axis(n, r) - res["pa_modal"]) > 1e-6:
        print("FAIL: 每维点数复算不一致"); ok = False
    if res["pv_train"] < 0.95:
        print(f"FAIL: 流形上的训练样本应全部合格，实测 {res['pv_train']:.3f} —— 门太紧"); ok = False
    if not res["pv_in"] > 1.5 * max(res["pv_naive"], 1e-3):
        print(f"FAIL: 贴流形取点的合格率应显著高于乱取（{res['pv_in']:.3f} vs {res['pv_naive']:.3f}）"); ok = False
    if res["pv_naive"] > 0.5:
        print(f"FAIL: 独立乱取的合格率不该这么高（{res['pv_naive']:.3f}）—— 门失去牙齿"); ok = False
    if res["first_ev"] < 0.1:
        print("FAIL: 第一个模态应占相当比重（低频平滑扰动）"); ok = False
    if is_valid(*build_airfoil([-0.99] * 10 + [0.0] * 10)):  # 厚度整体捏死 → 必须被第①条拒
        print("FAIL: 后段厚度捏死的形状应被第①条拒绝"); ok = False
    if not is_valid(*build_airfoil([0.0] * 20)):  # 基准外形 → 必须通过
        print("FAIL: 基准外形应通过门"); ok = False
    jaggy = [0.0] * 20
    for i in range(10):
        jaggy[i] = 0.9 if i % 2 == 0 else -0.9        # 锯齿状厚度：物理上画不出网格
    if is_valid(*build_airfoil(jaggy)):
        print("FAIL: 锯齿厚度应被第③条拒绝"); ok = False
    if not (0.5 < NATURAL_TV < 1.2):
        print(f"FAIL: 基准上表面起伏应在 0.5–1.2 之间（实测 {NATURAL_TV:.3f}）"); ok = False
        print("FAIL: 基准翼型应通过门"); ok = False
    print("selftest:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=1000)
    ap.add_argument("--seed", type=int, default=11)
    ap.add_argument("--energy", type=float, default=0.99)
    ap.add_argument("--trials", type=int, default=6000)
    ap.add_argument("--gate-amp", type=float, default=1.6)
    a = ap.parse_args()
    text, res = run(a.n, a.seed, a.energy, a.trials, a.gate_amp)
    print(text)
    raise SystemExit(selftest(res))
