"""Shared, standard-library repository paths and historical relocation helpers."""
import csv
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
MIGRATION = ROOT / '维护记录/2026-10-22-结构与期中/迁移清单.tsv'
CURRENT_INDEX = ROOT / '维护记录/当前文件索引.tsv'


def relocation_map():
    with MIGRATION.open(encoding='utf-8') as f:
        return {r['原路径']: r['归档路径'] for r in csv.DictReader(f, delimiter='\t')}


def relocate(path):
    """Resolve the second cleanup after the first dated manifest, once only."""
    return relocation_map().get(str(path), str(path))


def live_files():
    paths = subprocess.check_output(
        ['git', 'ls-files', '-c', '-o', '--exclude-standard', '-z'], cwd=ROOT
    ).decode().split('\0')
    return sorted({p for p in paths if p and (ROOT / p).is_file()})


def safe_path(value):
    path = (ROOT / value).resolve()
    if not path.is_relative_to(ROOT) or Path(value).is_absolute():
        raise ValueError('Path must be repository-relative: ' + value)
    return path
