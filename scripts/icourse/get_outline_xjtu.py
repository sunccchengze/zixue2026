from common import CSRF
import json
from common import SESSION

# CSRF comes from the local session environment.
TERM_ID = '1487844458'

url = f'https://www.icourse163.org/web/j/courseBean.getMocTermDto.rpc?csrfKey={CSRF}'
r = SESSION.post(url, data=f'termId={TERM_ID}&isDraft=0&excludeUnrelease=1'.encode(),
                 headers={'X-Requested-With': 'XMLHttpRequest',
                          'Content-Type': 'application/x-www-form-urlencoded'}, timeout=60)
print('status:', r.status_code, 'len:', len(r.text))
data = r.json()
print('code:', data.get('code'), 'msg:', data.get('message'))
json.dump(data, open('outline_xjtu.json', 'w', encoding='utf-8'), ensure_ascii=False)

result = data.get('result') or {}
print('courseName:', result.get('courseName'))
chs = result.get('chapters') or []
print('chapters:', len(chs))
for i, c in enumerate(chs, 1):
    lessons = c.get('lessons') or []
    n_pdf = sum(1 for l in lessons for u in (l.get('units') or []) if u.get('contentType') == 3)
    print(f"  {i}. {c.get('name')} | lessons={len(lessons)} pdf_units={n_pdf} contentType={c.get('contentType')}")
