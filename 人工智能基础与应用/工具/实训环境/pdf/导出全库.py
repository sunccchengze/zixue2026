#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""全库导出器：Markdown → PDF（typst）/ DOCX（pandoc）/ TeX（pandoc）· Agent 维护 · B7

一次性产出用户要的全部格式：
  ① 每个课题独立：课题NN-*/课题NN-*.pdf + .docx + .tex
  ② 整体版：合集/人工智能基础与应用-总集.{pdf,docx,tex}
           合集/课题全集-11个课题.{pdf,docx,tex}
  ③ 讲义与章程：讲义/pdf/大模型实训讲义-全书.{pdf,docx}、章程与地图/pdf/章程与地图-全书.{pdf,docx}

约定：
  · PDF 引擎用 typst（本机可用、中文正确、可离线；.tex 源同时给出，供 LaTeX 环境编译）
  · DOCX 走 pandoc + 自建 reference.docx（正文宋体 10.5pt / 标题黑体，中文字形在 Word 里正确）
  · 原始 Markdown 会被写进产物（合并版），但**母版永远是各目录下的 .md**

用法：
  python 导出全库.py --all          # 全量导出
  python 导出全库.py --topics       # 只做 11 个课题 + 整体版
  python 导出全库.py --lectures --charter
  python 导出全库.py --check        # 只核验已有产物的页数/体积/文本完整性
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
SUBJECT = HERE.parent.parent
sys.path.insert(0, str(HERE))

import md2typst as M                      # noqa: E402  复用自己的转换器与模板

FONT_DIR = M.FONT_DIR
TOPIC_DIRS = sorted(p for p in SUBJECT.glob("课题*") if p.is_dir())
COMBINE_DIR = SUBJECT / "合集"
REF_DOCX = HERE / "templates" / "reference.docx"

# 分隔页：用三种格式各自的 raw block，避免在别的格式里显示成正文
PAGEBREAK = """
```{=typst}
#pagebreak()
```

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

```{=latex}
\\newpage
```

"""


# ── 文件发现 ────────────────────────────────────────────────────────────────

def md_files_of(d: Path, prefer: list[str] | None = None) -> list[Path]:
    """目录下的 markdown，按 prefer 前缀排序（开题简报优先），其余按名排"""
    files = sorted(p for p in d.rglob("*.md") if p.is_file()
                   and not any(part in {"pdf", "docx", "合集"} for part in p.parts))
    if prefer:
        def key(p: Path) -> tuple[int, str]:
            for i, name in enumerate(prefer):
                if p.name.startswith(name):
                    return (i, p.name)
            return (len(prefer), p.name)
        files.sort(key=key)
    return files


def lecture_files() -> list[Path]:
    order = ["README.md", "M0-数学与机器学习地基.md", "M1-从n-gram到Transformer.md",
             "M2-分词与表示.md", "M3-Transformer内部机制.md", "M4-M9-待展开大纲.md"]
    files = [M.LECTURE_DIR / f for f in order if (M.LECTURE_DIR / f).exists()]
    files += sorted(p for p in M.LECTURE_DIR.glob("*.md") if p.name not in order)
    return files


def charter_files() -> list[Path]:
    order = ["知识地图-大模型全景.md", "对标教学资源清单.md", "知行合一规程.md",
             "实训路线图.md", "造轮子边界.md", "AI使用红线.md",
             "算力与成本预算.md", "判分与验收标准.md", "上游锁定清单.md"]
    d = SUBJECT / "章程与地图"
    files = [d / f for f in order if (d / f).exists()]
    files += sorted(p for p in d.glob("*.md") if p.name not in order)
    return files


# ── 合并与渲染 ──────────────────────────────────────────────────────────────

def merge_md(files: list[Path], out_md: Path, with_break: bool = True) -> Path:
    parts = []
    for i, f in enumerate(files):
        if i and with_break:
            parts.append(PAGEBREAK)
        parts.append(f.read_text(encoding="utf-8").rstrip() + "\n")
    out_md.write_text("\n".join(parts), encoding="utf-8")
    return out_md


def make_pdf(md_path: Path, out_pdf: Path, title: str, subtitle: str, toc: bool = False) -> tuple[bool, str]:
    """Markdown → typst → PDF（复用讲义排版模板，封面/目录可选）"""
    try:
        body = M.md_to_typst_body(md_path)
    except M.MathError as exc:
        return False, f"公式翻译失败：{exc}"
    if toc:
        # 在正文前插入目录页
        pre = ('#[\n  = 目录\n'
               '  #show outline.entry.where(level: 1): set text(weight: "bold", size: 11pt, fill: ACCENT)\n'
               '  #show outline.entry.where(level: 2): set text(size: 9.8pt, fill: luma(60))\n'
               '  #outline(title: none, depth: 2, indent: 1.15em)\n  #pagebreak()\n]\n')
    else:
        pre = ""
    typ = M.build_typst(title, body, subtitle=subtitle, pre=pre)
    ok, err = M.compile_pdf(typ, out_pdf)
    return ok, err


def pandoc_bin() -> str:
    import pypandoc
    return pypandoc.get_pandoc_path()


PANDOC_ARGS_COMMON = ["-f", "markdown+raw_attribute+pipe_tables+tex_math_dollars",
                      "--wrap=none", "--toc", "--toc-depth=2"]


def make_docx(md_path: Path, out_docx: Path, title: str) -> tuple[bool, str]:
    cmd = [pandoc_bin(), str(md_path), "-o", str(out_docx),
           *PANDOC_ARGS_COMMON, "--standalone",
           f"--metadata=title:{title}", "--metadata=lang:zh-CN"]
    if REF_DOCX.exists():
        cmd.append(f"--reference-doc={REF_DOCX}")
    r = subprocess.run(cmd, capture_output=True, text=True)
    return (r.returncode == 0), (r.stderr or "")[:400]


def make_tex(md_path: Path, out_tex: Path, title: str) -> tuple[bool, str]:
    cmd = [pandoc_bin(), str(md_path), "-o", str(out_tex), "-t", "latex", "--standalone",
           *PANDOC_ARGS_COMMON, "--number-sections",
           f"--metadata=title:{title}", "--metadata=lang:zh-CN",
           "-V", "documentclass=ctexart", "-V", "fontsize=11pt",
           "-V", "geometry:margin=2.2cm", "-V", 'CJKmainfont=Noto Serif SC',
           "-V", 'CJKsansfont=Noto Sans SC', "-V", 'CJKmonofont=DejaVu Sans Mono']
    r = subprocess.run(cmd, capture_output=True, text=True)
    return (r.returncode == 0), (r.stderr or "")[:400]


def build_reference_docx() -> Path | None:
    """生成 DOCX 样式模板：正文宋体/Times New Roman 10.5pt，标题黑体"""
    try:
        import docx                                     # python-docx
        from docx.oxml.ns import qn
        from docx.shared import Pt
    except ImportError:
        print("  ⚠ 未安装 python-docx，DOCX 将用 pandoc 默认样式（中文字体由 Word 回退）")
        return None
    REF_DOCX.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        base = Path(td) / "base.docx"
        with base.open("wb") as fh:
            subprocess.run([pandoc_bin(), "--print-default-data-file", "reference.docx"],
                           stdout=fh, check=True)
        d = docx.Document(str(base))
        spec = {
            "Normal":    ("宋体", "Times New Roman", 10.5),
            "Body Text": ("宋体", "Times New Roman", 10.5),
            "Title":     ("黑体", "Arial", 22),
            "Heading 1": ("黑体", "Arial", 16),
            "Heading 2": ("黑体", "Arial", 14),
            "Heading 3": ("黑体", "Arial", 12),
            "Heading 4": ("黑体", "Arial", 11),
            "Compact":   ("宋体", "Times New Roman", 10.5),
            "Source Code": ("DejaVu Sans Mono", "DejaVu Sans Mono", 9),
            "Verbatim Char": ("DejaVu Sans Mono", "DejaVu Sans Mono", 9),
            "Table Caption": ("宋体", "Times New Roman", 9.5),
        }
        for name, (east, latin, size) in spec.items():
            try:
                st = d.styles[name]
            except KeyError:
                continue
            rpr = st.element.get_or_add_rPr()
            rf = rpr.get_or_add_rFonts()
            rf.set(qn("w:ascii"), latin)
            rf.set(qn("w:hAnsi"), latin)
            rf.set(qn("w:eastAsia"), east)
            rf.set(qn("w:cs"), latin)
            st.font.size = Pt(size)
            # 去掉主题字体属性，确保显式字体一定生效（Word 里 theme 属性会干扰判断）
            for attr in ("w:asciiTheme", "w:hAnsiTheme", "w:eastAsiaTheme", "w:cstheme"):
                if rf.get(qn(attr)) is not None:
                    del rf.attrib[qn(attr)]
        # 全局默认字体（docDefaults）
        styles_el = d.styles.element
        dd = styles_el.find(qn("w:docDefaults"))
        if dd is not None:
            rpr_d = dd.find(qn("w:rPrDefault"))
            if rpr_d is not None:
                rpr = rpr_d.find(qn("w:rPr"))
                if rpr is None:
                    from docx.oxml import OxmlElement
                    rpr = OxmlElement("w:rPr"); rpr_d.append(rpr)
                rf = rpr.find(qn("w:rFonts"))
                if rf is None:
                    from docx.oxml import OxmlElement
                    rf = OxmlElement("w:rFonts"); rpr.insert(0, rf)
                for k, v in (("w:ascii", "Times New Roman"), ("w:hAnsi", "Times New Roman"),
                             ("w:eastAsia", "宋体"), ("w:cs", "Times New Roman")):
                    rf.set(qn(k), v)
        d.save(str(REF_DOCX))
    return REF_DOCX


# ── 清单渲染 ────────────────────────────────────────────────────────────────

ROWS: list[tuple[str, str, str, str]] = []


def note(kind: str, path: Path, ok: bool, err: str = "") -> None:
    if not ok:
        ROWS.append((kind, str(path.relative_to(SUBJECT)), "✘", err[:70] or "失败"))
        return
    size = path.stat().st_size
    pages = ""
    if path.suffix == ".pdf":
        try:
            import pymupdf
            pages = f"{pymupdf.open(path).page_count} 页"
        except Exception:                                  # noqa: BLE001
            pages = "?"
    elif path.suffix == ".docx":
        try:
            with zipfile.ZipFile(path) as z:
                xml = z.read("word/document.xml").decode("utf-8", "ignore")
            pages = f"{len(re.findall(r'<w:p[ >]', xml))} 段"
        except Exception:                                  # noqa: BLE001
            pages = "?"
    ROWS.append((kind, str(path.relative_to(SUBJECT)), f"{size/1024:.0f} KB", pages))


def dump_rows() -> int:
    bad = sum(1 for r in ROWS if r[2] == "✘")
    print("\n" + "=" * M.W)
    print(f"{'类型':<10}{'文件':<52}{'体积':>8}  {'规模':>8}")
    print("-" * M.W)
    for kind, f, size, pages in ROWS:
        print(f"{kind:<10}{f:<52}{size:>8}  {pages:>8}")
    print("=" * M.W)
    print(f"共 {len(ROWS)} 个产物，失败 {bad} 个" + ("  ✔ 全部通过" if not bad else "  ✘ 见上"))
    return bad


# ── 主流程 ──────────────────────────────────────────────────────────────────

def export_topic(d: Path, want=("pdf", "docx", "tex")) -> None:
    name = d.name
    files = md_files_of(d, prefer=["开题简报", "判卷记录", "报告", "README"])
    if not files:
        return
    print(f"\n【{name}】{len(files)} 份文档")
    with tempfile.TemporaryDirectory() as td:
        merged = merge_md(files, Path(td) / f"{name}.md")
        if "pdf" in want:
            out = d / f"{name}.pdf"
            ok, err = make_pdf(merged, out, name, "开题简报 · 交付要求 · 判卷记录", toc=len(files) > 1)
            note("课题PDF", out, ok, err)
            print(f"  PDF  {'✔' if ok else '✘'}  {out.name}")
        if "docx" in want:
            out = d / f"{name}.docx"
            ok, err = make_docx(merged, out, name)
            note("课题DOCX", out, ok, err)
            print(f"  DOCX {'✔' if ok else '✘'}  {out.name}")
        if "tex" in want:
            out = d / f"{name}.tex"
            ok, err = make_tex(merged, out, name)
            note("课题TeX", out, ok, err)
            print(f"  TeX  {'✔' if ok else '✘'}  {out.name}")


def export_combined(want=("pdf", "docx", "tex")) -> None:
    COMBINE_DIR.mkdir(parents=True, exist_ok=True)
    groups = {
        "课题全集-11个课题": [f for d in TOPIC_DIRS for f in md_files_of(d, prefer=["开题简报", "判卷记录"])],
        "人工智能基础与应用-总集": ([SUBJECT / "README.md"] + lecture_files() + charter_files()
                                   + [f for d in TOPIC_DIRS for f in md_files_of(d, prefer=["开题简报", "判卷记录"])]),
    }
    for title, files in groups.items():
        files = [f for f in files if f.exists()]
        print(f"\n【整体版：{title}】{len(files)} 份文档")
        with tempfile.TemporaryDirectory() as td:
            merged = merge_md(files, Path(td) / f"{title}.md")
            if "pdf" in want:
                out = COMBINE_DIR / f"{title}.pdf"
                ok, err = make_pdf(merged, out, title,
                                   "人工智能基础与应用 · 大模型实训" , toc=True)
                note("整体PDF", out, ok, err)
                print(f"  PDF  {'✔' if ok else '✘'}  {out.name}")
            if "docx" in want:
                out = COMBINE_DIR / f"{title}.docx"
                ok, err = make_docx(merged, out, title)
                note("整体DOCX", out, ok, err)
                print(f"  DOCX {'✔' if ok else '✘'}  {out.name}")
            if "tex" in want:
                out = COMBINE_DIR / f"{title}.tex"
                ok, err = make_tex(merged, out, title)
                note("整体TeX", out, ok, err)
                print(f"  TeX  {'✔' if ok else '✘'}  {out.name}")


def export_set(label: str, files: list[Path], outdir: Path, stem: str,
               subtitle: str, want=("pdf", "docx")) -> None:
    if not files:
        return
    print(f"\n【{label}】{len(files)} 份文档")
    outdir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        merged = merge_md(files, Path(td) / f"{stem}.md")
        if "pdf" in want:
            out = outdir / f"{stem}.pdf"
            ok, err = make_pdf(merged, out, label, subtitle, toc=True)
            note(label + "PDF", out, ok, err)
            print(f"  PDF  {'✔' if ok else '✘'}  {out.name}")
        if "docx" in want:
            out = outdir / f"{stem}.docx"
            ok, err = make_docx(merged, out, label)
            note(label + "DOCX", out, ok, err)
            print(f"  DOCX {'✔' if ok else '✘'}  {out.name}")


def verify_existing() -> int:
    """核验已有产物：PDF 页数 + 抽文本，DOCX 段落数 + 抽文本"""
    bad = 0
    for p in sorted(SUBJECT.rglob("*.pdf")):
        if any(x in p.parts for x in ("上游", "templates")):
            continue
        try:
            import pymupdf
            d = pymupdf.open(p)
            txt = "".join(pg.get_text() for pg in d)
            ok = d.page_count > 0 and len(txt) > 200
            note("核验PDF", p, ok, "" if ok else "内容过少")
            if not ok:
                bad += 1
        except Exception as exc:                           # noqa: BLE001
            note("核验PDF", p, False, str(exc))
            bad += 1
    for p in sorted(SUBJECT.rglob("*.docx")):
        if "templates" in p.parts:
            continue           # reference.docx 是样式模板（空壳），不是产物，别当内容不合规
        try:
            with zipfile.ZipFile(p) as z:
                xml = z.read("word/document.xml").decode("utf-8", "ignore")
            text = re.sub(r"<[^>]+>", "", xml)
            ok = len(text) > 400
            note("核验DOCX", p, ok, "" if ok else "内容过少")
            if not ok:
                bad += 1
        except Exception as exc:                           # noqa: BLE001
            note("核验DOCX", p, False, str(exc))
            bad += 1
    return bad


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true", help="全量：课题 + 讲义 + 章程 + 整体版")
    ap.add_argument("--topics", action="store_true", help="11 个课题 + 整体版")
    ap.add_argument("--lectures", action="store_true", help="讲义（PDF+DOCX）")
    ap.add_argument("--charter", action="store_true", help="章程与地图（PDF+DOCX）")
    ap.add_argument("--check", action="store_true", help="只核验已有产物")
    a = ap.parse_args()
    if not any([a.all, a.topics, a.lectures, a.charter, a.check]):
        a.all = True

    if not FONT_DIR.exists() or not (FONT_DIR / "NotoSerifSC-Regular.ttf").exists():
        print(f"✘ 缺少字体目录 {FONT_DIR}，请先运行 环境/pdf/bootstrap.sh")
        return 2

    if a.check:
        bad = verify_existing()
        return dump_rows()

    if a.all and not REF_DOCX.exists():
        print("准备 DOCX 样式模板（正文宋体 / 标题黑体）…")
        build_reference_docx()

    if a.all or a.lectures:
        export_set("大模型实训讲义 · 全书", lecture_files(), SUBJECT / "讲义" / "pdf",
                   "大模型实训讲义-全书", "从零实现大模型：M0–M9 知识主干")
    if a.all or a.charter:
        export_set("章程与地图 · 全书", charter_files(), SUBJECT / "章程与地图" / "pdf",
                   "章程与地图-全书", "本学科的宪法层：学什么 / 跟谁学 / 什么叫学过 / 何时学 / 谁写代码")
    if a.all or a.topics:
        for d in TOPIC_DIRS:
            export_topic(d, want=("pdf", "docx", "tex"))
        export_combined(want=("pdf", "docx", "tex"))

    return dump_rows()


if __name__ == "__main__":
    sys.exit(main())
