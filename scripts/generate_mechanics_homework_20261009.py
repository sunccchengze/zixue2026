#!/usr/bin/env python3
"""10月9日作业（2-12(a)、2-14、2-16）：裁原题图、先数值自检再画解答图。

仓库根运行：.venv/bin/python scripts/generate_mechanics_homework_20261009.py
依赖：numpy、matplotlib、Pillow、pymupdf。中文字体从 PyMuPDF 内置 CJK 提取到
忽略目录 .arena-tools/，不依赖沙箱系统字体。

页码换算（与历批一致，均从 1 计）：框架版 PDF 页＝教材页＋5；原件一卷 PDF 页＝教材页＋8。
2-12：教材53 / 框架58 / 原件61；2-14、2-16：教材54 / 框架59 / 原件62。
原题图在框架版与原件一卷两源 72 dpi 像素一致（本脚本断言），裁图取 220 dpi。

自检先于作图：三题各自独立列平衡方程用 numpy 解线性系统，与教材答案页
（框架版 PDF 第 289 页）逐位对照；对不上一律 raise，不产出图。
解答图为受力分析示意，箭头长短不表示力的大小。
"""
from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import numpy as np
import pymupdf

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "工程力学/作业/2026-10-09-作业/图"
TMP = ROOT / ".arena-tools/1009"
FRAME = ROOT / "工程力学/框架版教材/工程力学（框架汇编版）.pdf"
VOL1 = ROOT / "工程力学/资料原件/工程力学（第三版）_1-130.pdf"
INK, REACTION, LOAD, COUPLE = "#34434f", "#b33f3f", "#126696", "#7656a0"
CJK = None

# 教材页 -> (框架版1-based页, 原件一卷1-based页)
PAGES = {53: (58, 61), 54: (59, 62)}
# 裁图框（框架版 PDF 点坐标）
CROPS = {
    "题2-12a.png": (53, (100, 562, 266, 640)),
    "题2-14.png": (54, (185, 185, 350, 300)),
    "题2-16.png": (54, (78, 350, 242, 478)),
}


def prepare():
    global CJK
    TMP.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    font_path = TMP / "DroidSansFallback.ttf"
    if not font_path.exists():
        font_path.write_bytes(pymupdf.Font("china-s").buffer)
    CJK = FontProperties(fname=font_path)
    plt.rcParams["mathtext.fontset"] = "dejavusans"
    plt.rcParams["font.size"] = 12


def txt(ax, x, y, s, size=12, **kw):
    return ax.text(x, y, s, fontsize=size, fontproperties=CJK, **kw)


# ---------------------------------------------------------------- 自检
def solve_212a():
    """梁 AB：A 铰支、B 滚支；q 均布于 [0,2a]；x=2a 处逆时针力偶 M=qa^2。
    未知 (F_A, F_B)，均竖直向上；无水平载荷故 F_Ax=0。"""
    q, a = 1.0, 1.0
    M = q * a * a  # 逆时针为正
    A = np.array([[1.0, 1.0],          # ΣFy
                  [0.0, 3 * a]])       # ΣM_A（逆正）
    b = np.array([2 * q * a,           # 均布合力 2qa 向下
                  2 * q * a * a - M])  # 均布对A顺时针 2qa^2，力偶逆 +M 移项
    FA, FB = np.linalg.solve(A, b)
    return FA, FB


def solve_214(P=1.0, l=1.0, a=0.4, alpha_deg=75.0, h=0.8):
    """折叠梯：脚 B、C 在光滑地面（竖直反力）；绳 DE 水平，A 到绳的竖直距离 h；
    人重 P 在右腿 AC 上、距脚 C 沿腿 a；腿长 l、与地面夹角 alpha。
    未知 (N_B, N_C, F_T, A_x, A_y)。"""
    al = np.radians(alpha_deg)
    H = l * np.sin(al)          # 顶点高度
    xc = l * np.cos(al)         # C 的 x（B 在 -xc）
    xK = xc - a * np.cos(al)    # K 的 x
    yE = H - h                  # 绳的高度
    A = np.zeros((5, 5)); b = np.zeros(5)
    # 整体 ΣFy
    A[0, 0] += 1; A[0, 1] += 1; b[0] = P
    # 整体 ΣM_B（逆正）：N_C*(2xc) - P*(xK+xc)
    A[1, 1] += 2 * xc; b[1] = P * (xK + xc)
    # 右腿 ΣFx：A_x - F_T = 0
    A[2, 3] += 1; A[2, 2] -= 1
    # 右腿 ΣFy：A_y + N_C - P = 0
    A[3, 4] += 1; A[3, 1] += 1; b[3] = P
    # 右腿 ΣM_A（逆正）：xc*N_C - P*xK - F_T*(H-yE)，xK 为 K 的横坐标（A 在 x=0）
    A[4, 1] += xc; A[4, 2] -= (H - yE); b[4] = P * xK
    NB, NC, FT, Ax, Ay = np.linalg.solve(A, b)
    return NB, NC, FT, Ax, Ay, dict(al=al, H=H, xc=xc, xK=xK, yE=yE)


def solve_216(F=12.0, q=8.0):
    """三铰刚架：A(0,0)、B(12,0) 固定铰；顶梁 y=8，铰 C(6,8)；
    q 布满左半顶梁 [0,6]（合力48，作用 x=3）；F 向下作用 x=8。
    未知 (FAx, FAy, FBx, FBy, FCx, FCy)，FC 为左半对右半的作用力。"""
    W = q * 6.0
    A = np.zeros((6, 6)); b = np.zeros(6)
    # 整体 ΣFx / ΣFy / ΣM_A
    A[0, 0] += 1; A[0, 2] += 1
    A[1, 1] += 1; A[1, 3] += 1; b[1] = W + F
    A[2, 3] += 12.0; b[2] = W * 3.0 + F * 8.0
    # 右半 ΣFx / ΣFy / ΣM_C（C=(6,8)，B 相对 C=(6,-8)，F 作用点相对 C=(2,0)）
    A[3, 4] += 1; A[3, 2] += 1
    A[4, 5] += 1; A[4, 3] += 1; b[4] = F
    A[5, 3] += 6.0; A[5, 2] += 8.0; b[5] = F * 2.0
    return np.linalg.solve(A, b)


def self_check():
    FA, FB = solve_212a()
    assert abs(FA - 5 / 3) < 1e-12 and abs(FB - 1 / 3) < 1e-12, (FA, FB)
    NB, NC, FT, Ax, Ay, g = solve_214()
    P, l, a, al, h = 1.0, 1.0, 0.4, g["al"], 0.8
    assert abs(FT - P * a * np.cos(al) / (2 * h)) < 1e-12, FT
    assert abs(NB - P * a / (2 * l)) < 1e-12 and abs(NC - P * (2 * l - a) / (2 * l)) < 1e-12
    v = solve_216()
    want = [12.0, 40.0, -12.0, 20.0, 12.0, -8.0]
    assert np.allclose(v, want, atol=1e-9), v
    print("自检通过：2-12(a) F_A=5qa/3、F_B=qa/3；2-14 F_T=Pa·cosα/(2h)；"
          "2-16 (12,40,-12,20,12,-8) 与教材答案页一致")


# ---------------------------------------------------------------- 裁图
def crop_figures():
    frame = pymupdf.open(FRAME)
    vol1 = pymupdf.open(VOL1)
    for book_page, (fp, vp) in PAGES.items():
        a, bsrc = frame[fp - 1], vol1[vp - 1]
        assert a.get_pixmap(dpi=72).samples == bsrc.get_pixmap(dpi=72).samples, \
            f"双源不一致：教材{book_page} 框架{fp} 原件{vp}"
    for name, (book_page, box) in CROPS.items():
        fp = PAGES[book_page][0]
        frame[fp - 1].get_pixmap(dpi=220, clip=pymupdf.Rect(*box)).save(OUT / name)
        print("裁图", OUT / name)
    frame.close(); vol1.close()


# ---------------------------------------------------------------- 作图
def _arrow(ax, p, v, color, width=2.2, head=14):
    ax.annotate("", xy=(p[0] + v[0], p[1] + v[1]), xytext=p,
                arrowprops=dict(arrowstyle=f"-|>,head_width=.28,head_length=.55",
                                color=color, lw=width,
                                mutation_scale=head))


def _support_pin(ax, p, roller=False):
    x, y = p
    ax.plot([x, x - .22, x + .22, x], [y, y - .34, y - .34, y], color=INK, lw=1.6)
    if roller:
        for dx in (-.11, .11):
            ax.add_patch(plt.Circle((x + dx, y - .44), .075, fill=False, color=INK, lw=1.4))
        yy = y - .53
    else:
        yy = y - .36
    ax.plot([x - .34, x + .34], [yy, yy], color=INK, lw=1.6)
    for i in range(6):
        xx = x - .32 + i * .128
        ax.plot([xx, xx - .1], [yy, yy - .12], color=INK, lw=1)
    ax.add_patch(plt.Circle(p, .07, color="white", ec=INK, lw=1.6, zorder=5))


def _udl(ax, x0, x1, y, n=13, ln=.55):
    ax.plot([x0, x1], [y + ln, y + ln], color=LOAD, lw=1.6)
    for x in np.linspace(x0, x1, n):
        _arrow(ax, (x, y + ln), (0, -ln + .06), LOAD, width=1.3, head=9)


def draw_212a():
    fig, ax = plt.subplots(figsize=(9.4, 4.3))
    A, C, B = (0, 0), (2, 0), (3, 0)
    ax.plot([A[0], B[0]], [0, 0], color=INK, lw=3)
    _support_pin(ax, A); _support_pin(ax, B, roller=True)
    _udl(ax, 0, 2, 0)
    txt(ax, 1.0, .78, r"$q$", 15, color=LOAD, ha="center")
    # 逆时针力偶 M=qa^2（上←、下→）
    ax.plot([2, 2], [-.78, .98], color=COUPLE, lw=2.2)
    _arrow(ax, (2, .98), (-.5, 0), COUPLE); _arrow(ax, (2, -.78), (.5, 0), COUPLE)
    txt(ax, 2.14, 1.02, r"$M=qa^2$（逆）", 13, color=COUPLE)
    # 反力
    _arrow(ax, A, (0, 1.15), REACTION); txt(ax, -.20, 1.20, r"$F_A=\frac{5}{3}qa$", 14, color=REACTION, ha="right")
    _arrow(ax, B, (0, .72), REACTION); txt(ax, 3.12, .62, r"$F_B=\frac{1}{3}qa$", 14, color=REACTION)
    txt(ax, -.06, -.95, "A", 14, color=INK); txt(ax, 3.06, -.95, "B", 14, color=INK)
    ax.annotate("", xy=(0, -1.35), xytext=(2, -1.35), arrowprops=dict(arrowstyle="<->", color=INK, lw=1))
    txt(ax, 1.0, -1.62, r"$2a$", 13, ha="center", color=INK)
    ax.annotate("", xy=(2, -1.35), xytext=(3, -1.35), arrowprops=dict(arrowstyle="<->", color=INK, lw=1))
    txt(ax, 2.5, -1.62, r"$a$", 13, ha="center", color=INK)
    ax.set_title("习题 2-12(a) · 梁 AB 受力图（A 铰支、B 滚支；$F_{Ax}=0$）", fontproperties=CJK, fontsize=14, pad=14)
    ax.set_xlim(-1.1, 4.3); ax.set_ylim(-2.0, 1.6); ax.axis("off")
    fig.tight_layout(); fig.savefig(OUT / "解答-2-12a.png", dpi=180); plt.close(fig)


def draw_214():
    al = np.radians(72.0); l, a, h = 3.0, 1.1, 2.0
    H = l * np.sin(al); xc = l * np.cos(al)
    A = (0.0, H); B = (-xc, 0.0); C = (xc, 0.0)
    yE = H - h
    tE = (H - yE) / np.sin(al)          # E 沿腿距 A
    E = (tE * np.cos(al), yE); D = (-E[0], yE)
    tK = l - a
    K = (tK * np.cos(al), H - tK * np.sin(al))
    fig, axes = plt.subplots(1, 2, figsize=(12.6, 5.4))

    ax = axes[0]
    for p, q in ((A, B), (A, C)):
        ax.plot([p[0], q[0]], [p[1], q[1]], color=INK, lw=3)
    ax.plot([D[0], E[0]], [yE, yE], color=LOAD, lw=1.8)
    ax.add_patch(plt.Circle(A, .07, color="white", ec=INK, lw=1.8, zorder=5))
    ax.plot([B[0] - .35, C[0] + .35], [0, 0], color=INK, lw=2)
    for i in range(14):
        xx = B[0] - .3 + i * .16
        ax.plot([xx, xx - .1], [0, -.14], color=INK, lw=1)
    _arrow(ax, K, (0, -1.0), LOAD); txt(ax, K[0] + .12, K[1] - .5, r"$P$", 15, color=LOAD)
    _arrow(ax, B, (0, .8), REACTION); txt(ax, B[0] - .8, B[1] + .55, r"$F_{NB}=\frac{Pa}{2l}$", 13, color=REACTION)
    _arrow(ax, C, (0, 1.25), REACTION); txt(ax, C[0] + .12, C[1] + .95, r"$F_{NC}=\frac{(2l-a)P}{2l}$", 13, color=REACTION)
    for name, p in (("A", A), ("B", B), ("C", C)):
        txt(ax, p[0] - .28, p[1] + .12, name, 13, color=INK)
    txt(ax, K[0] - .68, K[1] + .02, "K", 13, color=INK)
    txt(ax, D[0] - .34, D[1] - .34, "D", 13, color=INK)
    txt(ax, E[0] - .16, E[1] - .36, "E", 13, color=INK)
    ax.set_title("整体：地面光滑，只有竖直反力", fontproperties=CJK, fontsize=13, pad=10)
    ax.set_xlim(-2.6, 2.9); ax.set_ylim(-.8, H + 1.1); ax.axis("off")

    ax = axes[1]
    ax.plot([A[0], C[0]], [A[1], C[1]], color=INK, lw=3)
    ax.add_patch(plt.Circle(A, .07, color="white", ec=INK, lw=1.8, zorder=5))
    ax.plot([C[0] - .3, C[0] + .3], [0, 0], color=INK, lw=2)
    _arrow(ax, K, (0, -1.0), LOAD); txt(ax, K[0] + .12, K[1] - .5, r"$P$", 15, color=LOAD)
    _arrow(ax, C, (0, 1.25), REACTION); txt(ax, C[0] + .12, C[1] + .95, r"$F_{NC}$", 13, color=REACTION)
    _arrow(ax, E, (-.95, 0), LOAD); txt(ax, E[0] - .55, E[1] + .16, r"$F_T$", 14, color=LOAD)
    _arrow(ax, A, (.85, 0), REACTION); txt(ax, A[0] + .55, A[1] + .18, r"$F_{Ax}$", 13, color=REACTION)
    _arrow(ax, A, (0, .8), REACTION); txt(ax, A[0] + .12, A[1] + .5, r"$F_{Ay}$", 13, color=REACTION)
    for name, p in (("A", A), ("C", C)):
        txt(ax, p[0] - .28, p[1] + .12, name, 13, color=INK)
    txt(ax, K[0] - .68, K[1] + .02, "K", 13, color=INK)
    txt(ax, E[0] - .16, E[1] - .36, "E", 13, color=INK)
    ax.annotate("", xy=(xc + .55, H), xytext=(xc + .55, yE),
                arrowprops=dict(arrowstyle="<->", color=INK, lw=1))
    txt(ax, xc + .68, (H + yE) / 2, r"$h$", 13, color=INK)
    ax.set_title("右腿 AC：绳张力、铰A两分量、$F_{NC}$、$P$", fontproperties=CJK, fontsize=13, pad=10)
    ax.set_xlim(-1.7, 2.9); ax.set_ylim(-.8, H + 1.1); ax.axis("off")
    fig.suptitle(r"习题 2-14 · 折叠梯受力图（绳中拉力 $F_T=\dfrac{Pa\cos\alpha}{2h}$）",
                 fontproperties=CJK, fontsize=16, y=.99)
    fig.tight_layout(rect=(0, 0, 1, .94)); fig.savefig(OUT / "解答-2-14.png", dpi=180); plt.close(fig)


def draw_216():
    A, B = (0, 0), (12, 0); TL, TR, C = (0, 8), (12, 8), (6, 8); xF = 8.0
    fig, axes = plt.subplots(1, 2, figsize=(13.2, 6.0))

    ax = axes[0]
    for p, q in ((A, TL), (TL, TR), (TR, B)):
        ax.plot([p[0], q[0]], [p[1], q[1]], color=INK, lw=3)
    ax.add_patch(plt.Circle(C, .16, color="white", ec=INK, lw=1.8, zorder=5))
    _support_pin(ax, A); _support_pin(ax, B)
    _udl(ax, 0, 6, 8, n=13, ln=1.1)
    txt(ax, 3.0, 9.5, r"$q=8\,\mathrm{kN/m}$", 13, color=LOAD, ha="center")
    _arrow(ax, (xF, 9.6), (0, -1.4), LOAD); txt(ax, xF - .9, 9.5, r"$F=12\,\mathrm{kN}$", 13, color=LOAD)
    _arrow(ax, A, (1.5, 0), REACTION); txt(ax, A[0] + .5, A[1] - .75, r"$F_{Ax}=12$", 12.5, color=REACTION)
    _arrow(ax, A, (0, 2.0), REACTION); txt(ax, A[0] - .35, A[1] + 2.05, r"$F_{Ay}=40$", 12.5, color=REACTION, ha="right")
    _arrow(ax, B, (-1.5, 0), REACTION); txt(ax, B[0] - 2.4, B[1] - .75, r"$F_{Bx}=12$", 12.5, color=REACTION)
    _arrow(ax, B, (0, 1.4), REACTION); txt(ax, B[0] + .5, B[1] + 1.0, r"$F_{By}=20$", 12.5, color=REACTION)
    for name, p in (("A", A), ("B", B), ("C", C)):
        txt(ax, p[0] + .25, p[1] + .3, name, 14, color=INK)
    ax.set_title("整体：四个支座分量（kN）", fontproperties=CJK, fontsize=13, pad=10)
    ax.set_xlim(-3.2, 15.2); ax.set_ylim(-2.0, 10.6); ax.axis("off")

    ax = axes[1]
    for p, q in ((C, TR), (TR, B)):
        ax.plot([p[0], q[0]], [p[1], q[1]], color=INK, lw=3)
    ax.add_patch(plt.Circle(C, .16, color="white", ec=INK, lw=1.8, zorder=5))
    _support_pin(ax, B)
    _arrow(ax, (xF, 9.6), (0, -1.4), LOAD); txt(ax, xF - .9, 9.5, r"$F$", 14, color=LOAD)
    _arrow(ax, C, (1.5, 0), REACTION); txt(ax, C[0] + .55, C[1] + .55, r"$F_{Cx}=12$", 12.5, color=REACTION)
    _arrow(ax, C, (0, -1.5), REACTION); txt(ax, C[0] - .40, C[1] - 1.85, r"$F_{Cy}=8$", 12.5, color=REACTION, ha="right")
    _arrow(ax, B, (-1.5, 0), REACTION); txt(ax, B[0] - 2.4, B[1] - .75, r"$F_{Bx}=12$", 12.5, color=REACTION)
    _arrow(ax, B, (0, 1.4), REACTION); txt(ax, B[0] + .5, B[1] + 1.0, r"$F_{By}=20$", 12.5, color=REACTION)
    txt(ax, B[0] + .25, B[1] + .3, "B", 14, color=INK)
    txt(ax, C[0] + .22, C[1] - .85, "C", 14, color=INK)
    ax.set_title("右半（C 铰右侧）：$F_{Cx}$、$F_{Cy}$ 为左半对它的作用", fontproperties=CJK, fontsize=13, pad=10)
    ax.set_xlim(2.6, 15.2); ax.set_ylim(-2.0, 10.6); ax.axis("off")
    fig.suptitle("习题 2-16 · 三铰刚架受力图（坐标：x 向右、y 向上，单位 kN）",
                 fontproperties=CJK, fontsize=16, y=.99)
    fig.tight_layout(rect=(0, 0, 1, .94)); fig.savefig(OUT / "解答-2-16.png", dpi=180); plt.close(fig)


def main():
    self_check()
    prepare()
    crop_figures()
    draw_212a()
    draw_214()
    draw_216()
    print("完成：", sorted(p.name for p in OUT.glob("*.png")))


if __name__ == "__main__":
    main()
