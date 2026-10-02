# -*- coding: utf-8 -*-
"""2026-09-29 批（1-4、3-6）解答图。先数值自检再作图（沿用仓库作图判例）。
仅用拉丁字母/数字标注，无需 CJK 字体。"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrow

OUT = "工程力学/作业/2026-09-29-作业/图/"

def arrow(ax, x, y, dx, dy, color="crimson", lw=2.0, hw=0.16):
    ax.add_patch(FancyArrow(x, y, dx, dy, width=0.02, head_width=hw,
                            length_includes_head=True, color=color, lw=lw))

# ─────────────────────────────────────────────────────────────
# 题 3-6：数值自检（与教材答案页逐项核对）
# 轴沿 y；A(0), C(400), B(1000), D(1400) mm
# F 在 C 处 +z，臂 200（x 向）；P 在 D 处 +x，臂 200（z 向）
F = 800.0
eq_ok = []
XA, ZA, XB, ZB = 320.0, -480.0, -1120.0, -320.0
# ΣF_x = XA+XB+P ; ΣF_z = ZA+ZB+F ; ΣM_x(A)=400*F+1000*ZB ; ΣM_z(A)=-1400*P-1000*XB
eq_ok.append(abs(XA+XB+F) < 1e-6)
eq_ok.append(abs(ZA+ZB+F) < 1e-6)
eq_ok.append(abs(400*F+1000*ZB) < 1e-6)
eq_ok.append(abs(-1400*F-1000*XB) < 1e-6)
# ΣM_y：-200F(来自F) +200P(来自P) =0
eq_ok.append(abs(-200*F+200*F) < 1e-6)
assert all(eq_ok), eq_ok
print("3-6 自检全过:", eq_ok)

fig, ax = plt.subplots(figsize=(11, 6.5))
ax.set_aspect("equal")
ax.axis("off")
# 轴（沿 y 画成水平）
ax.plot([0, 1400], [0, 0], color="0.2", lw=4, zorder=1)
for x, lab in [(0, "A"), (400, "C"), (1000, "B"), (1400, "D")]:
    ax.plot(x, 0, "o", ms=6, color="0.1")
    ax.text(x, -60, lab, fontsize=14, ha="center")
# 轴承 A、B 反力（按解出符号：XA=+320(+x→出纸面, 画成向右下示意), ZA=-480(向下)
# 这里用平面示意: x 方向画成垂直纸面向外用⊕/⊗不易, 改用侧视: 水平=y, 竖直=z
arrow(ax, 0, 0, 0, -120, "crimson"); ax.text(-40, -140, r"$Z_A$", fontsize=13, color="crimson")
arrow(ax, 1000, 0, 0, -80, "crimson"); ax.text(1010, -110, r"$Z_B$", fontsize=13, color="crimson")
# 主动力
arrow(ax, 400, -40, 0, 120, "navy"); ax.text(430, 90, r"$F$", fontsize=14, color="navy")
ax.text(360, -90, "arm 200 (+x)", fontsize=9, color="0.35")
# P 画成 +x (用 ⊙ 表示出纸面) 在 D, 臂200(z)
ax.plot(1400, 60, "o", ms=14, mfc="none", mec="navy")
ax.plot(1400, 60, ".", ms=4, color="navy")
ax.text(1430, 70, r"$P$ (+x)", fontsize=12, color="navy")
ax.text(1360, -90, "y=1400", fontsize=9, color="0.35")
for x, s in [(400, "400"), (1000, "600"), (1400, "400")]:
    pass
ax.annotate("", xy=(400, -180), xytext=(0, -180), arrowprops=dict(arrowstyle="<->"))
ax.text(200, -210, "400", fontsize=10, ha="center")
ax.annotate("", xy=(1000, -180), xytext=(400, -180), arrowprops=dict(arrowstyle="<->"))
ax.text(700, -210, "600", fontsize=10, ha="center")
ax.annotate("", xy=(1400, -180), xytext=(1000, -180), arrowprops=dict(arrowstyle="<->"))
ax.text(1200, -210, "400", fontsize=10, ha="center")
ax.set_title("3-6  F=P=800N, XA=320, ZA=-480, XB=-1120, ZB=-320 (N)", fontsize=11)
plt.tight_layout()
plt.savefig(OUT + "解答-3-6.png", dpi=200)
plt.close()
print("saved 解答-3-6.png")
