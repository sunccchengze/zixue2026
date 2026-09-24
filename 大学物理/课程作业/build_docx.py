# -*- coding: utf-8 -*-
"""生成《大学物理 期中考试范围（第十二~十五次作业）详解》docx"""
import os
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

from content12 import S12
from content13 import S13
from content14 import S14
from content15 import S15

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '大学物理期中考试范围详解（第十二~十五次作业）.docx')

ACCENT = RGBColor(0x1F, 0x4E, 0x79)   # 深蓝
ANS_BG = 'FFF2CC'                      # 答案底纹（浅黄）
GRAY = RGBColor(0x59, 0x59, 0x59)

def set_font(run, name_cn='宋体', name_en='Times New Roman', size=11, bold=False, color=None):
    run.font.name = name_en
    run.font.size = Pt(size)
    run.font.bold = bold
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = OxmlElement('w:rFonts'); rPr.append(rFonts)
    rFonts.set(qn('w:eastAsia'), name_cn)
    if color is not None:
        run.font.color.rgb = color

def shade_para(p, fill):
    pPr = p._p.get_or_add_pPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear'); shd.set(qn('w:fill'), fill)
    pPr.append(shd)

def para(doc, text='', size=11, bold=False, cn='宋体', en='Times New Roman',
         align=None, before=2, after=4, color=None, indent=None, fill=None):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(before); pf.space_after = Pt(after)
    pf.line_spacing = 1.28
    if align is not None: p.alignment = align
    if indent is not None: pf.left_indent = Cm(indent)
    if text:
        r = p.add_run(text)
        set_font(r, cn, en, size, bold, color)
    if fill: shade_para(p, fill)
    return p

def mixed(doc, parts, size=11, before=2, after=4, align=None, indent=None, fill=None):
    """parts: list of (text, bold, color)"""
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(before); pf.space_after = Pt(after)
    pf.line_spacing = 1.28
    if align is not None: p.alignment = align
    if indent is not None: pf.left_indent = Cm(indent)
    for t, b, c in parts:
        r = p.add_run(t); set_font(r, '宋体', 'Times New Roman', size, b, c)
    if fill: shade_para(p, fill)
    return p

def heading(doc, text, level=1):
    if level == 1:
        p = para(doc, text, size=16, bold=True, cn='黑体', align=WD_ALIGN_PARAGRAPH.CENTER,
                 before=10, after=8, color=ACCENT)
        # 下边框
        pPr = p._p.get_or_add_pPr()
        pBdr = OxmlElement('w:pBdr')
        bottom = OxmlElement('w:bottom')
        bottom.set(qn('w:val'), 'single'); bottom.set(qn('w:sz'), '12')
        bottom.set(qn('w:space'), '2'); bottom.set(qn('w:color'), '1F4E79')
        pBdr.append(bottom); pPr.append(pBdr)
    elif level == 2:
        p = para(doc, text, size=13, bold=True, cn='黑体', before=10, after=6, color=ACCENT)
    else:
        p = para(doc, text, size=11.5, bold=True, cn='黑体', before=8, after=4)
    return p

def image(doc, fname, caption, width=12.6):
    path = os.path.join(HERE, '图卡', fname)
    if not os.path.exists(path):
        return
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(6); p.paragraph_format.space_after = Pt(2)
    run = p.add_run(); run.add_picture(path, width=Cm(width))
    c = para(doc, caption, size=9, align=WD_ALIGN_PARAGRAPH.CENTER, before=0, after=8, color=GRAY)

def question(doc, num, stem, answer, explain, calc=False):
    mixed(doc, [(num + '　', True, ACCENT), (stem, False, None)], size=11, before=8, after=3)
    mixed(doc, [('参考答案：', True, RGBColor(0x9C, 0x57, 0x00)), (answer, True, None)],
          size=11, after=3, indent=0.55, fill=ANS_BG)
    lines = explain.split('\n')
    for i, ln in enumerate(lines):
        if i == 0:
            mixed(doc, [('详解：', True, ACCENT), (ln, False, None)], size=10.5, after=3, indent=0.55)
        else:
            para(doc, ln, size=10.5, after=3, indent=0.55)

def build_session(doc, S, idx):
    doc.add_page_break()
    heading(doc, f'第{idx}部分　{S["title"]}', 1)
    para(doc, '考点范围：' + S['topic'], size=10.5, after=6, color=GRAY, align=WD_ALIGN_PARAGRAPH.CENTER)
    # 知识框架
    heading(doc, '〇、知识框架（先读这页，再看逐题解析）', 2)
    for title, points in S['framework']:
        heading(doc, title, 3)
        for pt in points:
            p = para(doc, '· ' + pt, size=10.5, after=2, indent=0.3)
    for fname, cap in S['imgs']:
        image(doc, fname, cap)
    # 逐题
    heading(doc, '一、选择题（逐题解析）', 2)
    for q in S['choice']:
        num, stem = q['stem'].split(' ', 1)
        question(doc, num, stem, q['answer'], q['explain'])
    heading(doc, '二、填空题（逐空解析）', 2)
    for q in S['blank']:
        num, stem = q['stem'].split(' ', 1)
        question(doc, num, stem, q['answer'], q['explain'])
    heading(doc, '三、计算题（完整推导 + 参考答案）', 2)
    for q in S['calc']:
        num, stem = q['stem'].split(' ', 1)
        question(doc, num, stem, q['answer'], q['explain'], calc=True)

def quick_table(doc, S):
    t = doc.add_table(rows=1, cols=4)
    t.style = 'Table Grid'
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for c, txt in zip(t.rows[0].cells, ['题号', '参考答案', '题号', '参考答案']):
        c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = c.paragraphs[0].add_run(txt); set_font(r, '黑体', 'Times New Roman', 10, True)
        shade_para(c.paragraphs[0], 'D9E2F3')
    allq = S['choice'] + S['blank'] + S['calc']
    for i in range(0, len(allq), 2):
        row = t.add_row().cells
        for j in range(2):
            if i + j < len(allq):
                q = allq[i + j]
                num = q['stem'].split(' ', 1)[0].rstrip('、').strip()
                ans = q['answer']
                if len(ans) > 34:
                    ans = ans[:33] + '…'
                for col, txt in ((0, num), (1, ans)):
                    cell = row[j*2 + col]
                    cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER if col == 0 else WD_ALIGN_PARAGRAPH.LEFT
                    r = cell.paragraphs[0].add_run(txt)
                    set_font(r, '宋体', 'Times New Roman', 9.5, col == 0)
                row[j*2 + 1].width = Cm(5.6)
    for row in t.rows:
        for c in row.cells:
            for p in c.paragraphs:
                p.paragraph_format.space_before = Pt(1)
                p.paragraph_format.space_after = Pt(1)
                p.paragraph_format.line_spacing = 1.1
    return t

def main():
    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Cm(21), Cm(29.7)
    sec.left_margin = sec.right_margin = Cm(2.0)
    sec.top_margin, sec.bottom_margin = Cm(2.2), Cm(2.0)

    # 页脚页码
    fp = sec.footer.paragraphs[0]
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = fp.add_run()
    f1 = OxmlElement('w:fldChar'); f1.set(qn('w:fldCharType'), 'begin')
    it = OxmlElement('w:instrText'); it.text = 'PAGE'
    f2 = OxmlElement('w:fldChar'); f2.set(qn('w:fldCharType'), 'end')
    r._r.append(f1); r._r.append(it); r._r.append(f2)
    set_font(r, size=9, color=GRAY)

    # ===== 封面 =====
    para(doc, '', after=20)
    para(doc, '大学物理（下册）', size=26, bold=True, cn='黑体',
         align=WD_ALIGN_PARAGRAPH.CENTER, after=6, color=ACCENT)
    para(doc, '期中考试范围 · 作业详解', size=22, bold=True, cn='黑体',
         align=WD_ALIGN_PARAGRAPH.CENTER, after=14)
    para(doc, '第十二次　机械波　·　第十三次　波动光学 1（干涉）', size=13,
         align=WD_ALIGN_PARAGRAPH.CENTER, after=2)
    para(doc, '第十四次　波动光学 2（衍射与光栅）　·　第十五次　波动光学 3（光的偏振）', size=13,
         align=WD_ALIGN_PARAGRAPH.CENTER, after=24)

    info = doc.add_table(rows=5, cols=2)
    info.style = 'Table Grid'
    info.alignment = WD_TABLE_ALIGNMENT.CENTER
    rows = [('课　　程', '大学物理（期中考试范围：第十二~十五次作业）'),
            ('作　　业', '四次作业共 96 题 · 逐题参考答案 + 分步详解 + 知识框架'),
            ('姓　　名', '孙承泽　　　　　学号：2253710052'),
            ('班　　级', '能动强基2501'),
            ('日　　期', '2026 年 9 月 16 日')]
    for (k, v), row in zip(rows, info.rows):
        c0, c1 = row.cells
        c0.width = Cm(3.2); c1.width = Cm(11.8)
        r0 = c0.paragraphs[0].add_run(k); set_font(r0, '黑体', 'Times New Roman', 11, True)
        c0.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        shade_para(c0.paragraphs[0], 'EAF1F8')
        r1 = c1.paragraphs[0].add_run(v); set_font(r1, size=11)
        for p in (c0.paragraphs[0], c1.paragraphs[0]):
            p.paragraph_format.space_before = Pt(4); p.paragraph_format.space_after = Pt(4)
    para(doc, '', after=30)
    para(doc, '—— 老师划定的期中考试范围，按"知识框架 → 逐题解析 → 参考答案"组织 ——',
         size=10.5, align=WD_ALIGN_PARAGRAPH.CENTER, color=GRAY)

    # ===== 使用说明 + 答案速查 =====
    doc.add_page_break()
    heading(doc, '使用说明', 2)
    for t in [
        '本册覆盖期中考试全部范围：第十二次（机械波）、第十三次（波动光学 1·干涉）、第十四次（波动光学 2·衍射与光栅）、第十五次（波动光学 3·偏振），共 96 题。',
        '每个部分先给"知识框架"（本部分要背的公式与判据，含配图），再逐题给出【参考答案】（黄色底纹）与【详解】（建模依据 → 分步代入 → 常见陷阱）。',
        '选择题的详解会逐项排除错误选项；计算题给出完整推导；填空题给出每空的来源公式。',
        '复习路线建议：① 先背知识框架 → ② 合上答案重做计算题 21~24 与每部分的最后两道选择 → ③ 用本册末尾的答案速查表自测全部 96 题 → ④ 错题回看对应详解。']:
        para(doc, '· ' + t, size=10.5, after=3)

    for S in (S12, S13, S14, S15):
        heading(doc, '答案速查表　' + S['title'], 2)
        quick_table(doc, S)

    # ===== 四大部分 =====
    for idx, S in zip(['一', '二', '三', '四'], (S12, S13, S14, S15)):
        build_session(doc, S, idx)

    doc.save(OUT)
    print('OK', OUT)

if __name__ == '__main__':
    main()
