#!/usr/bin/env python3
"""Offline regression tests for the 2026-10 repository cleanup.

Run: python -m unittest discover -s scripts -p test_repository_maintenance.py -v
Dependencies: requests (mechanics downloader import only). No live login/network.
"""
import contextlib
import csv
import importlib.util
import io
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts/icourse'))
from archive_safety import archive_url, archive_text, safe_record


class ArchiveSafetyTests(unittest.TestCase):
    def test_signed_urls_remove_case_insensitive_credentials(self):
        url = ('https://example.invalid/a.pdf?download=lecture.pdf&Signature=dummy'
               '&NOSAccessKeyId=example&CSRFKey=test&Expires=123')
        result = archive_url(url)
        self.assertEqual(result, 'https://example.invalid/a.pdf?download=lecture.pdf&Expires=123')

    def test_normal_url_unchanged(self):
        url = 'https://example.invalid/learn?tid=123&name=a%20b'
        self.assertEqual(archive_url(url), url)

    def test_nested_logs_drop_opaque_bodies(self):
        sample = [{'url': 'https://example.invalid/?token=example',
                   'body': 'secret not to persist', 'req_body': 'private',
                   'resp_text': 'private', 'headers': {'Cookie': 'private'},
                   'status': 200}]
        self.assertEqual(safe_record(sample), [{'url': 'https://example.invalid/', 'status': 200}])

    def test_text_and_idempotence(self):
        text = 'Source https://example.invalid/a?signature=example&x=1 end'
        cleaned = archive_text(text)
        self.assertEqual(cleaned, 'Source https://example.invalid/a?x=1 end')
        self.assertEqual(archive_text(cleaned), cleaned)


class CorpusMetadataTests(unittest.TestCase):
    def test_actual_directory_layout(self):
        spec = importlib.util.spec_from_file_location('extract_for_test',
            ROOT / '工程力学/课程资源/理论力学MOOC/extract_text.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.assertEqual(module.course_metadata('理论力学/01 绪论/01 绪论/绪论.pdf'),
                         {'course': '理论力学', 'chapter': '01 绪论',
                          'lesson': '01 绪论', 'name': '绪论.pdf'})

    def test_userinfo_without_signature_is_removed(self):
        self.assertEqual(archive_url('https://test:example@example.invalid/a'),
                         'https://example.invalid/a')


class MechanicsDownloadTests(unittest.TestCase):
    """Exercise existing/overwrite/failure paths entirely with fake responses."""
    def setUp(self):
        path = ROOT / '工程力学/课程资源/理论力学MOOC/dl.py'
        spec = importlib.util.spec_from_file_location('mechanics_dl_for_test', path)
        self.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.module)
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name)
        self.module.HERE = str(self.home)
        self.module.OUT = str(self.home / 'downloads')
        self.destination = self.home / 'downloads/理论力学/01 Chapter/01 Lesson/lecture.pdf'
        self.destination.parent.mkdir(parents=True)
        self.original = b'%PDF-1.4\n' + b'original' * 200
        self.destination.write_bytes(self.original)

    def run_downloader(self, payload, *args, fail=False):
        class Response:
            def __enter__(self): return self
            def __exit__(self, *exc): return False
            def raise_for_status(self): pass
            def iter_content(self, _):
                yield payload
                if fail:
                    raise OSError('simulated transport interruption')
        class Session:
            calls = 0
            def get(self, *args, **kwargs):
                self.calls += 1
                return Response()
        class Client:
            def __init__(self, _): self.s = session
            def rpc(self, *args): return {'result': {'nickName': 'offline-test'}}
        session = Session()
        tree = {'chapters': [{'name': 'Chapter', 'lessons': [{'name': 'Lesson', 'units': [
            {'id': 1, 'name': 'lecture', 'contentType': 3}]}]}]}
        with patch.object(self.module, 'load_cookies', return_value={'NTESSTUDYSI': 'offline-test'}), \
             patch.object(self.module, 'Client', Client), \
             patch.object(self.module, 'get_tree', return_value=tree), \
             patch.object(self.module, 'pdf_link', return_value=(
                 'https://example.invalid/lecture.pdf?Signature=example', 'lecture.pdf')), \
             patch.object(sys, 'argv', ['dl.py', *args]), contextlib.redirect_stdout(io.StringIO()):
            self.module.main()
        return session

    def test_distinct_units_with_same_name_get_stable_paths(self):
        dest = str(self.destination)
        self.assertEqual(self.module.unique_path(dest, set()), dest)
        duplicate = str(self.destination.with_name('lecture (2).pdf'))
        self.assertEqual(self.module.unique_path(dest, {dest}), duplicate)

    def test_existing_file_is_skipped_without_numbered_duplicate(self):
        session = self.run_downloader(b'not used')
        self.assertEqual(session.calls, 0)
        self.assertEqual(self.destination.read_bytes(), self.original)
        self.assertFalse(self.destination.with_name('lecture (2).pdf').exists())

    def test_successful_overwrite_is_atomic_and_manifest_sanitized(self):
        data = b'%PDF-1.4\nreplacement'
        self.run_downloader(data, '--overwrite')
        self.assertEqual(self.destination.read_bytes(), data)
        manifest = (self.home / 'manifest.csv').read_text(encoding='utf-8-sig')
        self.assertNotIn('Signature=', manifest)
        self.assertFalse(Path(str(self.destination) + '.part').exists())

    def test_invalid_download_does_not_destroy_existing_original(self):
        self.run_downloader(b'<html>not a pdf</html>', '--overwrite')
        self.assertEqual(self.destination.read_bytes(), self.original)
        self.assertFalse(Path(str(self.destination) + '.part').exists())

    def test_interrupted_transfer_preserves_original(self):
        self.run_downloader(b'%PDF-partial', '--overwrite', fail=True)
        self.assertEqual(self.destination.read_bytes(), self.original)
        self.assertFalse(Path(str(self.destination) + '.part').exists())


class MaintenanceLinksTests(unittest.TestCase):
    def test_memory_navigation(self):
        for name in ['HANDOFF.md', 'PROGRESS.md']:
            for subject,link in [('大学化学','../../大化大作业/README.md'),
                                 ('工程力学','../课程资源/README.md')]:
                path = ROOT / subject / 'memory' / name
                self.assertIn('(' + link + ')', path.read_text())
                self.assertTrue((path.parent / link).is_file())

    def test_uploaded_binaries_still_match_recorded_source_hashes(self):
        import hashlib
        path = ROOT / '维护记录/2026-10-05/逐文件清单.tsv'
        with path.open() as f:
            rows = list(csv.DictReader(f, delimiter='\t'))
        checked = 0
        for row in rows:
            file = ROOT / row['归档路径']
            if file.suffix in ('.pdf', '.docx', '.pptx', '.png', '.mp4') and row['处置'] == '原字节保留':
                self.assertEqual(hashlib.sha256(file.read_bytes()).hexdigest(), row['原SHA256'], str(file))
                checked += 1
        self.assertEqual(checked, 163)


if __name__ == '__main__':
    unittest.main()
