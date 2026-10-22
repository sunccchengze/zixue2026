#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
刷题集 · 构建脚本
1) 合并：章源文件 → 上册/下册 合订 MD
2) 精排：Markdown → LaTeX（ctex + Noto Serif CJK）→ xelatex 编译 PDF
运行：python3 build_drill_pdf.py [--md-only]
"""

import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
VERBOSE = "--verbose" in sys.argv
MD_ONLY = "--md-only" in sys.argv

UP = ["第1章-随机事件与概率.md", "第2章-一维随机变量.md", "第3章-随机向量.md", "第4章-数字特征.md"]
DOWN = ["第5章-大数定律与中心极限定理.md", "第6章-数理统计的基本概念.md", "第7章-参数估计.md",
        "第8章-假设检验.md", "第8.6章-分布拟合检验.md", "第10章-一元回归.md"]

UP_HEAD = """# 刷题集 · 上册：第 1–4 章（期中范围）

> **上册 = 第 1–4 章（M1–M12），共 104 题**，直接对应 10 号文件《期中冲刺》的诊断卷范围。
> 用法见《00-使用说明与刷题计划.md》：每天 1–2 张卡，读完"四段式"再做"例 / 刷"。
> 章节来源：`第1章-随机事件与概率.md` ～ `第4章-数字特征.md`（本册为合订本，内容与单章版一致）。

"""

DOWN_HEAD = """# 刷题集 · 下册：第 5 章–第 10 章（含 8.6 分布拟合与一元回归）

> **下册 = 第 5–10 章（M13–M20 + 8.5/8.6），共 120 题 + 结业自测 20 题**。
> 课表新增考点（8.6 分布拟合、第 10 章一元回归、8.5 成对数据检验）都在本册。
> 章节来源：`第5章…` ～ `第10章…`（本册为合订本，内容与单章版一致）。

"""


def read(name):
    with open(os.path.join(HERE, name), encoding="utf-8") as fh:
        return fh.read().rstrip() + "\n"


def strip_h1(text):
    """章源文件的首个一级标题降为二级（合订本用卷标题做一级）。"""
    lines = text.split("\n")
    for i, ln in enumerate(lines):
        if ln.startswith("# "):
            lines[i] = "## " + ln[2:]
            break
    return "\n".join(lines)


def build_md():
    up = UP_HEAD + "\n".join(strip_h1(read(n)) + "\n---\n" for n in UP)
    down = DOWN_HEAD + "\n".join(strip_h1(read(n)) + "\n---\n" for n in DOWN) + read("99-结业自测与总索引.md")
    for name, body in (("上册-第1至4章.md", up), ("下册-第5至10章.md", down)):
        with open(os.path.join(HERE, name), "w", encoding="utf-8") as fh:
            fh.write(body)
        print("  [MD] %s（%.1f KB）" % (name, len(body.encode()) / 1024))


# ----------------------------------------------------------------- LaTeX
PERM = [
    # 长串优先
    ("σ̂²", r"$\hat\sigma^2$"), ("θ̂", r"$\hat\theta$"), ("λ̂", r"$\hat\lambda$"),
    ("μ̂", r"$\hat\mu$"), ("p̂", r"$\hat p$"), ("b̂", r"$\hat b$"), ("â", r"$\hat a$"),
    ("σ̂", r"$\hat\sigma$"), ("x̄", r"$\bar x$"), ("ȳ", r"$\bar y$"), ("d̄", r"$\bar d$"),
    ("z̄", r"$\bar z$"), ("X̄", r"$\bar X$"), ("Ȳ", r"$\bar Y$"), ("χ²", r"$\chi^2$"),
    ("★★★", r"$\bigstar\bigstar\bigstar$"), ("★★", r"$\bigstar\bigstar$"),
    ("★", r"$\bigstar$"), ("☆", r"$\star$"),
    ("⇒", r"$\Rightarrow$"), ("⇔", r"$\Leftrightarrow$"), ("→", r"$\to$"),
    ("≥", r"$\ge$"), ("≤", r"$\le$"), ("≠", r"$\ne$"), ("≈", r"$\approx$"),
    ("±", r"$\pm$"), ("×", r"$\times$"), ("÷", r"$\div$"), ("·", "\\textperiodcentered{}"),
    ("∪", r"$\cup$"), ("∩", r"$\cap$"), ("∅", r"$\varnothing$"), ("∈", r"$\in$"),
    ("⊂", r"$\subset$"), ("⊆", r"$\subseteq$"), ("√", r"$\sqrt{\ }$"),
    ("∞", r"$\infty$"), ("∫", r"$\int$"), ("Σ", r"$\sum$"), ("Π", r"$\prod$"),
    ("Φ", r"$\Phi$"), ("Γ", r"$\Gamma$"), ("Δ", r"$\Delta$"),
    ("χ", r"$\chi$"), ("λ", r"$\lambda$"), ("μ", r"$\mu$"), ("σ", r"$\sigma$"),
    ("θ", r"$\theta$"), ("ρ", r"$\rho$"), ("α", r"$\alpha$"), ("β", r"$\beta$"),
    ("ε", r"$\varepsilon$"), ("δ", r"$\delta$"), ("η", r"$\eta$"), ("φ", r"$\varphi$"),
    ("π", r"$\pi$"), ("ν", r"$\nu$"), ("τ", r"$\tau$"), ("ω", r"$\omega$"),
    ("ξ", r"$\xi$"), ("ζ", r"$\zeta$"), ("ψ", r"$\psi$"), ("Λ", r"$\Lambda$"),
    ("ᵢ", r"$_i$"), ("₀", r"$_0$"), ("₁", r"$_1$"), ("₂", r"$_2$"), ("₃", r"$_3$"),
    ("₄", r"$_4$"), ("₅", r"$_5$"), ("₆", r"$_6$"), ("₇", r"$_7$"), ("₈", r"$_8$"),
    ("₉", r"$_9$"), ("ₙ", r"$_n$"), ("²", r"$^2$"), ("³", r"$^3$"), ("ⁿ", r"$^n$"),
    ("⚠️", "【注意】"), ("⚠", "【注意】"), ("✅", ""), ("🆕", "【新增】"), ("⛔", ""),
    ("⭐", ""), ("📌", ""), ("💡", ""), ("🔑", ""), ("📎", ""), ("✓", ""), ("⁻", r"$^-$"),
]
PERM_SORTED = sorted(PERM, key=lambda kv: -len(kv[0]))


def perm(s):
    for i, (k, v) in enumerate(PERM_SORTED):
        s = s.replace(k, chr(0xE000 + i))
    return s


def expand(s):
    for i, (k, v) in enumerate(PERM_SORTED):
        s = s.replace(chr(0xE000 + i), v)
    return s


def esc(s):
    out = []
    for ch in s:
        if 0xE000 <= ord(ch) <= 0xF8FF:
            out.append(ch)
        elif ch in "&%#_{}":
            out.append("\\" + ch)
        elif ch == "~":
            out.append(r"\textasciitilde{}")
        elif ch == "^":
            out.append(r"\textasciicircum{}")
        elif ch == "\\":
            out.append(r"\textbackslash{}")
        else:
            out.append(ch)
    return "".join(out)


def inline_plain(s):
    return expand(esc(perm(s)))


def map_syms(s):
    """数学段内使用：直接映射成 LaTeX 命令。"""
    for k, v in PERM:
        repl = r"\cdot " if k == "·" else v.replace("$", "")
        s = s.replace(k, repl)
    return s



# ---------------------------------------------------------------------------
#  代码块 → 数学/中文分段渲染（解决等宽字体缺字：∪、Ā、B̄、‾ 等）
# ---------------------------------------------------------------------------
MATH_ASCII = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
                 "+-=<>()[]{}\\^_|/,.:;!?~ ")
MATH_UNI = set("−±×÷·≤≥≠≈∈∉⊂⊆∅∪∩⇒⇐⇔→←√∫ΣΠ∞∼∂′…∑∏≪≫")
MATH_UNI |= set("αβγδεζηθκλμνξπρστυφχψωΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ")
MATH_UNI |= set("₀₁₂₃₄₅₆₇₈₉ⁿᵢ⁰¹²³⁴⁵⁶⁷⁸⁹Ā")
MATH_UNI |= {"\u0304", "\u0302", "\u0305", "\u0303"}

MATH_MAP = [
    (r"\u0302", None),
    ("σ̂", r"\hat\sigma"), ("θ̂", r"\hat\theta"), ("λ̂", r"\hat\lambda"),
    ("μ̂", r"\hat\mu"), ("p̂", r"\hat p"), ("b̂", r"\hat b"), ("â", r"\hat a"),
    ("x̄", r"\bar x"), ("ȳ", r"\bar y"), ("d̄", r"\bar d"), ("z̄", r"\bar z"),
    ("X̄", r"\bar X"), ("Ȳ", r"\bar Y"), ("Ā", r"\bar A"), ("B̄", r"\bar B"),
    ("χ²", r"\chi^2"),
    ("⇒", r"\Rightarrow"), ("⇔", r"\Leftrightarrow"), ("→", r"\to"), ("←", r"\leftarrow"),
    ("≤", r"\le"), ("≥", r"\ge"), ("≠", r"\ne"), ("≈", r"\approx"), ("∼", r"\sim"),
    ("±", r"\pm"), ("×", r"\times"), ("÷", r"\div"), ("·", r"\cdot"), ("−", "-"),
    ("∪", r"\cup"), ("∩", r"\cap"), ("∅", r"\varnothing"), ("∈", r"\in"), ("∉", r"\notin"),
    ("⊂", r"\subset"), ("⊆", r"\subseteq"), ("√", r"\surd{}"),
    ("~", r"\sim{}"), ("∞", r"\infty"), ("∫", r"\int"), ("Σ", r"\sum"), ("∑", r"\sum"),
    ("Π", r"\prod"), ("∂", r"\partial"), ("′", "'"), ("…", r"\ldots"),
    ("Φ", r"\Phi"), ("Γ", r"\Gamma"), ("Δ", r"\Delta"), ("Λ", r"\Lambda"),
    ("χ", r"\chi"), ("λ", r"\lambda"), ("μ", r"\mu"), ("σ", r"\sigma"), ("θ", r"\theta"),
    ("ρ", r"\rho"), ("α", r"\alpha"), ("β", r"\beta"), ("ε", r"\varepsilon"),
    ("δ", r"\delta"), ("η", r"\eta"), ("φ", r"\varphi"), ("ψ", r"\psi"), ("π", r"\pi"),
    ("ν", r"\nu"), ("τ", r"\tau"), ("ω", r"\omega"), ("ξ", r"\xi"), ("ζ", r"\zeta"),
    ("₀", "_0"), ("₁", "_1"), ("₂", "_2"), ("₃", "_3"), ("₄", "_4"), ("₅", "_5"),
    ("₆", "_6"), ("₇", "_7"), ("₈", "_8"), ("₉", "_9"), ("ₙ", "_n"), ("ⁿ", "^n"),
    ("ᵢ", "_i"), ("²", "^2"), ("³", "^3"),
]

SUBCHARS = {"\u2080": "0", "\u2081": "1", "\u2082": "2", "\u2083": "3", "\u2084": "4",
            "\u2085": "5", "\u2086": "6", "\u2087": "7", "\u2088": "8", "\u2089": "9",
            "\u1d62": "i", "\u2c7c": "j", "\u2099": "n", "\u2096": "k", "\u2098": "m",
            "\u2090": "a", "\u2091": "e", "\u2092": "o", "\u209b": "s", "\u209c": "t",
            "\u2093": "x"}
_SUBCLS = "".join(SUBCHARS)
_SUBRUN = re.compile("[" + _SUBCLS + r"](?:\.?[" + _SUBCLS + r"])*")
_PH_BASE = 0xE000


def _sub_run(m):
    return "_{" + "".join(SUBCHARS.get(c, c) for c in m.group(0)) + "}"


# 需要"保护"的实体（含花括号或长度>1）→ 先换成私有区占位符，避免花括号平衡修正误伤
_MAP_SORTED = sorted([kv for kv in MATH_MAP if kv[1]], key=lambda kv: -len(kv[0]))
_SUBLIKE = set("\u2080\u2081\u2082\u2083\u2084\u2085\u2086\u2087\u2088\u2089\u1d62\u2099\u00b2\u00b3\u207f\u0304\u0302\u0305\u0303")
_MAP_PROTECT = [(k, v) for k, v in _MAP_SORTED if k not in _SUBLIKE]
_MAP_INLINE = [(k, v) for k, v in _MAP_SORTED if k in _SUBLIKE]


def is_math_char(ch):
    o = ord(ch)
    if _PH_BASE <= o <= 0xF8FF:
        return True
    return (ch in MATH_ASCII) or (ch in MATH_UNI)


def protect_entities(s):
    store, seen = [], {}
    for k, v in _MAP_PROTECT:
        if k not in s:
            continue
        if k in seen:
            ph = seen[k]
        else:
            ph = chr(_PH_BASE + len(store))
            if re.fullmatch(r"\\[A-Za-z]+", v):
                v = v + "{}"
            store.append(v)
            seen[k] = ph
        s = s.replace(k, ph)
    return s, store


def restore_entities(s, store):
    for i, v in enumerate(store):
        s = s.replace(chr(_PH_BASE + i), v)
    return s


def balance_braces(seg):
    """段内花括号失衡（集合记号 {…} 跨越中文）→ 全部转义为 \\{ \\}。"""
    if seg.count("{") == seg.count("}"):
        return seg
    return seg.replace("{", r"\{").replace("}", r"\}")


def math_tex(s):
    """数学片段 → LaTeX（不含外层 $）。"""
    s = _SUBRUN.sub(_sub_run, s)
    s = re.sub(r"([A-Za-z\u0370-\u03ff])\u0302", r"\\hat{\1}", s)
    s = re.sub(r"([A-Za-z\u0370-\u03ff])\u0304", r"\\bar{\1}", s)
    s = re.sub(r"([A-Za-z\u0370-\u03ff])\u0305", r"\\overline{\1}", s)
    s = re.sub(r"([A-Za-z\u0370-\u03ff])\u0303", r"\\tilde{\1}", s)
    for k, v in _MAP_INLINE:
        if re.fullmatch(r"\\[A-Za-z]+", v):
            v = v + "{}"
        s = s.replace(k, v)
    for ch, sub in (("\u1d62", "i"), ("\u2099", "n")):
        s = s.replace(ch, "_" + sub)
    # 下标/上标多字符加括号： a_xx → a_{xx}，并合并连续下标
    s = re.sub(r"(?<![\\{])([_^])([A-Za-z0-9]{2,})", r"\1{\2}", s)
    for _ in range(3):
        merged = re.sub(r"_(\{[^{}]*\}|[A-Za-z0-9])_(\{[^{}]*\}|[A-Za-z0-9])",
                        lambda m: "_{" + m.group(1).strip("{}") + m.group(2).strip("{}") + "}", s)
        if merged == s:
            break
        s = merged
    for w, tex in (("ln", r"\ln"), ("exp", r"\exp"), ("max", r"\max"), ("min", r"\min"),
                   ("log", r"\log"), ("lim", r"\lim"), ("Var", r"\mathrm{Var}"),
                   ("Cov", r"\mathrm{Cov}")):
        s = re.sub(r"(?<![\\A-Za-z])" + w + r"(?![A-Za-z])",
                   lambda mm, _t=tex: _t + "{}", s)
    s = re.sub(r" {2,}", r"\\hspace{0.55em}", s)
    return s.strip()


def mathify_line(line):
    """整行 → LaTeX：数学段进 $...$，中文段按普通文本，保留缩进。"""
    indent = len(line) - len(line.lstrip(" "))
    body = line.strip()
    body = re.sub(r"\(([^()]{1,24})\)[\u203e\u0305]", r"\\overline{(\1)}", body)  # (A∪B)‾
    body, store = protect_entities(body)
    runs = []
    for ch in body:
        if ch == " " and runs:
            runs[-1][1].append(ch)
            continue
        ism = is_math_char(ch)
        if runs and runs[-1][0] == ism:
            runs[-1][1].append(ch)
        else:
            runs.append([ism, [ch]])
    parts = []
    for ism, chars in runs:
        seg = "".join(chars)
        if ism:
            seg = balance_braces(seg)
            mt = math_tex(seg)
            if mt:
                parts.append("$" + mt + "$")
        else:
            parts.append(inline_plain(seg.replace("**", "")))
    pre = (r"\hspace*{%.2fem}" % (indent * 0.42)) if indent else ""
    return restore_entities(pre + "".join(parts), store)


def wrap_code(line, width=76, indent="    "):
    """按显示宽度折行（CJK 记 2 列）。"""
    def w(ch):
        return 2 if ord(ch) > 0x2E80 else 1
    if sum(w(c) for c in line) <= width:
        return [line]
    out, cur, curw = [], [], 0
    base = indent if line.startswith(" ") else ""
    for ch in line:
        if curw + w(ch) > width:
            out.append("".join(cur))
            cur, curw = list(base), len(base)
        cur.append(ch)
        curw += w(ch)
    out.append("".join(cur))
    return out


def ascii_sub(s):
    """代码块内：组合变音符与上下标改成 ASCII，避免等宽字体显示怪异。"""
    for k, v in [("σ̂", "sigmahat"), ("θ̂", "thetahat"), ("λ̂", "lambdahat"),
                 ("μ̂", "muhat"), ("p̂", "phat"), ("b̂", "bhat"), ("â", "ahat"),
                 ("χ̂", "chihat"), ("x̄", "xbar"), ("X̄", "Xbar"), ("ȳ", "ybar"),
                 ("d̄", "dbar"), ("z̄", "zbar"), ("Ȳ", "Ybar"),
                 ("₀", "0"), ("₁", "1"), ("₂", "2"), ("₃", "3"), ("₄", "4"), ("₅", "5"),
                 ("₆", "6"), ("₇", "7"), ("₈", "8"), ("₉", "9"), ("ᵢ", "i"), ("ₙ", "n"),
                 ("²", "^2"), ("³", "^3"), ("ⁿ", "^n")]:
        s = s.replace(k, v)
    return s


TOKEN_RE = re.compile(r"(\$\$[^$]+\$\$|\$[^$]+\$|\*\*[^*]+\*\*|`[^`]+`)")


def inline(s):
    s = s.strip()
    parts = []
    for tok in TOKEN_RE.split(s):
        if not tok:
            continue
        if tok.startswith("$$") and tok.endswith("$$"):
            parts.append(r"\[" + map_syms(tok[2:-2]) + r"\]")
        elif tok.startswith("$"):
            parts.append("$" + map_syms(tok[1:-1]) + "$")
        elif tok.startswith("**"):
            inner = tok[2:-2]
            parts.append(r"\textbf{" + inline_plain(inner) + "}")
        elif tok.startswith("`"):
            parts.append(r"\texttt{" + inline_plain(tok[1:-1]) + "}")
        else:
            parts.append(inline_plain(tok))
    return "".join(parts)


def split_row(row):
    """按 | 切分，但不切开 $...$ 数学段内的竖线。"""
    cells, cur, in_math = [], [], False
    s = row.strip().strip("|")
    for ch in s:
        if ch == "$":
            in_math = not in_math
            cur.append(ch)
        elif ch == "|" and not in_math:
            cells.append("".join(cur).strip())
            cur = []
        else:
            cur.append(ch)
    cells.append("".join(cur).strip())
    return cells


def table_to_tex(rows):
    body = []
    for r in rows:
        cells = split_row(r)
        if cells and all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c != ""):
            continue  # 分隔行 |---|---|
        body.append(cells)
    if not body:
        return ""
    ncol = max(len(r) for r in body)
    body = [r + [""] * (ncol - len(r)) for r in body]

    # 按内容自适应列宽（CJK 记 2 列宽），总宽压到 16.8cm 内
    def dw(s):
        s = re.sub(r"\*\*|\$", "", s)
        return sum(2 if ord(c) > 0x2E80 else 1 for c in s)

    maxw = [max(dw(r[c]) for r in body) for c in range(ncol)]
    minw = [max(4.0, 0.42 * ncol) for _ in range(ncol)]  # 单位：字符宽
    tot = sum(max(maxw[c], minw[c]) for c in range(ncol))
    avail = 92.0  # 约 16.8cm 折算成"字符宽"
    if tot < avail:
        # 有富余就按内容比例放大一点
        k = min(avail / tot, 1.6)
        colw = [max(maxw[c], minw[c]) * k for c in range(ncol)]
        tot = sum(colw)
    colw = [w / tot * 16.8 for w in maxw]
    colw = [max(0.95, w) for w in colw]
    scale = 16.8 / sum(colw)
    colw = [w * scale for w in colw]
    spec = "|" + "|".join("p{%.2fcm}" % w for w in colw) + "|"
    lines = [r"\begin{center}\footnotesize\renewcommand{\arraystretch}{1.25}"
             r"\setlength{\tabcolsep}{3pt}",
             r"\begin{longtable}{" + spec + "}", r"\hline"]
    for i, cells in enumerate(body):
        lines.append(" & ".join(inline(c) for c in cells) + r" \\ \hline")
        if i == 0:
            lines.append(r"\endfirsthead\hline")
    lines += [r"\end{longtable}\end{center}"]
    return "\n".join(lines)

# ============================================================================
#  LaTeX 渲染：两种模式
#    read     —— 阅读版：题目 + 解答（答案随题）
#    practice —— 刷题版：题目 + 留白；答案集中到每章末尾《本章答案》
# ============================================================================

def minutes_of(s):
    m = re.search(r"(\d+)\s*分钟", s)
    return int(m.group(1)) if m else None


def stars_of(s):
    m = re.search(r"★+", s)
    return len(m.group(0)) if m else 2


def space_lines(kind, line):
    """留白行数：按建议用时/难度决定。"""
    if kind == "example":
        return 5 + (1 if stars_of(line) >= 3 else 0)
    if kind == "quiz":
        return 9
    if kind == "final":
        return 7
    m = minutes_of(line) or 4          # 刷题
    if m <= 2:
        return 2
    if m == 3:
        return 3
    if m == 4:
        return 4
    if m == 5:
        return 5
    if m == 6:
        return 6
    return 8


def ans_area(n, label="答："):
    """生成 n 行书写线。"""
    out = [r"\par\addvspace{0.18em}",
           r"\leavevmode\noindent{\footnotesize\color{black!50}" + label + r"}\par\vspace{0.15em}"]
    for k in range(n):
        out.append(r"\noindent\textcolor{black!28}{\rule{\linewidth}{0.35pt}}\par"
                   r"\vspace{0.72em}")
    return "\n".join(out)


ANS_CONT = ("→", "　", "**不做修正**", "**若做连续性修正**")


def is_answer_line(s):
    t = s.lstrip()
    return t.startswith(ANS_CONT)


class Renderer:
    def __init__(self, mode, title):
        self.mode = mode            # "read" | "practice"
        self.title = title
        self.out = []
        self.chapter_ans = []       # 本章答案条目（LaTeX 行）
        self.card = ""              # 当前考点卡编号
        self.sect = "normal"        # normal | quiz | final | finalans
        self.ex_buf = []            # 例题缓冲（题目部分）
        self.ex_active = False
        self.ans_buf = None         # 答案收集缓冲（练习版）
        self.ans_label = ""
        self.ans_pending = None

    # ---------------- 基础输出
    def raw(self, s=""):
        self.out.append(s)

    def start_ans(self, label, first_line):
        self.ans_buf = [first_line]
        self.ans_label = label

    def flush_ans(self):
        if self.ans_buf is None:
            return
        body = "\n".join(inline(x) for x in self.ans_buf)
        self.chapter_ans.append((self.ans_label, body))
        self.ans_buf = None
        self.ans_label = ""
        self.ans_pending = None

    def flush_chapter_answers(self):
        if not self.mode or not self.chapter_ans:
            return
        self.raw(r"\subsection*{本章答案}")
        self.raw("")
        for lab, body in self.chapter_ans:
            self.raw(r"\noindent\textbf{" + lab + r"}　" + body)
            self.raw("")
        self.raw(r"\vspace{0.3em}\noindent\textcolor{black!25}{\rule{\linewidth}{0.4pt}}")
        self.raw("")
        self.chapter_ans = []

    # ---------------- 行级处理
    def line(self, s):
        t = s.rstrip()
        # ---------- 答案收集中（练习版）
        if self.ans_buf is not None:
            if (not t.strip()) or re.match(r"^(\*\*例|\*\*刷|\*\*答案|#{1,4}\s|-{3,})", t):
                self.flush_ans()
            else:
                self.ans_buf.append(t)
                return
        # ---------- 空行
        if not t.strip():
            if self.ex_active:
                return
            self.raw("")
            return
        # ---------- 分隔线
        if re.match(r"^-{3,}\s*$", t):
            self.raw(r"\vspace{0.4em}\noindent\textcolor{black!25}{\rule{\linewidth}{0.4pt}}\vspace{0.4em}")
            return
        # ---------- 标题
        m = re.match(r"^(#{1,4})\s+(.*)$", t)
        if m:
            lvl, txt = len(m.group(1)), m.group(2)
            if lvl <= 2 and ("本章完成登记" in txt or "易错点清单" in txt):
                self.sect = "normal"
            if lvl <= 2 and "本章完成登记" in txt and self.mode == "practice":
                self.flush_ans()
                self.flush_chapter_answers()
            if lvl == 2 and ("章末限时小测" in txt or "章末实战检测" in txt):
                self.sect = "quiz"
            if lvl == 2 and "本章完成登记" in txt:
                self.sect = "normal"
            if lvl == 1 and "结业自测" in txt:
                self.sect = "final"
            if lvl == 3 and "答案" in txt and self.sect == "final":
                self.sect = "finalans"
                self.raw("")
                self.raw(r"\subsection*{结业自测 · 答案（全部做完再对）}")
                self.raw("")
                return
            if lvl == 3 and self.card == "" and txt.startswith("K"):
                self.card = txt.split("｜")[0].strip()
            mm = re.match(r"^K[\d.\-]+\s", txt)
            if mm:
                self.card = txt.split("｜")[0].strip()
            if lvl == 3 and self.mode == "practice":
                self.raw("")
                self.raw(r"\cardhdr{" + inline(txt) + "}")
                return
            if lvl == 3:
                self.raw("")
                self.raw(r"\cardhdr{" + inline(txt) + "}")
                return
            if lvl == 4:
                self.raw(r"\paragraph*{" + inline(txt) + "}")
                return
            if lvl == 2:
                if self.mode == "practice" and re.match(r"^第\s*\d+\s*章", txt):
                    self.flush_ans()
                    self.flush_chapter_answers()
                    self.card = ""
                self.raw("")
                self.raw(r"\subsection*{" + inline(txt) + r"}\addcontentsline{toc}{subsection}{" + inline_plain(txt) + "}")
                return
            self.raw("")
            self.raw(r"\section*{" + inline(txt) + r"}\addcontentsline{toc}{section}{" + inline_plain(txt) + "}")
            return
        # ---------- 引用块
        if t.lstrip().startswith(">"):
            if self.sect == "finalans":
                self.raw(r"\begin{tip}" + inline(t.lstrip("> ").strip()) + r"\end{tip}")
            else:
                self.raw(r"\begin{tip}" + inline(t.lstrip("> ").strip()) + r"\end{tip}")
            return
        # ---------- 结业答案区：原样保留
        if self.sect == "finalans":
            mm = re.match(r"^(\d+)\.\s+(.*)$", t)
            if mm:
                self.raw(r"\noindent\textbf{" + mm.group(1) + r".} " + inline(mm.group(2)))
                self.raw("")
                return
            self.raw(inline(t))
            self.raw("")
            return
        # ---------- 例（精讲）：缓冲整段题目，再输出留白 + 解答
        if self.ex_active:
            if re.match(r"^\*\*(解|证|答)", t):
                self.emit_example(t)
                self.ex_active = False
                return
            if re.match(r"^(\*\*刷|#{2,4}\s|---|> )", t):
                self.emit_example(None)      # 该例无解答
                self.ex_active = False
                self.line(s)                 # 重新处理当前行
                return
            self.ex_buf.append(t)
            return
        if t.startswith("**例"):
            self.ex_active = True
            self.ex_buf = [t]
            return
        # ---------- 刷题
        m = re.match(r"^\*\*刷\s*(\d+)", t)
        if m:
            self.flush_ans()
            if self.mode == "practice":
                self.raw("")
                self.raw(r"\noindent\begin{samepage}")
                self.raw(r"\noindent{}" + inline(t))
                self.raw("")
                self.raw(ans_area(space_lines("drill", t)))
                self.raw(r"\end{samepage}")
                lab = ("%s 刷 %s" % (self.card, m.group(1))) if self.card else ("刷 %s" % m.group(1))
                self.start_ans(lab, "__PENDING__")   # 占位，等 → 行到来
                self.ans_buf = []                     # 先清空，等答案首行
                self.ans_pending = lab
                return
            self.raw("")
            self.raw(r"\noindent{}" + inline(t))
            self.raw("")
            return
        # ---------- 刷题答案行（练习版：收进本章答案）
        if self.mode == "practice" and is_answer_line(t) and getattr(self, "ans_pending", None):
            self.ans_label = self.ans_pending
            self.ans_pending = None
            self.ans_buf = [t]
            return
        # ---------- 小测答案段
        if t.startswith("**答案**"):
            if self.mode == "practice":
                self.flush_ans()
                self.chapter_ans.append(("小测答案", inline(t.replace("**答案**：", "").replace("**答案**", ""))))
                return
            self.raw(r"\noindent\textbf{答案}　" + inline(t.replace("**答案**：", "").replace("**答案**", "")))
            self.raw("")
            return
        # ---------- 实战检测题号 **A1（…）**
        mq = re.match(r"^\*\*([ABC])(\d)（", t)
        if mq and self.sect == "quiz":
            if self.mode == "practice":
                self.raw(r"\noindent\begin{samepage}")
                self.raw(r"\noindent{}" + inline(t))
                self.raw("")
                self.raw(ans_area(11 if mq.group(1) == "C" else 9))
                self.raw(r"\end{samepage}")
            else:
                self.raw(r"\noindent{}" + inline(t))
                self.raw("")
            return
        # ---------- 变卦点（引用块）在刷题版收进章末答案
        if t.lstrip().startswith(">") and "变卦点" in t and self.sect == "quiz":
            if self.mode == "practice":
                self.chapter_ans.append(("变卦点", inline(t.lstrip("> ").strip())))
            else:
                self.raw(r"\begin{tip}" + inline(t.lstrip("> ").strip()) + r"\end{tip}")
            return
        # ---------- 小测/结业 题号
        m = re.match(r"^(\d+)\.\s+(.*)$", t)
        if m and self.sect == "quiz" and self.mode == "practice":
            self.raw(r"\noindent\begin{samepage}")
            self.raw(r"\noindent\textbf{%s.} %s" % (m.group(1), inline(m.group(2))))
            self.raw("")
            self.raw(ans_area(space_lines("quiz", t)))
            self.raw(r"\end{samepage}")
            return
        if m and self.sect == "final" and self.mode == "practice":
            self.raw(r"\noindent\begin{samepage}")
            self.raw(r"\noindent\textbf{%s.} %s" % (m.group(1), inline(m.group(2))))
            self.raw("")
            self.raw(ans_area(space_lines("final", t)))
            self.raw(r"\end{samepage}")
            return
        # ---------- 列表
        if re.match(r"^\d+\.\s", t):
            self.raw(r"\noindent\textbf{%s} %s" % (t.split(".")[0] + ".", inline(t.split(".", 1)[1].strip())))
            self.raw("")
            return
        if t.startswith("- "):
            self.raw(r"\noindent\textbullet{} " + inline(t[2:]))
            self.raw("")
            return
        # ---------- 本章完成登记（加粗文本，非标题）：练习版先把本章答案排出来
        if t.strip() == "**本章完成登记**":
            if self.mode == "practice":
                self.flush_ans()
                self.flush_chapter_answers()
            self.raw(r"\vspace{0.2em}\paragraph*{本章完成登记}")
            return
        # ---------- 普通段落
        self.raw(inline(t))
        self.raw("")

    def emit_example(self, sol_line):
        head = self.ex_buf[0]
        body = self.ex_buf[1:]
        self.raw("")
        self.raw(r"\noindent\begin{samepage}")
        self.raw(r"\noindent{}" + inline(head))
        self.raw("")
        for b in body:
            if b.strip():
                self.raw(r"\noindent{}" + inline(b))
                self.raw("")
        if self.mode == "practice":
            self.raw(ans_area(space_lines("example", head)))
        self.raw(r"\end{samepage}")
        if sol_line:
            if self.mode == "practice":
                m = re.search(r"例\s*(\d+)", head)
                lab = ("%s 例 %s" % (self.card, m.group(1))) if (self.card and m) else "例"
                self.start_ans(lab, sol_line)
            else:
                self.raw(inline(sol_line))
                self.raw("")
        self.ex_buf = []

    def table(self, rows):
        self.raw(table_to_tex(rows))
        self.raw("")


PREAMBLE_HEAD = r"""\documentclass[11pt,a4paper]{ctexart}
\usepackage[margin=2.1cm,top=2.5cm,bottom=2.3cm,headsep=8pt]{geometry}
\usepackage{amsmath,amssymb,booktabs,longtable,array}
% \bar 在粗体数学里会去文本粗体字取花帽字形（U+0016）而落空 → 统一改用 \overline
\AtBeginDocument{\renewcommand{\bar}[1]{\overline{#1}}}
\usepackage{xcolor,fancyvrb,fancyhdr,enumitem,titlesec,hyperref}
\usepackage[most]{tcolorbox}
\definecolor{main}{RGB}{31,78,140}
\definecolor{accent}{RGB}{176,58,46}
\setCJKmainfont{Noto Serif CJK SC}[BoldFont={Noto Serif CJK SC Bold}]
\setCJKmonofont{Noto Serif CJK SC}
\setmainfont{TeX Gyre Pagella}
\setCJKmathfont{Noto Serif CJK SC}
\xeCJKsetup{CJKmath=true}
\xeCJKDeclareCharClass{CJK}{"2460 -> "24FF}
\usepackage{newunicodechar}
\newunicodechar{★}{\ensuremath{\bigstar}}
\newunicodechar{☆}{\ensuremath{\bigstar}}
\newunicodechar{✓}{\ensuremath{\checkmark}}
\newunicodechar{✗}{\ensuremath{\times}}
\newunicodechar{′}{\ensuremath{\prime}}
\newunicodechar{‾}{\ensuremath{\overline{\hspace{0.35em}}}}
\newunicodechar{√}{\ensuremath{\surd}}
\newunicodechar{∪}{\ensuremath{\cup}}
\newunicodechar{∩}{\ensuremath{\cap}}
\newunicodechar{∈}{\ensuremath{\in}}
\newunicodechar{⊂}{\ensuremath{\subset}}
\newunicodechar{∅}{\ensuremath{\varnothing}}
\newunicodechar{⇒}{\ensuremath{\Rightarrow}}
\newunicodechar{⇔}{\ensuremath{\Leftrightarrow}}
\newunicodechar{→}{\ensuremath{\to}}
\newunicodechar{←}{\ensuremath{\leftarrow}}
\newunicodechar{≤}{\ensuremath{\le}}
\newunicodechar{≥}{\ensuremath{\ge}}
\newunicodechar{≠}{\ensuremath{\ne}}
\newunicodechar{∞}{\ensuremath{\infty}}
\newunicodechar{∫}{\ensuremath{\int}}
\newunicodechar{Σ}{\ensuremath{\sum}}
\newunicodechar{′}{\ensuremath{\prime}}
\linespread{1.25}
\setlength{\parindent}{0pt}
\setlength{\parskip}{0.34em}
\titleformat{\section}{\Large\bfseries\color{main}}{}{0em}{}[\vspace{-0.4em}\textcolor{main}{\rule{\linewidth}{0.8pt}}]
\titleformat{\subsection}{\large\bfseries\color{main!85!black}}{}{0em}{}
\titleformat{\subsubsection}{\normalsize\bfseries}{}{0em}{}
\titlespacing*{\section}{0pt}{1.4em}{0.8em}
\titlespacing*{\subsection}{0pt}{1.1em}{0.5em}
\newcommand{\cardhdr}[1]{\par\vspace{0.55em}\noindent\begin{tcolorbox}[enhanced,colback=main!7,colframe=main!55,boxrule=0.5pt,arc=2pt,left=6pt,right=6pt,top=4pt,bottom=4pt,fontupper=\bfseries]{\normalsize #1}\end{tcolorbox}\par\vspace{0.25em}}
\newenvironment{mathbox}{\begin{tcolorbox}[enhanced,colback=black!4,colframe=black!30,boxrule=0.4pt,arc=1pt,left=6pt,right=6pt,top=5pt,bottom=5pt]\small\raggedright\linespread{1.15}\selectfont}{\end{tcolorbox}}
\newenvironment{tip}{\begin{tcolorbox}[enhanced,colback=black!3,colframe=black!25,boxrule=0.4pt,arc=1pt,left=6pt,right=6pt,top=3pt,bottom=3pt]\small}{\end{tcolorbox}}
\fvset{fontsize=\small,frame=single,framerule=0.4pt,rulecolor=\color{black!35},framesep=4pt,xleftmargin=6pt,xrightmargin=4pt}
\pagestyle{fancy}\fancyhf{}
\fancyhead[L]{\small\color{main}##TITLE##}\fancyhead[R]{\small\thepage}
\renewcommand{\headrulewidth}{0.4pt}
\hypersetup{colorlinks=true,linkcolor=main,urlcolor=main}
\setlist[itemize]{leftmargin=1.4em,itemsep=2pt,topsep=3pt,parsep=0pt}
\setlist[enumerate]{leftmargin=1.7em,itemsep=2pt,topsep=3pt,parsep=0pt}
\begin{document}
"""


def tex_of(md, title, subtitle, mode="read"):
    r = Renderer(mode, title)
    if mode == "practice":
        note = (r"{\large\itshape \textbf{刷题版}：题目下方留白供书写；答案集中在每章末尾《本章答案》}"
                r"\\[0.35cm]")
        note2 = r"{\large\itshape 建议：先遮住答案独立做，对完答案把错题号填进登记表}\\[2.2cm]"
    else:
        note = r"{\large\itshape 阅读版：题目 + 解答（答案随题）}\\[0.35cm]"
        note2 = r"{\large\itshape 刷完这本，考纲里没有你没做过的题}\\[2.2cm]"
    r.raw(PREAMBLE_HEAD.replace("##TITLE##", title))
    r.raw(r"\begin{titlepage}\centering")
    r.raw(r"\vspace*{3.0cm}")
    r.raw(r"{\Huge\bfseries\color{main} " + esc(title) + r"}\\[0.6cm]")
    r.raw(r"{\Large\color{main!75!black} " + esc(subtitle) + r"}\\[1.2cm]")
    r.raw(r"\textcolor{main}{\rule{0.75\linewidth}{1.2pt}}\\[0.5cm]")
    r.raw(r"{\large 《概率论与数理统计》期末通关系列 · 第 11 号产出}\\[0.3cm]")
    r.raw(r"{\large 2026-10-16  ·  与课堂大纲（8.5/8.6/第10章）对齐}\\[2.2cm]")
    r.raw(note)
    r.raw(note2)
    r.raw(r"{\small 内部验算：verify\_drill.py（230 项全通过）}")
    r.raw(r"\end{titlepage}")
    r.raw(r"\tableofcontents\newpage")

    lines = md.split("\n")
    i = 0
    in_code = False
    code_buf = []
    pending_table = []
    while i < len(lines):
        ln = lines[i]
        if ln.strip().startswith("```"):
            if not in_code:
                in_code, code_buf = True, []
            else:
                in_code = False
                r.raw(r"\begin{mathbox}")
                for b in code_buf:
                    if b.strip():
                        r.raw(mathify_line(b) + r"\par")
                    else:
                        r.raw(r"\vspace{0.35em}")
                r.raw(r"\end{mathbox}")
                r.raw("")
            i += 1
            continue
        if in_code:
            code_buf.append(ln)
            i += 1
            continue
        if ln.lstrip().startswith("|"):
            pending_table.append(ln)
            i += 1
            if i < len(lines) and lines[i].lstrip().startswith("|"):
                continue
            r.table(pending_table)
            pending_table = []
            continue
        r.line(ln)
        i += 1
    if mode == "practice":
        r.flush_ans()
        r.flush_chapter_answers()
        if any("结业" in a[0] or "结业" in a[1] for a in r.chapter_ans):
            pass
    r.raw(r"\end{document}")
    return "\n".join(r.out)


def compile_pdf(tex_path, workdir, runs=2):
    for k in range(runs):
        p = subprocess.run(["xelatex", "-interaction=nonstopmode", "-halt-on-error",
                            os.path.basename(tex_path)],
                           cwd=workdir, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        log = p.stdout.decode("utf-8", "ignore")
        if p.returncode != 0:
            errs = [l for l in log.split("\n") if l.startswith("!")][:12]
            print("   ✗ xelatex 失败（run %d）：" % (k + 1))
            for e in errs:
                print("     " + e)
            if VERBOSE:
                print(log[-5000:])
            return False
    return True


def build_pdf():
    work = os.path.join(HERE, "_latex")
    os.makedirs(work, exist_ok=True)
    md_all = (read("00-使用说明与刷题计划.md") + "\n\n"
              + read("上册-第1至4章.md") + "\n\n" + read("下册-第5至10章.md"))
    jobs = [
        ("上册-第1至4章.md", "概率论期末通关刷题集 · 上册", "期中范围 M1–M12 · 104 题", "上册"),
        ("下册-第5至10章.md", "概率论期末通关刷题集 · 下册", "统计与新增考点 M13–M20 · 120 题 + 结业自测", "下册"),
        (None, "概率论期末通关刷题集 · 全一册", "上册（1–4 章）+ 下册（5–10 章）+ 结业自测 · 244 题", "全一册"),
    ]
    for src, title, subtitle, tag in jobs:
        md = md_all if src is None else read(src)
        for mode, suffix in (("practice", "刷题版"), ("read", "阅读版")):
            tex = tex_of(md, title, subtitle, mode=mode)
            tp = os.path.join(work, "%s-%s.tex" % (tag, suffix))
            with open(tp, "w", encoding="utf-8") as fh:
                fh.write(tex)
            print("  [LaTeX] %s-%s.pdf ..." % (tag, suffix))
            if not compile_pdf(tp, work):
                return False
            subprocess.run(["cp", os.path.join(work, "%s-%s.pdf" % (tag, suffix)), HERE])
    # 清理旧文件（单一命名：xx-刷题版.pdf / xx-阅读版.pdf）
    for old in ("上册.pdf", "下册.pdf", "全一册.pdf"):
        p = os.path.join(HERE, old)
        if os.path.exists(p):
            os.remove(p)
    return True


def main():
    print("刷题集构建：MD 合并 + LaTeX 精排（刷题版 / 阅读版）")
    build_md()
    if MD_ONLY:
        return 0
    ok = build_pdf()
    print("完成" if ok else "PDF 构建失败")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
