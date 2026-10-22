#!/usr/bin/env python3
"""Read-only, standard-library audit of the 2026-10-22 course organization.

Run from any cwd: python /path/to/scripts/audit_repository_layout.py
The dated source SHA256 is immutable; final text SHA256 records maintenance edits.
This checks preservation and navigation, not academic correctness.
"""
import csv
import hashlib
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote, urlsplit
from repository_support import relocate, CURRENT_INDEX, MIGRATION, relocation_map

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / '维护记录/2026-10-22'
BINARY = {'.pdf', '.docx', '.pptx', '.xlsx', '.xls', '.rar', '.zip', '.png', '.jpg',
          '.jpeg', '.gif', '.mp4', '.lnk', '.bin'}
RETIRED = ['probability', '大物实验预习', '大化大作业', '英语大作业', '未分类']


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def rows():
    with (RECORD / '逐文件清单.tsv').open(encoding='utf-8') as f:
        return list(csv.DictReader(f, delimiter='\t'))


def markdown_links(text):
    """Yield inline link targets, respecting nested parentheses and escaped chars.

    Fenced code examples aren't navigation. Reference-style links and anchors are
    outside this small audit's scope; don't pretend to be a complete MD parser.
    """
    text = re.sub(r'^(`{3,}|~{3,}).*?^\1[^\n]*$', '', text, flags=re.M | re.S)
    for match in re.finditer(r'!?\[([^\]\n]*)\]\(', text):
        start = match.end()
        depth = 1
        end = start
        while end < len(text) and depth:
            ch = text[end]
            if ch == '\\':
                end += 2
                continue
            if ch == '\n':
                break
            if ch == '(':
                depth += 1
            elif ch == ')':
                depth -= 1
            if depth:
                end += 1
        if depth == 0:
            target = text[start:end].strip()
            if target.startswith('<') and '>' in target:
                target = target[1:target.index('>')]
            else:
                target = re.split(r'\s+[\'\"]', target, maxsplit=1)[0]
            yield match.group(1), target


def local_target(document, target):
    if not target or target.startswith(('#', '//')) or urlsplit(target).scheme:
        return None
    path = unquote(target.partition('#')[0].partition('?')[0])
    if not path or '\x00' in path:
        return None
    result = (document.parent / path).resolve()
    if not result.is_relative_to(ROOT):
        return None
    return result


def navigation_errors(document):
    errors = []
    for label, target in markdown_links(document.read_text(encoding='utf-8')):
        path = local_target(document, target)
        if path is not None and not path.exists():
            errors.append((label, target))
    return errors


def audit():
    errors = []
    records = rows()
    hashes = {}
    redirects = relocation_map()
    for row in records:
        path = ROOT / redirects.get(row['归档路径'], row['归档路径'])
        if not path.is_file():
            errors.append('Missing: ' + row['归档路径'])
            continue
        if path not in hashes:
            hashes[path] = digest(path)
        actual = hashes[path]
        if path.suffix.lower() in BINARY and actual != row['原SHA256']:
            errors.append('Original bytes changed: ' + row['归档路径'])
        # Historical text hashes are checkpoint evidence, not locks on living notes.
        if path.suffix.lower() in BINARY and actual != row['归档SHA256']:
            errors.append('Recorded archive hash differs: ' + row['归档路径'])
    source_destinations = len(hashes)
    # The second cleanup also contains files added after the first baseline.
    # Check their original binary bytes without freezing living text documents.
    with MIGRATION.open(encoding='utf-8') as f:
        latest = list(csv.DictReader(f, delimiter='\t'))
    for row in latest:
        path = ROOT / row['归档路径']
        if not path.is_file():
            errors.append('Missing latest baseline source: ' + row['归档路径'])
        elif path.suffix.lower() in BINARY:
            if path not in hashes:
                hashes[path] = digest(path)
            if hashes[path] != row['原SHA256']:
                errors.append('Latest original binary changed: ' + row['归档路径'])
    for retired in RETIRED:
        if (ROOT / retired).exists():
            errors.append('Retired directory returned: ' + retired)
    if any(ROOT.glob('（20261022*')):
        errors.append('Temporary upload directory still exists')
    # All newly supplied navigation pages must be free of local broken links.
    with (RECORD / '导航验收范围.txt').open(encoding='utf-8') as f:
        navigation = [line.strip() for line in f if line.strip()]
    for entry in navigation:
        document = ROOT / redirects.get(entry, entry)
        if not document.is_file():
            errors.append('Missing navigation: ' + entry)
            continue
        for _, target in navigation_errors(document):
            errors.append('Broken navigation: ' + entry + ' -> ' + target)
    # Every live file (tracked or intended for addition) must be indexed. Ignored
    # venv/build/caches are deliberately excluded by git, not by a custom walker.
    live = set(subprocess.check_output(
        ['git', 'ls-files', '-c', '-o', '--exclude-standard', '-z'], cwd=ROOT
    ).decode().split('\0'))
    live = {p for p in live if p and (ROOT / p).is_file()}
    with CURRENT_INDEX.open(encoding='utf-8') as f:
        indexed = {r['路径'] for r in csv.DictReader(f, delimiter='\t')}
    if live != indexed:
        errors.append(f'Index coverage differs: missing={sorted(live-indexed)}, stale={sorted(indexed-live)}')
    return errors, len(records), source_destinations, len(navigation), len(live)


def main():
    errors, sources, destinations, navigation, live = audit()
    for error in errors:
        print('FAIL:', error)
    if errors:
        return 1
    print(f'PASS: {sources} source records -> {destinations} preserved destinations; '
          f'{navigation} navigation pages; {live} indexed files.')
    print('Scope: byte preservation, recorded hashes, current navigation and index coverage; '
          'not academic verification. See dated report for pre-existing issues.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
