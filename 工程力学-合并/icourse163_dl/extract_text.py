#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把下载的所有 PDF 抽成结构化文本库 corpus.json"""
import os, glob, json, re
from pypdf import PdfReader

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "downloads")
corpus = []
for pdf in sorted(glob.glob(os.path.join(OUT, "**", "*.pdf"), recursive=True)):
    rel = os.path.relpath(pdf, OUT)
    parts = rel.split(os.sep)
    chap, les, fname = (parts + ["", "", ""])[:3]
    r = PdfReader(pdf)
    pages = []
    for i, p in enumerate(r.pages, 1):
        t = p.extract_text() or ""
        t = re.sub(r"[ \t]+", " ", t)
        t = re.sub(r"\n{3,}", "\n\n", t).strip()
        if t:
            pages.append({"page": i, "text": t})
    corpus.append({
        "file": rel, "chapter": chap, "lesson": les, "name": fname,
        "n_pages": len(r.pages), "pages": pages,
        "text": "\n".join(f"[p{p['page']}] {p['text']}" for p in pages),
    })
    print(f"{len(r.pages):3d}页 {len(corpus[-1]['text']):6d}字  {rel}")

json.dump(corpus, open("corpus.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"\n合计 {len(corpus)} 个文档, {sum(c['n_pages'] for c in corpus)} 页, "
      f"{sum(len(c['text']) for c in corpus)} 字符 -> corpus.json")
