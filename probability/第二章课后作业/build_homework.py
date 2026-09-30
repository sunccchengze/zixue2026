"""从两份经人工校对的 Markdown 原稿重建 A4 题卷及参考答案 PDF。
运行：python build_homework.py  （依赖 reportlab；PDF 渲染核对可用 pymupdf）
只处理已核实的施雨等教材《习题2》，不冒称 A/B 两部分。
"""
from pathlib import Path
import html
import re
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether

ROOT = Path(__file__).resolve().parent
pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
FONT = 'STSong-Light'
base = ParagraphStyle('base', fontName=FONT, fontSize=10, leading=16, spaceAfter=4)
heading = ParagraphStyle('heading', parent=base, fontSize=13, leading=20, spaceBefore=12, spaceAfter=5, keepWithNext=True)
title = ParagraphStyle('title', parent=base, fontSize=17, leading=25, alignment=TA_CENTER, spaceAfter=8)
small = ParagraphStyle('small', parent=base, fontSize=8.5, leading=13, spaceAfter=5)
notice = ParagraphStyle('notice', parent=base, fontSize=9, leading=14, textColor=colors.HexColor('#444444'))

def para(text, style=base):
    text = html.escape(text).replace('**', '')
    # ReportLab CID font lacks a few mathematical glyphs; use textual equivalents
    text = text.replace('Φ⁻¹', 'Phi逆').replace('Φ', 'Phi').replace('Σ', '求和').replace('∈', '属于')
    text = text.replace('⌊λ⌋', 'floor(lambda)').replace('～', '~')
    # STSong-Light 的 PDF 字体缺 U+2212、Unicode 上下标；静默丢字会颠倒数学结论。
    text = text.replace('−', '-').replace('²', '^2').replace('³', '^3').replace('·', '*')
    for digit, ascii_digit in zip('₀₁₂₃₄₅₆₇₈₉', '0123456789'):
        text = text.replace(digit, '_' + ascii_digit)
    return Paragraph(text, style)

def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont(FONT, 8)
    canvas.drawCentredString(A4[0]/2, 9*mm, f'第 {doc.page} 页 | 第二章习题：A/B 范围待核')
    canvas.restoreState()

def doc_build(filename, flow):
    SimpleDocTemplate(str(ROOT / filename), pagesize=A4, leftMargin=18*mm,
                      rightMargin=18*mm, topMargin=17*mm, bottomMargin=17*mm,
                      title=filename, author='孙承泽').build(flow, onFirstPage=footer, onLaterPages=footer)

def split_sections(text):
    found = re.findall(r'^### (\d+)([^\n]*)\n(.*?)(?=^### \d+|^## |\Z)', text, re.M | re.S)
    return [(int(n), (extra.strip()+'\n'+content).strip()) for n, extra, content in found]

# 试卷：页数未被指定，以答题空间为优先，不沿用第一章四页的题量约束。
qtext = (ROOT/'作业02-第二章习题偶数题-已核实部分.md').read_text()
questions = split_sections(qtext)
assert [n for n, _ in questions] == list(range(2, 31, 2))
flow = [para('第二章课后作业｜偶数题（已核实部分）', title),
        para('孙承泽　2253710052　能动强基2501　｜　截止 2026-10-13', small),
        para('来源：施雨等《概率论与数理统计》习题2，印刷页47—50。原书未标 A/B；若教师指定不同教材，须补原题后更换，不可直接交此卷。', notice), Spacer(1, 4*mm)]
for n, content in questions:
    content = re.sub(r'\|[^\n]*\|\n\|[-:| ]+\|\n\|[^\n]*\|',
                     'X：−2，−1，0，1，2，3；相应 P：1/15，1/10，1/6，1/3，3/10，1/30。', content)
    body = ' '.join(line.strip() for line in content.splitlines() if line.strip())
    block = [para(f'第 {n} 题', heading), para(body), Spacer(1, 2*mm)]
    # 按书写难度留空间，遇长题允许移至下一页；不要求不切断所有答题线。
    lines = 12 if n in (20,24) else 8 if n in (8,10,12,14,16,22,26,28,30) else 6
    rows = [[''] for _ in range(lines)]
    t = Table(rows, colWidths=[170*mm], rowHeights=[6.0*mm]*lines)
    t.setStyle(TableStyle([('LINEBELOW', (0,0),(-1,-1), 0.25, colors.HexColor('#aaaaaa'))]))
    block.extend([t, Spacer(1, 5*mm)])
    flow.append(KeepTogether(block))
doc_build('第二章课后作业-已核实部分-答题卷.pdf', flow)

atext = (ROOT/'作业02-第二章习题偶数题-已核实部分-参考答案.md').read_text()
flow = [para('第二章课后作业｜已核实部分参考答案', title),
        para('孙承泽　2253710052　能动强基2501　｜　A/B 范围待核', small),
        para('仅对应施雨等教材习题2的15道偶数题；教师要求的A/B两部分尚无法与现有教材对应，不能据此视为完整作业。', notice)]
for raw in atext.splitlines()[4:]:
    line = raw.strip()
    if not line or line == '---':
        continue
    if line.startswith('# '):
        continue
    if line.startswith('## '):
        flow.append(para(line[3:], heading))
    elif line.startswith('|'):
        # Markdown 表格转换为一行一记录；不让 Markdown 原始竖线入正文
        cells = [c.strip() for c in line.strip('|').split('|')]
        if all(re.fullmatch(r'[-: ]+', c) for c in cells): continue
        flow.append(para('  ·  '.join(cells), small))
    else:
        flow.append(para(line, base))
doc_build('第二章课后作业-已核实部分-完整解析.pdf', flow)
print('已生成：', len(questions), '题，两份PDF；A/B缺口尚待教材确认。')
