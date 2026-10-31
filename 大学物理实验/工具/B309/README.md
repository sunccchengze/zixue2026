# B309 KaTeX 报告生成与 PDF 导出

## 交付物与工作流

1. `实验报告-等厚干涉-完整版.md` 是 KaTeX 源稿：行内数学使用 `$…$`，独立公式使用 `$$…$$`。
2. `generate_B309_docx.py` 调用 KaTeX 输出 MathML，再映射为 Word 原生 Office Math Markup Language（OMML）对象；DOCX 公式不是截图。
3. `docx_to_pdf.py` 读取 DOCX 段落、表格、图片和 OMML 公式，以 Typst 排版导出 PDF。正文、公式、标题及表格统一使用至少 1.5 倍行距；当前环境无 LibreOffice，这是读取 DOCX 后按其内容与样式导出的 PDF，页数及页面已渲染检查。

## 依赖与复现

在仓库根目录执行：

```bash
python -m pip install python-docx lxml typst
npm install --no-save --no-package-lock katex
python 大学物理实验/工具/B309/generate_B309_docx.py
python 大学物理实验/工具/B309/docx_to_pdf.py
```

本目录 `fonts/` 已附必要的 KaTeX 数学字体及简体中文宋体字形子集；`fonts/KATEX-LICENSE.txt` 与 `fonts/OPEN-FONT-LICENSE.txt` 保存相应字体/软件许可文本。原始教材页扫描保存在 `大学物理实验/实验项目/assets/`，报告引用的是这些扫描的裁切衍生图，原始页图不覆盖。
