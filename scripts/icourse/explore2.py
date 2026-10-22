from common import CSRF
import re, json, random
from common import SESSION, TERM_ID, COURSE_PATH

url = 'https://www.icourse163.org/dwr/call/plaincall/CourseBean.getLearnedTermsByTermId.dwr'
body = (
    'callCount=1\n'
    'scriptSessionId=${scriptSessionId}187\n'
    f'httpSessionId={CSRF}\n'
    'c0-scriptName=CourseBean\n'
    'c0-methodName=getLearnedTermsByTermId\n'
    'c0-id=0\n'
    f'c0-param0=number:{TERM_ID}\n'
    'c0-param1=number:0\n'
    'c0-param2=string:\n'
    f'batchId={random.randint(100000,999999)}\n'
)
r = SESSION.post(url, data=body.encode('utf-8'),
                 headers={'Content-Type': 'text/plain'}, timeout=30)
print('dwr status:', r.status_code, 'len:', len(r.text))
open('outline_raw.txt', 'w', encoding='utf-8').write(r.text)
print(r.text[:800])
