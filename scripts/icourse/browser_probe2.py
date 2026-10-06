from archive_safety import archive_url, safe_record
import json, time
from playwright.sync_api import sync_playwright
from common import COOKIE, TERM_ID, COURSE_PATH

cookies = []
for part in COOKIE.split('; '):
    if '=' in part:
        k, v = part.split('=', 1)
        cookies.append({'name': k, 'value': v, 'domain': 'www.icourse163.org', 'path': '/'})

recs = []

def interesting(req):
    if req.resource_type in ('xhr', 'fetch', 'media', 'document', 'other'):
        u = archive_url(req.url)
        if not any(x in u for x in ['.css', '.png', '.jpg', '.gif', '.ico', '.woff', 'hubble', 'DATracker', 'log.']):
            return True
    return False

def on_request(req):
    if interesting(req):
        body = None
        try:
            body = req.post_data
        except Exception:
            pass
        recs.append({'type': req.resource_type, 'method': req.method, 'url': archive_url(req.url)})

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=['--no-sandbox'])
    ctx = b.new_context(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
                        viewport={'width': 1440, 'height': 900})
    ctx.add_cookies(cookies)
    pg = ctx.new_page()
    pg.on('request', on_request)
    pg.goto(f'https://www.icourse163.org/learn/{COURSE_PATH}?tid={TERM_ID}#/learn/content', timeout=60000, wait_until='domcontentloaded')
    time.sleep(6)
    el = pg.locator('text=课程介绍-ppt').first
    el.wait_for(timeout=20000)
    el.click()
    time.sleep(15)
    # capture responses for dwr + pdf-ish requests
    out = []
    for r in recs:
        u = r['url']
        if 'getLessonUnitLearnVo' in u or '.pdf' in u or 'pdf' in u.lower() or 'content?' in u or '/content' in u:
            r['match'] = True
        out.append(r)
    json.dump(out, open('net_log.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('total recs:', len(out))
    for r in out:
        flag = '*' if r.get('match') else ' '
        print(flag, r['type'], r['method'], r['url'][:160])
        if r.get('body'):
            print('      BODY:', r['body'][:300])
    b.close()
