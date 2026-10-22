"""Regression coverage for taxonomy, explicit versions and midterm workflows."""
import copy
import csv
from pathlib import Path
import unittest

from audit_repository_layout import navigation_errors
from manage_repository import load, expected_outputs, validate
from repository_support import ROOT, safe_path
from verify_midterm_mocks import verify


class GovernanceTests(unittest.TestCase):
    def setUp(self):
        self.schema, self.registry = load()

    def test_live_registry_is_valid(self):
        self.assertEqual(validate(self.schema, self.registry), [])

    def test_duplicate_role_is_rejected(self):
        registry = copy.deepcopy(self.registry)
        work = next(w for w in registry['works'] if w['current'])
        work['current'].append(copy.deepcopy(work['current'][0]))
        self.assertTrue(any('Multiple current' in e for e in validate(self.schema, registry)))

    def test_missing_current_file_is_rejected(self):
        registry = copy.deepcopy(self.registry)
        work = next(w for w in registry['works'] if w['current'])
        work['current'][0]['path'] = work['package'] + '/不存在的交付.pdf'
        self.assertTrue(any('Missing registered path' in e for e in validate(self.schema, registry)))

    def test_new_task_package_needs_a_version_record(self):
        registry = copy.deepcopy(self.registry)
        registry['works'] = [w for w in registry['works'] if w['id'] != 'chem-ch1']
        self.assertTrue(any('Unregistered task package' in e for e in validate(self.schema, registry)))

    def test_unknown_state_is_rejected(self):
        registry = copy.deepcopy(self.registry)
        registry['works'][0]['state'] = '最新所以自动通过'
        self.assertTrue(any('Unknown state' in e for e in validate(self.schema, registry)))

    def test_history_cannot_silently_become_current(self):
        registry = copy.deepcopy(self.registry)
        registry['works'][0]['current'][0]['path'] = (
            '大学物理/考试复习/期中/知识精讲/历史版本/大学物理期中考试范围详解（第十二~十五次作业）.docx')
        self.assertTrue(any('Current points into history' in e for e in validate(self.schema, registry)))

    def test_paths_cannot_escape_repository(self):
        with self.assertRaises(ValueError):
            safe_path('../outside.md')

    def test_generated_pages_and_index_are_synchronized(self):
        for path, expected in expected_outputs(self.schema, self.registry).items():
            self.assertEqual((ROOT / path).read_text(), expected, path)

    def test_generated_navigation_has_no_missing_local_targets(self):
        for path in expected_outputs(self.schema, self.registry):
            if path.endswith('.md'):
                self.assertEqual(navigation_errors(ROOT / path), [], path)

    def test_plans_have_executable_tasks_but_no_fabricated_results(self):
        for c in ['大学物理', '大学化学', '概率论与数理统计']:
            base = ROOT / c / '考试复习/期中'
            with (base / '复习记录.tsv').open() as f:
                records = list(csv.DictReader(f, delimiter='\t'))
            self.assertEqual(len(records), 14)
            self.assertEqual([int(r['轮次']) for r in records], list(range(1,15)))
            for row in records:
                self.assertIn(row['状态'], ['未开始', '进行中', '已核对', '已闭卷重做'])
                for field in ['课件知识任务','真题或题库任务','AI或复盘任务']:
                    self.assertTrue(row[field].strip())
            for name in ['README.md','课件与知识点.md','真题训练.md','复盘记录.md','AI模拟/卷01/题目.md','AI模拟/卷01/参考答案.md']:
                self.assertEqual(navigation_errors(base/name), [], str(base/name))

    def test_true_papers_are_not_confused_with_mooc_mocks(self):
        text = (ROOT / '概率论与数理统计/考试复习/期中/真题训练.md').read_text()
        self.assertIn('按MOOC模拟训练登记', text)
        self.assertIn('历年期末题，不是本课程期中原卷', text)
        chem = (ROOT / '大学化学/考试复习/期中/README.md').read_text()
        self.assertIn('平衡/酸碱/电化学/反应速率不混入', chem)
        physics = (ROOT / '大学物理/考试复习/期中/课件与知识点.md').read_text()
        self.assertIn('未定位到', physics)

    def test_ai_mock_numeric_and_structure_checks(self):
        errors, count = verify()
        self.assertEqual(errors, [])
        self.assertGreater(count, 50)

    def test_older_change_of_variable_error_is_fixed_in_source(self):
        text = (ROOT / '概率论与数理统计/考试复习/综合题库/2026秋/10-期中冲刺-第1至4章诊断卷与易错清单.md').read_text()
        self.assertIn('f_Y(y)=\\dfrac52 y^{3/2}', text)
        self.assertIn('2026-10-22勘误', text)


if __name__ == '__main__':
    unittest.main()
