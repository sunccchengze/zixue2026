#!/usr/bin/env python3
"""Generate/check course navigation, current selections and a live asset index.

python scripts/manage_repository.py refresh  # writes derived navigation/index
python scripts/manage_repository.py check    # read-only; exits nonzero on drift
Source of truth: 仓库目录规范.json + 课程资产登记.json. No implicit version guessing.
"""
import argparse
import csv
import io
import json
from pathlib import Path
import sys

from repository_support import ROOT, CURRENT_INDEX, live_files, safe_path


def load():
    return (json.loads((ROOT / '仓库目录规范.json').read_text()),
            json.loads((ROOT / '课程资产登记.json').read_text()))


def relative_link(document, target):
    import os
    return os.path.relpath(ROOT / target, (ROOT / document).parent).replace(' ', '%20')


def render_course(course, works, schema):
    name = course['path']
    page = name + '/当前入口.md'
    lines = [f'# {name} · 当前入口', '',
             '> 自动生成：只编辑根目录《课程资产登记.json》；运行 `python scripts/manage_repository.py refresh` 更新。',
             '> “在用”指本仓学习/编辑入口，不等于教师认可或可以直接提交。未确认的状态明确显示。', '']
    lines += ['## 按用途找文件', '', '| 用途 | 入口 |', '|---|---|']
    for p in sorted((ROOT / name).iterdir()):
        if p.is_dir() and p.name in schema['course_directories']:
            lines.append(f'| {schema["course_directories"][p.name]} | [{p.name}]({p.name}/) |')
    lines += ['', '## 当前工作包与版本', '', '| 工作包 | 状态 | 唯一入口 | 依据/边界 |', '|---|---|---|---|']
    for work in works:
        if work['course'] != name:
            continue
        link = relative_link(page, work['entry'])
        lines.append(f'| {work["title"]} | {work["state"]} | [打开]({link}) | {work["reason"]} |')
    if not any(w['course'] == name for w in works):
        lines.append('| 原有课程材料 | 在用-参考 | [课程资料](README.md) | 尚无独立交付包；不编造提交版本 |')
    lines += ['', '## 进度与历史', '',
              '- 本页只决定入口，不把资料生成、阅读计划或文件搬迁计为已掌握。']
    if (ROOT / name / 'memory/HANDOFF.md').exists():
        lines.append('- [会话交接](memory/HANDOFF.md) · [学习进度](memory/PROGRESS.md)。')
    history = ROOT / name / '章程与地图/历史导航-2026-10-22.md'
    if history.exists():
        lines.append('- [旧导航留档](章程与地图/历史导航-2026-10-22.md)仅作历史，不作为当前版本入口。')
    current = '\n'.join(lines) + '\n'
    readme = (f'# {name}\n\n> 本页由目录规范和资产登记生成，不手工维护另一份目录树。\n\n'
              f'**先看[当前入口](当前入口.md)**：课程用途、工作包、版本状态。\n\n'
              f'{course["description"]}\n\n')
    if course.get('midterm'):
        readme += '**近期重点：[期中复习计划](考试复习/期中/README.md)**（真题、PPT/课件、AI 模拟与复盘）。\n\n'
    readme += '新会话先读仓库 `AGENTS.md`，再按当前入口读取本学科交接；不要从旧日志猜最新提交版本。\n'
    return {page: current, name + '/README.md': readme}


def render_package(work):
    page = work['package'] + '/当前版本.md'
    lines = [f'# {work["title"]} · 当前版本', '',
             '> 自动生成：版本选择以根目录《课程资产登记.json》为准。', '',
             f'**状态：{work["state"]}**', '', work['reason'], '',
             '**提交状态：未确认可直接提交。** 学习参考、完成生成、通过结构检查与最终交付不是同一状态。', '',
             '## 当前选用', '', '| 角色 | 文件 |', '|---|---|']
    for item in work['current']:
        lines.append(f'| {item["role"]} | [{Path(item["path"]).name}]({relative_link(page, item["path"])}) |')
    if not work['current']:
        lines.append('| 无 | 尚无可选用的交付文件，不猜测版本 |')
    for key, title in [('sources', '原始资料/证据'), ('tools', '源码与复现'), ('history', '历史或候选版本')]:
        lines += ['', '## ' + title, '']
        for path in work.get(key, []):
            lines.append(f'- [{path.split("/")[-1]}]({relative_link(page, path)})')
        if not work.get(key):
            lines.append('- 暂未登记；不表示不存在，新增时须核对登记。')
    if work.get('reproduce'):
        lines += ['', '复现命令（仓库根运行，先安装对应依赖；生成结果仍须验收）：', '', '```bash',
                  *work['reproduce'], '```']
    return page, '\n'.join(lines) + '\n'


def asset_kind(path, explicit):
    if path in explicit:
        return explicit[path]
    for prefix in sorted(explicit, key=len, reverse=True):
        if path.startswith(prefix.rstrip('/') + '/'):
            return explicit[prefix]
    p = Path(path)
    if '/历史版本/' in path or '/上传版本/' in path or '/历史综合模拟/' in path or '/历史诊断/' in path:
        return '历史/候选，不作默认提交'
    if '/资料原件/' in path or '/上传原包/' in path or '/数据原包/' in path:
        return '原始资料（保留原字节）'
    if '/资料文本/' in path:
        return '提取文本（原件为准）'
    if p.suffix == '.py' or '/源文件/' in path:
        return '工具/编辑源码'
    if p.suffix in {'.png', '.jpg', '.jpeg', '.svg', '.mp4', '.csv'}:
        return '素材/数据（非自动删除缓存）'
    if p.suffix in {'.pdf', '.docx', '.pptx', '.xlsx', '.xls', '.zip', '.rar', '.bin', '.lnk'}:
        return '归档附件（未登记可复现，禁止当缓存删除）'
    return '知识/记忆/导航/配置'


def expected_outputs(schema, registry):
    outputs = {}
    for course in registry['courses']:
        outputs.update(render_course(course, registry['works'], schema))
    for work in registry['works']:
        page, text = render_package(work)
        outputs[page] = text
    explicit = {}
    for work in registry['works']:
        for key, kind in [('history', '历史/候选（登记，不作默认提交）'), ('sources', '原始资料/证据（登记）'), ('tools', '工具/编辑源码（登记）')]:
            for path in work.get(key, []):
                explicit.setdefault(path, kind)
    for work in registry['works']:
        for item in work['current']:
            explicit[item['path']] = '当前选用：' + item['role'] + '；' + work['state']
    # Include not-yet-written generated pages and the index itself.
    paths = sorted(set(live_files()) | set(outputs) | {CURRENT_INDEX.relative_to(ROOT).as_posix()})
    stream = io.StringIO()
    writer = csv.writer(stream, delimiter='\t', lineterminator='\n')
    writer.writerow(['课程或分类', '用途目录', '资产层', '路径'])
    for path in paths:
        parts = Path(path).parts
        writer.writerow([parts[0] if len(parts)>1 else '仓库级', parts[1] if len(parts)>2 else '入口/配置',
                         asset_kind(path, explicit), path])
    outputs[CURRENT_INDEX.relative_to(ROOT).as_posix()] = stream.getvalue()
    return outputs


def validate(schema, registry):
    errors = []
    ids = set()
    package_paths = set()
    course_names = {c['path'] for c in registry['courses']}
    live = live_files()
    packages = {w['package'] for w in registry['works']}
    for course in registry['courses']:
        home = ROOT / course['path']
        for p in home.iterdir():
            rel = p.relative_to(ROOT).as_posix()
            if p.is_dir() and any(x.startswith(rel+'/') for x in live) and p.name not in schema['course_directories']:
                errors.append('Unregistered course category: ' + rel)
            if p.is_file() and p.name not in ['README.md','当前入口.md','_开局指令-给新会话Agent.md','.gitignore']:
                errors.append('Loose course-root file: ' + rel)
        for category in ['课程作业', '课程大作业']:
            parent = home / category
            if not parent.exists():
                continue
            for package in parent.iterdir():
                rel = package.relative_to(ROOT).as_posix()
                if package.is_dir() and any(x.startswith(rel+'/') for x in live) and rel not in packages:
                    errors.append('Unregistered task package: ' + rel)
    for work in registry['works']:
        if work['id'] in ids: errors.append('Duplicate work id: ' + work['id'])
        ids.add(work['id'])
        if work['package'] in package_paths: errors.append('Duplicate package: ' + work['package'])
        package_paths.add(work['package'])
        if work['course'] not in course_names: errors.append('Unknown course: ' + work['course'])
        if work['state'] not in schema['work_states']: errors.append('Unknown state: ' + work['id'])
        if not work['reason'].strip(): errors.append('Missing version evidence: ' + work['id'])
        roles = set()
        for item in work['current']:
            if item['role'] in roles: errors.append('Multiple current files for one role: ' + work['id'])
            roles.add(item['role'])
        candidates = [work['package'], work['entry']] + [x['path'] for x in work['current']]
        candidates += sum([work.get(k, []) for k in ['sources', 'tools', 'history']], [])
        for value in candidates:
            try:
                path = safe_path(value)
                if not path.exists(): errors.append('Missing registered path: ' + value)
            except ValueError as error:
                errors.append(str(error))
        for item in work['current']:
            if '/历史版本/' in item['path'] and work['state'] != '历史留档':
                errors.append('Current points into history: ' + work['id'])
    # No remaining course-specific generators in the common tool directory.
    for p in (ROOT / 'scripts').glob('*.py'):
        if any(word in p.name for word in ['mechanics_homework', 'physics_midterm', 'B305', 'patch_zero']):
            errors.append('Course-specific tool returned to scripts/: ' + p.name)
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['refresh', 'check'])
    args = parser.parse_args()
    schema, registry = load()
    errors = validate(schema, registry)
    if errors:
        print('\n'.join('FAIL: '+e for e in errors))
        return 1
    outputs = expected_outputs(schema, registry)
    for path, text in outputs.items():
        p = ROOT / path
        if args.command == 'refresh':
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(text)
        elif not p.is_file() or p.read_text() != text:
            errors.append('Generated navigation/index drift: ' + path)
    print('\n'.join('FAIL: '+e for e in errors) if errors else
          f'PASS: {len(registry["courses"])} courses; {len(registry["works"])} explicit work selections; {len(outputs)} derived files')
    return bool(errors)


if __name__ == '__main__':
    sys.exit(main())
