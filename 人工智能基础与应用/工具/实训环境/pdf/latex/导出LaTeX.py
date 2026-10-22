#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LaTeX 导出通道：Markdown → 可编译 .tex → PDF（自带 Tectonic wasm 引擎）· Agent 维护 · B7

与 typst 通道（导出全库.py）的关系：
  · typst 通道负责"人读的主 PDF"（中文排版稳、字体子集化、页眉页脚）
  · 本通道负责"LaTeX 正典"：每份文档都有**真正能编译**的 .tex 与它编译出的 PDF
  两条通道都从同一份 Markdown 母版出发，所以内容永远一致。

产物（文件名里的「-LaTeX版」是刻意的，避免与 typst PDF 混淆）：
  ① 课题NN-*/课题NN-*-LaTeX版.pdf      + 课题NN-*.tex（就地替换为可编译版本）
  ② 合集/课题全集-11个课题-LaTeX版.pdf  + .tex
  ③ 合集/人工智能基础与应用-总集-LaTeX版.pdf + .tex
  ④ 讲义/pdf/大模型实训讲义-全书-LaTeX版.pdf + .tex
  ⑤ 章程与地图/pdf/章程与地图-全书-LaTeX版.pdf + .tex

用法：
  python 导出LaTeX.py --all          # 全部
  python 导出LaTeX.py --topics       # 11 个课题 + 两个整体版
  python 导出LaTeX.py --lectures --charter
  python 导出LaTeX.py --check        # 只核验已有 LaTeX PDF
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent          # 环境/pdf/latex/
PDF_DIR = HERE.parent                           # 环境/pdf/
SUBJECT = PDF_DIR.parent.parent                 # 人工智能基础与应用/
COMBINE_DIR = SUBJECT / "合集"
NODE = "node"
DRIVER = HERE / "编译LaTeX.mjs"
MD2TEX = HERE / "md到LaTeX.py"


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


EXP = _load("导出全库", PDF_DIR / "导出全库.py")     # 复用文件发现与合并逻辑
M2T = _load("md到LaTeX", MD2TEX)                    # 复用 MD→tex 转换器


# ── 文档清单 ────────────────────────────────────────────────────────────────

class Doc:
    def __init__(self, title: str, md_files: list[Path], tex: Path, pdf: Path,
                 toc: bool = True, subs: str = ""):
        self.title = title
        self.md_files = md_files
        self.tex = tex
        self.pdf = pdf
        self.toc = toc
        self.subs = subs


def topic_docs() -> list[Doc]:
    out = []
    for d in EXP.TOPIC_DIRS:
        files = EXP.md_files_of(d, prefer=["开题简报", "判卷记录", "报告", "README"])
        if not files:
            continue
        name = d.name
        out.append(Doc(name, files, d / f"{name}-LaTeX版.tex", d / f"{name}-LaTeX版.pdf"))
    return out


def combined_docs() -> list[Doc]:
    topics = [f for d in EXP.TOPIC_DIRS
              for f in EXP.md_files_of(d, prefer=["开题简报", "判卷记录"])]
    groups = {
        "课题全集-11个课题": topics,
        "人工智能基础与应用-总集": ([SUBJECT / "README.md"] + EXP.lecture_files()
                                    + EXP.charter_files() + topics),
    }
    out = []
    for title, files in groups.items():
        files = [f for f in files if f.exists()]
        out.append(Doc(title, files, COMBINE_DIR / f"{title}-LaTeX版.tex",
                       COMBINE_DIR / f"{title}-LaTeX版.pdf"))
    return out


def set_docs(kind: str) -> list[Doc]:
    if kind == "lectures":
        return [Doc("大模型实训讲义-全书", EXP.lecture_files(),
                    PDF_DIR.parent / "讲义" / "pdf" / "大模型实训讲义-全书-LaTeX版.tex",
                    PDF_DIR.parent / "讲义" / "pdf" / "大模型实训讲义-全书-LaTeX版.pdf")]
    d = SUBJECT / "章程与地图"
    return [Doc("章程与地图-全书", EXP.charter_files(),
                d / "pdf" / "章程与地图-全书-LaTeX版.tex",
                d / "pdf" / "章程与地图-全书-LaTeX版.pdf")]


# ── 渲染 ────────────────────────────────────────────────────────────────────

def build_tex(docs: list[Doc]) -> list[Doc]:
    """合并 Markdown → .tex（本函数结束后 docs 里的 .tex 都是最新的）"""
    import pypandoc
    pandoc = pypandoc.get_pandoc_path()
    ok_docs: list[Doc] = []
    with tempfile.TemporaryDirectory() as td:
        for doc in docs:
            if not doc.md_files:
                print(f"  ✘ {doc.title}：没有源文件")
                continue
            merged = EXP.merge_md(doc.md_files, Path(td) / f"{doc.title}.md")
            doc.tex.parent.mkdir(parents=True, exist_ok=True)
            ok, err, unknown = M2T.md_to_tex(merged, doc.tex, doc.title, pandoc,
                                             toc=doc.toc, number=True)
            flag = "✔" if ok else "✘"
            extra = f" 未覆盖字符 {unknown}" if unknown else ""
            print(f"  {flag} {doc.tex.name}  （{len(doc.md_files)} 份 md → tex）{extra}")
            if not ok:
                print("     ", err)
                continue
            if unknown:
                print(f"     ✘ 有 {len(unknown)} 个字符三套字体都不含 → 视为失败，先补字体再导出")
                continue
            ok_docs.append(doc)
    return ok_docs


def compile_all(docs: list[Doc]) -> int:
    """一次 node 调用编译全部 .tex（引擎只加载一次宏包树）"""
    if not docs:
        return 0
    # tex=pdf 显式指定输出名，避免覆盖 typst 通道的主 PDF
    cmd = [NODE, str(DRIVER), *[f"{d.tex}={d.pdf}" for d in docs]]
    r = subprocess.run(cmd, capture_output=True, text=True)
    print(r.stdout.rstrip())
    if r.stderr.strip():
        print("  [stderr]", r.stderr.strip()[:600])
    return r.returncode


def verify(docs: list[Doc]) -> int:
    """核验 PDF：页数、体积、文本层是否含中文"""
    import pymupdf
    bad = 0
    print("\n核验：")
    for doc in docs:
        if not doc.pdf.exists():
            print(f"  ✘ {doc.pdf.name}：缺文件")
            bad += 1
            continue
        try:
            d = pymupdf.open(doc.pdf)
            text = "".join(p.get_text() for p in d)
            cn = sum(1 for ch in text if "\u4e00" <= ch <= "\u9fff")
            kb = doc.pdf.stat().st_size / 1024
            good = d.page_count > 0 and kb > 20 and cn >= 80
            print(f"  {'✔' if good else '✘'} {doc.pdf.name}  {d.page_count} 页 / {kb:.0f} KB / 汉字 {cn}")
            if not good:
                bad += 1
        except Exception as exc:                     # noqa: BLE001
            print(f"  ✘ {doc.pdf.name}：打不开（{exc}）")
            bad += 1
    return bad


def check_all() -> int:
    docs = topic_docs() + combined_docs() + set_docs("lectures") + set_docs("charter")
    pairs = [(d, d.pdf) for d in docs]
    class _Shim:                                      # verify() 只用到 .pdf/.name
        def __init__(self, p):
            self.pdf = p
            self.name = p.name
    return verify([d for d, _ in pairs])


# ── 入口 ────────────────────────────────────────────────────────────────────

def main() -> int:
    ap = argparse.ArgumentParser(description="LaTeX 导出通道")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--topics", action="store_true", help="11 个课题 + 两个整体版")
    ap.add_argument("--lectures", action="store_true")
    ap.add_argument("--charter", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    if args.check:
        bad = check_all()
        print(f"\n核验完成：{'全部通过' if bad == 0 else str(bad) + ' 个有问题'}")
        return 1 if bad else 0

    wanted: list[Doc] = []
    if args.all or args.topics:
        wanted += topic_docs() + combined_docs()
    if args.all or args.lectures:
        wanted += set_docs("lectures")
    if args.all or args.charter:
        wanted += set_docs("charter")
    if not wanted:
        ap.print_help()
        return 2

    print(f"【LaTeX 通道】共 {len(wanted)} 份文档\n")
    print("第一步：Markdown → .tex")
    docs = build_tex(wanted)
    print(f"\n第二步：编译 {len(docs)} 份 .tex → PDF")
    compile_all(docs)
    print("\n第三步：核验")
    bad = verify(docs)
    print(f"\n完成：{'全部通过' if bad == 0 else str(bad) + ' 个有问题'}（{len(docs)} 份）")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
