#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_whitepaper.py —— 由讲稿源文件装配《机器学习与气动外形优化 · 自学白皮书》
=============================================================================
设计目的（学 Mr.GUO 仓库《燃气轮机智能设计与前沿算法自学白皮书》的重建思路）：
  1. 每一讲都是 docs/lectures/NN.md 独立源文件，便于逐讲修订与验收；
  2. 目录、篇标题、讲次与论文真实章节页码的对应关系由本脚本统一生成，杜绝手抄漂移；
  3. 第五篇代码由 code/ 下的真实文件原样嵌入，杜绝文档里的代码跑不通；
  4. 缺失的讲次显式标记为「待重建」，并列出该讲的覆盖范围与页码，而不是悄悄略写；
  5. 锚点使用 ASCII 稳定 ID（lec-01 / part-0 / code-kriging-py），不依赖渲染器对中文标题的 slug 实现。

用法：
    python3 tools/build_whitepaper.py
"""
from __future__ import annotations

import hashlib
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # → 论文精读/白皮书
DOC = os.path.join(ROOT, "docs")
LECT_DIR = os.path.join(DOC, "lectures")
CODE_DIR = os.path.join(ROOT, "code")
OUT = os.path.join(ROOT, "机器学习与气动外形优化自学白皮书.md")

TBD_MARK = "<!-- TBD -->"

# ---------------------------------------------------------------------------
# 篇表：键 / 标签 / 标题 / 导语（None 表示该篇正文由独立文件提供）
# ---------------------------------------------------------------------------
PARTS = {
    "0": ("第一篇", "【全景与地基篇】",
          "本篇覆盖**讲 01–02**。它只回答一个问题：**CFD 驱动的气动外形优化到底卡在哪，"
          "机器学习又是从哪条缝里挤进来的。** 先用一张 XDSM 把传统流程拆成五个模块、五种数据，"
          "再把论文 §2.2 的六个挑战逐条摊开；然后从最老牌的代理模型 Kriging 讲起——"
          "因为今天所有「用神经网络替 CFD」的野心，都是它那句「我顺便告诉你我有多不确定」的延长线。"),
    "1": ("第二篇", "【机器学习工具箱篇】",
          "本篇覆盖**讲 03–05**，对应论文 §3 全部。它是工具箱，不是百科全书："
          "我们只挑三件在气动设计里真正被反复用坏的家伙——**降维**（PCA / 流形 / DMD：把一个场压成几个数）、"
          "**缺标签的学习**（半监督与强化学习：标签不够和没有标签是两件事）、"
          "**生成网络全家桶**（ANN / CNN / RNN / AE / VAE / GAN / PINN：从拟合一个数到造一张图）。"
          "每讲结尾都回到同一个问题：这个工具能不能替我省一次 CFD？"),
    "2": ("第三篇", "【ML 进场：ASO 的三大战场篇】",
          "本篇覆盖**讲 06–08**，对应论文 §4——全篇最承重的一章。它把战场切成三格："
          "**几何设计空间**（把几百维收窄成几十维，同时把畸形叶型挡在门外）、"
          "**气动评估**（预测三个系数 vs 预测整个流场，两种世界观）、"
          "**加速与工程约束**（设计点之外的抖振、载荷怎么便宜地算）。"
          "读完这三讲，你应该能在组会上把任何一篇「ML 做气动」的论文塞进这三格之一。"),
    "3": ("第四篇", "【优化架构与结论篇】",
          "本篇覆盖**讲 09–10**，对应论文 §4.3 与 §5。前面所有讲次都在省「一次评估」，"
          "这一篇问的是**整个循环长什么样**：代理式优化怎么排兵布点，"
          "交互式设计怎么把 CFD 的成本从循环里搬进训练里，强化学习优化为什么只在少量设计变量上灵过，"
          "生成式反设计凭什么能「看图造形」。最后以作者的三条结论与一句自我批评收口。"),
    "4": ("第五篇", "【实践与代码篇】可运行原型库", None),
    "5": ("第六篇", "【批判、对比与前瞻篇】", None),
}

# ---------------------------------------------------------------------------
# 讲次表：编号 / 所属篇 / 标题 / 覆盖章节 / PDF 页 / 配图
# 章节页码来自 ../章程与地图/资料映射.md（由 PDF 书签直读，非估算）
# ---------------------------------------------------------------------------
LECTURES = [
    ("01", "0", "XDSM 与六个挑战：传统气动外形优化长什么样、卡在哪", "§2 全部（2.1 / 2.2）", "4–6", "Fig. 1（p5）"),
    ("02", "0", "Kriging 及其亲戚：一个全局趋势 + 一张「谁跟谁像」的关系表", "§3.1", "7–16", "Fig. 2–16（p8–19）"),
    ("03", "1", "降维的本质：把一整个流场压成几个数", "§3.2", "17–25", "Fig. 17–24（p18–25）"),
    ("04", "1", "标签不够与没有标签：半监督、RBM/DBN 与强化学习", "§3.3–3.4", "26–31", "Fig. 25–31（p26–31）"),
    ("05", "1", "神经网络全家桶：从 ANN 到 PINN", "§3.5", "32–40", "Fig. 32–41（p32–41）"),
    ("06", "2", "几何设计空间：模态参数化与几何过滤", "§4.1（4.1.1 / 4.1.2）", "41–46", "Fig. 42–44（p44–47）"),
    ("07", "2", "气动评估：预测三个系数，还是预测整个流场", "§4.2.1–4.2.2", "47–56", "Table 2–3、Fig. 45（p57）"),
    ("08", "2", "别让 CFD 从零起跑：加速三招 + 把测不起的约束换成算得起的式子", "§4.2.3–4.2.4", "56–58", "Fig. 45（p57）"),
    ("09", "3", "优化架构：代理式、交互式、RL 与生成式反设计", "§4.3（4.3.1–4.3.4）", "58–67", "Fig. 46–47（p64–65）"),
    ("10", "3", "作者的三条结论与一句自我批评", "§5 Conclusions and Outlook", "68", "—"),
    ("11", "5", "批判性阅读：这篇综述的边界与可复现性", "全文 + 参考文献", "1–103", "—"),
    ("12", "5", "知识整合：一页报告与下一步选题清单", "（装配生成）", "—", "—"),
]

FRONT_PATH = os.path.join(DOC, "front_matter.md")
CH0_PATH = os.path.join(DOC, "chapter0.md")
PART6_PATH = os.path.join(DOC, "part6.md")
CODE_README = os.path.join(CODE_DIR, "README.md")


def read(path: str) -> str:
    if not os.path.exists(path):
        return ""
    with open(path, encoding="utf-8") as f:
        return f.read().strip()


def aid_tag(aid: str) -> str:
    return f'<a id="{aid}" name="{aid}"></a>'


def code_aid(filename: str) -> str:
    stem = re.sub(r"[^A-Za-z0-9]+", "-", filename).strip("-").lower()
    return f"code-{stem}"


def lecture_text(num: str) -> str:
    """返回讲稿正文；缺失或含 TBD 标记则返回显式待重建占位段。"""
    raw = read(os.path.join(LECT_DIR, f"{num}.md"))
    for num_, pp, title, scope, pages, figs in LECTURES:
        if num_ == num:
            break
    if not raw or TBD_MARK in raw:
        return stub(num, title, scope, pages, figs)
    return raw


def stub(num: str, title: str, scope: str, pages: str, figs: str) -> str:
    return (
        f"### 【讲{num}】{title}\n\n"
        f"> **状态：待重建。** 本讲正文尚未写入 `docs/lectures/{num}.md`——"
        "装配脚本拒绝用一段话冒充一讲（这是「宣称」与「内容」对不上的老病，必须公开挂牌，不许温和沉默）。\n>\n"
        f"> **已排定的骨架**：覆盖 **{scope}** ｜ PDF **第 {pages} 页** ｜ 配图 **{figs}**。\n>\n"
        "> **待写十节结构**：① 元数据表 → ② 生活与物理直觉引子 → ③ 工程死穴 → ④ 先认词表 → "
        "⑤ 数学从 0 到 1 推导 → ⑥ 操作流与图表读法 → ⑦ 审稿人批判 → ⑧ 承前启后 → "
        "⑨ 你的 Rotor 37 平台接哪一步 → ⑩ 自测 10 题（2 选择 + 2 填空 + 6 问答） → ⑪ 一句收口。"
    )


def src_hash() -> str:
    h = hashlib.sha256()
    for name in ("front_matter.md", "chapter0.md", "part6.md"):
        h.update(read(os.path.join(DOC, name)).encode())
    if os.path.isdir(LECT_DIR):
        for fn in sorted(os.listdir(LECT_DIR)):
            if fn.endswith(".md"):
                h.update(read(os.path.join(LECT_DIR, fn)).encode())
    if os.path.isdir(CODE_DIR):
        for fn in sorted(os.listdir(CODE_DIR)):
            if fn.endswith(".py"):
                with open(os.path.join(CODE_DIR, fn), "rb") as f:
                    h.update(f.read())
    return h.hexdigest()[:12]


def lecture_status_table() -> str:
    """十二讲 ↔ 章节对照表：状态由文件系统现算，杜绝 front matter 手抄漂移。"""
    rows = ["| 讲 | 覆盖 | PDF 页 | 配图 | 状态 |",
            "| :--- | :--- | :---: | :--- | :---: |"]
    n_done = 0
    for num, pp, title, scope, pages, figs in LECTURES:
        raw = read(os.path.join(LECT_DIR, f"{num}.md"))
        ok = bool(raw) and TBD_MARK not in raw
        n_done += ok
        rows.append(f"| {num} | {scope} ｜ {title} | {pages} | {figs} | "
                    f"{'✅ 已完成' if ok else '⬜ 待重建'} |")
    rows.append("")
    rows.append(f"> **本表由 `tools/build_whitepaper.py` 现算（讲稿文件在不在、有没有 `<!-- TBD -->` 标记），"
                f"不靠手抄。** 当前 **{n_done} / {len(LECTURES)}** 讲有正文；进度以 `../memory/PROGRESS.md` 为准。")
    return "\n".join(rows)


def build() -> str:
    out: list[str] = []
    front = read(FRONT_PATH).replace("<!-- LECTURE_STATUS_TABLE -->", lecture_status_table())
    out.append(front)
    out.append("")
    out.append(read(CH0_PATH))
    out.append("")

    # ---------------- 目录（渲染器无关的稳定锚点） ----------------
    toc = ['## 目录', '']
    toc.append('- [第零章 从零地基：一个黑箱、一千次预算与维度灾难](#ch0)')
    toc.append("  - [0.1 这本书的研究对象：一根会喘气的管子](#ch0-1)")
    toc.append("  - [0.2 什么是 CFD：把牛顿定律扔给超算去解](#ch0-2)")
    toc.append("  - [0.3 什么是「优化」：为什么不能全枚举](#ch0-3)")
    toc.append("  - [0.4 维度灾难：一个 74 维的算术题](#ch0-4)")
    for num, pp, title, scope, pages, figs in LECTURES:
        if pp not in ("0", "1", "2", "3") or num == "12":
            continue
        label, ptitle, _ = PARTS[pp]
        aid = f"part-{pp}"
        toc.append(f"- [{label} {ptitle}](#{aid})")
        done = read(os.path.join(LECT_DIR, f"{num}.md"))
        flag = "" if done and TBD_MARK not in done else "（⬜ 待重建）"
        toc.append(f"  - [【讲{num}】{title}{flag} ｜ {scope} ｜ PDF p{pages}](#lec-{num})")
    toc.append("- [第五篇 【实践与代码篇】可运行原型库](#part-4)")
    if os.path.isdir(CODE_DIR):
        for fn in sorted(os.listdir(CODE_DIR)):
            if fn.endswith(".py"):
                toc.append(f"  - [`{fn}`](#{code_aid(fn)})")
    toc.append("- [第六篇 【批判、对比与前瞻篇】](#part-5)")
    d12 = read(os.path.join(LECT_DIR, "12.md"))
    f12 = "" if d12 and TBD_MARK not in d12 else "（⬜ 待重建）"
    toc.append(f"- [【讲12】知识整合：一页报告与下一步选题清单{f12}](#lec-12)")
    out.append("\n".join(toc))
    out.append("")
    out.append("---")
    out.append("")
    out.append("> 📌 **本文件由 `tools/build_whitepaper.py` 自动装配生成，请勿直接编辑。**")
    out.append("> 要改内容请改 `docs/lectures/` 下的讲稿源文件，然后重跑装配脚本；"
               "验收请跑 `python3 tools/verify_all.py`。")
    out.append(f"> 内容版本：src-{src_hash()}（讲稿/代码源文件内容哈希；源不变则装配结果逐字节不变）")
    out.append("")
    out.append("---")
    out.append("")

    # ---------------- 各篇 + 讲次（篇 0–3，按讲次顺序；篇 5 的讲 11 挪到第六篇下） ----------------
    emitted: set[str] = set()
    for num, pp, title, scope, pages, figs in LECTURES:
        if num in ("11", "12") or pp not in ("0", "1", "2", "3"):
            continue
        if pp not in emitted:
            label, ptitle, lead = PARTS[pp]
            out.append(aid_tag(f"part-{pp}"))
            out.append(f"# {label} {ptitle}")
            out.append("")
            out.append(lead)
            out.append("")
            emitted.add(pp)
        out.append(aid_tag(f"lec-{num}"))
        out.append(lecture_text(num))
        out.append("")
        out.append("---")
        out.append("")

    # ---------------- 第五篇：代码 ----------------
    out.append(aid_tag("part-4"))
    out.append("# 第五篇 【实践与代码篇】可运行原型库")
    out.append("")
    out.append("本篇一律「能跑才算写完」：每个模块直接 `python3 code/<name>.py` 即可运行，"
               "末尾打印自检数字与 `PASS` 标记。正文里凡写「由 `code/xxx.py` 复算」的数字，"
               "都由本库当场算出，不是抄来的。")
    out.append("")
    readme = read(CODE_README)
    if readme:
        out.append(readme)
        out.append("")
    if os.path.isdir(CODE_DIR):
        for fn in sorted(os.listdir(CODE_DIR)):
            if not fn.endswith(".py"):
                continue
            out.append(aid_tag(code_aid(fn)))
            out.append(f"### `{fn}`")
            out.append("")
            out.append("```python")
            out.append(read(os.path.join(CODE_DIR, fn)))
            out.append("```")
            out.append("")
    out.append("---")
    out.append("")

    # ---------------- 第六篇（含讲 11 与讲 12） ----------------
    out.append(aid_tag("part-5"))
    out.append("# 第六篇 【批判、对比与前瞻篇】")
    out.append("")
    out.append(read(PART6_PATH))
    out.append("")
    out.append(aid_tag("lec-11"))
    out.append(lecture_text("11"))
    out.append("")
    out.append("---")
    out.append("")
    p12 = read(os.path.join(LECT_DIR, "12.md"))
    if p12 and TBD_MARK not in p12:
        out.append(aid_tag("lec-12"))
        out.append(p12)
        out.append("")

    text = "\n".join(out)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text + "\n"


if __name__ == "__main__":
    md = build()
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(md)
    done = [num for num, *_ in LECTURES
            if os.path.exists(os.path.join(LECT_DIR, f"{num}.md"))
            and TBD_MARK not in read(os.path.join(LECT_DIR, f"{num}.md"))]
    print(f"已装配 → {os.path.relpath(OUT, ROOT)}")
    print(f"  讲次共 {len(LECTURES)} 讲，其中正文已完成 {len(done)} 讲：{'、'.join(done) or '（无）'}")
    print(f"  字符数 {len(md)}，图片引用 {md.count('![')} 处")
