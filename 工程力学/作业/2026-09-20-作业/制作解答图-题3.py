#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""2026-09-20 作业第三题（四面体空间力系，照片题）：题图重绘 + 解答图
运行: /home/user/opt/.venv/bin/python 工程力学/作业/2026-09-20-作业/制作解答图-题3.py
自检：R、M_O、螺旋轴全部断言。
"""
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D  # noqa
from matplotlib import font_manager
from matplotlib.patches import FancyArrowPatch
import matplotlib.projections as mproj

font_manager.fontManager.addfont("/home/user/opt/fonts/NotoSansSC-Bold.ttf")
plt.rcParams["font.family"] = font_manager.FontProperties(
    fname="/home/user/opt/fonts/NotoSansSC-Bold.ttf").get_name()
plt.rcParams["axes.unicode_minus"] = False

OUT = "工程力学/作业/2026-09-20-作业/图"

# ---------------- 数值（a=F=1，方向余弦无量纲） ----------------
A = np.array([1., 0, 0]); B = np.array([0, 1., 0]); C = np.array([0, 0, 1.])
uCA = (A-C)/np.linalg.norm(A-C); uCB = (B-C)/np.linalg.norm(B-C); uAB = (B-A)/np.linalg.norm(B-A)
F1 = np.sqrt(2)*uCA; F2 = np.sqrt(2)*uCB; F3 = 2*np.sqrt(2)*uAB
R = F1+F2+F2*0+F3
R = F1+F2+F3
MO = np.cross(C,F1)+np.cross(C,F2)+np.cross(A,F3)+np.array([0,1.,0])+np.array([1.,0,0])
assert np.allclose(R, [-1,3,-2]) and np.allclose(MO, [0,2,2])
assert abs(np.linalg.norm(R)-math.sqrt(14)) < 1e-9 and abs(np.linalg.norm(MO)-2*math.sqrt(2)) < 1e-9
dot = R@MO
Mpar = (dot/np.linalg.norm(R)**2)*R
r0 = np.cross(R,MO)/np.linalg.norm(R)**2
assert np.allclose(np.linalg.norm(Mpar), math.sqrt(14)/7)
assert np.allclose(r0, [5/7, 1/7, -1/7])
assert np.allclose(MO-np.cross(r0,R), Mpar)
print("自检通过  R=(-1,3,-2)F  M_O=(0,2,2)aF  r0=(5a/7, a/7, -a/7)  |M∥|=√14 aF/7")

def base_scene(ax):
    """画 OABC 四面体骨架 + 三坐标轴（OA/OB/OC 虚线 = 隐藏棱，出三角后实线箭头）"""
    for p, n, t in ((A, "x", "A"), (B, "y", "B"), (C, "z", "C")):
        ax.plot([0, p[0]], [0, p[1]], [0, p[2]], ls=(0, (4, 3)), lw=1.1, color="k", zorder=1)
        ax.quiver(p[0], p[1], p[2], p[0]*0.30, p[1]*0.30, p[2]*0.30,
                  color="k", lw=1.3, arrow_length_ratio=0.30, zorder=1)
    for e in ((A, B), (B, C), (C, A)):
        ax.plot(*zip(e[0], e[1]), color="k", lw=1.6, zorder=2)
    ax.text(*A*1.28, "  A", fontsize=10)
    ax.text(*B*1.28, "  B", fontsize=10)
    ax.text(*C*1.30, "  C", fontsize=10)
    ax.text(0.10, 0.16, 0.06, "O", fontsize=10)
    ax.text(*A*1.30+(0.02,-0.12,-0.08), "x", fontsize=9, style="italic")
    ax.text(*B*1.30+(0.12,0.02,-0.08), "y", fontsize=9, style="italic")
    ax.text(*C*1.30+(-0.10,0.06,0.04), "z", fontsize=9, style="italic")
    ax.set_xlim(-0.35, 1.5); ax.set_ylim(-0.35, 1.5); ax.set_zlim(-0.35, 1.5)
    ax.set_box_aspect((1, 1, 1))
    ax.view_init(elev=35, azim=45)
    ax.set_axis_off()

def force_arrow(ax, p, f, L=0.34, color="k", lw=2.0, zorder=5):
    u = f/np.linalg.norm(f)
    q = p + u*L
    ax.quiver(p[0], p[1], p[2], u[0]*L, u[1]*L, u[2]*L,
              color=color, lw=lw, arrow_length_ratio=0.35, zorder=zorder)
    return q

def arc_arrow(ax, pts, color="crimson", lw=1.6, zorder=6, head=0.05):
    """pts: 弧上点列（含箭头终点）；末段画箭头"""
    pts = np.asarray(pts)
    ax.plot(pts[:-1,0], pts[:-1,1], pts[:-1,2], color=color, lw=lw, zorder=zorder)
    d = pts[-1]-pts[-2]; L = np.linalg.norm(d)
    ax.quiver(pts[-2,0], pts[-2,1], pts[-2,2], d[0]/L*head*3, d[1]/L*head*3, d[2]/L*head*3,
              color=color, lw=lw, arrow_length_ratio=0.9, zorder=zorder)

# ================= 题图（照照片重绘） =================
fig = plt.figure(figsize=(4.6, 4.0), dpi=200)
ax = fig.add_subplot(111, projection="3d")
base_scene(ax)
# F1: 边 CA 上, C→A（箭头朝 A）
q = force_arrow(ax, C*0.80, F1, L=0.52, lw=2.6)
ax.text(*C*0.62+(-0.06, -0.42, 0.06), "F1", fontsize=11, style="italic")
# F2: 边 CB 上, C→B（箭头朝 B）
force_arrow(ax, C*0.80, F2, L=0.52, lw=2.6)
ax.text(*C*0.62+(0.06, 0.44, 0.06), "F2", fontsize=11, style="italic")
# F3: 边 AB 上, A→B（箭头朝 B, 较粗）
force_arrow(ax, A*0.42, F3, L=0.56, lw=2.8)
ax.text(*A*0.42+(-0.06, -0.34, -0.16), "F3", fontsize=11, style="italic")
# M1: OAC 面（xOz 面）力偶, C→A 转向（+z→+x ⇒ +ŷ）: 弧在 y=0 面
t = np.linspace(math.radians(78), math.radians(14), 26)
arc_arrow(ax, np.c_[0.34*np.cos(t), 0.0*np.ones_like(t), 0.34*np.sin(t)])
ax.text(0.05, -0.40, 0.30, "M1", fontsize=11, style="italic")
# M2: OBC 面（yOz 面）力偶, B→C 转向（+y→+z ⇒ +x̂）: 弧在 x=0 面
t = np.linspace(math.radians(16), math.radians(78), 26)
arc_arrow(ax, np.c_[0.0*np.ones_like(t), 0.34*np.cos(t), 0.34*np.sin(t)])
ax.text(0.05, 0.42, 0.32, "M2", fontsize=11, style="italic")
fig.tight_layout()
fig.savefig(f"{OUT}/题3.png", bbox_inches="tight", facecolor="white")
plt.close(fig)
print("saved", f"{OUT}/题3.png")

# ================= 解答图 =================
fig = plt.figure(figsize=(5.6, 4.6), dpi=200)
ax = fig.add_subplot(111, projection="3d")
base_scene(ax)
force_arrow(ax, C*0.52, F1, L=0.30, lw=1.4)
force_arrow(ax, C*0.52, F2, L=0.30, lw=1.4)
force_arrow(ax, A*0.55, F3, L=0.34, lw=1.8)
# 主矢 R（自 O）
Rn = R/np.linalg.norm(R)
force_arrow(ax, np.zeros(3), R, L=0.62, color="b", lw=2.6)
ax.text(*Rn*0.72+( -0.30, 0.10, 0.10), "R=√14 F", fontsize=11, color="b")
# M_O（自 O, 方向 (0,1,1)）
MOn = MO/np.linalg.norm(MO)
force_arrow(ax, np.zeros(3), MO, L=0.50, color="darkorange", lw=2.2)
ax.text(*MOn*0.72+(0.14, 0.10, 0.10), "M_O=2√2 aF", fontsize=10.5, color="darkorange")
# 螺旋轴: 过 r0, 方向 R（虚线, 双向延伸）
r0v = r0
ax.plot(*zip(r0v - Rn*0.55, r0v + Rn*0.75), ls=(0, (4, 3)), color="g", lw=1.6, zorder=4)
ax.scatter(*r0v, s=22, color="g", zorder=6)
ax.text(*(r0v + Rn*0.86)+(0.05, 0.10, 0.02), "螺旋轴", fontsize=10, color="g")
ax.text(*(r0v - Rn*0.60)+(-0.52, -0.28, -0.10), "轴上点 r0=(5a/7, a/7, −a/7)", fontsize=9, color="g")
# 轴上力偶（同向小弧, 示意）
t = np.linspace(math.radians(200), math.radians(320), 24)
c0 = r0v + Rn*0.25
u1, u2 = Rn, np.array([0, 1., 1])/math.sqrt(2)
u3 = np.cross(u1, u2)
arc_pts = c0[:,None] + 0.16*(np.outer(np.cos(t), u2) + np.outer(np.sin(t), u3)).T
arc_arrow(ax, arc_pts, color="g", lw=1.4)
ax.text(*(r0v + Rn*0.10)+(0.16, 0.42, 0.30), "M∥=(√14/7)aF\n（与 R 同向）",
        fontsize=9.5, color="g")
fig.tight_layout()
fig.savefig(f"{OUT}/解答-题3.png", bbox_inches="tight", facecolor="white")
plt.close(fig)
print("saved", f"{OUT}/解答-题3.png")
