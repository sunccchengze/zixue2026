from pathlib import Path
REPO = Path(__file__).resolve().parents[2]
import json, os, re, glob, unicodedata

def safe(name, maxlen=80):
    name = unicodedata.normalize('NFKC', name or 'untitled')
    name = re.sub(r'[\\/:*?"<>|\r\n\t]+', '_', name).strip(' ._')
    return name[:maxlen] or 'untitled'

def build_plan(outline_path, root):
    data = json.load(open(outline_path, encoding='utf-8'))
    renames = []  # (old_path, new_path)
    for ch_i, ch in enumerate(data['result']['chapters'], 1):
        if '复变函数_课件_前五章' in root and ch_i > 5:
            break
        lessons = ch.get('lessons') or []
        lessons = sorted(lessons, key=lambda l: l.get('position') if l.get('position') is not None else 0)
        ch_dir = os.path.join(root, safe(f"{ch_i:02d} {ch.get('name') or ''}"))
        existing = set(os.listdir(ch_dir)) if os.path.isdir(ch_dir) else set()
        gseq = 0
        for lesson in lessons:
            units = lesson.get('units') or []
            units = sorted(units, key=lambda u: u.get('position') if u.get('position') is not None else 0)
            lseq = 0
            for u in units:
                if u.get('contentType') != 3:
                    continue
                lseq += 1
                gseq += 1
                old_name = safe(f"{lseq:02d} {u.get('name') or ''}") + '.pdf'   # 下载时用的命名
                new_name = safe(f"{gseq:02d} {u.get('name') or ''}") + '.pdf'   # 按章全局顺序
                if old_name not in existing:
                    print(f'  !! 缺失: {ch_dir}/{old_name}')
                    continue
                renames.append((os.path.join(ch_dir, old_name), os.path.join(ch_dir, new_name)))
    # 冲突检测
    targets = {}
    for o, n in renames:
        if n in targets:
            print('  !! 目标重名:', n)
        targets[n] = o
    return renames

plans = {
    str(REPO / '复变函数与积分变换/资料原件/复变函数_课件_前五章'): str(REPO / 'scripts/icourse/outline_xjtu.json'),
    str(REPO / '数理方程/资料原件/数学物理方程_课程课件'): str(REPO / 'scripts/icourse/outline.json'),
}
for root, outline in plans.items():
    print('====', root)
    for o, n in build_plan(outline, root):
        tag = 'SAME' if os.path.basename(o) == os.path.basename(n) else 'MOVE'
        print(f'  [{tag}] {os.path.basename(o)}  ->  {os.path.basename(n)}')
