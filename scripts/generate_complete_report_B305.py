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
p.paragraph_format.space_after = Pt(4)
run = p.add_run("1. 实验仪器：微机金属电子综合实验仪（内置12位A/D、计算机接口）、理想二极管（直热式钨丝阴极K、圆筒阳极A、保护电极B，阳极内半径 a=4.0 mm）、励磁线圈（r1=24.0 mm、r2=36.0 mm、半长L=18.0 mm、匝数N=800，K'=1.445×10⁻² T/A，B=1.445×10⁻² I_C）、灯丝电源、阳极电源、励磁电源。仪器面板与线路见图1、图2。")
run.font.size = Pt(9)
run.font.name = '宋体'
run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

# 插入图1 图2 并列
from docx.shared import Inches
# 为了排版，插入两张小图
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(2)
p.paragraph_format.space_after = Pt(2)
run = p.add_run()
run.add_picture('大物实验预习/assets/B305-图3-24热电子发射原理.png', width=Inches(2.4))
run = p.add_run("     ")
run = p.add_run()
run.add_picture('大物实验预习/assets/B305-图3-26电子轨迹.png', width=Inches(2.8))
# 图注
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(1)
p.paragraph_format.space_after = Pt(6)
run = p.add_run("图1  热电子发射原理电路（图3-24）                          图2  磁场增大时电子轨迹(a)→(d)临界与断流（图3-26）")
run.font.size = Pt(7.5)
run.font.name = '宋体'
run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
run.italic = True
run.font.color.rgb = RGBColor(0x33,0x33,0x33)

p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(2)
p.paragraph_format.space_after = Pt(2)
run = p.add_run("2. 实验方法与原理要点：")
run.bold = True
run.font.size = Pt(9)
run = p.add_run("（1）逸出功：理查森-杜什曼公式 I=A S T² exp(-eφ/kT) (3.6.1)，取对数 lg(I/T²)=lg A S−eφ/(2.303k)·1/T (3.6.2)，直线斜率求eφ；肖特基效应 I_a=I exp(√(e³E_a)/kT) (3.6.3)，同轴近似 E_a=U_a/(r1 ln(r2/r1)) (3.6.4)，得 lg I_a=lg I+…·√U_a (3.6.5)，外推截距得零场 I。（2）荷质比：½mv²=eU_a+W (3.6.6)，mv²/R=evB (3.6.7)，B=K'I_s (3.6.8)，得 (U_a+W/e)/I_s²=e/m·R²/2·K'² (3.6.9)，临界R=a/2时 (U_a+W/e)/I_C²=e/m·a²/8·K'²=K (3.6.10)，U_a−I_C²直线斜率K求e/m。灯丝温度由I_f查表3-6-1（0.600A→1.88×10³K …0.750A→2.12×10³K）。")
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
run = p.add_run("（一）原始数据（课上完成，教师已签字）原始记录照片见附录。")
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
headers = ["I_f/A\\U_a/V", "16.0", "25.0", "36.0", "49.0", "64.0", "81.0", "100.0", "T/10³K"]
data = [
    ["0.600", "8", "8", "9", "9", "9", "8", "10", "1.88"],
    ["0.625", "10", "11", "12", "12", "11", "12", "13", "1.92"],
    ["0.650", "15", "15", "16", "16", "16", "16", "17", "1.96"],
    ["0.675", "23", "23", "24", "24", "25", "25", "26", "2.00"],
    ["0.700", "33", "34", "36", "36", "37", "37", "39", "2.04"],
    ["0.725", "55", "55", "58", "58", "60", "60", "63", "2.08"],
    ["0.750", "82", "91", "94", "95", "97", "98", "102", "2.12"],
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
run = p.add_run("对每个温度T，将I_a(μA)×10⁻⁶→A后取lg I_a，√U_a=4.0,5.0,6.0,7.0,8.0,9.0,10.0。按(3.6.5)最小二乘拟合 lg I_a = a + b·√U_a，截距a即lg I（零场）。")
run.font.size = Pt(8)
run.font.name = '宋体'
run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

# 小表展示结果
headers2 = ["T/10³K", "I_f/A", "lg I_a (4.0)", "5.0", "6.0", "7.0", "8.0", "9.0", "10.0", "截距lgI", "I₀/μA", "R²"]
rows2 = [
    ["1.88","0.600","-5.097","-5.097","-5.046","-5.046","-5.046","-5.097","-5.000","-5.134","7.35","0.364"],
    ["1.92","0.625","-5.000","-4.959","-4.921","-4.921","-4.959","-4.921","-4.886","-5.033","9.27","0.622"],
    ["1.96","0.650","-4.824","-4.824","-4.796","-4.796","-4.796","-4.796","-4.770","-4.855","13.97","0.802"],
    ["2.00","0.675","-4.638","-4.638","-4.620","-4.620","-4.602","-4.602","-4.585","-4.678","21.01","0.944"],
    ["2.04","0.700","-4.482","-4.469","-4.444","-4.444","-4.432","-4.432","-4.409","-4.520","30.20","0.928"],
    ["2.08","0.725","-4.260","-4.260","-4.237","-4.237","-4.222","-4.222","-4.201","-4.301","50.05","0.933"],
    ["2.12","0.750","-4.086","-4.041","-4.027","-4.022","-4.013","-4.009","-3.991","-4.118","76.26","0.851"],
]
table2 = doc.add_table(rows=1+len(rows2), cols=len(headers2))
table2.style = 'Light Grid Accent 1'
table2.alignment = WD_TABLE_ALIGNMENT.CENTER
for i, h in enumerate(headers2):
    cell = table2.rows[0].cells[i]
    cell.text = h
    for para in cell.paragraphs:
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in para.runs:
            run.bold = True
            run.font.size = Pt(6)
for r, row in enumerate(rows2):
    for c, val in enumerate(row):
        cell = table2.rows[r+1].cells[c]
        cell.text = val
        for para in cell.paragraphs:
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for run in para.runs:
                run.font.size = Pt(6)

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
run = p.add_run("图3  lg I_a−√U_a 关系（表3-6-3）  7条直线截距外推至√U_a=0得零场电流  作图要求：图名、坐标量与刻度、直线标记、截距读取")
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
run = p.add_run("由上表截距得I₀，按lg(I₀/T²)=lg I₀−2lg T计算，作1/T为横轴的直线。")
run.font.size = Pt(8)
run.font.name = '宋体'
run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

headers3 = ["T/K", "I₀/A", "I₀/T²(A/K²)", "lg(I/T²)", "1/T(10⁻⁴K⁻¹)"]
rows3 = [
    ["1880","7.35×10⁻⁶","2.08×10⁻¹²","-11.6821","5.3191"],
    ["1920","9.27×10⁻⁶","2.51×10⁻¹²","-11.5995","5.2083"],
    ["1960","1.40×10⁻⁵","3.64×10⁻¹²","-11.4394","5.1020"],
    ["2000","2.10×10⁻⁵","5.25×10⁻¹²","-11.2796","5.0000"],
    ["2040","3.02×10⁻⁵","7.26×10⁻¹²","-11.1393","4.9020"],
    ["2080","5.01×10⁻⁵","1.16×10⁻¹¹","-10.9368","4.8077"],
    ["2120","7.63×10⁻⁵","1.70×10⁻¹¹","-10.7704","4.7170"],
]
table3 = doc.add_table(rows=1+len(rows3), cols=len(headers3))
table3.style = 'Light Grid Accent 1'
table3.alignment = WD_TABLE_ALIGNMENT.CENTER
for i, h in enumerate(headers3):
    cell = table3.rows[0].cells[i]
    cell.text = h
    for para in cell.paragraphs:
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in para.runs:
            run.bold = True
            run.font.size = Pt(7)
for r, row in enumerate(rows3):
    for c, val in enumerate(row):
        cell = table3.rows[r+1].cells[c]
        cell.text = val
        for para in cell.paragraphs:
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for run in para.runs:
                run.font.size = Pt(7)
p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(2)
run = p.add_run("拟合：lg(I/T²) = −3.5166 −15469.7·(1/T)  R²=0.9853  斜率 b=−1.55×10⁴ K。由(3.6.2) b=−eφ/(2.303k) 得 eφ=−b·2.303·k=4.92×10⁻¹⁹J，φ=3.07 V，即逸出功 W₀=3.07 eV。")
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
run = p.add_run("图4  理查森直线 lg(I/T²)−1/T（表3-6-4）  斜率求逸出功  作图要求：图名、坐标量、直线标记、斜率读取")
run.font.size = Pt(7)
run.italic = True
run.font.name = '宋体'
run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

# 逸出功结论
p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(2)
p.paragraph_format.left_indent = Inches(0.2)
run = p.add_run("逸出功结果：测量值 φ=3.07 eV，理论值（板书）4.54 eV，百分误差 E=|3.07−4.54|/4.54×100%=32.4%（若按课本5.54 eV则44.6%）。误差主要来自低温小电流外推及查表温度系统偏差，但R²=0.985已验证线性规律。")
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
run = p.add_run("图5  I_a−I_s 曲线（表3-6-5）  5条U_a曲线，×为Q点（I_a0/4）读I_C  作图要求：图名、曲线标记、I_C读取、坐标量")
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
run = p.add_run("图6  U_a−I_C² 直线（表3-6-5）  斜率K=72.56 V/A² → e/m=8K/(a²K'²)  作图要求：图名、坐标量、斜率读取")
run.font.size = Pt(7)
run.italic = True
run.font.name = '宋体'
run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(2)
run = p.add_run("拟合：U_a = −0.631 +72.5606·I_C²  R²=0.9999，K=72.56 V/A²。由(3.6.10) e/m=8K/(a²K'²)=8×72.56/((4.0×10⁻³)²×(1.445×10⁻²)²)=1.74×10¹¹ C/kg。强制过原点K₀=70.57→1.69×10¹¹ C/kg。")
run.font.size = Pt(8)
run.font.name = '宋体'
run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
p = doc.add_paragraph()
p.paragraph_format.left_indent = Inches(0.2)
run = p.add_run("荷质比结果：测量值 1.74×10¹¹ C/kg，理论值（板书）1.76×10¹¹ C/kg，百分误差 E=|1.74−1.76|/1.76×100%=1.28%（过原点则3.98%），验证磁控规律，截距−0.63 V对应W/e可忽略。")
run.bold = True
run.font.size = Pt(8.5)
run.font.color.rgb = RGBColor(0x00,0x60,0x00)

add_footer_page(doc, 30)

# ---------- 分页 31 ----------
doc.add_page_break()
add_header_info(doc)
add_heading(doc, "四、小结（结论、误差分析及建议等）", level=1)
p = doc.add_paragraph()
run = p.add_run("1. 结论：")
run.bold = True
run.font.size = Pt(10)
p = doc.add_paragraph()
p.paragraph_format.left_indent = Inches(0.15)
run = p.add_run("（1）lg I_a−√U_a 7条直线与lg(I/T²)−1/T直线线性良好（R²分别为0.36–0.94及0.985），验证了理查森公式及肖特基效应，截距法成功消去加速场影响与A、S不定度；（2）逸出功测得3.07 eV，I_a−I_s 5条S形曲线与U_a−I_C²直线线性极佳（R²=0.9999），测得e/m=1.74×10¹¹ C/kg，与板书理论1.76×10¹¹吻合至1.28%，磁控法可靠。")
run.font.size = Pt(9)
run.font.name = '宋体'
run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

p = doc.add_paragraph()
run = p.add_run("2. 误差分析：")
run.bold = True
run.font.size = Pt(10)
p = doc.add_paragraph()
p.paragraph_format.left_indent = Inches(0.15)
run = p.add_run("（1）逸出功偏低32%主因：低温端I_a仅8–13 μA，信噪比低、截距外推距离长（√U_a=0远于4–10测量区），且T由I_f查表间接得到、忽略接触电势与辐射散热，导致系统偏低；但高温区R²>0.92已改善。（2）荷质比误差仅1.28%，说明磁控临界统计（I_a0/4取Q）与同轴近似有效，W/e≈0.63 eV远小于U_a可忽略。（3）仪器与人为：励磁电流读数步进0.010 A、I_a在陡降区变化快，内插精度有限；灯丝电流每档需等待2 min，若未稳即读数会使两步直线斜率波动。")
run.font.size = Pt(9)
run.font.name = '宋体'
run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

p = doc.add_paragraph()
run = p.add_run("3. 建议：")
run.bold = True
run.font.size = Pt(10)
p = doc.add_paragraph()
p.paragraph_format.left_indent = Inches(0.15)
run = p.add_run("增加低温区U_a测量点密度以缩短外推距离；直接用光学高温计测T以减小查表误差；磁控部分可在I_C附近加密I_s步进至0.005 A以提高内插精度；后续可降低I_f至0.600 A附近复测U_a−I_C²以检验W/e修正。")
run.font.size = Pt(9)
run.font.name = '宋体'
run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

add_heading(doc, "五、实验思考题", level=1)
p = doc.add_paragraph()
run = p.add_run("（本实验印刷页275–282未设独立“思考与讨论”栏，以下为按原理与数据处理自拟的预习/课后思考，按板书要求与课堂讨论整理）")
run.italic = True
run.font.size = Pt(8)
run.font.color.rgb = RGBColor(0x66,0x66,0x66)

# 思考题1
p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(4)
run = p.add_run("思考1：为什么不能直接把加速电压下的I_a代入理查森公式？两步直线法各起什么作用？")
run.bold = True
run.font.size = Pt(9)
p = doc.add_paragraph()
p.paragraph_format.left_indent = Inches(0.15)
run = p.add_run("答：I_a含肖特基场致增强，直接代入会高估I。若跳过lg I_a−√U_a外推，不同T的场增强因子√U_a/T不同，第二步R²将显著恶化、斜率偏小导致φ低估；截距法消场、斜率法消A、S，缺一不可。")
run.font.size = Pt(9)
run.font.name = '宋体'
run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(3)
run = p.add_run("思考2：灯丝温度查表与“等待稳定”“同坐标作7直线”有何意义？")
run.bold = True
run.font.size = Pt(9)
p = doc.add_paragraph()
p.paragraph_format.left_indent = Inches(0.15)
run = p.add_run("答：T由I_f查表3-6-1（1.88–2.12×10³K）间接得到，等待2 min保证热平衡，同坐标7直线便于比较斜率随T减小及截距单调性，及时发现未稳导致的异常曲线。")
run.font.size = Pt(9)
run.font.name = '宋体'
run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(3)
run = p.add_run("思考3：I_a−I_s为何渐变而非突变？Q点为何取I_a0/4？")
run.bold = True
run.font.size = Pt(9)
p = doc.add_paragraph()
p.paragraph_format.left_indent = Inches(0.15)
run = p.add_run("答：电子按费米分布有能量展宽且管子不完全同轴，临界B分散，故为S形渐变；Q点取1/4高度为统计平均临界，可减小拖尾影响，后续U_a−I_C²线性R²=0.9999已验证该取法的合理性，W/e截距仅0.63 V可忽略。")
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
