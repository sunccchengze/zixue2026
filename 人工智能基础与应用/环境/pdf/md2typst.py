#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""markdown → typst → PDF（讲义排版器）· Agent 维护 · B7

为什么自己写而不用 pandoc：
  1) pandoc 的 typst 数学转写有损（实测 \\langle x,y \\rangle 被改写成 (x,y)）；
  2) 表格/emoji/代码块样式不可控，而讲义是"读"的材料，排版就是内容；
  3) 自研转换器只依赖 PyPI 的 typst 包 + 字体文件，**编译期完全离线**。

设计要点：
  · 未知 LaTeX 命令 → 直接报错（绝不静默丢公式）——讲义里的公式都是知识锚点
  · emoji → 等宽符号（思源宋体不含 emoji，直接输出会变豆腐块）
  · 表格按内容长度自动分配列宽，跨页自动重复表头
  · 代码块用等宽字体 + 浅底 + 左侧色条；CJK 走字体回退

用法：
  python md2typst.py --all                 # 每份讲义各出一个 PDF → 讲义/pdf/
  python md2typst.py --book                # 合并成一本《讲义全书》+ 目录 + 版权页
  python md2typst.py --one M2              # 只做一个（文件名含 M2）
  python md2typst.py --check               # 只做语法体检，不编译
  python md2typst.py --book --preview 12   # 编译后顺便导出第 12 页 PNG 供肉眼检查
"""
from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SUBJECT = HERE.parent.parent          # 人工智能基础与应用/
LECTURE_DIR = SUBJECT / "讲义"
OUT_DIR = LECTURE_DIR / "pdf"
FONT_DIR = Path("/home/user/opt/fonts")   # 由 bootstrap.sh 准备；可用环境变量覆盖

SUBJECT_NAME = "人工智能基础与应用 · 大模型实训"
AUTHOR = "孙承泽 · 能动强基2501 · 西安交通大学"
BOOK_TITLE = "大模型实训讲义 · 全书"
BOOK_SUB = "从零实现大模型：M0–M9 知识主干（16 周 / 11 课题 / 零预算）"

W = 88  # 控制台输出宽度


# ────────────────────────────────────────────────────────────────────────────
# 1. 文本层：符号替换与 typst 转义
# ────────────────────────────────────────────────────────────────────────────

# emoji 在思源宋体/黑体里没有字形，直接输出会是豆腐块；换成等宽可用符号
SYMBOL_MAP = {
    "✅": "✔", "❌": "✘", "☑": "☑", "⚠️": "⚠", "🚨": "❗",
    "🟡": "◐", "🟢": "●", "🔴": "●", "⭐": "★", "🌟": "★",
    "🦙": "Llama", "📌": "▸", "💡": "☞", "🔧": "⚒", "🚧": "⚠",
    "🎯": "◎", "⏳": "◷", "🏁": "▶", "🔑": "⚿", "📖": "▤",
    "🧪": "▣", "📊": "▦", "🧠": "◈", "🛠": "⚒", "📝": "▤",
    "🇨": "C", "️⃣": "", "\ufe0f": "", "\u200d": "",
}

# typst 正文里需要转义的字符
_ESCAPE = {
    "\\": "\\\\", "#": "\\#", "$": "\\$", "*": "\\*", "_": "\\_",
    "`": "\\`", "<": "\\<", ">": "\\>", "@": "\\@", "[": "\\[",
    "]": "\\]", "~": "\\~",
}
# 注意：typst 里行首的 "-" "=" "+" 有语义，但只有行首才需要处理，正文中安全


def map_symbols(s: str) -> str:
    for k, v in SYMBOL_MAP.items():
        if k in s:
            s = s.replace(k, v)
    return s


def esc(s: str) -> str:
    """把普通文本转成安全的 typst 文本

    特别注意：typst 把 `//` 与 `/*` 当注释（markup 模式也一样），一旦出现就会
    静默吞掉后文——路径里的 `证据/*.yaml`、URL 里的 `https://` 都是活雷。
    所以 `/` 后紧跟 `*` 或 `/` 时必须转义成 `\\/`。
    """
    s = map_symbols(s)
    out: list[str] = []
    for i, ch in enumerate(s):
        if ch == "/" and i + 1 < len(s) and s[i + 1] in "*/":
            out.append("\\/")
        else:
            out.append(_ESCAPE.get(ch, ch))
    return "".join(out)


# ────────────────────────────────────────────────────────────────────────────
# 2. LaTeX 数学 → typst 数学
# ────────────────────────────────────────────────────────────────────────────

# 单命令 → typst 数学符号/函数
# 实测发现：typst 的符号「名字」随版本变动且不好猜（angle.l / dot.circle / diff
# 全都不存在），而**字面 Unicode 字符**在数学模式里一律可用并能被数学字体正确渲染。
# 所以策略是：能用字面字符的统统用字面字符；只有需要"带上下限排版"的才用函数名。
MATH_CMD = {
    # ——— 运算与关系符号：字面字符（实测可靠）———
    "times": "×", "cdot": "⋅", "odot": "⊙", "otimes": "⊗", "oplus": "⊕",
    "approx": "≈", "neq": "≠", "ne": "≠", "leq": "≤", "le": "≤",
    "geq": "≥", "ge": "≥", "equiv": "≡", "sim": "∼", "propto": "∝",
    "in": "∈", "notin": "∉", "subset": "⊂", "subseteq": "⊆",
    "cup": "∪", "cap": "∩", "setminus": "∖", "emptyset": "∅",
    "forall": "∀", "exists": "∃", "infty": "∞", "partial": "∂", "nabla": "∇",
    "top": "⊤", "bot": "⊥", "perp": "⊥", "pm": "±", "mp": "∓",
    "to": "→", "rightarrow": "→", "leftarrow": "←", "Rightarrow": "⇒",
    "Leftrightarrow": "⇔", "mapsto": "↦", "uparrow": "↑", "downarrow": "↓",
    "langle": "⟨", "rangle": "⟩", "lceil": "⌈", "rceil": "⌉",
    "lfloor": "⌊", "rfloor": "⌋", "mid": "∣", "vert": "|", "Vert": "‖",
    "ast": "∗", "star": "⋆", "circ": "∘", "bullet": "∙",
    "ll": "≪", "gg": "≫", "because": "∵", "therefore": "∴",
    # ——— 需要带上下限/正体排版：用 typst 函数名（实测可用）———
    "log": "log", "ln": "ln", "exp": "exp", "max": "max", "min": "min",
    "arg": "arg", "tanh": "tanh", "sin": "sin", "cos": "cos", "lim": "lim",
    "sum": "sum", "prod": "product", "int": "integral",
    "dots": "dots.h", "ldots": "dots.h", "cdots": "dots.h.c", "vdots": "dots.v",
    "quad": "quad", "qquad": "quad quad", ",": "thin", ";": "med", " ": "thin",
    "!": "",
    # ——— 希腊字母：typst 名字稳定（alpha…omega）———
    "alpha": "alpha", "beta": "beta", "gamma": "gamma", "delta": "delta",
    "epsilon": "epsilon", "varepsilon": "epsilon", "zeta": "zeta",
    "eta": "eta", "theta": "theta", "kappa": "kappa", "lambda": "lambda",
    "mu": "mu", "nu": "nu", "xi": "xi", "pi": "pi", "rho": "rho",
    "sigma": "sigma", "tau": "tau", "phi": "phi", "chi": "chi", "psi": "psi",
    "omega": "omega", "Delta": "Delta", "Theta": "Theta", "Lambda": "Lambda",
    "Sigma": "Sigma", "Phi": "Phi", "Omega": "Omega",
    "Pr": "Pr", "textnormal": None,  # None 走 \\text 分支
}

# 防御性补充：以后讲义里出现这些命令时不会因为"没映射"而中断导出。
# 原则不变——**没映射就直接报错**（绝不静默丢公式），这里只是把常见的一次补齐。
MATH_CMD.update({
    # 字体变体与特殊字母（字面 Unicode，实测在 typst 数学里可靠）
    "ell": "ℓ", "hbar": "ℏ", "Re": "ℜ", "Im": "ℑ", "wp": "℘", "aleph": "ℵ",
    "vartheta": "ϑ", "varphi": "ϕ", "varpi": "ϖ", "varrho": "ϱ", "varsigma": "ς",
    "mho": "℧", "eth": "ð", "S": "§", "P": "¶", "dag": "†", "ddag": "‡",
    # 符号
    "degree": "°", "celsius": "℃", "angle": "∠", "measuredangle": "∡",
    "triangle": "△", "square": "□", "blacksquare": "■", "surd": "√",
    "checkmark": "✓", "pounds": "£", "euro": "€", "yen": "¥", "permil": "‰",
    "prime": "′", "second": "″", "parallel": "∥", "nparallel": "∦",
    "simeq": "≃", "cong": "≅", "ncong": "≇", "asymp": "≍", "doteq": "≐",
    "lesssim": "≲", "gtrsim": "≳", "ll": "≪", "gg": "≫",
    "iff": "⟺", "implies": "⟹", "gets": "←", "leadsto": "⇝",
    "land": "and", "wedge": "and", "lor": "or", "vee": "or",
    "lnot": "not", "neg": "not", "colon": "med",
    # 函数名
    "gcd": "gcd", "det": "det", "dim": "dim", "ker": "ker", "deg": "deg",
    "bmod": "mod", "sup": "sup", "inf": "inf", "rank": "rank", "tr": "tr",
    # 排版控制（无视觉影响，吞掉即可）
    "displaystyle": "", "textstyle": "", "scriptstyle": "", "limits": "",
    "nolimits": "", "big": "", "Big": "", "bigg": "", "Bigg": "",
    "bigl": "", "bigr": "", "Bigl": "", "Bigr": "", "!" : "", " " : "thin",
})

MATH_BRACES = {"{": "brace.l", "}": "brace.r", "|": "bar.v", "#": "hash",
               "%": "percent", "$": "dollar", "&": "amp"}
# typst 数学里可直接书写的字符
MATH_SAFE = set("+-=<>/()[]!',.:;*|^_ abcdefghijklmnopqrstuvwxyz"
                "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")


class MathError(RuntimeError):
    pass


def _read_group(src: str, i: int) -> tuple[str, int]:
    """读一个 {..} 组或单个 token，返回 (内容, 新位置)"""
    while i < len(src) and src[i] == " ":
        i += 1
    if i < len(src) and src[i] == "{":
        depth, j = 1, i + 1
        while j < len(src) and depth:
            if src[j] == "{" and (j == 0 or src[j - 1] != "\\"):
                depth += 1
            elif src[j] == "}" and src[j - 1] != "\\":
                depth -= 1
            j += 1
        return src[i + 1:j - 1], j
    if i >= len(src):
        return "", i
    if src[i] == "\\":                      # \cmd 作为单 token
        m = re.match(r"\\[a-zA-Z]+|\\.", src[i:])
        return src[i:i + m.end()], i + m.end()
    return src[i], i + 1


def _join(pieces: list[str]) -> str:
    """拼接数学片段。

    typst 数学的一个硬规则：**连写的多个字母会被当成一个标识符**，未定义即报错
    （实测 `xy`、`QK`、`argmax` 全炸）。所以在「上一片以字母/数字结尾、下一片以
    字母开头」时必须补一个空格——空格在 typst 数学里就是"两个因子分开了"。
    """
    out = ""
    for p in pieces:
        if not p:
            continue
        # 前一片以字母/数字收尾、后一片以字母/数字起头 → 必须断开，
        # 否则 typst 会把它们粘成一个标识符（`QK`、`times12` 都是这么炸的）
        if out and out[-1].isalnum() and p[0].isalnum():
            out += " "
        out += p
    return out


def tex_math(src: str) -> str:
    """把讲义里用到的 LaTeX 数学子集翻译成 typst 数学。未知命令即报错。"""
    src = src.strip()
    out: list[str] = []
    i = 0
    while i < len(src):
        c = src[i]
        if c == "\\":
            m = re.match(r"\\([a-zA-Z]+|.)", src[i:])
            if not m:
                raise MathError(f"孤立的反斜杠：…{src[max(0,i-10):i+10]}…")
            cmd = m.group(1)
            i += m.end()
            if cmd in ("frac", "dfrac", "tfrac"):
                a, i = _read_group(src, i)
                b, i = _read_group(src, i)
                out.append(f"frac({tex_math(a)}, {tex_math(b)})")
            elif cmd == "sqrt":
                a, i = _read_group(src, i)
                out.append(f"sqrt({tex_math(a)})")
            elif cmd in ("text", "mathrm", "textnormal", "operatorname"):
                a, i = _read_group(src, i)
                out.append('"' + a.replace('"', "'") + '"')
            elif cmd in ("mathbb", "mathbf", "mathcal", "boldsymbol"):
                a, i = _read_group(src, i)
                fn = {"mathbb": "bb", "mathbf": "bold", "mathcal": "cal",
                      "boldsymbol": "bold"}[cmd]
                out.append(f"{fn}({tex_math(a)})")
            elif cmd == "vec":
                a, i = _read_group(src, i)
                out.append(f"arrow({tex_math(a)})")
            elif cmd in ("overline", "underline"):
                a, i = _read_group(src, i)
                out.append(f"{cmd}({tex_math(a)})")
            elif cmd in ("left", "right"):
                # \left( → lr(( ，\right) → ))
                # 注意：开闭括号要分别查表（早期版本只看开括号，导致 \right) 被吞掉）
                nxt = src[i] if i < len(src) else ""
                i += 1
                OPEN = {"(": "lr((", "[": "lr([", "{": "lr({", "|": "lr(|",
                        ".": "", "<": "lr(⟨"}
                CLOSE = {")": "))", "]": "])", "}": "})", "|": "|)",
                         ".": "", ">": "⟩)"}
                if cmd == "left" and nxt in OPEN:
                    out.append(OPEN[nxt])
                elif cmd == "right" and nxt in CLOSE:
                    out.append(CLOSE[nxt])
                else:
                    out.append("")
            elif cmd == ".":                      # \, \; \! \ 等间距
                out.append("thin")
            elif cmd in MATH_BRACES:              # \# \% \{ \} \| 等字面符号
                out.append(MATH_BRACES[cmd])
            elif cmd in MATH_CMD:
                v = MATH_CMD[cmd]
                out.append("" if v is None else v)
            else:
                raise MathError(f"未知 LaTeX 命令：\\{cmd}（出现在 {src!r}）")
        elif c in "^_":
            grp, i = _read_group(src, i + 1)
            out.append(f"{c}({tex_math(grp)})")
        elif c == "{":
            grp, i = _read_group(src, i)
            out.append(tex_math(grp))
        elif c in MATH_BRACES:
            out.append(MATH_BRACES[c])
            i += 1
        else:
            out.append(c)
            i += 1
    txt = _join(out)
    # 合并常见的 ^(2) → ^2 让观感更紧凑；后面必须不是字母/数字，否则会与后续
    # 标识符粘连（曾把 `w_t \mid` 粘成 `w_tmid` → typst 报 unknown variable）
    txt = re.sub(r"\^\((\w)\)(?![A-Za-z0-9])", r"^\1", txt)
    txt = re.sub(r"_\((\w)\)(?![A-Za-z0-9])", r"_\1", txt)
    return txt


# ────────────────────────────────────────────────────────────────────────────
# 3. 行内 markdown → typst
# ────────────────────────────────────────────────────────────────────────────

def raw_inline(code: str, lang: str | None = None) -> str:
    code = code.replace("\\", "\\\\").replace('"', '\\"')
    if lang:
        return f'#raw("{code}", lang: "{lang}")'
    return f'#raw("{code}")'


def inline(text: str) -> str:
    out: list[str] = []
    i, n = 0, len(text)
    while i < n:
        c = text[i]
        # markdown 反斜杠转义
        if c == "\\" and i + 1 < n and text[i + 1] in r"\`*_{}[]()#+-.!$~><|":
            out.append(esc(text[i + 1])); i += 2; continue
        # 行内代码
        if c == "`":
            j = text.find("`", i + 1)
            if j > i:
                out.append(raw_inline(text[i + 1:j])); i = j + 1; continue
        # 行内公式 / 块级公式（行内出现 $$...$$ 时也按行内处理）
        if text.startswith("$$", i):
            j = text.find("$$", i + 2)
            if j > i + 2:
                out.append("$ " + tex_math(text[i + 2:j]) + " $"); i = j + 2; continue
        if c == "$":
            j = text.find("$", i + 1)
            if j > i + 1:
                out.append("$" + tex_math(text[i + 1:j]) + "$"); i = j + 1; continue
        # 粗体 / 斜体
        # 不用 typst 的 `*...*` / `_..._`：实测 `③*bpb*` 这种「数字字符+星号+拉丁」
        # 会让 typst 判错强调边界并报 unclosed delimiter（中文里太容易踩）。
        # 函数式写法 #strong[..] / #emph[..] 没有边界歧义。
        if text.startswith("**", i):
            j = text.find("**", i + 2)
            if j > i + 2:
                out.append("#strong[" + inline(text[i + 2:j]) + "]"); i = j + 2; continue
        if c in "*_":
            j = text.find(c, i + 1)
            if j > i + 1:
                out.append("#emph[" + inline(text[i + 1:j]) + "]"); i = j + 1; continue
        # 链接
        if c == "[":
            m = re.match(r"\[([^\]]*)\]\(([^)\s]+)\)", text[i:])
            if m:
                label = m.group(1) or m.group(2)
                out.append(f'#link("{m.group(2)}")[{inline(label)}]')
                i += m.end(); continue
        # 删除线
        if text.startswith("~~", i):
            j = text.find("~~", i + 2)
            if j > i + 2:
                out.append("#strike[" + inline(text[i + 2:j]) + "]"); i = j + 2; continue
        out.append(esc(c)); i += 1
    return "".join(out)


# ────────────────────────────────────────────────────────────────────────────
# 4. 块级 markdown → typst
# ────────────────────────────────────────────────────────────────────────────

RE_HEAD = re.compile(r"^(#{1,6})\s+(.*)$")
RE_HR = re.compile(r"^\s*([-*_])\s*(\1\s*){2,}$")
RE_ULI = re.compile(r"^(\s*)([-*+])\s+(.*)$")
RE_OLI = re.compile(r"^(\s*)(\d+)[.)]\s+(.*)$")
RE_CODE = re.compile(r"^(\s*)```([^\s`]*)\s*$")
RE_QUOTE = re.compile(r"^>\s?(.*)$")
RE_TABLE = re.compile(r"^\s*\|.*\|\s*$")


def code_block(code: str, lang: str) -> str:
    code = code.rstrip("\n").replace("\\", "\\\\").replace('"', '\\"')
    langarg = f', lang: "{lang}"' if lang else ""
    return ("#block(width: 100%, above: 9pt, below: 9pt, inset: (x: 10pt, y: 8pt), "
            "radius: (right: 4pt), fill: luma(248), stroke: (left: 2.5pt + luma(165)))[\n"
            f'  #raw("{code}", block: true{langarg})\n]\n')


def table_block(rows: list[list[str]]) -> str:
    if not rows:
        return ""
    header, body = rows[0], rows[1:]
    ncol = max(len(r) for r in rows)
    # 依内容长度分配列宽（开方压缩，避免超长列吃掉整页）
    weights = []
    for c in range(ncol):
        m = max(len(r[c]) if c < len(r) else 0 for r in rows)
        weights.append(max(0.75, m ** 0.55))
    total = sum(weights)
    cols = ", ".join(f"{w / total:.3f}fr" for w in weights)

    def cells(row: list[str]) -> str:
        got = [inline(x) for x in row] + [""] * (ncol - len(row))
        return ", ".join(f"[{c}]" for c in got)

    lines = ["#block(width: 100%, above: 8pt, below: 10pt)[",
             "#text(size: 9pt)[", f"  #table(",
             f"    columns: ({cols}),",
             "    inset: (x: 7pt, y: 5pt),",
             "    align: left + top,",
             "    stroke: (x, y) => (bottom: if y == 0 { 0.9pt + luma(105) } "
             "else { 0.25pt + luma(220) }),",
             f"    table.header({cells(header)}),"]
    for row in body:
        lines.append(f"    {cells(row)},")
    lines += ["  )", "]", "]"]
    return "\n".join(lines) + "\n"


def list_block(items: list[tuple[int, str, str]]) -> str:
    """items: (层级, 类型('ul'|'ol'), 文本)"""
    out: list[str] = []
    stack: list[int] = []          # 各级缩进
    for level, kind, text in items:
        if not stack:
            stack.append(level)
        elif level > stack[-1]:
            stack.append(level)
        else:
            while len(stack) > 1 and level < stack[-1]:
                stack.pop()
        depth = len(stack) - 1
        pad = "  " * depth
        marker = "-" if kind == "ul" else "+"
        item = inline(text)
        if text.strip().startswith("[ ] "):
            item = "□ " + inline(text.strip()[4:])
        elif text.strip().lower().startswith("[x] "):
            item = "☑ " + inline(text.strip()[4:])
        out.append(f"{pad}{marker} {item}")
    return "\n".join(out) + "\n"


def convert(lines: list[str]) -> str:
    out: list[str] = []
    i, n = 0, len(lines)
    while i < n:
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            i += 1
            continue

        # 代码块 / raw 块
        m = RE_CODE.match(line)
        if m:
            lang = m.group(2)
            i += 1
            buf: list[str] = []
            while i < n and not re.match(r"^\s*```\s*$", lines[i]):
                buf.append(lines[i]); i += 1
            i += 1
            if lang.startswith("{="):
                # raw_attribute：只有 typst 的原样保留，别的格式（openxml/latex/docx）
                # 在 typst 输出里直接丢弃，避免把 XML 当正文排进去
                if "typst" in lang:
                    out.append("\n".join(buf) + "\n")
                continue
            out.append(code_block("\n".join(buf), lang))
            continue

        # 标题
        m = RE_HEAD.match(line)
        if m:
            lvl = len(m.group(1))
            out.append("=" * lvl + " " + inline(m.group(2).strip()) + "\n")
            i += 1
            continue

        # 分隔线
        if RE_HR.match(line):
            out.append("#v(4pt)\n#line(length: 100%, stroke: 0.6pt + luma(200))\n#v(4pt)\n")
            i += 1
            continue

        # 引用块
        if RE_QUOTE.match(line):
            buf = []
            while i < n and RE_QUOTE.match(lines[i]):
                buf.append(RE_QUOTE.match(lines[i]).group(1)); i += 1
            inner = convert(buf).strip()
            out.append(
                "#block(width: 100%, above: 9pt, below: 9pt, "
                "inset: (left: 12pt, right: 8pt, y: 6pt), "
                "stroke: (left: 3pt + luma(180)), fill: luma(252))[\n"
                f"#text(size: 9.8pt)[\n{inner}\n]\n]\n")
            continue

        # 表格
        if RE_TABLE.match(line):
            rows: list[list[str]] = []
            while i < n and RE_TABLE.match(lines[i]):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c != ""):
                    rows.append(cells)
                i += 1
            out.append(table_block(rows))
            continue

        # 列表
        if RE_ULI.match(line) or RE_OLI.match(line):
            items: list[tuple[int, str, str]] = []
            while i < n:
                cur = lines[i]
                mu, mo = RE_ULI.match(cur), RE_OLI.match(cur)
                if mu:
                    items.append((len(mu.group(1)), "ul", mu.group(3)))
                elif mo:
                    items.append((len(mo.group(1)), "ol", mo.group(3)))
                elif cur.strip() and cur.startswith(("  ", "\t")) and items:
                    lv, kd, tx = items[-1]                 # 续行并入上一项
                    items[-1] = (lv, kd, tx + " " + cur.strip())
                else:
                    break
                i += 1
            out.append(list_block(items))
            continue

        # 段落
        buf = [line.strip()]
        i += 1
        while i < n and lines[i].strip() and not any(
                r.match(lines[i]) for r in (RE_HEAD, RE_HR, RE_QUOTE, RE_TABLE,
                                            RE_ULI, RE_OLI, RE_CODE)):
            if lines[i - 1].endswith("  "):      # markdown 硬换行
                buf.append("#linebreak()")
            buf.append(lines[i].strip())
            i += 1
        out.append(inline(" ".join(buf)) + "\n")
    return "\n".join(out)


# ────────────────────────────────────────────────────────────────────────────
# 5. typst 模板
# ────────────────────────────────────────────────────────────────────────────

PREAMBLE = r"""
// ══ 讲义排版模板（由 md2typst.py 生成，请勿手改）══
#set document(title: "{doc_title}", author: "{author}")

// 字体回退链：CJK → 拉丁兜底 → 单色 emoji（讲义里偶尔出现 emoji 或方块字符）
#let SERIF = ("Noto Serif SC", "DejaVu Sans", "Noto Emoji")
#let SANS  = ("Noto Sans SC", "DejaVu Sans", "Noto Emoji")
#let MONO  = ("DejaVu Sans Mono", "Noto Sans SC", "Noto Emoji")
#let ACCENT = rgb("#1d4e6b")
#let ACCENT2 = rgb("#2c6f92")

#set page(
  paper: "a4",
  margin: (x: 1.95cm, top: 2.05cm, bottom: 2.0cm),
  header-ascent: 1em,
  header: context {
    let h = query(selector(heading.where(level: 1)).before(here()))
    if h.len() > 0 and here().page() > 1 {
      set text(size: 8pt, fill: luma(140), font: SANS)
      align(right)[#h.last().body]
      v(-0.6em)
      line(length: 100%, stroke: 0.4pt + luma(215))
    }
  },
  footer: context {
    set text(size: 8.5pt, fill: luma(130), font: SANS)
    align(center)[— #counter(page).display() —]
  },
)

#set text(font: SERIF, size: 10.5pt, lang: "zh", region: "cn", hyphenate: false)
#set par(justify: true, leading: 1.02em, spacing: 0.95em, first-line-indent: 0em)
#set raw(tab-size: 2)
#show raw: set text(font: MONO, size: 8.3pt, fill: luma(35))
#show link: set text(fill: ACCENT2)

#show heading: set text(font: SANS, weight: "bold", fill: ACCENT)
#show heading.where(level: 1): it => {
  pagebreak(weak: true)
  v(0.25em)
  block(width: 100%)[
    #text(size: 19.5pt, fill: ACCENT)[#it.body]
    #v(3pt)
    #line(length: 100%, stroke: 1.3pt + ACCENT)
  ]
  v(0.8em)
}
#show heading.where(level: 2): it => block(above: 1.25em, below: 0.55em, width: 100%)[
  #text(size: 13.5pt, fill: ACCENT2)[#it.body]
]
#show heading.where(level: 3): it => block(above: 1.0em, below: 0.45em)[
  #text(size: 11.5pt, fill: rgb("#33566b"))[#it.body]
]
#show heading.where(level: 4): it => block(above: 0.9em, below: 0.4em)[
  #text(size: 10.5pt, fill: rgb("#33566b"))[#it.body]
]
"""


def cover(title: str, subtitle: str, extra: str = "") -> str:
    today = dt.date.today().isoformat()
    extra_line = f"\n    #v(0.5cm)\n    #text(size: 9.5pt, fill: luma(110))[{extra}]" if extra else ""
    return f"""#[
  #set page(header: none, footer: none)
  #v(3.0cm)
  #align(center)[
    #text(font: SANS, size: 12pt, fill: luma(110), tracking: 0.15em)[{esc(SUBJECT_NAME)}]
    #v(1.4cm)
    #text(font: SANS, size: 27pt, weight: "bold", fill: ACCENT)[{esc(title)}]
    #v(0.5cm)
    #text(font: SANS, size: 12.5pt, fill: ACCENT2)[{esc(subtitle)}]
    #v(1.0cm)
    #line(length: 45%, stroke: 0.8pt + luma(150))
    #v(1.0cm)
    #text(size: 11pt, fill: luma(70))[{esc(AUTHOR)}]
    #v(0.25cm)
    #text(size: 9.5pt, fill: luma(130))[{today} 生成　·　版本 v1.0]{extra_line}
  ]
  #v(4.4cm)
  #align(center)[
    #text(size: 8.5pt, fill: luma(150), font: SANS)[Markdown 母版：人工智能基础与应用/讲义/ 下的 .md 文件　·　配套上游：CS336 A1–A5 · nanochat · minimind]
  ]
  #pagebreak()
]
"""


COLOPHON = r"""#[
  #set heading(numbering: none)
  = 版权与使用说明
  #text(size: 9.5pt)[
  *这是什么。* 本 PDF 是「人工智能基础与应用 · 大模型实训」知识轨的讲义合集，由 `讲义/*.md` 自动排版生成。
  讲义与课题一一对应：每讲都由「要回答的问题 → 主干 → 伪代码骨架 → 代码在哪里 → 常见误解 → 能立刻跑的实验 → 代码级提问 → 记忆锚」八件套组成。
  *为什么以 Markdown 为母版。* PDF 便于通读与打印，但**唯一真相是仓库里的 `.md`**：
  内容修订、代码定位、实验数据只改 Markdown，PDF 随时重新生成。看到 PDF 与仓库不一致时，以仓库为准。

  *重新生成。*

  ```bash
  cd 人工智能基础与应用
  环境/pdf/生成讲义PDF.sh --book      # 生成全书
  环境/pdf/生成讲义PDF.sh --all       # 每讲各出一个 PDF
  ```

  *字体与排版。* 正文思源宋体（Noto Serif SC），标题思源黑体（Noto Sans SC），代码 DejaVu Sans Mono；
  三者均按 SIL OFL 1.1 / Bitstream Vera 许可授权，可自由再分发。排版引擎 typst 0.15。
  字体文件由 `环境/pdf/bootstrap.sh` 从 npm（\@expo-google-fonts 系列）取得，编译过程完全离线。

  *读法建议。* 先读每讲开头的「要回答的问题」，自己试着答一遍；再读对标名师的原始材料（见《对标教学资源清单》）；
  然后回到本讲义看主干与代码定位；最后做「代码级提问」并写下预测，再动手改代码验证。
  预测错不是失败——#strong[预测错 + 实验打脸]才是这套学法里质量最高的时刻。
  ]
  #pagebreak()
]
"""


def title_toc() -> str:
    return """#[
  = 目录
  #show outline.entry.where(level: 1): set text(weight: "bold", size: 11pt, fill: ACCENT)
  #show outline.entry.where(level: 2): set text(size: 9.8pt, fill: luma(60))
  #outline(title: none, depth: 2, indent: 1.15em)
  #pagebreak()
]
"""


def typst_str(s: str) -> str:
    """放进 typst 字符串字面量里用的转义（标题里可能有中文引号/英文引号）"""
    return s.replace("\\", "\\\\").replace('"', '\\"')


def build_typst(doc_title: str, body: str, with_cover: bool = True,
                subtitle: str = "", pre: str = "") -> str:
    head = (PREAMBLE.replace("{doc_title}", typst_str(doc_title))
                    .replace("{author}", typst_str(AUTHOR)))
    parts = [head]
    if with_cover:
        parts.append(cover(doc_title, subtitle or BOOK_SUB))
    parts.append(pre)
    parts.append(body)
    return "\n".join(parts)


# ────────────────────────────────────────────────────────────────────────────
# 6. CLI
# ────────────────────────────────────────────────────────────────────────────

def md_to_typst_body(path: Path) -> str:
    return convert(path.read_text(encoding="utf-8").splitlines())


def doc_title_of(path: Path) -> str:
    for line in path.read_text(encoding="utf-8").splitlines():
        m = RE_HEAD.match(line)
        if m and len(m.group(1)) == 1:
            return m.group(2).strip()
    return path.stem


def lecture_files() -> list[Path]:
    """讲义正文顺序：README 说明 → M0 → M1 → M2 → M3 → M4–M9 大纲"""
    order = ["README.md", "M0-数学与机器学习地基.md", "M1-从n-gram到Transformer.md",
             "M2-分词与表示.md", "M3-Transformer内部机制.md", "M4-M9-待展开大纲.md"]
    files = [LECTURE_DIR / f for f in order if (LECTURE_DIR / f).exists()]
    extra = sorted(p for p in LECTURE_DIR.glob("*.md") if p.name not in order)
    return files + extra


_CMAP_CACHE: dict[str, set[int]] = {}


def font_cmap(name: str) -> set[int]:
    """读字体里实际有的码位（字体已子集化，缺字必须报出来而不是出豆腐块）"""
    if name in _CMAP_CACHE:
        return _CMAP_CACHE[name]
    from fontTools.ttLib import TTFont
    p = FONT_DIR / name
    codes: set[int] = set()
    if p.exists():
        f = TTFont(p, lazy=True)
        for t in f["cmap"].tables:
            codes |= set(t.cmap.keys())
        f.close()
    _CMAP_CACHE[name] = codes
    return codes


def glyph_check(paths: list[Path]) -> int:
    """字形覆盖自检：正文/标题（宋体链）与代码（等宽链）各查一遍"""
    chains = {
        "正文/标题": ["NotoSerifSC-Regular.ttf", "NotoSansSC-Regular.ttf",
                     "DejaVuSans.ttf", "NotoEmoji-Regular.ttf"],
        "代码块": ["DejaVuSansMono.ttf", "NotoSansSC-Regular.ttf", "NotoEmoji-Regular.ttf"],
    }
    have = {label: set().union(*(font_cmap(n) for n in names))
            for label, names in chains.items()}
    bad = 0
    for f in paths:
        text = f.read_text(encoding="utf-8")
        body = re.sub(r"```.*?```", "", text, flags=re.S)
        code = "".join(re.findall(r"```.*?\n(.*?)```", text, flags=re.S))
        for label, chunk in (("正文/标题", body), ("代码块", code)):
            # 行内代码里的字符同样走等宽链
            missing = sorted({c for c in chunk if len(c) == 1 and ord(c) > 0x20
                              and ord(c) not in have[label]})
            if missing:
                show = "".join(missing[:24])
                print(f"  ⚠ [{f.name} · {label}] {len(missing)} 个字符无字形（会渲染成豆腐块）：{show}")
                print(f"      U+{' U+'.join(f'{ord(c):04X}' for c in missing[:12])}")
                bad += 1
    if bad == 0:
        print("  ✔ 字形覆盖自检通过（讲义用到的字符全在字体链里）")
    return bad


def extract_math(paths: list[Path]) -> list[tuple[str, str]]:
    """抽出讲义里所有数学片段（跳过代码块）"""
    spans: list[tuple[str, str]] = []
    for f in paths:
        t = re.sub(r"```.*?```", "", f.read_text(encoding="utf-8"), flags=re.S)
        for m in re.findall(r"\$\$(.+?)\$\$", t, flags=re.S):
            spans.append((f.name, m))
        for m in re.findall(r"(?<!\$)\$([^$\n]+)\$(?!\$)", t):
            spans.append((f.name, m))
    return spans


def check_math(paths: list[Path]) -> int:
    """逐条把公式单独编译一遍——公式是讲义的知识锚点，一条都不能默默坏掉"""
    import typst
    spans = extract_math(paths)
    uniq: dict[str, str] = {}
    bad = 0
    for name, m in spans:
        try:
            uniq.setdefault(tex_math(m), name)
        except MathError as exc:
            print(f"  ✘ [{name}] 翻译失败：{exc}")
            bad += 1
    print(f"  公式：共 {len(spans)} 处，去重 {len(uniq)} 条，正在逐条编译…")
    for k, (typ, name) in enumerate(uniq.items()):
        p = Path(f"/tmp/math_{k}.typ")
        p.write_text(f"#set text(font: (\"Noto Serif SC\",))\n$ {typ} $\n", encoding="utf-8")
        try:
            typst.compile(str(p), output=f"/tmp/math_{k}.pdf", font_paths=[str(FONT_DIR)])
        except Exception as exc:                      # noqa: BLE001
            print(f"  ✘ [{name}] typst 编译失败：{str(exc).strip().splitlines()[0]}")
            print(f"      公式：{typ[:120]}")
            bad += 1
    if bad == 0:
        print("  ✔ 全部公式可独立编译")
    return bad


def compile_pdf(typ: str, out: Path) -> tuple[bool, str]:
    import typst
    tmp = out.with_suffix(".typ")
    tmp.write_text(typ, encoding="utf-8")
    try:
        typst.compile(str(tmp), output=str(out), font_paths=[str(FONT_DIR)])
        return True, ""
    except Exception as exc:                       # noqa: BLE001
        return False, str(exc)


def preview(pdf: Path, page: int, out_png: Path | None = None) -> Path | None:
    import pymupdf
    doc = pymupdf.open(pdf)
    if page < 1 or page > doc.page_count:
        return None
    png = out_png or pdf.with_name(f"{pdf.stem}-p{page}.png")
    doc[page - 1].get_pixmap(dpi=115).save(str(png))
    return png


def heading_gaps(md: Path, pdf: Path) -> list[str]:
    """章节齐备性自检：markdown 里的每个二级/三级标题都必须出现在 PDF 里。

    这是防止「排版悄悄吞内容」的最后一道闸——比肉眼看几页可靠。
    """
    import pymupdf
    text = "".join(p.get_text() for p in pymupdf.open(pdf))
    flat = re.sub(r"[^0-9A-Za-z\u4e00-\u9fff]", "", text)
    missing = []
    for line in md.read_text(encoding="utf-8").splitlines():
        m = RE_HEAD.match(line)
        if not m or len(m.group(1)) not in (1, 2, 3):
            continue
        title = re.sub(r"[*`$]", "", m.group(2)).strip()
        if "$" in m.group(2):        # 标题里含公式：公式在 PDF 里渲染成排版字形，
            title = m.group(2).split("$")[0]   # 只核对公式之前那一段中文
        if len(title) < 4:
            continue
        # 指纹 = 只留中文与字母数字后的整条标题。引号、破折号、顿号在 PDF 里
        # 的字体与写法与 markdown 不同，留着就会假报缺失。
        probe = re.sub(r"[^0-9A-Za-z\u4e00-\u9fff]", "", title)
        if len(probe) >= 4 and probe not in flat:
            missing.append(title[:40])
    return missing


def report(ok: bool, out: Path, err: str = "", md: Path | None = None) -> None:
    if ok:
        kb = out.stat().st_size / 1024
        try:
            import pymupdf
            pages = pymupdf.open(out).page_count
        except Exception:                          # noqa: BLE001
            pages = -1
        gaps = heading_gaps(md, out) if md else []
        flag = "" if not gaps else f"  ⚠ 缺 {len(gaps)} 个标题：{gaps[:3]}"
        print(f"  ✔ {out.name:<42} {pages:>4} 页 {kb:>6.0f} KB{flag}")
    else:
        print(f"  ✘ {out.name:<44} 编译失败")
        print("    " + (err.strip().splitlines() or [""])[0][:200])
        for line in err.strip().splitlines()[1:14]:
            print("    " + line[:200])


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true", help="每份讲义各出一个 PDF")
    ap.add_argument("--book", action="store_true", help="合并全书（含封面/版权页/目录）")
    ap.add_argument("--charter", action="store_true", help="另出《章程与地图》分册（本学科宪法层）")
    ap.add_argument("--one", metavar="KEY", help="只处理文件名含 KEY 的一份")
    ap.add_argument("--check", action="store_true", help="只做转换体检，不编译")
    ap.add_argument("--preview", type=int, metavar="PAGE", help="导出该页 PNG 供肉眼检查")
    ap.add_argument("--out", default=str(OUT_DIR), help="输出目录")
    a = ap.parse_args()

    if not FONT_DIR.exists():
        print(f"✘ 找不到字体目录 {FONT_DIR}，请先运行 环境/pdf/bootstrap.sh")
        return 2
    out_dir = Path(a.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    files = lecture_files()
    if a.one:
        files = [f for f in files if a.one in f.name]
    if not files:
        print("✘ 没有匹配的讲义文件"); return 2
    if not (a.all or a.book or a.one or a.check or a.charter):
        a.all = True

    problems = 0
    print(f"讲义源：{LECTURE_DIR}")
    glyph_check(files)

    # 体检（并把转换结果打印出来，便于定位）
    bodies: dict[str, str] = {}
    for f in files:
        try:
            bodies[f.name] = md_to_typst_body(f)
        except MathError as exc:
            print(f"  ✘ {f.name}：{exc}")
            problems += 1
    if problems:
        print(f"\n✘ 有 {problems} 个文件存在无法翻译的公式，已中止（绝不静默丢公式）")
        return 1
    if a.check:
        print("  ✔ 结构可翻译；开始字体与公式体检")
        problems += glyph_check(files)
        problems += check_math(files)
        return 1 if problems else 0

    def single_title(f: Path) -> str:
        # 封面大标题不再重复"讲义"二字（H1 里已含），副标题统一用课程定位
        return re.sub(r"^讲义\s*", "", doc_title_of(f)).strip() or f.stem

    if a.one:
        f = files[0]
        t = build_typst(single_title(f), bodies[f.name], subtitle=BOOK_SUB)
        out = out_dir / (f.stem + ".pdf")
        ok, err = compile_pdf(t, out)
        report(ok, out, err, md=f)
        if ok and a.preview:
            png = preview(out, a.preview)
            print(f"    ↳ 预览图：{png}")
        return 0 if ok else 1

    if a.all:
        for f in files:
            t = build_typst(single_title(f), bodies[f.name], subtitle=BOOK_SUB)
            out = out_dir / (f.stem + ".pdf")
            ok, err = compile_pdf(t, out)
            report(ok, out, err, md=f)
            problems += 0 if ok else 1
            if ok and a.preview:
                preview(out, a.preview)

    if a.book:
        body = "\n#pagebreak()\n".join(bodies[f.name] for f in files)
        t = build_typst(BOOK_TITLE, body, subtitle=BOOK_SUB, pre=COLOPHON + title_toc())
        out = out_dir / "大模型实训讲义-全书.pdf"
        ok, err = compile_pdf(t, out)
        report(ok, out, err)
        problems += 0 if ok else 1
        if ok and a.preview:
            png = preview(out, a.preview)
            print(f"    ↳ 预览图：{png}")

    if a.charter:
        cdir = SUBJECT / "章程与地图"
        order = ["知识地图-大模型全景.md", "对标教学资源清单.md", "知行合一规程.md",
                 "实训路线图.md", "造轮子边界.md", "AI使用红线.md",
                 "算力与成本预算.md", "判分与验收标准.md", "上游锁定清单.md"]
        cfs = [cdir / f for f in order if (cdir / f).exists()]
        cfs += [p for p in sorted(cdir.glob("*.md")) if p.name not in order]
        try:
            cbodies = [md_to_typst_body(f) for f in cfs]
        except MathError as exc:
            print(f"  ✘ 章程排版失败：{exc}"); return 1
        cbody = "\n#pagebreak()\n".join(cbodies)
        cout = cdir / "pdf"
        cout.mkdir(parents=True, exist_ok=True)
        t = build_typst("章程与地图 · 全书", cbody,
                        subtitle="本学科的宪法层：学什么 / 跟谁学 / 什么叫学过 / 何时学 / 谁写代码",
                        pre=title_toc())
        out = cout / "章程与地图-全书.pdf"
        ok, err = compile_pdf(t, out)
        report(ok, out, err)
        problems += 0 if ok else 1
        if ok and a.preview:
            png = preview(out, a.preview)
            print(f"    ↳ 预览图：{png}")

    if problems:
        print(f"\n✘ {problems} 个输出失败")
        return 1
    print(f"\n✔ 完成 → {out_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
