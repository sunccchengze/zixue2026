#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""2026-09-20 工程力学作业 2-2、2-7 解答图（精确坐标 + 自检）
运行: /home/user/opt/.venv/bin/python 工程力学/作业/2026-09-20-作业/制作解答图.py
"""
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyArrowPatch, Arc, Circle, Rectangle, Polygon

FONT = font_manager.FontProperties(fname="/home/user/opt/fonts/NotoSansSC-Bold.ttf")
plt.rcParams["font.family"] = FONT.get_name()
font_manager.fontManager.addfont("/home/user/opt/fonts/NotoSansSC-Bold.ttf")
plt.rcParams["axes.unicode_minus"] = False

OUT = "工程力学/作业/2026-09-20-作业/图"

def arrow(ax, p0, p1, lw=1.8, ms=14, color="k", **kw):
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle="-|>", mutation_scale=ms,
                                 lw=lw, color=color, **kw))

# ---------------- 自检：数值 ----------------
F, M, G, P1, P2 = 2740.0, 552.5, 5280.0, 193.0, 140.0
Rx, Ry = -(P1+P2), -(F+G)
R = math.hypot(Rx, Ry)
MO = P1*21 + P2*10.7 + M
y_axis = MO/abs(Rx); x_base = -MO/abs(Ry); d_perp = MO/R
assert abs(R-8026.91) < 0.05 and abs(MO-6103.5) < 1e-9
c60,s60,c30,s30 = [math.cos(math.radians(a)) for a in (60,30)]+[math.sin(math.radians(a)) for a in (60,30)]
A_,B_,C_,D_ = (-240,100),(240,100),(240,-100),(-240,-100)
F1 = (-400*c60, 400*s60); F2 = (400*c60, -400*s60)
F3 = (-300*c30, -300*s30); F4 = (300*c30, 300*s30)
mz = lambda p,f: p[0]*f[1]-p[1]*f[0]
M1 = mz(B_,F1)+mz(D_,F2); M2 = mz(A_,F3)+mz(C_,F4)
assert abs(M1-206276.9) < 1 and abs(M2-123961.5) < 1 and abs((M1+M2)/1000-330.24) < 0.01
print("自检通过  R=%.1f kN  MO=%.1f kN·m  M1=%.0f  M2=%.0f  N·mm" % (R, MO, M1, M2))

# ================= 2-2 =================
fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.0, 3.6), dpi=200)
def pier(ax, alpha=1.0, draw_O=True):
    ax.add_patch(Polygon([(-2.6,0),(2.6,0),(0.9,21),(-0.9,21)], closed=True,
                         fc="#dceefc", ec="k", lw=1.2, alpha=alpha, zorder=1))
    ax.add_patch(Rectangle((-1.5,21), 3.0, 1.1, fc="#dceefc", ec="k", lw=1.2, zorder=1))
    ax.plot([0,0],[0,22.1], ls=(0,(3,2)), lw=0.7, color="k", zorder=1)
    ax.plot([-4.6,4.6],[0,0], lw=1.0, color="k")
    for x in range(-45, 46, 9):
        ax.plot([x/10, x/10-0.35],[0,-0.35], lw=0.6, color="k")
    if draw_O:
        ax.text(0, -0.75, "O", ha="center", va="top", fontsize=9)
    ax.set_xlim(-4.8, 5.4); ax.set_ylim(-1.1, 23.4); ax.set_aspect("equal"); ax.axis("off")

for ax, dim in ((a1, True), (a2, False)):
    pier(ax, draw_O=(ax is a1))
# (a) 原力系
a1.set_title("（a）原力系", fontsize=10)
arrow(a1, (0,23.0), (0,21.6))                       # F
a1.text(0.5, 22.9, "F=2740kN", fontsize=8.5)
arc = Arc((-1.35,22.15), 1.5, 1.0, angle=0, theta1=115, theta2=265, lw=1.4, color="k")
a1.add_patch(arc)
arrow(a1, (-2.05,22.45), (-1.85,22.62), ms=10)      # M 逆时针箭头
a1.text(-4.6, 21.85, "M=552.5kN·m", fontsize=8.5, ha="left")
arrow(a1, (2.6,21.55), (1.7,21.55))                 # P1 向左
a1.text(2.75, 21.55, "P1=193kN", fontsize=8.5, va="center")
arrow(a1, (0,12.1), (0,10.9))                       # G
a1.text(0.25, 11.3, "G=5280kN", fontsize=8.5)
arrow(a1, (2.7,10.7), (1.15,10.7))                  # P2 向左
a1.text(2.85, 10.7, "P2=140kN", fontsize=8.5, va="center")
if dim:
    axd = a1
    axd.annotate("", xy=(-3.6,0), xytext=(-3.6,22.1),
                 arrowprops=dict(arrowstyle="<->", lw=0.8, color="k"))
    axd.text(-3.95, 11, "21m", rotation=90, fontsize=8, ha="center", va="center")
    axd.plot([-2.9,-3.6],[10.7,10.7], lw=0.5, color="k")
    axd.annotate("", xy=(-2.9,0), xytext=(-2.9,10.7),
                 arrowprops=dict(arrowstyle="<->", lw=0.8, color="k"))
    axd.text(-3.25, 5.3, "10.7m", rotation=90, fontsize=8, ha="center", va="center")
# (b) 简化结果
a2.set_title("（b）向 O 点简化：R + M_O（合力作用线如图虚线）", fontsize=10)
y0, x0 = y_axis, x_base
a2.plot([x0, 0], [0, y0], ls="--", lw=0.9, color="b", zorder=3)      # 作用线（延长过轴）
def xon(y): return x0 + y/24.084
arrow(a2, (xon(11.2), 11.2), (xon(1.9), 1.9), lw=2.2, ms=17, color="b")   # R 沿作用线
a2.text(xon(6.5)-0.3, 6.5, "R=8027kN", fontsize=9, color="b", ha="right", rotation=87.6)
arc2 = Arc((0,0.6), 2.6, 1.9, angle=0, theta1=110, theta2=300, lw=1.4, color="r")
a2.add_patch(arc2)
arrow(a2, (-1.28,0.98), (-1.05,1.18), ms=11, color="r")
a2.text(-5.3, -0.85, "M_O=6103.5kN·m（逆时针）", fontsize=8.5, color="r", ha="left")
a2.set_xlim(-5.6, 5.4)
a2.plot([x0, 0], [1.05, 1.05], lw=0.8, color="k")
a2.annotate("", xy=(x0,1.05), xytext=(0,1.05), arrowprops=dict(arrowstyle="<->", lw=0.7, color="k"))
a2.text(x0/2, 1.28, "0.76m", fontsize=8, ha="center")
a2.text(0.32, -0.42, "O", fontsize=9, ha="left")
a2.plot([0,0],[y0,y0], lw=0.5, color="b")
a2.annotate("作用线交墩轴线\n高 18.33m", xy=(0, y0), xytext=(1.6, 16.6),
            fontsize=8, color="b", arrowprops=dict(arrowstyle="->", lw=0.7, color="b"))
fig.tight_layout()
fig.savefig(f"{OUT}/解答-2-2.png", bbox_inches="tight", facecolor="white")
plt.close(fig)
print("saved", f"{OUT}/解答-2-2.png")

# ================= 2-7 =================
fig, ax = plt.subplots(figsize=(6.4, 4.4), dpi=200)
ax.add_patch(Rectangle((-240,-100), 480, 200, fc="#eaf6fd", ec="k", lw=1.4, zorder=1))
for p, nm in ((A_,"A"),(B_,"B"),(C_,"C"),(D_,"D")):
    ax.add_patch(Circle(p, 11, fc="white", ec="k", lw=1.2, zorder=4))
    ax.plot(*p, "+", ms=4, color="k", zorder=5)
off = lambda p, u, L: (p[0]+u[0]*L, p[1]+u[1]*L)
# 绳1: B-D, 400N
uB1 = (-c60, s60); uBD = (B_[0]-D_[0], B_[1]-D_[1]); L=math.hypot(*uBD); uBD=(uBD[0]/L, uBD[1]/L)
uAC = (C_[0]-A_[0], C_[1]-A_[1]); L=math.hypot(*uAC); uAC=(uAC[0]/L, uAC[1]/L)
ax.plot(*zip(*[off(B_, uBD, -430), off(D_, uBD, 430)]), lw=1.6, color="k", zorder=3)   # B-D 绳
ax.plot(*zip(*[off(A_, uAC, -430), off(C_, uAC, 430)]), lw=1.6, color="k", zorder=3)   # A-C 绳
arrow(ax, off(B_, uB1, 25), off(B_, uB1, 265), lw=1.8)
ax.text(*off(B_, uB1, 280), "F1=400N", fontsize=9)
arrow(ax, off(D_, (c60,-s60), 25), off(D_, (c60,-s60), 265), lw=1.8)
ax.text(*off(D_, (c60,-s60), 280), "F2=400N", fontsize=9)
arrow(ax, off(A_, (-c30,-s30), 25), off(A_, (-c30,-s30), 235), lw=1.8)
ax.text(off(A_, (-c30,-s30), 245)[0]-55, off(A_, (-c30,-s30), 245)[1]-16, "F3=300N", fontsize=9)
arrow(ax, off(C_, (c30,s30), 25), off(C_, (c30,s30), 235), lw=1.8)
ax.text(*off(C_, (c30,s30), 250), "F4=300N", fontsize=9)
# 角度标注
a = Arc(B_, 90, 90, angle=0, theta1=120, theta2=180, lw=0.9, color="k")
ax.add_patch(a); ax.text(B_[0]-95, B_[1]+34, "60°", fontsize=8)
a = Arc(D_, 90, 90, angle=0, theta1=-60, theta2=0, lw=0.9, color="k")
ax.add_patch(a); ax.text(D_[0]+58, D_[1]-40, "60°", fontsize=8)
a = Arc(A_, 80, 80, angle=0, theta1=180, theta2=210, lw=0.9, color="k")
ax.add_patch(a); ax.text(A_[0]-150, A_[1]+8, "30°", fontsize=8)
a = Arc(C_, 80, 80, angle=0, theta1=0, theta2=30, lw=0.9, color="k")
ax.add_patch(a); ax.text(C_[0]+95, C_[1]+22, "30°", fontsize=8)
# 尺寸
ax.annotate("", xy=(-240,-150), xytext=(0,-150), arrowprops=dict(arrowstyle="<->", lw=0.8, color="k"))
ax.annotate("", xy=(0,-150), xytext=(240,-150), arrowprops=dict(arrowstyle="<->", lw=0.8, color="k"))
ax.text(-120, -168, "240", fontsize=8, ha="center"); ax.text(120, -168, "240", fontsize=8, ha="center")
ax.plot([-240,-240],[0,-150], lw=0.5, color="k"); ax.plot([240,240],[0,-150], lw=0.5, color="k")
ax.plot([0,0],[100,-150], ls=(0,(3,2)), lw=0.6, color="k")
ax.annotate("", xy=(-320,100), xytext=(-320,-100), arrowprops=dict(arrowstyle="<->", lw=0.8, color="k"))
ax.text(-352, 0, "200", rotation=90, fontsize=8, ha="center")
ax.plot([-320,-240],[100,100], lw=0.5, color="k"); ax.plot([-320,-240],[-100,-100], lw=0.5, color="k")
# 力偶转向（逆时针，箭头在弧的终点 300° 处沿切向）
arc_c = Arc((0,0), 220, 120, angle=0, theta1=60, theta2=300, lw=1.6, color="crimson")
ax.add_patch(arc_c)
t = math.radians(300)
pt = (110*math.cos(t), 60*math.sin(t))
tg = (-110*math.sin(t), 60*math.cos(t)); L = math.hypot(*tg); tg = (tg[0]/L, tg[1]/L)
arrow(ax, (pt[0]-28*tg[0], pt[1]-28*tg[1]), pt, lw=1.6, ms=14, color="crimson")
ax.text(-118, 62, "M1=206.3N·m(逆时针)", fontsize=8.5, color="crimson")
ax.text(-118, 34, "M2=124.0N·m(逆时针)", fontsize=8.5, color="crimson")
ax.text(-118, 6, "M=M1+M2=330.2N·m(逆时针)", fontsize=9, color="crimson", weight="bold")
ax.set_xlim(-420, 470); ax.set_ylim(-205, 240); ax.set_aspect("equal"); ax.axis("off")
fig.tight_layout()
fig.savefig(f"{OUT}/解答-2-7.png", bbox_inches="tight", facecolor="white")
plt.close(fig)
print("saved", f"{OUT}/解答-2-7.png")
