#!/usr/bin/env python3
"""Extract downloaded course PDFs, preserving course/chapter/lesson metadata.

Run from any cwd. Dependency: pypdf. Output defaults next to this script.
"""
from pathlib import Path
import argparse
import json
import re

HERE = Path(__file__).resolve().parent


def course_metadata(relative):
    parts = Path(relative).parts
    if len(parts) < 3:
        raise ValueError('Expected [course/]chapter/lesson/file.pdf')
    return {
        'course': '/'.join(parts[:-3]),
        'chapter': parts[-3],
        'lesson': parts[-2],
        'name': parts[-1],
    }


def extract_corpus(source, output):
    from pypdf import PdfReader
    corpus = []
    for pdf in sorted(source.rglob('*.pdf')):
        relative = pdf.relative_to(source)
        reader = PdfReader(pdf)
        pages = []
        for i, page in enumerate(reader.pages, 1):
            text = re.sub(r'[ \t]+', ' ', page.extract_text() or '')
            text = re.sub(r'\n{3,}', '\n\n', text).strip()
            if text:
                pages.append({'page': i, 'text': text})
        corpus.append({
            'file': relative.as_posix(), **course_metadata(relative),
            'n_pages': len(reader.pages), 'pages': pages,
            'text': '\n'.join(f"[p{p['page']}] {p['text']}" for p in pages),
        })
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('w', encoding='utf-8') as stream:
        json.dump(corpus, stream, ensure_ascii=False, indent=1)
        stream.write('\n')
    return corpus


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=HERE / 'downloads')
    parser.add_argument('--output', type=Path, default=HERE / 'corpus.json')
    args = parser.parse_args()
    records = extract_corpus(args.source, args.output)
    print(f'{len(records)} documents; {sum(r["n_pages"] for r in records)} pages -> {args.output}')
