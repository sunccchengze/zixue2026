"""扫描习题 PDF → 可检索 Markdown；OCR 仅作检索，公式以原图人工校对为准。
依赖: pymupdf, rapidocr_onnxruntime, opencv-python-headless。运行: python ocr_second_edition.py
"""
from pathlib import Path
import pymupdf
from rapidocr_onnxruntime import RapidOCR
import re

HERE=Path(__file__).resolve().parent
PDF=HERE.parent/'资料原件/概率论与数理统计-第二版-课后题.pdf'
OUT=HERE/'概率论与数理统计-第二版-课后题-OCR.md'
pdf=pymupdf.open(PDF);ocr=RapidOCR()
with OUT.open('w') as w:
 w.write('# 概率论与数理统计（第二版）课后题｜OCR 检索稿\n\n')
 w.write('> 来源：`../资料原件/概率论与数理统计-第二版-课后题.pdf`，43 页；PDF 页序并非教材印刷页序。自动 OCR 可用于全文搜索，但公式、上下标、补集、表格均须对照对应 PDF 页原图，不可直接用于判卷。第二章精校题面另见 `../第二章课后作业/`。\n\n')
 for i,p in enumerate(pdf):
  pix=p.get_pixmap(matrix=pymupdf.Matrix(2,2));res,elapsed=ocr(pix.tobytes('png'))
  lines=[r[1] for r in (res or [])]
  # 不自动猜印刷页码：普通数字也常被误识别为页码。
  w.write(f'## PDF 第 {i+1} 页\n\n')
  w.write('\n\n'.join(lines)+'\n\n')
  print(i+1,'/',len(pdf),'lines',len(lines),flush=True)
