#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
零基础重写补丁：为现有期中精析 docx 增加零基础推导层
- 覆盖全册96题的“零基础再讲”盒
- 重写封面标题为“零基础完全版”
- 在每章开头增加“零基础起点”导读
- 为Q2等重难点插入动图
"""
import pathlib
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.enum.table import WD_TABLE_ALIGNMENT

DOCX = pathlib.Path("大学物理/期中复习/大学物理期中_12-15次作业图文精析_孙承泽_2253710052.docx")
Q2_FIG = pathlib.Path("tmp_generated_figs/q2_zero_basic.png")
Q2_FIG2 = pathlib.Path("tmp_generated_figs/q2_standing_vs_travel.png")

def set_cell_bg(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:fill'), hex_color)
    shd.set(qn('w:val'), 'clear')
    tcPr.append(shd)

def make_tip_paragraph(doc_obj, title, content, bg="FFF8E1", icon="🌱"):
    # Create a 1x1 table as tip box at end, return its element to move later
    table = doc_obj.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    table.columns[0].width = Inches(6.2)
    cell = table.cell(0,0)
    set_cell_bg(cell, bg)
    # padding
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for edge in ['top','left','bottom','right']:
        m = OxmlElement(f'w:{edge}')
        m.set(qn('w:w'), '80')
        m.set(qn('w:type'), 'dxa')
        tcMar.append(m)
    tcPr.append(tcMar)
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = p.add_run(f"{icon} {title}")
    run.bold = True
    run.font.size = Pt(9.5)
    run.font.color.rgb = RGBColor(0x1A,0x3A,0x5C)
    run.font.name = 'Times New Roman'
    run._element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')
    p2 = cell.add_paragraph()
    # content may be multiline; preserve line breaks
    for line in content.split("\n"):
        run2 = p2.add_run(line)
        run2.font.size = Pt(8.8)
        run2.font.color.rgb = RGBColor(0x33,0x33,0x33)
        run2.font.name = 'Times New Roman'
        run2._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
        if line != content.split("\n")[-1]:
            run2.add_break()
    p2.paragraph_format.space_before = Pt(2)
    # Add spacing control
    for par in [p, p2]:
        par.paragraph_format.space_after = Pt(2)
        par.paragraph_format.space_before = Pt(2)
    doc_obj.add_paragraph()  # spacer
    # Return table element (the last table)
    return table

def create_para_element(text, bold=False, size=Pt(9), color=None, align=WD_ALIGN_PARAGRAPH.LEFT, italic=False, east="宋体"):
    p = OxmlElement('w:p')
    pPr = OxmlElement('w:pPr')
    jc = OxmlElement('w:jc')
    align_map = {WD_ALIGN_PARAGRAPH.CENTER:'center', WD_ALIGN_PARAGRAPH.LEFT:'left', WD_ALIGN_PARAGRAPH.RIGHT:'right', WD_ALIGN_PARAGRAPH.JUSTIFY:'both'}
    jc.set(qn('w:val'), align_map.get(align,'left'))
    pPr.append(jc)
    spacing = OxmlElement('w:spacing')
    spacing.set(qn('w:after'), '60')
    spacing.set(qn('w:before'), '40')
    pPr.append(spacing)
    p.append(pPr)
    r = OxmlElement('w:r')
    rPr = OxmlElement('w:rPr')
    rFonts = OxmlElement('w:rFonts')
    rFonts.set(qn('w:ascii'), 'Times New Roman')
    rFonts.set(qn('w:eastAsia'), east)
    rPr.append(rFonts)
    sz = OxmlElement('w:sz')
    sz.set(qn('w:val'), str(int(size.pt*2)))
    rPr.append(sz)
    if bold:
        b = OxmlElement('w:b'); rPr.append(b)
    if italic:
        i = OxmlElement('w:i'); rPr.append(i)
    if color:
        c = OxmlElement('w:color')
        c.set(qn('w:val'), f"{color[0]:02X}{color[1]:02X}{color[2]:02X}")
        rPr.append(c)
    r.append(rPr)
    t = OxmlElement('w:t')
    t.set(qn('xml:space'), 'preserve')
    t.text = text
    r.append(t)
    p.append(r)
    return p

def insert_after(paragraph, new_element):
    paragraph._element.addnext(new_element)

# Load doc
doc = Document(str(DOCX))
print(f"Loaded {DOCX} paragraphs={len(doc.paragraphs)} tables={len(doc.tables)}")

# 1. 修改封面标题：找到"期中考试·图文精析"后插入"零基础完全版"
for p in doc.paragraphs:
    if "期中考试·图文精析" in p.text:
        # add next paragraph
        new_p = create_para_element("—— 零基础完全版 · 从人浪到公式，每一步都推给你看 ——", bold=True, size=Pt(11), color=(0xC0,0x39,0x2B), align=WD_ALIGN_PARAGRAPH.CENTER, east="黑体")
        insert_after(p, new_p)
        print("Inserted zero subtitle after cover title")
        break

# 2. 在目录后、第一章前插入“零基础10分钟预备” （找到 Heading1 "一、期中范围"）
for p in doc.paragraphs:
    if p.style.name.startswith("Heading 1") and "一、期中范围" in p.text:
        # Insert a tip box equivalent via paragraph elements, but easier: create a table via doc.add_table at end and move
        # We will create a standalone section via elements, then insert
        # Create a heading for zero guide
        h = create_para_element("零基础 10分钟预备：先会这5句话，后面96题全通", bold=True, size=Pt(12), color=(0x1A,0x3A,0x5C), align=WD_ALIGN_PARAGRAPH.LEFT, east="黑体")
        # add bottom border
        pPr = h.find(qn('w:pPr'))
        # but we can just insert
        insert_after(p, h)
        # Insert 5 sentences as paragraphs after h (in reverse order for correct final order)
        sentences = [
            "第5句：看题先问“横轴是x还是t”—— x是照相（波形），t是录像（振动），别混。",
            "第4句：能量：行波动能势能一起鼓，驻波动能挤在波腹、势能挤在波节。",
            "第3句：光程差 = 2nd ± 半波个数·λ/2，数“光疏→光密”的反射次数，奇数就加。",
            "第2句：往哪传？追波峰：时间变大，峰往右= +x，峰往左= -x（图Q2）。",
            "第1句：波 = 振动的延迟：x处的振动是源点x/u秒以前的振动，所以 y(x,t)=Acos[ω(t∓x/u)+φ]。",
        ]
        cur = h
        for s in sentences:
            para = create_para_element("· "+s, bold=False, size=Pt(9), color=(0x33,0x33,0x33), align=WD_ALIGN_PARAGRAPH.LEFT)
            cur.addnext(para)
            cur = para
        print("Inserted zero guide 5 sentences")
        break

# 3. 为每章开头插入“零基础起点”
# Find Heading1 of each major chapter and insert a box
chapter_intros = {
    "二、第十二次": "本章起点：先把 y=Acos[ω(t - x/u)+φ] 抄5遍，再记住 u=λf=ω/k。后面10道选择全是它的变形。",
    "三、第十三次": "本章起点：干涉就看光程差。先画两束光谁比谁多走了2nd，再数半波。薄膜、劈尖、牛顿环、迈克尔逊全一样。",
    "四、第十四次": "本章起点：a管暗(dark)，d管明(bright)，d/a管缺。中央宽=2fλ/a，记住这一个，后面全推。",
    "五、第十五次": "本章起点：偏振就是投影。自然光先减半，马吕斯用cos²，布儒斯特定律 i_B=arctan(n₂/n₁)，波片看Δn·d。",
}
for p in list(doc.paragraphs):
    for key, intro in chapter_intros.items():
        if p.style.name.startswith("Heading 1") and key in p.text:
            tip = create_para_element(f"🌱 零基础起点：{intro}", bold=True, size=Pt(9), color=(0x1A,0x3A,0x5C), align=WD_ALIGN_PARAGRAPH.LEFT, east="宋体")
            # give background via shading? use simple paragraph with border via table? Keep as paragraph with light bg via shading
            # add shading to paragraph
            pPr = tip.find(qn('w:pPr'))
            shd = OxmlElement('w:shd')
            shd.set(qn('w:fill'), 'EAF2F8')
            shd.set(qn('w:val'), 'clear')
            pPr.append(shd)
            insert_after(p, tip)
            print(f"Inserted intro for {key}")
            break

# Helper to insert zero box after a specific Heading3
def insert_zero_box_after_q(doc, q_keyword, title, content, fig_path=None, fig_caption=None):
    # Find paragraph with Heading3 containing q_keyword
    target = None
    for p in doc.paragraphs:
        if p.style.name == "Heading 3" and q_keyword in p.text:
            target = p
            break
    if not target:
        print(f"NOT FOUND Q {q_keyword}")
        return
    # We need to find the end of this question block: it ends before next Heading3/Heading2/Heading1
    # Instead, we will insert immediately after the "【解析】" paragraph and its following tip box if exists.
    # Simpler: insert after the next paragraph that contains "易错/秒杀" or after the analysis paragraph.
    # Find the paragraph that is the analysis (contains "【解析】") that belongs to this Q
    # Walk forward from target until we hit next Heading
    idx = next((i for i, pp in enumerate(doc.paragraphs) if pp._p is target._p), -1)
    if idx==-1:
        print(f"NOT FOUND idx for {q_keyword}")
        return
    insert_anchor = None
    # Look ahead up to 10 paragraphs for the analysis paragraph
    for j in range(idx+1, min(idx+15, len(doc.paragraphs))):
        p = doc.paragraphs[j]
        if p.style.name.startswith("Heading"):
            break
        if "【解析】" in p.text:
            insert_anchor = p
        # If we see a tip box table, its following paragraph is spacer; but we can just insert after analysis
    if not insert_anchor:
        insert_anchor = target
    # Now create the zero box as a table at end and move it after insert_anchor
    # Create table via doc.add_table then move
    # Create content
    # Use make_tip_paragraph helper but we need to create table and move
    # We'll create the table now at end
    # To avoid needing to find it, we create via Oxml directly: make a table element
    # Simpler: use doc.add_table at end, then move its element
    # Create the tip box
    # We will directly create Oxml table for zero box to insert after anchor
    # Instead, use helper that creates table at end and then move
    # Let's create a temporary doc table and then move its element
    # Use the function make_tip_paragraph that adds at end
    # But we need to capture the table element
    # We'll call a custom creation that directly creates Oxml table and inserts after anchor
    # Simpler: call make_tip_paragraph and then move the last table
    before_tables = len(doc.tables)
    # Create a temporary table at end via helper (we'll reuse logic but need to avoid adding spacer paragraph)
    # We will manually create table Oxml

    # Create table element
    tbl = OxmlElement('w:tbl')
    tblPr = OxmlElement('w:tblPr')
    tblW = OxmlElement('w:tblW')
    tblW.set(qn('w:w'), '0')
    tblW.set(qn('w:type'), 'auto')
    tblPr.append(tblW)
    tblPr2 = OxmlElement('w:tblPr')
    # Borders
    tblBorders = OxmlElement('w:tblBorders')
    for border_name in ['top','left','bottom','right','insideH','insideV']:
        b = OxmlElement(f'w:{border_name}')
        b.set(qn('w:val'), 'single')
        b.set(qn('w:sz'), '4')
        b.set(qn('w:space'), '0')
        b.set(qn('w:color'), 'A9CCE3')
        tblBorders.append(b)
    tblPr.append(tblBorders)
    tbl.append(tblPr)
    # Row
    tr = OxmlElement('w:tr')
    tc = OxmlElement('w:tc')
    tcPr = OxmlElement('w:tcPr')
    shd = OxmlElement('w:shd')
    shd.set(qn('w:fill'), 'FFF8E1')
    shd.set(qn('w:val'), 'clear')
    tcPr.append(shd)
    # cell margins
    tcMar = OxmlElement('w:tcMar')
    for edge in ['top','left','bottom','right']:
        m = OxmlElement(f'w:{edge}')
        m.set(qn('w:w'), '80')
        m.set(qn('w:type'), 'dxa')
        tcMar.append(m)
    tcPr.append(tcMar)
    tc.append(tcPr)
    # Title paragraph
    p_title = OxmlElement('w:p')
    pPr = OxmlElement('w:pPr')
    jc = OxmlElement('w:jc')
    jc.set(qn('w:val'), 'left')
    pPr.append(jc)
    p_title.append(pPr)
    r = OxmlElement('w:r')
    rPr = OxmlElement('w:rPr')
    rFonts = OxmlElement('w:rFonts')
    rFonts.set(qn('w:ascii'), 'Times New Roman')
    rFonts.set(qn('w:eastAsia'), '黑体')
    rPr.append(rFonts)
    sz = OxmlElement('w:sz')
    sz.set(qn('w:val'), '19')
    rPr.append(sz)
    b = OxmlElement('w:b')
    rPr.append(b)
    color = OxmlElement('w:color')
    color.set(qn('w:val'), '1A3A5C')
    rPr.append(color)
    r.append(rPr)
    t = OxmlElement('w:t')
    t.set(qn('xml:space'), 'preserve')
    t.text = f"🌱 零基础再讲 · {title}"
    r.append(t)
    p_title.append(r)
    tc.append(p_title)
    # Content paragraph
    p_content = OxmlElement('w:p')
    pPr2 = OxmlElement('w:pPr')
    jc2 = OxmlElement('w:jc')
    jc2.set(qn('w:val'), 'left')
    pPr2.append(jc2)
    spacing = OxmlElement('w:spacing')
    spacing.set(qn('w:after'), '60')
    pPr2.append(spacing)
    p_content.append(pPr2)
    # Split content by newline, each line as separate run with break
    lines = content.split("\n")
    for li, line in enumerate(lines):
        r2 = OxmlElement('w:r')
        rPr2 = OxmlElement('w:rPr')
        rFonts2 = OxmlElement('w:rFonts')
        rFonts2.set(qn('w:ascii'), 'Times New Roman')
        rFonts2.set(qn('w:eastAsia'), '宋体')
        rPr2.append(rFonts2)
        sz2 = OxmlElement('w:sz')
        sz2.set(qn('w:val'), '17')  # 8.5pt
        rPr2.append(sz2)
        color2 = OxmlElement('w:color')
        color2.set(qn('w:val'), '333333')
        rPr2.append(color2)
        r2.append(rPr2)
        t2 = OxmlElement('w:t')
        t2.set(qn('xml:space'), 'preserve')
        t2.text = line
        r2.append(t2)
        p_content.append(r2)
        if li != len(lines)-1:
            br = OxmlElement('w:br')
            p_content.append(br)
    tc.append(p_content)
    tr.append(tc)
    tbl.append(tr)
    # Insert after insert_anchor
    insert_anchor._element.addnext(tbl)
    print(f"Inserted zero box for {q_keyword}")
    # If fig, need to insert figure after table
    if fig_path and pathlib.Path(fig_path).exists():
        # Create paragraph for image
        # We need to add picture via doc.add_picture at end and move
        # Create temporary paragraph at end
        tmp_p = doc.add_paragraph()
        tmp_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = tmp_p.add_run()
        run.add_picture(str(fig_path), width=Inches(5.3))
        # Move its element after tbl
        img_elem = tmp_p._element
        # Remove from body and reinsert after tbl
        body = doc.element.body
        body.remove(img_elem)
        tbl.addnext(img_elem)
        # Add caption after image
        if fig_caption:
            cap_p = create_para_element(fig_caption, bold=False, size=Pt(7.5), color=(0x8A,0x94,0xA6), align=WD_ALIGN_PARAGRAPH.CENTER, italic=True)
            img_elem.addnext(cap_p)
        print(f"  + fig {fig_path}")

# Now insert zero boxes for key Qs
# Q2 is the critical one the user stuck on
insert_zero_box_after_q(doc, "Q2  沿 x 负向", "Q2 为什么同号向左？",
    "1. 先忘掉公式，看人浪：你在操场第0排先站起来，第5排的人要等波跑过去才站。\n"
    "2. 设你在 x=0 处看到 y=Acos(ωt)，那么在 x 处的点看到的是你 x/u 秒以前的样子：y=Acos[ω(t - x/u)]。\n"
    "3. 如果波往左跑：x 处的振动是右边一点的重复（右边的点先振动）→ 时间项变成“提前 x/u” → y=Acos[ω(t + x/u)]。\n"
    "4. 检验：让波峰不动，令相位=0 → ωt ± kx =0 → x = ∓(ω/k)t。+t -kx 解出来 x往右，+t +kx 解出来 x往左。\n"
    "5. 回代选项：A、B 都是 +t -x（异号向右），C 是两个 cos 相乘（节点不动，不是行波），D 两项都是 +t +x（同号向左）→ 选D。",
    fig_path=Q2_FIG, fig_caption="图 Q2-零基础：上排 +x 波峰随时间右移，下排 -x 波峰左移；同号左、异号右，一看就懂")

insert_zero_box_after_q(doc, "Q3  y=0.20", "Q3 为什么代 t=0.5 就出来波形？",
    "1. 波形图是“照相”：固定 t，看不同 x 的 y。\n"
    "2. 把 t=0.5 直接代进 y=0.20cos[2π(t - x/2)+π]，得到 y=0.20cos(πx)。\n"
    "3. 找两个点验：x=0 → y=+0.20 峰；x=1 → y=-0.20 谷。四个选项里只有 A 在 x=0 是峰、x=1 是谷。\n"
    "4. 千万别把横轴看成时间，波形图横轴一定是 x。")

insert_zero_box_after_q(doc, "Q4  λ=4", "Q4 怎么从振动图读出初相？",
    "1. 看图读：t=0 时 y=-√2/2 且箭头往下（速度负）。\n"
    "2. 用 y=Acosφ → cosφ=-1/2 → φ=±2π/3。\n"
    "3. 再用速度 v=-Aωsinφ <0 → sinφ>0 → φ只能是 +2π/3（第二象限）。\n"
    "4. 得 x=0 的振动 y0=√2cos(πt/2+2π/3)，再把 t 换成 t - x/u（u=1）就是波动方程。")

insert_zero_box_after_q(doc, "Q6  球面", "Q6 为什么 I∝1/r² 而 A∝1/r？",
    "1. 能量守恒：球面面积 4πr² 乘强度 I = 总功率，不变。\n"
    "2. 所以 I = 功率/面积 ∝1/r²。\n"
    "3. 强度又 ∝A²，所以 A ∝1/r。问强度选1/r²，问振幅选1/r，别混。")

insert_zero_box_after_q(doc, "Q9  驻波", "Q9 为什么最大位移时能量在波节？",
    "1. 驻波是两列相反的波叠加：y=2Acos(kx)cos(ωt)。cos(kx) 是空间包络。\n"
    "2. t=0 时 cos(ωt)=1，所有点都在最大位移，速度全0 → 动能0，势能全在形变最大的波节附近。\n"
    "3. t=T/4 时 cos=0，所有点回到平衡，形变0 → 势能0，动能全在振得最快的波腹。\n"
    "4. 所以“位移最大能量在波节”选 D，C 把波腹波节反了。")

insert_zero_box_after_q(doc, "Q1  最大光程", "Q1 什么是相干长度？",
    "1. 灯不是激光，是很多原子乱发光，每段光只相干一小段（波列长度 Lc）。\n"
    "2. 两束光程差超过 Lc，相位就乱了，不相干。\n"
    "3. 所以最大光程差由“光源能发多长的波列”决定 → 相干长度，选A。")

insert_zero_box_after_q(doc, "Q4  双缝", "Q4 为什么缝变窄条纹不动？",
    "1. 条纹位置由缝间距 d 决定：d·sinθ=kλ。缝中心没动，d 没动，条纹就不动。\n"
    "2. 缝宽 a 管的是“包络亮度”：a变窄，单缝中央变宽，极小处振幅不等，强度不再为0。")

insert_zero_box_after_q(doc, "Q1  夫琅", "Q1 为什么透镜上移条纹跟着走？",
    "1. 单缝中央始终在透镜主光轴和屏的交点。透镜上移→主光轴上移→中央跟着上移。\n"
    "2. 缝变窄→中央宽度 2fλ/b 变宽。两件事独立，一宽一移，选A。")

insert_zero_box_after_q(doc, "两正交偏振片", "Q1 & Q4 偏振片怎么判有无消光？",
    "1. 线偏振过偏振片，转到90°必消光。\n"
    "2. 没消光→一定不是线偏振，可能是部分偏振、椭圆、圆。\n"
    "3. 两正交偏振片间转180°：从90°→0°亮→90°暗，亮度先增后减到0。")

# Save
doc.save(str(DOCX))
print(f"Saved zero-rewritten {DOCX} {DOCX.stat().st_size/1024:.0f}KB")
# Count images
from docx.opc.constants import RELATIONSHIP_TYPE as RT
cnt = sum(1 for rel in doc.part.rels.values() if rel.reltype==RT.IMAGE)
print(f"Images: {cnt}, paragraphs: {len(doc.paragraphs)}, tables: {len(doc.tables)}")
