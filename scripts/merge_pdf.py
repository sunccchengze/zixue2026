#!/usr/bin/env python3
"""merge_pdf.py · 仓级通用 PDF 合并器（带书签目录）

用法：
    python scripts/merge_pdf.py -o 输出.pdf --item "书签标题|源文件.pdf" [--item ...]

说明：
- 只用 pypdf（纯 Python，无系统依赖），逐字节搬运页面对象，不做重排/重压缩，
  因此矢量图、公式、字体嵌入全部保持原样；
- 每个 --item 生成一条一级书签（outline），指向该文件的第一页；
- 输出会打印每段的页码区间，便于人工核对。
"""
from __future__ import annotations

import argparse
import os
import sys

from pypdf import PdfReader, PdfWriter


def merge(items: list[tuple[str, str]], out_path: str) -> int:
    writer = PdfWriter()
    total = 0
    plan = []
    for title, path in items:
        if not os.path.isfile(path):
            raise FileNotFoundError(path)
        reader = PdfReader(path)
        if reader.is_encrypted:
            try:
                reader.decrypt("")
            except Exception as exc:  # pragma: no cover
                raise RuntimeError(f"{path} 加密且无法解密: {exc}") from exc
        start = len(writer.pages)
        for page in reader.pages:
            writer.add_page(page)
        n = len(reader.pages)
        writer.add_outline_item(title, start)
        plan.append((title, path, start + 1, start + n, n))
        total += n

    os.makedirs(os.path.dirname(os.path.abspath(out_path)) or ".", exist_ok=True)
    with open(out_path, "wb") as fh:
        writer.write(fh)

    print(f"[merge_pdf] -> {out_path}")
    for title, path, a, b, n in plan:
        print(f"    p{a:>4}-{b:<4} ({n:>3}页)  {title}   <= {os.path.basename(path)}")
    print(f"[merge_pdf] 合计 {total} 页，{len(items)} 个来源")
    return total


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="合并 PDF 并生成书签")
    ap.add_argument("-o", "--out", required=True, help="输出 PDF 路径")
    ap.add_argument(
        "--item",
        action="append",
        required=True,
        metavar="TITLE|PATH",
        help="书签标题|源 PDF 路径（可重复，按给定顺序合并）",
    )
    args = ap.parse_args(argv)

    items = []
    for raw in args.item:
        if "|" not in raw:
            print(f"[merge_pdf] --item 需要 '标题|路径' 形式，收到: {raw}", file=sys.stderr)
            return 2
        title, path = raw.split("|", 1)
        items.append((title.strip(), path.strip()))
    merge(items, args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
