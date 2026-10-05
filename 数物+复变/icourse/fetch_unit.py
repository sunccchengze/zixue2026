import random, re, time
from common import SESSION, COURSE_ID, TERM_ID

def get_unit_vo(content_id, content_type, unit_id, retries=3):
    """Call getLessonUnitLearnVo(contentId, contentType, 0, unitId)."""
    lines = [
        'callCount=1',
        'scriptSessionId=${scriptSessionId}190',
        'httpSessionId=9778371d40004721a72a7f3cbd0f4603',
        'c0-scriptName=CourseBean',
        'c0-methodName=getLessonUnitLearnVo',
        'c0-id=0',
        f'c0-param0=number:{content_id}',
        f'c0-param1=number:{content_type}',
        'c0-param2=number:0',
        f'c0-param3=number:{unit_id}',
        f'batchId={int(time.time()*1000)}',
    ]
    body = '\n'.join(lines) + '\n'
    url = 'https://www.icourse163.org/dwr/call/plaincall/CourseBean.getLessonUnitLearnVo.dwr'
    for attempt in range(retries):
        try:
            r = SESSION.post(url, data=body.encode('utf-8'),
                             headers={'Content-Type': 'text/plain'}, timeout=60)
            txt = r.text
            m = re.search(r'_remoteHandleCallback\([^,]+,[^,]+,(.*)\);\s*$', txt, re.S)
            if m:
                return m.group(1)
            if 'Exception' in txt and attempt < retries - 1:
                time.sleep(2 + attempt * 2)
                continue
            return None
        except Exception:
            if attempt < retries - 1:
                time.sleep(2 + attempt * 2)
    return None


def extract_field(vo, field):
    m = re.search(field + r':"(.*?)"', vo or '')
    if m:
        return m.group(1).encode('utf-8').decode('unicode_escape') if '\\u' in m.group(1) else m.group(1)
    return None
