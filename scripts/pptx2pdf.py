#!/usr/bin/env python3
"""pptx2pdf.py · 纯 Python 的 PPTX → PDF 转换器（不依赖 LibreOffice/Office）

为什么自研：沙箱无 LibreOffice，apt 源不可达；而课程 PPT 的实际构成是
"整页扫描图(PNG) + 少量 EMF 包裹的位图 + 极少数文本框"，用 python-pptx 读几何、
PyMuPDF 画页面即可高保真还原，不需要通用 Office 渲染引擎。

能力清单：
- 页面尺寸 = 幻灯片尺寸（EMU→pt）；形状按 z-order 叠放；
- 图片形状：PNG/JPG 直接嵌入（含 alpha）；EMF/WMF 中 EMR_STRETCHDIBITS 包裹的
  DIB 位图解包为 JPEG 后嵌入（课程扫描件都是这种）；.wdp（HD Photo 透明层）忽略，
  其 PNG 主图已足够；
- 母版/版式/幻灯片的图片背景（<p:bg><a:blipFill>）铺满整页；
- 文本框/占位符：CJK 内建字体（china-s），支持字号、加粗（双描摹仿粗）、颜色、
  对齐（含母版 titleStyle/bodyStyle 继承）、多段落、自动换行（CJK 按字折行）、
  垂直锚点与内边距；
- 纯色填充的自选图形画矩形（无填充的跳过）。

用法：
    python scripts/pptx2pdf.py 输入.pptx [-o 输出.pdf]
"""
from __future__ import annotations

import argparse
import io
import os
import re
import struct
import zipfile

import pymupdf
from PIL import Image
from pptx import Presentation
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN

EMU2PT = 1.0 / 12700.0


def _zip_name(part) -> str:
    """python-pptx 的 partname 带前导斜杠，zip 内路径不带。"""
    return str(part).lstrip("/")
DEFAULT_MARGIN = {"l": 7.2, "r": 7.2, "t": 3.6, "b": 3.6}  # 0.1in / 0.05in


# ---------------------------------------------------------------- EMF / WMF
def emf_blob_to_jpeg(blob: bytes, quality: int = 90) -> bytes | None:
    """从 EMF 的 EMR_STRETCHDIBITS 记录里取出 DIB 位图并转成 JPEG。"""
    if len(blob) < 88 or struct.unpack_from("<II", blob, 0)[0] != 1:
        return None
    off = 0
    while off + 8 <= len(blob):
        itype, size = struct.unpack_from("<II", blob, off)
        if size < 8 or off + size > len(blob):
            return None
        if itype == 81:  # EMR_STRETCHDIBITS
            v = struct.unpack_from("<20i", blob, off)
            off_bmi, cb_bmi, off_bits, cb_bits = v[12], v[13], v[14], v[15]
            bmi = blob[off + off_bmi: off + off_bmi + cb_bmi]
            bits = blob[off + off_bits: off + off_bits + cb_bits]
            if len(bmi) < 40:
                return None
            comp = struct.unpack_from("<I", bmi, 30)[0]
            if comp not in (0, 3):  # BI_RGB / BI_BITFIELDS
                return None
            bmp = (b"BM" + struct.pack("<IHHI", 14 + len(bmi) + len(bits), 0, 0, 14 + len(bmi))
                   + bmi + bits)
            im = Image.open(io.BytesIO(bmp))
            im.load()
            buf = io.BytesIO()
            im.convert("RGB").save(buf, "JPEG", quality=quality)
            return buf.getvalue()
        if itype == 14:  # EMR_EOF
            return None
        off += size
    return None


# ---------------------------------------------------------------- 背景图
def _part_bg_blip(zf: zipfile.ZipFile, partname: str) -> str | None:
    """返回该 part 的 <p:bg> 图片 media 名（若为 blipFill）。"""
    try:
        xml = zf.read(partname).decode("utf8", "ignore")
    except KeyError:
        return None
    m = re.search(r"<p:bg>.*?</p:bg>", xml, re.S)
    if not m:
        return None
    emb = re.search(r'<a:blip[^>]*r:embed="([^"]+)"', m.group(0))
    if not emb:
        return None
    rels = partname.rsplit("/", 1)[0] + "/_rels/" + partname.rsplit("/", 1)[1] + ".rels"
    try:
        rxml = zf.read(rels).decode("utf8", "ignore")
    except KeyError:
        return None
    for rm in re.finditer(r'Id="([^"]+)"[^>]*Target="([^"]+)"', rxml):
        if rm.group(1) == emb.group(1):
            tgt = rm.group(2)
            if tgt.startswith("../"):
                return "ppt/" + tgt[3:]
            return partname.rsplit("/", 1)[0] + "/" + tgt
    return None


def slide_bg_bytes(zf: zipfile.ZipFile, slide, prs) -> bytes | None:
    """按 幻灯片 → 版式 → 母版 的顺序找图片背景。"""
    layout = slide.slide_layout
    master = layout.slide_master
    for part in (slide.part.partname, layout.part.partname, master.part.partname):
        media = _part_bg_blip(zf, _zip_name(part))
        if media:
            return zf.read(media)
    return None


# ---------------------------------------------------------------- 母版默认字
def master_style_defaults(zf: zipfile.ZipFile, prs) -> dict:
    xml = zf.read(_zip_name(prs.slide_masters[0].part.partname)).decode("utf8", "ignore")
    out = {}
    for key, tag in (("title", "titleStyle"), ("body", "bodyStyle")):
        m = re.search(rf"<p:{tag}>.*?</p:{tag}>", xml, re.S)
        if not m:
            continue
        lvl = re.search(r"<a:lvl1pPr[^>]*>", m.group(0))
        algn = re.search(r'algn="(\w+)"', lvl.group(0)) if lvl else None
        sz = re.search(r'<a:defRPr[^>]*\bsz="(\d+)"', m.group(0))
        out[key] = {
            "size": float(sz.group(1)) / 100 if sz else (44.0 if key == "title" else 18.0),
            "align": (algn.group(1) if algn else "l"),
        }
    return out


ALIGN_MAP = {
    PP_ALIGN.LEFT: 0, PP_ALIGN.CENTER: 1, PP_ALIGN.RIGHT: 2, PP_ALIGN.JUSTIFY: 3,
    None: None,
}
SCHEME_ALIGN = {"l": 0, "ctr": 1, "r": 2, "just": 3, "dist": 3}


# ---------------------------------------------------------------- 文本绘制
def _wrap(font, text, size, max_w):
    lines, cur = [], ""
    for ch in text:
        if ch == " ":
            trial = cur + ch
            if font.text_length(trial, fontsize=size) > max_w and cur:
                lines.append(cur.rstrip())
                cur = ""
            else:
                cur = trial
            continue
        trial = cur + ch
        if font.text_length(trial, fontsize=size) > max_w and cur:
            lines.append(cur)
            cur = ch
        else:
            cur = trial
    if cur.strip():
        lines.append(cur)
    return lines or [""]


def draw_text_frame(page, tf, rect, defaults, font):
    if not tf.text.strip():
        return
    ml = (tf.margin_left if tf.margin_left is not None else 91440) * EMU2PT
    mr = (tf.margin_right if tf.margin_right is not None else 91440) * EMU2PT
    mt = (tf.margin_top if tf.margin_top is not None else 45720) * EMU2PT
    mb = (tf.margin_bottom if tf.margin_bottom is not None else 45720) * EMU2PT
    max_w = rect.width - ml - mr
    if max_w <= 0:
        max_w = rect.width

    rows = []  # (text, size, color, bold, align, line_h)
    for para in tf.paragraphs:
        ptext = "".join(r.text for r in para.runs)
        if not ptext.strip():
            continue
        size = None
        bold = False
        color = (0, 0, 0)
        for r in para.runs:
            if r.font.size is not None and size is None:
                size = r.font.size.pt
            if r.font.bold:
                bold = True
            try:
                if r.font.color is not None and r.font.color.type is not None and r.font.color.rgb is not None:
                    rgb = r.font.color.rgb
                    color = (rgb[0] / 255, rgb[1] / 255, rgb[2] / 255)
            except Exception:
                pass
        if size is None:
            size = defaults.get("size", 18.0)
        algn = ALIGN_MAP.get(para.alignment)
        if algn is None:
            algn = SCHEME_ALIGN.get(defaults.get("align", "l"), 0)
        for ln in _wrap(font, ptext, size, max_w):
            rows.append((ln, size, color, bold, algn, size * 1.25))

    total_h = sum(r[5] for r in rows)
    anchor = tf.vertical_anchor
    y = rect.y0 + mt
    if anchor == MSO_ANCHOR.MIDDLE:
        y = rect.y0 + max(mt, (rect.height - total_h) / 2)
    elif anchor == MSO_ANCHOR.BOTTOM:
        y = rect.y1 - mb - total_h

    writers: dict = {}
    yy = y
    for ln, size, color, bold, algn, lh in rows:
        w = font.text_length(ln, fontsize=size)
        if algn == 1:
            x = rect.x0 + ml + max(0.0, (max_w - w) / 2)
        elif algn in (2, 3):
            x = rect.x0 + ml + max(0.0, max_w - w)
        else:
            x = rect.x0 + ml
        baseline = yy + size * font.ascender
        key = tuple(round(c, 3) for c in color)
        t = writers.setdefault(key, pymupdf.TextWriter(page.rect))
        t.append((x, baseline), ln, font=font, fontsize=size)
        if bold:
            t.append((x + size * 0.035, baseline), ln, font=font, fontsize=size)
        yy += lh
    for key, t in writers.items():
        t.write_text(page, color=key)


# ---------------------------------------------------------------- 主流程
def convert(pptx_path: str, out_path: str) -> int:
    prs = Presentation(pptx_path)
    zf = zipfile.ZipFile(pptx_path)
    font = pymupdf.Font("china-s")
    masters = master_style_defaults(zf, prs)
    W = prs.slide_width * EMU2PT
    H = prs.slide_height * EMU2PT

    doc = pymupdf.open()
    for idx, slide in enumerate(prs.slides, 1):
        page = doc.new_page(width=W, height=H)
        page.draw_rect(page.rect, color=None, fill=(1, 1, 1), overlay=False)

        bg = slide_bg_bytes(zf, slide, prs)
        if bg:
            page.insert_image(page.rect, stream=bg, keep_proportion=False, overlay=False)

        for sh in slide.shapes:
            if sh.shape_type == 13:  # PICTURE
                try:
                    blob = sh.image.blob
                except Exception as exc:  # pragma: no cover
                    print(f"  [warn] slide {idx} 图片读取失败: {exc}")
                    continue
                if sh.image.ext in ("wmf", "emf") or blob[:4] == b"\x01\x00\x00\x00":
                    jb = emf_blob_to_jpeg(blob)
                    if jb is None:
                        print(f"  [warn] slide {idx} EMF 解包失败，跳过该图")
                        continue
                    blob = jb
                rect = pymupdf.Rect(sh.left * EMU2PT, sh.top * EMU2PT,
                                    (sh.left + sh.width) * EMU2PT, (sh.top + sh.height) * EMU2PT)
                page.insert_image(rect, stream=blob, keep_proportion=False)
                continue

            if sh.has_text_frame and sh.text_frame.text.strip():
                rect = pymupdf.Rect(sh.left * EMU2PT, sh.top * EMU2PT,
                                    (sh.left + sh.width) * EMU2PT, (sh.top + sh.height) * EMU2PT)
                ph = None
                if sh.is_placeholder:
                    ph = str(sh.placeholder_format.type)
                if ph and ("TITLE" in ph):
                    defaults = masters.get("title", {"size": 44.0, "align": "l"})
                else:
                    defaults = masters.get("body", {"size": 18.0, "align": "l"})
                draw_text_frame(page, sh.text_frame, rect, defaults, font)
                continue

            if sh.shape_type == 1:  # AUTO_SHAPE
                try:
                    if sh.fill.type is not None and str(sh.fill.type).startswith("SOLID"):
                        rgb = sh.fill.fore_color.rgb
                        rect = pymupdf.Rect(sh.left * EMU2PT, sh.top * EMU2PT,
                                            (sh.left + sh.width) * EMU2PT, (sh.top + sh.height) * EMU2PT)
                        page.draw_rect(rect, color=None,
                                       fill=(rgb[0] / 255, rgb[1] / 255, rgb[2] / 255))
                except Exception:
                    pass
                continue

            if sh.shape_type == 6:  # GROUP：未实现，提示
                print(f"  [warn] slide {idx} 含组合形状，未渲染")

    os.makedirs(os.path.dirname(os.path.abspath(out_path)) or ".", exist_ok=True)
    doc.save(out_path, deflate=True, garbage=3)
    n = doc.page_count
    doc.close()
    print(f"[pptx2pdf] {pptx_path} -> {out_path} ({n} 页)")
    return n


def main() -> int:
    ap = argparse.ArgumentParser(description="PPTX → PDF（纯 Python）")
    ap.add_argument("src")
    ap.add_argument("-o", "--out", default=None)
    a = ap.parse_args()
    out = a.out or os.path.splitext(a.src)[0] + ".pdf"
    convert(a.src, out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
