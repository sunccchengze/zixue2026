import json
from common import SESSION, TERM_ID

CSRF = '9778371d40004721a72a7f3cbd0f4603'
url = f'https://www.icourse163.org/web/j/courseBean.getMocTermDto.rpc?csrfKey={CSRF}'
r = SESSION.post(url,
                 data={'termId': TERM_ID, 'isDraft': 'false', 'excludeUnrelease': 'true'},
                 headers={'X-Requested-With': 'XMLHttpRequest'},
                 timeout=60)
print('status:', r.status_code, 'len:', len(r.text))
data = r.json()
print('code:', data.get('code'), 'msg:', data.get('message'))
open('outline.json', 'w', encoding='utf-8').write(json.dumps(data, ensure_ascii=False))

result = data.get('result') or {}
moc = result.get('mocTermDto') or result
chapters = moc.get('chapterDtos') or moc.get('mocTermChapterDtos') or []
print('top keys:', list(result.keys())[:15])
print('chapters:', len(chapters))

lessons = []
for ch_i, ch in enumerate(chapters, 1):
    ch_name = ch.get('name') or ''
    for lesson in (ch.get('lessonDtos') or ch.get('mocTermLessonDtos') or []):
        lessons.append({
            'chapter_idx': ch_i,
            'chapter': ch_name,
            'name': lesson.get('name'),
            'id': lesson.get('id'),
        })
print('total lessons:', len(lessons))
for l in lessons[:8]:
    print(l)
json.dump(lessons, open('lessons.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
