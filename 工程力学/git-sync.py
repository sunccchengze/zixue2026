#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
git-sync.py — 工程力学 session 一键同步（提交 + 推送 + 校验）
用法：  python3 工程力学/git-sync.py "提交信息"

针对本沙箱的三个环境怪癖（每回合开始可能触发）做防御：
  ① 本地 .git refs 被重置回基点（remote-tracking ref 被清空）
  ② 历史对象丢失（旧提交查不到）
  ③ 工作区被恢复成旧快照（上轮新增/修改的文件可能暂时消失或回退）

内置防御（顺序执行，任一失败即中止并保留现场）：
  1. 始终显式 fetch 本 session 分支（不依赖残留 ref）
  2. reset --soft 接到远端 tip（不碰工作区内容）
  3. 远端树里有、磁盘上没有的文件 → 自动从远端恢复（快照丢的文件）
  4. 暂存 diff 若含"删除已跟踪文件" → 立即中止（防把旧快照的误删提交上去）
  5. 推送后校验 远端 tip == 本地 HEAD，并打印远端树文件数

纪律：每个归档节点（课题验收/交接更新/资料入库）只跑这一条命令；
      若脚本以 SYNC-ERROR 中止，说明状态异常，停下来排查，不要绕过它手工 push。
"""
import subprocess, sys, os

BR = "arena/01a02459-zixue2026"
MSG = sys.argv[1] if len(sys.argv) > 1 else "工程力学：进度更新"

def run(*a, check=True, data=False):
    r = subprocess.run(a, capture_output=True, text=not data)
    if check and r.returncode != 0:
        err = (r.stderr if data is False else r.stderr) or ''
        if isinstance(err, bytes):
            err = err.decode('utf-8', 'replace')
        print(f"SYNC-ERROR: {' '.join(str(x) for x in a[:3])} 失败: {err[:400]}")
        sys.exit(1)
    return r

def tree(ref):
    out = run('git', 'ls-tree', '-r', '--name-only', '-z', ref, data=True).stdout.decode('utf-8')
    return set(p for p in out.split('\0') if p)

root = run('git', 'rev-parse', '--show-toplevel').stdout.strip()
os.chdir(root)

if run('git', 'rev-parse', '--abbrev-ref', 'HEAD').stdout.strip() != BR:
    print(f"SYNC-ERROR: 当前不在 {BR} 分支"); sys.exit(1)

# 1) 显式 fetch（refspec 可能被环境清掉）
run('git', 'fetch', '-q', 'origin', f'refs/heads/{BR}:refs/remotes/origin/{BR}')
REMOTE = f'origin/{BR}'

# 2) 接到远端 tip（保留工作区与 index）
run('git', 'reset', '-q', '--soft', REMOTE)

# 3) 自动恢复快照丢失的文件（远端树有、磁盘没有）
remote_tree = tree(REMOTE)
lost = sorted(p for p in remote_tree if not os.path.exists(p))
if lost:
    print(f'[restore] 工作区快照丢失 {len(lost)} 个文件，已从远端恢复:')
    for p in lost:
        print('  +', p)
    run('git', 'checkout', '-q', REMOTE, '--', *lost)

# 4) 暂存全部
run('git', 'add', '-A')

# 5) 误删拦截：暂存区里出现"删除已跟踪文件"即中止
st = run('git', 'status', '--porcelain', '-z').stdout
deleted = [e[3:] for e in st.split('\0') if e.startswith('D ')]
if deleted:
    print('SYNC-ERROR: 暂存区含已跟踪文件的删除，中止（疑似旧快照误删）:')
    for d in deleted[:20]:
        print('  -', d)
    run('git', 'reset', '-q')
    sys.exit(1)

# 6) 有变更才提交推送
if run('git', 'diff', '--cached', '--quiet', check=False).returncode == 0:
    print('[ok] 无变更，远端已是最新')
else:
    run('git', 'commit', '-q', '-m', MSG)
    run('git', 'push', '-q', 'origin', BR)
    print('[ok] 已提交并推送')

# 7) 校验
tip = run('git', 'ls-remote', 'origin', f'refs/heads/{BR}').stdout.split()[0]
head = run('git', 'rev-parse', 'HEAD').stdout.strip()
n = len(tree('HEAD'))
print(f'[verify] 远端tip==本地HEAD: {tip == head} ({tip[:8]}) | 远端树文件数: {n}')
if tip != head:
    print('SYNC-ERROR: 推送后远端 tip != 本地 HEAD！')
    sys.exit(1)
print('[done] 同步完成')
