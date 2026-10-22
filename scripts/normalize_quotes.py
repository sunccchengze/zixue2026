#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 知识框架精讲_v4.py 里的 « » 占位符统一转成中文引号 “ ”。

为什么要这一步
--------------
撰写底稿时，中文引号 “ ” 容易被编辑器/工具链静默规范化成 ASCII 双引号 "，
从而把 Python 字符串提前截断（SyntaxError）。因此底稿一律用 « » 书写，
由本脚本一次性、可重复地（幂等）转成最终排版用的中文引号。

用法：
    python scripts/normalize_quotes.py            # 原地转换
    python scripts/normalize_quotes.py --check    # 只体检，不写入
"""
from __future__ import annotations

import argparse
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "大学物理" / "课程作业" / "知识框架精讲_v4.py",
]

# 成对替换时使用“遇开则开、遇闭则闭”的状态机，
# 这样同一对占位符可以跨越引号、换行、字段边界。
OPEN = "“"
CLOSE = "”"


def convert(text: str) -> str:
    out = []
    opening = True
    for ch in text:
        if ch == "«":
            out.append(OPEN)
            opening = False
        elif ch == "»":
            out.append(CLOSE)
            opening = True
        else:
            out.append(ch)
    if not opening:
        print("警告：占位符 « / » 数量不成对，请检查", file=sys.stderr)
    return "".join(out)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="只统计，不写入")
    args = parser.parse_args()

    total = 0
    for path in TARGETS:
        if not path.exists():
            print(f"跳过（不存在）：{path}")
            continue
        raw = path.read_text(encoding="utf-8")
        count = raw.count("«") + raw.count("»")
        if count == 0:
            print(f"已规范：{path.name}（无占位符）")
            continue
        if args.check:
            print(f"待转换：{path.relative_to(ROOT)}（{count} 个占位符）")
            total += count
            continue
        path.write_text(convert(raw), encoding="utf-8")
        print(f"已转换：{path.relative_to(ROOT)}（{count} 个占位符）")
        total += count
    print(f"合计 {total} 个占位符")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
