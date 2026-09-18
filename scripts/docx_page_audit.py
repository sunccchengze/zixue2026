#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""docx 单页审计：直接读回 .docx 的 XML，按 Word 的排版规则累加高度 · 通用工具

用途：确认一份「必须一页」的 docx 真的只占一页（不靠肉眼、不靠生成时的估算）。

判定依据（都是 Word 会严格照做的量）：
  · 段落行距若为 exact（w:spacing/@w:lineRule="exact"）→ 高度＝该磅值
  · 若为 auto/multiple → 用「字号 × 1.35」保守估算
  · 段落前后间距 w:before / w:after 照加
  · 图片：w:drawing 里的 wp:extent（EMU）→ 精确高度
  · 表格：逐行取各单元格内容高度的最大值
  · 页面：sectPr 的 pgSz / pgMar 算可用高度

用法：
    python scripts/docx_page_audit.py 文件.docx [--verbose]
"""
from __future__ import annotations

import sys
import zipfile
from pathlib import Path

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
WP = "{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}"
EMU_PER_CM = 360000


def _int(el, attr, default=0):
    if el is None:
        return default
    v = el.get(W + attr)
    try:
        return int(v)
    except (TypeError, ValueError):
        return default


def _text_cm(p) -> tuple[float, float]:
    """(文本宽度, 最大字号) 估算——用于判断这一段会折成几行"""
    size = 10.5
    for sz in p.iter(W + "sz"):
        v = sz.get(W + "val")
        if v and v.isdigit():
            size = max(size, int(v) / 2.0)
    width = 0.0
    for t in p.iter(W + "t"):
        for ch in (t.text or ""):
            width += size * (1.0 if ord(ch) > 0x2E7F else 0.5)
    return width * (2.54 / 72.0), size


def para_height_cm(p, avail_cm: float | None = None) -> float:
    """单个段落的高度（cm）。给 avail_cm 时会估算折行行数。"""
    pPr = p.find(W + "pPr")
    sp = pPr.find(W + "spacing") if pPr is not None else None
    before = _int(sp, "before") / 20.0        # twips → pt
    after = _int(sp, "after") / 20.0
    line = _int(sp, "line")
    rule = sp.get(W + "lineRule") if sp is not None else None

    # 图片高度（占位行）
    img_cm = 0.0
    for ext in p.iter(WP + "extent"):
        cx, cy = _int(ext, "cx"), _int(ext, "cy")
        img_cm = max(img_cm, cy / EMU_PER_CM)
    line_cm = (line / 20.0) * (2.54 / 72.0) if rule == "exact" and line else 0.0

    # 文字行：exact 行距就按它算；auto/multiple 用 字号×1.35（保守）
    # 折行估算：exact 行距下，Word 每行就占这些磅值，行数 = 文本宽 / 可用宽
    n_lines = 1
    if avail_cm:
        tw, _ = _text_cm(p)
        if tw > 0:
            n_lines = max(1, int(tw / avail_cm) + (1 if tw % avail_cm else 0))
    if line_cm:
        text_cm = line_cm * n_lines
    else:
        _, size = _text_cm(p)
        text_cm = size * 1.35 * (2.54 / 72.0) * n_lines

    body = max(img_cm, text_cm)
    return body + (before + after) * (2.54 / 72.0)


def cell_height_cm(tc, avail_cm: float) -> float:
    return sum(para_height_cm(p, avail_cm) for p in tc.findall(W + "p"))


def table_height_cm(tbl, avail_cm: float) -> float:
    total = 0.0
    for tr in tbl.findall(W + "tr"):
        rows = []
        for tc in tr.findall(W + "tc"):
            tcPr = tc.find(W + "tcPr")
            w = _int(tcPr.find(W + "tcW") if tcPr is not None else None, "w", 0) / 567.0
            rows.append(cell_height_cm(tc, w or avail_cm))
        h = max(rows) if rows else 0.0
        # 行高若写了 exact（w:trHeight/@hRule="exact"），Word 严格照办，取较大者
        trPr = tr.find(W + "trPr")
        th = trPr.find(W + "trHeight") if trPr is not None else None
        if th is not None and th.get(W + "hRule") == "exact":
            h = max(h, _int(th, "val") / 567.0)
        total += h
    return total


def audit(path: Path, verbose: bool = False) -> int:
    with zipfile.ZipFile(path) as z:
        xml = z.read("word/document.xml").decode("utf-8")
    body = xml.split("<w:body>", 1)[1].rsplit("</w:body>", 1)[0]

    import re
    # 取 body 直接子元素（段落 / 表格 / sectPr）
    root = re.sub(r"^\s*<\?xml[^>]*\?>", "", xml)
    from xml.etree import ElementTree as ET
    tree = ET.fromstring(root)
    b = tree.find(W + "body")

    # 页面可用高度
    sect = b.find(W + "sectPr")
    pg_h_cm = 29.7
    pg_w_cm = 21.0
    margins = 0.0
    if sect is not None:
        pg = sect.find(W + "pgSz")
        mar = sect.find(W + "pgMar")
        if pg is not None:
            pg_h_cm = _int(pg, "h", int(29.7 * 567)) / 567.0
            pg_w_cm = _int(pg, "w", int(21.0 * 567)) / 567.0
        if mar is not None:
            margins = (_int(mar, "top", 851) + _int(mar, "bottom", 851)) / 567.0
    usable = pg_h_cm - margins
    mar_l = mar_r = 851
    if sect is not None:
        _m = sect.find(W + "pgMar")
        if _m is not None:
            mar_l = _int(_m, "left", 851)
            mar_r = _int(_m, "right", 851)
    avail_w = pg_w_cm - (mar_l + mar_r) / 567.0

    total = 0.0
    items = []
    for child in b:
        if child.tag == W + "p":
            h = para_height_cm(child, avail_w)
            total += h
            txt = "".join(t.text or "" for t in child.iter(W + "t"))[:28]
            has_img = any(True for _ in child.iter(WP + "extent"))
            items.append((h, ("[图片] " if has_img else "") + txt))
        elif child.tag == W + "tbl":
            h = table_height_cm(child, avail_w)
            total += h
            items.append((h, "[表格]"))
    # 最后一节的 sectPr 也算 body 子元素但无高度

    print(f"审计：{path.name}")
    print(f"  页面可用高度 {usable:.2f} cm ｜ XML 累加高度 {total:.2f} cm"
          f" ｜ 余量 {usable - total:.2f} cm")
    if verbose:
        for h, label in items:
            print(f"    {h:6.2f} cm  {label}")
    verdict = "✔ 一页放得下" if total <= usable else "✘ 超出一页"
    print(f"  判定：{verdict}")
    return 0 if total <= usable else 1


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    verbose = "--verbose" in sys.argv
    if not args:
        print(__doc__)
        return 2
    return audit(Path(args[0]), verbose)


if __name__ == "__main__":
    sys.exit(main())
