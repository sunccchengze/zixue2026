from pathlib import Path
REPO = Path(__file__).resolve().parents[2]
import json, os, re, sys, time, unicodedata
import requests
from common import SESSION
from fetch_unit import get_unit_vo, extract_field

ROOT = str(REPO / 'build/icourse/数学物理方程_课程课件')
os.makedirs(ROOT, exist_ok=True)

data = json.load(open('outline.json', encoding='utf-8'))
chapters = data['result']['chapters']

def safe(name, maxlen=80):
    name = unicodedata.normalize('NFKC', name or 'untitled')
    name = re.sub(r'[\\/:*?"<>|\r\n\t]+', '_', name).strip(' ._')
    return name[:maxlen] or 'untitled'

tasks = []
for ch_i, ch in enumerate(chapters, 1):
    ch_dir = os.path.join(ROOT, safe(f"{ch_i:02d} {ch.get('name') or ''}"))
    for l_i, lesson in enumerate(ch.get('lessons') or [], 1):
        seq = 0
        for u in (lesson.get('units') or []):
            if u.get('contentType') == 3:  # PDF courseware unit
                seq += 1
                tasks.append({
                    'dir': ch_dir,
                    'fname': safe(f"{seq:02d} {u.get('name') or ''}") + '.pdf',
                    'content_id': u['contentId'],
                    'content_type': u['contentType'],
                    'unit_id': u['id'],
                    'chapter': ch.get('name'),
                    'lesson': lesson.get('name'),
                    'unit_name': u.get('name'),
                })

print('total pdf units:', len(tasks))
index = []
ok = fail = 0
for i, t in enumerate(tasks, 1):
    os.makedirs(t['dir'], exist_ok=True)
    path = os.path.join(t['dir'], t['fname'])
    if os.path.exists(path) and os.path.getsize(path) > 1000:
        print(f"[{i}/{len(tasks)}] SKIP {t['fname']}")
        ok += 1
        index.append({**t, 'file': path, 'status': 'exists'})
        continue
    vo = get_unit_vo(t['content_id'], t['content_type'], t['unit_id'])
    url = extract_field(vo, 'textUrl') or extract_field(vo, 'textOrigUrl')
    if not url:
        print(f"[{i}/{len(tasks)}] FAIL no url: {t['unit_name']} vo={str(vo)[:120]}")
        fail += 1
        index.append({**t, 'file': None, 'status': 'no_url'})
        continue
    try:
        r = requests.get(url, timeout=120, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/129.0.0.0 Safari/537.36',
            'Referer': 'https://www.icourse163.org/'})
        r.raise_for_status()
        blob = r.content
        if not blob.startswith(b'%PDF'):
            print(f"[{i}/{len(tasks)}] FAIL not-pdf: {t['unit_name']} head={blob[:20]!r}")
            fail += 1
            index.append({**t, 'file': None, 'status': 'not_pdf'})
            continue
        open(path, 'wb').write(blob)
        ok += 1
        print(f"[{i}/{len(tasks)}] OK {len(blob)//1024}KB {t['fname']}")
        index.append({**t, 'file': path, 'status': 'ok', 'bytes': len(blob), 'url': url})
    except Exception as e:
        print(f"[{i}/{len(tasks)}] FAIL download {t['unit_name']}: {e}")
        fail += 1
        index.append({**t, 'file': None, 'status': f'error: {e}'})
    time.sleep(0.4)

json.dump(index, open('download_index.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(f"\nDONE ok={ok} fail={fail}")
