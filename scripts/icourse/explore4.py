import re, json, random
from common import SESSION, TERM_ID, COURSE_ID

def dwr(method, params, bean='CourseBean'):
    lines = [
        'callCount=1',
        'scriptSessionId=${scriptSessionId}187',
        f'c0-scriptName={bean}',
        f'c0-methodName={method}',
        'c0-id=0',
    ]
    for i, p in enumerate(params):
        lines.append(f'c0-param{i}={p}')
    lines.append(f'batchId={random.randint(100000,999999)}')
    body = '\n'.join(lines) + '\n'
    url = f'https://www.icourse163.org/dwr/call/plaincall/{bean}.{method}.dwr'
    r = SESSION.post(url, data=body.encode('utf-8'),
                     headers={'Content-Type': 'text/plain'}, timeout=60)
    return r.text

# try getMocTermDto with (courseId, termId, boolean)
variants = [
    [f'number:{COURSE_ID}', f'number:{TERM_ID}', 'boolean:false'],
    [f'number:{COURSE_ID}', f'number:{TERM_ID}', 'number:0'],
    [f'number:{TERM_ID}', 'boolean:false'],
]
for v in variants:
    print('===', v)
    txt = dwr('getMocTermDto', v)
    print('len:', len(txt), txt[:300].replace('\n', '\\n'))
    if 'Exception' not in txt and len(txt) > 500:
        open('term_raw.txt', 'w', encoding='utf-8').write(txt)
        print('SAVED term_raw.txt')
        break
