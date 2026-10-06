from common import CSRF
import re, json, random
from common import SESSION, TERM_ID, COURSE_PATH

# 1) check login + course page
r = SESSION.get(f'https://www.icourse163.org/learn/{COURSE_PATH}?tid={TERM_ID}', timeout=30)
print('learn page status:', r.status_code, 'len:', len(r.text))
m = re.search(r'<title>(.*?)</title>', r.text, re.S)
print('title:', m.group(1).strip() if m else None)
m = re.search(r'nickname["\s:]+([^",<]+)', r.text)
print('nickname hit:', m.group(1)[:80] if m else None)

# 2) DWR: course outline (chapters/lessons)
url = 'https://www.icourse163.org/dwr/call/plaincall/CourseBean.getLearnedTermsByTermId.dwr'
data = {
    'callCount': '1',
    'scriptSessionId': '${scriptSessionId}187',
    'httpSessionId': CSRF,
    'c0-scriptName': 'CourseBean',
    'c0-methodName': 'getLearnedTermsByTermId',
    'c0-id': '0',
    'c0-param0': f'number:{TERM_ID}',
    'c0-param1': 'number:0',
    'c0-param2': 'string:',
    'batchId': str(random.randint(100000, 999999)),
}
r2 = SESSION.post(url, data=data, timeout=30)
print('dwr status:', r2.status_code, 'len:', len(r2.text))
open('outline_raw.txt', 'w', encoding='utf-8').write(r2.text)
print(r2.text[:600])
