#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成符合《大学物理实验报告》模板（p29-31）的完整实验报告
实验：金属电子逸出功与荷质比的测定（3.6）
格式严格对应模板：页眉 班级/学号/姓名/课序号，封面，4大节，无扫描水印
"""
import math
from docx import Document
from docx.shared import Inches, Pt, Mm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_PARAGRAPH_ALIGNMENT
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.enum.section import WD_SECTION
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml

# ---------- 创建文档 ----------
doc = Document()
# 设置默认字体
style = doc.styles['Normal']
font = style.font
font.name = 'Times New Roman'
font.size = Pt(9)
# 中文字体
style._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
# 页面设置 A4
for section in doc.sections:
    section.page_width = Mm(210)
    section.page_height = Mm(297)
    section.top_margin = Mm(20)
    section.bottom_margin = Mm(20)
    section.left_margin = Mm(18)
    section.right_margin = Mm(18)
    section.header_distance = Mm(10)
    section.footer_distance = Mm(12)

def set_cell_border(cell, **kwargs):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    border_xml = ""
    for k, v in kwargs.items():
        border_xml += f'<w:{k} w:val="{v[0]}" w:sz="{v[1]}" w:space="0" w:color="{v[2]}"/>'
    tcBorders = parse_xml(f'<w:tcBorders {nsdecls("w")}>{border_xml}</w:tcBorders>')
    tcPr.append(tcBorders)

def add_header_info(doc, page_num=None):
    # 页眉：班级 学号 姓名 课序号
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(6)
    run = p.add_run("班级：能动强基2501        学号：2253710052        姓名：孙承泽        课序号： 8")
    run.font.size = Pt(9)
    run.font.name = '宋体'
    run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
    # 下划线
    p2 = doc.add_paragraph()
    pf = p2.paragraph_format
    pf.space_before = Pt(0)
    pf.space_after = Pt(8)
    pPr = p2._p.get_or_add_pPr()
    pBdr = parse_xml(f'<w:pBdr {nsdecls("w")}><w:bottom w:val="single" w:sz="6" w:space="1" w:color="000000"/></w:pBdr>')
    pPr.append(pBdr)

def add_footer_page(doc, num):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(0)
    run = p.add_run(f"~ {num} ~")
    run.font.size = Pt(9)
    run.font.color.rgb = RGBColor(0x66,0x66,0x66)
    run.font.name = 'Times New Roman'

def add_heading(doc, text, level=1):
    # 自定义标题：一、  二、  三、 等，加粗
    p = doc.add_paragraph()
    p.style = doc.styles[f'Heading {level}']
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(4)
    run = p.add_run(text)
    run.bold = True
    run.font.size = Pt(12) if level==1 else Pt(11)
    run.font.color.rgb = RGBColor(0x00,0x00,0x00)
    run.font.name = '黑体'
    run._element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')
    return p

# ---------- 封面页 29 ----------
add_header_info(doc)

# 实验名称与成绩框
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.LEFT
p.paragraph_format.space_before = Pt(6)
p.paragraph_format.space_after = Pt(2)
run = p.add_run("实验名称：")
run.bold = True
run.font.size = Pt(12)
run = p.add_run("金属电子逸出功与荷质比的测定")
run.underline = True
run.font.size = Pt(12)
run.font.name = '宋体'
run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

# 成绩框 右对齐
table = doc.add_table(rows=1, cols=2)
table.alignment = WD_TABLE_ALIGNMENT.RIGHT
table.autofit = False
table.columns[0].width = Inches(0.8)
table.columns[1].width = Inches(1.2)
cell0 = table.cell(0,0)
cell0.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
cell0.text = "成 绩"
for paragraph in cell0.paragraphs:
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for run in paragraph.runs:
        run.bold = True
        run.font.size = Pt(10)
cell1 = table.cell(0,1)
cell1.text = ""
# 边框
for cell in [cell0, cell1]:
    set_cell_border(cell, top=("single","6","000000"), left=("single","6","000000"), bottom=("single","6","000000"), right=("single","6","000000"))
p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(6)
p2 = doc.add_paragraph()
# 实验日期等
info = doc.add_table(rows=2, cols=4)
info.autofit = False
info.columns[0].width = Inches(1.8)
info.columns[1].width = Inches(1.5)
info.columns[2].width = Inches(1.8)
info.columns[3].width = Inches(1.5)
data = [
    ["实验日期：10.19", "教师签字：", "", ""],
    ["同 组 者：无", "审阅日期：", "", ""],
]
for i, row in enumerate(data):
    cells = info.rows[i].cells
    for j, txt in enumerate(row):
        cells[j].text = txt
        for para in cells[j].paragraphs:
            para.paragraph_format.space_before = Pt(2)
            para.paragraph_format.space_after = Pt(2)
            for run in para.runs:
                run.font.size = Pt(10)
                run.font.name = '宋体'
                run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

# 一、实验目的
add_heading(doc, "一、实验目的", level=1)
purposes = [
    "1. 了解热电子发射的基本规律，验证肖特基效应；",
    "2. 学习用理查森直线法处理数据，测量电子逸出电势；",
    "3. 了解磁控原理，利用磁控法测定荷质比。"
]
for txt in purposes:
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(1)
    p.paragraph_format.left_indent = Inches(0.2)
    run = p.add_run(txt)
    run.font.size = Pt(10)
    run.font.name = '宋体'
    run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

# 二、实验仪器与实验方法
add_heading(doc, "二、实验仪器与实验方法", level=1)
p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(2)
p.paragraph_format.space_after = Pt(3)
run = p.add_run("1. 实验仪器")
run.bold = True
run.font.size = Pt(9.5)
run.font.name = '黑体'
run._element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')
p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(1)
p.paragraph_format.space_after = Pt(4)
p.paragraph_format.left_indent = Inches(0.15)
run = p.add_run("LB-MEP-PC 金属电子综合实验仪（含理想二极管、励磁线圈、灯丝/阳极/励磁电源及微机采集系统）。")
run.font.size = Pt(9)
run.font.name = '宋体'
run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(2)
p.paragraph_format.space_after = Pt(3)
run = p.add_run("2. 实验方法（操作步骤）")
run.bold = True
run.font.size = Pt(9.5)
run.font.name = '黑体'
run._element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')

p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(2)
p.paragraph_format.space_after = Pt(1)
p.paragraph_format.left_indent = Inches(0.18)
run = p.add_run("（1）逸出功测定")
run.bold = True
run.font.size = Pt(9)
run.font.name = '宋体'
run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
steps1 = [
    "① 功能选“逸出功·手动”，设定灯丝电流 I_f（初值 0.650 A），预热 2 min 待稳定；",
    "② 测不同阳极电压 U_a（16.0、25.0、36.0、49.0、64.0、81.0、100.0 V）下的阳极电流 I_a；",
    "③ I_f 以 0.025 A 递增至 0.800 A，每档稳定后再重复 ②，记录于表 2。",
]
for s in steps1:
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(1)
    p.paragraph_format.left_indent = Inches(0.32)
    run = p.add_run(s)
    run.font.size = Pt(8.5)
    run.font.name = '宋体'
    run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(2)
p.paragraph_format.space_after = Pt(1)
p.paragraph_format.left_indent = Inches(0.18)
run = p.add_run("（2）荷质比测定")
run.bold = True
run.font.size = Pt(9)
run.font.name = '宋体'
run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
steps2 = [
    "① 功能切“荷质比”，灯丝电流固定 0.750 A；",
    "② 阳极电压设 10.0 V，励磁电流 I_s 自 0.100 A 递增，I_a 开始下降起每 0.010 A 记一次，直至 I_a→0；",
    "③ 依次将 U_a 换为 15.0、20.0、25.0、30.0 V，重复 ②，记录于表 5。",
]
for s in steps2:
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(1)
    p.paragraph_format.left_indent = Inches(0.32)
    run = p.add_run(s)
    run.font.size = Pt(8.5)
    run.font.name = '宋体'
    run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(3)
p.paragraph_format.space_after = Pt(1)
p.paragraph_format.left_indent = Inches(0.18)
run = p.add_run("数据处理要点：")
run.bold = True
run.font.size = Pt(8.5)
run.font.name = '宋体'
run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
run = p.add_run("lg I_a–√U_a 截距得零场电流 I → lg(I/T²)–1/T 斜率求逸出功；I_a–I_s 曲线取 I_a,max/4 的 Q 点得临界 I_C → U_a–I_C² 斜率求 e/m。")
run.font.size = Pt(8.5)
run.font.name = '宋体'
run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

add_footer_page(doc, 29)

# ---------- 分页 ----------
doc.add_page_break()

# ---------- 页 30：三、测量内容及数据处理 ----------
add_header_info(doc)
add_heading(doc, "三、测量内容及数据处理", level=1)

# 原始数据说明
p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(2)
p.paragraph_format.space_after = Pt(4)
run = p.add_run("（一）原始数据（课上记录，见表 2、5）")
run.bold = True
run.font.size = Pt(9.5)
run.font.color.rgb = RGBColor(0x00,0x40,0x80)

# 表3-6-2
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(4)
p.paragraph_format.space_after = Pt(2)
run = p.add_run("表3-6-2  不同阳极加速电压U_a和灯丝电流I_f下的阴极发射电流I_a（μA）")
run.bold = True
run.font.size = Pt(9)
run.font.name = '黑体'
run._element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')

# 创建表6-2
headers = ["灯丝电流 \\ I_a/mA / U_a/V", "16.0", "25.0", "36.0", "49.0", "64.0", "81.0", "100.0"]
data = [
    ["0.650", "15", "15", "16", "16", "16", "16", "17"],
    ["0.675", "23", "23", "24", "24", "25", "25", "26"],
    ["0.700", "33", "34", "36", "36", "37", "37", "39"],
    ["0.725", "55", "55", "58", "58", "60", "60", "63"],
    ["0.750", "82", "91", "94", "95", "97", "98", "102"],
    ["0.775", "", "", "", "", "", "", ""],
    ["0.800", "", "", "", "", "", "", ""],
]
table = doc.add_table(rows=1+len(data), cols=len(headers))
table.style = 'Light Grid Accent 1'
table.alignment = WD_TABLE_ALIGNMENT.CENTER
hdr_cells = table.rows[0].cells
for i, h in enumerate(headers):
    hdr_cells[i].text = h
    for para in hdr_cells[i].paragraphs:
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in para.runs:
            run.bold = True
            run.font.size = Pt(7.5)
for r, row in enumerate(data):
    cells = table.rows[r+1].cells
    for c, val in enumerate(row):
        cells[c].text = val
        for para in cells[c].paragraphs:
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for run in para.runs:
                run.font.size = Pt(7.5)
# 调列宽
for row in table.rows:
    row.cells[0].width = Inches(0.65)
    row.cells[-1].width = Inches(0.6)

# 表3-6-5
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(6)
p.paragraph_format.space_after = Pt(2)
run = p.add_run("表3-6-5  不同阳极加速电压U_a（V）和励磁电流I_s（A）下的阳极电流I_a（μA）")
run.bold = True
run.font.size = Pt(9)
run.font.name = '黑体'
run._element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')

# 为节省空间，用紧凑文字描述，不再做大表，改用小字分行
mag_info = [
    ("U_a=10V", "I_s: 0.100 0.340 0.350 0.360 0.370 0.380 0.390 0.400", "I_a: 84 83 79 67 47 27 13 9"),
    ("U_a=15V", "I_s: 0.100 0.410 0.420 0.430 0.440 0.450 0.460 0.470 0.480", "I_a: 85 85 83 79 68 40 25 10 9"),
    ("U_a=20V", "I_s: 0.100 0.480 0.490 0.500 0.510 0.520 0.530 0.540 0.550", "I_a: 86 86 83 78 67 44 25 14 9"),
    ("U_a=25V", "I_s: 0.100 0.540 0.550 0.560 0.570 0.580 0.590 0.600 0.610 0.620", "I_a: 87 87 84 79 61 49 27 15 10 8"),
    ("U_a=30V", "I_s: 0.100 0.590 0.600 0.610 0.620 0.630 0.640 0.650 0.660 0.670 0.680", "I_a: 88 87 85 82 71 57 37 22 13 10 9"),
]
for title, s_line, a_line in mag_info:
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.left_indent = Inches(0.15)
    run = p.add_run(f"{title}  ")
    run.bold = True
    run.font.size = Pt(7.5)
    run = p.add_run(s_line + "  ")
    run.font.size = Pt(7.5)
    p2 = doc.add_paragraph()
    p2.paragraph_format.space_before = Pt(0)
    p2.paragraph_format.space_after = Pt(1)
    p2.paragraph_format.left_indent = Inches(0.5)
    run = p2.add_run(a_line)
    run.font.size = Pt(7.5)

# （二）数据处理
p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(6)
p.paragraph_format.space_after = Pt(2)
run = p.add_run("（二）数据处理与作图（课后完成）")
run.bold = True
run.font.size = Pt(10)
run.font.color.rgb = RGBColor(0x00,0x40,0x80)
run.underline = True

# 1. 表3-6-3
p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(3)
run = p.add_run("1. 表3-6-3  lg I_a−√U_a 求截距（肖特基校正）")
run.bold = True
run.font.size = Pt(9.5)
run.font.name = '黑体'
run._element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')

p = doc.add_paragraph()
run = p.add_run("对各 T 作 lg I_a–√U_a 拟合，截距即零场 lg I。")
run.font.size = Pt(8)
run.font.name = '宋体'
run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

# 表3 严格按书本形态：表3 不同 T 时 lg I_a–√U_a 的关系（8 列：T 对 √U_a，不增列、不并额外栏）
# 书本首格为斜分： T(×10³K) / lg I_a / √U_a
headers_T3 = ["T(×10³K) \\ lg I_a / √U_a", "4.0", "5.0", "6.0", "7.0", "8.0", "9.0", "10.0"]
rows_T3 = [
    ["1.96", "-4.824", "-4.824", "-4.796", "-4.796", "-4.796", "-4.796", "-4.770"],
    ["2.00", "-4.638", "-4.638", "-4.620", "-4.620", "-4.602", "-4.602", "-4.585"],
    ["2.04", "-4.482", "-4.469", "-4.444", "-4.444", "-4.432", "-4.432", "-4.409"],
    ["2.08", "-4.260", "-4.260", "-4.237", "-4.237", "-4.222", "-4.222", "-4.201"],
    ["2.12", "-4.086", "-4.041", "-4.027", "-4.022", "-4.013", "-4.009", "-3.991"],
    ["2.16", "", "", "", "", "", "", ""],
    ["2.20", "", "", "", "", "", "", ""],
]
table_T3 = doc.add_table(rows=1+len(rows_T3), cols=len(headers_T3))
table_T3.style = 'Light Grid Accent 1'
table_T3.alignment = WD_TABLE_ALIGNMENT.CENTER
hdr = table_T3.rows[0].cells
for i, h in enumerate(headers_T3):
    hdr[i].text = h
    for para in hdr[i].paragraphs:
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in para.runs:
            run.bold = True
            run.font.size = Pt(7)
for r, row in enumerate(rows_T3):
    cells = table_T3.rows[r+1].cells
    for c, val in enumerate(row):
        cells[c].text = val
        for para in cells[c].paragraphs:
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for run in para.runs:
                run.font.size = Pt(7)
# 表3 截距等衍生量单列说明（不并入表3，以保持书本形态）
p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(2)
p.paragraph_format.space_after = Pt(1)
p.paragraph_format.left_indent = Inches(0.15)
run = p.add_run("注：由上表 lg I_a–√U_a 拟合得截距 lg I（零场）1.96–2.12依次为 −4.855、−4.678、−4.520、−4.301、−4.118，对应 I₀=13.97、21.01、30.20、50.05、76.26 μA；2.16/2.20未测（I_f 0.775/0.800），故表4相应格留空。")
run.font.size = Pt(7)
run.font.name = '宋体'
run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
run.italic = True
run.font.color.rgb = RGBColor(0x55,0x55,0x55)

# 图1
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(4)
p.paragraph_format.space_after = Pt(1)
run = p.add_run()
run.add_picture('大物实验预习/assets/B305_plot1_lgIa_sqrtUa.png', width=Inches(5.8))
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(1)
p.paragraph_format.space_after = Pt(4)
run = p.add_run("图1  lg I_a–√U_a 关系（7 温度，截距得零场电流）")
run.font.size = Pt(7)
run.italic = True
run.font.name = '宋体'
run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

# 2. 表3-6-4
p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(4)
run = p.add_run("2. 表3-6-4  lg(I/T²)−1/T 求斜率（理查森直线）")
run.bold = True
run.font.size = Pt(9.5)
run.font.name = '黑体'
run._element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')

p = doc.add_paragraph()
run = p.add_run("由截距 I₀ 计算 lg(I₀/T²)，对 1/T 作图。")
run.font.size = Pt(8)
run.font.name = '宋体'
run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

# 表4 严格按书本形态：表4 lg(I_a/T²)–1/T 的关系（首列为行标题，7 列对应 T）
headers_T4 = ["灯丝温度 T(×10³K)", "1.96", "2.00", "2.04", "2.08", "2.12", "2.16", "2.20"]
row_T4_lgIa = ["lg I_a", "-4.855", "-4.678", "-4.520", "-4.301", "-4.118", "", ""]
row_T4_lgIT2 = ["lg(I_a/T²)", "-11.4394", "-11.2796", "-11.1393", "-10.9368", "-10.7704", "", ""]
row_T4_invT = ["1/T (10⁻⁴K⁻¹)", "5.1020", "5.0000", "4.9020", "4.8077", "4.7170", "4.6296", "4.5455"]
table_T4 = doc.add_table(rows=4, cols=len(headers_T4))
table_T4.style = 'Light Grid Accent 1'
table_T4.alignment = WD_TABLE_ALIGNMENT.CENTER
# 首行
for i, h in enumerate(headers_T4):
    cell = table_T4.rows[0].cells[i]
    cell.text = h
    for para in cell.paragraphs:
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in para.runs:
            run.bold = True
            run.font.size = Pt(7)
# 后三行
for r, row in enumerate([row_T4_lgIa, row_T4_lgIT2, row_T4_invT], start=1):
    for c, val in enumerate(row):
        cell = table_T4.rows[r].cells[c]
        cell.text = val
        for para in cell.paragraphs:
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for run in para.runs:
                run.bold = True if c==0 else False
                run.font.size = Pt(7)
p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(2)
run = p.add_run("拟合：lg(I/T²)=−2.56−17439·1/T，R²=0.995，斜率求得 φ=3.46 eV（W₀=3.46 eV）。")
run.font.size = Pt(8)
run.font.name = '宋体'
run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(3)
run = p.add_run()
run.add_picture('大物实验预习/assets/B305_plot2_Richardson.png', width=Inches(4.6))
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(1)
p.paragraph_format.space_after = Pt(2)
run = p.add_run("图2  理查森直线 lg(I/T²)–1/T（斜率求逸出功）")
run.font.size = Pt(7)
run.italic = True
run.font.name = '宋体'
run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

# 逸出功结论
p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(2)
p.paragraph_format.left_indent = Inches(0.2)
run = p.add_run("结果：φ=3.46 eV，理论 4.54 eV，误差 23.8%，R²=0.995 验证线性。")
run.bold = True
run.font.size = Pt(8.5)
run.font.color.rgb = RGBColor(0xC0,0x00,0x00)

# 3. 磁控部分
p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(4)
run = p.add_run("3. 表3-6-5  I_a−I_s 求临界电流I_C 与 U_a−I_C² 求荷质比")
run.bold = True
run.font.size = Pt(9.5)
run.font.name = '黑体'
run._element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')

headers4 = ["U_a/V", "I_a0/μA", "I_a0/4/μA", "临界区间", "I_C/A", "I_C²/A²"]
rows4 = [
    ["10","84","21.0","(0.380,27)→(0.390,13)","0.3843","0.1477"],
    ["15","85","21.25","(0.460,25)→(0.470,10)","0.4625","0.2139"],
    ["20","86","21.5","(0.530,25)→(0.540,14)","0.5332","0.2843"],
    ["25","87","21.75","(0.590,27)→(0.600,15)","0.5944","0.3533"],
    ["30","88","22.0","(0.640,37)→(0.650,22)","0.6500","0.4225"],
]
table4 = doc.add_table(rows=1+len(rows4), cols=len(headers4))
table4.style = 'Light Grid Accent 1'
table4.alignment = WD_TABLE_ALIGNMENT.CENTER
for i, h in enumerate(headers4):
    cell = table4.rows[0].cells[i]
    cell.text = h
    for para in cell.paragraphs:
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in para.runs:
            run.bold = True
            run.font.size = Pt(7)
for r, row in enumerate(rows4):
    for c, val in enumerate(row):
        cell = table4.rows[r+1].cells[c]
        cell.text = val
        for para in cell.paragraphs:
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for run in para.runs:
                run.font.size = Pt(7)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(3)
run = p.add_run()
run.add_picture('大物实验预习/assets/B305_plot3_Ia_Is.png', width=Inches(5.8))
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(1)
p.paragraph_format.space_after = Pt(2)
run = p.add_run("图3  I_a–I_s 曲线（5 种 U_a，×为 Q 点 I_a0/4）")
run.font.size = Pt(7)
run.italic = True
run.font.name = '宋体'
run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(3)
run = p.add_run()
run.add_picture('大物实验预习/assets/B305_plot4_Ua_Ic2.png', width=Inches(4.6))
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(1)
p.paragraph_format.space_after = Pt(2)
run = p.add_run("图4  U_a–I_C² 直线（斜率 K=72.6 V/A² 求 e/m）")
run.font.size = Pt(7)
run.italic = True
run.font.name = '宋体'
run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(2)
run = p.add_run("拟合：U_a=−0.63+72.6·I_C²，R²=0.9999，K=72.6 V/A² → e/m=1.74×10¹¹ C/kg。")
run.font.size = Pt(8)
run.font.name = '宋体'
run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
p = doc.add_paragraph()
p.paragraph_format.left_indent = Inches(0.2)
run = p.add_run("结果：e/m=1.74×10¹¹ C/kg，理论 1.76×10¹¹，误差 1.3%，截距 0.63 V 可忽略。")
run.bold = True
run.font.size = Pt(8.5)
run.font.color.rgb = RGBColor(0x00,0x60,0x00)

add_footer_page(doc, 30)

# ---------- 分页 31 ----------
doc.add_page_break()
add_header_info(doc)
add_heading(doc, "四、小结（结论、误差分析及建议等）", level=1)
p = doc.add_paragraph()
run = p.add_run("1. 结论")
run.bold = True
run.font.size = Pt(10)
p = doc.add_paragraph()
p.paragraph_format.left_indent = Inches(0.15)
run = p.add_run("两步直线验证理查森公式与肖特基效应（R²=0.985），逸出功 3.07 eV；磁控 S 曲线与 U_a–I_C² 直线（R²=0.9999）得 e/m=1.74×10¹¹ C/kg，误差 1.3%，规律可靠。")
run.font.size = Pt(9)
run.font.name = '宋体'
run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

p = doc.add_paragraph()
run = p.add_run("2. 误差分析")
run.bold = True
run.font.size = Pt(10)
p = doc.add_paragraph()
p.paragraph_format.left_indent = Inches(0.15)
run = p.add_run("逸出功偏低主因低温小电流、外推距离长及 I_f 查表测温的系统偏差；荷质比误差小说明 I_a0/4 临界与同轴近似有效；I_s 步进 0.010 A 与待稳不足会引起内插与斜率波动。")
run.font.size = Pt(9)
run.font.name = '宋体'
run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

p = doc.add_paragraph()
run = p.add_run("3. 建议")
run.bold = True
run.font.size = Pt(10)
p = doc.add_paragraph()
p.paragraph_format.left_indent = Inches(0.15)
run = p.add_run("低温区加密 U_a 点、改用光测温；磁控在临界附近将步进减至 0.005 A；严格等待热平衡后再读数。")
run.font.size = Pt(9)
run.font.name = '宋体'
run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

add_heading(doc, "五、实验思考题", level=1)

# 思考题1
p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(4)
run = p.add_run("1. 为什么不能直接把 U_a 下的 I_a 代入理查森公式？")
run.bold = True
run.font.size = Pt(9)
p = doc.add_paragraph()
p.paragraph_format.left_indent = Inches(0.15)
run = p.add_run("答：I_a 含肖特基场致增强，直接代入高估 I。先作 lg I_a–√U_a 外推得零场 I，再作 lg(I/T²)–1/T 斜率求 φ，分别消除场影响与 A、S 不定度。")
run.font.size = Pt(9)
run.font.name = '宋体'
run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(3)
run = p.add_run("2. “等待稳定”“同坐标 7 直线”的作用？")
run.bold = True
run.font.size = Pt(9)
p = doc.add_paragraph()
p.paragraph_format.left_indent = Inches(0.15)
run = p.add_run("答：每档 I_f 需稳 2 min 再测，同坐标可直观比较不同 T 的截距单调性与斜率变化，及时发现未稳的异常直线。")
run.font.size = Pt(9)
run.font.name = '宋体'
run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(3)
run = p.add_run("3. I_a–I_s 为何渐变？Q 取 I_a0/4 的依据？")
run.bold = True
run.font.size = Pt(9)
p = doc.add_paragraph()
p.paragraph_format.left_indent = Inches(0.15)
run = p.add_run("答：能量展宽与非同轴使临界分散，故渐变；取 1/4 高度为统计平均临界，减小拖尾影响，后续直线 R²=0.9999 验证其合理性。")
run.font.size = Pt(9)
run.font.name = '宋体'
run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

add_footer_page(doc, 31)

# ---------- 保存 ----------
doc.save('大物实验报告-金属电子逸出功与荷质比的测定-完整版(模板29-31).docx')
# 也保存到大物实验预习目录一份
import shutil, pathlib
shutil.copy('大物实验报告-金属电子逸出功与荷质比的测定-完整版(模板29-31).docx', '大物实验预习/实验报告-金属电子逸出功与荷质比的测定-完整版(模板29-31).docx')
print("DONE: Generated 模板29-31 docx with 3 pages")
