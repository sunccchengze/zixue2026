"""Regression tests for course organization; uses only the standard library."""
from pathlib import Path
import tempfile
import unittest

from audit_repository_layout import ROOT, audit, local_target, markdown_links, rows


class LinkParserTests(unittest.TestCase):
    def test_parentheses_and_spaces_in_filenames(self):
        links = list(markdown_links('[报告](报告(模板29-31).docx)\n[教材](教材%20第二版.pdf)'))
        self.assertEqual(links, [('报告', '报告(模板29-31).docx'), ('教材', '教材%20第二版.pdf')])

    def test_fenced_examples_are_not_navigation(self):
        self.assertEqual(list(markdown_links('```md\n[示例](不存在.md)\n```\n[真链接](README.md)')),
                         [('真链接', 'README.md')])

    def test_remote_and_anchor_links_are_excluded(self):
        for url in ['https://example.invalid/a', '#章节', 'mailto:a@example.invalid']:
            self.assertIsNone(local_target(ROOT / 'README.md', url))

    def test_encoded_relative_path(self):
        self.assertEqual(local_target(ROOT / 'README.md', '工具书/Python/a%20b.pdf#page=1'),
                         ROOT / '工具书/Python/a b.pdf')


class LayoutTests(unittest.TestCase):
    def test_preservation_navigation_and_coverage(self):
        errors, *_ = audit()
        self.assertEqual(errors, [])

    def test_every_baseline_source_is_accounted_for(self):
        records = rows()
        self.assertEqual(len(records), 1994)
        self.assertEqual(len({r['原路径'] for r in records}), 1994)

    def test_misfiled_uploads_have_content_based_destinations(self):
        destinations = {r['原路径'].split('/2026秋/', 1)[-1]: r['归档路径'] for r in rows()}
        for source, prefix in [
            ('02_大学化学/第三章奇数题-参考答案.md', '概率论与数理统计/'),
            ('02_大学化学/第1-3讲-课件合集.pdf', '人工智能基础与应用/'),
            ('02_大学化学/第五章习题-答题纸.pdf', '复变函数与积分变换/'),
            ('05_大学物理实验/实验报告_剩余部分_填写内容.md', '大学化学实验/'),
        ]:
            self.assertTrue(destinations[source].startswith(prefix), source)

    def test_duplicate_destinations_have_equal_source_hashes(self):
        hashes = {}
        for row in rows():
            dest = row['归档路径']
            if dest in hashes:
                self.assertEqual(row['原SHA256'], hashes[dest], dest)
            hashes[dest] = row['原SHA256']


if __name__ == '__main__':
    unittest.main()
