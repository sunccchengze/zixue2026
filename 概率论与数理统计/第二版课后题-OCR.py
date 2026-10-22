#!/usr/bin/env python3
"""将扫描版课后题PDF按页OCR成可检索Markdown。

依赖：PyMuPDF、rapidocr_onnxruntime、opencv-python-headless。
用法：python 第二版课后题-OCR.py [输入PDF] [输出Markdown]
OCR仅供检索；公式和符号须回看PDF原页。
"""
from pathlib import Path
import sys
import pymupdf
from rapidocr_onnxruntime import RapidOCR

ROOT = Path(__file__).resolve().parent
DEFAULT_PDF = ROOT / "（！！！以后作业以这个为准）概率论与数理统计 第二版 课后题.pdf"
DEFAULT_MD = ROOT / "第二版课后题-OCR.md"
src = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else DEFAULT_PDF
out = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else DEFAULT_MD

doc = pymupdf.open(src)
ocr = RapidOCR()
with out.open("w", encoding="utf-8") as f:
    f.write("# 《概率论与数理统计（第二版）》课后题 OCR 转写\n\n")
    f.write(f"> 来源：`{src.name}`；共 {len(doc)} 页扫描件。以下为 OCR 初稿，公式、上下标、补集符号和题号可能识别错误；正式作业以对应 PDF 原页为准。章节及题号便于检索，数学符号务必回看扫描原件。\n\n")
    f.write("## 页码映射\n\n| PDF物理页 | 印刷页/页面内容 | OCR内容 |\n|---:|---|---|\n")
    pages = []
    for i, page in enumerate(doc, 1):
        pix = page.get_pixmap(matrix=pymupdf.Matrix(2, 2), alpha=False)
        result, _ = ocr(pix.tobytes("png"))
        lines = [str(item[1]).strip() for item in (result or []) if len(item) > 1 and str(item[1]).strip()]
        text = "\n".join(lines)
        summary = "；".join(lines[:2]).replace("|", "/")[:100] or "（未识别）"
        f.write(f"| {i} | {summary} | [跳转](#pdf第{i}页) |\n")
        pages.append((i, text))
        if i % 5 == 0:
            print(f"OCR {i}/{len(doc)}", flush=True)
    f.write("\n---\n")
    for i, text in pages:
        f.write(f"\n## PDF第{i}页\n\n")
        if text:
            for line in text.splitlines():
                f.write(line.replace("`", "\\`").rstrip() + "\n")
        else:
            f.write("（未识别到文字）\n")
print(f"Wrote {out} ({out.stat().st_size:,} bytes)")
