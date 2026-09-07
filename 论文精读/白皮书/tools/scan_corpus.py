#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scan_corpus.py —— 从论文提取语料现场统计"承重 / 盲区 / 口径"，供白皮书引用
=============================================================================
为什么要有这个脚本：白皮书第六篇与讲 11 会宣称"某技术在本综述 0 命中""某文献被引 N 次"。
这种话若靠人记忆，三年后就是假新闻。所以：**每次装配前重跑本脚本，讲稿只引用脚本输出**。

统计口径：
  · 正文区间 = PDF p3–p68（参考文献自 p69 起）；
  · 引用标记 = `[N]`、`[N, M]`、`[N–M]`/`[N-M]` 里的每一个编号（区间会展开）；
  · 参考文献条目数 = 参考文献区里行首编号的最大值；
  · 盲区关键词 = 在**参考文献区**做不区分大小写子串检索（连字与空白归一化后）。

用法：
    python3 tools/scan_corpus.py                 # 打印 + 写 corpus/facts/scan-results.md
    python3 tools/scan_corpus.py --dump PINN     # 打印某关键词全部命中页
"""
from __future__ import annotations

import argparse
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXTRACT = os.path.join(os.path.dirname(ROOT), "资料原件", "论文全文-提取文本.md")
OUT = os.path.join(ROOT, "corpus", "facts", "scan-results.md")

BODY_LO, BODY_HI, REF_LO = 3, 68, 69
BLINDSPOT_KEYS = ["fourier neural operator", "deeponet", "transformer", "diffusion", "sindy",
                  "physics-informed", "adjoint", "kriging", "nondeterministic polynomial"]
TOP_N = 12

LIG = {"ﬁ": "fi", "ﬂ": "fl", "ﬀ": "ff", "ﬃ": "ffi", "ﬄ": "ffl",
       "–": "-", "—": "-", "’": "'"}


def norm(t: str) -> str:
    for k, v in LIG.items():
        t = t.replace(k, v)
    return re.sub(r"\s+", " ", t)


def load_pages() -> dict[int, str]:
    txt = open(EXTRACT, encoding="utf-8").read()
    parts = re.split(r"<!-- ===== PDF 第 (\d+) 页 ===== -->", txt)
    return {int(parts[i]): parts[i + 1] for i in range(1, len(parts), 2)}


CIT = re.compile(r"\[([0-9]{1,3}(?:\s*,\s*[0-9]{1,3}){0,40}|[0-9]{1,3}\s*-\s*[0-9]{1,3})\]")


def ref_boundary(pages: dict[int, str]) -> tuple[int, int]:
    """返回参考文献区起点（页, 该页字符偏移）。PDF 书签说 §6 Bibliography 在 p69，
    但 p69 前 3.3k 字符仍是 §5 的尾巴，故按页内偏移切分。"""
    for p in range(BODY_HI, max(pages) + 1):
        i = pages.get(p, "").find("Bibliography")
        if i >= 0:
            return p, i
    return BODY_HI + 1, 0


def cite_counts(pages: dict[int, str]) -> tuple[dict[int, int], int]:
    cnt: dict[int, int] = {}
    total = 0
    for p in range(BODY_LO, BODY_HI + 1):
        raw = norm(pages.get(p, ""))
        for m in CIT.finditer(raw):
            body = m.group(1)
            if len(body) > 260:      # 明显是页码/公式串，跳过
                continue
            for tok in body.split(","):
                tok = tok.strip()
                mm = re.match(r"^(\d{1,3})\s*-\s*(\d{1,3})$", tok)
                if mm:
                    a, b = int(mm.group(1)), int(mm.group(2))
                    if 1 <= a < b <= 800 and b - a <= 40:
                        for k in range(a, b + 1):
                            cnt[k] = cnt.get(k, 0) + 1
                            total += 1
                    continue
                if tok.isdigit():
                    k = int(tok)
                    if 1 <= k <= 800:
                        cnt[k] = cnt.get(k, 0) + 1
                        total += 1
    return cnt, total


def max_ref_no(pages: dict[int, str]) -> int:
    """参考文献区条目用 [N] 起头；取该区最大编号即为条目数（本综述 528 条）。"""
    mx = 0
    for p in range(REF_LO, max(pages) + 1):
        for m in re.finditer(r"\[\s*(\d{1,3})\s*\]", pages.get(p, "")):
            mx = max(mx, int(m.group(1)))
    return mx


def keyword_hits(pages: dict[int, str], key: str, lo: int, hi: int) -> list[int]:
    k = norm(key).lower()
    out = []
    for p in range(lo, hi + 1):
        if k in norm(pages.get(p, "")).lower():
            out.append(p)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dump", metavar="KEY", help="打印某关键词在正文与参考文献中的命中页")
    args = ap.parse_args()
    if not os.path.exists(EXTRACT):
        print(f"❌ 找不到语料：{EXTRACT}")
        return 1
    pages = load_pages()
    cnt, total = cite_counts(pages)
    nref = max_ref_no(pages)

    if args.dump:
        hits_b = keyword_hits(pages, args.dump, BODY_LO, BODY_HI)
        hits_r = keyword_hits(pages, args.dump, REF_LO, max(pages))
        print(f"关键词「{args.dump}」：正文命中页 {hits_b}；参考文献命中页 {hits_r}")
        return 0

    top = sorted(cnt.items(), key=lambda kv: (-kv[1], kv[0]))[:TOP_N]
    blind = {k: keyword_hits(pages, k, REF_LO, max(pages)) for k in BLINDSPOT_KEYS}

    lines = ["# 语料扫描结果（自动生成，勿手改）", "",
             f"- 语料：`{os.path.basename(EXTRACT)}`（{len(pages)} 页）",
             f"- 统计区间：正文 p{BODY_LO}–p{BODY_HI}；参考文献 p{REF_LO}–p{max(pages)}",
             f"- 正文引用标记展开后的编号出现次数合计：**{total}**",
             f"- 不同被引编号个数：**{len(cnt)}**；参考文献区最大条目号：**{nref}**",
             "", "## 一、承重榜（本综述正文里被引最多的文献编号）", "",
             "| 参考文献编号 | 正文出现次数 |", "| :--- | :---: |"]
    for k, v in top:
        lines.append(f"| [{k}] | {v} |")
    lines += ["", "## 二、盲区关键词（在参考文献区 p{}–{} 的命中页数）".format(REF_LO, max(pages)), "",
              "| 关键词 | 命中页数 | 命中页 |", "| :--- | :---: | :--- |"]
    for k, hits in blind.items():
        s = "、".join(str(h) for h in hits[:8]) + ("…" if len(hits) > 8 else "")
        lines.append(f"| {k} | {len(hits)} | {s or '—'} |")
    lines += ["", "> 复核方法：`python3 tools/scan_corpus.py --dump \"<关键词>\"`。",
              "> 白皮书正文引用本文件时，必须写「由 `tools/scan_corpus.py` 实测」，不得写「论文说」。", ""]

    body = "\n".join(lines)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w", encoding="utf-8").write(body)
    print(body)
    print(f"→ 已写入 {os.path.relpath(OUT, ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
