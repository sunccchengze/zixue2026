#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DOCX -> PDF 转换器（支持 Word 原生 OMML <m:oMath>/<m:oMathPara> 公式、表格着色与边框、高亮框、图片与页眉页脚）
采用 KaTeX 字体族 + New Computer Modern Math + 思源宋体 (Source Han Serif) 矢量排版引擎输出印刷级 PDF。

用法：
    python 大学物理实验/工具/B309/docx_to_pdf.py [输入.docx] [输出.pdf]
"""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path
from lxml import etree
from docx import Document
from docx.oxml.ns import qn

M_URI = "http://schemas.openxmlformats.org/officeDocument/2006/math"
W_URI = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
R_URI = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
EMU_PER_INCH = 914400.0

ROOT = next(p for p in Path(__file__).resolve().parents if (p / "AGENTS.md").is_file())
TOOL_DIR = Path(__file__).resolve().parent
FONT_DIR = TOOL_DIR / "fonts"
KATEX_FONT_DIR = FONT_DIR / "katex"
DEFAULT_DOCX = ROOT / "大学物理实验/实验项目/实验报告/B309-等厚干涉/实验报告-等厚干涉-完整版.docx"
DEFAULT_PDF = ROOT / "大学物理实验/实验项目/实验报告/B309-等厚干涉/实验报告-等厚干涉-完整版.pdf"

OP_MAP = {
    "−": "-",
    "⋅": "dot.op",
    "×": "times",
    "±": "plus.minus",
    "≈": "approx",
    "∝": "prop",
    "→": "arrow.r",
    "⇒": "arrow.r.double",
    "⟹": "arrow.r.double.long",
    "∣": "bar.v",
    "|": "bar.v",
    "∼": "tilde.op",
    "°": "degree",
    "…": "dots.h",
    "∑": "sum",
    "%": "\\%",
    "/": "\\/",
    "(": "\\(",
    ")": "\\)",
    "[": "\\[",
    "]": "\\]",
}


def local(el: etree._Element) -> str:
    return etree.QName(el).localname


def esc_typst_text(s: str) -> str:
    # 转义 Typst 标记模式特殊字符
    out = []
    for ch in s:
        if ch in ("\\", "#", "*", "_", "`", "$", "@", "<", ">", "[", "]", "~"):
            out.append("\\" + ch)
        else:
            out.append(ch)
    return "".join(out)


def esc_typst_str(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"')


def omath_to_typst(el: etree._Element | None, display: bool = False) -> str:
    if el is None:
        return ""
    t = local(el)
    if t in ("oMathPara", "oMath", "e", "num", "den", "sub", "sup"):
        parts = [omath_to_typst(c, display=display) for c in el]
        return " ".join(p for p in parts if p)
    if t == "r":
        rPr = el.find(f"{{{M_URI}}}rPr")
        is_nor = rPr is not None and rPr.find(f"{{{M_URI}}}nor") is not None
        mt = el.find(f"{{{M_URI}}}t")
        txt = (mt.text or "") if mt is not None else ""
        if not txt:
            return ""
        if is_nor:
            return f'"{esc_typst_str(txt)}"'
        if txt in OP_MAP:
            return OP_MAP[txt]
        if all(c.isdigit() or c == "." for c in txt):
            return txt
        if len(txt) == 1:
            return OP_MAP.get(txt, txt)
        tokens = []
        buf_num = ""
        for ch in txt:
            if ch.isdigit() or ch == ".":
                buf_num += ch
            else:
                if buf_num:
                    tokens.append(buf_num)
                    buf_num = ""
                if ch.isspace():
                    continue
                tokens.append(OP_MAP.get(ch, ch))
        if buf_num:
            tokens.append(buf_num)
        return " ".join(tokens)
    if t == "f":
        num = omath_to_typst(el.find(f"{{{M_URI}}}num"), display=display)
        den = omath_to_typst(el.find(f"{{{M_URI}}}den"), display=display)
        frac_code = f"frac({num}, {den})"
        return f"display({frac_code})" if display else frac_code
    if t == "rad":
        body = omath_to_typst(el.find(f"{{{M_URI}}}e"), display=display)
        return f"sqrt({body})"
    if t == "bar":
        body = omath_to_typst(el.find(f"{{{M_URI}}}e"), display=display)
        return f"overline({body})"
    if t == "acc":
        body = omath_to_typst(el.find(f"{{{M_URI}}}e"), display=display)
        return f"hat({body})"
    if t == "sSub":
        base = omath_to_typst(el.find(f"{{{M_URI}}}e"), display=display)
        sub = omath_to_typst(el.find(f"{{{M_URI}}}sub"), display=display)
        return f"attach({base}, b: ({sub}))"
    if t == "sSup":
        base = omath_to_typst(el.find(f"{{{M_URI}}}e"), display=display)
        sup = omath_to_typst(el.find(f"{{{M_URI}}}sup"), display=display)
        return f"attach({base}, t: ({sup}))"
    if t == "sSubSup":
        base = omath_to_typst(el.find(f"{{{M_URI}}}e"), display=display)
        sub = omath_to_typst(el.find(f"{{{M_URI}}}sub"), display=display)
        sup = omath_to_typst(el.find(f"{{{M_URI}}}sup"), display=display)
        return f"attach({base}, b: ({sub}), t: ({sup}))"
    if t == "nary":
        naryPr = el.find(f"{{{M_URI}}}naryPr")
        chr_el = naryPr.find(f"{{{M_URI}}}chr") if naryPr is not None else None
        op_ch = chr_el.get(f"{{{M_URI}}}val", "∑") if chr_el is not None else "∑"
        op_typ = {"∑": "sum", "∏": "product", "∫": "integral"}.get(op_ch, "sum")
        sub = omath_to_typst(el.find(f"{{{M_URI}}}sub"), display=display)
        sup = omath_to_typst(el.find(f"{{{M_URI}}}sup"), display=display)
        body = omath_to_typst(el.find(f"{{{M_URI}}}e"), display=display)
        head = f"limits({op_typ})" if display else op_typ
        return f"attach({head}, b: ({sub}), t: ({sup})) {body}"
    return ""


def get_omath_style(om_el: etree._Element) -> tuple[float | None, bool, str | None]:
    wrPr = om_el.find(f".//{{{W_URI}}}rPr")
    if wrPr is None:
        return None, False, None
    sz_el = wrPr.find(f"{{{W_URI}}}sz")
    size_pt = int(sz_el.get(f"{{{W_URI}}}val")) / 2.0 if (sz_el is not None and sz_el.get(f"{{{W_URI}}}val")) else None
    bold = wrPr.find(f"{{{W_URI}}}b") is not None
    col_el = wrPr.find(f"{{{W_URI}}}color")
    col = col_el.get(f"{{{W_URI}}}val") if col_el is not None else None
    if col and col.lower() == "auto":
        col = None
    return size_pt, bold, col


def extract_run_style(r_el: etree._Element) -> tuple[float | None, bool, bool, str | None]:
    rPr = r_el.find(f"{{{W_URI}}}rPr")
    if rPr is None:
        return None, False, False, None
    sz_el = rPr.find(f"{{{W_URI}}}sz")
    size_pt = int(sz_el.get(f"{{{W_URI}}}val")) / 2.0 if (sz_el is not None and sz_el.get(f"{{{W_URI}}}val")) else None
    bold = rPr.find(f"{{{W_URI}}}b") is not None
    italic = rPr.find(f"{{{W_URI}}}i") is not None
    col_el = rPr.find(f"{{{W_URI}}}color")
    col = col_el.get(f"{{{W_URI}}}val") if col_el is not None else None
    if col and col.lower() == "auto":
        col = None
    return size_pt, bold, italic, col


def style_wrap(content: str, size_pt: float | None = None, bold: bool = False,
               italic: bool = False, color: str | None = None) -> str:
    if not content:
        return ""
    args = []
    if size_pt is not None:
        args.append(f"size: {size_pt:.2f}pt")
    if bold:
        args.append('weight: "bold"')
    if color:
        args.append(f'fill: rgb("#{color}")')
    if italic and not args:
        return f"#emph[{content}]"
    if args:
        inner = f"#emph[{content}]" if italic else content
        return f"#text({', '.join(args)})[{inner}]"
    return content


def render_paragraph_children(p_el: etree._Element, doc: Document, img_dir: Path, img_counter: list[int]) -> tuple[str, bool]:
    """返回 (Typst 内容字符串, 是否仅包含独立行间公式或图片)"""
    pieces: list[str] = []
    has_display_or_img = False
    for child in p_el:
        ctag = local(child)
        if ctag == "r":
            # 检查是否含内嵌图片
            blip = child.find(".//" + qn("a:blip"))
            ext = child.find(".//" + qn("wp:extent"))
            if blip is not None and ext is not None:
                rel_id = blip.get(f"{{{R_URI}}}embed")
                part = doc.part.related_parts[rel_id]
                img_counter[0] += 1
                suffix = Path(str(part.partname)).suffix or ".png"
                img_file = img_dir / f"img_{img_counter[0]}{suffix}"
                img_file.write_bytes(part.blob)
                w_in = int(ext.get("cx")) / EMU_PER_INCH
                pieces.append(f'#image("{img_file.name}", width: {w_in:.2f}in)')
                has_display_or_img = True
                continue
            t_nodes = child.findall(f"{{{W_URI}}}t")
            txt = "".join((tn.text or "") for tn in t_nodes)
            if not txt:
                continue
            sz, b, it, col = extract_run_style(child)
            pieces.append(style_wrap(esc_typst_text(txt), sz, b, it, col))
        elif ctag == "oMath":
            t_math = omath_to_typst(child, display=False)
            sz, b, col = get_omath_style(child)
            pieces.append(style_wrap(f"${t_math}$", sz, b, False, col))
        elif ctag == "oMathPara":
            om = child.find(f"{{{M_URI}}}oMath")
            t_math = omath_to_typst(om, display=True)
            sz, b, col = get_omath_style(om) if om is not None else (None, False, None)
            pieces.append(style_wrap(f"$ {t_math} $", sz, b, False, col))
            has_display_or_img = True
    return "".join(pieces), has_display_or_img


def parse_para_props(p_el: etree._Element) -> dict:
    info = {
        "align": "left",
        "before_pt": 0.0,
        "after_pt": 3.0,
        "indent_pt": 0.0,
        "fill": None,
        "borders": {},
        "page_break_before": False,
    }
    pPr = p_el.find(f"{{{W_URI}}}pPr")
    if pPr is None:
        return info
    page_break = pPr.find(f"{{{W_URI}}}pageBreakBefore")
    page_break_val = page_break.get(f"{{{W_URI}}}val", "1") if page_break is not None else "0"
    info["page_break_before"] = page_break is not None and page_break_val.lower() not in ("0", "false", "off", "none")
    jc = pPr.find(f"{{{W_URI}}}jc")
    if jc is not None:
        val = jc.get(f"{{{W_URI}}}val", "")
        if val in ("center",):
            info["align"] = "center"
        elif val in ("right", "end"):
            info["align"] = "right"
    sp = pPr.find(f"{{{W_URI}}}spacing")
    if sp is not None:
        if sp.get(f"{{{W_URI}}}before"):
            info["before_pt"] = int(sp.get(f"{{{W_URI}}}before")) / 20.0
        if sp.get(f"{{{W_URI}}}after"):
            info["after_pt"] = int(sp.get(f"{{{W_URI}}}after")) / 20.0
    ind = pPr.find(f"{{{W_URI}}}ind")
    if ind is not None and ind.get(f"{{{W_URI}}}firstLine"):
        info["indent_pt"] = int(ind.get(f"{{{W_URI}}}firstLine")) / 20.0
    shd = pPr.find(f"{{{W_URI}}}shd")
    if shd is not None:
        fill = shd.get(f"{{{W_URI}}}fill")
        if fill and fill.lower() not in ("auto", "ffffff"):
            info["fill"] = fill
    pBdr = pPr.find(f"{{{W_URI}}}pBdr")
    if pBdr is not None:
        for side in ("left", "top", "right", "bottom"):
            b_el = pBdr.find(f"{{{W_URI}}}{side}")
            if b_el is not None and b_el.get(f"{{{W_URI}}}val") not in (None, "none", "nil"):
                sz = int(b_el.get(f"{{{W_URI}}}sz", "4")) / 8.0
                col = b_el.get(f"{{{W_URI}}}color", "000000")
                info["borders"][side] = (sz, col)
    return info


def emit_paragraph(p_el: etree._Element, doc: Document, img_dir: Path, img_counter: list[int], in_cell: bool = False) -> str:
    content, _ = render_paragraph_children(p_el, doc, img_dir, img_counter)
    props = parse_para_props(p_el)
    if not content.strip() and not props["fill"] and not props["borders"]:
        return "" if in_cell else f"#v({max(2.0, props['after_pt']):.1f}pt)"

    inner = content
    if props["indent_pt"] > 0 and props["align"] == "left":
        inner = f"#h({props['indent_pt']:.1f}pt){inner}"
    if props["align"] == "center":
        inner = f"#align(center)[{inner}]"
    elif props["align"] == "right":
        inner = f"#align(right)[{inner}]"

    if in_cell:
        return inner

    block_args = ["width: 100%"]
    block_args.append(f"above: {max(1.5, props['before_pt'] + 1.5):.1f}pt")
    block_args.append(f"below: {max(2.0, props['after_pt'] + 1.5):.1f}pt")

    if props["fill"]:
        block_args.append(f'fill: rgb("#{props["fill"]}")')

    if props["borders"]:
        stroke_parts = []
        for side, (sz_pt, col) in props["borders"].items():
            stroke_parts.append(f'{side}: {sz_pt:.2f}pt + rgb("#{col}")')
        block_args.append(f"stroke: ({', '.join(stroke_parts)})")

    if props["fill"] or props["borders"]:
        inset_parts = []
        if "left" in props["borders"]:
            inset_parts.append("left: 7pt")
        else:
            inset_parts.append("left: 5pt")
        inset_parts.extend(["right: 5pt", "top: 4.5pt", "bottom: 4.5pt"])
        block_args.append(f"inset: ({', '.join(inset_parts)})")
        if props["fill"] == "DEEAF6":
            # 章节标题与紧随段保持同页不断行
            block_args.append("sticky: true")

    block = f"#block({', '.join(block_args)})[{inner}]"
    return ("#pagebreak()\n" if props["page_break_before"] else "") + block


def emit_table(tbl_el: etree._Element, doc: Document, img_dir: Path, img_counter: list[int], usable_in: float) -> str:
    rows = tbl_el.findall(f"{{{W_URI}}}tr")
    if not rows:
        return ""
    first_cells = rows[0].findall(f"{{{W_URI}}}tc")
    raw_widths = []
    for tc in first_cells:
        tcPr = tc.find(f"{{{W_URI}}}tcPr")
        tcW = tcPr.find(f"{{{W_URI}}}tcW") if tcPr is not None else None
        w_dxa = int(tcW.get(f"{{{W_URI}}}w", "1440")) if tcW is not None else 1440
        raw_widths.append(w_dxa / 1440.0)
    total_w = sum(raw_widths) or 1.0
    scale = min(1.0, usable_in / total_w)
    col_spec = ", ".join(f"{w * scale:.3f}in" for w in raw_widths)

    cell_entries: list[str] = []
    for r_el in rows:
        for tc in r_el.findall(f"{{{W_URI}}}tc"):
            tcPr = tc.find(f"{{{W_URI}}}tcPr")
            fill_str = "none"
            if tcPr is not None:
                shd = tcPr.find(f"{{{W_URI}}}shd")
                if shd is not None and shd.get(f"{{{W_URI}}}fill") and shd.get(f"{{{W_URI}}}fill").lower() != "auto":
                    fill_str = f'rgb("#{shd.get(f"{{{W_URI}}}fill")}")'
            p_strs = []
            for p_el in tc.findall(f"{{{W_URI}}}p"):
                ps = emit_paragraph(p_el, doc, img_dir, img_counter, in_cell=True)
                if ps:
                    p_strs.append(ps)
            cell_body = "\n".join(p_strs)
            cell_entries.append(f"  table.cell(fill: {fill_str})[{cell_body}],")

    return (
        f"#align(center)[#table(\n"
        f"  columns: ({col_spec}),\n"
        f"  align: center + horizon,\n"
        f"  inset: (x: 4pt, y: 3.5pt),\n"
        f"  stroke: 0.45pt + rgb(\"#888888\"),\n"
        + "\n".join(cell_entries)
        + "\n)]\n"
    )


def ensure_fonts_and_typst():
    """Use the bundled report fonts; install the small Typst Python binding if needed."""
    try:
        import typst  # type: ignore
    except ImportError as exc:
        raise RuntimeError("PDF export requires the Typst Python package: python -m pip install typst") from exc

    if not FONT_DIR.is_dir() or not KATEX_FONT_DIR.is_dir():
        raise RuntimeError(f"Required bundled fonts are missing: {FONT_DIR}")
    return typst, [str(FONT_DIR), str(KATEX_FONT_DIR)]


def convert_docx_to_pdf(docx_path: Path, pdf_path: Path) -> int:
    typst_mod, font_dirs = ensure_fonts_and_typst()
    doc = Document(str(docx_path))
    sec = doc.sections[0]
    pw_in = sec.page_width.inches
    ph_in = sec.page_height.inches
    mt_in = sec.top_margin.inches
    mb_in = sec.bottom_margin.inches
    ml_in = sec.left_margin.inches
    mr_in = sec.right_margin.inches
    usable_in = pw_in - ml_in - mr_in

    hdr_txt = "".join(p.text for p in sec.header.paragraphs).strip()

    with tempfile.TemporaryDirectory(prefix="docx2pdf_") as tmpdir:
        tmp = Path(tmpdir)
        img_counter = [0]
        body_blocks: list[str] = []

        for child in doc.element.body.iterchildren():
            tag = local(child)
            if tag == "p":
                b = emit_paragraph(child, doc, tmp, img_counter, in_cell=False)
                if b:
                    body_blocks.append(b)
            elif tag == "tbl":
                body_blocks.append(emit_table(child, doc, tmp, img_counter, usable_in))

        header_typ = ""
        if hdr_txt:
            header_typ = f'header: align(center)[#text(size: 7.5pt, fill: rgb("#666666"))[{esc_typst_text(hdr_txt)}]],'

        typ_source = f"""#set page(
  width: {pw_in:.3f}in,
  height: {ph_in:.3f}in,
  margin: (top: {mt_in:.3f}in, bottom: {mb_in:.3f}in, left: {ml_in:.3f}in, right: {mr_in:.3f}in),
  {header_typ}
  footer: align(center)[#text(size: 7.5pt, fill: rgb("#666666"))[#context counter(page).display()]],
)
#set text(
  font: ("KaTeX_Main", "Source Han Serif", "WenQuanYi Micro Hei"),
  size: 9pt,
  lang: "zh",
)
#show math.equation: set text(font: ("New Computer Modern Math", "KaTeX_Main", "Source Han Serif"))
#set par(leading: 1.0em, justify: true) // PDF 采用更宽松的行距，明确体现至少 1.5 倍的视觉效果

""" + "\n\n".join(body_blocks) + "\n"

        typ_file = tmp / "document.typ"
        typ_file.write_text(typ_source, encoding="utf-8")
        pdf_bytes = typst_mod.compile(str(typ_file), font_paths=font_dirs)
        pdf_path.parent.mkdir(parents=True, exist_ok=True)
        pdf_path.write_bytes(pdf_bytes)

    import pymupdf
    with pymupdf.open(str(pdf_path)) as pdf_doc:
        pages = len(pdf_doc)
    print(f"OK: {docx_path.name} -> {pdf_path} ({pdf_path.stat().st_size} bytes, {pages} pages)")
    return pages


def main() -> int:
    src = Path(sys.argv[1]) if len(sys.argv) >= 2 else DEFAULT_DOCX
    dst = Path(sys.argv[2]) if len(sys.argv) >= 3 else src.with_suffix(".pdf")
    convert_docx_to_pdf(src, dst)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
