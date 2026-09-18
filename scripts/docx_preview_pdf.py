#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""docx 预览器：把 .docx 按 Word 的排版规则画成 PDF（供肉眼验收）· 通用工具

为什么要自己画：本沙箱 apt 源不可达（HTTP 000），装不了 LibreOffice；typst 只有
Python 包没有 CLI，pandoc 的 --pdf-engine 用不上。于是这里直接按 **docx 里写死的量**
复现排版：段落 exact 行距、前后间距、图片显示尺寸（EMU）、单元格宽度、段落底边框。

因为配套生成器（generate_homework_sheet_docx.py）全部使用 exact 行距与精确图片尺寸，
"预览的版式 ≈ Word 的版式"：预览里能放进一页，Word 里就能放进一页；
若内容溢出，预览会直接多出一页，一眼可见。

用法：
    python scripts/docx_preview_pdf.py 文件.docx [输出.pdf]
退出码：0 = 恰好一页；1 = 多于一页（超页）
"""
from __future__ import annotations

import sys
from pathlib import Path

import pymupdf
from docx import Document
from docx.oxml.ns import qn
from docx.table import Table
from docx.text.paragraph import Paragraph

FONT_DIR = Path("/home/user/opt/fonts")
SONG = FONT_DIR / "NotoSerifSC-Regular.ttf"
HEI = FONT_DIR / "NotoSansSC-Bold.ttf"
LATIN = FONT_DIR / "DejaVuSans.ttf"

EMU_PER_CM = 360000
PT_PER_CM = 72 / 2.54
FONT_CACHE: dict[str, pymupdf.Font] = {}


def get_font(bold: bool) -> tuple[str, str]:
    """返回 (注册名, 字体文件路径)；同名同文件才复用，避免 PyMuPDF 串字体"""
    path = HEI if bold else SONG
    if not path.exists():
        path = LATIN
    name = f"F{int(bold)}_{path.stem}"
    if name not in FONT_CACHE:
        FONT_CACHE[name] = pymupdf.Font(fontfile=str(path))
    return name, str(path)



def compress_image(raw: bytes, quality: int = 82) -> bytes:
    """把题图转成 JPEG 再嵌入——PNG 直嵌会让预览 PDF 膨胀到几 MB（图是线稿，JPEG 足够）"""
    try:
        pix = pymupdf.Pixmap(raw)
        if pix.n > 3 or pix.alpha:
            pix = pymupdf.Pixmap(pymupdf.csRGB, pix)
        return pix.tobytes("jpeg", jpg_quality=quality)
    except Exception:                       # noqa: BLE001
        return raw


def text_width_cm(font: pymupdf.Font, text: str, size: float) -> float:
    return font.text_length(text, size) / PT_PER_CM


def wrap(font: pymupdf.Font, text: str, size: float, avail_cm: float) -> list[str]:
    lines, cur = [], ""
    for ch in text:
        if cur and text_width_cm(font, cur + ch, size) > avail_cm:
            lines.append(cur)
            cur = ch
        else:
            cur += ch
    if cur or not lines:
        lines.append(cur)
    return lines


def para_props(p: Paragraph):
    pPr = p._p.find(qn("w:pPr"))
    sp = pPr.find(qn("w:spacing")) if pPr is not None else None

    def g(el, k, d=0):
        if el is None:
            return d
        try:
            return int(el.get(qn("w:" + k)))
        except (TypeError, ValueError):
            return d

    before = g(sp, "before") / 20.0
    after = g(sp, "after") / 20.0
    line = g(sp, "line") / 20.0
    rule = sp.get(qn("w:lineRule")) if sp is not None else None
    has_bottom = False
    if pPr is not None:
        bdr = pPr.find(qn("w:pBdr"))
        has_bottom = bdr is not None and bdr.find(qn("w:bottom")) is not None
    return before, after, line, rule, has_bottom


def runs_of(p: Paragraph):
    out = []
    for r in p.runs:
        out.append({
            "text": r.text or "",
            "size": r.font.size.pt if r.font.size else 10.5,
            "bold": bool(r.font.bold),
            "pic": bool(r._element.findall(".//" + qn("w:drawing"))),
            "run": r,
        })
    return out


def draw_text(page, x_cm, y_cm, text, size, bold, avail_cm, align="left") -> float:
    """在 (x_cm, y_cm) 左上角开始画文本，返回占用高度（cm）"""
    name, path = get_font(bold)
    font = FONT_CACHE[name]
    line_h = size * 1.35 / PT_PER_CM
    for i, ln in enumerate(wrap(font, text, size, avail_cm)):
        w = text_width_cm(font, ln, size)
        xx = x_cm + ((avail_cm - w) / 2 if align == "center" else 0)
        page.insert_text((xx * PT_PER_CM, (y_cm + i * line_h + size * 0.80 / PT_PER_CM) * PT_PER_CM),
                         ln, fontsize=size, fontname=name, fontfile=path)
    return line_h * max(1, len(wrap(font, text, size, avail_cm)))


def cell_width_cm(cell, default: float) -> float:
    tcPr = cell._tc.find(qn("w:tcPr"))
    if tcPr is None:
        return default
    tcW = tcPr.find(qn("w:tcW"))
    if tcW is None:
        return default
    try:
        return int(tcW.get(qn("w:w")) or 0) / 567.0 or default
    except (TypeError, ValueError):
        return default


def render(docx_path: Path, out_pdf: Path) -> int:
    doc = Document(str(docx_path))
    sec = doc.sections[0]
    pg_w, pg_h = sec.page_width.cm, sec.page_height.cm
    ml, mr = sec.left_margin.cm, sec.right_margin.cm
    mt = sec.top_margin.cm
    usable_w = pg_w - ml - mr

    pdf = pymupdf.open()
    page = pdf.new_page(width=pg_w * PT_PER_CM, height=pg_h * PT_PER_CM)
    y = mt
    pages = 1

    def newpage():
        nonlocal page, y, pages
        page = pdf.new_page(width=pg_w * PT_PER_CM, height=pg_h * PT_PER_CM)
        y, pages = mt, pages + 1

    for block in doc.element.body.iterchildren():
        if block.tag == qn("w:p"):
            p = Paragraph(block, doc)
            before, after, line, rule, has_bottom = para_props(p)
            y += before / PT_PER_CM
            parts = runs_of(p)
            text = "".join(x["text"] for x in parts)
            if any(x["pic"] for x in parts):
                continue                      # 图片由表格分支负责
            size = max([x["size"] for x in parts] or [10.5])
            bold = any(x["bold"] for x in parts)
            align = "center" if p.alignment == 1 else "left"
            h = draw_text(page, ml, y, text, size, bold, usable_w, align) if text else 0.0
            if not text:
                h = (line / PT_PER_CM) if rule == "exact" and line else size * 1.35 / PT_PER_CM
            y += h
            if has_bottom:
                yy = y * PT_PER_CM
                page.draw_line(pymupdf.Point(ml * PT_PER_CM, yy),
                               pymupdf.Point((ml + usable_w) * PT_PER_CM, yy),
                               color=(0.75, 0.75, 0.75), width=0.5, dashes="[2 3] 0")
            y += after / PT_PER_CM
        elif block.tag == qn("w:tbl"):
            tbl = Table(block, doc)
            tpr = tbl._tbl.tblPr
            bd = tpr.find(qn("w:tblBorders")) if tpr is not None else None

            def border_on(edge):
                if bd is None:
                    return False
                el = bd.find(qn("w:" + edge))
                return el is not None and el.get(qn("w:val")) not in (None, "none")

            row_lines, bottom_line = border_on("insideH"), border_on("bottom")
            widths = [cell_width_cm(c, usable_w / max(1, len(tbl.rows[0].cells)))
                      for c in tbl.rows[0].cells]
            tbl_top = y
            for r_ in tbl.rows:
                # 行高：优先 exact 的 trHeight，否则按单元格内容量
                trPr = r_._tr.find(qn("w:trPr"))
                h_cm = 0.0
                if trPr is not None:
                    th = trPr.find(qn("w:trHeight"))
                    if th is not None and th.get(qn("w:hRule")) == "exact":
                        h_cm = int(th.get(qn("w:val")) or 0) / 567.0
                x = ml
                for idx, cell in enumerate(r_.cells):
                    cw = widths[idx] if idx < len(widths) else usable_w
                    cy, cy_max = y, y
                    for p in cell.paragraphs:
                        before, after, line, rule, _ = para_props(p)
                        cy += before / PT_PER_CM
                        parts = runs_of(p)
                        pics = [q for q in parts if q["pic"]]
                        if pics:
                            for q in pics:
                                el = q["run"]._element
                                blip = el.find(".//" + qn("a:blip"))
                                ext = el.find(".//" + qn("wp:extent"))
                                if blip is None or ext is None:
                                    continue
                                img = compress_image(
                                    doc.part.related_parts[blip.get(qn("r:embed"))].blob)
                                w_cm = int(ext.get("cx")) / EMU_PER_CM
                                pic_h = int(ext.get("cy")) / EMU_PER_CM
                                page.insert_image(
                                    pymupdf.Rect((x + (cw - w_cm) / 2) * PT_PER_CM, cy * PT_PER_CM,
                                                 (x + (cw + w_cm) / 2) * PT_PER_CM,
                                                 (cy + pic_h) * PT_PER_CM),
                                    stream=img)
                                cy += pic_h
                        else:
                            txt = "".join(q["text"] for q in parts)
                            if txt.strip():
                                size = max(q["size"] for q in parts)
                                bold = any(q["bold"] for q in parts)
                                align = "center" if p.alignment == 1 else "left"
                                h_txt = draw_text(page, x, cy, txt, size, bold, cw, align)
                                if rule == "exact" and line:
                                    n = max(1, round(h_txt / (line / PT_PER_CM)))
                                    cy += n * line / PT_PER_CM
                                else:
                                    cy += h_txt
                            elif rule == "exact" and line:
                                cy += line / PT_PER_CM
                        cy += after / PT_PER_CM
                        cy_max = max(cy_max, cy)
                    x += cw
                    h_cm = max(h_cm, cy_max - y)
                y += h_cm
            # 逐行画线：insideH 画在行与行之间，bottom 画在表尾
            if row_lines or bottom_line:
                acc = tbl_top
                for ri, r_ in enumerate(tbl.rows):
                    trPr = r_._tr.find(qn("w:trPr"))
                    h_cm = 0.0
                    if trPr is not None:
                        th = trPr.find(qn("w:trHeight"))
                        if th is not None and th.get(qn("w:hRule")) == "exact":
                            h_cm = int(th.get(qn("w:val")) or 0) / 567.0
                    acc += h_cm or (y - tbl_top) / max(1, len(tbl.rows))
                    last = ri == len(tbl.rows) - 1
                    if (not last and row_lines) or (last and bottom_line):
                        page.draw_line(pymupdf.Point(ml * PT_PER_CM, acc * PT_PER_CM),
                                       pymupdf.Point((ml + usable_w) * PT_PER_CM, acc * PT_PER_CM),
                                       color=(0.75, 0.75, 0.75), width=0.5, dashes="[2 3] 0")
        if y > pg_h - sec.bottom_margin.cm:
            newpage()

    # 字体子集化：不这么做会把整只思源宋体（3.7 MB）嵌进只有两三行字的预览里
    try:
        pdf.subset_fonts()
    except Exception as exc:                    # noqa: BLE001
        print("  （字体子集化跳过：%s）" % exc)
    pdf.save(str(out_pdf), garbage=4, deflate=True)
    print(f"预览：{out_pdf}　共 {pages} 页　（末页已用 {y:.2f} cm / 可用 "
          f"{pg_h - mt - sec.bottom_margin.cm:.2f} cm）")
    return pages


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    src = Path(sys.argv[1])
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else src.with_suffix(".preview.pdf")
    return 0 if render(src, out) == 1 else 1


if __name__ == "__main__":
    sys.exit(main())
