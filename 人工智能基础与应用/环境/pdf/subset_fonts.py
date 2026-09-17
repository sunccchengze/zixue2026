#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""字体子集化 · 让讲义字体从 43 MB 降到几 MB（B7 脚手架）

为什么要做：中文字体动辄 15 MB/个字重，四个字重就 43 MB。这些字体并不进 git
（在仓库外的 /home/user/opt/fonts/），但会占持久化快照的额度。子集化到"实际会
用到的字符集"后体积降一个数量级，而**渲染结果完全不变**。

覆盖集的三层保险（宁可留多，不可少字）：
  ① GB2312 全部 6763 个汉字（讲义正文必然落在这一层）
  ② **仓库里所有 .md 文件实际出现过的每一个字符**（当前讲义 + 章程 + 记忆 + 课题，一个不落）
  ③ 拉丁/希腊/西里尔 + 常用标点 + 数学符号 + 箭头 + 圈号 + 几何/制表符（公式与符号用）

安全网：`环境/pdf/md2typst.py` 每次编译都会做**字形覆盖自检**，
若讲义里出现字体链没有的字形（会渲染成豆腐块），会直接报出来。
真缺字时的兜底：重跑 `bootstrap.sh`（从 npm 取回**完整**字体）。

用法：
  python3 subset_fonts.py            # 于 /home/user/opt/fonts 就地子集化
  python3 subset_fonts.py --report   # 只看覆盖统计，不写文件
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont

FONT_DIR = Path("/home/user/opt/fonts")
REPO = Path("/home/user/zixue2026")

TARGETS = {
    "NotoSerifSC-Regular.ttf": "宋体正文",
    "NotoSerifSC-Bold.ttf": "宋体粗体",
    "NotoSansSC-Regular.ttf": "黑体正文",
    "NotoSansSC-Bold.ttf": "黑体粗体",
}
KEEP_AS_IS = ["NotoEmoji-Regular.ttf", "DejaVuSans.ttf", "DejaVuSansMono.ttf"]


def gb2312_chars() -> set[str]:
    """GB2312 全部汉字 + 全角标点（用编码往返枚举，比抄表可靠）"""
    out: set[str] = set()
    for hi in range(0xA1, 0xF8):
        for lo in range(0xA1, 0xFF):
            try:
                out.add(bytes([hi, lo]).decode("gb2312"))
            except UnicodeDecodeError:
                pass
    return out


def repo_text_chars() -> set[str]:
    """仓库里所有 Markdown / YAML / Python / Shell 文件出现过的字符"""
    out: set[str] = set()
    exts = {".md", ".yaml", ".yml", ".py", ".sh", ".txt", ".json"}
    for p in REPO.rglob("*"):
        if not p.is_file() or p.suffix.lower() not in exts:
            continue
        parts = set(p.parts)
        if parts & {"上游", ".git", ".venv", "node_modules", "pdf"}:   # 上游代码与本目录产物跳过
            continue
        try:
            out |= set(p.read_text(encoding="utf-8"))
        except Exception:                        # noqa: BLE001
            continue
    return out


def symbol_ranges() -> set[str]:
    """拉丁/希腊/西里尔 + 标点 + 数学 + 箭头 + 圈号 + 几何/制表 + 常用 CJK 标点"""
    ranges = [
        (0x0020, 0x007E), (0x00A0, 0x00FF), (0x0100, 0x017F),        # ASCII / Latin-1 / Latin Ext-A
        (0x0180, 0x024F), (0x0370, 0x03FF), (0x0400, 0x04FF),        # Latin Ext-B / Greek / Cyrillic
        (0x2000, 0x206F), (0x20A0, 0x20BF), (0x2100, 0x214F),        # 标点 / 货币 / 字母式符号
        (0x2150, 0x218F), (0x2190, 0x21FF), (0x2200, 0x22FF),        # 数字形 / 箭头 / 数学算子
        (0x2300, 0x23FF), (0x2460, 0x24FF), (0x2500, 0x257F),        # 技术符号 / 圈号 / 制表符
        (0x2580, 0x259F), (0x25A0, 0x25FF), (0x2600, 0x26FF),        # 方块 / 几何 / 杂项
        (0x2700, 0x27BF), (0x2E80, 0x2EFF), (0x3000, 0x303F),        # 装饰 / CJK 部首 / CJK 标点
        (0x3040, 0x30FF), (0xFF00, 0xFFEF), (0xFE30, 0xFE4F),        # 假名 / 全角 / CJK 兼容形式
    ]
    out: set[str] = set()
    for a, b in ranges:
        for cp in range(a, b + 1):
            try:
                out.add(chr(cp))
            except ValueError:
                pass
    return out


def coverage(font: TTFont) -> set[int]:
    cmap: set[int] = set()
    for table in font["cmap"].tables:
        cmap |= set(table.cmap.keys())
    return cmap


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", action="store_true", help="只报告，不写文件")
    a = ap.parse_args()

    chars = gb2312_chars() | repo_text_chars() | symbol_ranges()
    print(f"覆盖集：{len(chars)} 个码位"
          f"（GB2312 {len(gb2312_chars())} + 仓库实际用字 + 符号区）")

    total_before = total_after = 0
    for name, label in TARGETS.items():
        p = FONT_DIR / name
        if not p.exists():
            print(f"  ⚠ 缺少 {name}（先跑 bootstrap.sh）"); continue
        before = p.stat().st_size
        f = TTFont(p, lazy=True)
        have = coverage(f)
        # 必须保留 .notdef 与布局需要的字符；只取覆盖集与之的交集，再并上 0x20 等基础
        keep = {cp for cp in have if (chr(cp) in chars if cp < 0x110000 else False)} | {0x20, 0xA0}
        missing = sorted({ord(c) for c in chars if len(c) == 1 and ord(c) not in have})
        print(f"  {name:<26} {before/1048576:6.1f} MB → 保留 {len(keep):>5} 字形"
              f"（覆盖集里缺 {len(missing)} 个码位）")
        if a.report:
            continue
        out = p.with_suffix(".subset.ttf")
        opts = subset.Options()
        opts.layout_features = ["*"]        # 保留 kerning 等排印特性
        opts.name_IDs = ["*"]
        opts.notdef_outline = True
        opts.recalc_bounds = True
        opts.drop_tables = ["EBDT", "EBLC", "SVG "]   # 位图/彩色变体不需要
        font = subset.load_font(str(p), opts)
        subsetter = subset.Subsetter(options=opts)
        subsetter.populate(unicodes=keep)
        subsetter.subset(font)
        subset.save_font(font, str(out), opts)
        after = out.stat().st_size
        out.replace(p)                      # 就地替换
        total_before += before; total_after += after
        print(f"      → {after/1048576:6.2f} MB")

    if not a.report and total_before:
        print(f"\n合计 {total_before/1048576:.1f} MB → {total_after/1048576:.1f} MB"
              f"（省 {100*(1-total_after/total_before):.0f}%）")
        print("兜底：若讲义出现缺字，重跑 bootstrap.sh 取回完整字体")
    return 0


if __name__ == "__main__":
    sys.exit(main())
