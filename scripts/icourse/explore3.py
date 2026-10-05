import re
from common import SESSION

for bean in ['CourseBean', 'LearnBean', 'LessonBean', 'MocQuizBean', 'PostBean', 'CourseWikiBean']:
    url = f'https://www.icourse163.org/dwr/interface/{bean}.js'
    try:
        r = SESSION.get(url, timeout=30)
        print('=====', bean, r.status_code, len(r.text))
        open(f'iface_{bean}.js', 'w', encoding='utf-8').write(r.text)
        # list methods mentioning Term / Lesson / LessonUnit / Document / Pdf
        for m in re.finditer(r'(\w+)\s*=\s*function\(', r.text):
            name = m.group(1)
            if re.search(r'Term|Lesson|Pdf|Document|Learn|Unit', name):
                print('   ', name)
    except Exception as e:
        print(bean, 'ERR', e)
