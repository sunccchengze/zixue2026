#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Markdown → 可编译 LaTeX（含中文与符号的字体分组）· Agent 维护 · B7

为什么需要这一步，而不是直接 `pandoc -t latex`：
  本学科的讲义与课题简报是**中文 + 数学 + 箭头/圈号/方块等符号**混排。
  排版引擎（Tectonic 的 XeTeX 内核）**没有字符级字体回退**：任何一个字形不在
  当前字体里，就直接 "Missing character"，而且 xdvipdfmx 会因此拒绝出 PDF
  （报 `Cannot proceed without .vf or "physical" font`）。
  实测结论：
    · 中文/全角标点在 lmodern（拉丁字体）里没有 → 必须切到中文字体
    · `→ ≈ ≤ ① ▁ ✔` 等符号在中文字体里也未必有 → 需要按**字符**挑字体
    · 数学公式必须走 Latin Modern（`\\usepackage{lmodern}`），否则 CM 的
      .pfb 物理字模缺失 → PDF 生成失败
  所以这里的做法是：读字体 cmap，**逐字符选字体**，把连续同类字符包成
  `{\\zh …}` / `{\\sym …}` / `{\\emo …}`，并在汉字之间插入零宽可断胶水
  （因为 ICU 的 zh 断行数据不在 bundle 里，中文需要自己给断行点）。

产出：单文件、自带导言区、可直接 `xelatex` 编译的 .tex
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PDF_DIR = HERE.parent                     # 环境/pdf/
SUBJECT = PDF_DIR.parent.parent           # 人工智能基础与应用/
REPO = SUBJECT.parent
FONT_DIR = Path("/home/user/opt/fonts")   # wasm 引擎与本地编译都用这套（子集化后）
REPO_FONT_DIR = PDF_DIR / "字体"           # 仓库内的字体副本（随仓库分发）

# 汉字之间的零宽断行点。**必须是控制字宏**：CJK 字符的 catcode 是 11（字母），
# 直接写 `\hskip0pt plus .04em minus .01em\relax题` 会被 TeX 读成控制字 `\relax题`
# → Undefined control sequence。用宏名 + 后面的保险空格就稳了。
GLUE = r"\zhglue"


# ── 字体覆盖表 ──────────────────────────────────────────────────────────────

def load_cmaps() -> dict[str, set[int]]:
    from fontTools.ttLib import TTFont
    out: dict[str, set[int]] = {}
    for name in ("NotoSerifSC-Regular.ttf", "DejaVuSans.ttf", "NotoEmoji-Regular.ttf"):
        p = FONT_DIR / name
        if not p.exists():
            p = REPO_FONT_DIR / name
        codes: set[int] = set()
        if p.exists():
            f = TTFont(p, lazy=True)
            for t in f["cmap"].tables:
                codes |= set(t.cmap.keys())
            f.close()
        out[name] = codes
    return out


CMAPS: dict[str, set[int]] = {}
# 字体类别 → LaTeX 宏（在导言区定义）
CLASSES = ("zh", "sym", "emo")


def classify(ch: str) -> str | None:
    """返回该字符应当使用的字体类别；ASCII 返回 None（用默认拉丁字体）"""
    cp = ord(ch)
    if cp < 0x80:
        return None
    # 顺序有意为之：符号先查 DejaVu，再查思源宋，最后 emoji。
    # （思源宋里没有 ⭐✅❌ 这类符号；而 ⚠️ 之类需要 emoji 字体）
    for cls, fname in (("sym", "DejaVuSans.ttf"),
                       ("emo", "NotoEmoji-Regular.ttf"),
                       ("zh", "NotoSerifSC-Regular.ttf")):
        if cp in CMAPS.get(fname, ()):
            return cls
    return "?"


# ── 导言区 ──────────────────────────────────────────────────────────────────

PREAMBLE = r"""% ═══ 由 环境/pdf/latex/md到LaTeX.py 生成 ═══
% 中文字体：思源宋体（子集，SIL OFL 1.1）；拉丁/数学：Latin Modern（随 TeX Live 分发）
% 编译：xelatex（本仓库自带 wasm 版 XeTeX 引擎，见 环境/pdf/latex/编译LaTeX.mjs）
\usepackage[T1]{fontenc}      % 否则 ASCII 的 < > | 在 OT1 下排成 ¡ ¿ —
\usepackage{lmodern}          % 必需：数学的物理字模（否则 xdvipdfmx 拒绝出 PDF）
\usepackage{amsmath,amssymb,mathtools}
\usepackage{booktabs,longtable,array,multirow}
\usepackage{graphicx}
\usepackage{xcolor}
\usepackage{listings}
% 不用 hyperref：新版 hyperref 强制依赖 bookmark.sty，而 bundle 里没有。
% 链接命令用降级定义，保证正文里的 \href / \url 不会报错。
\providecommand{\href}[2]{#2}
\providecommand{\url}[1]{\texttt{#1}}
\providecommand{\hypertarget}[2]{#2}
\providecommand{\hyperlink}[2]{#2}
\providecommand{\urlstyle}[1]{}
\providecommand{\texorpdfstring}[2]{#1}   % hyperref 的命令，剥离后仍被模板/标题用到
\providecommand{\phantomsection}{}
\providecommand{\pdfstringdef}[2]{}
\providecommand{\hypersetup}[1]{}

% ── 三套字体：中文 / 符号 / emoji（按字符 cmap 自动选择）──
\font\zhfont="[NotoSerifSC-Regular.ttf]:script=hani" at 10.5pt
\font\symfont="[DejaVuSans.ttf]" at 10.5pt
\font\emofont="[NotoEmoji-Regular.ttf]" at 10.5pt
\font\zhmonofont="[NotoSansSC-Regular.ttf]" at 9pt
% 用法：\zh{中文} / \sym{→} / \emo{🦙}
% 注意：必须**带参数**。写成 \def\zh{{\zhfont}} 是错的——字体赋值只在小群里有效，
% 那个小群随 \zh 立刻结束，于是中文仍然用拉丁字体排，报 Missing character。
\def\zh#1{{\zhfont #1}}
\def\sym#1{{\symfont #1}}
\def\emo#1{{\emofont #1}}
% 含汉字的行内代码：listings 的 \lstinline 遇到汉字必炸（`\lst@arg ->判`
% 未定义控制字，catcode 设 12 也无效），所以直接自己排。
\def\codezh#1{{\zhmonofont #1}}

\def\zhglue{\hskip0pt plus .06em minus .01em}
\linespread{1.12}
\setlength{\parindent}{0pt}
\setlength{\parskip}{0.45em}

% ── 代码块：等宽 + 中文字体（listings 默认字体不含汉字）──
\lstset{
  basicstyle=\zhmonofont,
  breaklines=true,
  breakatwhitespace=false,
  columns=fullflexible,
  keepspaces=true,
  showstringspaces=false,
  frame=single,
  framesep=4pt,
  rulecolor=\color{gray!45},
  backgroundcolor=\color{gray!7},
  xleftmargin=6pt,
  extendedchars=true,
  tabsize=2,
  % 代码块里的 emoji：NotoSansSC 没有这些字形（listings 不做字符级回退）。
  % 用 escapeinside 开口子，转换器把 emoji 逐字包成 (*@{\emo{⭐}}@*)。
  % 试过 literate={⭐}{{\emofont ⭐}}1，会把 ASCII 字母也吞掉并报
  % `Improper alphabetic constant`，不可用。
  escapeinside={(*@}{@*)},
}
\renewcommand{\lstlistingname}{代码}

% ── 表格线宽（booktabs 风格）──
\renewcommand{\arraystretch}{1.25}

% ── 标题样式 ──
\usepackage{titlesec}
\titleformat{\section}{\Large\bfseries}{\thesection}{0.6em}{}
\titlespacing*{\section}{0pt}{1.1em}{0.5em}
"""

PANDOC_HEADER = PREAMBLE


# ── 正文后处理 ──────────────────────────────────────────────────────────────

VERBATIM_CMDS = ("href", "url", "includegraphics", "label", "ref", "eqref", "pageref",
                 "cite", "citep", "citet", "index", "hypertarget", "hyperlink",
                 "lstinline", "verb", "input", "include", "includegraphics")
VERBATIM_ENVS = ("lstlisting", "verbatim", "Verbatim", "minted")


SPECIALS = {
    "\\": "\\textbackslash{}", "{": "\\{", "}": "\\}", "$": "\\$", "&": "\\&",
    "#": "\\#", "^": "\\textasciicircum{}", "_": "\\_", "%": "\\%",
    "~": "\\textasciitilde{}",
}


def alt_font_class(ch: str) -> str | None:
    """代码字体（NotoSansSC）缺这个字形时，给出可用的替代字体类别。

    代码里什么字符都可能出现（emoji、替换符 U+FFFD、罕见符号），而 listings
    没有任何字符级字体回退——不处理就是静默丢字。CJK 本身在 NotoSansSC 里，
    所以这里主要命中 ⭐✅🚨 与 � 这类。
    """
    if ord(ch) < 128 or ch in CMAPS.get("NotoSansSC-Regular.ttf", ()):
        return None
    cls = classify(ch)
    return cls if cls in ("zh", "sym", "emo") else None


def wrap_inline(text: str) -> str:
    """行内代码：直接嵌字体切换宏（\\codezh 内部已按字体排版）"""
    return "".join(f"{{\\{c}{{{ch}}}}}" if (c := alt_font_class(ch)) else ch for ch in text)


def wrap_listing(text: str) -> str:
    """代码块：走 \\lstset 里的 escapeinside 口子 `(*@ … @*)`"""
    return "".join(f"(*@{{\\{c}{{{ch}}}}}@*)" if (c := alt_font_class(ch)) else ch
                   for ch in text)


def tex_escape(text: str) -> str:
    out = [SPECIALS.get(ch, ch) for ch in text]
    return wrap_inline("".join(out))


class Processor:
    def __init__(self, text: str):
        self.s = text
        self.i = 0
        self.n = len(text)
        self.out: list[str] = []
        self.unknown: dict[str, int] = {}

    # —— 主循环 ——
    def run(self) -> str:
        """整份处理（含导言区）：\title{中文} 这类也在导言区，同样需要字体切换。

        安全性：包装只作用于**非 ASCII 字符**，导言区里的宏包名/路径/选项全是 ASCII，
        注释与数学/verbatim 区域整体跳过，所以不会动到命令结构。
        """
        return self._scan()

    def _finish_tail(self) -> str:
        return self.s[self.i:]

    def _scan(self) -> str:
        start = self.i
        buf: list[str] = []
        while self.i < self.n:
            c = self.s[self.i]
            # 注释：整行原样
            if c == "%":
                self._flush(buf)
                j = self.s.find("\n", self.i)
                j = self.n if j < 0 else j
                self.out.append(self.s[self.i:j])
                self.i = j
                continue
            # 数学：$…$ / $$…$$ / \(…\) / \[…\]
            if c == "$":
                self._flush(buf)
                self._math()
                continue
            if c == "\\" and self.s[self.i:self.i + 2] in ("\\(", "\\["):
                self._flush(buf)
                self._until_closing(kind="paren" if self.s[self.i + 1] == "(" else "bracket")
                continue
            # 环境（verbatim 类原样）
            if self.s.startswith("\\begin{", self.i):
                m = re.match(r"\\begin\{([^}]+)\}", self.s[self.i:])
                env = m.group(1)
                if env in VERBATIM_ENVS:
                    self._flush(buf)
                    end = self.s.find(f"\\end{{{env}}}", self.i)
                    end = self.n if end < 0 else end + len(f"\\end{{{env}}}")
                    self.out.append(self._verbatim_body(self.s[self.i:end]))
                    self.i = end
                    continue
            # 命令
            if c == "\\":
                m = re.match(r"\\([A-Za-z@]+|[^A-Za-z@\s]?)", self.s[self.i:])
                if m:
                    name = m.group(1).rstrip("*")
                    self._flush(buf)
                    if name in ("lstinline", "verb"):
                        # 行内代码是**分隔符定界**（\lstinline!code!），且命令本身要由
                        # _copy_delimited 决定去留：含汉字时整段换成 \codezh{}
                        self.i += m.end()
                        self._copy_delimited(m.group(0))
                        continue
                    self.out.append(m.group(0))
                    self.i += m.end()
                    if name in VERBATIM_CMDS or name in ("begin", "end", "pandocbounded",
                                                         "tightlist", "toprule", "midrule",
                                                         "bottomrule", "hline", "cline",
                                                         "tablehead", "endhead"):
                        if name in ("begin", "end"):
                            mm = re.match(r"\{([^}]*)\}", self.s[self.i:])
                            env = mm.group(1) if mm else ""
                            self._copy_braced_arg()          # 环境名
                            self._copy_optional()
                            if name == "begin" and env in VERBATIM_ENVS:
                                # 代码块原文照抄：里面的 { } % \ 不能被当正文处理
                                end = f"\\end{{{env}}}"
                                j = self.s.find(end, self.i)
                                j = self.n if j < 0 else j + len(end)
                                self.out.append(self._verbatim_body(self.s[self.i:j]))
                                self.i = j
                            continue
                        self._copy_optional()
                        self._copy_all_braced()
                        continue
                    continue
                # 兜底：单个反斜杠（如行尾）。**必须先 flush**，否则这一小片段会
                # 跑到缓冲区内容之前——表格里就出现「行分隔符跑进单元格」的怪象
                self._flush(buf)
                self.out.append(c)
                self.i += 1
                continue
            # 普通文本
            buf.append(c)
            self.i += 1
        self._flush(buf)
        return "".join(self.out)

    # —— 辅助 ——
    def _flush(self, buf: list[str]) -> None:
        if buf:
            self.out.append(self._wrap("".join(buf)))
            buf.clear()

    def _copy_optional(self) -> None:
        if self.i < self.n and self.s[self.i] == "[":
            depth = 1
            j = self.i + 1
            while j < self.n and depth:
                if self.s[j] == "[": depth += 1
                elif self.s[j] == "]": depth -= 1
                j += 1
            self.out.append(self.s[self.i:j])
            self.i = j

    def _copy_braced_arg(self) -> None:
        if self.i < self.n and self.s[self.i] == "{":
            depth, j = 1, self.i + 1
            while j < self.n and depth:
                if self.s[j] == "{" and self.s[j - 1] != "\\": depth += 1
                elif self.s[j] == "}" and self.s[j - 1] != "\\": depth -= 1
                j += 1
            self.out.append(self.s[self.i:j])
            self.i = j

    def _copy_all_braced(self) -> None:
        while self.i < self.n and self.s[self.i] == "{":
            self._copy_braced_arg()
            if self.i < self.n and self.s[self.i] == "{":
                continue
            break

    @staticmethod
    def _verbatim_body(body: str) -> str:
        """代码块：原文照抄，但把 emoji 走 escapeinside 口子切字体（否则静默丢字）"""
        return wrap_listing(body)

    def _copy_delimited(self, cmd: str = "") -> None:
        """拷贝 `\\lstinline!...!` / `\\verb|...|` 这类分隔符定界的参数。

        pandoc 的行内代码就是这种形式；里面的字符（如 `!`）不能被我们的
        字体包装或空格保险碰到，否则定界符错位 → `Runaway argument?`
        """
        if self.i < self.n and self.s[self.i] == "[":
            self._copy_optional()
        j = self.i
        while j < self.n and self.s[j] in " \t":
            j += 1
        if j >= self.n:
            return
        delim = self.s[j]
        end = self.s.find(delim, j + 1)
        end = self.n if end < 0 else end + 1
        body = self.s[j + 1:end - 1]
        if any(ord(c) > 127 for c in body):
            # 含汉字的行内代码：走 \codezh（转义 TeX 特殊字符），绕开 listings 的坑
            self.out.append("\codezh{" + tex_escape(body) + "}")
        else:
            # ASCII 行内代码：保留 `\lstinline!code!` 整体
            # （少了命令名，`!` 定界符就会印在纸上）
            self.out.append(cmd + self.s[self.i:end])
        self.i = end

    def _math_cjk(self, math: str) -> str:
        r"""数学区里的中文：`\text{总 FLOPs}` → `\text{\zh{总} FLOPs}}`

        公式整体原样保留（数学字体不能动），但 `\text{}` 里常写中文说明，
        那些字走的是数学/文本字体（T1 拉丁），必然缺字 → 逐字切到中文字体。
        """
        def fix(m: re.Match) -> str:
            cmd, inner = m.group(1), m.group(2)
            if not any(ord(c) > 127 for c in inner):
                return m.group(0)
            return f"{cmd}{{{self._wrap(inner)}}}"

        return re.sub(r"(\\(?:text|textrm|mathrm|mbox|hbox|operatorname))\{([^{}]*)\}", fix, math)

    def _math(self) -> None:
        start = self.i
        if self.s.startswith("$$", self.i):
            j = self.s.find("$$", self.i + 2)
            j = self.n if j < 0 else j + 2
        else:
            j = self.s.find("$", self.i + 1)
            # 跳过转义的 \$
            while j > 0 and self.s[j - 1] == "\\":
                j = self.s.find("$", j + 1)
            j = self.n if j < 0 else j + 1
        self.out.append(self._math_cjk(self.s[start:j]))
        self.i = j

    def _until_closing(self, kind: str) -> None:
        pat = r"\\\)" if kind == "paren" else r"\\\]"
        m = re.search(pat, self.s[self.i:])
        j = self.n if not m else self.i + m.end()
        # `\[ … \]` / `\( … \)` 也是数学区：同样要处理里面的中文
        self.out.append(self._math_cjk(self.s[self.i:j]))
        self.i = j

    # —— 核心：按字符选字体 ——
    def _wrap(self, text: str) -> str:
        if not text:
            return ""
        pieces: list[str] = []
        cur_cls: str | None = None
        run: list[str] = []

        def flush_run() -> None:
            if not run:
                return
            if cur_cls is None:
                pieces.append("".join(run))
            else:
                body = "".join(run)
                if cur_cls == "zh":
                    body = self._cjk_glue(body)
                pieces.append("\\" + cur_cls + "{" + body + "}")
            run.clear()

        for ch in text:
            cls = classify(ch)
            if cls == "?":
                # DejaVu 兜底（首个覆盖它的字体会被 classify 判成 sym，走不到这里；
                # 走到这里说明三套字体都没有这个字形）
                self.unknown[ch] = self.unknown.get(ch, 0) + 1
                cls = "sym" if ord(ch) in CMAPS.get("DejaVuSans.ttf", ()) else None
                if cls is None:
                    ch = "?"          # 保守兜底：宁可显示问号，也不让整份文档编译失败
            if cls != cur_cls:
                flush_run()
                cur_cls = cls
            run.append(ch)
        flush_run()
        out = "".join(pieces)
        # 保险：CJK 字符 catcode=11，紧跟控制字会被吞进去（`\relax题` → 未定义控制字）
        out = re.sub(r"(\\[A-Za-z@]+|\\[^A-Za-z@\\])"
                     r"(?=[\u2e80-\u9fff\u3000-\u303f\uff00-\uffef])", r"\1 ", out)
        return out

    @staticmethod
    def _cjk_glue(text: str) -> str:
        """在汉字之间插入零宽可断胶水——中文断行点（bundle 缺 ICU zh 数据）"""
        out: list[str] = []
        for k, ch in enumerate(text):
            out.append(ch)
            nxt = text[k + 1] if k + 1 < len(text) else ""
            if nxt and re.match(r"[\u2e80-\u9fff\u3000-\u303f\uff00-\uffef]", ch or "") \
                    and re.match(r"[\u2e80-\u9fff\u3000-\u303f\uff00-\uffef]", nxt):
                out.append(GLUE)
        return "".join(out)


TEMPLATE_STRIP = (
    "\\usepackage{unicode-math}",
    "\\defaultfontfeatures",
    "babel",
    "footnote",          # footnote.sty 不在 bundle 里（长表格脚注本学科用不到）
    "makesavenoteenv",   # 同上，来自 footnote 宏包
)


# 这些宏包即使 bundle 里有也不能用（会链条式依赖缺失的包）
# hyperref：新版强制加载 bookmark.sty，而 bundle 缺 bookmark.sty
BLACKLIST_PKGS = {"hyperref"}


BUNDLE_DIR = Path("/home/user/opt/tex/glyphtex/bundle")


def bundle_packages() -> set[str]:
    """引擎 bundle 里实际可用的宏包/文档类名"""
    if not BUNDLE_DIR.exists():
        return set()
    return {p.stem for p in BUNDLE_DIR.iterdir()
            if p.suffix in (".sty", ".cls", ".def", ".fd", ".ldf")}


def strip_missing_packages(text: str, log: list[str] | None = None) -> str:
    r"""把导言区里引用"bundle 里没有的宏包"的行整行剥掉。

    这是踩坑换来的：pandoc 模板会自动加载 unicode-math / bookmark / footnote 等
    宏包，而我们的离线 bundle 并不都有；缺一个就 `File not found` 而整份编译失败
    （引擎被终止在交互式提问上：`terminal input forbidden`）。
    与其一个个手写，不如按 bundle 实际内容自动判断。
    """
    avail = bundle_packages()
    if not avail:
        return text
    head, sep, body = text.partition(r"\begin{document}")
    out: list[str] = []
    for line in head.splitlines():
        pkgs: list[str] = []
        for m in re.finditer(r"\\(?:usepackage|RequirePackage)(\[[^\]]*\])?\{([^}]*)\}", line):
            pkgs += [p.strip() for p in m.group(2).split(",") if p.strip()]
        missing = [p for p in pkgs if p not in avail or p in BLACKLIST_PKGS]
        if missing:
            if log is not None:
                log.append(f"剥离缺失宏包：{', '.join(missing)}")
            continue
        out.append(line)
    return "\n".join(out) + sep + body


def strip_template(text: str) -> str:
    r"""剥掉 pandoc 模板里与本引擎不兼容的行。

    实测三处必须去掉：
      · `\usepackage{unicode-math}`（会连带 fontspec）——bundle 里没有这两个宏包，
        且我们用的是 XeTeX 原语字体切换，不需要它们
      · `\defaultfontfeatures{...}`（来自 fontspec）
      · `\usepackage[...]{babel}`（babel 的 bidi 支持在 XeTeX 下会报错，本学科用不到）
      · `\documentclass[chinese,]{article}` 的 chinese 选项（需要 ctex 宏包）
    """
    out = []
    for line in text.splitlines():
        if any(k in line for k in TEMPLATE_STRIP):
            continue
        if line.strip() == "chinese,":
            continue
        out.append(line)
    return "\n".join(out)


def md_to_tex(md: Path, tex: Path, title: str, pandoc: str,
              toc: bool = True, number: bool = True) -> tuple[bool, str, dict[str, int]]:
    import subprocess
    global CMAPS
    if not CMAPS:
        # 被当模块导入时（导出器）必须在这里初始化字体覆盖表，
        # 否则 classify() 对每个汉字都返回"无覆盖"，正文会被兜底成 ???
        CMAPS = load_cmaps()
    header = PDF_DIR / "latex" / "_preamble.tex"
    header.parent.mkdir(parents=True, exist_ok=True)
    header.write_text(PANDOC_HEADER, encoding="utf-8")

    args = [pandoc, str(md), "-o", str(tex), "-t", "latex", "--standalone",
            "-f", "markdown+raw_attribute+pipe_tables+tex_math_dollars",
            "--wrap=none", "--listings",
            f"--metadata=title:{title}", "--metadata=lang:zh-CN",
            f"--include-in-header={header}"]
    if toc:
        args += ["--toc", "--toc-depth=2"]
    if number:
        args.append("--number-sections")
    r = subprocess.run(args, capture_output=True, text=True)
    if r.returncode != 0:
        return False, (r.stderr or "")[:300], {}

    stripped: list[str] = []
    raw = strip_template(tex.read_text(encoding="utf-8"))
    raw = strip_missing_packages(raw, stripped)
    if stripped:
        for note in sorted(set(stripped)):
            print("   ·", note)
    proc = Processor(raw)
    tex.write_text(proc.run(), encoding="utf-8")
    unknown = dict(sorted(proc.unknown.items(), key=lambda kv: -kv[1]))
    return True, "", unknown


def main() -> int:
    global CMAPS
    CMAPS = load_cmaps()
    print("字体覆盖面：", {k: len(v) for k, v in CMAPS.items()})
    if len(sys.argv) > 1:
        md = Path(sys.argv[1])
        out = Path(sys.argv[2]) if len(sys.argv) > 2 else md.with_suffix(".tex")
        import pypandoc
        ok, err, unknown = md_to_tex(md, out, md.stem, pypandoc.get_pandoc_path())
        print("转换:", "✔" if ok else "✘ " + err)
        if unknown:
            print("无字体覆盖的字符：", unknown)
    return 0


if __name__ == "__main__":
    sys.exit(main())
