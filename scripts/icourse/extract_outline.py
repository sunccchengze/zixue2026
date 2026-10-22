import re, json

html = open('learn_page.html', encoding='utf-8').read()
m = re.search(r'window\.termDto\s*=\s*(\{.*?\});?\s*(?:window\.|</script>)', html, re.S)
assert m, 'termDto not found'
raw = m.group(1)
term = json.loads(raw)
json.dump(term, open('term.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

lessons = []
for ch_i, chapter in enumerate(term.get('chapterDtos') or [], 1):
    ch_name = chapter.get('name') or ''
    for unit_i, unit in enumerate(chapter.get('lessonDtos') or [], 1):
        lessons.append({
            'chapter': ch_name,
            'chapter_idx': ch_i,
            'name': unit.get('name'),
            'id': unit.get('id'),
            'state': unit.get('state'),
        })

print('course name:', term.get('name'))
print('total lessons:', len(lessons))
for l in lessons[:12]:
    print(l['chapter_idx'], l['chapter'], '|', l['name'], l['id'])
json.dump(lessons, open('lessons.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
