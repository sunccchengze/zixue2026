#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify_trainfield.py —— 训练场机器验收（I1–I5）
=====================================================================
对照 `../优化方案-v3-AI教练训练场.md` §8。教材卷的 A–H 八项不在此核（那是 make all）。

  I1 结构    units/u00–u12 各自存在；已有单元必须含 关卡卡.md / 教练脚本.md / 资产/
  I2 模板    关卡卡含 §3.2 的 7 个固定小节标题；教练脚本含 §3.3 的 7 个固定小节标题；
             文件头标记 <!-- uNN 关卡卡 v3.0 --> / <!-- uNN 教练脚本 v3.0 --> 与目录号一致
  I3 引用    关卡卡/教练脚本里的 〔教材卷 讲NN §k 题j〕〔教材卷 第零章 0.N〕〔code:xx.py〕
             〔B4 #n〕〔6.3 选题 n〕〔P01-local #n〕 逐条核到目标存在（防内容漂移）
  I4 资产账   资产总账.md 表头合法（8 列）；每行数据行的资产文件路径真实存在
  I5 抽查     每个教练脚本含「禁代写」；关卡卡含「时间盒 / 资产槽」；u12 脚本须含「一页报告」

用法：
    python3 tools/verify_trainfield.py             # 已有单元全核；未建单元 🔶 挂牌不算 FAIL
    python3 tools/verify_trainfield.py --require-all   # 要求 u00–u12 全部就位（W3 总验收用）
"""
from __future__ import annotations

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))     # → 论文精读/白皮书
TF = os.path.join(ROOT, "训练场")
UNITS = os.path.join(TF, "units")
DOCS = os.path.join(ROOT, "docs")
CODE = os.path.join(ROOT, "code")
FACTS = os.path.join(ROOT, "corpus", "facts")

ALL_UNITS = [f"u{i:02d}" for i in range(13)]        # u00–u12

LEVEL_CARD = [
    "## 0. 目标与验收线",
    "## 1. 前置与闸门",
    "## 2. 阅读地图（教材卷引用，JIT）",
    "## 3. 输出任务",
    "## 4. 判卷与入队",
    "## 5. 资产槽",
    "## 6. 时间盒与档位",
]
LEVEL_COACH = [
    "## 0. 开场",
    "## 1. 闸门判分要点",
    "## 2. 追问链",
    "## 3. 打脸与出处表",
    "## 4. 任务验收清单",
    "## 5. 禁代写清单",
    "## 6. 收尾写账模板",
]


def read(path: str) -> str:
    with open(path, encoding="utf-8") as f:
        return f.read()


def _unit_dir(u: str) -> str | None:
    """uNN 对应的目录（uNN-任意短名 或 uNN）。"""
    for name in sorted(os.listdir(UNITS)):
        if name == u or name.startswith(u + "-"):
            return os.path.join(UNITS, name)
    return None


def check_I1() -> tuple[int, list[str]]:
    """已有单元结构齐全；未建单元列出（不算 FAIL，--require-all 时才算）。"""
    n, fails = 0, []
    missing = []
    for u in ALL_UNITS:
        d = _unit_dir(u)
        if d is None:
            missing.append(u)
            continue
        for f in ("关卡卡.md", "教练脚本.md"):
            n += 1
            if not os.path.isfile(os.path.join(d, f)):
                fails.append(f"{u} 缺 {f}")
        if not os.path.isdir(os.path.join(d, "资产")):
            fails.append(f"{u} 缺 资产/ 目录")
    return n, fails, missing


def check_I2() -> tuple[int, list[str]]:
    n, fails = 0, []
    for u in ALL_UNITS:
        d = _unit_dir(u)
        if d is None:
            continue
        for name, heads in (("关卡卡.md", LEVEL_CARD), ("教练脚本.md", LEVEL_COACH)):
            p = os.path.join(d, name)
            if not os.path.isfile(p):
                continue
            txt = read(p)
            for h in heads:
                n += 1
                if h not in txt:
                    fails.append(f"{u}/{name} 缺固定小节标题：{h}")
            marker = f"<!-- {u} {'关卡卡' if name == '关卡卡.md' else '教练脚本'} v3.0 -->"
            n += 1
            if marker not in txt:
                fails.append(f"{u}/{name} 文件头标记缺失或目录号不一致：应为 {marker}")
    return n, fails


def _lecture_has_section(num: str, sec: str) -> bool:
    """讲 NN 是否含 '#### sec. ' 小节。"""
    p = os.path.join(DOCS, "lectures", f"{int(num):02d}.md")
    if not os.path.isfile(p):
        return False
    for line in read(p).splitlines():
        s = line.strip()
        m = re.match(r"^####\s*(\d+)\.", s)
        if m and m.group(1) == str(int(sec)):
            return True
    return False


def check_I3() -> tuple[int, list[str]]:
    """引用可回溯：〔教材卷 讲NN §k〕〔第零章 0.N〕〔code:…〕〔B4 #n〕〔6.3 选题 n〕
    〔P01-local #n[/#n…]〕〔原文 P## "…"〕逐条核到目标存在（防内容漂移）。"""
    n, fails = 0, []
    pat = re.compile(r"〔([^〕]+)〕")
    part6 = read(os.path.join(DOCS, "part6.md")) if os.path.isfile(os.path.join(DOCS, "part6.md")) else ""
    p01 = read(os.path.join(FACTS, "P01-local.md")) if os.path.isfile(os.path.join(FACTS, "P01-local.md")) else ""
    ch0 = read(os.path.join(DOCS, "chapter0.md")) if os.path.isfile(os.path.join(DOCS, "chapter0.md")) else ""
    book_txt = ""
    for bp in ([os.path.join(DOCS, "front_matter.md"), ch0, part6]
               + [os.path.join(DOCS, "lectures", f) for f in os.listdir(os.path.join(DOCS, "lectures"))
                  if f.endswith(".md")]):
        if os.path.isfile(bp):
            book_txt += read(bp) + "\n"

    def check_book(num: str, sec: str, quiz: str | None) -> str | None:
        lp = os.path.join(DOCS, "lectures", f"{int(num):02d}.md")
        if not os.path.isfile(lp):
            return f"docs/lectures/{num}.md 不存在"
        if not _lecture_has_section(num, sec):
            return f"讲{num} 无 §{sec} 小节"
        if quiz is not None:
            qn = int(quiz)
            if not any(re.match(rf"^\s*{qn}\.\s*（(选|填|答)）", ln) for ln in read(lp).splitlines()):
                return f"讲{num} §11 无第 {qn} 题"
        return None

    for u in ALL_UNITS:
        d = _unit_dir(u)
        if d is None:
            continue
        for name in ("关卡卡.md", "教练脚本.md"):
            p = os.path.join(d, name)
            if not os.path.isfile(p):
                continue
            txt = read(p)
            for body in pat.findall(txt):
                if body in ("存疑", "待核实", "延伸·待核实"):
                    continue  # 软标记，不判
                # ① code:xxx.py
                m = re.match(r"^code:([\w.-]+\.py)$", body)
                if m:
                    n += 1
                    if not os.path.isfile(os.path.join(CODE, m.group(1))):
                        fails.append(f"{u}/{name}：{body} → code/ 下无此文件")
                    continue
                # ② 教材卷 讲NN §k [题j] [标签]
                m = re.match(r"^(?:教材卷\s*)?讲(\d{2})\s*§(\d+)(\s*题(\d+))?(\s*[^〕]*)$", body)
                if m:
                    n += 1
                    err = check_book(m.group(1), m.group(2), m.group(4))
                    if err:
                        fails.append(f"{u}/{name}：{body} → {err}")
                    continue
                # ③ (教材卷 )第零章 0.N[a] [表]
                m = re.match(r"^(?:教材卷\s*)?第零章\s*0\.(\d+)([a-z]?)(\s*表)?$", body)
                if m:
                    n += 1
                    if not any(re.match(rf"^###\s*0\.{m.group(1)}\s", ln) for ln in ch0.splitlines()):
                        fails.append(f"{u}/{name}：{body} → 第零章无 0.{m.group(1)} 小节")
                    continue
                # ④ B4 #n
                m = re.match(r"^B4\s*#(\d+)$", body)
                if m:
                    n += 1
                    if not re.search(rf"^\|\s*#{int(m.group(1))}\s*\|", part6, re.M):
                        fails.append(f"{u}/{name}：{body} → part6.md 6.8 无该行")
                    continue
                # ⑤ 6.3 选题 n（①–⑥ 或 1–6）
                m = re.match(r"^6\.3\s*选题\s*([①-⑥]|\d+)$", body)
                if m:
                    n += 1
                    rows = re.findall(r"^\|\s*[①-⑥][^\n]*", part6, re.M)
                    idx = int(m.group(1)) if m.group(1).isdigit() else "①③⑤②④⑥".find(m.group(1)) // 2 + 1
                    if not (1 <= idx <= len(rows)):
                        fails.append(f"{u}/{name}：{body} → part6.md 6.3 表行数不足")
                    continue
                # ⑥ P01-local #n[/#m…]
                m = re.match(r"^P01-local\s*#(\d+)((?:/#\d+)*)$", body)
                if m:
                    n += 1
                    for num in [m.group(1)] + re.findall(r"#(\d+)", m.group(2)):
                        if not re.search(rf"^\|\s*{int(num)}\s*\|", p01, re.M):
                            fails.append(f"{u}/{name}：{body} → P01-local.md 无第 {int(num)} 行")
                    continue
                # ⑦ 原文 P## "连续片段"（须能在 docs/ 任一源文件脚注里找到同页同串）
                m = re.match(r'^原文\s*P(\d+)\s*"([^"]+)"', body)
                if m:
                    n += 1
                    page, quote = m.group(1), m.group(2)
                    if not re.search(rf'P{page}\s*"[^"]*{re.escape(quote)}', book_txt):
                        fails.append(f"{u}/{name}：{body} → docs/ 源文件脚注中找不到 P{page} 同串")
                    continue
                print(f"      · 〔{body}〕（{u}/{name}）未匹配 I3 语法，人工确认")
    return n, fails


def check_I4() -> tuple[int, list[str]]:
    n, fails = 0, []
    p = os.path.join(TF, "资产总账.md")
    if not os.path.isfile(p):
        return 0, ["缺 训练场/资产总账.md"]
    txt = read(p)
    head_ok = all(k in txt for k in ("| 行 |", "| 编号 |", "| 单元 |", "| 类 |", "| 资产文件",
                                     "| 名称/一句话 |", "| 状态 |", "| 日期 |"))
    if not head_ok:
        fails.append("资产总账.md 表头不合法（需 8 列，列不许增删改序）")
    for ln in txt.splitlines():
        if not re.match(r"^\|\s*\d+\s*\|", ln):
            continue
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if len(cells) != 8:
            fails.append(f"资产总账.md 行 {ln[:60]}… 列数 = {len(cells)} ≠ 8")
            continue
        n += 1
        rel = cells[4].strip("`")
        if rel in ("（此处列资产相对路径）", ""):
            continue
        if not os.path.isfile(os.path.join(TF, rel)):
            fails.append(f"资产总账.md 指向不存在：{rel}")
    return n, fails


def check_I5() -> tuple[int, list[str]]:
    n, fails = 0, []
    for u in ALL_UNITS:
        d = _unit_dir(u)
        if d is None:
            continue
        cp, sp = os.path.join(d, "关卡卡.md"), os.path.join(d, "教练脚本.md")
        if os.path.isfile(cp):
            txt = read(cp)
            for kw in ("## 5. 资产槽", "## 6. 时间盒与档位"):
                n += 1
                if kw not in txt:
                    fails.append(f"{u}/关卡卡.md 缺 {kw}")
        if os.path.isfile(sp):
            txt = read(sp)
            n += 1
            if "禁代写" not in txt:
                fails.append(f"{u}/教练脚本.md 缺 禁代写 小节")
            if u == "u12" and "一页报告" not in txt:
                fails.append("u12/教练脚本.md 须含「一页报告」收口件验收线")
    return n, fails


def main() -> int:
    require_all = "--require-all" in sys.argv
    bad = 0
    print("验收对象：训练场/（units/u00–u12）")
    i1n, i1f, missing = check_I1()
    if require_all and missing:
        i1f = i1f + [f"缺单元：{'、'.join(missing)}（--require-all）"]
    print("-" * 68)
    for name, fn in (("I1 结构", lambda: (i1n, i1f)), ("I2 模板", check_I2),
                     ("I3 引用", check_I3), ("I4 资产账", check_I4), ("I5 抽查", check_I5)):
        n, fails = fn()
        if fails:
            bad += 1
            print(f"❌ {name}：{len(fails)} 处问题（检查 {n} 项）")
            for f in fails[:12]:
                print(f"     · {f}")
            if len(fails) > 12:
                print(f"     · …另 {len(fails) - 12} 处")
        else:
            print(f"✅ {name}：{n} 项全过")
    if not require_all and missing:
        print(f"🔶 待建单元（不算 FAIL，W3 前补齐）：{'、'.join(missing)}")
    print("-" * 68)
    if bad:
        print("结论：训练场有验收未过 → 不得声称完成")
        return 1
    print("结论：训练场验收通过")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
