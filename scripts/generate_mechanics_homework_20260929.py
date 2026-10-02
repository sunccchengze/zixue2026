#!/usr/bin/env python3
"""9月29日作业的精确受力图：1-4的12个分离体、3-6的完整空间力系。

仓库根运行：.venv/bin/python scripts/generate_mechanics_homework_20260929.py
依赖：numpy、matplotlib、Pillow、pymupdf。可加 --question 1-4 或 --question 3-6。

先检验受力模型再绘图。1-4没有官方答案、也没有尺寸数据；图中几何仅为示意，
验算采用自选示意尺寸，不冒充题设。箭头长度不表示力大小。中文字体从PyMuPDF
内置CJK提取到忽略目录，不依赖沙箱里的系统字体。旧日期目录脚本保留为入口。
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass, field
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.patches import Circle
import numpy as np
from PIL import Image
import pymupdf

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "工程力学/作业/2026-09-29-作业/图"
TMP = ROOT / ".arena-tools/0929"
INK, REACTION, LOAD, LINK = "#34434f", "#b33f3f", "#126696", "#7656a0"
CJK = None


@dataclass
class Force:
    point: np.ndarray
    vector: np.ndarray
    symbol: str
    color: str = REACTION


@dataclass
class Body:
    title: str
    nodes: dict[str, tuple[float, float]]
    forces: list[Force]
    segments: list[list[tuple[float, float]]] = field(default_factory=list)
    circles: list[tuple[tuple[float, float], float]] = field(default_factory=list)
    ropes: list[list[tuple[float, float]]] = field(default_factory=list)


def force(point, vector, symbol, color=REACTION):
    return Force(np.asarray(point, dtype=float), np.asarray(vector, dtype=float), symbol, color)


def unit(p, q):
    v = np.asarray(q, dtype=float) - np.asarray(p, dtype=float)
    return v / np.linalg.norm(v)


def components(point, vector, x, y):
    return [force(point, (vector[0], 0), x), force(point, (0, vector[1]), y)]


def models_14(p=2.0):
    """外力、几何和作用点共同用于验算及绘制；p只是自检载荷，不是题设数值。"""
    bodies = {}
    # (a) AB受拉、BC受压；销钉上两杆力都具有向上的分量。
    A, B, C = (0, 3.9), (3.3, 2.5), (0, 0)
    n_ab, n_bc = unit(B, A), unit(C, B)
    n, m = np.linalg.solve(np.column_stack((n_ab, n_bc)), (0, p))
    ab, bc = n * n_ab, m * n_bc
    bodies["a-ab"] = Body("(a) 杆 AB · 二力杆", {"A": A, "B": B},
                           [force(A, ab, "N_{AB}"), force(B, -ab, "N_{AB}")], [[A, B]])
    bodies["a-bc"] = Body("(a) 杆 BC · 二力杆", {"B": B, "C": C},
                           [force(B, -bc, "N_{BC}"), force(C, bc, "N_{BC}")], [[B, C]])
    bodies["a-pin"] = Body("(a) 销钉 B", {"B": B},
                            [force(B, ab, "N_{AB}"), force(B, bc, "N_{BC}"),
                             force(B, (0, -p), "P", LOAD)])
    bodies["a-whole"] = Body("(a) 整体 · 只画外力", {"A": A, "B": B, "C": C},
                              [force(A, ab, "R_A"), force(C, bc, "R_C"),
                               force(B, (0, -p), "P", LOAD)], [[A, B], [B, C]])

    # (b) E与轮D顶部切线同高，绳另一端系于D轴，H左右各一条竖直绳。
    A, B, C, D, E = (0, 4.7), (2.8, 1.9), (0, 1.9), (4.8, 1.9), (1.85, 2.85)
    r = E[1] - D[1]
    H, rh = (D[0] + r / 2, -0.1), r / 2
    t = p / 2
    b_y = -2 * t * D[0] / B[0]
    b_x = -(B[0] * b_y + (A[1] - E[1]) * t) / (A[1] - B[1])
    on_ab = np.array((b_x, b_y))
    on_a = -on_ab - (t, 0)
    on_d = np.array((-t, -2 * t))  # 轮/销对杆CD的力。
    on_c = on_ab - on_d
    bodies["b-ab"] = Body("(b) 杆 AB", {"A": A, "E": E, "B": B},
                           components(A, on_a, "A_x", "A_y")
                           + components(B, on_ab, "B_x", "B_y")
                           + [force(E, (t, 0), "T", LOAD)], [[A, B]])
    bodies["b-cd"] = Body("(b) 杆 CD", {"C": C, "B": B, "D": D},
                           components(C, on_c, "C_x", "C_y")
                           + components(B, -on_ab, "B_x", "B_y")
                           + components(D, on_d, "D_x", "D_y"), [[C, D]])
    bodies["b-h"] = Body("(b) 动滑轮 H", {"H": H},
                          [force((H[0] - rh, H[1]), (0, t), "T", LOAD),
                           force((H[0] + rh, H[1]), (0, t), "T", LOAD),
                           force(H, (0, -p), "P", LOAD)], circles=[(H, rh)])
    bodies["b-d"] = Body("(b) 销钉与轮 D", {"D": D},
                          components(D, -on_d, "D_x", "D_y")
                          + [force((D[0], D[1] + r), (-t, 0), "T", LOAD),
                             force((D[0] + r, D[1]), (0, -t), "T", LOAD),
                             force(D, (0, -t), "T", LOAD)], circles=[(D, r)])
    weight = (H[0], H[1] - 1.1)
    weight_box = [(weight[0] - .25, weight[1] - .2), (weight[0] + .25, weight[1] - .2),
                  (weight[0] + .25, weight[1] + .2), (weight[0] - .25, weight[1] + .2),
                  (weight[0] - .25, weight[1] - .2)]
    bodies["b-whole"] = Body("(b) 整体 · 绳/销为内部", {"A": A, "C": C, "B": B, "D": D, "H": H},
                              components(A, on_a, "A_x", "A_y")
                              + components(C, on_c, "C_x", "C_y")
                              + [force(weight, (0, -p), "P", LOAD)],
                              [[A, B], [C, D], [H, weight], weight_box], [(D, r), (H, rh)],
                              [[E, (D[0], D[1] + r)], [D, (D[0], H[1])],
                               [(D[0] + r, D[1]), (D[0] + r, H[1])]])

    # (c) D连接两杆，故AB与CE两图均须画D的两分量，且等大反向。
    A, B, D, E, C = (0, 1.7), (6.2, 1.7), (3.4, 1.7), (3.4, 4.4), (3.4, -.9)
    r = .55
    n_eb = unit(B, E)
    s = (D[1] - C[1]) * p / ((E[1] - D[1]) * -n_eb[0])
    eb_on_ce = s * n_eb
    d_on_ce = np.array((p, p)) - eb_on_ce
    nb = (D[0] * d_on_ce[1] + B[0] * eb_on_ce[1]) / B[0]
    a = d_on_ce + eb_on_ce - (0, nb)
    c_top, c_right = (C[0], C[1] + r), (C[0] + r, C[1])
    rope_forces = [force(c_top, (-p, 0), "T", LOAD), force(c_right, (0, -p), "P", LOAD)]
    bodies["c-ab"] = Body("(c) 杆 AB 与销钉 B", {"A": A, "D": D, "B": B},
                           components(A, a, "A_x", "A_y")
                           + components(D, -d_on_ce, "D_x", "D_y")
                           + [force(B, (0, nb), "N_B"), force(B, -eb_on_ce, "F_{EB}", LINK)], [[A, B]])
    bodies["c-ce"] = Body("(c) 杆 CE 与滑轮", {"E": E, "D": D, "C": C},
                           components(D, d_on_ce, "D_x", "D_y")
                           + [force(E, eb_on_ce, "F_{EB}", LINK)] + rope_forces,
                           [[E, C]], [(C, r)])
    bodies["c-whole"] = Body("(c) 整体 · D/EB力不画", {"A": A, "D": D, "B": B, "E": E, "C": C},
                              components(A, a, "A_x", "A_y") + [force(B, (0, nb), "N_B")]
                              + rope_forces, [[A, B], [E, C], [E, B]], [(C, r)])
    return bodies


def model_36(p=800., arm_f=200., arm_p=200., yc=400., yb=1000., yd=1400.):
    """右手系：rF=(arm_f,yc,0)，rP=(0,yd,arm_p)，故My=-arm_f*F+arm_p*P。"""
    f = arm_p * p / arm_f
    xb, zb = -yd * p / yb, -yc * f / yb
    xa, za = -p - xb, -f - zb
    loads = [force((0, 0, 0), (xa, 0, 0), "X_A"), force((0, 0, 0), (0, 0, za), "Z_A"),
             force((0, yb, 0), (xb, 0, 0), "X_B"), force((0, yb, 0), (0, 0, zb), "Z_B"),
             force((arm_f, yc, 0), (0, 0, f), "F", LOAD),
             force((0, yd, arm_p), (p, 0, 0), "P", LOAD)]
    return loads, {"F": f, "X_A": xa, "Z_A": za, "X_B": xb, "Z_B": zb, "P": p}


def equilibrium(loads):
    ndim = len(loads[0].vector)
    total = sum((load.vector for load in loads), np.zeros(ndim))
    scale = max(1., sum(np.linalg.norm(load.vector) for load in loads))
    assert np.linalg.norm(total) < 1e-10 * scale, total
    if ndim == 2:
        moments = [load.point[0] * load.vector[1] - load.point[1] * load.vector[0] for load in loads]
        assert abs(sum(moments)) < 1e-10 * max(1., sum(map(abs, moments))), moments
    else:
        moments = [np.cross(load.point, load.vector) for load in loads]
        assert np.linalg.norm(sum(moments)) < 1e-10 * max(1., sum(np.linalg.norm(m) for m in moments))


def self_check():
    for p in (1., 2., 731.):
        bodies = models_14(p)
        assert len(bodies) == 12
        for body in bodies.values():
            equilibrium(body.forces)
    # 使用不等的F/P力臂，避免用F替P的恒等式“自检”。
    for p, af, ap in ((800., 200., 200.), (730., 180., 290.), (41., 320., 150.)):
        equilibrium(model_36(p, af, ap)[0])
    assert model_36()[1] == {"F": 800., "X_A": 320., "Z_A": -480., "X_B": -1120., "Z_B": -320., "P": 800.}
    print("PASS：1-4十二个分离体的示意模型平衡；3-6六个外力的完整向量平衡与题设数值")


def prepare():
    global CJK
    OUT.mkdir(parents=True, exist_ok=True)
    TMP.mkdir(parents=True, exist_ok=True)
    font_path = TMP / "DroidSansFallback.ttf"
    if not font_path.exists():
        font_path.write_bytes(pymupdf.Font("china-s").buffer)
    CJK = FontProperties(fname=font_path)
    plt.rcParams["mathtext.fontset"] = "dejavusans"
    plt.rcParams["font.size"] = 13
    plt.rcParams["figure.facecolor"] = "white"


def chinese(ax, x, y, text, size=12, **kw):
    return ax.text(x, y, text, fontsize=size, fontproperties=CJK, **kw)


def arrow(ax, start, vector, label, color, length=1.05, label_pos=None, size=13):
    start = np.asarray(start, float)
    u = np.asarray(vector, float) / np.linalg.norm(vector)
    end = start + length * u
    ax.annotate("", xy=end, xytext=start,
                arrowprops=dict(arrowstyle="-|>", color=color, lw=2, mutation_scale=17), zorder=5)
    pos = end + .18 * u if label_pos is None else np.asarray(label_pos)
    ha = "right" if u[0] < -.3 else "left" if u[0] > .3 else "center"
    va = "bottom" if u[1] > .3 else "top" if u[1] < -.3 else "center"
    if label_pos is None and abs(u[1]) < .1:
        # 内向的两项水平分量常挤在同一段杆上；分列箭头上下，不能盖掉C_x等标签。
        above = u[0] > 0
        pos = start + .55 * length * u + (0, .24 if above else -.24)
        ha, va = "center", "bottom" if above else "top"
    ax.text(*pos, label, color=color, fontsize=size, ha=ha, va=va,
            bbox=dict(facecolor="white", edgecolor="none", pad=.15), zorder=6)
    return end, pos


def plot_body(ax, body):
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(body.title, fontproperties=CJK, fontsize=14, pad=16)
    extents = []
    for points in body.segments:
        points = np.asarray(points)
        ax.plot(points[:, 0], points[:, 1], color=INK, lw=3, zorder=1)
        extents.extend(points)
    for points in body.ropes:
        points = np.asarray(points)
        ax.plot(points[:, 0], points[:, 1], color="#98a5af", lw=1.3, zorder=1)
        extents.extend(points)
    for center, radius in body.circles:
        ax.add_patch(Circle(center, radius, edgecolor=INK, facecolor="none", lw=2))
        extents.extend((np.array(center) - radius, np.array(center) + radius))
    for name, point in body.nodes.items():
        ax.plot(*point, "o", ms=4.5, color=INK, zorder=7)
        at_node = [load for load in body.forces if np.allclose(load.point, point)]
        horizontal = [load for load in at_node if abs(load.vector[1]) < 1e-10 and load.vector[0] != 0]
        vertical = [load for load in at_node if abs(load.vector[0]) < 1e-10 and load.vector[1] != 0]
        dx = (-.16 if horizontal[0].vector[0] > 0 else .16) if horizontal else -.13
        dy = (-.25 if vertical[0].vector[1] > 0 else .20) if vertical else -.23
        ax.text(point[0] + dx, point[1] + dy, name, fontsize=12,
                ha="right" if dx < 0 else "left", va="top" if dy < 0 else "bottom",
                bbox=dict(facecolor="white", edgecolor="none", pad=.1), zorder=8)
        extents.extend((point, (point[0] + 2 * dx, point[1] + 2 * dy)))
    for load in body.forces:
        end, pos = arrow(ax, load.point, load.vector, f"${load.symbol}$", load.color)
        extents.extend((load.point, end, pos))
    points = np.asarray(extents)
    lo, hi = points.min(axis=0), points.max(axis=0)
    ax.set_xlim(lo[0] - .7, hi[0] + .7)
    ax.set_ylim(lo[1] - .6, hi[1] + .6)


def save_group(bodies, group, shape, figsize):
    fig, axes = plt.subplots(*shape, figsize=figsize)
    axes = np.asarray(axes).ravel()
    selected = [body for key, body in bodies.items() if key.startswith(group + "-")]
    for ax, body in zip(axes, selected):
        plot_body(ax, body)
    for ax in axes[len(selected):]:
        ax.axis("off")
        chinese(ax, .08, .82, "动滑轮 H：2T = P", 15, transform=ax.transAxes)
        chinese(ax, .08, .63, "轮 D：顶部、右侧、轴心各一项 T", 12, transform=ax.transAxes)
        chinese(ax, .08, .44, "B、D两侧的同名分量等大反向", 12, transform=ax.transAxes)
        chinese(ax, .08, .25, "整体只保留 A、C 支反力和 P", 12, transform=ax.transAxes)
    fig.suptitle(f"习题 1-4（{group}）· 指定物体的完整受力图", fontproperties=CJK, fontsize=21, y=.98)
    fig.text(.04, .045, "红：支座/铰链反力   蓝：外载/绳张力   紫：二力杆传力；箭头长短不表示力大小。", fontproperties=CJK, fontsize=11)
    fig.text(.04, .01, "铰链分量采用图示正向；同名内部力在两物体上等大反向。示意图无题设尺寸，不按比例。", fontproperties=CJK, fontsize=10)
    fig.subplots_adjust(left=.025, right=.975, top=.87, bottom=.14, wspace=.20, hspace=.30)
    fig.savefig(OUT / f"解答-1-4-{group}.png", dpi=180)
    plt.close(fig)


def draw_14():
    bodies = models_14()
    save_group(bodies, "a", (1, 4), (16, 4.7))
    save_group(bodies, "b", (2, 3), (15, 9.5))
    save_group(bodies, "c", (1, 3), (15, 6.3))
    # 保留旧链接，但替换错误的旧总图；正文用三个分图，避免12图挤在一张里。
    images = []
    for group in "abc":
        with Image.open(OUT / f"解答-1-4-{group}.png") as im:
            rgb = im.convert("RGB")
            images.append(rgb.resize((2700, round(rgb.height * 2700 / rgb.width)), Image.Resampling.LANCZOS))
    combined = Image.new("RGB", (2700, sum(im.height for im in images)), "white")
    y = 0
    for im in images:
        combined.paste(im, (0, y))
        y += im.height
    combined.save(OUT / "解答-1-4.png")
    print("saved：解答-1-4-a/b/c.png 与兼容旧链接的总图")


def project(point):
    """空间示意投影：+x向右下，+y向右上，+z竖直向上。坐标单位mm。"""
    x, y, z = np.asarray(point) / 100
    return np.array((.60 * x + .95 * y, -.45 * x + .28 * y + z))


def draw_36():
    loads, values = model_36()
    fig, ax = plt.subplots(figsize=(12.5, 7.0))
    ax.set_aspect("equal")
    ax.axis("off")
    points = {"A": (0, 0, 0), "C": (0, 400, 0), "B": (0, 1000, 0), "D": (0, 1400, 0)}
    a, d = project(points["A"]), project(points["D"])
    ax.plot((a[0], d[0]), (a[1], d[1]), color=INK, lw=4, zorder=1)
    for name, point in points.items():
        pos = project(point)
        ax.plot(*pos, "o", color=INK, ms=5, zorder=5)
        ax.text(pos[0] - .20, pos[1] + .20, name, fontsize=14, color=INK,
                bbox=dict(facecolor="white", edgecolor="none", pad=.1), zorder=6)
    # 实际作用点与轴线的两项200mm偏心距均保留，不将偏心力错误搬到轴线上。
    for center, application, label, label_offset in [
        (points["C"], (200, 400, 0), "200 mm (+x)", (.35, -.90)),
        (points["D"], (0, 1400, 200), "200 mm (+z)", (-1.85, -.10)),
    ]:
        p0, p1 = project(center), project(application)
        ax.plot((p0[0], p1[0]), (p0[1], p1[1]), "--", color="#8998a4", lw=1.5)
        ax.plot(*p1, "o", color=LOAD, ms=4)
        ax.text(*((p0 + p1) / 2 + label_offset), label, color="#61727e", fontsize=11)
    lengths = {"X_A": 1.5, "Z_A": 1.7, "X_B": 1.8, "Z_B": 1.6, "F": 2.1, "P": 2.0}
    label_positions = {"X_A": (1.30, -.45), "Z_A": (-.15, -1.85),
                       "X_B": (7.72, 4.00), "Z_B": (9.70, 1.05),
                       "F": (5.22, 2.35), "P": (15.10, 4.88)}
    for load in loads:
        magnitude = abs(values[load.symbol])
        symbol = f"|{load.symbol}|" if values[load.symbol] < 0 else load.symbol
        label = f"${symbol}={magnitude:g}$ N"
        arrow(ax, project(load.point), project(load.vector), label, load.color,
              length=lengths[load.symbol], label_pos=label_positions[load.symbol], size=13)
    # 轴向尺寸链。
    offset = np.array((0, -2.55))
    for name in points:
        q = project(points[name])
        ax.plot((q[0], q[0]), (q[1] - .15, q[1] + offset[1] - .10), color="#b8c2c9", lw=.8, zorder=0)
    for left, right, distance in (("A", "C", 400), ("C", "B", 600), ("B", "D", 400)):
        p0, p1 = project(points[left]) + offset, project(points[right]) + offset
        ax.annotate("", xy=p1, xytext=p0, arrowprops=dict(arrowstyle="<->", lw=1, color=INK))
        ax.text(*((p0 + p1) / 2 + (0, -.40)), f"{distance} mm", fontsize=12, ha="center", color=INK)
    # 独立坐标图，避免与支座处的力箭头混淆。
    origin = np.array((.6, 3.85))
    for direction, label in (((1, 0, 0), "$+x$"), ((0, 1, 0), "$+y$"), ((0, 0, 1), "$+z$")):
        arrow(ax, origin, project(direction), label, "#7d8c97", length=.95, size=11)
    chinese(ax, .3, 6.15, "习题 3-6 · 完整受力图（箭头按计算后的实际方向）", 19)
    chinese(ax, .3, 5.55, "轴承只有 X、Z 两分量；红色为轴承反力，蓝色为凸轮上的外力。", 12)
    chinese(ax, .02, .055, "图示大小：F = 800 N；A处 320 N 沿+x、480 N 沿-z；B处 1120 N 沿-x、320 N 沿-z。", 11, transform=ax.transAxes)
    chinese(ax, .02, .01, "有符号分量：XA=320，ZA=-480，XB=-1120，ZB=-320（N）。箭头长度不表示力大小。", 10, transform=ax.transAxes)
    ax.set_xlim(-1.3, 18)
    ax.set_ylim(-4.0, 7.1)
    fig.subplots_adjust(left=.03, right=.98, top=.99, bottom=.10)
    fig.savefig(OUT / "解答-3-6.png", dpi=180)
    plt.close(fig)
    print("saved：解答-3-6.png（四个轴承分量、两项偏心力及完整尺寸链）")


def main(questions=("1-4", "3-6")):
    self_check()
    prepare()
    if "1-4" in questions:
        draw_14()
    if "3-6" in questions:
        draw_36()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--question", choices=("1-4", "3-6"))
    args = parser.parse_args()
    main((args.question,) if args.question else ("1-4", "3-6"))
