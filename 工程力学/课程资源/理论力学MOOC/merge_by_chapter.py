#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 downloads/ 下的讲义按「一章一个 PDF」合并，并写入嵌套书签（章 → 课时 → 讲义）。

用法:
    python3 merge_by_chapter.py              # 输出到 按章节合并/
    python3 merge_by_chapter.py --out DIR    # 指定输出目录
"""
import os, re, glob, argparse
from pypdf import PdfReader, PdfWriter

HERE = os.path.dirname(os.path.abspath(__file__))
SRC  = os.path.join(HERE, "downloads")
DEFAULT_OUT = os.path.join(HERE, "按章节合并")

# Windows / GitHub 不友好的字符 → 替换
BAD = {'：': ' ', ':': ' ', '/': '-', '\\': '-', '*': '-',
       '?': '', '"': '', '<': '', '>': '', '|': '-'}


def safe(name):
    for k, v in BAD.items():
        name = name.replace(k, v)
    return re.sub(r'\s+', ' ', name).strip()


def strip_num(name):
    """去掉目录名前面的 '01 ' 序号，用于书签显示"""
    return re.sub(r'^\d+\s*', '', name).strip()


def has_pdf_tree(d):
    """目录 d 的子目录里是否直接含 PDF（即 d 是「章」这一层）"""
    for sub in os.listdir(d):
        p = os.path.join(d, sub)
        if os.path.isdir(p) and glob.glob(os.path.join(p, "*.pdf")):
            return True
    return False


def find_chapter_dirs(src):
    """自动下钻到「章」这一层（downloads/ 下可能还套了一层课程名目录）"""
    level = src
    for _ in range(3):
        kids = sorted(d for d in os.listdir(level)
                      if os.path.isdir(os.path.join(level, d)))
        if not kids:
            break
        if any(has_pdf_tree(os.path.join(level, k)) for k in kids):
            return level, kids
        if len(kids) == 1:                      # 只有一层包装目录 → 下钻
            level = os.path.join(level, kids[0])
        else:
            break
    return level, sorted(d for d in os.listdir(level)
                         if os.path.isdir(os.path.join(level, d)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=DEFAULT_OUT)
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    CH_ROOT, chapters = find_chapter_dirs(SRC)
    print(f"章节根目录: {os.path.relpath(CH_ROOT, HERE)}")
    print(f"识别到 {len(chapters)} 章: {chapters}\n")
    report = []

    for ch in chapters:
        ch_dir = os.path.join(CH_ROOT, ch)
        lessons = sorted(d for d in os.listdir(ch_dir)
                         if os.path.isdir(os.path.join(ch_dir, d)))

        writer = PdfWriter()
        ch_title = safe(ch)
        # 章级书签（指向第 0 页）
        root = writer.add_outline_item(ch_title, 0)
        files_used, page_i = [], 0

        for les in lessons:
            les_dir = os.path.join(ch_dir, les)
            pdfs = sorted(glob.glob(os.path.join(les_dir, "*.pdf")))
            if not pdfs:
                continue
            # 课时级书签（指向该课时第一页）
            les_bookmark = writer.add_outline_item(
                f"{strip_num(safe(les))}", page_i, parent=root)

            for pdf in pdfs:
                reader = PdfReader(pdf)
                n = len(reader.pages)
                for p in reader.pages:
                    writer.add_page(p)
                # 讲义级书签（指向该份讲义第一页）
                fname = os.path.splitext(os.path.basename(pdf))[0]
                writer.add_outline_item(
                    f"{fname}  ({n}页)", page_i, parent=les_bookmark)
                files_used.append((os.path.relpath(pdf, SRC), n))
                page_i += n

        total = len(writer.pages)
        writer.add_metadata({
            "/Title": f"理论力学 · {ch_title}",
            "/Author": "西安交通大学 吴莹 教授",
            "/Subject": "中国大学MOOC 理论力学 课件合订本",
            "/Creator": "merge_by_chapter.py",
        })
        out_path = os.path.join(args.out, f"{safe(ch)}.pdf")
        with open(out_path, "wb") as f:
            writer.write(f)

        size_mb = os.path.getsize(out_path) / 1024 / 1024
        report.append((ch, len(lessons), len(files_used), total, size_mb, out_path))
        print(f"✅ {safe(ch)}.pdf")
        print(f"   {len(lessons)} 个课时 · {len(files_used)} 份讲义 · "
              f"{total} 页 · {size_mb:.2f} MB")

    # 汇总
    tp = sum(r[3] for r in report)
    ts = sum(r[4] for r in report)
    tn = sum(r[2] for r in report)
    print(f"\n合计 {len(report)} 章 / {tn} 份讲义 / {tp} 页 / {ts:.2f} MB")
    print("输出目录:", args.out)

    # 对照表
    idx = os.path.join(args.out, "_合并对照表.csv")
    import csv
    with open(idx, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["合并后文件", "章节", "课时", "原讲义文件名", "页数"])
        for ch in chapters:
            ch_dir = os.path.join(CH_ROOT, ch)
            for les in sorted(os.listdir(ch_dir)):
                les_dir = os.path.join(ch_dir, les)
                if not os.path.isdir(les_dir):
                    continue
                for pdf in sorted(glob.glob(os.path.join(les_dir, "*.pdf"))):
                    w.writerow([f"{safe(ch)}.pdf", ch, les,
                                os.path.basename(pdf), len(PdfReader(pdf).pages)])
    print("对照表:", idx)


if __name__ == "__main__":
    main()
