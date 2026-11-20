#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成 B309《等厚干涉及其应用》完整版实验报告 (.docx)
所有数学公式均由 KaTeX 语法 ($...$ / $$...$$) 经 KaTeX 官方 MathML 引擎转换为 Word 原生 OMML (<m:oMath> / <m:oMathPara>)。
"""
from __future__ import annotations

import json
import pathlib
import re
import subprocess
import zipfile
from lxml import etree
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml

ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "AGENTS.md").is_file())
OUT = ROOT / "大学物理实验/实验项目/实验报告/B309-等厚干涉/实验报告-等厚干涉-完整版.docx"
ASSETS = ROOT / "大学物理实验/实验项目/assets"

M_URI = "http://schemas.openxmlformats.org/officeDocument/2006/math"
W_URI = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NSMAP = {"m": M_URI, "w": W_URI}


def m_el(tag: str, **attrs) -> etree._Element:
    el = etree.Element(f"{{{M_URI}}}{tag}", nsmap=NSMAP)
    for k, v in attrs.items():
        el.set(f"{{{M_URI}}}{k}", v)
    return el


def w_el(tag: str, **attrs) -> etree._Element:
    el = etree.Element(f"{{{W_URI}}}{tag}", nsmap=NSMAP)
    for k, v in attrs.items():
        el.set(f"{{{W_URI}}}{k}", v)
    return el


# ─── KaTeX -> MathML 批量预编译缓存 ───────────────────────────────────────────
KATEX_CACHE: dict[tuple[bool, str], str] = {}


def precompile_katex(texts: list[str]) -> None:
    pattern = re.compile(r"\$\$([\s\S]+?)\$\$|\$([^\$\n]+?)\$")
    jobs: list[tuple[bool, str]] = []
    seen = set()
    for txt in texts:
        for m in pattern.finditer(txt):
            disp = m.group(1) is not None
            tex = (m.group(1) if disp else m.group(2)).strip()
            key = (disp, tex)
            if key not in seen:
                seen.add(key)
                jobs.append(key)
    if not jobs:
        return

    node_script = """
    const fs = require('fs');
    const katex = require('katex');
    const jobs = JSON.parse(fs.readFileSync(0, 'utf8'));
    const out = jobs.map(([disp, tex]) =>
      katex.renderToString(tex, { displayMode: disp, output: 'mathml', throwOnError: true, strict: 'error' })
    );
    process.stdout.write(JSON.stringify(out));
    """
    res = subprocess.run(
        ["node", "-e", node_script],
        input=json.dumps(jobs),
        text=True,
        capture_output=True,
        check=True,
        cwd=ROOT,
    )
    mmls = json.loads(res.stdout)
    for key, mml in zip(jobs, mmls):
        KATEX_CACHE[key] = mml


# ─── MathML DOM -> Word OMML (<m:oMath>) 转换器 ───────────────────────────────
def _local(el: etree._Element) -> str:
    return etree.QName(el).localname


def _make_mr(text: str, style: str | None = None, normal: bool = False, size_pt: float | None = None,
             bold: bool = False, color: str | None = None) -> etree._Element:
    r = m_el("r")
    if normal or style:
        mrPr = m_el("rPr")
        if normal:
            mrPr.append(m_el("nor"))
        if style:
            mrPr.append(m_el("sty", val=style))
        r.append(mrPr)
    wrPr = w_el("rPr")
    rFonts = w_el("rFonts")
    rFonts.set(f"{{{W_URI}}}ascii", "Cambria Math")
    rFonts.set(f"{{{W_URI}}}hAnsi", "Cambria Math")
    rFonts.set(f"{{{W_URI}}}eastAsia", "宋体")
    wrPr.append(rFonts)
    if bold:
        wrPr.append(w_el("b"))
    if size_pt is not None:
        val = str(int(round(size_pt * 2)))
        wrPr.append(w_el("sz", val=val))
        wrPr.append(w_el("szCs", val=val))
    if color:
        wrPr.append(w_el("color", val=color))
    r.append(wrPr)
    mt = m_el("t")
    if text.startswith(" ") or text.endswith(" "):
        mt.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    mt.text = text
    r.append(mt)
    return r


def _wrap_me(nodes: list[etree._Element]) -> etree._Element:
    e = m_el("e")
    for n in nodes:
        e.append(n)
    return e


def _mml_children_to_omml(children: list[etree._Element], fmt: dict) -> list[etree._Element]:
    out: list[etree._Element] = []
    i = 0
    while i < len(children):
        ch = children[i]
        tag = _local(ch)
        # 处理 <munderover>∑ ... </munderover> 把紧随其后的被求和项吸收进 <m:nary><m:e>
        if tag == "munderover" and len(ch) == 3 and "".join(ch[0].itertext()).strip() in ("∑", "∏", "∫"):
            op_txt = "".join(ch[0].itertext()).strip()
            nary = m_el("nary")
            naryPr = m_el("naryPr")
            naryPr.append(m_el("chr", val=op_txt))
            naryPr.append(m_el("limLoc", val="undOvr"))
            nary.append(naryPr)
            sub = m_el("sub")
            for n in _mml_to_omml(ch[1], fmt):
                sub.append(n)
            sup = m_el("sup")
            for n in _mml_to_omml(ch[2], fmt):
                sup.append(n)
            nary.append(sub)
            nary.append(sup)
            # 吸收后续兄弟直到遇到二元加减等号或结束
            body_mml: list[etree._Element] = []
            j = i + 1
            while j < len(children):
                nx = children[j]
                if _local(nx) == "mo" and ("".join(nx.itertext()).strip() in ("=", "+", "−", "-", ",", "≈", "⇒", "⟹")):
                    break
                body_mml.append(nx)
                j += 1
            if body_mml:
                body_nodes = _mml_children_to_omml(body_mml, fmt)
                nary.append(_wrap_me(body_nodes))
                i = j
            else:
                nary.append(_wrap_me([_make_mr(" ", normal=True, **fmt)]))
                i += 1
            out.append(nary)
            continue
        out.extend(_mml_to_omml(ch, fmt))
        i += 1
    return out


def _mml_to_omml(el: etree._Element, fmt: dict) -> list[etree._Element]:
    tag = _local(el)
    if tag == "annotation":
        return []
    if tag in ("span", "math", "semantics", "mrow", "mstyle"):
        return _mml_children_to_omml(list(el), fmt)
    if tag == "mi":
        txt = "".join(el.itertext())
        if not txt:
            return []
        variant = el.get("mathvariant", "")
        is_upright = variant == "normal" or (len(txt) > 1 and txt.isalpha())
        return [_make_mr(txt, style="p" if is_upright else "i", **fmt)]
    if tag == "mn":
        txt = "".join(el.itertext())
        return [_make_mr(txt, style="p", **fmt)] if txt else []
    if tag == "mo":
        txt = "".join(el.itertext())
        return [_make_mr(txt, style="p", **fmt)] if txt else []
    if tag == "mtext":
        txt = "".join(el.itertext()).replace("\u00a0", " ")
        return [_make_mr(txt, normal=True, **fmt)] if txt else []
    if tag == "mspace":
        w = el.get("width", "")
        sp = "  " if ("em" in w and not w.startswith("0.1") and not w.startswith("0.2")) else " "
        return [_make_mr(sp, normal=True, **fmt)]
    if tag == "mfrac" and len(el) == 2:
        f = m_el("f")
        num = m_el("num")
        for n in _mml_to_omml(el[0], fmt):
            num.append(n)
        den = m_el("den")
        for n in _mml_to_omml(el[1], fmt):
            den.append(n)
        f.append(num)
        f.append(den)
        return [f]
    if tag == "msqrt":
        rad = m_el("rad")
        radPr = m_el("radPr")
        radPr.append(m_el("degHide", val="1"))
        rad.append(radPr)
        rad.append(m_el("deg"))
        rad.append(_wrap_me(_mml_children_to_omml(list(el), fmt)))
        return [rad]
    if tag == "msub" and len(el) == 2:
        sSub = m_el("sSub")
        sSub.append(_wrap_me(_mml_to_omml(el[0], fmt)))
        sub = m_el("sub")
        for n in _mml_to_omml(el[1], fmt):
            sub.append(n)
        sSub.append(sub)
        return [sSub]
    if tag == "msup" and len(el) == 2:
        sSup = m_el("sSup")
        sSup.append(_wrap_me(_mml_to_omml(el[0], fmt)))
        sup = m_el("sup")
        for n in _mml_to_omml(el[1], fmt):
            sup.append(n)
        sSup.append(sup)
        return [sSup]
    if tag == "msubsup" and len(el) == 3:
        sSubSup = m_el("sSubSup")
        sSubSup.append(_wrap_me(_mml_to_omml(el[0], fmt)))
        sub = m_el("sub")
        for n in _mml_to_omml(el[1], fmt):
            sub.append(n)
        sup = m_el("sup")
        for n in _mml_to_omml(el[2], fmt):
            sup.append(n)
        sSubSup.append(sub)
        sSubSup.append(sup)
        return [sSubSup]
    if tag == "mover" and len(el) == 2:
        acc_txt = "".join(el[1].itertext()).strip()
        if acc_txt in ("ˉ", "¯", "\u00af", "\u203e", "‾"):
            bar = m_el("bar")
            barPr = m_el("barPr")
            barPr.append(m_el("pos", val="top"))
            bar.append(barPr)
            bar.append(_wrap_me(_mml_to_omml(el[0], fmt)))
            return [bar]
        acc = m_el("acc")
        accPr = m_el("accPr")
        accPr.append(m_el("chr", val=acc_txt or "ˆ"))
        acc.append(accPr)
        acc.append(_wrap_me(_mml_to_omml(el[0], fmt)))
        return [acc]
    if tag == "munderover" and len(el) == 3:
        sSubSup = m_el("sSubSup")
        sSubSup.append(_wrap_me(_mml_to_omml(el[0], fmt)))
        sub = m_el("sub")
        for n in _mml_to_omml(el[1], fmt):
            sub.append(n)
        sup = m_el("sup")
        for n in _mml_to_omml(el[2], fmt):
            sup.append(n)
        sSubSup.append(sub)
        sSubSup.append(sup)
        return [sSubSup]
    return _mml_children_to_omml(list(el), fmt)


def katex_to_omml_element(tex: str, display: bool = False, size_pt: float | None = None,
                          bold: bool = False, color: str | None = None) -> etree._Element:
    mml_str = KATEX_CACHE[(display, tex.strip())]
    root = etree.fromstring(mml_str.encode("utf-8"))
    fmt = {"size_pt": size_pt, "bold": bold, "color": color}
    omath = m_el("oMath")
    for node in _mml_to_omml(root, fmt):
        omath.append(node)
    if display:
        omath_para = m_el("oMathPara")
        omath_para.append(omath)
        return omath_para
    return omath


# ─── Word 段落/表格辅助函数（支持混排中文与 $...$ / $$...$$ KaTeX 公式）─────────
MATH_RE = re.compile(r"\$\$([\s\S]+?)\$\$|\$([^\$\n]+?)\$")


def append_rich_content(p, text: str, size=9, bold=False, color=None, italic=False,
                        font="宋体", en_font="Times New Roman"):
    size *= 1.12  # 保持正文/注释在纸面上的可读字号，同时保留标题层级
    pos = 0
    markdown_bold = False
    for m in MATH_RE.finditer(text):
        if m.start() > pos:
            plain = text[pos:m.start()]
            markdown_bold = _add_text_segment(
                p, plain, size=size, bold=bold, markdown_bold=markdown_bold,
                color=color, italic=italic, font=font, en_font=en_font)
        disp = m.group(1) is not None
        tex = (m.group(1) if disp else m.group(2)).strip()
        omml_el = katex_to_omml_element(
            tex, display=disp, size_pt=size, bold=(bold or markdown_bold), color=color)
        p._p.append(omml_el)
        pos = m.end()
    if pos < len(text):
        _add_text_segment(p, text[pos:], size=size, bold=bold,
                          markdown_bold=markdown_bold, color=color, italic=italic,
                          font=font, en_font=en_font)


def _add_text_segment(p, text: str, size=9, bold=False, markdown_bold=False,
                      color=None, italic=False, font="宋体", en_font="Times New Roman"):
    # Markdown **...** may span several KaTeX runs; carry the emphasis state across segments.
    parts = text.split("**")
    for idx, val in enumerate(parts):
        if idx:
            markdown_bold = not markdown_bold
        if not val:
            continue
        run = p.add_run(val)
        run.font.size = Pt(size)
        run.bold = bold or markdown_bold
        run.italic = italic
        if color:
            run.font.color.rgb = RGBColor.from_string(color)
        run.font.name = font
        rPr = run._element.get_or_add_rPr()
        rFonts = rPr.get_or_add_rFonts()
        rFonts.set(qn("w:eastAsia"), font)
        rFonts.set(qn("w:ascii"), en_font)
        rFonts.set(qn("w:hAnsi"), en_font)
    return markdown_bold


def set_margins(section, top=0.72, bottom=0.72, left=0.78, right=0.78):
    section.top_margin = Inches(top)
    section.bottom_margin = Inches(bottom)
    section.left_margin = Inches(left)
    section.right_margin = Inches(right)
    section.header_distance = Inches(0.28)
    section.footer_distance = Inches(0.28)


def set_cell_border(cell, **kwargs):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcBorders = tcPr.first_child_found_in("w:tcBorders")
    if tcBorders is None:
        tcBorders = parse_xml(f'<w:tcBorders {nsdecls("w")}/>')
        tcPr.append(tcBorders)
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        edge_data = kwargs.get(edge)
        if edge_data:
            tag = f"w:{edge}"
            ele = tcBorders.find(qn(tag))
            if ele is None:
                ele = parse_xml(
                    f'<{tag} {nsdecls("w")} w:val="{edge_data["val"]}" '
                    f'w:sz="{edge_data["sz"]}" w:space="0" w:color="{edge_data["color"]}" />'
                )
                tcBorders.append(ele)
            else:
                for k, v in edge_data.items():
                    ele.set(qn(f"w:{k}"), str(v))


def shade_cell(cell, color):
    shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color}" w:val="clear"/>')
    cell._tc.get_or_add_tcPr().append(shading)


# ─── 文档内容列表（供预编译 KaTeX 后写入）────────────────────────────────────
BLOCKS: list[tuple] = []


def reg_para(text, **kw):
    BLOCKS.append(("para", text, kw))


def reg_eq(tex, **kw):
    BLOCKS.append(("eq", f"$${tex}$$", kw))


def reg_box(text, fill, border_color, text_color, left_sz="6", all_borders=True, align="center", size=9.5, space_before=4, space_after=4, page_break_before=False):
    BLOCKS.append(("box", text, {
        "fill": fill, "border_color": border_color, "text_color": text_color,
        "left_sz": left_sz, "all_borders": all_borders, "align": align,
        "size": size, "space_before": space_before, "space_after": space_after,
        "page_break_before": page_break_before,
    }))


def reg_sec(num, title, en="", page_break_before=False):
    BLOCKS.append(("sec", f"{num}  {title}", {"en": en, "page_break_before": page_break_before}))


def reg_table(headers, rows, col_widths, header_shade="1F4E78", font_size=7.5):
    BLOCKS.append(("table", (headers, rows), {"col_widths": col_widths, "header_shade": header_shade, "font_size": font_size}))


def reg_image(path, width_in=5.0, caption=None, cap_size=7.5):
    BLOCKS.append(("image", str(path), {"width_in": width_in, "caption": caption, "cap_size": cap_size}))


def define_report():
    reg_para("UNIVERSITY PHYSICS LABORATORY  ·  B309", size=8.5, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, color="B58A28", space_after=3, space_before=10)
    reg_para("大学物理实验报告", size=23, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, color="17324D", space_after=1)
    reg_para("等厚干涉及其应用", size=17, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, color="2E75B6", space_after=3)
    reg_para("牛顿环测曲率半径  ·  劈尖测金属箔厚度", size=10.5, align=WD_ALIGN_PARAGRAPH.CENTER, color="607080", space_after=5)
    reg_para("实验 2.22  /  B309", size=9, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, color="B58A28", space_after=7, bottom_rule="D6A83B")

    reg_table(
        ["姓名 / 学号", "班级", "课程 / 教师", "实验编号 / 日期"],
        [["孙承泽  ·  2253710052", "能动强基2501", "大学物理实验 I-2  ·  刘瑞丰", "B309  ·  2026-10-31"]],
        col_widths=[1.65, 1.45, 2.05, 1.5],
        header_shade="EAF1F6",
        font_size=8.2,
    )
    reg_para("测量结果速览  /  Results at a glance", size=8.5, bold=True, color="17324D", space_before=8, space_after=2)
    reg_table(
        ["牛顿环  ·  曲率半径 $R$", "劈尖  ·  金属箔厚度 $D$"],
        [["$R = (1014.4 \\pm 6.4)\\text{ mm}$", "$D = (23.2 \\pm 1.1)\\ \\mu\\text{m}$"],
         ["$E_R = 0.63\\%$  ·  $k=1$", "$E_D = 4.8\\%$  ·  $k=1$"]],
        col_widths=[3.3, 3.3], header_shade="17324D", font_size=10,
    )
    reg_para("数据处理以转录的原始显微镜读数为准；原始读数未改写，所有差值及派生量均据此复核。",
             size=8.2, color="607080", italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=4)
    reg_para("依据《大学物理实验（第三版）》实验 2.22（印刷页 219–224）  ·  钠光 $\\lambda = 589.3\\text{ nm}$  ·  测微鼓轮分度值 $0.01\\text{ mm}$",
             size=8, align=WD_ALIGN_PARAGRAPH.CENTER, color="607080", space_after=6)

    # 一、实验目的
    reg_sec("一、", "实验目的", "Objectives")
    reg_para("1. 观察牛顿环同心圆与劈尖平行直条纹，认识分振幅薄膜干涉中的半波损失现象；", size=9.5, space_after=3)
    reg_para("2. 掌握读数显微镜调节与单向测量法，用牛顿环逐差法测定平凸透镜曲率半径；", size=9.5, space_after=3)
    reg_para("3. 比较劈尖总暗纹计数与条纹间距两种测箔厚方法，并完成不确定度评定。", size=9.5, space_after=4)
    reg_image(ASSETS / "B309-图-等厚干涉几何示意.png", width_in=6.4,
              caption="图 1  牛顿环等厚线与空气劈尖参数示意（结构与比例均为示意，不代表实测装置）。", cap_size=8)
    reg_para("数据处理路径", size=8.5, bold=True, color="17324D", space_before=3, space_after=2)
    reg_table(["01 读数", "02 逐差", "03 统计", "04 表示"],
              [["原始值照录", "$u_k$、$l_k$", "$s$ 与传递", "$R$、$D$ ± $s$"],
               ["不改写输入", "消去固定项", "$k=1$ 标准不确定度", "保留单位与有效位"]],
              col_widths=[1.62, 1.62, 1.62, 1.62], header_shade="EAF1F6", font_size=7.8)
    reg_para("判据：$R$ 取五级逐差法；箔厚 $D$ 以平均条纹间距法为主，$N=70$ 计数值仅作对照。", size=7.8, color="607080", italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=1)
    reg_para("复核边界：手写原始记录影像未提供；本版仅复核转录读数的算术一致性，不声称逐位核验手写原件。", size=7.8, color="607080", italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=1, space_after=1)
    reg_para("阅读导引：§2 仪器与方法 → §3 原始读数、回归交叉核验与不确定度 → §4 结论 → §5 思考题。", size=8, color="607080", italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=1, space_after=1)
    reg_para("图表为基于转录读数重绘的分析图，并非原始记录影像；原始读数与计算派生量分列，便于追溯。", size=7.8, color="607080", italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=2)
    reg_para("全文保留原始读数；图表标题均置于图注，回归线仅作独立一致性检查，主结果仍按指定逐差法计算。", size=7.8, color="607080", italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=2)

    # 二、实验仪器与实验方法（精简版：仅仪器+方法+一句原理+图2-135）
    reg_sec("二、", "实验仪器与实验方法", "Apparatus & Method", page_break_before=True)
    reg_para("**实验仪器：**读数显微镜（含测微鼓轮 $0.01\\text{ mm}$、十字叉丝、载物台，$41\\times$ 显微镜头）、钠光灯（$\\lambda = 589.3\\text{ nm}$）、牛顿环装置（平凸透镜待测 $R \\approx 1\\text{ m}$＋平板玻璃）、劈尖装置（两光学平板一端垫待测金属箔）、$45^\\circ$ 半反玻璃片 $\\text{M}$、金属箔、擦镜纸。", size=9, space_after=2)
    reg_para("**实验方法与步骤（按课本 p221–222，钠光 $\\lambda = 589.3\\text{ nm}$，逐差法 $m = 5$）：**① 调节：$\\text{M}$ 镜 $45^\\circ$ 对钠光、反光镜转开不遮光，叉丝调至垂直于载物台移动方向，镜筒调焦至视场清晰（牛顿环为同心圆、劈尖为等间距直条纹）；② 牛顿环：单向测 $6\\sim 15$ 级左右读数，求直径 $d_k$；③ 劈尖：数总暗纹级数 $N$，每隔 $10$ 条读 $n_k$ 求 $l_k$ 与 $\\bar{s}$，另测三次 $L$ 求 $\\bar{L}$；全程单向移动，转过头须退回多级重测。", size=9.5, space_after=4)
    reg_table(
        ["观察项目", "读数与质量控制"],
        [["牛顿环", "暗环清晰后单向读 $6\\sim15$ 级两侧位置；叉丝对准同一暗环，中心穿越后仍保持同向。"],
         ["劈尖", "确认暗纹平行；每隔 $10$ 条读数求 $l_k$，另独立测量 $L$ 三次。"],
         ["数据", "原始读数照录；改变移动方向后退回多级再测，派生值只由原始读数计算。"]],
        col_widths=[1.25, 5.25], header_shade="17324D", font_size=8.3,
    )
    reg_para("处理模型与适用条件（$\\lambda = 589.3\\text{ nm} = 0.0005893\\text{ mm}$）：", size=8.2, bold=True, color="17324D", space_before=3, space_after=1)
    reg_eq(r"d_k^2 = 4R\lambda k + C, \qquad R = \frac{d_{k+5}^2-d_k^2}{20\lambda} = \frac{u_k}{20\lambda}", size=8.6)
    reg_eq(r"D_N = N\frac{\lambda}{2}, \qquad \alpha \approx \frac{D}{L}, \quad s \approx \frac{\lambda}{2\alpha} \implies D \approx \frac{L}{s}\frac{\lambda}{2}", size=8.6)
    reg_para("牛顿环平方差消去接触点常数 $C$；劈尖计数式仅作对照，厚度主结果采用实测平均条纹间距与长度。$20\\lambda = 0.011786\\text{ mm}$。", size=7.8, color="595959", italic=True, space_after=3)
    reg_image(ASSETS / "B309-图2-135显微镜观测-裁切.png", width_in=2.7, caption="图 2-135  读数显微镜＋45°半反镜 M 观测光路（方法调节用）")

    # 三、测量内容及数据处理
    reg_sec("三、", "测量内容及数据处理", "Measurement & Data Reduction", page_break_before=True)
    reg_para("3.1 原始读数与派生数据（原始实测读数保留，派生量按读数复算）：", size=8.5, bold=True, color="1F4E78", space_after=3)
    reg_para("**复核说明：**保留表中所有原始显微镜读数不变；原稿若干派生数与这些读数相减/平方不一致，本版按原始读数复算。差值校验为：牛顿环 $14.623-9.907=4.716$、$14.510-10.038=4.472$、$14.224-10.317=3.907$、$5.652^2=31.945$；劈尖 $34.621-19.370=15.251$、$33.452-0.000=33.452$。表内派生量显示至 $0.001$，统计计算使用未舍入值。", size=7.5, color="595959", italic=True, space_after=3)
    reg_para("表 2-22-1  平凸透镜曲率半径 $R$ 的测量（钠光 $\\lambda = 589.3\\text{ nm}$，$m = 5$，单位 $\\text{mm}$）", size=9, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, color="1F4E78", space_after=2)
    headers1 = ["级数 $k$", "初读数 $/\\text{mm}$", "末读数 $/\\text{mm}$", "$d_k = \\lvert x_{\\text{末}} - x_{\\text{初}} \\rvert\\ /\\text{mm}$", "$d_k^2\\ /\\text{mm}^2$", "$u_k = d_{k+5}^2 - d_k^2\\ /\\text{mm}^2$"]
    rows1 = [
        ["$15$", "$15.187$", "$9.342$", "$5.845$", "$34.164$", "$u_{10} = 11.923$"],
        ["$14$", "$15.101$", "$9.449$", "$5.652$", "$31.945$", "$u_9 = 11.946$"],
        ["$13$", "$14.979$", "$9.551$", "$5.428$", "$29.463$", "$u_8 = 12.241$"],
        ["$12$", "$14.869$", "$9.666$", "$5.203$", "$27.071$", "$u_7 = 11.807$"],
        ["$11$", "$14.758$", "$9.796$", "$4.962$", "$24.621$", "$u_6 = 11.862$"],
        ["$10$", "$14.623$", "$9.907$", "$4.716$", "$22.241$", "$\\bar{u} = 11.956$"],
        ["$9$", "$14.510$", "$10.038$", "$4.472$", "$19.999$", ""],
        ["$8$", "$14.315$", "$10.165$", "$4.150$", "$17.223$", ""],
        ["$7$", "$14.224$", "$10.317$", "$3.907$", "$15.265$", ""],
        ["$6$", "$14.049$", "$10.477$", "$3.572$", "$12.759$", ""],
    ]
    reg_table(headers1, rows1, col_widths=[0.6, 0.98, 0.98, 1.45, 0.95, 1.55], header_shade="1F4E78", font_size=7.5)
    reg_para("注：初、末读数为原始实测值，本表 $d_k$、$d_k^2$、$u_k$ 均由这些读数复算；计算使用未舍入的差值与平方，表中显示至 $0.001$。例如 $u_{10}=5.845^2-4.716^2=11.923369$、$u_9=5.652^2-4.472^2=11.946320$；$\\bar{u}=11.9558386\\text{ mm}^2\\approx11.956\\text{ mm}^2$。",
             size=7.2, color="595959", italic=True, space_after=3)
    reg_image(ASSETS / "B309-图-牛顿环d²-k线性拟合.png", width_in=6.2,
              caption="图 2  牛顿环 $d_k^2$—级数 $k$ 线性回归交叉核验（点为表 2-22-1 原始读数的平方，线为最小二乘拟合）。", cap_size=7.8)
    reg_para("十组读数拟合斜率 $a=2.38914\\text{ mm}^2/\\text{级}$，$R^2=0.999716$；按 $a=4R\\lambda$ 得 $R_{\\rm fit}=1.01355\\text{ m}$，与逐差主结果 $1.0144\\text{ m}$ 相差约 $0.08\\%$。该回归仅作独立一致性检查，报告主结果仍采用五级逐差法。", size=8, color="607080", italic=True, space_after=4)

    reg_para("表 2-22-2  金属箔厚度 $D$ 的测量（劈尖，现场数得暗纹总级数 $N = 70$）", size=10, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, color="17324D", space_after=5, space_before=12, page_break_before=True)
    reg_para("劈尖暗纹级数 $N = 70$ 级　　上段：逐差法求相邻暗纹间距 $\\bar{s}$", size=8, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
    headers2a = ["级数 $k$", "读数 $n_k\\ /\\text{mm}$", "$l_k = \\lvert n_{k+40} - n_k \\rvert\\ /\\text{mm}$", "统计"]
    rows2a = [
        ["$0$", "$49.475$", "$19.026$", "$40$ 条间距"],
        ["$10$", "$44.128$", "$17.572$", ""],
        ["$20$", "$39.115$", "$16.260$", ""],
        ["$30$", "$34.621$", "$15.251$", ""],
        ["$40$", "$30.449$", "$\\bar{l} = 17.027$", "$4$ 个 $l_k$ 平均"],
        ["$50$", "$26.556$", "—", "—"],
        ["$60$", "$22.855$", "—", "—"],
        ["$70$", "$19.370$", "—", "—"],
        ["$80$", "—", "—", "—"],
    ]
    reg_table(headers2a, rows2a, col_widths=[0.7, 1.3, 2.3, 1.5], header_shade="548235", font_size=7.5)
    reg_para("$\\bar{l} = \\frac{19.026 + 17.572 + 16.260 + 15.251}{4} = 17.02725\\text{ mm}\\approx17.027\\text{ mm}$，$\\bar{s} = \\frac{\\bar{l}}{40} = 0.425681\\text{ mm}\\approx0.4257\\text{ mm}$；四个 $l_k$ 呈单调递减（$19.026 \\to 15.251\\text{ mm}$），反映劈尖楔角非完全均匀。",
             size=7.2, color="595959", italic=True, space_after=4)

    reg_para("下段：劈尖长度 $L$（$50$ 级处）", size=8, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
    headers2b = ["组别 $i$", "$n_{0i}\\ /\\text{mm}$", "$n_i\\ /\\text{mm}$", "$L_i = \\lvert n_i - n_{0i} \\rvert\\ /\\text{mm}$"]
    rows2b = [
        ["$1$", "$0.000$", "$33.452$", "$33.452$"],
        ["$2$", "$-0.065$", "$33.455$", "$33.520$"],
        ["$3$", "$0.000$", "$33.585$", "$33.585$"],
        ["平均", "—", "—", "$\\bar{L} = 33.519\\text{ mm}$"],
    ]
    reg_table(headers2b, rows2b, col_widths=[0.9, 1.5, 1.5, 1.9], header_shade="548235", font_size=7.5)
    reg_para("三次长度均由原始读数相减：$L_1=33.452-0.000=33.452\\text{ mm}$，$L_2=33.455-(-0.065)=33.520\\text{ mm}$，$L_3=33.585-0.000=33.585\\text{ mm}$；$\\bar{L}=33.519\\text{ mm}$。",
             size=7.2, color="595959", italic=True, space_after=3)
    reg_image(ASSETS / "B309-图-劈尖间距l_k.png", width_in=6.2,
              caption="图 3  劈尖四个逐差量 $l_k$ 及其均值；阴影表示 $\\pm s(l_k)$，数据源为表 2-22-2。", cap_size=7.8)
    reg_para("四个观测段的逐差量单调递减，图示离散范围亦体现楔角的非均匀性；厚度主结果据四段平均值计算。", size=8, color="607080", italic=True, space_after=3)

    # 课本表格扫描留在 assets 供核对；报告正文只保留清晰排印的实测表，避免重复展示教材空白模板。

    # 3.2 数据处理与不确定度
    reg_para("3.2 数据处理与不确定度（$k = 1$，不计 $\\lambda$ 误差）", size=11, bold=True, color="17324D", space_before=4, space_after=6, page_break_before=True)

    reg_para("（1）牛顿环求 $R$（逐差法，$m = 5$）", size=9, bold=True, space_after=2, space_before=2)
    reg_para("由等厚干涉暗纹条件 $\\delta = 2e_k + \\frac{\\lambda}{2} = (2k+1)\\frac{\\lambda}{2}$ 及几何关系 $e_k \\approx \\frac{r_k^2}{2R} = \\frac{d_k^2}{8R}$，采用逐差法（$m = 5$）消去接触点附加厚度，得式 (2.22.4)：", size=9, space_after=2, indent=18)
    reg_eq(r"R = \frac{d_{k+m}^2 - d_k^2}{4m\lambda} = \frac{d_{k+5}^2 - d_k^2}{20\lambda} = \frac{u_k}{20\lambda}", size=9)
    reg_para("由表 2-22-1 得 $\\bar{u}=11.9558386\\text{ mm}^2$。表中列出未舍入差值与均值偏差，便于复核样本标准差：", size=9, space_after=2, indent=18)
    reg_table(["$k$", "$u_k$（mm²）", "$u_k-\\bar{u}$（mm²）", "$(u_k-\\bar{u})^2$（mm⁴）"],
              [["6", "11.862260", "−0.093579", "0.008757"],
               ["7", "11.806560", "−0.149279", "0.022284"],
               ["8", "12.240684", "+0.284845", "0.081137"],
               ["9", "11.946320", "−0.009519", "0.000091"],
               ["10", "11.923369", "−0.032470", "0.001054"],
               ["Σ", "—", "—", "0.113323"]],
              col_widths=[0.6, 1.35, 1.6, 1.75], header_shade="EAF1F6", font_size=7.6)
    reg_eq(r"s(u_k) = \sqrt{\frac{0.11332}{4}} = 0.1683\text{ mm}^2, \qquad s_{\bar{u}} = \frac{s(u_k)}{\sqrt{5}} = 0.07527\text{ mm}^2", size=9)
    reg_para("代入 $20\\lambda = 0.011786\\text{ mm}$，得曲率半径平均值及其标准不确定度、相对不确定度：", size=9, space_after=2, indent=18)
    reg_eq(r"\bar{R} = \frac{\bar{u}}{20\lambda} = \frac{11.95584}{0.011786} = 1014.4\text{ mm} = 1.0144\text{ m}, \quad s_R = \frac{s_{\bar{u}}}{20\lambda} = 6.39\text{ mm}, \quad E_R = \frac{s_R}{\bar{R}} = 0.63\%", size=9)
    reg_box("结果：  $R = (1.0144 \\pm 0.0064)\\text{ m} = (1014.4 \\pm 6.4)\\text{ mm}$　　（$E_R = 0.63\\%$，$k = 1$）",
            fill="FFF2CC", border_color="D6A83B", text_color="7F6003", size=9.5, space_before=3, space_after=4)
    reg_image(ASSETS / "B309-图-牛顿环逐差量u_k.png", width_in=6.4,
              caption="图 4  牛顿环逐差量 $u_k$ 的离散；阴影表示 $\\pm s(u_k)$，数据源为表 2-22-1。", cap_size=8)
    reg_para("与课本标称约 $1.0\\text{ m}$ 符合；若取包含因子 $k = 2$，$U = 2s_R \\approx 12.8\\text{ mm}$，则 $R = (1.014 \\pm 0.013)\\text{ m}$。", size=8.5, color="607080", italic=True, space_after=2)

    reg_para("（2）劈尖求 $D$（两式对照，以 (2.22.6) 式为准）", size=10, bold=True, color="17324D", space_after=5, space_before=4, page_break_before=True)
    reg_para("总暗纹计数式 (2.22.5)（仅计数，不计误差，作对照）：$D_N = N\\cdot\\frac{\\lambda}{2} = 70 \\times \\frac{0.0005893}{2} = 0.0206\\text{ mm} = 20.6\\ \\mu\\text{m}$。", size=9, space_after=2, indent=18)
    reg_para("条纹间距式 (2.22.6)：代入 $\\bar{s} = 0.4257\\text{ mm}$、$\\bar{L} = 33.519\\text{ mm}$，得：", size=9, space_after=2, indent=18)
    reg_eq(r"D = \frac{\bar{L}}{\bar{s}}\cdot\frac{\lambda}{2} = \frac{33.519}{0.4257}\times\frac{0.0005893}{2} = 0.0232\text{ mm} = 23.2\ \mu\text{m}", size=9)
    reg_para("不确定度传递与合成：$4$ 个 $l_k$ 的标准偏差 $s(l_k) = \\sqrt{\\frac{\\sum(l_k - \\bar{l})^2}{3}} = 1.6366\\text{ mm}$，故 $s_{\\bar{l}} = \\frac{s(l_k)}{\\sqrt{4}} = 0.8183\\text{ mm}$，$E_{\\bar{l}} = 4.806\\%$；$3$ 个 $L_i$ 的标准偏差 $s(L_i) = 0.06651\\text{ mm}$，故 $s_{\\bar{L}} = \\frac{s(L_i)}{\\sqrt{3}} = 0.03840\\text{ mm}$，$E_{\\bar{L}} = 0.1146\\%$。方和根合成：", size=9, space_after=2, indent=18)
    reg_eq(r"E_D = \sqrt{E_{\bar{l}}^2 + E_{\bar{L}}^2} = 4.807\%, \qquad s_D = E_D \cdot D = 0.001115\text{ mm} \approx 1.1\ \mu\text{m}", size=9)
    reg_box("结果：  $D = (0.0232 \\pm 0.0011)\\text{ mm} = (23.2 \\pm 1.1)\\ \\mu\\text{m}$　　（$E_D = 4.8\\%$，$k = 1$）",
            fill="EAF3E6", border_color="6C914D", text_color="375C1E", size=9.5, space_before=3, space_after=3)
    reg_para("以 (2.22.6) 式为准；(2.22.5) 式偏小约 $11\\%$，因所数 $N = 70$ 未达垫片边缘且 $\\bar{s}$ 轻微非均匀（$\\frac{\\bar{L}}{\\bar{s}} \\approx 78.74$，末条距边缘尚约 $9$ 条间距）。若 $N$ 正好到边缘且劈尖均匀，两式结果一致。",
             size=7.5, color="595959", italic=True, space_after=5, indent=18)

    # 四、小结
    reg_sec("四、", "小结（结论、误差分析及建议）", "Summary")
    reg_para("**结论：**牛顿环逐差法测得平凸透镜曲率半径 $R = (1014.4 \\pm 6.4)\\text{ mm} = (1.0144 \\pm 0.0064)\\text{ m}$（$E_R = 0.63\\%$），与课本标称约 $1.0\\text{ m}$ 符合；劈尖以 $\\frac{\\bar{L}}{\\bar{s}}\\cdot\\frac{\\lambda}{2}$ 法测得金属箔厚度 $D = (23.2 \\pm 1.1)\\ \\mu\\text{m}$（$E_D = 4.8\\%$），对照计数式 $D_N = 20.6\\ \\mu\\text{m}$ 偏小 $2.6\\ \\mu\\text{m}$，反映末条暗纹距薄端边缘尚约 $9$ 条间距，验证了两式的适用条件。", size=9, space_after=2)
    reg_para("**误差分析：**$R$ 的 $0.63\\%$ 主要为 $5$ 个 $u_k$ 的随机分散（$s(u_k) = 0.1683\\text{ mm}^2$），源于读数显微镜 $0.01\\text{ mm}$ 读数估读与十字叉丝对准误差；全程单向移动已抑制回程差，逐差法已消除中心接触点附加光程差。$D$ 的 $4.8\\%$ 几乎全来自 $\\bar{s}$（即 $\\bar{l}$）的 $4.806\\%$（$l_k$ 从 $19.026 \\to 15.251\\text{ mm}$ 系统递减），$\\bar{L}$ 仅 $0.115\\%$ 可忽略，说明劈尖平板微弯或接触处压紧不均使楔角 $\\alpha$ 随位置缓变（若均匀则 $4$ 个 $l_k$ 应在 $17.0\\text{ mm}$ 附近一致）。", size=9, space_after=2)
    reg_para("**建议：**① 牛顿环对准时使叉丝严格切于暗环正中弦位并估读至 $0.001\\text{ mm}$；② 劈尖测 $s$ 避开两端受压边缘段，或增至 $5\\sim 9$ 段平均以抑制楔角缓变；③ 长度 $L$ 用同一显微镜单向三次独立定端，减小端点判读误差。", size=9, space_after=4)
    reg_para("结果与主要不确定度来源", size=8.5, bold=True, color="17324D", space_before=2, space_after=2)
    reg_table(["测量量", "报告结果（$k=1$）", "主要影响项"],
              [["曲率半径 $R$", "$(1.0144\\pm0.0064)\\text{ m}$；$E_R=0.63\\%$", "$u_k$ 的随机离散"],
               ["金属箔厚 $D$", "$(23.2\\pm1.1)\\mu\\text{m}$；$E_D=4.8\\%$", "$l_k$ 随位置递减，楔角非均匀"]],
              col_widths=[1.35, 2.55, 2.6], header_shade="EAF1F6", font_size=7.7)
    reg_para("评分点核对（总分 10 分）", size=8.5, bold=True, color="17324D", space_before=3, space_after=2)
    reg_table(["评分项", "分值", "报告定位"],
              [["格式与量纲", "2", "全文；数据表与公式"],
               ["$R$ 计算", "3", "§3；逐差法及不确定度"],
               ["$D$ 计算", "3", "§3；两法对照及误差合成"],
               ["思考题 2", "1", "§5；中心亮斑证明"],
               ["小结", "1", "§4；结论、误差与建议"],
               ["合计", "10", "—"]],
              col_widths=[1.4, 0.65, 4.45], header_shade="17324D", font_size=7.5)

    # 五、实验思考题
    reg_sec("五、", "实验思考题（重点：思考题2 为评分1分题，课本p224第2题）", "Exercises", page_break_before=True)
    reg_para("按课本 p224 七题中选三作答，按计算与证明题标准分步推导；题干以灰字抄录便于核分。评分：格式 2 分、$R$ 计算 3 分、$D$ 计算 3 分、思考题 2 占 1 分、小结 1 分。",
             size=7.2, color="595959", italic=True, space_after=4)

    reg_para("思考题1（p224-1：平板局部凸起导致的牛顿环形变）",
             size=8, color="595959", italic=True, space_after=1, space_before=2)
    reg_para("答：同级 $k$ 暗环对应固定空气膜厚度 $e_k = k\\frac{\\lambda}{2}$（中心最薄，向外按 $e = \\frac{r^2}{2R}$ 增厚）。当平板玻璃局部凸起 $\\Delta e > 0$ 时，该处空气膜减薄，原半径 $r_k$ 处实际空气隙减为 $\\frac{r_k^2}{2R} - \\Delta e < e_k$；为维持同级暗纹厚度 $e_k$（光程差 $\\delta = 2e_k + \\frac{\\lambda}{2} = (2k+1)\\frac{\\lambda}{2}$ 不变），条纹须移向外侧更厚处，满足 $\\frac{r'^2}{2R} - \\Delta e = \\frac{r_k^2}{2R}$，即 $r' = \\sqrt{r_k^2 + 2R\\Delta e} > r_k$，故该处牛顿环背离中心**局部外凸**（反之若局部凹陷则向中心内凹）。",
             size=9, space_after=4, indent=18)

    reg_box("思考题2（p224-2，评分1分：牛顿环中心亮斑及其对 $R$ 测量的影响）",
            fill="FFF2CC", border_color="BF9000", text_color="7F6003", all_borders=False, align="left", size=9, space_before=4, space_after=2, page_break_before=False)
    reg_para("答：**原因：**接触点夹有微尘或未压紧时存在附加空气隙 $e_0 > 0$，中心光程差 $\\delta_0 = 2e_0 + \\frac{\\lambda}{2}$；当满足明纹条件 $2e_0 + \\frac{\\lambda}{2} = j\\lambda$（如 $e_0 = \\frac{\\lambda}{4}$）时中心即为亮斑。**影响及证明：**对逐差法测 $R$ **无影响**（仅对单环式 $r_k^2 = kR\\lambda$ 有系统误差）。设附加厚度为 $e_0$，第 $k$ 级暗环处总厚度 $e_k' = \\frac{r_k^2}{2R} + e_0$，代入暗纹条件：",
             size=9, space_after=2, indent=18)
    reg_eq(r"2\left(\frac{r_k^2}{2R} + e_0\right) + \frac{\lambda}{2} = (2k + 1)\frac{\lambda}{2} \implies r_k^2 = (k\lambda - 2e_0)R", size=9)
    reg_para("对第 $k+m$ 级暗环同理有 $r_{k+m}^2 = [(k+m)\\lambda - 2e_0]R$，两式相减消去附加项 $2e_0 R$ 并改用直径 $d_k = 2r_k$：", size=9, space_after=2, indent=18)
    reg_eq(r"r_{k+m}^2 - r_k^2 = mR\lambda \implies R = \frac{r_{k+m}^2 - r_k^2}{m\lambda} = \frac{d_{k+m}^2 - d_k^2}{4m\lambda}", size=9)
    reg_para("可见常数附加厚度 $e_0$ 在平方差中完全抵消，本实验采用 $m = 5$ 逐差式 $R = \\frac{\\bar{u}}{20\\lambda}$，故中心亮斑不影响 $R$ 的测量结果。", size=9, space_after=4, indent=18)

    reg_para("思考题3（p224-3：牛顿环条纹疏密与级数的关系）",
             size=8, color="595959", italic=True, space_after=1, space_before=2)
    reg_para("答：由 $r_k = \\sqrt{kR\\lambda}$ 得相邻两级暗环半径差 $\\Delta r_k = r_{k+1} - r_k = \\frac{r_{k+1}^2 - r_k^2}{r_{k+1} + r_k} = \\frac{R\\lambda}{r_{k+1} + r_k} \\approx \\frac{1}{2}\\sqrt{\\frac{R\\lambda}{k}} \\propto \\frac{1}{\\sqrt{k}}$，随级数 $k$ 增大而减小，故外密内疏；而劈尖倾角 $\\alpha$ 恒定，间距 $s = \\frac{\\lambda}{2\\alpha}$ 为常数，故呈等距直条纹。",
             size=9, space_after=4, indent=18)

    reg_box("附录  原始记录与数据复核说明",
            fill="F2F2F2", border_color="D9D9D9", text_color="595959", all_borders=False, left_sz="0", align="center", size=7.2, space_before=6, space_after=2)
    reg_para("原始手写记录影像目前未提供，因此本次仅复核转录读数的算术一致性，未逐位核验手写原件；报告数据来源为用户提供的转录读数。",
             size=8, color="607080", italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=6)


def build_docx():
    define_report()

    # 收集所有含数学公式的字符串并一次性通过 KaTeX 编译
    all_strings: list[str] = []
    for kind, payload, kw in BLOCKS:
        if kind in ("para", "eq", "box"):
            all_strings.append(payload)
        elif kind == "table":
            headers, rows = payload
            all_strings.extend(headers)
            for row in rows:
                all_strings.extend(row)
        elif kind == "image" and kw.get("caption"):
            all_strings.append(kw["caption"])
    precompile_katex(all_strings)

    doc = Document()

    style = doc.styles["Normal"]
    style.font.name = "宋体"
    style._element.rPr.rFonts.set(qn("w:eastAsia"), "宋体")
    style.font.size = Pt(10.2)
    style.paragraph_format.line_spacing = 1.5
    style.paragraph_format.space_after = Pt(5)

    for sec in doc.sections:
        set_margins(sec)
        sec.page_height = Inches(11.69)
        sec.page_width = Inches(8.27)

    section = doc.sections[0]
    hp = section.header.paragraphs[0]
    hp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = hp.add_run("大学物理实验 I-2  ·  B309 等厚干涉及其应用  ·  实验 2.22")
    r.font.size = Pt(8)
    r.font.color.rgb = RGBColor(0x60, 0x70, 0x80)
    r.font.name = "宋体"
    r._element.rPr.rFonts.set(qn("w:eastAsia"), "宋体")
    r._element.rPr.rFonts.set(qn("w:ascii"), "Times New Roman")
    hp._p.get_or_add_pPr().append(parse_xml(
        f'<w:pBdr {nsdecls("w")}><w:bottom w:val="single" w:sz="4" w:space="3" w:color="D6A83B"/></w:pBdr>'
    ))

    fp = section.footer.paragraphs[0]
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for fld_xml in (
        f'<w:fldChar {nsdecls("w")} w:fldCharType="begin"/>',
        f'<w:instrText {nsdecls("w")} xml:space="preserve"> PAGE </w:instrText>',
        f'<w:fldChar {nsdecls("w")} w:fldCharType="end"/>',
    ):
        rr = fp.add_run()
        rr.font.size = Pt(7.5)
        rr.font.color.rgb = RGBColor(0x66, 0x66, 0x66)
        rr.font.name = "Times New Roman"
        rr._r.append(parse_xml(fld_xml))

    for kind, payload, kw in BLOCKS:
        if kind == "para":
            p = doc.add_paragraph()
            p.paragraph_format.space_after = Pt(kw.get("space_after", 4))
            p.paragraph_format.space_before = Pt(kw.get("space_before", 0))
            p.paragraph_format.line_spacing = kw.get("line_spacing", 1.12)
            p.paragraph_format.widow_control = True
            p.paragraph_format.page_break_before = kw.get("page_break_before", False)
            if kw.get("align") is not None:
                p.alignment = kw["align"]
            if kw.get("indent") is not None:
                p.paragraph_format.first_line_indent = Pt(kw["indent"])
            if kw.get("bottom_rule"):
                pPr = p._p.get_or_add_pPr()
                pPr.append(parse_xml(
                    f'<w:pBdr {nsdecls("w")}><w:bottom w:val="single" w:sz="6" w:space="2" w:color="{kw["bottom_rule"]}"/></w:pBdr>'
                ))
            append_rich_content(
                p, payload,
                size=kw.get("size", 9),
                bold=kw.get("bold", False),
                color=kw.get("color"),
                italic=kw.get("italic", False),
            )

        elif kind == "eq":
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(3)
            append_rich_content(p, payload, size=kw.get("size", 9))

        elif kind == "box":
            p = doc.add_paragraph()
            pPr = p._p.get_or_add_pPr()
            pPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{kw["fill"]}" w:val="clear"/>'))
            bc = kw["border_color"]
            lsz = kw["left_sz"]
            if kw["all_borders"]:
                bdr_xml = (
                    f'<w:pBdr {nsdecls("w")}>'
                    f'<w:left w:val="single" w:sz="{lsz}" w:space="4" w:color="{bc}"/>'
                    f'<w:top w:val="single" w:sz="3" w:space="2" w:color="{bc}"/>'
                    f'<w:bottom w:val="single" w:sz="3" w:space="2" w:color="{bc}"/>'
                    f'<w:right w:val="single" w:sz="3" w:space="2" w:color="{bc}"/>'
                    f'</w:pBdr>'
                )
                pPr.append(parse_xml(bdr_xml))
            elif lsz != "0":
                pPr.append(parse_xml(
                    f'<w:pBdr {nsdecls("w")}><w:left w:val="single" w:sz="{lsz}" w:space="4" w:color="{bc}"/></w:pBdr>'
                ))
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if kw["align"] == "center" else WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(kw["space_before"])
            p.paragraph_format.space_after = Pt(kw["space_after"])
            p.paragraph_format.page_break_before = kw.get("page_break_before", False)
            append_rich_content(p, payload, size=kw["size"], bold=(kw["fill"] != "F2F2F2"),
                                italic=(kw["fill"] == "F2F2F2"), color=kw["text_color"])

        elif kind == "sec":
            p = doc.add_paragraph()
            pPr = p._p.get_or_add_pPr()
            pPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="DEEAF6" w:val="clear"/>'))
            pPr.append(parse_xml(
                f'<w:pBdr {nsdecls("w")}><w:left w:val="single" w:sz="12" w:space="4" w:color="2E75B6"/></w:pBdr>'
            ))
            p.paragraph_format.space_before = Pt(7)
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.page_break_before = kw.get("page_break_before", False)
            p.paragraph_format.keep_with_next = True
            r = p.add_run(f"  {payload}")
            r.bold = True
            r.font.size = Pt(12)
            r.font.color.rgb = RGBColor(0x17, 0x32, 0x4D)
            r.font.name = "宋体"
            r._element.rPr.rFonts.set(qn("w:eastAsia"), "宋体")
            r._element.rPr.rFonts.set(qn("w:ascii"), "Times New Roman")
            if kw.get("en"):
                r2 = p.add_run(f"  {kw['en']}")
                r2.font.size = Pt(7.5)
                r2.font.color.rgb = RGBColor(0x5A, 0x5A, 0x5A)
                r2.italic = True
                r2.font.name = "Times New Roman"

        elif kind == "table":
            headers, rows = payload
            col_widths = kw["col_widths"]
            header_shade = kw["header_shade"]
            fs = kw["font_size"] * 1.23
            table = doc.add_table(rows=1 + len(rows), cols=len(headers))
            table.alignment = WD_TABLE_ALIGNMENT.CENTER
            table.autofit = False
            for i, w in enumerate(col_widths):
                for cell in table.columns[i].cells:
                    cell.width = Inches(w)
            for i, h in enumerate(headers):
                cell = table.cell(0, i)
                cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
                shade_cell(cell, header_shade)
                p = cell.paragraphs[0]
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p.paragraph_format.space_before = Pt(2)
                p.paragraph_format.space_after = Pt(2)
                header_color = "17324D" if header_shade.upper() in {"EAF1F6", "F3F6F9", "E2EFDA"} else "FFFFFF"
                append_rich_content(p, str(h), size=fs, bold=True, color=header_color)
                set_cell_border(
                    cell,
                    top={"val": "single", "sz": "4", "color": "404040"},
                    left={"val": "single", "sz": "4", "color": "404040"},
                    bottom={"val": "single", "sz": "4", "color": "404040"},
                    right={"val": "single", "sz": "4", "color": "404040"},
                )
            for r_i, row in enumerate(rows):
                for c_i, val in enumerate(row):
                    cell = table.cell(r_i + 1, c_i)
                    cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
                    p = cell.paragraphs[0]
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    p.paragraph_format.space_before = Pt(1.5)
                    p.paragraph_format.space_after = Pt(1.5)
                    append_rich_content(p, str(val), size=fs)
                    if r_i % 2 == 1:
                        shade_cell(cell, "F2F2F2")
                    set_cell_border(
                        cell,
                        top={"val": "single", "sz": "3", "color": "999999"},
                        left={"val": "single", "sz": "3", "color": "999999"},
                        bottom={"val": "single", "sz": "3", "color": "999999"},
                        right={"val": "single", "sz": "3", "color": "999999"},
                    )

        elif kind == "image":
            img_path = pathlib.Path(payload)
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(3)
            p.paragraph_format.space_after = Pt(2)
            p.add_run().add_picture(str(img_path), width=Inches(kw["width_in"]))
            if kw.get("caption"):
                cp = doc.add_paragraph()
                cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
                cp.paragraph_format.space_before = Pt(0)
                cp.paragraph_format.space_after = Pt(5)
                append_rich_content(cp, kw["caption"], size=kw["cap_size"], italic=True, color="333333")

    # 最终统一覆盖所有正文、公式、标题及表格段落，避免局部默认值造成行距低于 1.5 倍。
    all_paragraphs = list(doc.paragraphs)
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                all_paragraphs.extend(cell.paragraphs)
    for sec in doc.sections:
        all_paragraphs.extend(sec.header.paragraphs)
        all_paragraphs.extend(sec.footer.paragraphs)
    for paragraph in all_paragraphs:
        paragraph.paragraph_format.line_spacing = 1.5

    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(OUT))

    # 校验 OOXML 结构完整性
    assert zipfile.ZipFile(OUT).testzip() is None
    with zipfile.ZipFile(OUT) as zf:
        xml_root = etree.fromstring(zf.read("word/document.xml"))
        omath_cnt = len(xml_root.findall(f".//{{{M_URI}}}oMath"))
    recheck = Document(str(OUT))
    print(f"OK: {OUT} ({OUT.stat().st_size} bytes, {len(recheck.paragraphs)} paras, {omath_cnt} OMML equations)")


if __name__ == "__main__":
    build_docx()
