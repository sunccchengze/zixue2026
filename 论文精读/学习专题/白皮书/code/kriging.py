#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
kriging.py —— 最小可用 Kriging（高斯相关 + 常数趋势 + θ 的极大似然）
============================================================================
逐行对应论文 §3.1.4 的式 (11)–(18)：
  式 (11)  Y(x) = β f(x) + σ² Z                  常数趋势 ⇒ f(x) = 1
  式 (13)  μ(x′) = fᵀβ + r(x)ᵀ R⁻¹ (y − Fβ)
  式 (14)  σ²(x′) = σ²(1 − rᵀR⁻¹r + uᵀ(FᵀR⁻¹F)⁻¹u)
  式 (15)  β = (FᵀR⁻¹F)⁻¹ FᵀR⁻¹ y
  式 (17)  R(x,x′) = exp(−Σᵢ ((xᵢ−x′ᵢ)/θᵢ)²)
  式 (18)  θ̂ = argmin ½log det R + (N/2)log σ̂²

只用标准库：自己实现 Cholesky 解与 log det。教学实现，别拿去跑 1000 点。

用法： python3 code/kriging.py
"""
from __future__ import annotations

import math
from typing import Iterable, Sequence


# ------------------------------------------------------------------ 线代小工具
def solve(A: list[list[float]], b: list[float]) -> list[float]:
    """高斯消元（部分主元），A 非奇异。返回 x 使 Ax=b。"""
    n = len(A)
    M = [row[:] + [b[i]] for i, row in enumerate(A)]
    for c in range(n):
        piv = max(range(c, n), key=lambda r: abs(M[r][c]))
        if abs(M[piv][c]) < 1e-14:
            M[c][c] += 1e-12                     # 加微抖动，防奇异
            piv = c
        M[c], M[piv] = M[piv], M[c]
        pv = M[c][c]
        for r in range(c + 1, n):
            f = M[r][c] / pv
            if f:
                for k in range(c, n + 1):
                    M[r][k] -= f * M[c][k]
    x = [0.0] * n
    for r in range(n - 1, -1, -1):
        x[r] = (M[r][n] - sum(M[r][k] * x[k] for k in range(r + 1, n))) / M[r][r]
    return x


def solve_many(A: list[list[float]], B: list[list[float]]) -> list[list[float]]:
    return [solve(A, col) for col in zip(*B)]


def logdet_spd(A: list[list[float]]) -> float:
    """对称正定矩阵的 log det，用 Cholesky；失败则退回 LU 对角。"""
    n = len(A)
    L = [[0.0] * n for _ in range(n)]
    try:
        for i in range(n):
            for j in range(i + 1):
                s = A[i][j] - sum(L[i][k] * L[j][k] for k in range(j))
                L[i][j] = math.sqrt(max(s, 1e-16)) if i == j else s / L[j][j]
        return 2.0 * sum(math.log(L[i][i]) for i in range(n))
    except (ValueError, ZeroDivisionError):
        M = [r[:] for r in A]
        ld = 0.0
        for c in range(n):
            piv = max(range(c, n), key=lambda r: abs(M[r][c]))
            M[c], M[piv] = M[piv], M[c]
            ld += math.log(abs(M[c][c]) + 1e-300)
            for r in range(c + 1, n):
                f = M[r][c] / M[c][c]
                for k in range(c, n):
                    M[r][k] -= f * M[c][k]
        return ld


# ------------------------------------------------------------------- 模型本体
class Kriging:
    def __init__(self, theta_grid: Iterable[float] = (0.05, 0.1, 0.2, 0.4, 0.8, 1.6, 3.2, 6.4, 12.8),
                 nugget: float = 1e-8):
        self.theta_grid = list(theta_grid)
        self.nugget = nugget

    @staticmethod
    def corr(a: Sequence[float], b: Sequence[float], th: Sequence[float]) -> float:
        s = sum(((ai - bi) / ti) ** 2 for ai, bi, ti in zip(a, b, th))
        return math.exp(-s)

    def _mat(self, X, th):
        n = len(X)
        return [[self.corr(X[i], X[j], th) + (self.nugget if i == j else 0.0)
                 for j in range(n)] for i in range(n)]

    def fit(self, X: list[list[float]], y: list[float]):
        """网格搜索 θ（式 18），对每个候选 θ 解 β 与 σ²（式 15）。"""
        n, d = len(X), len(X[0])
        one = [1.0] * n
        best = None
        for th0 in self.theta_grid:
            th = [th0] * d
            R = self._mat(X, th)
            Ri_y = solve(R, y)
            Ri_1 = solve(R, one)
            beta = sum(one[i] * Ri_y[i] for i in range(n)) / sum(one[i] * Ri_1[i] for i in range(n))
            resid = [y[i] - beta for i in range(n)]
            Ri_r = solve(R, resid)
            s2 = max(sum(resid[i] * Ri_r[i] for i in range(n)) / n, 1e-14)
            ld = logdet_spd(R)
            nll = 0.5 * ld + 0.5 * n * math.log(s2)                       # 式 (18)，略去常数
            if best is None or nll < best[0]:
                best = (nll, th, beta, s2)
        self.X, self.y, self.theta = X, y, best[1]
        self.nll, self.beta, self.s2 = best[0], best[2], best[3]
        self.R = lambda: self._mat(self.X, self.theta)
        self.Ri_y = solve(self.R(), [y[i] - self.beta for i in range(n)])
        return self

    def predict(self, xq: Sequence[float]):
        """返回 (μ(x′), σ(x′))，对应式 (13) 与式 (14)（常数趋势下 F 全 1）。"""
        n = len(self.X)
        R = self.R()
        one = [1.0] * n
        r = [self.corr(self.X[i], xq, self.theta) for i in range(n)]
        Ri_r = solve(R, r)
        mu = self.beta + sum(r[i] * self.Ri_y[i] for i in range(n))       # 式 (13)
        quad = sum(r[i] * Ri_r[i] for i in range(n))
        Ri_1 = solve(R, one)
        u = sum(Ri_1[i] * r[i] for i in range(n)) - 1.0                   # 式 (16)
        Fu = sum(one[i] * Ri_1[i] for i in range(n))                     # FᵀR⁻¹F
        var = self.s2 * max(1.0 - quad + u * u / Fu, 0.0)                # 式 (14)
        return mu, math.sqrt(var)


def demo() -> int:
    X = [[float(i)] for i in range(6)]
    y = [x * math.sin(x) for x in range(6)]
    m = Kriging().fit(X, y)
    print(f"θ̂ = {m.theta[0]:.3f}   nll = {m.nll:.4f}   β = {m.beta:.4f}   σ² = {m.s2:.5f}")
    print("查询点      μ(x)      σ(x)      真值")
    worst_mean = 0.0
    for q in range(6):
        mu, sd = m.predict([float(q)])
        err = abs(mu - y[q])
        worst_mean = max(worst_mean, err)
        print(f"x={q:<3}    {mu:>8.4f}  {sd:>8.5f}   {y[q]:>8.4f}")
    for q in (2.5, 4.5, 9.0):
        mu, sd = m.predict([q])
        print(f"x={q:<3}    {mu:>8.4f}  {sd:>8.5f}   {q * math.sin(q):>8.4f}")
    # 自检：训练点处应当"插值"（误差小）且 σ 很小；范围外 σ 必须明显更大
    s_in = m.predict([9.0])[1] / max(m.predict([2.5])[1], 1e-12)
    ok = worst_mean < 1e-2 and s_in > 1.05
    print("\n自检：训练点插值误差 < 1e-2 ⇒", worst_mean < 1e-2)
    print("自检：域外 σ / 域内 σ > 1.05 ⇒", round(s_in, 2), s_in > 1.05)
    print("selftest:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(demo())
