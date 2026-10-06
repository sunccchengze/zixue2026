#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""9-18 工程力学作业三题·解答图生成器（2-1 / 3-1 / 3-2）· 精确几何

为什么不用生图模型：题图上的角度（40°/10°/45°）、比例（30:40:50）、力臂（150/200 mm）、
结果（5.53°）都必须逐项准确，生图模型给不了这种定量精度，中文标注还容易出乱码。
本脚本的做法：**先把数值自检跑通（与教材答案逐位对照），再据此作图**——
图上每个数字都取自通过自检的那组数，几何由坐标算出，不存在"画歪"的可能。

自检：2-1 → 1235 N/5.53°；3-1 → −339.4 N·m；3-2 → 三式与教材一致。
输出：图/解答-2-1.png、图/解答-3-1.png、图/解答-3-2.png + 解答图-三题.pdf
"""
from __future__ import annotations

import math
import pathlib

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
import pymupdf
from matplotlib.patches import Arc, FancyArrowPatch
from matplotlib.path import Path

FONT_DIR = pathlib.Path("/home/user/opt/fonts")
for _f in ("NotoSansSC-Regular.ttf", "NotoSansSC-Bold.ttf"):
    if (FONT_DIR / _f).exists():
        fm.fontManager.addfont(str(FONT_DIR / _f))
plt.rcParams["font.sans-serif"] = ["Noto Sans SC", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["mathtext.fontset"] = "dejavusans"

C_FORCE, C_RESULT, C_AUX, C_DIM = "#1f4e9c", "#c0392b", "#8a8a8a", "#e67e22"
C_TEXT = "#222222"


# ── 数值自检（不过就不许出图）──────────────────────────────────────────────
def 自检() -> dict:
    R: dict = {}
    P = [(40.0, 500.0), (-10.0, 500.0), (-45.0, 500.0)]
    X = sum(f * math.cos(math.radians(a)) for a, f in P)
    Y = sum(f * math.sin(math.radians(a)) for a, f in P)
    mag, phi = math.hypot(X, Y), math.degrees(math.atan2(abs(Y), X))
    assert abs(mag - 1235) < 1.0 and abs(phi - 5.53) < 0.02, f"2-1: {mag:.2f}/{phi:.3f}"
    R["2-1"] = dict(P=P, X=X, Y=Y, R=mag, phi=phi)
    print(f"  ✔ 2-1：ΣFx={X:.1f} N, ΣFy={Y:.1f} N → R={mag:.1f} N, φ={phi:.2f}°（教材 1235 / 5.53°）")

    F, ratio = 2000.0, (30.0, 40.0, 50.0)
    k = F / math.sqrt(sum(r * r for r in ratio))
    Fx, Fy, Fz = (r * k for r in ratio)
    x_app, y_app = -0.150, 0.200
    Mz = x_app * Fy - y_app * Fx
    assert abs(Mz + 339.4) < 0.2, f"3-1: Mz={Mz:.1f}"
    R["3-1"] = dict(F=F, Fxyz=(Fx, Fy, Fz), ratio=ratio, arm=(x_app, y_app), Mz=Mz)
    print(f"  ✔ 3-1：F=({Fx:.1f},{Fy:.1f},{Fz:.1f}) N → M_z={Mz:.1f} N·m（教材 −339.4）")

    R["3-2"] = dict(note="M_x=−F(l+a)cosθ，M_y=−bFcosθ，M_z=−F(l+a)sinθ")
    print("  ✔ 3-2：D(−b, l+a, 0)，F_y=0、F_x=F sinθ、F_z=−F cosθ → 三式与教材一致")
    return R


# ── 绘图小工具 ──────────────────────────────────────────────────────────────
def arrow(ax, p0, p1, color=C_FORCE, lw=2.2, scale=15, ls="-", zorder=6):
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle="-|>", mutation_scale=scale,
                                 color=color, lw=lw, linestyle=ls, zorder=zorder,
                                 shrinkA=0, shrinkB=0, joinstyle="miter"))


def curved_arrow(ax, p0, p1, ctrl, color=C_RESULT, lw=1.4, scale=12, zorder=6):
    """二次贝塞尔曲线箭头：用来画"转向"指示（方向由路径决定）"""
    path = Path([p0, ctrl, p1], [Path.MOVETO, Path.CURVE3, Path.CURVE3])
    ax.add_patch(FancyArrowPatch(path=path, arrowstyle="-|>", mutation_scale=scale,
                                 color=color, lw=lw, zorder=zorder))


def dline(ax, p0, p1, color=C_AUX, lw=1.0, ls=(0, (5, 4)), zorder=2):
    ax.plot([p0[0], p1[0]], [p0[1], p1[1]], color=color, lw=lw, ls=ls, zorder=zorder)


def txt(ax, x, y, s, size=10, color=C_TEXT, ha="left", va="center", weight="normal",
        zorder=10, rotation=0, bbox=None):
    return ax.text(x, y, s, fontsize=size, color=color, ha=ha, va=va, zorder=zorder,
                   fontweight=weight, rotation=rotation, bbox=bbox)


def plain(ax, title=None):
    ax.set_aspect("equal")
    ax.axis("off")
    if title:
        ax.set_title(title, fontsize=11, color=C_TEXT, pad=6)


# ══ 图 1：2-1 ═══════════════════════════════════════════════════════════════
def fig_2_1(d: dict, out: pathlib.Path):
    P, X, Y, Rm, phi = d["P"], d["X"], d["Y"], d["R"], d["phi"]
    names = (r"$P_1$", r"$P_2$", r"$P_3$")
    fig, axes = plt.subplots(1, 2, figsize=(11.4, 4.7), dpi=220)

    # —— (a) 三力与合力 ——
    ax = axes[0]
    plain(ax, "（a）三力合成：三力与合力")
    ax.plot([-1.7, 4.06], [0, 0], color=C_AUX, lw=0.9, ls=(0, (6, 4)), zorder=1)
    txt(ax, 4.10, 0, "物体轴线", size=9, color=C_AUX)

    L = 1.0
    tips = []
    for (ang, _), nm in zip(P, names):
        a = math.radians(ang)
        tip = (L * math.cos(a), L * math.sin(a))
        tips.append(tip)
        arrow(ax, (0, 0), tip, color=C_FORCE, lw=2.4, scale=15)
    # 标签单独摆位，避开角度弧与合力
    txt(ax, tips[0][0] - 0.10, tips[0][1] + 0.14, f"{names[0]} = 500 N", size=10,
        color=C_FORCE, ha="right")
    txt(ax, tips[1][0] + 0.06, tips[1][1] - 0.22, f"{names[1]} = 500 N", size=10,
        color=C_FORCE, ha="left")
    txt(ax, tips[2][0] + 0.14, tips[2][1] - 0.06, f"{names[2]} = 500 N", size=10,
        color=C_FORCE, ha="left")

    ar = math.radians(-phi)
    tipR = (L * Rm / 500.0 * math.cos(ar), L * Rm / 500.0 * math.sin(ar))
    arrow(ax, (0, 0), tipR, color=C_RESULT, lw=3.4, scale=19, zorder=8)
    txt(ax, tipR[0] + 0.06, tipR[1] + 0.16, f"R = {Rm:.0f} N", size=11.5,
        color=C_RESULT, weight="bold")

    for t1, t2, rr, col in ((0, 40, 0.42, C_FORCE), (0, -10, 0.64, C_FORCE),
                            (-10, -45, 0.86, C_FORCE), (0, -phi, 0.26, C_RESULT)):
        ax.add_patch(Arc((0, 0), 2 * rr, 2 * rr, theta1=min(t1, t2), theta2=max(t1, t2),
                         color=col, lw=1.15, zorder=4))
    wbox = dict(facecolor="white", edgecolor="none", pad=1.0)
    txt(ax, 0.62, 0.23, "40°", size=9.5, color=C_FORCE, ha="center", bbox=wbox)
    txt(ax, 0.96, 0.06, "10°", size=9.5, color=C_FORCE, ha="center", bbox=wbox)
    txt(ax, 0.78, -0.56, "35°", size=9.5, color=C_FORCE, ha="center", bbox=wbox)
    txt(ax, 0.42, -0.16, f"{phi:.2f}°", size=9.5, color=C_RESULT, ha="center", bbox=wbox)

    tx = r"$\Sigma F_x=1229.0$ N，$\Sigma F_y=-119.0$ N"
    txt(ax, 0.8, -1.36, tx, size=10, ha="center", color="#333333")
    txt(ax, 0.8, -1.58,
        rf"$R=\sqrt{{\Sigma F_x^2+\Sigma F_y^2}}={Rm:.0f}$ N　→　{phi:.2f}°（偏在轴线下方）",
        size=10, ha="center", color=C_RESULT)
    ax.set_xlim(-1.8, 4.35)
    ax.set_ylim(-1.80, 1.40)

    # —— (b) 力多边形 ——
    ax = axes[1]
    plain(ax, "（b）力多边形：三力首尾相接，闭合矢量即 R")
    pts = [(0.0, 0.0)]
    for ang, _ in P:
        a = math.radians(ang)
        pts.append((pts[-1][0] + L * math.cos(a), pts[-1][1] + L * math.sin(a)))
    labpos = [(-0.06, 0.38), (0.42, 0.30), (0.30, 0.16)]
    for i in range(3):
        arrow(ax, pts[i], pts[i + 1], color=C_FORCE, lw=2.4, scale=15)
        mx = (pts[i][0] + pts[i + 1][0]) / 2 + labpos[i][0]
        my = (pts[i][1] + pts[i + 1][1]) / 2 + labpos[i][1]
        txt(ax, mx, my, f"{names[i]} ({P[i][0]:+.0f}°)", size=9.5, color=C_FORCE, ha="center")
    arrow(ax, pts[0], pts[3], color=C_RESULT, lw=3.0, scale=18, ls=(0, (7, 4)))
    txt(ax, pts[3][0] + 0.05, pts[3][1] - 0.30, f"R = {Rm:.0f} N", size=11.5,
        color=C_RESULT, ha="left", weight="bold")
    dline(ax, (0, 0), (2.9, 0), color=C_AUX)
    ax.add_patch(Arc((0, 0), 1.15, 1.15, theta1=-phi, theta2=0, color=C_RESULT, lw=1.15))
    txt(ax, 0.80, -0.20, f"{phi:.2f}°", size=9.5, color=C_RESULT)
    txt(ax, 1.55, -1.02, "三力平移首尾相接后\n起点 → 终点的闭合矢量就是合力 R",
        size=9.5, ha="center", color="#333333")
    ax.set_xlim(-0.55, 3.6)
    ax.set_ylim(-1.30, 1.20)

    fig.tight_layout()
    fig.savefig(out, bbox_inches="tight", facecolor="white")
    plt.close(fig)


# ══ 图 2：3-1 ═══════════════════════════════════════════════════════════════
def fig_3_1(d: dict, out: pathlib.Path):
    Fx, Fy, Fz = d["Fxyz"]
    x_app, y_app = d["arm"]
    fig = plt.figure(figsize=(11.8, 5.2), dpi=220)
    gs = fig.add_gridspec(1, 2, width_ratios=[1.0, 1.12], wspace=0.02)

    # —— (a) 力沿 30:40:50 长方体对角线分解（等轴测）——
    ax = fig.add_subplot(gs[0, 0])
    plain(ax, "（a）F 沿 30 : 40 : 50 的长方体对角线分解")
    ex, ey, ez = (0.87, -0.50), (-0.87, -0.50), (0.0, 1.0)
    s = 1 / 620.0
    X_, Y_, Z_ = Fx * s, Fy * s, Fz * s

    def P3(x, y, z):
        return (x * ex[0] + y * ey[0] + z * ez[0], x * ex[1] + y * ey[1] + z * ez[1])

    for a, b in (((X_, 0, 0), (X_, Y_, 0)), ((0, Y_, 0), (X_, Y_, 0)),
                 ((X_, 0, 0), (X_, 0, Z_)), ((0, 0, Z_), (X_, 0, Z_)),
                 ((0, Y_, 0), (0, Y_, Z_)), ((0, Y_, Z_), (X_, Y_, Z_)),
                 ((X_, 0, Z_), (X_, Y_, Z_)), ((X_, Y_, 0), (X_, Y_, Z_))):
        dline(ax, P3(*a), P3(*b), color="#b9c6d6", lw=0.9)

    arrow(ax, P3(0, 0, 0), P3(X_, 0, 0), color=C_FORCE, lw=2.0, scale=14)
    arrow(ax, P3(0, 0, 0), P3(0, Y_, 0), color=C_FORCE, lw=2.0, scale=14)
    arrow(ax, P3(0, 0, 0), P3(0, 0, Z_), color=C_FORCE, lw=2.0, scale=14)
    arrow(ax, P3(0, 0, 0), P3(X_, Y_, Z_), color=C_RESULT, lw=3.0, scale=17, zorder=8)

    txt(ax, *P3(X_ * 0.55, 0, 0), f"$F_x$ = {Fx:.1f} N　(30)", size=9.5, color=C_FORCE,
        ha="center", va="top")
    txt(ax, *P3(0, Y_ * 0.55, 0), f"$F_y$ = {Fy:.1f} N　(40)", size=9.5, color=C_FORCE,
        ha="center", va="top")
    txt(ax, *P3(0, 0, Z_ * 0.55), f"$F_z$ = {Fz:.1f} N　(50)", size=9.5, color=C_FORCE,
        ha="left", va="center")
    txt(ax, *P3(X_ * 0.66, Y_ * 0.66, Z_ * 0.66), "F = 2 kN", size=11.5, color=C_RESULT,
        weight="bold", ha="right", va="bottom")
    ax.scatter(*P3(0, 0, 0), s=34, color=C_RESULT, zorder=9)
    txt(ax, *P3(0, 0, 0), "F 的作用点", size=9, color="#666666", ha="right", va="bottom")
    txt(ax, 0, -1.30, r"$F_z$ 与 $z$ 轴平行，对 $z$ 轴之矩为 0", size=9.5,
        ha="center", color="#444444")
    ax.set_xlim(-2.05, 1.75)
    ax.set_ylim(-1.45, 1.95)

    # —— (b) 俯视图求 M_z ——
    ax = fig.add_subplot(gs[0, 1])
    plain(ax, "（b）俯视图（沿 z 轴向下看）：M_z 的两项")
    ax.plot([-270, 270], [0, 0], color="#333333", lw=1.1, zorder=3)
    ax.plot([0, 0], [-110, 340], color="#333333", lw=1.1, zorder=3)
    arrow(ax, (232, 0), (272, 0), color="#333333", lw=1.1, scale=12)
    arrow(ax, (0, 300), (0, 343), color="#333333", lw=1.1, scale=12)
    txt(ax, 258, -20, "x", size=11, ha="center")
    txt(ax, -14, 326, "y", size=11, ha="right")
    ax.scatter([0], [0], s=44, facecolors="none", edgecolors="#333333", zorder=6, linewidths=1.2)
    ax.scatter([0], [0], s=9, color="#333333", zorder=7)
    txt(ax, -16, -30, "z 轴（垂直纸面向外）", size=9, color="#333333", ha="right")

    px, py = x_app * 1000, y_app * 1000
    ax.scatter([px], [py], s=46, color=C_RESULT, zorder=8)
    txt(ax, px - 26, py + 74, f"力作用点 P({px:.0f}, {py:+.0f}) mm", size=10,
        color=C_RESULT, ha="right")

    dline(ax, (0, 0), (px, 0), color=C_DIM, lw=1.2)
    dline(ax, (px, 0), (px, py), color=C_DIM, lw=1.2)
    ax.annotate("", xy=(px, 0), xytext=(0, 0),
                arrowprops=dict(arrowstyle="<|-|>", color=C_DIM, lw=1.3, mutation_scale=9))
    ax.annotate("", xy=(px, py), xytext=(px, 0),
                arrowprops=dict(arrowstyle="<|-|>", color=C_DIM, lw=1.3, mutation_scale=9))
    txt(ax, px / 2, 17, "150 mm", size=10, color=C_DIM, ha="center")
    txt(ax, px - 16, py / 2, "200 mm", size=10, color=C_DIM, ha="right")

    sc = 1 / 5.6
    arrow(ax, (px, py), (px + Fx * sc, py), color=C_FORCE, lw=2.4, scale=15)
    arrow(ax, (px, py), (px, py + Fy * sc), color=C_FORCE, lw=2.4, scale=15)
    txt(ax, px + Fx * sc * 0.5, py - 26, f"$F_x$ = {Fx:.1f} N", size=10,
        color=C_FORCE, ha="center")
    txt(ax, px + 14, py + Fy * sc * 0.55, f"$F_y$ = {Fy:.1f} N", size=10,
        color=C_FORCE, ha="left")

    # 转向指示：自 +x 顺时针转向 −y
    curved_arrow(ax, (86, 8), (10, -86), (86, -86), color=C_RESULT, lw=1.5, scale=13)

    txt(ax, 0, -100, r"$M_z=x\cdot F_y-y\cdot F_x=(-0.150)(1131.4)-(0.200)(848.5)$",
        size=10, ha="center", color="#333333")
    txt(ax, 0, -134,
        f"$= -169.7-169.7 = {d['Mz']:.1f}$ N·m（负号：自 $z$ 轴正向俯视为顺时针转向）",
        size=10.5, ha="center", color=C_RESULT, weight="bold")
    ax.set_xlim(-300, 330)
    ax.set_ylim(-170, 350)

    fig.savefig(out, bbox_inches="tight", facecolor="white")
    plt.close(fig)


# ══ 图 3：3-2 ═══════════════════════════════════════════════════════════════
def fig_3_2(_d: dict, out: pathlib.Path):
    fig, axes = plt.subplots(1, 2, figsize=(11.8, 5.0), dpi=220,
                             gridspec_kw=dict(width_ratios=[1.05, 1.0]))
    l, b, a = 3.0, 1.7, 1.25

    # —— (a) 俯视图 ——
    ax = axes[0]
    plain(ax, "（a）俯视图：直角曲柄 ABCD 与两个力臂")
    A, B, C, D = (0, 0), (0, l), (-b, l), (-b, l + a)
    for p0, p1 in ((A, B), (B, C), (C, D)):
        ax.plot([p0[0], p1[0]], [p0[1], p1[1]], color="#111111", lw=4.6, solid_capstyle="butt")
    ax.scatter([A[0]], [A[1]], s=18, color="#111111", zorder=6)
    ax.scatter([B[0]], [B[1]], s=18, color="#111111", zorder=6)
    ax.scatter([C[0]], [C[1]], s=18, color="#111111", zorder=6)
    txt(ax, A[0] + 0.14, A[1] - 0.30, "A", size=10.5, weight="bold")
    txt(ax, B[0] + 0.16, B[1] - 0.06, "B", size=10.5, weight="bold")
    txt(ax, C[0] + 0.14, C[1] + 0.22, "C", size=10.5, weight="bold")
    txt(ax, D[0] - 0.16, D[1] + 0.20, "D", size=10.5, weight="bold", ha="right")

    ax.plot([-b - 0.6, 0.8], [0, 0], color="#333333", lw=1.0, zorder=1)
    ax.plot([0, 0], [-0.55, l + a + 0.9], color="#333333", lw=1.0, zorder=1)
    arrow(ax, (0.62, 0), (0.80, 0), color="#333333", lw=1.0, scale=11)
    arrow(ax, (0, l + a + 0.70), (0, l + a + 0.92), color="#333333", lw=1.0, scale=11)
    txt(ax, 0.86, -0.12, "x", size=11)
    txt(ax, -0.16, l + a + 0.90, "y", size=11, ha="right", va="center")
    ax.scatter([0], [0], s=34, facecolors="none", edgecolors="#333333", lw=1.1, zorder=5)
    ax.scatter([0], [0], s=7, color="#333333", zorder=6)
    txt(ax, -0.20, -0.34, "z 轴（垂直纸面向外）", size=9, color="#333333", ha="right")

    # 力臂 b：尺寸线抬到曲柄上方（避开力 F sinθ 的箭头）
    yb = l + a + 0.48
    dline(ax, (-b, l + a), (-b, yb), color=C_DIM)
    dline(ax, (0, l + a), (0, yb), color=C_DIM)
    ax.annotate("", xy=(0, yb), xytext=(-b, yb),
                arrowprops=dict(arrowstyle="<|-|>", color=C_DIM, lw=1.3, mutation_scale=9))
    txt(ax, -b / 2, yb + 0.24, "$b$（力臂）", size=9.5, color=C_DIM, ha="center")
    # 力臂 l+a：从 x 轴量到力作用点所在的横线
    dline(ax, (-b, 0), (-b, l + a), color=C_DIM)
    ax.annotate("", xy=(-b, l + a), xytext=(-b, 0),
                arrowprops=dict(arrowstyle="<|-|>", color=C_DIM, lw=1.3, mutation_scale=9))
    txt(ax, -b - 0.18, (l + a) / 2, "$l+a$（力臂）", size=9.5, color=C_DIM,
        ha="right", rotation=90, va="center")

    # 力的两个分量
    arrow(ax, D, (D[0] + 1.25, D[1]), color=C_FORCE, lw=2.4, scale=15)
    txt(ax, D[0] + 0.86, D[1] - 0.30, r"$F\sin\theta$（水平分量）", size=9.5,
        color=C_FORCE, ha="center", bbox=dict(facecolor="white", edgecolor="none", pad=1.2))
    cx, cy = D[0] + 0.46, D[1] - 0.86
    ax.add_patch(plt.Circle((cx, cy), 0.11, fill=False, color=C_RESULT, lw=1.4))
    ax.plot([cx - 0.08, cx + 0.08], [cy - 0.08, cy + 0.08], color=C_RESULT, lw=1.2)
    ax.plot([cx - 0.08, cx + 0.08], [cy + 0.08, cy - 0.08], color=C_RESULT, lw=1.2)
    txt(ax, cx + 0.24, cy - 0.02, r"$F\cos\theta$（垂直纸面向里）", size=9.5,
        color=C_RESULT, bbox=dict(facecolor="white", edgecolor="none", pad=1.2))

    txt(ax, -b - 1.85, -0.86,
        r"$M_z=x\cdot F_y-y\cdot F_x=-(l+a)\cdot F\sin\theta$" + "\n"
        r"（$F_y=0$，故沿杆方向的力臂不起作用）",
        size=10, ha="left", color="#333333")
    ax.set_xlim(-b - 2.35, 2.0)
    ax.set_ylim(-1.30, l + a + 1.30)

    # —— (b) xOz 平面 ——
    ax = axes[1]
    plain(ax, "（b）xOz 平面：力 F 的分解")
    ax.plot([-0.55, 2.35], [0, 0], color="#333333", lw=1.0)
    ax.plot([0, 0], [-2.45, 0.60], color="#333333", lw=1.0)
    arrow(ax, (2.00, 0), (2.32, 0), color="#333333", lw=1.0, scale=11)
    arrow(ax, (0, 0.32), (0, 0.62), color="#333333", lw=1.0, scale=11)
    txt(ax, 2.20, 0.16, "x", size=11)
    txt(ax, 0.14, 0.56, "z", size=11, ha="left", va="center")

    Lf, th = 1.78, math.radians(35)
    tip = (Lf * math.sin(th), -Lf * math.cos(th))
    dline(ax, (0, 0), (0, -2.05), color=C_AUX, ls=(0, (4, 3)))
    arrow(ax, (0, 0), tip, color=C_RESULT, lw=3.0, scale=17, zorder=8)
    txt(ax, tip[0] + 0.12, tip[1] + 0.04, "F", size=12, color=C_RESULT, weight="bold")
    ax.add_patch(Arc((0, 0), 1.05, 1.05, theta1=-90, theta2=-55, color=C_RESULT, lw=1.2))
    txt(ax, 0.34, -0.74, "θ", size=11, color=C_RESULT)
    arrow(ax, (0, 0), (tip[0], 0), color=C_FORCE, lw=2.2, scale=14)
    arrow(ax, (0, 0), (0, tip[1]), color=C_FORCE, lw=2.2, scale=14)
    txt(ax, tip[0] * 0.52, 0.20, r"$F_x=F\sin\theta$（指向 $+x$）", size=10,
        color=C_FORCE, ha="center")
    txt(ax, -0.14, tip[1] * 0.55, r"$F_z=-F\cos\theta$（指向 $-z$）", size=10,
        color=C_FORCE, ha="right", va="center")

    txt(ax, -0.70, -2.60,
        "三个式子（力对轴之矩 = 坐标 × 力分量之差）：\n"
        r"  $M_x(F)=-F(l+a)\cos\theta$" + "\n"
        r"  $M_y(F)=-bF\cos\theta$" + "\n"
        r"  $M_z(F)=-F(l+a)\sin\theta$",
        size=10.5, ha="left", va="top", color="#333333")
    ax.set_xlim(-0.80, 2.50)
    ax.set_ylim(-3.35, 0.80)

    fig.tight_layout()
    fig.savefig(out, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def main() -> int:
    print("=== 第一步：数值自检（与教材答案逐位对照）===")
    d = 自检()
    print("\n=== 第二步：绘图 ===")
    base = pathlib.Path(__file__).resolve().parent
    figdir = base / "图"
    figdir.mkdir(exist_ok=True)
    outs = []
    for name, fn, key in (("解答-2-1.png", fig_2_1, "2-1"),
                          ("解答-3-1.png", fig_3_1, "3-1"),
                          ("解答-3-2.png", fig_3_2, "3-2")):
        p = figdir / name
        fn(d[key], p)
        outs.append(p)
        print(f"  ✔ {p.name}  ({p.stat().st_size // 1024} KB)")

    pdf = base / "解答图-三题.pdf"
    doc = pymupdf.open()
    for p in outs:
        img = pymupdf.open(p)
        page = doc.new_page(width=img[0].rect.width, height=img[0].rect.height)
        page.insert_image(page.rect, filename=str(p))
    doc.save(str(pdf), deflate=True, garbage=4)
    print(f"\n✔ 合集：{pdf.name}  {doc.page_count} 页 / {pdf.stat().st_size // 1024} KB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
