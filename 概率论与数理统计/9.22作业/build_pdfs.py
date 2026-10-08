#!/usr/bin/env python3
"""Build the 9.22 Chapter-1 (2nd ed.) homework pack: 4-page sheet, solutions, quality report.

真公式排版：matplotlib mathtext 300dpi 透明 PNG 内联；cases/array 真表格＋花括号；中文 STSong-Light。
图1.9–1.11 按教材矢量重绘。答题纸硬门禁：严格4页。
"""
from pathlib import Path
import re, html, hashlib
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, PageBreak,
                                Table, TableStyle, HRFlowable, Image as RLImage,
                                KeepTogether)
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image

ROOT = Path(__file__).resolve().parent
QMD = ROOT/'第一章奇数题-题面.md'
AMD = ROOT/'第一章奇数题-参考答案.md'
RMD = ROOT/'题目质量分析.md'
QPDF = ROOT/'9.22概率论作业-孙承泽-试卷.pdf'
APDF = ROOT/'9.22概率论作业-孙承泽-完整解析.pdf'
RPDF = ROOT/'9.22概率论作业-题目质量分析报告.pdf'
CACHE = Path('/tmp/mathcache'); CACHE.mkdir(parents=True, exist_ok=True)
DPI = 300
BS = chr(92)
pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))

RE_INLINE = re.compile(re.escape(BS+'(') + '.+?' + re.escape(BS+')'), re.S)
RE_TEXT = re.compile(re.escape(BS+'text{') + '([^{}]*)' + re.escape('}'))
RE_CASES = re.compile(re.escape(BS+'begin{cases}') + '(.*?)' + re.escape(BS+'end{cases}'), re.S)
RE_ARRAY = re.compile(re.escape(BS+'begin{array}') + r'\{([^}]*)\}' + '(.*?)' + re.escape(BS+'end{array}'), re.S)
RE_BOXED = re.compile(re.escape(BS+'boxed{') + '(.*)' + re.escape('}'), re.S)
RE_ROWS = re.compile(re.escape(BS*2))
CJK = re.compile('[一-鿿]')

# ---------------------------------------------------------------- reportlab CJK+inline-image patch
# reportlab 5.x 的 cjkFragSplit 在换行点落到内联 <img>（text 为 '' 的 frag）时 ord('') 崩溃。
# 这里安装打过补丁的副本：把空 frag 当作不可拆分的原子单元（整块移到下一行）。
from reportlab.platypus import paragraph as _rlpara
from reportlab.lib.utils import isBytes
from unicodedata import category as _unicat

def _cjkFragSplit(frags, maxWidths, calcBounds, encoding='utf8'):
    cjkU, makeCJKParaLine = _rlpara.cjkU, _rlpara.makeCJKParaLine
    ALL_CANNOT_START, _FUZZ = _rlpara.ALL_CANNOT_START, _rlpara._FUZZ
    ParaLines = _rlpara.ParaLines
    U = []
    for f in frags:
        text = f.text
        if isBytes(text):
            text = text.decode(encoding)
        if text:
            U.extend([cjkU(t, f, encoding) for t in text])
        else:
            U.append(cjkU(text, f, encoding))
    lines = []
    i = widthUsed = lineStartPos = 0
    maxWidth = maxWidths[0]
    nU = len(U)
    while i < nU:
        u = U[i]
        i += 1
        w = u.width
        if hasattr(w, 'normalizedValue'):
            w._normalizer = maxWidth
            w = w.normalizedValue(maxWidth)
        widthUsed += w
        lineBreak = hasattr(u.frag, 'lineBreak')
        endLine = (widthUsed > maxWidth + _FUZZ and widthUsed > 0) or lineBreak
        if endLine:
            extraSpace = maxWidth - widthUsed
            if not lineBreak:
                if u and ord(u) < 0x3000:
                    limitCheck = (lineStartPos + i) >> 1
                    for j in range(i-1, limitCheck, -1):
                        uj = U[j]
                        if (uj and _unicat(uj) == 'Zs') or (uj and ord(uj) >= 0x3000):
                            k = j + 1
                            if k < i:
                                j = k + 1
                                extraSpace += sum(U[ii].width for ii in range(j, i))
                                w = U[k].width
                                u = U[k]
                                i = j
                                break
                if u not in ALL_CANNOT_START and i > lineStartPos + 1:
                    i -= 1
                    extraSpace += w
            lines.append(makeCJKParaLine(U[lineStartPos:i], maxWidth, widthUsed, extraSpace, lineBreak, calcBounds))
            try:
                maxWidth = maxWidths[len(lines)]
            except IndexError:
                maxWidth = maxWidths[-1]
            lineStartPos = i
            widthUsed = 0
    if widthUsed > 0:
        lines.append(makeCJKParaLine(U[lineStartPos:], maxWidth, widthUsed, maxWidth - widthUsed, False, calcBounds))
    return ParaLines(kind=1, lines=lines)

_rlpara.cjkFragSplit = _cjkFragSplit

# ---------------------------------------------------------------- styles
# autoLeading='max' 让行高按行内实际内容（含内联公式图）伸缩，否则高公式会压行
base = ParagraphStyle('base', fontName='STSong-Light', fontSize=10, leading=16, spaceAfter=4,
                      wordWrap='CJK', autoLeading='max')
small = ParagraphStyle('small', parent=base, fontSize=9, leading=13, textColor=colors.HexColor('#444444'))
h1 = ParagraphStyle('h1', parent=base, fontSize=17, leading=24, alignment=1, spaceAfter=9)
h2 = ParagraphStyle('h2', parent=base, fontSize=13, leading=18, spaceBefore=7, spaceAfter=5)
h3 = ParagraphStyle('h3', parent=base, fontSize=11, leading=16, spaceBefore=6, spaceAfter=3)
qbody = ParagraphStyle('qbody', parent=base, fontSize=10.5, leading=15.5, spaceBefore=4, spaceAfter=2)
sol = ParagraphStyle('sol', parent=base, fontSize=10, leading=16.5, spaceAfter=5)
cell = ParagraphStyle('cell', parent=base, fontSize=9, leading=13, spaceAfter=0)
cellc = ParagraphStyle('cellc', parent=cell, alignment=1)
disp = ParagraphStyle('disp', parent=base, alignment=1, leading=19, spaceAfter=4)

# ---------------------------------------------------------------- math rendering
def _normalize_args(expr):
    """mathtext 要求 \\frac/\\binom/\\sqrt 的参数带花括号：把 \\frac12 这类无括号形式补全。"""
    out, i, n = [], 0, len(expr)
    cmdre = re.compile(re.escape(BS) + '(frac|binom|sqrt)(?![a-zA-Z])')
    while i < n:
        m = cmdre.match(expr, i)
        if m:
            cmd = m.group(1)
            out.append(BS+cmd)
            i = m.end()
            for _ in range(1 if cmd == 'sqrt' else 2):
                while i < n and expr[i].isspace():
                    i += 1
                if i >= n:
                    break
                if expr[i] == '{':
                    depth, j = 1, i+1
                    while j < n and depth:
                        if expr[j] == '{':
                            depth += 1
                        elif expr[j] == '}':
                            depth -= 1
                        j += 1
                    out.append('{' + _normalize_args(expr[i+1:j-1]) + '}'); i = j
                elif expr[i] == BS:
                    m2 = re.match(re.escape(BS) + '[a-zA-Z]+', expr[i:])
                    tok = m2.group(0) if m2 else expr[i:i+2]
                    out.append('{'+tok+'}'); i += len(tok)
                else:
                    out.append('{'+expr[i]+'}'); i += 1
            continue
        out.append(expr[i]); i += 1
    return ''.join(out)

def _prep(expr):
    expr = expr.replace(BS+'displaystyle', '').replace(BS+'dfrac', BS+'frac').replace(BS+'tfrac', BS+'frac')
    expr = expr.replace(BS+'operatorname', BS+'mathrm')
    expr = expr.replace(BS+',', ' ').replace(BS+';', ' ').replace(BS+'!', '')
    for short, long in (('le', 'leq'), ('ge', 'geq'), ('ne', 'neq')):
        expr = re.sub(re.escape(BS+short) + r'(?![a-zA-Z])', lambda m, L=long: BS+L, expr)
    for g in ('Biggl', 'Biggr', 'Bigl', 'Bigr', 'bigl', 'bigr', 'Bigg', 'bigg', 'Big', 'big'):
        expr = expr.replace(BS+g, '')
    expr = expr.replace(BS+'dots', BS+'ldots')
    expr = RE_TEXT.sub(lambda m: m.group(1) if CJK.search(m.group(1)) else BS+'mathrm{'+m.group(1)+'}', expr)
    expr = _normalize_args(expr)
    return expr.strip()

def math_img(expr, size=10.5, boxed=False):
    expr = _prep(expr)
    key = hashlib.md5(f'{expr}|{size}|{boxed}'.encode()).hexdigest()
    png = CACHE/f'{key}.png'
    if not png.exists():
        fig = plt.figure(dpi=DPI)   # 与 savefig 同 dpi，保证 boxed 矩形坐标一致
        if boxed:
            from matplotlib.patches import Rectangle
            t = fig.text(0.5, 0.5, f'${expr}$', fontsize=size, ha='center', va='center')
            fig.canvas.draw()
            bb = t.get_window_extent(renderer=fig.canvas.get_renderer())
            fig.patches.append(Rectangle((bb.x0-5, bb.y0-5), bb.width+10, bb.height+10,
                                         fill=False, lw=1.1, edgecolor='black', transform=None))
        else:
            t = fig.text(0, 0, f'${expr}$', fontsize=size)
        fig.savefig(png, dpi=DPI, transparent=True, bbox_inches='tight', pad_inches=0.012)
        plt.close(fig)
    w, h = Image.open(png).size
    return str(png), w/DPI*72, h/DPI*72

def img_tag(expr, size=10.5, boxed=False):
    p, w, h = math_img(expr, size, boxed)
    return f'<img src="{p}" width="{w:.2f}" height="{h:.2f}"/>'

RE_TXBX = re.compile('(?P<tx>' + RE_TEXT.pattern + ')|(?P<bx>' + RE_BOXED.pattern + ')', re.S)

def _math_mixed(expr, size):
    """Math chunk possibly containing CJK \\text{..} or nested \\boxed{..}: interleave images/text."""
    out, buf = [], ''
    def flush():
        nonlocal buf
        if buf.strip():
            out.append(img_tag(buf, size))
        buf = ''
    pos = 0
    for m in RE_TXBX.finditer(expr):
        if m.group(1) is not None:                      # \text{...}
            content = m.group(2)
            if CJK.search(content):
                buf += expr[pos:m.start()]
                flush()
                out.append(html.escape(content, quote=False))
                pos = m.end()
            else:
                buf += expr[pos:m.end()]                # 非中文 \text 留给 mathtext 处理
                pos = m.end()
        else:                                           # \boxed{...} -> 带框公式图
            buf += expr[pos:m.start()]
            flush()
            out.append(img_tag(m.group(4), size, boxed=True))
            pos = m.end()
    buf += expr[pos:]
    flush()
    if not out:
        return ''
    if len(out) == 1:
        return out[0]
    return ' '.join(out)

def mixed_xml(s, size=10.5, bold_all=False):
    """Markdown+latex string -> reportlab paragraph XML with real math images."""
    out = []
    for tok in re.split(r'(\*\*.*?\*\*)', s.strip()):
        if not tok:
            continue
        bold = tok.startswith('**') and tok.endswith('**')
        body = tok[2:-2] if bold else tok
        seg = []
        pos = 0
        for m in RE_INLINE.finditer(body):
            seg.append(html.escape(body[pos:m.start()], quote=False))
            seg.append(_math_mixed(m.group(0)[2:-2], size))
            pos = m.end()
        seg.append(html.escape(body[pos:], quote=False))
        piece = ''.join(seg)
        if bold or bold_all:
            piece = f'<b>{piece}</b>'
        out.append(piece)
    return ''.join(out)

# ---------------------------------------------------------------- environments
from reportlab.platypus.flowables import Flowable

class Brace(Flowable):
    """矢量左花括号，高度精确等于分段表格高度。"""
    def __init__(self, width, height, thickness=1.0):
        Flowable.__init__(self)
        self.width, self.height, self.thickness = width, height, thickness
    def wrap(self, aw, ah):
        return self.width, self.height
    def draw(self):
        c = self.canv
        w, h = self.width, self.height
        c.setLineWidth(self.thickness); c.setLineCap(1); c.setLineJoin(1)
        c.setStrokeColor(colors.black)
        p = c.beginPath()
        p.moveTo(w, h)
        p.curveTo(w*0.55, h*0.985, w*0.60, h*0.88, w*0.60, h*0.74)
        p.curveTo(w*0.60, h*0.58, w*0.45, h*0.52, w*0.06, h*0.5)
        p.curveTo(w*0.45, h*0.48, w*0.60, h*0.42, w*0.60, h*0.26)
        p.curveTo(w*0.60, h*0.12, w*0.55, h*0.015, w, 0)
        c.drawPath(p, stroke=1, fill=0)

def parse_cases(body):
    rows = [r.strip() for r in RE_ROWS.split(body.strip()) if r.strip()]
    parsed = []
    for r in rows:
        c = [x.strip() for x in r.split('&')]
        parsed.append((c[0], c[1] if len(c) > 1 else ''))
    return parsed

def parse_array(spec, body):
    rows, hlines, idx = [], [0], 0
    for raw in RE_ROWS.split(body.strip()):
        line = raw.strip()
        if BS+'hline' in line:
            line = line.replace(BS+'hline', '').strip()
            hlines.append(idx)
            if not line:
                continue
        if line:
            rows.append([c.strip() for c in line.split('&')])
            idx += 1
    hlines.append(idx)
    return rows, sorted(set(hlines)), '|' in spec

def display_flow(expr, size=11.0):
    expr = expr.strip()
    boxed = False
    m = RE_BOXED.fullmatch(expr)
    if m:
        boxed, expr = True, m.group(1).strip()
    flows = []
    mc = RE_CASES.search(expr)
    ma = RE_ARRAY.search(expr)
    if mc:
        pre = expr[:mc.start()].strip()
        rows = parse_cases(mc.group(1))
        data = [[Paragraph(_math_mixed(e, size), cell), Paragraph(_math_mixed(c, size), cell)] for e, c in rows]
        t = Table(data, colWidths=[72*mm, 78*mm], rowHeights=[7.0*mm]*len(rows), hAlign='LEFT')
        t.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                               ('LEFTPADDING', (0, 0), (-1, -1), 2), ('RIGHTPADDING', (0, 0), (-1, -1), 6)]))
        brace = Brace(3.2*mm, len(rows)*7.0*mm)
        preflow = Paragraph(_math_mixed(pre, size), ParagraphStyle('cpre', parent=base, alignment=2, leading=19)) if pre else ''
        outer = Table([[preflow, brace, t]], hAlign='CENTER')
        outer.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                                   ('LEFTPADDING', (0, 0), (-1, -1), 0), ('RIGHTPADDING', (0, 0), (-1, -1), 2)]))
        flows.append(outer)
    elif ma:
        pre = expr[:ma.start()].strip()
        if pre:
            flows.append(Paragraph(_math_mixed(pre, size), disp))
        rows, hlines, vline = parse_array(ma.group(1), ma.group(2))
        data = [[Paragraph(_math_mixed(c, size-0.5), cellc) if c else Paragraph('', cellc) for c in r] for r in rows]
        cmds = [('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('LEFTPADDING', (0, 0), (-1, -1), 6), ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 2), ('BOTTOMPADDING', (0, 0), (-1, -1), 3)]
        for hl in hlines:
            cmds.append(('LINEABOVE', (0, hl), (-1, hl), 0.7, colors.black))
        if vline:
            cmds.append(('LINEBEFORE', (1, 0), (1, -1), 0.7, colors.black))
        t = Table(data, hAlign='CENTER')
        t.setStyle(TableStyle(cmds))
        flows.append(t)
    else:
        flows.append(Paragraph(_math_mixed(expr, size), disp))
    if boxed:
        flows = [Table([[flows[-1]]], hAlign='CENTER',
                       style=TableStyle([('BOX', (0, 0), (-1, -1), 0.9, colors.black),
                                         ('LEFTPADDING', (0, 0), (-1, -1), 7), ('RIGHTPADDING', (0, 0), (-1, -1), 7),
                                         ('TOPPADDING', (0, 0), (-1, -1), 3), ('BOTTOMPADDING', (0, 0), (-1, -1), 3)]))]
    return flows

# ---------------------------------------------------------------- reliability diagrams (图1.9–1.11)
def _box(ax, x, y, w=0.72, h=0.42, text='', fs=11):
    from matplotlib.patches import Rectangle
    ax.add_patch(Rectangle((x - w/2, y - h/2), w, h, linewidth=1.35,
                           edgecolor='black', facecolor='white', zorder=3))
    if text:
        ax.text(x, y, text, ha='center', va='center', fontsize=fs, zorder=4)

def _line(ax, x1, y1, x2, y2):
    ax.plot([x1, x2], [y1, y2], color='black', lw=1.35, solid_capstyle='round', zorder=2)

def _dots(ax, x, y):
    ax.plot([x-0.22, x, x+0.22], [y, y, y], 'k.', ms=3.2, zorder=2)

def draw_a29(path):
    fig, axes = plt.subplots(1, 2, figsize=(7.6, 2.9), dpi=220)
    ax = axes[0]
    ax.set_xlim(-0.2, 8.4); ax.set_ylim(0.2, 3.8); ax.axis('off')
    ax.text(-0.05, 2.0, 'I', ha='center', va='center', fontsize=13, fontweight='bold')
    _line(ax, 0.35, 2.0, 1.15, 2.0)
    _line(ax, 1.15, 2.0, 1.15, 3.15); _line(ax, 1.15, 2.0, 1.15, 0.85)
    for y in (3.15, 0.85):
        _line(ax, 1.15, y, 1.7, y); _box(ax, 2.15, y)
        _line(ax, 2.51, y, 3.05, y); _box(ax, 3.5, y)
        _line(ax, 3.86, y, 4.25, y); _dots(ax, 4.55, y)
        _line(ax, 4.85, y, 5.25, y); _box(ax, 5.7, y)
        _line(ax, 6.06, y, 6.7, y)
    _line(ax, 6.7, 3.15, 6.7, 0.85); _line(ax, 6.7, 2.0, 7.7, 2.0)
    ax.set_title('Fig. 1.9   System I', fontsize=10, pad=3)
    ax = axes[1]
    ax.set_xlim(-0.2, 8.6); ax.set_ylim(0.2, 3.8); ax.axis('off')
    ax.text(-0.05, 2.0, 'II', ha='center', va='center', fontsize=13, fontweight='bold')
    xs = [1.55, 4.15, 6.75]
    _line(ax, 0.35, 2.0, xs[0]-0.7, 2.0)
    for i, x in enumerate(xs):
        _line(ax, x-0.7, 2.0, x-0.7, 3.15); _line(ax, x-0.7, 2.0, x-0.7, 0.85)
        _line(ax, x-0.7, 3.15, x-0.36, 3.15); _box(ax, x+0.1, 3.15)
        _line(ax, x+0.46, 3.15, x+0.7, 3.15); _line(ax, x+0.7, 3.15, x+0.7, 2.0)
        _line(ax, x-0.7, 0.85, x-0.36, 0.85); _box(ax, x+0.1, 0.85)
        _line(ax, x+0.46, 0.85, x+0.7, 0.85); _line(ax, x+0.7, 0.85, x+0.7, 2.0)
        if i == 0:
            _line(ax, x+0.7, 2.0, xs[1]-0.7, 2.0)
        elif i == 1:
            _line(ax, x+0.7, 2.0, x+1.05, 2.0); _dots(ax, x+1.28, 2.0)
            _line(ax, x+1.52, 2.0, xs[2]-0.7, 2.0)
    _line(ax, xs[-1]+0.7, 2.0, 8.15, 2.0)
    ax.set_title('Fig. 1.10   System II', fontsize=10, pad=3)
    fig.tight_layout(pad=0.25)
    fig.savefig(path, dpi=220, transparent=True, bbox_inches='tight', pad_inches=0.05)
    plt.close(fig)

def draw_b5(path):
    fig, axes = plt.subplots(1, 2, figsize=(7.8, 3.05), dpi=220)
    ax = axes[0]
    ax.set_xlim(-0.2, 8.2); ax.set_ylim(0.05, 3.85); ax.axis('off')
    _line(ax, 0.2, 2.0, 1.1, 2.0)
    _line(ax, 1.1, 2.0, 1.1, 3.2); _line(ax, 1.1, 2.0, 1.1, 0.8)
    _line(ax, 1.1, 3.2, 1.7, 3.2); _box(ax, 2.2, 3.2, text='1')
    _line(ax, 2.56, 3.2, 3.15, 3.2); _box(ax, 3.65, 3.2, text='2')
    _line(ax, 4.01, 3.2, 4.7, 3.2)
    _line(ax, 1.1, 0.8, 1.7, 0.8); _box(ax, 2.2, 0.8, text='3')
    _line(ax, 2.56, 0.8, 3.15, 0.8); _box(ax, 3.65, 0.8, text='4')
    _line(ax, 4.01, 0.8, 4.7, 0.8)
    _line(ax, 4.7, 3.2, 4.7, 0.8); _line(ax, 4.7, 2.0, 5.35, 2.0)
    _box(ax, 5.85, 2.0, text='5'); _line(ax, 6.21, 2.0, 7.3, 2.0)
    ax.text(3.7, 0.22, 'System I', ha='center', fontsize=10)
    ax = axes[1]
    ax.set_xlim(-0.2, 8.2); ax.set_ylim(0.05, 3.85); ax.axis('off')
    _line(ax, 0.2, 2.0, 1.15, 2.0)
    _line(ax, 1.15, 2.0, 1.15, 3.2); _line(ax, 1.15, 2.0, 1.15, 0.8)
    _line(ax, 1.15, 3.2, 1.75, 3.2); _box(ax, 2.25, 3.2, text='1')
    _line(ax, 2.61, 3.2, 4.05, 3.2); _box(ax, 4.55, 3.2, text='2')
    _line(ax, 4.91, 3.2, 5.7, 3.2)
    _line(ax, 1.15, 0.8, 1.75, 0.8); _box(ax, 2.25, 0.8, text='3')
    _line(ax, 2.61, 0.8, 4.05, 0.8); _box(ax, 4.55, 0.8, text='4')
    _line(ax, 4.91, 0.8, 5.7, 0.8)
    _line(ax, 3.4, 3.2, 3.4, 2.52); _box(ax, 3.4, 2.0, w=0.55, h=0.7, text='5')
    _line(ax, 3.4, 1.48, 3.4, 0.8)
    _line(ax, 5.7, 3.2, 5.7, 0.8); _line(ax, 5.7, 2.0, 7.3, 2.0)
    ax.text(3.7, 0.22, 'System II', ha='center', fontsize=10)
    fig.tight_layout(pad=0.2)
    fig.savefig(path, dpi=220, transparent=True, bbox_inches='tight', pad_inches=0.05)
    plt.close(fig)

FIG_A29 = CACHE/'fig_a29.png'
FIG_B5 = CACHE/'fig_b5.png'
draw_a29(FIG_A29)
draw_b5(FIG_B5)

def fig_flow(name, width_mm=165):
    p = FIG_A29 if name == 'a29' else FIG_B5
    w, h = Image.open(p).size
    rw = width_mm * mm
    rh = rw * h / w
    img = RLImage(str(p), width=rw, height=rh)
    img.hAlign = 'CENTER'
    return img

# ---------------------------------------------------------------- markdown blocks
def split_blocks(text):
    lines = text.splitlines()
    i, n = 0, len(lines)
    stops = ('#', '>', '|', BS+'[', '---', '[[')
    while i < n:
        ln = lines[i]
        if not ln.strip():
            i += 1; continue
        s = ln.strip()
        if s.startswith('[[fig:') and s.endswith(']]'):
            yield ('fig', s[6:-2].strip()); i += 1
        elif ln.startswith('# '):
            yield ('h1', ln[2:].strip()); i += 1
        elif ln.startswith('## '):
            yield ('h2', ln[3:].strip()); i += 1
        elif ln.startswith('### '):
            yield ('h3', ln[4:].strip()); i += 1
        elif ln.startswith('>'):
            buf = [ln[1:].strip()]; i += 1
            while i < n and lines[i].startswith('>'):
                buf.append(lines[i][1:].strip()); i += 1
            yield ('quote', ' '.join(x for x in buf if x))
        elif s == '---':
            yield ('hr', ''); i += 1
        elif ln.startswith('|'):
            buf = [ln.strip()]; i += 1
            while i < n and lines[i].startswith('|'):
                buf.append(lines[i].strip()); i += 1
            yield ('table', buf)
        elif s.startswith(BS+'['):
            buf = [s]; i += 1
            while i < n and not buf[-1].endswith(BS+']'):
                buf.append(lines[i].strip()); i += 1
            yield ('disp', ' '.join(buf)[2:-2].strip())
        else:
            buf = [s]; i += 1
            while i < n and lines[i].strip() and not lines[i].strip().startswith(stops):
                buf.append(lines[i].strip()); i += 1
            yield ('para', ' '.join(buf))

def md_table_flow(rows_md):
    rows = [[c.strip() for c in r.strip('|').split('|')] for r in rows_md]
    rows = [r for r in rows if not all(re.fullmatch(r':?-{2,}:?', c) for c in r)]
    data = []
    for ri, r in enumerate(rows):
        data.append([Paragraph(mixed_xml(c, 9, bold_all=(ri == 0)), cell) for c in r])
    t = Table(data, hAlign='CENTER', repeatRows=1)
    t.setStyle(TableStyle([('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#888888')),
                           ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                           ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#efefef')),
                           ('LEFTPADDING', (0, 0), (-1, -1), 4), ('RIGHTPADDING', (0, 0), (-1, -1), 4),
                           ('TOPPADDING', (0, 0), (-1, -1), 2), ('BOTTOMPADDING', (0, 0), (-1, -1), 2)]))
    return t

def para_flowables(content, style, size=10.5, max_inline_h=20.0):
    """段落渲染：行内公式若过高（带上下限的求和/积分等），自动升格为独立居中行，避免压行。"""
    flows, acc = [], ''
    def flush():
        nonlocal acc
        if acc.strip():
            flows.append(Paragraph(acc, style))
        acc = ''
    for tok in re.split(r'(\*\*.*?\*\*)', content.strip()):
        if not tok:
            continue
        bold = tok.startswith('**') and tok.endswith('**')
        body = tok[2:-2] if bold else tok
        pos = 0
        for m in RE_INLINE.finditer(body):
            pre = body[pos:m.start()]
            expr = m.group(0)[2:-2]
            # 逐段检查高度：含 \text 拆分后分别测量
            pieces = []
            tp = 0
            tall = False
            for tm in RE_TXBX.finditer(expr):
                seg = expr[tp:tm.start()]
                if seg.strip():
                    pieces.append(('img', seg))
                if tm.group(1) is not None:
                    pieces.append(('txt', tm.group(2)))
                else:
                    pieces.append(('boximg', tm.group(4)))
                tp = tm.end()
            if expr[tp:].strip():
                pieces.append(('img', expr[tp:]))
            for kind2, val in pieces:
                if kind2 == 'txt':
                    acc += html.escape(val, quote=False)
                else:
                    _, _, hpt = math_img(val, size, boxed=(kind2 == 'boximg'))
                    if hpt > max_inline_h:
                        tall = True
            if tall:
                flush()
                xml = ''
                for kind2, val in pieces:
                    if kind2 == 'txt':
                        xml += html.escape(val, quote=False)
                    else:
                        xml += img_tag(val, size, boxed=(kind2 == 'boximg'))
                flows.append(Paragraph(xml, disp))
            else:
                xml = ''
                for kind2, val in pieces:
                    if kind2 == 'txt':
                        xml += html.escape(val, quote=False)
                    else:
                        xml += img_tag(val, size, boxed=(kind2 == 'boximg'))
                acc += html.escape(pre, quote=False) + (f'<b>{xml}</b>' if bold else xml)
            pos = m.end()
        tail = body[pos:]
        acc += (f'<b>{html.escape(tail, quote=False)}</b>' if bold else html.escape(tail, quote=False))
    flush()
    # 孤立的纯标点段落（升格公式把句子切断后残留）并回前一段/公式行
    merged = []
    for f in flows:
        txt = getattr(f, 'text', '').replace('<b>', '').replace('</b>', '').strip()
        if merged and txt and set(txt) <= set('。，；、,.;：:'):
            prev = merged[-1]
            merged[-1] = Paragraph(prev.text + txt, prev.style)
        else:
            merged.append(f)
    return merged

def render_blocks(text, styles, disp_size=11.0):
    story = []
    for kind, content in split_blocks(text):
        if kind == 'h1':
            story.append(Paragraph(mixed_xml(content), styles['h1']))
        elif kind == 'h2':
            story.append(Paragraph(mixed_xml(content), styles['h2']))
        elif kind == 'h3':
            story.append(Paragraph(mixed_xml(content), styles['h3']))
        elif kind == 'quote':
            story.append(Paragraph(mixed_xml(content), styles['small']))
        elif kind == 'hr':
            story += [Spacer(1, 2*mm), HRFlowable(width='100%', thickness=0.5, color=colors.HexColor('#999999')), Spacer(1, 2*mm)]
        elif kind == 'table':
            story += [md_table_flow(content), Spacer(1, 2*mm)]
        elif kind == 'fig':
            story.append(Spacer(1, 1.0*mm))
            story.append(fig_flow(content, width_mm=styles.get('figw', 158)))
            story.append(Spacer(1, 1.0*mm))
        elif kind == 'disp':
            story.append(Spacer(1, 1.0*mm))
            story.extend(display_flow(content, disp_size))
            story.append(Spacer(1, 1.0*mm))
        else:
            if content.startswith('- '):
                content = '•　' + content[2:]
            story.extend(para_flowables(content, styles['body']))
    return story

# ---------------------------------------------------------------- sheet (hard 4-page gate)
def footer(canvas, doc):
    canvas.saveState(); canvas.setFont('STSong-Light', 8); canvas.setFillColor(colors.HexColor('#666666'))
    canvas.drawCentredString(A4[0]/2, 8*mm, f'{doc.page}')
    canvas.restoreState()

def read_question_blocks():
    found, current, buf = [], None, []
    for line in QMD.read_text(encoding='utf-8').splitlines():
        if line.startswith('### '):
            if current:
                found.append((current, '\n'.join(buf).strip()))
            current, buf = line[4:].strip(), []
        elif current and (line.startswith('## ') or line.strip() == '---'):
            found.append((current, '\n'.join(buf).strip())); current = None
        elif current:
            buf.append(line)
    if current:
        found.append((current, '\n'.join(buf).strip()))
    return dict(found)

blocks = read_question_blocks()
qbody_s = ParagraphStyle('qbody_s', parent=qbody, fontSize=9.4, leading=13.2, spaceBefore=2, spaceAfter=1)
h1s = ParagraphStyle('h1s', parent=h1, fontSize=15, leading=20, spaceAfter=4)
h2s = ParagraphStyle('h2s', parent=h2, fontSize=11, leading=14, spaceBefore=2, spaceAfter=2)
groups = [['A1', 'A3', 'A5', 'A7', 'A9'],
          ['A11', 'A13', 'A15', 'A17', 'A19'],
          ['A21', 'A23', 'A25', 'A27', 'A29'],
          ['B1', 'B3', 'B5']]
line_count = {'A1': 4, 'A3': 3, 'A5': 3, 'A7': 4, 'A9': 3,
              'A11': 6, 'A13': 3, 'A15': 4, 'A17': 3, 'A19': 3,
              'A21': 3, 'A23': 3, 'A25': 3, 'A27': 2,
              'A29': 3, 'B1': 5, 'B3': 5, 'B5': 4}
row_h = {'A1': 5.0, 'A3': 4.8, 'A5': 5.0, 'A7': 5.0, 'A9': 4.8,
         'A11': 5.0, 'A13': 4.8, 'A15': 5.0, 'A17': 4.8, 'A19': 4.8,
         'A21': 4.8, 'A23': 4.8, 'A25': 4.8, 'A27': 4.6,
         'A29': 4.6, 'B1': 5.2, 'B3': 5.2, 'B5': 5.0}
qs = [Paragraph('《9.22  概率论作业-孙承泽》', h1s),
      Paragraph('姓名：孙承泽　　学号：2253710052　　班级：能动强基2501', small),
      Paragraph('第一章　随机事件与概率　｜　第二版习题1　A、B奇数题', h2s),
      Paragraph('请按教材题号作答。题目依据第二版印刷页25至27誊录；图1.9、1.10、1.11已按原图重绘。', small), Spacer(1, 1.6*mm)]
for gi, group in enumerate(groups):
    if gi:
        qs.append(PageBreak())
    for label in group:
        figw = 155 if label in ('A29', 'B5') else 158
        qs.extend(render_blocks('**' + label + '.**　' + blocks[label],
                                {'h1': h1s, 'h2': h2s, 'h3': h3, 'small': small, 'body': qbody_s, 'figw': figw},
                                disp_size=9.5))
        n = line_count[label]
        rh = row_h[label]*mm
        blank = Table([[''] for _ in range(n)], colWidths=[176*mm], rowHeights=[rh]*n)
        blank.setStyle(TableStyle([('LINEBELOW', (0, 0), (-1, -1), .28, colors.HexColor('#b7b7b7'))]))
        qs += [blank, Spacer(1, 1.5*mm)]
SimpleDocTemplate(str(QPDF), pagesize=A4, rightMargin=15*mm, leftMargin=15*mm,
                  topMargin=10*mm, bottomMargin=11*mm).build(qs, onFirstPage=footer, onLaterPages=footer)

def _page_count(path):
    try:
        import pymupdf
        with pymupdf.open(str(path)) as d:
            return d.page_count
    except Exception:
        return len(re.findall(rb'/Type\s*/Page[^s]', Path(path).read_bytes()))

NP = _page_count(QPDF)
print(f'[gate] 答题纸页数={NP}（用户硬性要求：严格4页）')
assert NP == 4, f'答题纸页数门禁失败：实际{NP}页 != 4页'

# ---------------------------------------------------------------- solutions
astory = render_blocks(AMD.read_text(encoding='utf-8'),
                       {'h1': h1, 'h2': h2, 'h3': h3, 'small': small, 'body': sol, 'figw': 160}, disp_size=11.0)
SimpleDocTemplate(str(APDF), pagesize=A4, rightMargin=18*mm, leftMargin=18*mm,
                  topMargin=15*mm, bottomMargin=14*mm).build(astory, onFirstPage=footer, onLaterPages=footer)

# ---------------------------------------------------------------- quality report
rstory = render_blocks(RMD.read_text(encoding='utf-8'),
                       {'h1': h1, 'h2': h2, 'h3': h3, 'small': small, 'body': sol}, disp_size=10.5)
SimpleDocTemplate(str(RPDF), pagesize=A4, rightMargin=18*mm, leftMargin=18*mm,
                  topMargin=15*mm, bottomMargin=14*mm).build(rstory, onFirstPage=footer, onLaterPages=footer)
print(f'Built {QPDF.name} ({NP}页), {APDF.name} ({_page_count(APDF)}页), {RPDF.name} ({_page_count(RPDF)}页)')
