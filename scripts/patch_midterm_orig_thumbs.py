#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""期中精析：为四次作业各插入一张原卷首页缩略图（图 2-0 ~ 图 5-0），置于章标题之后。
图片来源：大学物理/作业/tmp_ocr/image17-20.png（从 09-16 版 docx 中提取的原始嵌入图，
与当时 资料原件 扫描件首页渲染一致；若需重渲：pymupdf 渲染 资料原件/第十二 十三 十四 十五次 .pdf 的
P6/P12/P18/P24，dpi≈150）。幂等：说明行已存在则跳过。"""
import pathlib
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.text.paragraph import Paragraph

DOCX = pathlib.Path("大学物理/期中复习/大学物理期中_12-15次作业图文精析_孙承泽_2253710052.docx")
FIGDIR = pathlib.Path("大学物理/期中复习/原卷缩略图")

ITEMS = [
    ("二、第十二次", "第十二次-p7.png",
     "图 2-0  第十二次《机械波》作业原卷首页（班级 能动强基2501 孙承泽 2253710052，p7；完整 6 页见分支文件）"),
    ("三、第十三次", "第十三次-p13.png",
     "图 3-0  第十三次《波动光学 1》原卷首页（p13；共 6 页，双缝·薄膜·牛顿环·迈克尔逊）"),
    ("四、第十四次", "第十四次-p19.png",
     "图 4-0  第十四次《波动光学 2》原卷首页（p19；单缝·光栅·分辨本领）"),
    ("五、第十五次", "第十五次-p25.png",
     "图 5-0  第十五次《波动光学 3》原卷首页（p25；偏振·马吕斯·布儒斯特·波片）"),
]

doc = Document(str(DOCX))
all_text = "\n".join(p.text for p in doc.paragraphs)

for head, fname, cap in ITEMS:
    if cap.split("原卷首页")[0] + "原卷首页" in all_text:
        print(f"  skip {fname}（已存在）")
        continue
    anchor = None
    for p in doc.paragraphs:
        if p.text.strip().startswith(head):
            anchor = p
            break
    if anchor is None:
        raise SystemExit(f"未找到章标题: {head}")
    fig = FIGDIR / fname
    if not fig.exists():
        raise SystemExit(f"缺图: {fig}")

    # 说明段 + 图段，均插入到章标题之后（图在说明之上）
    cap_p = OxmlElement('w:p')
    img_p = OxmlElement('w:p')
    anchor._p.addnext(cap_p)
    anchor._p.addnext(img_p)  # img 最终位于 cap 之前

    ipara = Paragraph(img_p, anchor._parent)
    ipara.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = ipara.add_run()
    run.add_picture(str(fig), width=Inches(5.8))

    cpara = Paragraph(cap_p, anchor._parent)
    cpara.alignment = WD_ALIGN_PARAGRAPH.CENTER
    crun = cpara.add_run(cap)
    crun.font.size = Pt(8.5)
    crun.font.color.rgb = RGBColor(0x5A, 0x6C, 0x7D)
    crun.italic = True
    crun.font.name = 'Times New Roman'
    crun._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
    print(f"  + {fname} after 「{head}…」")

doc.save(str(DOCX))
print("thumbs done ->", DOCX)
