#!/usr/bin/env python3
# 生成《原子结构科学史作业-卢瑟福》Word 文档
# 用法: python3 build_docx.py
import re
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import os

BASE = os.path.dirname(os.path.abspath(__file__))
IMG = lambda name: os.path.join(BASE, '图卡', name)
OUT = os.path.join(BASE, '原子结构科学史作业-卢瑟福与原子核式模型.docx')

# ---------- 颜色 ----------
NAVY = RGBColor(0x1F, 0x38, 0x64)
ACCENT = RGBColor(0x2E, 0x5B, 0x94)
DARK = RGBColor(0x26, 0x26, 0x26)
GRAY = RGBColor(0x59, 0x59, 0x59)
LGRAY = RGBColor(0x8C, 0x8C, 0x8C)

# ---------- 基础工具 ----------
def fmt(run, ea='宋体', ascii_f='Times New Roman', size=12, bold=False,
        italic=False, color=None):
    run.font.name = ascii_f
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = OxmlElement('w:rFonts')
        rPr.append(rFonts)
    rFonts.set(qn('w:ascii'), ascii_f)
    rFonts.set(qn('w:hAnsi'), ascii_f)
    rFonts.set(qn('w:eastAsia'), ea)
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    if color is not None:
        run.font.color.rgb = color

def indent2(p):
    pPr = p._p.get_or_add_pPr()
    ind = pPr.find(qn('w:ind'))
    if ind is None:
        ind = OxmlElement('w:ind')
        pPr.append(ind)
    ind.set(qn('w:firstLineChars'), '200')
    ind.set(qn('w:firstLine'), '480')

def new_par(doc, before=0, after=6, line=1.5):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)
    pf.line_spacing = line
    return p

def rich(p, text, ea='宋体', size=12, color=DARK, bold=False, ascii_f='Times New Roman'):
    """支持 **加粗** 的段落写入"""
    for part in re.split(r'(\*\*.+?\*\*)', text):
        if not part:
            continue
        if part.startswith('**') and part.endswith('**'):
            r = p.add_run(part[2:-2])
            fmt(r, ea=ea, ascii_f=ascii_f, size=size, bold=True, color=NAVY)
        else:
            r = p.add_run(part)
            fmt(r, ea=ea, ascii_f=ascii_f, size=size, bold=bold, color=color)
    return p

def body(doc, text, indent=True, size=12, after=6, line=1.5, color=DARK, ea='宋体'):
    p = new_par(doc, after=after, line=line)
    if indent:
        indent2(p)
    rich(p, text, ea=ea, size=size, color=color)
    return p

def list_item(doc, marker, text, size=12):
    p = new_par(doc, after=4, line=1.45)
    p.paragraph_format.left_indent = Cm(0.75)
    p.paragraph_format.first_line_indent = Cm(-0.5)
    r = p.add_run(marker + ' ')
    fmt(r, size=size, bold=True, color=ACCENT, ascii_f='Arial')
    rich(p, text, size=size)
    return p

def h1(doc, text):
    p = doc.add_paragraph(style='Heading 1')
    p.paragraph_format.space_before = Pt(18)
    p.paragraph_format.space_after = Pt(8)
    r = p.add_run(text)
    fmt(r, ea='黑体', ascii_f='Arial', size=15, bold=True, color=NAVY)
    return p

def h2(doc, text):
    p = doc.add_paragraph(style='Heading 2')
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(6)
    r = p.add_run(text)
    fmt(r, ea='黑体', ascii_f='Arial', size=12.5, bold=True, color=ACCENT)
    return p

def shade(cell, fill):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill)
    tcPr.append(shd)

def table_borders(table, color='BFBFBF', sz='4', val='single'):
    tblPr = table._tbl.tblPr
    borders = OxmlElement('w:tblBorders')
    for e in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        el = OxmlElement('w:' + e)
        el.set(qn('w:val'), val)
        el.set(qn('w:sz'), sz)
        el.set(qn('w:space'), '0')
        el.set(qn('w:color'), color)
        borders.append(el)
    tblPr.append(borders)

def table_noborders(table):
    table_borders(table, val='none')

def cell_margins(table, top=100, bottom=100, left=160, right=160):
    tblPr = table._tbl.tblPr
    m = OxmlElement('w:tblCellMar')
    for tag, v in (('top', top), ('left', left), ('bottom', bottom), ('right', right)):
        el = OxmlElement('w:' + tag)
        el.set(qn('w:w'), str(v))
        el.set(qn('w:type'), 'dxa')
        m.append(el)
    tblPr.append(m)

def quote_box(doc, lines, fill='F2F6FB', border='9DB6D9', size=11.5):
    """lines: list of (text, {kwargs}) 或 str"""
    t = doc.add_table(rows=1, cols=1)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_borders(t, color=border, sz='6')
    cell_margins(t, top=180, bottom=180, left=240, right=240)
    cell = t.cell(0, 0)
    cell.width = Cm(15.8)
    shade(cell, fill)
    first = True
    for item in lines:
        if isinstance(item, tuple):
            text, kw = item
        else:
            text, kw = item, {}
        if first:
            p = cell.paragraphs[0]
            first = False
        else:
            p = cell.add_paragraph()
        p.paragraph_format.line_spacing = 1.4
        p.paragraph_format.space_after = Pt(kw.pop('after', 2))
        if kw.pop('center', False):
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        rich(p, text, size=kw.pop('size', size), color=kw.pop('color', DARK),
             ea=kw.pop('ea', '宋体'), bold=kw.pop('bold', False))
    sp = new_par(doc, after=4)
    return t

def figure(doc, path, caption, width_cm=14.5):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(4)
    p.add_run().add_picture(path, width=Cm(width_cm))
    cap = doc.add_paragraph()
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap.paragraph_format.space_after = Pt(10)
    r = cap.add_run(caption)
    fmt(r, ea='楷体', ascii_f='Times New Roman', size=9.5, color=GRAY, bold=True)

def add_field(par, instr, size=9, color=LGRAY):
    runs = []
    r1 = par.add_run()
    f1 = OxmlElement('w:fldChar'); f1.set(qn('w:fldCharType'), 'begin'); r1._r.append(f1)
    r2 = par.add_run()
    it = OxmlElement('w:instrText'); it.set(qn('xml:space'), 'preserve'); it.text = instr
    r2._r.append(it)
    r3 = par.add_run()
    f2 = OxmlElement('w:fldChar'); f2.set(qn('w:fldCharType'), 'separate'); r3._r.append(f2)
    r4 = par.add_run('1')
    r5 = par.add_run()
    f3 = OxmlElement('w:fldChar'); f3.set(qn('w:fldCharType'), 'end'); r5._r.append(f3)
    for r in (r1, r2, r3, r4, r5):
        fmt(r, ascii_f='Arial', ea='宋体', size=size, color=color)
    runs.extend((r1, r2, r3, r4, r5))
    return runs

def hrule(p, color='BFBFBF', sz='6', space='4'):
    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    b = OxmlElement('w:bottom')
    b.set(qn('w:val'), 'single'); b.set(qn('w:sz'), sz)
    b.set(qn('w:space'), space); b.set(qn('w:color'), color)
    pBdr.append(b)
    pPr.append(pBdr)

# ---------- 文档 ----------
doc = Document()
doc.core_properties.title = '原子结构科学史作业——卢瑟福与原子核式结构模型的诞生'
doc.core_properties.author = '大学化学课程作业'

# 页面
sec = doc.sections[0]
sec.page_width = Cm(21.0)
sec.page_height = Cm(29.7)
sec.top_margin = Cm(2.4)
sec.bottom_margin = Cm(2.2)
sec.left_margin = Cm(2.5)
sec.right_margin = Cm(2.5)
sec.different_first_page_header_footer = True

# Normal 样式
normal = doc.styles['Normal']
normal.font.name = 'Times New Roman'
normal.font.size = Pt(12)
normal.element.get_or_add_rPr()
rf = normal.element.rPr.find(qn('w:rFonts'))
if rf is None:
    rf = OxmlElement('w:rFonts'); normal.element.rPr.append(rf)
rf.set(qn('w:eastAsia'), '宋体')

# 标题样式（保证导航窗格可见）
for name, size, color in (('Heading 1', 15, NAVY), ('Heading 2', 12.5, ACCENT)):
    st = doc.styles[name]
    st.font.name = 'Arial'
    st.font.size = Pt(size)
    st.font.bold = True
    st.font.color.rgb = color
    st.element.get_or_add_rPr()
    st_rPr = st.element.rPr
    st_rf = st_rPr.find(qn('w:rFonts'))
    if st_rf is None:
        st_rf = OxmlElement('w:rFonts'); st_rPr.append(st_rf)
    st_rf.set(qn('w:eastAsia'), '黑体')

# 页眉（第 2 页起）
hp = sec.header.paragraphs[0]
hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
hr = hp.add_run('西安交通大学 化学学院 · 大学化学课程作业')
fmt(hr, ea='黑体', ascii_f='Arial', size=8.5, color=LGRAY)
hrule(hp, color='D9D9D9', sz='4', space='2')

# 页脚（第 2 页起，页码）
fp = sec.footer.paragraphs[0]
fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = fp.add_run('第 '); fmt(r, ascii_f='Arial', size=9, color=LGRAY)
add_field(fp, 'PAGE')
r = fp.add_run(' 页 / 共 '); fmt(r, ascii_f='Arial', size=9, color=LGRAY)
add_field(fp, 'NUMPAGES')
r = fp.add_run(' 页'); fmt(r, ascii_f='Arial', size=9, color=LGRAY)

# ================= 封面 =================
p = new_par(doc, after=2, line=1.0)
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run('西安交通大学 · 化学学院')
fmt(r, ea='黑体', ascii_f='Arial', size=13, bold=True, color=GRAY)
hrule(p, color='9DB6D9', sz='8', space='6')

p = new_par(doc, before=6, after=10, line=1.0)
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.add_run().add_picture(IMG('图1-封面-原子.png'), width=Cm(15.6))

p = new_par(doc, before=14, after=4, line=1.2)
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run('像把“15英寸炮弹”射向一张薄纸')
fmt(r, ea='黑体', ascii_f='Arial', size=21, bold=True, color=NAVY)

p = new_par(doc, after=16, line=1.2)
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run('—— 欧内斯特·卢瑟福与原子核式结构模型的诞生')
fmt(r, ea='楷体', ascii_f='Arial', size=13, color=ACCENT)

meta = doc.add_table(rows=5, cols=2)
meta.alignment = WD_TABLE_ALIGNMENT.CENTER
table_noborders(meta)
cell_margins(meta, top=60, bottom=60, left=0, right=120)
meta_rows = [
    ('课　　程', '大学化学'),
    ('作　　业', '原子结构认识的科学史 · 我最钦佩的科学家'),
    ('姓　　名', '孙承泽　　　　　学号：2253710052'),
    ('班　　级', '能动强基2501'),
    ('日　　期', '2026 年 9 月 16 日'),
]
for i, (k, v) in enumerate(meta_rows):
    c0, c1 = meta.rows[i].cells
    c0.width = Cm(2.8)
    c1.width = Cm(11.0)
    p0 = c0.paragraphs[0]; p0.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r = p0.add_run(k); fmt(r, ea='黑体', ascii_f='Arial', size=11, color=GRAY)
    p1 = c1.paragraphs[0]
    r = p1.add_run(v); fmt(r, size=11, color=DARK)

p = new_par(doc, before=22, after=0, line=1.0)
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run('全文约 3000 字 · 配图 5 幅 · 供思源学堂（讨论模块）分享')
fmt(r, ea='楷体', size=9.5, color=LGRAY)

doc.add_page_break()

# ================= 正文 =================
quote_box(doc, [
    ('**导读 · 一句话概括本文**', {'size': 12, 'after': 4}),
    ('1909 年，两位科研助手在黑暗的实验室里，用显微镜数了数周的闪光——其中约 1/8000 的闪光出现在“绝不可能”的位置。正是这微小的意外，推翻了当时主流十余年的原子模型，把人类带进了原子核时代。下文以卢瑟福的金箔实验为核心，讲这个故事，以及他为什么是我在原子结构科学史中最钦佩的科学家。', {'size': 11.5}),
], fill='F2F6FB', border='9DB6D9')

# ---------- 一 ----------
h1(doc, '一、我最钦佩的科学家：欧内斯特·卢瑟福（Ernest Rutherford）')

pt = doc.add_table(rows=1, cols=2)
pt.alignment = WD_TABLE_ALIGNMENT.CENTER
table_noborders(pt)
cell_margins(pt, top=40, bottom=40, left=60, right=140)
cl, cr = pt.rows[0].cells
cl.width = Cm(5.6)
cr.width = Cm(10.0)
shade(cl, 'F7F9FC')
pimg = cl.paragraphs[0]
pimg.alignment = WD_ALIGN_PARAGRAPH.CENTER
pimg.paragraph_format.space_before = Pt(6)
pimg.add_run().add_picture(IMG('图2-卢瑟福肖像.png'), width=Cm(5.0))
cap = cl.add_paragraph()
cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
cap.paragraph_format.space_after = Pt(6)
r = cap.add_run('图 1　卢瑟福画像（概念示意图）')
fmt(r, ea='楷体', size=9, color=GRAY, bold=True)

profile = [
    ('**欧内斯特·卢瑟福**（1871—1937），生于新西兰纳尔逊省的一个贫苦农家，家中十二个孩子，他排行第三。1895 年，19 岁的他以奖学金进入英国剑桥大学三一学院，获博士学位后留校任教。', {'after': 4}),
    ('此后他历任麦吉尔大学、曼彻斯特大学物理学教授，1919 年回英执掌剑桥大学卡文迪许实验室（接替他的老师 J.J. 汤姆孙），1926 年赴加拿大，被誉为加拿大历史上第一位“科学大臣”（正式头衔为麦吉尔大学访问教授）。', {'after': 4}),
    ('1908 年，他因“对元素衰变和放射性物质化学的研究”获得**诺贝尔化学奖**（与索迪及另一位同名的英国化学家 E·卢瑟福共同获得）。1931 年受封“纳尔逊的卢瑟福男爵”，是 20 世纪因物理学成就受封贵族、极为罕见的科学家。1937 年 10 月 19 日，卢瑟福因肾结石并发感染在剑桥去世，享年 66 岁。', {'after': 4}),
    ('他一生工作横跨“原子能”的三个起点：放射性、原子核、人工核反应。科学界尊称他为**“原子核物理学之父”**。', {'after': 2}),
]
first = True
for text, kw in profile:
    if first:
        p = cr.paragraphs[0]; first = False
    else:
        p = cr.add_paragraph()
    p.paragraph_format.line_spacing = 1.35
    p.paragraph_format.space_after = Pt(kw['after'])
    rich(p, text, size=11)

h2(doc, '他的两句名言')
quote_box(doc, [
    ('“这就像用 15 英寸口径的炮弹射击一张薄纸，炮弹却弹回来打中自己。”', {'size': 11.5, 'after': 2}),
    ('—— 卢瑟福，1911 年，描述金箔实验的惊人结果', {'size': 10, 'color': GRAY, 'after': 8}),
    ('“所有科学，要么就是物理学，要么就是集邮。”', {'size': 11.5, 'after': 2}),
    ('—— 广为流传的卢瑟福俏皮话（强调科学要讲定量理解，而非仅仅分类收藏）', {'size': 10, 'color': GRAY, 'after': 2}),
], fill='FFF9EF', border='E3D3AC')

# ---------- 二 ----------
h1(doc, '二、背景：世纪之交，原子“不可分”的光环')
body(doc, '从古希腊德谟克利特提出“原子”（atomos，不可再分）一词，到 1803 年道尔顿的实心球模型，两千年来原子一直被视为物质的最小单位、一个“没有内部结构的小球”。1897 年，J.J. 汤姆孙发现了**电子**——人类找到的第一个亚原子粒子，“原子不可分”的观念第一次被打破：原子既然含有更小的粒子，它内部到底是什么样子？')
body(doc, '1904 年，汤姆孙提出“**葡萄干布丁模型**”（又称“梅子布丁模型”）：原子像一个均匀的正电“布丁”，带负电的电子像葡萄干一样嵌在其中，原子整体呈电中性。这个模型随后十几年里是教科书的标准答案，被认为是原子结构问题的“圆满解答”。')
body(doc, '但矛盾暗藏其中：如果正电荷真的均匀摊在整个球里，那么一个高速、带 2 个正电荷、质量较大的 α 粒子穿过去时，受到的排斥力应当非常弱——就像“用重型炮弹射击一袋棉花”。1909 年，曼彻斯特的两位助手真的做了这个实验，结果完全相反。')

# ---------- 三 ----------
h1(doc, '三、经典研究成果：金箔实验（1909）')
h2(doc, '3.1　简单的装置，巨大的问题')
body(doc, '在卢瑟福的指导下，盖革（H. Geiger）和马斯登（E. Marsden）在曼彻斯特大学做了 α 粒子散射实验。装置极其朴素，设计却极为讲究：', after=4)
list_item(doc, '①', '**源**：放射性元素钋放出的 α 粒子（相当于氦核，带 2 个单位正电荷），速度约 1.6×10⁷ m/s，又重又快；')
list_item(doc, '②', '**靶**：金箔。金延展性极好，可以锤成仅约 400 个原子层厚的薄膜，且不易氧化——这是唯一能把它做得这么“薄”的金属；')
list_item(doc, '③', '**探测**：硫化锌（ZnS）荧光屏，α 粒子打到它上面会发出一个个微小闪光。盖革和马斯登在暗室里用显微镜**逐个数闪光**，一干就是数周；')
list_item(doc, '④', '**巧妙之处**：荧光屏可以绕金箔摆到不同角度的位置——闪光出现在哪个角度，就说明粒子被偏转到了哪里。')
figure(doc, IMG('图3-金箔实验示意.png'), '图 2　盖革–马斯登金箔实验示意图（概念图）：多数 α 粒子直线穿过，极少数大角度偏转甚至折返', 14.5)

h2(doc, '3.2　八千分之一：意外的那道光')
body(doc, '如果“葡萄干布丁模型”正确，α 粒子应该几乎全部直线穿过金箔，最大偏转角不超过约 1°。但数据讲述了一个完全不同的故事：**绝大多数 α 粒子确实直直穿过，可每约 8000 个里就有 1 个偏转角超过 90°，有的几乎被原路弹回。**')
quote_box(doc, [
    ('卢瑟福后来用一句话形容这种震惊：“这是我一生中遇到的最难以置信的事情。**这就像用 15 英寸口径的炮弹射击一张薄纸，炮弹却弹回来打中自己。**”', {'size': 11.5}),
], fill='F2F6FB', border='9DB6D9')
body(doc, '**一个小故事**：晚年，当有人问他做金箔实验时“原本期待什么结果”，卢瑟福回答：“如果实验结果和我预期的那样，我只能说我们干了一大堆糟糕的工作。正因为它是这么意外的结果，才有趣到值得花上几年时间去琢磨。”——在卢瑟福眼里，**反常不是失败，而是大自然递来的邀请函**。')

h2(doc, '3.3　定量推理：斥力从何而来？')
body(doc, '卢瑟福的推理只有两步，却环环相扣：', after=4)
list_item(doc, '第一步', 'α 粒子重、快、带 2 个正电荷，只有**极强的静电排斥力**才能让它大角度偏转；')
list_item(doc, '第二步', '库仑力随距离急剧增大（与距离平方成反比）——要在“一次相遇”中产生近 180° 的反弹，原子的**全部正电荷和几乎全部质量必须集中在中心一个极小的区域**。')
body(doc, '接着他做了一次漂亮的数量级估算：对正对碰撞的粒子，由动能全部转化为库仑势能可得最近距离 d = 2kZe²/(mv²)。代入 α 粒子参数，得到这个“核心”的直径不超过约 10⁻¹³ ~ 10⁻¹⁴ m——比整个原子（约 10⁻¹⁰ m）**小至少一万倍**。他给这个核心起了个名字：**原子核**。', ea='宋体')

# ---------- 四 ----------
h1(doc, '四、核式结构模型（1911）：一幅被彻底换掉的图景')
body(doc, '1911 年 1 月，卢瑟福向英国皇家学会宣读论文《α 和 β 粒子在物质中的散射与原子结构》。有个耐人寻味的细节：当时卢瑟福还不是皇家学会会员，按规定不能亲自宣读，于是由时任皇家学会主席、他的老师 J.J. 汤姆孙代为宣读——**旧模型的缔造者，亲手把新模型推上了台**。历史的一丝黑色幽默。')
body(doc, '核式结构模型的内容只有三句话：', after=4)
quote_box(doc, [
    ('**①** 原子中心有一个**原子核**，体积极小，却集中了全部正电荷和几乎全部原子质量；', {'size': 11.5, 'after': 3}),
    ('**②** 电子在核外空间**绕核运动**，靠库仑引力维系；', {'size': 11.5, 'after': 3}),
    ('**③** 原子的绝大部分体积是“**空旷**”的。', {'size': 11.5, 'after': 2}),
], fill='F2F6FB', border='9DB6D9')
figure(doc, IMG('图4-两种原子模型对比.png'), '图 3　左：汤姆孙“葡萄干布丁模型”（1904）；右：卢瑟福核式模型（1911）——概念对比图', 14.5)
body(doc, '与“摊开的布丁”相比，“浓缩的核”把原子的图景彻底换了。但新模型也留下一个当时无法解答的问题：按经典电磁理论，绕核运动的电子会不断辐射能量、轨道收缩，约 10⁻¹¹ 秒内就会“螺旋坠入”原子核——原子不该稳定存在。卢瑟福心里清楚这一点，但他坚持先把实验撑起来的模型交出去；**剩下的难题，交给接棒的人**。')
h2(doc, '模型的接力')
list_item(doc, '1913', '**玻尔**把量子化条件引入核式模型，提出定态轨道，成功解释了氢原子光谱——核式模型第一次有了“理论外壳”；')
list_item(doc, '1919', '**卢瑟福**用 α 粒子轰击氮气，实现了人类历史上第一次**人工核反应**（元素嬗变）：⁴He + ¹⁴N → ¹H + ¹⁷O，并在这个过程中发现了质子；')
figure(doc, IMG('图5-首次人工核嬗变.png'), '图 4　1919 年首次人工核嬗变：α 粒子（4 个球）轰击氮核，打出质子（白球），生成氧-17（17 个球）——概念图', 12.5)
list_item(doc, '1926', '**薛定谔**建立波方程，原子结构进入量子力学时代（轨道、电子云）；')
list_item(doc, '1932', '**查德威克**（卢瑟福的学生）发现中子。')
body(doc, '从汤姆孙到卢瑟福，从卢瑟福到玻尔、薛定谔——原子结构模型从来不是某个天才的“终极答案”，而是一棒接一棒的接力。')

# ---------- 五 ----------
h1(doc, '五、我为什么最钦佩他')
list_item(doc, '1. 敢于推翻权威。', '他推翻的模型，正是他的老师、教科书和整个学界的“标准答案”。他依靠的不是更精密的仪器，而是别人可能归为“误差”的 1/8000——**权威可以让位于一个诚实的反常数据**。')
list_item(doc, '2. 实验的美学。', '铅块、狭缝、一片金箔、一块荧光屏——装置简单到学生实验室就能搭起来，问的却是最根本的问题：“原子长什么样？”这正是他推崇的风格：**用最简单的方式，逼问最本质的问题**。')
list_item(doc, '3. 让“意外”说话。', '“如果结果如我所料，只能说我们干了糟糕的工作。”反常不是失败，是大自然递来的邀请函。这种对待异常数据的姿态，比任何具体结论都更值得学习。')
list_item(doc, '4. 量化的力量。', '“所有科学要么就是物理学，要么就是集邮。”核式模型不是凭空猜想：他用库仑力和偏转角，把一个定性的图景钉在了 10⁻¹³ ~ 10⁻¹⁴ m 的数量级上。**定性给图景，定量给边界**，这是现代科学方法最好的示范。')
list_item(doc, '5. 接力的品格。', '盖革、马斯登、查德威克（中子的发现者）……卢瑟福执掌下的卡文迪许实验室被誉为“物理学的哈佛”。他不仅自己改变了模型，还培养了一批继续改变模型的人。**最顶级的科学家，也是最好的传球手**。')

# ---------- 六 ----------
h1(doc, '六、反思：接力，与这门课')
body(doc, '这次作业，老师给了我们 PhET 的“Build an Atom（搭建原子）”模拟。在模拟里，我们拖拽质子、中子和电子，辨认同位素、判断核的稳定性——我们现在能如此轻松地“搭建”原子，靠的正是卢瑟福和同时代人们用无数个荧光闪光换来的那幅图景。**历史让我意识到：模拟软件里每一个按钮背后，都站着一串真实的人。**')
body(doc, '原子结构模型的一百年接力，大致是这样的：', after=6)

rows = [
    ('年份', '科学家', '里程碑'),
    ('1803', '道尔顿', '实心球模型：原子是不可再分的实心小球'),
    ('1897', 'J.J. 汤姆孙', '发现电子：原子有内部结构'),
    ('1904', 'J.J. 汤姆孙', '“葡萄干布丁模型”'),
    ('1909', '盖革、马斯登（卢瑟福指导）', '金箔实验：1/8000 的大角度散射'),
    ('1911', '卢瑟福', '**核式结构模型**：原子核的发现'),
    ('1913', '玻尔', '定态轨道模型，解释氢原子光谱'),
    ('1919', '卢瑟福', '首次人工核嬗变，发现质子'),
    ('1926', '薛定谔', '波方程：原子结构的量子力学模型'),
    ('1932', '查德威克', '发现中子'),
    ('今天', '——', '量子力学模型：量子数、轨道、电子云（本课程正在学的“现代原子结构模型”）'),
]
tt = doc.add_table(rows=len(rows), cols=3)
tt.alignment = WD_TABLE_ALIGNMENT.CENTER
table_borders(tt, color='C9D6EA', sz='4')
cell_margins(tt, top=70, bottom=70, left=110, right=110)
widths = (Cm(1.9), Cm(4.9), Cm(9.0))
for i, row in enumerate(rows):
    for j, text in enumerate(row):
        cell = tt.rows[i].cells[j]
        cell.width = widths[j]
        p = cell.paragraphs[0]
        p.paragraph_format.line_spacing = 1.25
        p.paragraph_format.space_after = Pt(0)
        if i == 0:
            shade(cell, '1F3864')
            r = p.add_run(text)
            fmt(r, ea='黑体', ascii_f='Arial', size=10.5, bold=True, color=RGBColor(0xFF, 0xFF, 0xFF))
        else:
            if i % 2 == 0:
                shade(cell, 'F4F8FD')
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if j < 2 else WD_ALIGN_PARAGRAPH.LEFT
            if '**' in text:
                rich(p, text, size=10.5)
            else:
                r = p.add_run(text)
                fmt(r, size=10.5, color=DARK)
new_par(doc, after=8)
body(doc, '原子不是我们“看见”的，而是被一代代人**建立**出来的模型——并且这个模型今后还会被继续修正、继续深化。也许若干年后，在某位今天还在读书的人手里，会出现属于他们时代的“1/8000”。')

# ---------- 参考文献 ----------
h1(doc, '参考文献')
refs = [
    '[1] Rutherford E. The Scattering of α and β Particles by Matter and the Structure of the Atom[J]. Philosophical Magazine, 1911, 21(125): 669-688.',
    '[2] Geiger H, Marsden E. On a Diffusion Theory of α-Particle Scattering[J]. Philosophical Magazine, 1909, 18(119): 209-223.',
    '[3] Rutherford E. Collision of α particles with light atoms. IV. A new class of radiations from nitrogen[J]. Philosophical Magazine, 1919, 37(220): 581-603.',
    '[4] Segrè E. From X-rays to Quarks: A History of Modern Physics[M]. New York: Free Press, 1980.',
    '[5] University of Colorado Boulder. Build an Atom: Simulations[EB/OL]. https://phet.colorado.edu/sims/html/build-an-atom/latest/build-an-atom_all.html?locale=zh_CN .',
    '[6] 天津大学等. 普通化学（第 4 版）[M]. 北京: 高等教育出版社, 2018.（原子结构章节）',
]
for ref in refs:
    p = new_par(doc, after=3, line=1.3)
    r = p.add_run(ref)
    fmt(r, size=10, color=GRAY)

p = new_par(doc, before=14, after=0, line=1.0)
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run('—— 全文完（本文配图均为概念示意图，供课堂讨论使用）——')
fmt(r, ea='楷体', size=9.5, color=LGRAY)

doc.save(OUT)
print('OK', OUT)
