#!/usr/bin/env python3
"""Compare every merged courseware page with its original source page.

Read-only; no network. Dependency: pymupdf. Raster at 36 dpi supplements exact
text/page-size checks; this is a preservation check, not semantic proofreading.
"""
from pathlib import Path
import hashlib
import json
import sys
import pymupdf

ROOT = Path(__file__).resolve().parents[1]
BUNDLES = [
    ('复变函数', ROOT / '复变函数与积分变换/资料原件/复变函数_课件_前五章', None),
    ('数理方程', ROOT / '数理方程/资料原件/数学物理方程_课程课件', None),
    ('理论力学', ROOT / '工程力学/课程资源/理论力学MOOC', 'downloads/理论力学'),
]


def page_signature(page):
    pix = page.get_pixmap(dpi=36, alpha=False)
    return (tuple(page.rect), page.get_text(), pix.width, pix.height,
            hashlib.sha256(pix.samples).hexdigest())


def audit():
    results = []
    for label, bundle, source_subdir in BUNDLES:
        source_root = bundle / source_subdir if source_subdir else bundle
        merged_root = bundle / ('按章节合并' if source_subdir else '合并版')
        merged_paths = sorted(merged_root.glob('*.pdf'))
        chapters = sorted(p for p in source_root.iterdir()
                          if p.is_dir() and p.name[:2].isdigit())
        if len(merged_paths) != len(chapters):
            raise AssertionError(f'{label}: chapter/merged file count mismatch')
        for chapter in chapters:
            candidates = [p for p in merged_paths if p.name[:2] == chapter.name[:2]]
            if len(candidates) != 1:
                raise AssertionError(f'{label}/{chapter.name}: no unique merged PDF')
            originals = sorted(chapter.rglob('*.pdf'))
            if not originals:
                raise AssertionError(f'{chapter}: empty source chapter')
            with pymupdf.open(candidates[0]) as merged:
                offset = 0
                for original in originals:
                    with pymupdf.open(original) as doc:
                        for index, page in enumerate(doc):
                            if offset >= len(merged) or page_signature(page) != page_signature(merged[offset]):
                                raise AssertionError(f'{label}: {original.name} page {index+1} != merged page {offset+1}')
                            offset += 1
                if offset != len(merged):
                    raise AssertionError(f'{label}: extra merged pages')
            results.append({'course': label, 'chapter': chapter.name,
                            'source_pdfs': len(originals), 'pages': offset,
                            'check': 'page size + exact text + 36dpi pixel SHA256'})
    return results


if __name__ == '__main__':
    try:
        rows = audit()
        print(json.dumps(rows, ensure_ascii=False, indent=2))
        print(f'PASS: {len(rows)} chapters; {sum(x["pages"] for x in rows)} original/merged page pairs')
    except (AssertionError, OSError, ValueError) as exc:
        print(f'FAIL: {exc}', file=sys.stderr)
        sys.exit(1)
