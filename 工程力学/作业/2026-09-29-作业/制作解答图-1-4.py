# -*- coding: utf-8 -*-
"""1-4 受力示意图（方向为准、比例示意）。拉丁字母标注，无需 CJK。
约定：二力杆两端力沿杆轴等大反向；绳张力 T；光滑铰两分量；辊轴竖直。"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrow

OUT = "工程力学/作业/2026-09-29-作业/图/"
S = 0.9  # 箭头长度

def unit(p, q):
    v = np.array(q, float) - np.array(p, float); return v / np.linalg.norm(v)

def ar(ax, p, d, lab="", c="crimson", fs=10):
    p = np.array(p, float); d = np.array(d, float)
    d = d / np.linalg.norm(d) * S
    ax.add_patch(FancyArrow(p[0], p[1], d[0], d[1], width=0.015, head_width=0.10,
                            length_includes_head=True, color=c, lw=1.6))
    if lab:
        ax.text(p[0]+d[0]*1.35, p[1]+d[1]*1.35, lab, fontsize=fs, color=c, ha="center", va="center")

def rod(ax, p, q):
    ax.plot([p[0], q[0]], [p[1], q[1]], color="0.25", lw=2.5, zorder=1)

def panel(ax, title):
    ax.set_aspect("equal"); ax.axis("off"); ax.set_title(title, fontsize=10)
    ax.set_xlim(-1.6, 4.4); ax.set_ylim(-1.6, 4.4)

fig = plt.figure(figsize=(16, 11))

# ───────── (a) ─────────
A, B, C = (0, 3), (2, 2), (0, 0)
uAB, uBC = unit(A, B), unit(B, C)
ax = fig.add_subplot(3, 4, 1); panel(ax, "(a) AB two-force")
rod(ax, A, B); ar(ax, A, -uAB, "N_AB"); ar(ax, B, uAB, "N_AB")
ax = fig.add_subplot(3, 4, 2); panel(ax, "(a) BC two-force")
rod(ax, B, C); ar(ax, B, -uBC, "N_BC"); ar(ax, C, uBC, "N_BC")
ax = fig.add_subplot(3, 4, 3); panel(ax, "(a) pin B")
ar(ax, (1, 1), (0, -1), "P"); ar(ax, (1, 1), uAB, "N_AB"); ar(ax, (1, 1), uBC, "N_BC")
ax = fig.add_subplot(3, 4, 4); panel(ax, "(a) whole")
rod(ax, A, B); rod(ax, B, C); ar(ax, A, -uAB, "R_A"); ar(ax, C, uBC, "R_C"); ar(ax, B, (0, -1), "P")

# ───────── (b) ─────────
Ab, Bb, Cb, Db, Eb, Hb = (0, 3), (1.6, 1.2), (0, 1.2), (3, 1.2), (1.1, 1.7), (3, 0.2)
ax = fig.add_subplot(3, 5, 6); panel(ax, "(b) AB")
rod(ax, Ab, Bb); ar(ax, Ab, (0.5, 0.6), "Ax"); ar(ax, Ab, (-0.5, 0.5), "Ay"); ar(ax, Eb, (1, 0), "T"); ar(ax, Bb, (0.6, 0.4), "Bx,By")
ax = fig.add_subplot(3, 5, 7); panel(ax, "(b) CD")
rod(ax, Cb, Db); ar(ax, Cb, (-0.6, 0.4), "Cx,Cy"); ar(ax, Bb, (0.5, 0.5), "Bx',By'"); ar(ax, Db, (0.5, 0.6), "Dx,Dy")
ax = fig.add_subplot(3, 5, 8); panel(ax, "(b) wheel H")
ar(ax, (0, 0), (0, 1), "T"); ar(ax, (0.4, 0), (0, 1), "T"); ar(ax, (0.2, -0.2), (0, -1), "P")
ax = fig.add_subplot(3, 5, 9); panel(ax, "(b) pin+wheel D")
ar(ax, (0, 0.4), (-1, 0), "T"); ar(ax, (0.4, 0), (0, -1), "T"); ar(ax, (0, 0), (0, -1), "T"); ar(ax, (-0.2, 0), (0.6, 0.7), "Dx',Dy'")
ax = fig.add_subplot(3, 5, 10); panel(ax, "(b) whole")
rod(ax, Ab, Bb); rod(ax, Cb, Db); ar(ax, Ab, (0.6, 0.4), "A"); ar(ax, Cb, (-0.6, 0.4), "C"); ar(ax, Hb, (0, -1), "P")

# ───────── (c) ─────────
Ac, Bc, Ec, Dc, Cc = (0, 2), (3, 2), (1.6, 3.2), (1.6, 2), (1.6, 0.6)
uEB = unit(Ec, Bc)
ax = fig.add_subplot(3, 3, 7); panel(ax, "(c) AB+pinB")
rod(ax, Ac, Bc); ar(ax, Ac, (0.5, 0.5), "Ax,Ay"); ar(ax, Bc, (0, 1), "N_B"); ar(ax, Bc, uEB, "F_EB")
ax = fig.add_subplot(3, 3, 8); panel(ax, "(c) CE+pulley")
rod(ax, Ec, Cc); ar(ax, Ec, -uEB, "F_EB"); ar(ax, Dc, (0.7, 0.3), "Dx,Dy"); ar(ax, Cc, (-1, 0), "T"); ar(ax, Cc, (0.3, -1), "P")
ax = fig.add_subplot(3, 3, 9); panel(ax, "(c) whole")
rod(ax, Ac, Bc); rod(ax, Ec, Cc); ar(ax, Ac, (0.5, 0.5), "A"); ar(ax, Bc, (0, 1), "N_B"); ar(ax, Cc, (-1, 0), "T"); ar(ax, Cc, (0.3, -1), "P")

plt.tight_layout()
plt.savefig(OUT + "解答-1-4.png", dpi=180)
plt.close()
print("saved 解答-1-4.png")
