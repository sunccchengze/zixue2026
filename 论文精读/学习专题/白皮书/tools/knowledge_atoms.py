#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
knowledge_atoms.py —— 知识原子账本抽取器（v2 知识守恒协议）
=============================================================================
从 v1 冻结源（docs/archive/v1/）抽取六类知识原子，供 verify_all.py H 项验收：
  cite     〔…〕 方括号标签（原文 P## / 延伸 / 待核实）→ 整条标签须原样出现在 v2 同源文件
  num      正文数字 token（代码块/图行/锚点行除外）→ 数字串须出现在 v2 同源文件
  term     先认词表词条（中文词 + 英文缩写）→ 须出现
  bold     加粗术语 **xx**（2–20 字含汉字）→ 须出现
  quiz     自测题干（§9 编号行，"答案要点"前）→ 去空白后须逐字出现
  critique 审稿人批判编号条目 → 去空白后须逐字出现

用法：
    python3 tools/knowledge_atoms.py            # 从 docs/archive/v1/ 抽取 → docs/knowledge_atoms_v1.{json,md}
    python3 tools/knowledge_atoms.py --check    # 用当前 docs/ 源对照账本（等价 H 项，独立运行用）

守恒口径（S13）：v2 只许加解释/例子/题目/图/指路；六类原子一条不许丢。
"""
from __future__ import annotations

import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V1_DIR = os.path.join(ROOT, "docs", "archive", "v1")
OUT_JSON = os.path.join(ROOT, "docs", "knowledge_atoms_v1.json")
OUT_MD = os.path.join(ROOT, "docs", "knowledge_atoms_v1.md")

# 文件映射：账本键 → v1 路径 / v2 路径（v2 保持同路径，改的是原文件）
FILES = {
    "front_matter": "front_matter.md",
    "chapter0": "chapter0.md",
    "lectures/01": "lectures/01.md",
    "lectures/02": "lectures/02.md",
    "lectures/03": "lectures/03.md",
    "lectures/04": "lectures/04.md",
    "lectures/05": "lectures/05.md",
    "lectures/06": "lectures/06.md",
    "lectures/07": "lectures/07.md",
    "lectures/08": "lectures/08.md",
    "lectures/09": "lectures/09.md",
    "lectures/10": "lectures/10.md",
    "lectures/11": "lectures/11.md",
    "lectures/12": "lectures/12.md",
    "part6": "part6.md",
}

CJK = re.compile(r"[\u4e00-\u9fff]")
CITE_TAG = re.compile(r"〔[^〔〕\n]{1,140}〕")
NUM = re.compile(r"\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+\.\d+|\d+\^\d+|\d+")
SINGLE_DIGIT_UNITS = set("维次条个张讲篇步级格层组点模秒小时年天页篇幅")


def norm(t: str) -> str:
    """归一化：×/x 统一、空白折叠。用于原子比对。"""
    t = t.replace("×", "×").replace("ｘ", "×")
    return re.sub(r"\s+", " ", t).strip()


def strip_code_and_noise(t: str) -> str:
    """去掉代码块、图片行、锚点行、表格分隔行——数字/加粗原子不从这里取。"""
    t = re.sub(r"```.*?```", "", t, flags=re.S)
    t = "\n".join(
        ln
        for ln in t.split("\n")
        if not ln.strip().startswith("![")
        and not ln.strip().startswith("<a id=")
        and not re.match(r"^\s*\|[\s:\-|]+\|\s*$", ln)
    )
    return t


def extract_cites(t: str) -> list[str]:
    return sorted(set(m.group(0) for m in CITE_TAG.finditer(t)))


def extract_nums(t: str) -> list[str]:
    t = CITE_TAG.sub("", t)
    out: set[str] = set()
    for m in NUM.finditer(t):
        tok = m.group(0)
        if re.search(r"[.,^]", tok):
            out.add(tok)
            continue
        val = int(tok.replace(",", ""))
        if val >= 10:
            out.add(tok)
            continue
        # 单位数字：后两字符内须跟单位字
        tail = t[m.end(): m.end() + 2]
        if tail and CJK.search(tail) and tail[0] in SINGLE_DIGIT_UNITS:
            out.add(tok)
    return sorted(out, key=lambda s: (len(s), s))


def extract_terms(t: str) -> list[str]:
    """先认词表：找到含「先认词」的表格块，取每行第 1 列中文词 + 第 2 列英文缩写。"""
    out: set[str] = set()
    blocks = re.split(r"\n\s*\n", t)
    for b in blocks:
        if "先认词" not in b and "先认词" not in "\n".join(blocks[blocks.index(b) - 1:blocks.index(b) + 1]):
            continue
        for ln in b.split("\n"):
            ln = ln.strip()
            if not ln.startswith("|"):
                continue
            cells = [c.strip() for c in ln.strip("|").split("|")]
            if len(cells) < 3 or set(cells[0]) <= set(" :-") or cells[0] in ("中文",):
                continue
            if CJK.search(cells[0]) and len(cells[0]) <= 12:
                out.add(cells[0])
            for en in re.findall(r"[A-Za-z][A-Za-z\-]{1,}", cells[1]):
                if en not in ("The", "and", "also", "known", "Free", "Form"):
                    out.add(en)
    return sorted(out)


def extract_bold(t: str) -> list[str]:
    out: set[str] = set()
    for m in re.finditer(r"\*\*([^*\n]{2,20})\*\*", t):
        s = m.group(1).strip()
        if CJK.search(s) and not re.fullmatch(r"[\d\s\W_]+", s):
            out.add(norm(s))
    return sorted(out)


def _numbered_items(sec: str) -> list[str]:
    """取节内编号列表项（含换行续行），去空白归一化。"""
    items: list[str] = []
    lines = sec.split("\n")
    i = 0
    while i < len(lines):
        m = re.match(r"^\s*(\d+)[\.、]\s*(.+)$", lines[i])
        if m:
            item = m.group(2)
            j = i + 1
            while j < len(lines):
                nxt = lines[j]
                if re.match(r"^\s*\d+[\.、]\s", nxt) or not nxt.strip() or nxt.lstrip().startswith(("#", ">", "|", "**答案", "---")):
                    break
                item += " " + nxt.strip()
                j += 1
            items.append(norm(item))
            i = j
        else:
            i += 1
    return items


def extract_quiz(t: str) -> list[str]:
    """§9 自测题干：到『答案要点』或下一 #### 为止。"""
    m = re.search(r"(?:^|\n)####\s*9\.[^\n]*\n(.*?)(?=\n####\s|\*\*答案要点|\Z)", t, flags=re.S)
    if not m:
        return []
    sec = m.group(1)
    k = sec.find("**答案要点")
    if k >= 0:
        sec = sec[:k]
    items = []
    for it in _numbered_items(sec):
        if it.startswith(("（选", "（填", "（答", "选）", "填）", "答）")) or re.match(r"^[（(]?", it):
            items.append(it)
    return sorted(set(items))


def extract_critique(t: str) -> list[str]:
    m = re.search(r"(?:^|\n)####\s*\d+\.[^\n]*审稿人批判[^\n]*\n(.*?)(?=\n####\s|\Z)", t, flags=re.S)
    if not m:
        return []
    return sorted(set(_numbered_items(m.group(1))))


def extract_file(path: str) -> dict[str, list[str]]:
    t = open(path, encoding="utf-8").read()
    body = strip_code_and_noise(t)
    return {
        "cite": extract_cites(t),
        "num": extract_nums(body),
        "term": extract_terms(body),
        "bold": extract_bold(body),
        "quiz": extract_quiz(t),
        "critique": extract_critique(t),
    }


def build() -> None:
    ledger: dict[str, dict[str, list[str]]] = {}
    for key, rel in FILES.items():
        p = os.path.join(V1_DIR, rel)
        if not os.path.exists(p):
            sys.exit(f"缺少 v1 冻结源：{p}")
        ledger[key] = extract_file(p)
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(ledger, f, ensure_ascii=False, indent=1)

    total = sum(len(a) for d in ledger.values() for a in d.values())
    lines = ["# 知识原子账本 v1（冻结基线，2026-09-07）", "",
             "> 由 `tools/knowledge_atoms.py` 从 `docs/archive/v1/` 抽取。**v2 重写不得丢失任何一条原子**"
             "（`verify_all.py` H 项逐条核）。新事实原子预算 = 0。", "",
             f"| 文件 | cite | num | term | bold | quiz | critique | 小计 |",
             "| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |"]
    for key in FILES:
        d = ledger[key]
        sub = sum(len(v) for v in d.values())
        lines.append(f"| {key} | {len(d['cite'])} | {len(d['num'])} | {len(d['term'])} | "
                     f"{len(d['bold'])} | {len(d['quiz'])} | {len(d['critique'])} | {sub} |")
    lines.append(f"| **合计** | {sum(len(d['cite']) for d in ledger.values())} | "
                 f"{sum(len(d['num']) for d in ledger.values())} | {sum(len(d['term']) for d in ledger.values())} | "
                 f"{sum(len(d['bold']) for d in ledger.values())} | {sum(len(d['quiz']) for d in ledger.values())} | "
                 f"{sum(len(d['critique']) for d in ledger.values())} | **{total}** |")
    for key in FILES:
        d = ledger[key]
        lines += ["", f"## {key}", ""]
        for typ in ("cite", "term", "quiz", "critique", "bold", "num"):
            if d[typ]:
                lines.append(f"- **{typ}**（{len(d[typ])}）：" + "；".join(d[typ]))
    open(OUT_MD, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print(f"账本已生成：{total} 条原子 → {os.path.relpath(OUT_JSON, ROOT)} / {os.path.relpath(OUT_MD, ROOT)}")


def check() -> int:
    """当前 docs/ 源对照 v1 账本（H 项独立运行版）。"""
    if not os.path.exists(OUT_JSON):
        sys.exit("账本不存在，先运行 python3 tools/knowledge_atoms.py")
    ledger = json.load(open(OUT_JSON, encoding="utf-8"))
    bad = 0
    for key, atoms in ledger.items():
        p = os.path.join(ROOT, "docs", FILES[key].replace("lectures/", "lectures/"))
        cur = norm(open(p, encoding="utf-8").read())
        missing = {t: [a for a in lst if norm(a) not in cur] for t, lst in atoms.items()}
        missing = {t: v for t, v in missing.items() if v}
        if missing:
            bad += 1
            print(f"[FAIL] {key}:")
            for t, v in missing.items():
                for a in v[:8]:
                    print(f"    {t} 缺失: {a[:60]}")
                if len(v) > 8:
                    print(f"    … 共 {len(v)} 条 {t} 缺失")
        else:
            print(f"[OK] {key}: 六类原子全在")
    return 1 if bad else 0


if __name__ == "__main__":
    if "--check" in sys.argv:
        sys.exit(check())
    build()
