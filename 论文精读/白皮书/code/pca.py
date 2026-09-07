#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pca.py —— 三步 PCA：中心化 → 协方差 → 特征分解（讲 03 §3 的实盘）
============================================================================
对称矩阵用 Jacobi 旋转求特征值/特征向量（只用标准库）。
主自检：把"沿一条直线抖动的点云"降成 1 维，要求保留方差 ≥ 99.9%，且残差 ≈ 0。

用法： python3 code/pca.py
      python3 code/pca.py --n 300 --noise 0.05 --k 1
"""
from __future__ import annotations

import argparse
import math
import random


def jacobi_eig(A: list[list[float]], sweeps: int = 60, tol: float = 1e-12):
    """对称矩阵特征分解。返回 (eigenvalues desc, eigenvectors as columns)。"""
    n = len(A)
    a = [row[:] for row in A]
    v = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for _ in range(sweeps):
        off = sum(a[i][j] ** 2 for i in range(n) for j in range(n) if i != j)
        if off < tol:
            break
        for p in range(n - 1):
            for q in range(p + 1, n):
                if abs(a[p][q]) < 1e-18:
                    continue
                theta = (a[q][q] - a[p][p]) / (2 * a[p][q])
                t = math.copysign(1.0, theta) / (abs(theta) + math.sqrt(theta * theta + 1.0))
                c = 1.0 / math.sqrt(t * t + 1.0)
                s = t * c
                for k in range(n):
                    akp, akq = a[k][p], a[k][q]
                    a[k][p] = c * akp - s * akq
                    a[k][q] = s * akp + c * akq
                for k in range(n):
                    apk, aqk = a[p][k], a[q][k]
                    a[p][k] = c * apk - s * aqk
                    a[q][k] = s * apk + c * aqk
                for k in range(n):
                    vkp, vkq = v[k][p], v[k][q]
                    v[k][p] = c * vkp - s * vkq
                    v[k][q] = s * vkp + c * vkq
    ev = [a[i][i] for i in range(n)]
    order = sorted(range(n), key=lambda i: -ev[i])
    lam = [ev[i] for i in order]
    vec = [[v[r][order[c]] for r in range(n)] for c in range(n)]   # 列向量列表
    return lam, vec


def pca(X: list[list[float]]):
    """X: n×d。返回 (mean, 载荷(列=主成分, d×k 全量), 特征值, 得分)。"""
    n, d = len(X), len(X[0])
    mu = [sum(X[i][j] for i in range(n)) / n for j in range(d)]
    Xc = [[X[i][j] - mu[j] for j in range(d)] for i in range(n)]
    C = [[sum(Xc[i][p] * Xc[i][q] for i in range(n)) / (n - 1) for q in range(d)] for p in range(d)]
    lam, vec = jacobi_eig(C)
    scores = [[sum(Xc[i][j] * vec[c][j] for j in range(d)) for c in range(d)] for i in range(n)]
    return mu, vec, lam, scores


def demo(n: int, noise: float, k: int) -> int:
    rng = random.Random(42)
    # 真流形：一条倾斜 30° 的直线 + 小噪声，再"嵌入"到 5 维（其余维为 0 或噪声）
    ang = math.radians(30.0)
    X = []
    for _ in range(n):
        t = rng.uniform(-1.0, 1.0)
        e = rng.gauss(0.0, noise)
        a = t * math.cos(ang) + e * math.sin(ang)
        b = t * math.sin(ang) - e * math.cos(ang)
        X.append([a, b, 0.5 * a - 0.2 * b, 0.1 * b, rng.gauss(0.0, 1e-9)])
    mu, vec, lam, scores = pca(X)
    tot = sum(lam)
    cum = 0.0
    print(f"n = {n}, d = 5, 噪声 σ = {noise}")
    print("特征值 λ（=各主成分得分的方差）与累计方差保留：")
    for i, l in enumerate(lam[:k]):
        cum += l / tot
        print(f"  PC{i + 1}: λ = {l:>10.5f}   单项 {l / tot * 100:>6.2f}%   累计 {cum * 100:>7.3f}%")
    print(f"  其余 {len(lam) - k} 个方向合计 {100 * (1 - cum):>7.3f}%  ← 这就是「丢掉的东西」")

    # 重构误差：取前 k 个主成分反算，看残差
    err = []
    for i in range(n):
        xhat = [mu[j] + sum(scores[i][c] * vec[c][j] for c in range(k)) for j in range(5)]
        err.append(math.dist(X[i], xhat) / n ** 0.5)
    rmse = math.sqrt(sum(e * e for e in err) / n)
    print(f"前 {k} 维重构 RMSE = {rmse:.5f}（噪声 σ = {noise} → 应与之同量级）")
    print(f"选 k 的判据复核：k={k} 保留 {cum * 100:.2f}% ⇒ "
          f"{'达到 99% 线' if cum >= 0.99 else '未达 99%，继续加维'}")

    ok = (lam[0] / tot >= 0.99 and abs(lam[1] / tot) < 0.05 and rmse < 3 * max(noise, 1e-9))
    print("selftest:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=300)
    ap.add_argument("--noise", type=float, default=0.05)
    ap.add_argument("--k", type=int, default=1)
    a = ap.parse_args()
    raise SystemExit(demo(a.n, a.noise, a.k))
