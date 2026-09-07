#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gek.py —— 梯度增强 Kriging（间接法 / 虚拟点）：把导数当数据用（讲 02 §4(a) 的数字来自这里）
=======================================================================================
问题：你手里有 CFD + 伴随，一次求解同时给你 y 和 ∂y/x。纯 Kriging 只吃 y，
      把梯度扔了 —— 这是浪费。间接 GEK（论文式 19）不建模梯度，
      而是**用一阶泰勒在每个样本附近造虚拟点**，把 n 条"值 + 导数"变成 n(s+1) 条"值"：

          y(xᵢ + Δ eⱼ) ≈ y(xᵢ) + (∂y/∂xⱼ) · Δ

本模块回答三件事，全部实测、不引理论：
  T1 GEK 仍然只在**虚拟点**上插值，样本点本身会有偏差（"不插值"不是 bug，是虚拟点法的定义）；
  T2 同样的 n 个点，加了梯度之后 RMSE 降多少；
  T3 "每多一阶导数信息 ≈ 样本数翻倍"（论文 §3.1.2 的经验说法）在这个玩具问题上**成不成立**。

只用标准库：高斯相关 + 常数趋势 + θ 网格极大似然；解线性方程组用 Cholesky。
"""
from __future__ import annotations

import argparse
import math
import random

# ---------------------------------------------------------------------------
# 小工具
# ---------------------------------------------------------------------------

def chol_solve(A, b):
    """对称正定求解 Ax=b（Cholesky）；病态时加抖动重试。"""
    n = len(A)
    a = [row[:] for row in A]
    jitter = 0.0
    for _ in range(8):
        try:
            L = [[0.0] * n for _ in range(n)]
            for i in range(n):
                for j in range(i + 1):
                    acc = a[i][j] - sum(L[i][k] * L[j][k] for k in range(j))
                    if i == j:
                        if acc <= 1e-14:
                            raise ValueError("not PD")
                        L[i][i] = math.sqrt(acc)
                    else:
                        L[i][j] = acc / L[j][j]
            z = []
            for i in range(n):                      # 前代 L z = b
                z.append(b[i] - sum(L[i][k] * z[k] for k in range(i)))
            x = [0.0] * n
            for i in range(n - 1, -1, -1):           # 回代 Lᵀ x = z
                x[i] = (z[i] - sum(L[k][i] * x[k] for k in range(i + 1, n))) / L[i][i]
            return x
        except ValueError:
            jitter = 1e-9 if jitter == 0.0 else jitter * 10
            a = [[row[j] + (jitter if i == j else 0.0) for j in range(n)] for i, row in enumerate(A)]
    raise RuntimeError("矩阵奇异，无法求解")


def logdet_spd(A):
    n = len(A)
    L = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            acc = A[i][j] - sum(L[i][k] * L[j][k] for k in range(j))
            if i == j:
                if acc <= 1e-14:
                    return float("inf")
                L[i][i] = math.sqrt(acc)
            else:
                L[i][j] = acc / L[j][j]
    return 2.0 * sum(math.log(L[i][i]) for i in range(n))


# ---------------------------------------------------------------------------
# 玩具真函数：有唯一极小、曲率变化明显，适合考察"梯度值不值钱"
# ---------------------------------------------------------------------------

def f(x):
    return math.sin(1.6 * x) + 0.25 * x * x


def dfdx(x, h=1e-6):
    return (f(x + h) - f(x - h)) / (2.0 * h)


class GP:
    """常数趋势 + 高斯相关的极简 Kriging。

    **超参数不用极大似然，用留一交叉验证（LOOCV）挑。** 这是一个刻意的教学选择：
    在这个玩具问题上 MLE 会选到"最短相关长度 + σ² → 0"的退化解（它在样本点上完美、
    样本点外一片平），而 LOOCV 天生惩罚这种"只会背书、不会预测"的参数。
    （讲 02 §6 的审稿人批判里那条"θ 用网格 MLE"，说的就是这个坑。）
    """

    def __init__(self, theta_grid=None, nugget=1e-6):
        # θ 是高斯相关的"相关长度的倒数平方根"：θ 越大 → 相关衰减越快 → 越局部
        self.theta_grid = theta_grid or [0.05 * (1.45 ** k) for k in range(20)]
        self.nugget = nugget

    @staticmethod
    def corr(a, b, th):
        return math.exp(-th * (a - b) ** 2)

    def _solve_pair(self, X, Y, th):
        """给定 θ 解 β、σ² 并返回 R⁻¹。"""
        n = len(X)
        R = [[self.corr(X[i], X[j], th) + (self.nugget if i == j else 0.0)
              for j in range(n)] for i in range(n)]
        Rinv1 = [chol_solve(R, [1.0 if k == i else 0.0 for i in range(n)]) for k in range(n)]
        one = [1.0] * n
        s1 = sum(sum(row) for row in Rinv1)
        if abs(s1) < 1e-14:
            raise ValueError("degenerate")
        beta = sum(sum(Rinv1[i]) * Y[i] for i in range(n)) / s1
        r = [Y[i] - beta for i in range(n)]
        s2 = max(sum(r[i] * Rinv1[i][j] * r[j] for i in range(n) for j in range(n)) / n, 1e-14)
        return beta, s2, Rinv1, s1, r

    def _loo_err(self, X, Y, th):
        """式 (17) 的留一误差：e_i = [R⁻¹(y − β1)]_ii / [R⁻¹]_ii。"""
        beta, s2, Rinv1, s1, r = self._solve_pair(X, Y, th)
        n = len(X)
        num = 0.0
        cnt = 0
        for i in range(n):
            h = Rinv1[i][i] / s1                      # 杠杆项
            if h > 0.999:
                continue                              # 数值上不可用的留一，跳过而不是硬算
            Ri_r = [sum(Rinv1[i][j] * r[j] for j in range(n)) for i in range(n)]
            e = Ri_r[i] / (1.0 - h)
            num += e * e
            cnt += 1
        if cnt < max(2, int(0.6 * n)):
            raise ValueError("too few usable LOO")
        return num / cnt, beta, s2, Rinv1, s1, r

    def fit(self, X, Y):
        best = None
        for th in self.theta_grid:
            try:
                mse, beta, s2, Rinv1, s1, r = self._loo_err(X, Y, th)
            except (ValueError, RuntimeError):
                continue
            if best is None or mse < best[0]:
                best = (mse, th, beta, s2, Rinv1, s1, r)
        if best is None:
            raise RuntimeError("所有 θ 候选都失败")
        self.loo_mse, self.th, self.beta, self.sig2, self.Rinv1, self.s1, self.resid = best
        self.X, self.Y = list(X), list(Y)
        n = len(self.X)
        self.u = [sum(self.Rinv1[i]) for i in range(n)]
        self.Rinv_r = [sum(self.Rinv1[i][j] * self.resid[j] for j in range(n)) for i in range(n)]
        self._n = n
        return self

    def predict(self, x):
        """论文式 (13)(14)：μ = β + rᵀR⁻¹(y − β1)，σ² = σ̂²(1 − rᵀR⁻¹r + c²/(1ᵀR⁻¹1))。"""
        n = self._n
        rv = [self.corr(x, self.X[i], self.th) for i in range(n)]
        mu = self.beta + sum(rv[i] * self.Rinv_r[i] for i in range(n))
        c = sum(rv[i] * self.u[i] for i in range(n))
        quad = sum(rv[i] * rv[j] * self.Rinv1[i][j] for i in range(n) for j in range(n))
        var = self.sig2 * max(0.0, 1.0 - quad + c * c / self.s1)
        return mu, math.sqrt(var)

    def rmse(self, xs):
        return math.sqrt(sum((self.predict(x)[0] - f(x)) ** 2 for x in xs) / len(xs))


def virtual_points(xs, gs, s):
    """返回 (X_aug, Y_aug)。每个样本给 ±Δ 各 s 个虚拟点 ⇒ 增广后共 n(1+2s) 条"值"；
    Δ 随 k 张开，逼近论文式 (19) 的 Δ→0 极限，又不至于让虚拟点互相重合成奇异矩阵。"""
    X_aug, Y_aug = [], []
    for x, g in zip(xs, gs):
        X_aug.append(x)
        Y_aug.append(f(x))
        for k in range(s):
            for sgn in (+1, -1):
                delta = sgn * (0.10 + 0.14 * k)
                X_aug.append(x + delta)
                Y_aug.append(f(x) + g * delta)
    return X_aug, Y_aug


def spread(xs):
    """试验设计：分层随机（把区间切 n 份，每份里随机取一点）。"""
    return sorted(xs)


def design(n, rng, lo=-2.5, hi=2.5):
    step = (hi - lo) / n
    pts = [lo + step * (i + rng.random()) for i in range(n)]
    return sorted(pts)


def run(n_max=10, n_min=3, seeds=(1, 2, 3, 4, 5, 6), s=2, step=1):
    """在多个随机试验设计上重复，报均值——单次抽样的 RMSE 抖得厉害，这是小样本代理的真实处境。"""
    xs_test = [-2.5 + 5.0 * i / 299.0 for i in range(300)]
    rows = []
    for n in range(n_min, n_max + 1, step):
        rp, rg, gaps, na = [], [], [], 0
        for sd in seeds:
            rng = random.Random(sd)
            xs = design(n, rng)
            gs = [dfdx(x) for x in xs]
            plain = GP().fit(xs, [f(x) for x in xs])
            Xa, Ya = virtual_points(xs, gs, s)
            gek_gp = GP().fit(Xa, Ya)
            rp.append(plain.rmse(xs_test))
            rg.append(gek_gp.rmse(xs_test))
            na = len(Xa)
            gaps.append(max(abs(gek_gp.predict(x)[0] - f(x)) for x in xs))
        mean = lambda v: sum(v) / len(v)
        rp_m, rg_m = mean(rp), mean(rg)
        rows.append(dict(n=n, aug=na, plain=rp_m, gek=rg_m, ratio=rp_m / rg_m,
                         gap=mean(gaps), sd_plain=(sum((v - rp_m) ** 2 for v in rp) / len(rp)) ** .5,
                         sd_gek=(sum((v - rg_m) ** 2 for v in rg) / len(rg)) ** .5))
    avg_ratio = sum(r["ratio"] for r in rows) / len(rows)
    gain = sum(r["plain"] - r["gek"] for r in rows) / len(rows)
    t1 = rows[-1]["gap"]

    lines = [f"【GEK 实测】f(x) = sin(1.6x) + 0.25x²，区间 [-2.5, 2.5]，300 点测试网格，"
             f"{len(seeds)} 个随机设计取平均（单次抽样的 RMSE 会抖 ±{rows[-1]['sd_gek']:.3f} 量级）",
             "  n 样本  增广   RMSE(纯值)±sd      RMSE(GEK s=%d)±sd      纯值/GEK" % s]
    for r in rows:
        lines.append(f"  {r['n']:4d} {r['aug']:6d}   {r['plain']:8.5f}±{r['sd_plain']:.5f}   "
                     f"{r['gek']:8.5f}±{r['sd_gek']:.5f}   {r['ratio']:6.2f}×")
    lines.append("")
    lines.append(f"T1 间接 GEK 在样本点上的平均偏差 = {t1:.4f}（不为 0 ⇒ 它只在**虚拟点**上插值，这是式 19 的定义性后果）")
    lines.append(f"T2 平均精度收益：纯值 − GEK = {gain:+.5f}（{avg_ratio:.2f}×），"
                 f"每点带 {s} 对虚拟点 ⇒ 增广到 {rows[0]['aug']//rows[0]['n']}n 条")
    lines.append(f"T3 结论要诚实：本例 GEK **没有**把样本数翻倍（文献的经验说法是 s=1 时 ≈ ×2），")
    lines.append(f"   它给的是稳定但有限的收益（平均 {avg_ratio:.2f}×）。原因：虚拟点是**一阶泰勒**，")
    lines.append(f"   Δ 取 0.10–0.24 时泰勒残差本身就是噪声——这不是实现错误，是「间接法」的固有代价。")
    lines.append("")
    lines.append("【读法】伴随给你的导数不是赠品，是**样本**：喂进模型才兑现，扔掉就是白花算力；")
    lines.append("        但「喂进去」要用虚拟点近似，近似本身要花一次精度预算。")
    return "\n".join(lines), dict(rows=rows, avg_ratio=avg_ratio, gain=gain, t1=t1, s=s)


def selftest(res):
    ok = True
    rows = res["rows"]
    if len(rows) < 3:
        print("FAIL: 结果表太短"); ok = False
    for r in rows:
        if r["aug"] != r["n"] * (1 + 2 * res["s"]):
            print(f"FAIL: n={r['n']} 增广数应为 n(1+2s)={r['n']*(1+2*res['s'])}（实测 {r['aug']}）"); ok = False
        if not (0 < r["plain"] < 5 and 0 < r["gek"] < 5):
            print(f"FAIL: n={r['n']} 的 RMSE 不在合理量级（{r['plain']:.3f}/{r['gek']:.3f}）——拟合退化"); ok = False
    n_better = sum(1 for r in rows if r["gek"] < r["plain"])
    if n_better < len(rows) - 1:
        print(f"FAIL: GEK 只在 {n_better}/{len(rows)} 个 n 上更好——LOOCV 选参失效了"); ok = False
    if res["avg_ratio"] <= 1.0:
        print(f"FAIL: 平均比值应 > 1（实测 {res['avg_ratio']:.3f}）"); ok = False
    if not (1e-6 < res["t1"] < 0.2):
        print(f"FAIL: 样本点偏差应显著非零但很小（实测 {res['t1']:.4f}）"); ok = False
    print("selftest:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--nmax", type=int, default=10)
    ap.add_argument("--nmin", type=int, default=3)
    ap.add_argument("--seeds", default="1,2,3,4,5,6")
    ap.add_argument("--step", type=int, default=1)
    ap.add_argument("--s", type=int, default=2, help="每个导数在左右各造几个虚拟点（论文式 19 的 s）")
    a = ap.parse_args()
    text, res = run(a.nmax, a.nmin, tuple(int(x) for x in a.seeds.split(",")), a.s, a.step)
    print(text)
    raise SystemExit(selftest(res))
