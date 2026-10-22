#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把《知识框架精讲_v4.py》的零基础精讲底稿导出成 Markdown。

为什么要有这一步
----------------
2026-09-29 有两个会话并行做了同一个需求。对方除 docx 外还手写了一份
`12-15次作业·知识精讲（零基础版）.md`，而它与 docx 的口径并不一致
（md 覆盖四次，docx 当时只重写了第十三次）。两份产物讲同一件事却内容不同，
正是《仓库使用手册.md》判例⑯说的“撞错门”。

解决办法：把 Markdown 变成**从同一份底稿生成**的第二个渲染后端，
而不是另一份手写稿。底稿 = `大学物理/课程作业/知识框架精讲_v4.py`，
渲染后端 = docx（scripts/generate_physics_midterm_docx_v4.py）＋ 本脚本。
两者口径必然一致。

用法：
    python scripts/export_framework_markdown.py            # 写入目标文件
    python scripts/export_framework_markdown.py --stdout   # 打到标准输出（便于 diff）
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE = ROOT / "大学物理" / "课程作业"
OUT = ROOT / "大学物理" / "期中复习" / "12-15次作业·知识精讲（零基础版）.md"

sys.path.insert(0, str(COURSE))
from 知识框架精讲_v4 import DEEP_FRAMEWORK, SECTION_TITLES  # noqa: E402
from 逐题深度解析_v3 import ERRATA  # noqa: E402

CIRCLED = "①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳"
SESSIONS = [
    (12, "机械波", "波动方程 · 干涉 · 驻波 · 波的能量 · 多普勒效应"),
    (13, "波动光学 1：干涉", "相干条件 · 时间/空间相干性 · 双缝 · 薄膜 · 劈尖 · 牛顿环 · 迈克尔逊"),
    (14, "波动光学 2：衍射与光栅", "单缝半波带法 · 光栅方程 · 缺级 · 光谱重叠 · 分辨本领"),
    (15, "波动光学 3：偏振", "偏振态 · 马吕斯定律 · 布儒斯特角 · 双折射 · 波片"),
]
# 提示框颜色 → Markdown 标记，与 docx 的四色一一对应
CALLOUT_TAG = {"key": "【结论要点】", "warn": "【易错提醒】",
               "tip": "【技巧补充】", "myth": "【反直觉】"}


def block_to_md(block) -> str:
    kind = block[0]
    if kind == "h3":
        return f"### {block[1]}"
    if kind == "h4":
        return f"#### {block[1]}"
    if kind == "p":
        return block[1]
    if kind == "ul":
        return "\n".join(f"- {item}" for item in block[1])
    if kind == "ol":
        return "\n".join(
            f"{CIRCLED[i] if i < len(CIRCLED) else str(i + 1) + '.'} {item}"
            for i, item in enumerate(block[1]))
    if kind == "formula":
        return f"> **{block[1]}**"
    if kind == "callout":
        tag = CALLOUT_TAG.get(block[3] if len(block) > 3 else "key", "【结论要点】")
        return f"> **{tag}** {block[2]}"
    if kind == "table":
        headers, rows = block[1], block[2]
        lines = ["| " + " | ".join(headers) + " |",
                 "|" + "|".join(["---"] * len(headers)) + "|"]
        for row in rows:
            lines.append("| " + " | ".join(str(c) for c in row) + " |")
        return "\n".join(lines)
    if kind == "figure":
        return f"![{block[2]}](../课程作业/图卡/{block[1]})"
    if kind == "summary":
        return f"> **一句话总结** {block[1]}"
    raise ValueError(f"未知块类型：{kind!r}")


def build_markdown() -> str:
    parts = [
        "# 大学物理 12–15 次作业 · 知识精讲（零基础版）",
        "",
        "> 孙承泽　·　能动强基2501　·　2026-09-29",
        "> 本文件与 docx《大学物理期中_12-15次作业图文精析》**共用同一份底稿**"
        "（`大学物理/课程作业/知识框架精讲_v4.py`），由 "
        "`scripts/export_framework_markdown.py` 生成，内容不会与 docx 走偏。",
        "> 阅读顺序：先读本文件把物理图像建立起来，再去做 docx 里的逐题解析。",
        "> 标记：**粗体**＝关键词；【结论要点】＝必须背；【易错提醒】＝高频失分点；"
        "【技巧补充】＝省时间；【反直觉】＝老师一定会停下来强调的地方。",
        "",
        "---",
        "",
    ]
    for session, title, topic in SESSIONS:
        parts.append(f"## 第 {session} 次　{title}")
        parts.append("")
        parts.append(f"**本次考点：**{topic}")
        parts.append("")
        for block in DEEP_FRAMEWORK[session]:
            parts.append(block_to_md(block))
            parts.append("")
        parts.append(f"### 速览表　（{' / '.join(SECTION_TITLES[session])}）")
        parts.append("")
        for idx, item in enumerate(SECTION_TITLES[session], 1):
            parts.append(f"{idx:02d}　{item}")
        parts.append("")
        parts.append("---")
        parts.append("")

    parts.append("## 附录一　答案资料差异与勘误")
    parts.append("")
    parts.append("下列条目会直接影响选项或计算结果。docx 的附录节是同一份列表，"
                 "两个后端口径一致。")
    parts.append("")
    for idx, note in enumerate(ERRATA, 1):
        parts.append(f"{idx:02d}　{note}")
    parts.append("")
    parts.append("## 附录二　重建与校验")
    parts.append("")
    parts.append("- 底稿：`大学物理/课程作业/知识框架精讲_v4.py`"
                 "（改动后先跑 `python scripts/normalize_quotes.py` 把 « » 转成中文引号）")
    parts.append("- 生成 docx：`python scripts/generate_physics_midterm_docx_v4.py`")
    parts.append("- 生成本 md：`python scripts/export_framework_markdown.py`")
    parts.append("- 审计两者：`python scripts/audit_physics_midterm_v4.py`")
    parts.append("- 底稿里的中文引号请一律写成 `«` `»` 占位符——直接写 `“` `”` "
                 "会被工具链静默规范化成 ASCII 双引号，导致 Python 字符串截断。")
    parts.append("")
    return "\n".join(parts)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stdout", action="store_true", help="打到标准输出，不写文件")
    args = parser.parse_args()
    md = build_markdown()
    if args.stdout:
        print(md)
        return 0
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(md, encoding="utf-8")
    print(f"Created: {OUT} ({OUT.stat().st_size / 1024:.0f} KB, {md.count(chr(10)) + 1} 行)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
