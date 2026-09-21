#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""2026-09-20 工程力学作业 2-2、2-7 解答图（精确坐标 + 自检）
运行: python3 工程力学/作业/2026-09-20-作业/制作解答图.py [2-2|2-7]   # 带参数只重画该题

⚠️ 2026-09-20 复核更正（2-7）：首版把滑轮布局误读成"四角矩形"（B 放右上角），得
M=330.2N·m 并误判教材 247.1N·m 为旧版遗留。教材图实际布局（像素级复核）：
A(0,200)、B(240,200)、D(0,0)、C(480,0)——A、D 同在左列，B 在中列，C 在右列；
底部尺寸链 240+240 是 AD列→B列→C列（不是板半宽）。按正确布局 M=247.1N·m 逆时针，
与教材答案页逐位一致。判例见 memory/ERRORS.md（2026-09-20 读图判例）。
"""
import math
import pathlib
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyArrowPatch, Arc, Circle, Rectangle, Polygon

_FONT_CANDIDATES = [
    "/home/user/opt/fonts/NotoSansSC-Bold.ttf",
    "/usr/local/lib/python3.11/dist-packages/mplfonts/fonts/NotoSansCJKsc-Regular.otf",
]
FONT_PATH = next((p for p in _FONT_CANDIDATES if pathlib.Path(p).exists()), None)
if FONT_PATH:
    font_manager.fontManager.addfont(FONT_PATH)
    plt.rcParams["font.family"] = font_manager.FontProperties(fname=FONT_PATH).get_name()
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
# 2-7 滑轮实际布局（教材图，2026-09-20 复核更正）：以 D 为原点，
# A(0,200)、B(240,200)、D(0,0)、C(480,0)；行距 200，尺寸链 240(AD列→B列)+240(B列→C列)。
A_,B_,C_,D_ = (0,200),(240,200),(480,0),(0,0)
F1 = (-400*c60, 400*s60); F2 = (400*c60, -400*c60)      # F1@B 左上60°、F2@D 右下60°（B-D绳）
F3 = (-300*c30, -300*s30); F4 = (300*c30, 300*s30)      # F3@A 左下30°、F4@C 右上30°（A-C绳）
mz = lambda p,f: p[0]*f[1]-p[1]*f[0]
M1 = mz(B_,F1)+mz(D_,F2); M2 = mz(A_,F3)+mz(C_,F4)
# 力偶臂复核：d1=240·sin60+200·cos60=307.85；d2=480·sin30+200·cos30=413.21
assert abs(M1-123138.4) < 1 and abs(M2-123961.5) < 1 and abs((M1+M2)/1000-247.1) < 0.01
assert abs(400*(240*s60+200*c60)-M1) < 1e-6 and abs(300*(480*s30+200*c30)-M2) < 1e-6
print("自检通过  R=%.1f kN  MO=%.1f kN·m  M1=%.1f N·mm  M2=%.1f N·mm  M=%.2f N·m(逆)"
      % (R, MO, M1, M2, (M1+M2)/1000))

# ================= 2-2 =================
def fig_2_2():
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

# ================= 2-7（2026-09-20 复核更正版）=================
def fig_2_7():
    fig, ax = plt.subplots(figsize=(7.0, 4.6), dpi=200)
    off = lambda p, u, L: (p[0]+u[0]*L, p[1]+u[1]*L)
    # 板（滑轮外接矩形再外扩；板形不影响计算，尺寸以滑轮位置为准）
    ax.add_patch(Rectangle((-80,-55), 640, 310, fc="#eaf6fd", ec="k", lw=1.4, zorder=1))
    for p, nm, dx, dy in ((A_,"A",-36,20),(B_,"B",22,20),(D_,"D",-40,-4),(C_,"C",24,-4)):
        ax.add_patch(Circle(p, 12, fc="white", ec="k", lw=1.2, zorder=4))
        ax.plot(*p, "+", ms=4, color="k", zorder=5)
        ax.text(p[0]+dx, p[1]+dy, nm, fontsize=10, zorder=5)
    # 两根绳的中间段（B-D、A-C，轮缘到轮缘）
    for p, q in ((B_,D_),(A_,C_)):
        ux, uy = q[0]-p[0], q[1]-p[1]
        L = math.hypot(ux,uy); ux, uy = ux/L, uy/L
        ax.plot(*zip(off(p,(ux,uy),12), off(q,(-ux,-uy),12)), lw=1.6, color="k", zorder=3)
    # 四个绳端的拉力（=作用在板上的力，沿自由端方向）
    for p, u, lab, lx, ly in ((B_,(-c60,s60),"F1=400N",-14,14),
                              (D_,(c60,-s60),"F2=400N",14,-16),
                              (A_,(-c30,-s30),"F3=300N",-16,-12),
                              (C_,(c30,s30),"F4=300N",16,10)):
        arrow(ax, off(p,u,14), off(p,u,230), lw=1.8)
        ax.text(*off(p,u,248), lab, fontsize=9, ha="center",
                va="bottom" if u[1] >= 0 else "top")
    # 角度标注（60°@B、60°@D、30°@A、30°@C，均自水平量起）
    ax.add_patch(Arc(B_, 70, 70, angle=0, theta1=120, theta2=180, lw=0.9, color="k"))
    ax.text(B_[0]-62, B_[1]+26, "60°", fontsize=8)
    ax.add_patch(Arc(D_, 70, 70, angle=0, theta1=-60, theta2=0, lw=0.9, color="k"))
    ax.text(D_[0]+36, D_[1]-34, "60°", fontsize=8)
    ax.add_patch(Arc(A_, 64, 64, angle=0, theta1=180, theta2=210, lw=0.9, color="k"))
    ax.text(A_[0]-66, A_[1]-22, "30°", fontsize=8)
    ax.add_patch(Arc(C_, 64, 64, angle=0, theta1=0, theta2=30, lw=0.9, color="k"))
    ax.text(C_[0]+42, C_[1]+20, "30°", fontsize=8)
    # 尺寸链：240(AD列→B列) + 240(B列→C列)；左侧 200（行距）
    for x in (0, 240, 480):
        ax.plot([x,x],[-60,-252], lw=0.5, color="k")
    ax.annotate("", xy=(0,-240), xytext=(240,-240), arrowprops=dict(arrowstyle="<->", lw=0.8, color="k"))
    ax.annotate("", xy=(240,-240), xytext=(480,-240), arrowprops=dict(arrowstyle="<->", lw=0.8, color="k"))
    ax.text(120, -262, "240", fontsize=8, ha="center", va="top")
    ax.text(360, -262, "240", fontsize=8, ha="center", va="top")
    ax.plot([0,-258],[0,0], lw=0.5, color="k"); ax.plot([0,-258],[200,200], lw=0.5, color="k")
    ax.annotate("", xy=(-250,0), xytext=(-250,200), arrowprops=dict(arrowstyle="<->", lw=0.8, color="k"))
    ax.text(-272, 100, "200", rotation=90, fontsize=8, ha="center", va="center")
    # 合力偶（逆时针，箭头在弧的终点 300° 处沿切向）
    cx, cy, rx, ry = 240, 100, 105, 60
    ax.add_patch(Arc((cx,cy), 2*rx, 2*ry, angle=0, theta1=60, theta2=300, lw=1.6, color="crimson"))
    t = math.radians(300)
    pt = (cx+rx*math.cos(t), cy+ry*math.sin(t))
    tg = (-rx*math.sin(t), ry*math.cos(t)); L = math.hypot(*tg); tg = (tg[0]/L, tg[1]/L)
    arrow(ax, (pt[0]-28*tg[0], pt[1]-28*tg[1]), pt, lw=1.6, ms=14, color="crimson")
    ax.text(-80, 330, "M1=123.1N·m(逆时针)", fontsize=8.5, color="crimson")
    ax.text(-80, 300, "M2=124.0N·m(逆时针)", fontsize=8.5, color="crimson")
    ax.text(-80, 266, "M=M1+M2=247.1N·m(逆时针)", fontsize=9, color="crimson", weight="bold")
    ax.set_xlim(-330, 760); ax.set_ylim(-300, 430); ax.set_aspect("equal"); ax.axis("off")
    fig.tight_layout()
    fig.savefig(f"{OUT}/解答-2-7.png", bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("saved", f"{OUT}/解答-2-7.png")

if __name__ == "__main__":
    ONLY = sys.argv[1] if len(sys.argv) > 1 else ""
    if not ONLY or ONLY == "2-2":
        fig_2_2()
    if not ONLY or ONLY == "2-7":
        fig_2_7()
