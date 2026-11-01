# B309《等厚干涉及其应用》报告生成

## 交付物与排版原则

- 源稿：`大学物理实验/实验项目/实验报告/B309-等厚干涉/实验报告-等厚干涉-完整版.md`。
- `generate_B309_docx.py` 调用 KaTeX 输出 MathML，并映射为 Word 原生 Office Math Markup Language（OMML）；公式不是截图。
- `docx_to_pdf.py` 读取 DOCX 的段落、表格、图片与 OMML 公式，以 Typst 排版导出 PDF。DOCX 全部段落（包括表格、公式、标题、页眉页脚）行距统一为至少 1.5 倍；PDF 采用相应的宽松行距。
- 版式参照用户提供的精排版：A4 留白、海军蓝与金色层级、封面信息与结果摘要、清晰分开的原始数据表、逐步编号的计算、测量派生量图表、统一页眉页码。
- 原始手写记录影像未提供；报告只依据转录读数进行算术复核，不声称已逐位核验手写原件，也不改动原始读数。

## 依赖与复现

在仓库根目录执行：

```bash
python -m pip install python-docx lxml typst Pillow
npm install --no-save --no-package-lock katex
python 大学物理实验/工具/B309/generate_B309_charts.py
python 大学物理实验/工具/B309/generate_B309_docx.py
python 大学物理实验/工具/B309/docx_to_pdf.py
```

`generate_B309_charts.py` 根据报告中已复核的派生读数绘制牛顿环逐差量和劈尖间距图，并输出示意图；它不重新计算、替换原始测量读数。PDF 生成后，应渲染全部页面作视觉复核。

本目录 `fonts/` 附有 KaTeX 数学字体及简体中文字体子集；许可文本见 `fonts/KATEX-LICENSE.txt` 与 `fonts/OPEN-FONT-LICENSE.txt`。课本原始页面和裁切衍生图保存在 `大学物理实验/实验项目/assets/`，源页图不覆盖。
