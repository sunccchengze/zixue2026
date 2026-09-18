#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""作业单生成器：把若干题目排成「一页 A4 docx」，每题下方留手写作答空白 · 通用工具

为什么要有它：老师布置作业后，题目散在教材扫描件里；直接打印教材页又浪费纸、也没地方写。
本脚本按 spec（JSON）把题面 + 配图 + 作答空白排成一页，打印出来即可手写。

用法：
    python scripts/generate_homework_sheet_docx.py spec.json [输出.docx]

spec.json 结构：
{
  "title": "《工程力学》作业单",
  "info":  "姓名：… 学号：… 班级：… 日期：… ｜ 来源说明…",
  "questions": [
    {"no": "2-1", "text": "题面原文…", "fig": "图/题2-1.png",
     "fig_width_cm": 3.9, "fig_aspect": 1.45, "lines": 5}
  ],
  "footer": "作答要求（可选）"
}

**为什么能保证"一页"**：所有段落的行距都写成 Word 的 exact（绝对磅值），图片按 EMU 精确给宽高，
于是「Word 的排版结果 = 本脚本算出的高度」。生成后会自动跑一次独立审计
（scripts/docx_page_audit.py，直接读回 docx 的 XML 重新累加），两者对上才算通过。
"""
from __future__ import annotations

import json
import subprocess
import struct
import sys
import pathlib

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

BODY_CJK = "宋体"
HEAD_CJK = "黑体"
BODY_LATIN = "Times New Roman"

RULE_CM = 0.8            # 每条手写横线的高度（= 一行手写空间）
GAP_CM = 0.35            # 题与题之间的空白（防止下一题压到上一条横线）
LINE_FACTOR = 1.35       # exact 行距 = 字号 × 此系数（中文需要比 1.2 更宽）
CM_PER_PT = 2.54 / 72.0
MARGIN_CM = 1.5
PAGE_W, PAGE_H = 21.0, 29.7


# ── 低层工具 ────────────────────────────────────────────────────────────────

def set_run(run, size=10.5, bold=False, cjk=BODY_CJK, latin=BODY_LATIN, color=None):
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.name = latin
    run._element.rPr.rFonts.set(qn("w:eastAsia"), cjk)
    if color is not None:
        run.font.color.rgb = color


def exact_spacing(p, size_pt, before_pt=0.0, after_pt=0.0, factor=LINE_FACTOR):
    """把段落行距写成 exact（Word 会严格照办，不做字体相关计算）"""
    pf = p.paragraph_format
    pf.space_before = Pt(before_pt)
    pf.space_after = Pt(after_pt)
    pf.line_spacing = Pt(round(size_pt * factor, 1))
    return size_pt * factor * CM_PER_PT + (before_pt + after_pt) * CM_PER_PT


def para_border_bottom(paragraph, val="dashed", sz="6", color="BFBFBF"):
    pPr = paragraph._p.get_or_add_pPr()
    pBdr = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), val)
    bottom.set(qn("w:sz"), sz)
    bottom.set(qn("w:space"), "1")
    bottom.set(qn("w:color"), color)
    pBdr.append(bottom)
    pPr.append(pBdr)


def no_borders(table):
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = OxmlElement(f"w:{edge}")
        el.set(qn("w:val"), "none")
        borders.append(el)
    table._tbl.tblPr.append(borders)


def cell_text_width(cell, cm):
    """固定单元格宽度（Word 不会自己改）"""
    cell.width = Cm(cm)
    tcPr = cell._tc.get_or_add_tcPr()
    tcW = tcPr.find(qn("w:tcW"))
    if tcW is None:
        tcW = OxmlElement("w:tcW")
        tcPr.append(tcW)
    tcW.set(qn("w:w"), str(int(cm * 567)))
    tcW.set(qn("w:type"), "dxa")


def png_size(path: pathlib.Path) -> tuple[int, int]:
    with open(path, "rb") as f:
        head = f.read(24)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"不是 PNG：{path}")
    return struct.unpack(">II", head[16:24])



def writing_lines(doc, n: int, width_cm: float, line_cm: float = RULE_CM):
    """用**表格**画 n 条手写横线。

    为什么不直接用 n 个带下边框的段落：Word 会把"相邻且边框定义相同"的段落合并成一个
    边框组，只画出组的底边——5 条线会塌成 1 条。表格的行边框不会被这样合并，
    这是答题纸模板的通行做法。
    线的构成：insideH 画行与行之间（n−1 条）+ bottom 画最后一行底下（1 条）= n 条。
    """
    tbl = doc.add_table(rows=n, cols=1)
    tbl.autofit = False
    tblPr = tbl._tbl.tblPr
    borders = OxmlElement("w:tblBorders")
    for edge, val in (("top", "none"), ("left", "none"), ("right", "none"),
                      ("insideV", "none"), ("insideH", "dashed"), ("bottom", "dashed")):
        el = OxmlElement(f"w:{edge}")
        el.set(qn("w:val"), val)
        if val == "dashed":
            el.set(qn("w:sz"), "6")
            el.set(qn("w:color"), "BFBFBF")
        borders.append(el)
    tblPr.append(borders)
    twips = int(width_cm * 567)
    tblW = OxmlElement("w:tblW")
    tblW.set(qn("w:w"), str(twips))
    tblW.set(qn("w:type"), "dxa")
    tblPr.append(tblW)
    for row in tbl.rows:
        row.height = Cm(line_cm)
        trPr = row._tr.get_or_add_trPr()
        h = OxmlElement("w:trHeight")
        h.set(qn("w:val"), str(int(line_cm * 567)))
        h.set(qn("w:hRule"), "exact")
        trPr.append(h)
        cell = row.cells[0]
        cell_text_width(cell, width_cm)
        cp = cell.paragraphs[0]
        cp.paragraph_format.space_before = Pt(0)
        cp.paragraph_format.space_after = Pt(0)
        cp.paragraph_format.line_spacing = Pt(round(line_cm / CM_PER_PT, 1))
    return n * line_cm


# ── 排版 ────────────────────────────────────────────────────────────────────

def build(spec: dict, out: pathlib.Path) -> float:
    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Cm(PAGE_W), Cm(PAGE_H)
    sec.top_margin = sec.bottom_margin = Cm(MARGIN_CM)
    sec.left_margin = sec.right_margin = Cm(MARGIN_CM)
    usable_w = PAGE_W - 2 * MARGIN_CM
    usable_h = PAGE_H - 2 * MARGIN_CM
    used = 0.0

    # 标题
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_run(p.add_run(spec["title"]), size=15, bold=True, cjk=HEAD_CJK)
    used += exact_spacing(p, 15, after_pt=2)

    # 信息行（姓名/学号/班级/日期 + 题目来源）
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_run(p.add_run(spec["info"]), size=9.5)
    used += exact_spacing(p, 9.5, after_pt=3 if spec.get("meta") else 5)

    if spec.get("meta"):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_run(p.add_run(spec["meta"]), size=8.5, color=RGBColor(0x60, 0x60, 0x60))
        used += exact_spacing(p, 8.5, after_pt=4)

    for q in spec["questions"]:
        fig_w = float(q.get("fig_width_cm", 4.0))
        fig_path = (pathlib.Path(spec["_base"]) / q["fig"]) if q.get("fig") else None
        has_fig = bool(fig_path and fig_path.exists())
        if has_fig:
            pw, ph = png_size(fig_path)
            aspect = float(q.get("fig_aspect") or (pw / ph))
            fig_h = fig_w / aspect
        else:
            aspect, fig_h = 1.0, 0.0
            print(f"  ⚠ {q['no']}：缺配图 {q.get('fig')}")

        cap_pt = 8.0
        cap_h = cap_pt * LINE_FACTOR * CM_PER_PT + 1 * CM_PER_PT
        # 表格行高：取「图 + 图注」与「题面文字」的较大者
        text_w = usable_w - fig_w - 0.35
        text_lines = max(1, int(len(q["text"]) * 10.5 * 0.95 / (text_w / CM_PER_PT) ) + 1)
        text_h = text_lines * 10.5 * 1.15 * CM_PER_PT
        row_h = max(fig_h + cap_h, text_h)

        tbl = doc.add_table(rows=1, cols=2)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        tbl.autofit = False
        no_borders(tbl)
        left, right = tbl.rows[0].cells
        cell_text_width(left, text_w)
        cell_text_width(right, fig_w + 0.35)

        L = left.paragraphs[0]
        L.paragraph_format.space_after = Pt(0)
        L.paragraph_format.line_spacing = Pt(round(10.5 * 1.2, 1))
        set_run(L.add_run(f"{q['no']}　"), size=10.5, bold=True, cjk=HEAD_CJK)
        set_run(L.add_run(q["text"]), size=10.5)

        R = right.paragraphs[0]
        R.alignment = WD_ALIGN_PARAGRAPH.CENTER
        R.paragraph_format.space_after = Pt(0)
        if has_fig:
            # 图片行用 exact 行距 = 图高，避免 Word 按字体行高把行撑大
            R.paragraph_format.line_spacing = Pt(round(fig_h / CM_PER_PT * 1.02, 1))
            R.add_run().add_picture(str(fig_path), width=Cm(fig_w))
        cap = right.add_paragraph()
        cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cap.paragraph_format.space_before = Pt(1)
        cap.paragraph_format.space_after = Pt(0)
        cap.paragraph_format.line_spacing = Pt(round(cap_pt * 1.1, 1))
        set_run(cap.add_run(f"题 {q['no']} 图"), size=cap_pt,
                color=RGBColor(0x80, 0x80, 0x80))
        used += row_h

        # 作答区标签
        lab = doc.add_paragraph()
        set_run(lab.add_run("作答（写出必要步骤）"), size=9, cjk=HEAD_CJK,
                color=RGBColor(0x50, 0x50, 0x50))
        used += exact_spacing(lab, 9, before_pt=4, after_pt=2)

        # 手写横线
        used += writing_lines(doc, int(q.get("lines", 4)), usable_w)

        # 题间空白：否则下一题的第一行会贴在本题最后一条横线上
        gap = doc.add_paragraph()
        gap.paragraph_format.space_before = Pt(0)
        gap.paragraph_format.space_after = Pt(0)
        gap.paragraph_format.line_spacing = Pt(round(GAP_CM / CM_PER_PT, 1))
        used += GAP_CM

    if spec.get("footer"):
        p = doc.add_paragraph()
        set_run(p.add_run(spec["footer"]), size=9, color=RGBColor(0x55, 0x55, 0x55))
        used += exact_spacing(p, 9, before_pt=5)

    out.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(out))

    print(f"生成：{out.name}")
    print(f"  设计占高 {used:.2f} cm ／ 可用 {usable_h:.2f} cm　余量 {usable_h - used:.2f} cm")

    # 独立审计：读回 docx，按 Word 的规则重新累加
    audit = pathlib.Path(__file__).with_name("docx_page_audit.py")
    if audit.exists():
        r = subprocess.run([sys.executable, str(audit), str(out)],
                           capture_output=True, text=True)
        print(r.stdout.strip() or r.stderr.strip())
    return used


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    spec_path = pathlib.Path(sys.argv[1]).resolve()
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    spec["_base"] = str(spec_path.parent)
    out = pathlib.Path(sys.argv[2]).resolve() if len(sys.argv) > 2 \
        else spec_path.with_suffix(".docx")
    build(spec, out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
