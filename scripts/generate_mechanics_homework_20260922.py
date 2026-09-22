#!/usr/bin/env python3
"""9月22日习题1-2：教材裁图、七张精确受力图与一页作业单。

在仓库根运行：.venv/bin/python scripts/generate_mechanics_homework_20260922.py
依赖：pymupdf、python-docx、Pillow、matplotlib、numpy。
复用仓级作业单/审计/预览工具，不修改教材；字体与中间产物仅写入忽略目录。
自检为约束方向/切线/作用反作用及示例平衡检查，不冒充教材答案核验。
"""
from pathlib import Path
import json
import math
import sys

import pymupdf
import numpy as np
from PIL import Image
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.patches import Circle

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import generate_homework_sheet_docx as sheet
import docx_preview_pdf as preview

OUT = ROOT / '工程力学/作业'
FIG = OUT / '2026-09-22-作业/图'
TMP = ROOT / '.arena-tools/0922'
BOOK = ROOT / '工程力学/框架版教材/工程力学（框架汇编版）.pdf'
STEM = '2026-09-22-工程力学作业单（1-2）'


def cross(r, f):
    return r[0] * f[1] - r[1] * f[0]


def self_check():
    a, b = math.radians(30), math.radians(35)
    # (a) 绳与AC共线，墙反力法向；三力平衡。
    T = 1 / math.cos(a)
    assert np.allclose(T * np.array([-math.sin(a), math.cos(a)]) + [math.tan(a), -1], 0)
    assert abs(cross([-math.sin(a), math.cos(a)], [-math.sin(a), math.cos(a)])) < 1e-12
    # (b) 两接触力分别沿半径，正压力可保持平衡。
    na, nb = np.array([math.sin(a), math.cos(a)]), np.array([-math.cos(b), math.sin(b)])
    mag = np.linalg.solve(np.column_stack([na, nb]), [0, 1])
    assert (mag > 0).all()
    assert np.allclose(mag[0] * na + mag[1] * nb, [0, 1])
    assert abs(np.dot(na, [math.cos(a), -math.sin(a)])) < 1e-12
    # (c/e) 斜面支承反力垂直支承面。
    nc = np.array([-math.sin(a), math.cos(a)])
    assert abs(np.dot(nc, [math.cos(a), math.sin(a)])) < 1e-12
    # (d) 两轮上分别有两项绳力；切线力矩相消，动滑轮P=2F。
    r, f = np.array([-.8, .6]), np.array([-.6, -.8])
    assert abs(np.dot(r, f)) < 1e-12
    assert abs(cross(r, f) + cross([1, 0], [0, -1])) < 1e-12
    assert np.allclose(f + [0, -1] + [.6, 1.8], 0)
    assert np.allclose(np.array([0, 1]) + [0, 1] + [0, -2], 0)
    assert cross([-1, 0], [0, 1]) + cross([1, 0], [0, 1]) == 0
    # (e) 自选尺寸仅用于验算拓扑与符号，不是题设数据。
    # A=0,D=2,B=3,C=5；q=2作用于AD，P=3作用于x=4。
    C = 1.5 / math.cos(a) * nc
    B_on_BC = np.array([-C[0], 1.5])
    B_on_AB = -B_on_BC
    A, D = np.array([-B_on_AB[0], 1.25]), np.array([0, 4.25])
    assert np.allclose(B_on_BC + C + [0, -3], 0)
    assert abs(cross([2, 0], C) + cross([1, 0], [0, -3])) < 1e-12
    assert np.allclose(A + D + B_on_AB + [0, -4], 0)
    assert abs(cross([2, 0], D) + cross([3, 0], B_on_AB) + cross([1, 0], [0, -4])) < 1e-12
    assert np.allclose(B_on_AB + B_on_BC, 0)
    print('PASS：法向/径向/绳切线、两滑轮力矩、内铰反向及两梁平衡自检')


def crop_sources():
    book = pymupdf.open(BOOK)
    original = pymupdf.open(ROOT / '工程力学/资料原件/工程力学（第三版）_1-130.pdf')
    assert len(book) == 295
    # 同一教材页的文本与渲染双源比对；1-based页码：30/31与33/34。
    for i, j in [(29, 32), (30, 33)]:
        assert book[i].get_text() == original[j].get_text()
        assert book[i].get_pixmap(dpi=72).samples == original[j].get_pixmap(dpi=72).samples
    boxes = [
        (29, (73, 549, 149, 661), 'a'),
        (29, (179, 560, 283, 661), 'b'),
        (29, (310, 563, 454, 661), 'c'),
        (30, (72, 69, 188, 219), 'd'),
        (30, (215, 83, 437, 219), 'e'),
    ]
    for i, box, name in boxes:
        book[i].get_pixmap(dpi=240, clip=pymupdf.Rect(box)).save(FIG / f'题1-2-{name}.png')
    # 两行拼图，保留原书(a)-(e)及指定对象；无解答内容。
    canvas = Image.new('RGB', (1600, 1160), 'white')
    slots = [(0, 0, 480, 565), (485, 0, 975, 565), (980, 0, 1600, 565),
             (0, 580, 580, 1160), (590, 580, 1600, 1160)]
    for name, (x0, y0, x1, y1) in zip('abcde', slots):
        im = Image.open(FIG / f'题1-2-{name}.png').convert('RGB')
        im.thumbnail((x1-x0-12, y1-y0-12), Image.Resampling.LANCZOS)
        canvas.paste(im, (x0+(x1-x0-im.width)//2, y0+(y1-y0-im.height)//2))
    canvas.save(FIG / '题1-2-全图.png')
    print('PASS：原件与框架版两页文本/72dpi像素一致；完整裁出(a)-(e)')


CJK = None
BLUE, RED, INK = '#226699', '#b34130', '#26333e'


def text(ax, x, y, value, size=12, **kw):
    return ax.text(x, y, value, fontproperties=CJK, fontsize=size, **kw)


def force(ax, point, vec, label, label_pos=None, color=BLUE):
    p, v = np.array(point), np.array(vec)
    end = p + v
    ax.annotate('', xy=end, xytext=p, arrowprops=dict(arrowstyle='-|>', color=color, lw=2, mutation_scale=17))
    pos = np.array(label_pos) if label_pos is not None else end + [.06, .08]
    ax.text(*pos, label, fontsize=14, color=color, bbox=dict(fc='white', ec='none', pad=.2))


def line(ax, points, color=INK, lw=3, **kw):
    arr = np.array(points)
    ax.plot(arr[:, 0], arr[:, 1], color=color, lw=lw, **kw)


def dot(ax, p, label, offset=(.08, .10)):
    ax.plot(*p, 'o', ms=4, color=INK)
    ax.text(p[0]+offset[0], p[1]+offset[1], label, fontsize=12)


def setup(ax, title, note, limits=(-2, 2, -1.65, 2.1)):
    ax.set_aspect('equal')
    ax.set_xlim(limits[:2]); ax.set_ylim(limits[2:]); ax.axis('off')
    ax.set_title(title, fontproperties=CJK, fontsize=15, loc='left', pad=14)
    text(ax, .0, -.08, note, 10, transform=ax.transAxes, va='top')


def draw_answers():
    plt.rcParams['mathtext.fontset'] = 'dejavusans'
    fig, axs = plt.subplots(1, 3, figsize=(15, 5.3))
    fig.suptitle('习题1-2受力图 · (a)—(c)', fontproperties=CJK, fontsize=22, y=.98)
    ax = axs[0]; setup(ax, '(a) 球', '绳力沿 AC；墙面反力水平向右。')
    ax.add_patch(Circle((0, 0), 1, fill=False, lw=2, edgecolor=INK))
    A = (-.5, math.sqrt(3)/2)
    line(ax, [A, (0, 0)], lw=1, linestyle='--', color='#999999')
    dot(ax, (0, 0), 'C', (.08, .04)); dot(ax, A, 'A', (.10, -.03)); dot(ax, (-1, 0), 'B', (-.22, -.25))
    force(ax, (0, 0), (0, -1.45), '$P$', color=RED)
    force(ax, A, (-.52, .90), '$T$', (-1.25, 1.70))
    force(ax, (-1, 0), (.8, 0), '$N_B$', (-.85, .15))
    ax = axs[1]; setup(ax, '(b) 球', 'A：垂直斜面；B：沿尖角 B 指向球心 C。')
    ax.add_patch(Circle((0, 0), 1, fill=False, lw=2, edgecolor=INK))
    a, b = math.radians(30), math.radians(35)
    A = np.array([-math.sin(a), -math.cos(a)])
    B = np.array([math.cos(b), -math.sin(b)])
    line(ax, [A, (0, 0), B], lw=1, linestyle='--', color='#999999')
    dot(ax, (0, 0), 'C'); dot(ax, A, 'A', (-.28, -.13)); dot(ax, B, 'B', (.1, -.15))
    force(ax, (0, 0), (0, -1.45), '$P$', color=RED)
    force(ax, A, -.86*A, '$N_A$', (-.65, .16))
    force(ax, B, -.86*B, '$N_B$', (.55, .1))
    ax = axs[2]; setup(ax, '(c) 杆 AB', 'A：铰支座两分量；B：光滑斜面法向力。', (-1.0, 5.7, -1.8, 3.0))
    line(ax, [(0, 0), (4.6, 0)])
    dot(ax, (0, 0), 'A', (-.35, -.4)); dot(ax, (4.6, 0), 'B', (.15, -.4))
    force(ax, (0, 0), (1.05, 0), '$A_x$', (.45, -.46))
    force(ax, (0, 0), (0, 1.5), '$A_y$', (.12, 1.4))
    force(ax, (4.6, 0), (-.85, 1.47), '$N_B$', (4.10, 1.60))
    force(ax, (1.5, 1.6), (0, -1.6), '$P_1$', (1.65, 1.35), color=RED)
    force(ax, (3.7, 1.5), (-.9, -1.5), '$P_2$', (3.0, 1.80), color=RED)
    fig.subplots_adjust(left=.03, right=.98, top=.80, bottom=.16, wspace=.20)
    fig.savefig(FIG / '解答-1-2-abc.png', dpi=180, facecolor='white')
    plt.close(fig)

    fig, axs = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle('习题1-2受力图 · (d)—(e)', fontproperties=CJK, fontsize=22, y=.98)
    ax = axs[0, 0]; setup(ax, '(d) 定滑轮 A', '两段绳均沿轮缘切线拉轮；轴心画两个反力分量。', (-2.2, 2.4, -1.7, 1.8))
    ax.add_patch(Circle((0, 0), 1, fill=False, lw=2, edgecolor=INK))
    dot(ax, (0, 0), 'A', (-.28, .08))
    force(ax, (-.8, .6), (-.72, -.96), '$F$', (-1.8, -.45), color=RED)
    force(ax, (1, 0), (0, -1.4), '$F$', (1.12, -1.2), color=RED)
    force(ax, (0, 0), (1.7, 0), '$A_x$', (1.65, .15))
    force(ax, (0, 0), (0, 1.4), '$A_y$', (.1, 1.4))
    ax = axs[0, 1]; setup(ax, '(d) 动滑轮 B', '左右两段绳各给向上的 F；挂物经连接件向下拉轮。', (-2.1, 2.2, -1.7, 1.8))
    ax.add_patch(Circle((0, 0), 1, fill=False, lw=2, edgecolor=INK))
    dot(ax, (0, 0), 'B')
    force(ax, (-1, 0), (0, 1.4), '$F$', (-1.3, 1.42))
    force(ax, (1, 0), (0, 1.4), '$F$', (1.1, 1.42))
    force(ax, (0, 0), (0, -1.45), '$P$', (.1, -1.4), color=RED)
    ax = axs[1, 0]; setup(ax, '(e) 梁 AB', 'q 只在 AD 段；B 是内铰，不传递力偶。', (-.85, 5.6, -1.65, 2.2))
    line(ax, [(0, 0), (4.2, 0)])
    dot(ax, (0, 0), 'A', (-.38, -.38)); dot(ax, (2.5, 0), 'D', (-.1, -.4)); dot(ax, (4.2, 0), 'B', (.16, .04))
    force(ax, (0, 0), (1.0, 0), '$A_x$', (.40, -.42))
    force(ax, (0, 0), (0, 1.5), '$A_y$', (-.70, 1.45))
    force(ax, (2.5, 0), (0, 1.5), '$N_D$', (2.7, 1.42))
    force(ax, (4.2, 0), (-1.0, 0), '$B_x$', (3.35, .20))
    force(ax, (4.2, 0), (0, -1.1), '$B_y$', (4.32, -1.0))
    line(ax, [(0, .9), (2.5, .9)], lw=1, color=RED)
    for x in np.linspace(.15, 2.4, 9):
        ax.annotate('', xy=(x, .02), xytext=(x, .9), arrowprops=dict(arrowstyle='->', color=RED, lw=1))
    ax.text(1.1, 1.05, '$q$', fontsize=14, color=RED)
    ax = axs[1, 1]; setup(ax, '(e) 梁 BC', '两图同名 Bx、By 等大反向；C 反力垂直斜面。', (-.85, 5.6, -1.65, 2.2))
    line(ax, [(0, 0), (4.2, 0)])
    dot(ax, (0, 0), 'B', (-.35, -.4)); dot(ax, (4.2, 0), 'C', (.15, -.4))
    force(ax, (0, 0), (1.0, 0), '$B_x$', (.45, -.42))
    force(ax, (0, 0), (0, 1.5), '$B_y$', (.1, 1.55))
    force(ax, (4.2, 0), (-.85, 1.47), '$N_C$', (3.60, 1.63))
    force(ax, (2, 1.65), (0, -1.65), '$P$', (2.15, 1.45), color=RED)
    fig.text(.05, .035, '说明：忽略未给出的构件自重与摩擦；铰支座/内铰分量箭头为假定正向。绳、光滑接触按物理方向画。', fontproperties=CJK, fontsize=11)
    fig.subplots_adjust(left=.05, right=.97, top=.88, bottom=.12, hspace=.40, wspace=.18)
    fig.savefig(FIG / '解答-1-2-de.png', dpi=180, facecolor='white')
    plt.close(fig)


def make_sheet():
    spec = json.loads((OUT / '2026-09-22-作业单.json').read_text())
    spec['_base'] = str(OUT)
    sheet.build(spec, OUT / f'{STEM}.docx')
    preview.SONG = preview.HEI = TMP / 'DroidSansFallback.ttf'
    assert preview.render(OUT / f'{STEM}.docx', OUT / f'{STEM}.preview.pdf') == 1
    pdf = pymupdf.open(OUT / f'{STEM}.preview.pdf')
    assert len(pdf) == 1 and '2253710052' in pdf[0].get_text()
    pdf[0].get_pixmap(dpi=120).save(TMP / '作业单预览.png')


def main():
    global CJK
    FIG.mkdir(parents=True, exist_ok=True)
    TMP.mkdir(parents=True, exist_ok=True)
    font_path = TMP / 'DroidSansFallback.ttf'
    font_path.write_bytes(pymupdf.Font('china-s').buffer)
    CJK = FontProperties(fname=font_path)
    self_check()
    crop_sources()
    draw_answers()
    make_sheet()


if __name__ == '__main__':
    main()
