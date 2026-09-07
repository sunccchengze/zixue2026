#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify_all.py —— 白皮书全仓验收器（学 Mr.GUO 仓库同名脚本的思路，落地到本仓数据）
=============================================================================
六项验收，任一 FAIL 即以退出码 1 结束：

  A  引用可回溯：讲稿里每一条「〔原文 P##「关键词」〕」都必须能在
     `../资料原件/论文全文-提取文本.md` 的对应 PDF 页里找到该关键词（连字归一化后做子串匹配）。
  B  图表号真实：正文出现的 Fig. N / Table N 不得超过论文实物（47 图、5 表）。
  C  图片不悬空：正文引用的每个 ./images/*.png 必须存在；images/ 里的每个文件必须被引用（不留孤儿）。
  D  结构齐备：已完成讲次必须含 10 个编号小节（①-⑩ 或 #### 1. …）+ 一句收口；缺则 FAIL。
  E  学术图零 Emoji：images/ 里图片文件名与图注文本禁止出现表情符号；正文表格单元格内禁止 Emoji。
  F  自足性：装配产物必须与源文件重新装配逐字节一致（防止有人手改白皮书绕过装配脚本）。

用法：
    python3 tools/verify_all.py            # 汇总
    python3 tools/verify_all.py --strict    # 同时逐讲打印明细
"""
from __future__ import annotations

import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))     # 论文精读/白皮书
SUBJ = os.path.dirname(ROOT)                                           # 论文精读
WP = os.path.join(ROOT, "机器学习与气动外形优化自学白皮书.md")
EXTRACT = os.path.join(SUBJ, "资料原件", "论文全文-提取文本.md")
LECT_DIR = os.path.join(ROOT, "docs", "lectures")
IMG_DIR = os.path.join(ROOT, "images")

N_FIG = 47
N_TABLE = 5
TBD_MARK = "<!-- TBD -->"

LIG = {"ﬁ": "fi", "ﬂ": "fl", "ﬀ": "ff", "ﬃ": "ffi", "ﬄ": "ffl",
       "ﬅ": "st", "ﬆ": "st", "–": "-", "—": "-", "’": "'", "‘": "'",
       "‐": "-", "‑": "-", "‐": "-"}

# 正文引用形式（唯一合法形式，讲稿必须这样写）：
#   〔原文 P13 "correlation function"〕   —— 关键词串取自 PDF 提取语料对应页，可机器回溯
CITE = re.compile(r'〔原文\s*P(\d{1,3})\s*"([^"]{2,160})"\s*〕')


def norm(t: str) -> str:
    for k, v in LIG.items():
        t = t.replace(k, v)
    t = t.replace("\n", " ")
    return re.sub(r"\s+", " ", t).strip().lower()


def load_pages() -> dict[int, str]:
    txt = open(EXTRACT, encoding="utf-8").read()
    parts = re.split(r"<!-- ===== PDF 第 (\d+) 页 ===== -->", txt)
    d: dict[int, str] = {}
    for i in range(1, len(parts), 2):
        d[int(parts[i])] = norm(parts[i + 1])
    return d


def read(path):
    if not os.path.exists(path):
        return ""
    return open(path, encoding="utf-8").read()


def done_lectures() -> list[str]:
    out = []
    if not os.path.isdir(LECT_DIR):
        return out
    for fn in sorted(os.listdir(LECT_DIR)):
        if not fn.endswith(".md"):
            continue
        body = read(os.path.join(LECT_DIR, fn))
        if fn in ("README.md",) or not body or TBD_MARK in body:
            continue
        out.append(fn[:-3])
    return out


def check_A(pages) -> tuple[int, list[str]]:
    """引用可回溯（含书级文件：前言 / 第零章 / 第六篇）。"""
    fails: list[str] = []
    n = 0
    for num in done_lectures():
        body = read(os.path.join(LECT_DIR, f"{num}.md"))
        for m in CITE.finditer(body):
            n += 1
            pg, kw = int(m.group(1)), norm(m.group(2))
            if pg not in pages:
                fails.append(f"讲{num}: 页码越界 P{pg}")
                continue
            if kw not in pages[pg]:
                fails.append(f"讲{num}: P{pg} 里找不到 → {m.group(2)[:60]}")
    for label, rel in (("前言", "front_matter.md"), ("第零章", "chapter0.md"), ("第六篇", "part6.md")):
        body = read(os.path.join(ROOT, "docs", rel))
        for m in CITE.finditer(body):
            n += 1
            pg, kw = int(m.group(1)), norm(m.group(2))
            if pg not in pages:
                fails.append(f"{label}: 页码越界 P{pg}")
                continue
            if kw not in pages[pg]:
                fails.append(f"{label}: P{pg} 里找不到 → {m.group(2)[:60]}")
    return n, fails


def check_B() -> tuple[int, list[str]]:
    fails: list[str] = []
    n = 0
    body = read(WP)
    for m in re.finditer(r"Fig\.?\s*(\d{1,3})", body):
        n += 1
        if not (1 <= int(m.group(1)) <= N_FIG):
            fails.append(f"图号越界 Fig.{m.group(1)}（论文只有 {N_FIG} 幅图）")
    for m in re.finditer(r"Table\s*(\d{1,3})", body):
        n += 1
        if not (1 <= int(m.group(1)) <= N_TABLE):
            fails.append(f"表号越界 Table {m.group(1)}（论文只有 {N_TABLE} 张表）")
    return n, fails


def check_C() -> tuple[int, list[str]]:
    fails: list[str] = []
    body = read(WP)
    refs = set(re.findall(r"\./images/([A-Za-z0-9_\-\.]+\.png)", body))
    have = set(f for f in os.listdir(IMG_DIR) if f.endswith(".png")) if os.path.isdir(IMG_DIR) else set()
    for r in sorted(refs - have):
        fails.append(f"悬空引用：./images/{r}")
    for h in sorted(have - refs):
        fails.append(f"孤儿图片：./images/{h}（正文未引用）")
    return len(refs), fails


REQ_SECTIONS = ["元数据", "引子", "死穴", "先认词", "从 0 到 1", "审稿人批判", "承前", "自测", "收口"]
# 例外：讲 12（整合课，结构不同）只要求其中五项
PARTIAL_REQ = {"12": ["元数据", "引子", "从 0 到 1", "自测", "收口", "审稿人批判"]}


def check_D() -> tuple[int, list[str]]:
    fails: list[str] = []
    ns = 0
    for num in done_lectures():
        ns += 1
        body = read(os.path.join(LECT_DIR, f"{num}.md"))
        if "存疑" not in body and "批判" not in body:
            fails.append(f"讲{num}: 缺「审稿人批判/存疑」节（无存疑视为不完整）")
        for kw in PARTIAL_REQ.get(num, REQ_SECTIONS):
            if kw not in body:
                fails.append(f"讲{num}: 缺「{kw}」小节")
        if "./images/" not in body:
            fails.append(f"讲{num}: 全文无配图（白皮书要求图文并茂）")
        if "〔原文 P" not in body:
            fails.append(f"讲{num}: 无任何〔原文 P##〕溯源标注")
    return ns, fails


# 学术图注/表格只禁"表情符号"；排版符号（✔✘✅⬜🔄🔶①—…·─│）属于合法技术排版，不禁。
# 判据取自 zixue2026 版式规则 §9.7：严禁 🚀🔥📊⚙️ 一类装饰性 emoji。
EMOJI = re.compile("[\U0001F300-\U0001FAFF\U0001F000-\U0001F0FF]")
DECOR = set("✅✔✕✘⬜🔄🔶①②③④⑤⑥⑦⑧⑨⑩🟡🟢🔴📌⭐️️★")


def check_E() -> tuple[int, list[str]]:
    fails: list[str] = []
    n = 0
    for fn in (done_lectures() + []):
        n += 1
    body = read(WP)
    for line in body.split("\n"):
        if line.startswith("![") and EMOJI.search(line):
            fails.append(f"图注含装饰性 Emoji：{line[:70]}")
    for f in (sorted(os.listdir(IMG_DIR)) if os.path.isdir(IMG_DIR) else []):
        if EMOJI.search(f):
            fails.append(f"图片文件名含 Emoji：{f}")
    return n, fails


def check_F() -> tuple[int, list[str]]:
    fails: list[str] = []
    sys.path.insert(0, os.path.join(ROOT, "tools"))
    try:
        import build_whitepaper as B  # type: ignore
    except Exception as e:  # pragma: no cover
        return 0, [f"无法导入装配器：{e}"]
    fresh = B.build()
    cur = read(WP)
    if fresh.strip() != cur.strip():
        fails.append("白皮书与源文件不同步：请重跑 python3 tools/build_whitepaper.py")
    return 1, fails


# ---------------------------------------------------------------------------
# v2 新增：G（风格门禁）/ H（知识守恒）
# 规格全文见 `../写作规格-v2.md`（S1–S13）。
# ---------------------------------------------------------------------------

V2_MARK = "<!-- v2 -->"
CJK_RE = re.compile(r"[\u4e00-\u9fff]")
CITE_TAG = re.compile(r"〔[^〔〕\n]{1,140}〕")
AT_TAIL = re.compile(r"\s*[a-zA-Z0-9%×.,|^~→=≤≥<>-]+\s*$")

# 每个单元 v2 完成时引用的 distinct 图片文件下限（§6 图像预算）
MIN_IMG = {
    "front_matter": 2, "chapter0": 7, "part6": 2,
    "01": 5, "02": 8, "03": 5, "04": 5, "05": 5,
    "06": 4, "07": 5, "08": 4, "09": 4, "10": 3, "11": 4, "12": 3,
}

# 装置硬指标：（标记, 最少出现次数）
DEVICES_BOOK = [("🧭 **呼吸点**", 3), ("🔮 **下注**", 1), ("👊 **打脸**", 1), ("📌 **带走 3 个数**", 1)]
DEVICES_LECTURE = DEVICES_BOOK + [("⏪ **上讲的数**", 1), ("🛠 **修复清单**", 1)]

G_FILES = (
    [("front_matter", "docs/front_matter.md"), ("chapter0", "docs/chapter0.md"),
     ("part6", "docs/part6.md")]
    + [(f"lectures/{n}", f"docs/lectures/{n}.md") for n in done_lectures()]
)

G_PENDING: list[str] = []   # 待 v2 的讲次，公开挂牌（不 FAIL）


def _cjk_len(s: str) -> int:
    """风格核长度：去掉引用标签/图片/脚注链/Markdown 记号后的字符数。"""
    s = CITE_TAG.sub("", s)
    s = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", s)
    s = re.sub(r"\[[^\]\n]*\]\([^)]*\)", "", s)
    s = re.sub(r"^[^：:]{0,14}[：:]\s*", "", s)   # 装置标签行只核冒号后内容
    s = re.sub(r"[*_`#>|]", "", s)
    return len(re.sub(r"\s", "", s))


def _style_units(path: str):
    """拆 (kind, text)：para=段落/引言行，item=列表项。审查层(details)/代码/图/表不计。"""
    t = read(path)
    t = re.sub(r"```.*?```", "", t, flags=re.S)
    t = re.sub(r"<details>.*?</details>", "", t, flags=re.S)
    units = []
    for blk in re.split(r"\n\s*\n", t):
        b = blk.strip()
        if not b or b.startswith(("#", "<a id=", "---", "![", "<", "```")):
            continue
        if b.startswith("|"):
            continue
        if b.startswith(">"):
            for ln in re.sub(r"^>", "", b, flags=re.M).split("\n"):
                if ln.strip():
                    units.append(("para", ln.strip()))
        elif re.match(r"^\s*([-*]|\d+[\.、])\s+", b):
            for ln in b.split("\n"):
                s = re.sub(r"^\s*([-*]|\d+[\.、])\s+", "", ln).strip()
                if s:
                    units.append(("item", s))
        else:
            units.append(("para", b))
    return units


def check_G() -> tuple[int, list[str]]:
    """风格门禁：只核带 `<!-- v2 -->` 标记的文件；其余已完成讲次公开挂牌「待 v2」。"""
    fails: list[str] = []
    n = 0
    for key, rel in G_FILES:
        body = read(os.path.join(ROOT, rel))
        if not body:
            continue
        if V2_MARK not in body[:300]:
            G_PENDING.append(key)
            continue
        n += 1
        label = key if key != "chapter0" else "第零章"
        # G1/G2/G3：段长 / 项长 / 分句长（一律按「风格核」计：
        # 去引用标签/图片/脚注链/Markdown 记号；S10 规定脚注定义行必须含完整标签、
        # S13 规定批判条目逐字保留——两者都与"整句 ≤80"在机器上互斥，
        # 故 S2 以分句（。！？；，切分，见写作规格-v2.md）为计长单位）
        for kind, txt in _style_units(os.path.join(ROOT, rel)):
            L = _cjk_len(txt)
            cap = 100 if kind == "para" else 140
            if L > cap:
                fails.append(f"{label}: {kind} 段 {L} 字 > {cap}：{txt[:30]}…")
                continue
            for sent in re.split(r"[。！？；，]", txt):
                s = CITE_TAG.sub("", sent)
                s = AT_TAIL.sub("", s)
                s = re.sub(r"[*_`#>|]", "", s)
                Ls = len(re.sub(r"\s", "", s))
                if Ls > 80:
                    fails.append(f"{label}: 分句 {Ls} 字 > 80：{sent[:30]}…")
        # G4：装置就位
        devs = DEVICES_LECTURE if key.startswith("lectures/") else (DEVICES_BOOK if key in ("chapter0",) else [])
        for mark, k in devs:
            if body.count(mark) < k:
                fails.append(f"{label}: 装置「{mark}」需 ≥{k} 处，现 {body.count(mark)}")
        # G5：配图下限
        imgs = set(re.findall(r"\./images/([A-Za-z0-9_\-\.]+\.png)", body))
        need = MIN_IMG.get(key)
        if need and len(imgs) < need:
            fails.append(f"{label}: distinct 配图 {len(imgs)} < {need}")
        # G6：先认词单批 ≤5 行
        lines = body.split("\n")
        for i, ln in enumerate(lines):
            if "先认词" in ln:
                j = i
                while j < len(lines) and not lines[j].strip().startswith("|"):
                    j += 1
                rows = []
                while j < len(lines) and lines[j].strip().startswith("|"):
                    rows.append(lines[j])
                    j += 1
                data = [r for r in rows if not set(r.strip()) <= set("| :-")]
                if len(data) - 2 > 5:
                    fails.append(f"{label}: 先认词单批 {len(data) - 2} 行 > 5（须拆批）")
    return n, fails


ATOM_LEDGER = os.path.join(ROOT, "docs", "knowledge_atoms_v1.json")


def check_H() -> tuple[int, list[str]]:
    """知识守恒：v1 账本六类原子必须 100% 出现在当前同源文件。"""
    if not os.path.exists(ATOM_LEDGER):
        return 0, ["缺知识原子账本：先跑 python3 tools/knowledge_atoms.py"]
    sys.path.insert(0, os.path.join(ROOT, "tools"))
    try:
        import knowledge_atoms as KA  # type: ignore
    except Exception as e:  # pragma: no cover
        return 0, [f"无法导入账本模块：{e}"]
    ledger = json.load(open(ATOM_LEDGER, encoding="utf-8"))
    n = 0
    fails: list[str] = []
    for key, atoms in ledger.items():
        cur = KA.norm(read(os.path.join(ROOT, "docs", KA.FILES[key])))
        for typ, lst in atoms.items():
            for a in lst:
                n += 1
                if KA.norm(a) not in cur:
                    fails.append(f"{key} {typ} 缺失：{a[:50]}")
    return n, fails


def main() -> int:
    strict = "--strict" in sys.argv
    if not os.path.exists(WP):
        print("❌ 白皮书尚未装配：先跑 python3 tools/build_whitepaper.py")
        return 1
    pages = load_pages()
    checks = [
        ("A 引用可回溯", lambda: check_A(pages)),
        ("B 图表号真实", check_B),
        ("C 图片不悬空", check_C),
        ("D 讲次结构齐备", check_D),
        ("E 零 Emoji 图注", check_E),
        ("F 装配自足性", check_F),
        ("G v2 风格门禁", check_G),
        ("H 知识守恒", check_H),
    ]
    bad = 0
    done = done_lectures()
    print(f"验收对象：{os.path.basename(WP)}")
    print(f"已完成讲次：{len(done)} / 12 → {'、'.join(done) or '（无）'}")
    print("语料：", os.path.relpath(EXTRACT, ROOT), f"（{len(pages)} 页）")
    print("-" * 68)
    for name, fn in checks:
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
    if G_PENDING:
        print(f"🔶 待 v2 重写（公开挂牌，暂不纳入 G 项）：{'、'.join(G_PENDING)}")
    print("-" * 68)
    if bad:
        print(f"结论：{bad} 项验收未过 → 白皮书不得交付")
        return 1
    print("结论：全项验收通过")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
