# LaTeX 通道：Markdown → 真正能编译的 .tex → PDF

本目录是"LaTeX 正典"通道，配套 `环境/pdf/` 的 typst 主通道。两条通道都从同一份 Markdown 母版出发，
所以内容永远一致；区别只在排版引擎。

| 通道 | 产物 | 特点 |
| --- | --- | --- |
| typst（`环境/pdf/导出全库.py`） | `<名>.pdf` | 中文排版稳、字体子集化、页眉页脚，**人读首选** |
| LaTeX（本目录） | `<名>-LaTeX版.pdf` + `<名>-LaTeX版.tex` | **真 LaTeX**：可拿到 Overleaf/本机 xelatex 继续改 |
| DOCX（pandoc） | `<名>.docx` | Word 原生公式（OMML），交作业用 |

## 为什么不是"装个 TeX Live"

本沙箱实测：`ctan.org`、`mirror.ctan.org`、`tug.org`、`conda` 全部不可达（curl 返回 000），
GitHub release 资产域也断流（`gh api` 能读元数据，下载 EOF）。唯一能拿到 LaTeX 引擎的通道是 **npm**：

- 包：**`glyphtex-engine@0.1.0`**（MIT，约 20 MB）
- 内含：`wasm/tectonic_wasm.wasm`（Tectonic 编译的 **XeTeX** 引擎，3.4 MB）
  + `wasm/tectonic-bundle.tar.gz`（TeX Live 宏包树，1130 文件、150 个 sty/cls）
  + `wasm/packs/*.tar.gz`（10 个可选宏包包：writing / figures / tables-plus / fonts-latinmodern …）
  + `dist/index.js`（JS API：`TexEngine.load` → `addFile` → `compile` → `pdf()`）

装法见 `bootstrap_latex.sh`（一条命令，约 1 分钟）。

## 三个脚本

```bash
# 1) 装引擎（一次即可；引擎装在 /home/user/opt/tex/glyphtex，不入库）
bash 环境/pdf/latex/bootstrap_latex.sh

# 2) 批量导出（15 份：11 课题 + 2 合集 + 讲义 + 章程）
/home/user/opt/.venv/bin/python 环境/pdf/latex/导出LaTeX.py --all
#    也可以 --topics / --lectures / --charter / --check

# 3) 单份编译（调试用）
node 环境/pdf/latex/编译LaTeX.mjs a.tex [b.tex ...]      # 同名 .pdf
node 环境/pdf/latex/编译LaTeX.mjs a.tex=out.pdf         # 指定输出名
```

- `md到LaTeX.py`：Markdown →（pandoc）→ 模板清理 → **按字符挑字体** → 可编译 .tex
- `编译LaTeX.mjs`：wasm 引擎驱动；报告 `status / 缺字 / 错误`，缺字与错误都会被上层的门禁拦住
- `导出LaTeX.py`：合并 md → 转换 → 一次性编译 → 核验（页数 / 体积 / 汉字数）

## 关键机制：为什么必须"逐字符挑字体"

XeTeX **没有字符级字体回退**：字形不在当前字体里就直接 `Missing character`，xdvipdfmx 还会
因此拒绝出 PDF。而本学科文档是"中文 + 数学 + 箭头/圈号/emoji + 代码"混排，一套字体不可能全覆盖。
所以 `md到LaTeX.py` 读三套字体的 cmap，**按字符**把连续同类字符包成：

| 宏 | 字体 | 管什么 |
| --- | --- | --- |
| `\zh{…}` | Noto Serif SC（`script=hani`） | 汉字、全角标点 |
| `\sym{…}` | DejaVu Sans | `→ ≈ ≤ ① ▁ ✔` 等符号 |
| `\emo{…}` | Noto Emoji | `⭐ ✅ 🚨 🦙` 等 |
| `\codezh{…}` | Noto Sans SC | 含汉字的行内代码 |

汉字之间插 `\zhglue`（`\hskip0pt plus .06em minus .01em`）当断行点——bundle 里没有 ICU 的
中文断行数据，`\XeTeXlinebreaklocale "zh"` 必失败（实测）。

## 踩过的坑（改代码前务必读）

1. **`\define 宏必须带参数**：`\def\zh{{\zhfont}}` 是错的——字体赋值只在组内有效，那个组
   随 `\zh` 立刻结束，中文仍用拉丁字体排。
2. **CJK 的 catcode 是 11（字母）**：`\relax题` 会被读成**一个控制字** `\relax题` →
   `Undefined control sequence`。所以胶水必须写成控制字宏，且控制字后紧跟汉字要补空格。
3. **`\lstinline` 遇汉字必炸**（`\lst@arg ->判` 未定义控制字，改 catcode 也无效）→ 含汉字的
   行内代码改走 `\codezh{}`，ASCII 的保留 `\lstinline!…!`。
4. **`listings` 的 `literate={⭐}{…}1` 不可用**：会把 ASCII 字母也吞掉并报
   `Improper alphabetic constant`；改用 `escapeinside={(*@}{@*)}`，转换器把 emoji 包成
   `(*@{\emo{⭐}}@*)`。
5. **数学区里的中文**：`\[\text{总 FLOPs}\]` 的 `总` 会落到拉丁字体 → 必须把 `\text{}`/`\mathrm{}`
   里的汉字再包一层 `\zh{}`（`_math_cjk()`）。
6. **`\tableofcontents` 会展开脆弱命令**：`.toc` 里留下 `\zhfont`（宏被展开、组还在），
   所以字体宏别写成会在写文件时崩掉的形式；本次实测 `\DeclareRobustCommand` 与 `\def` 均可用。
7. **bundle 缺 `bookmark.sty`** → 直接**不用 hyperref**（新版 hyperref 强制依赖它），
   `\href/\url/\texorpdfstring/\hypersetup/\urlstyle` 全部给降级定义。
   其余缺失宏包由 `strip_missing_packages()` 按 bundle 实际内容自动整行剥离并打印。
8. **数学必须 `\usepackage{lmodern}`**：否则 CM 数学字体缺 `.pfb` 物理字模，
   xdvipdfmx 报 `Cannot proceed without .vf or "physical" font`，PDF 只有 15 字节。
9. 需要 `\usepackage[T1]{fontenc}`：OT1 下 ASCII 的 `< > |` 会排成 `¡ ¿ —`。
10. **驱动别把输出写成同名 .pdf**：会覆盖 typst 主 PDF。用 `源.tex=输出.pdf` 显式指定。

## 字体与授权

`NotoSerifSC-Regular.ttf`（思源宋体）与 `NotoSansSC-Regular.ttf`（思源黑体）为 **SIL OFL 1.1**，
随仓库放在 `环境/pdf/字体/`（已子集化，48 MB → 12 MB）；DejaVu Sans 与 Noto Emoji 亦为自由许可。
TeX 宏包与 Tectonic 引擎（MIT）不入库，用 `bootstrap_latex.sh` 重建。

在**真实 TeX Live** 上编译本目录的 .tex：`xelatex 文件名.tex`，并把 `环境/pdf/字体/*.ttf`
拷到同目录（.tex 里按文件名引用字体）。
