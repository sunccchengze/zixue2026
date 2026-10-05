import json, time
from playwright.sync_api import sync_playwright
from common import COOKIE, TERM_ID, COURSE_PATH

cookies = []
for part in COOKIE.split('; '):
    if '=' in part:
        k, v = part.split('=', 1)
        cookies.append({'name': k, 'value': v, 'domain': 'www.icourse163.org', 'path': '/'})

records = []

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=['--no-sandbox'])
    ctx = b.new_context(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
                        viewport={'width': 1440, 'height': 900})
    ctx.add_cookies(cookies)
    pg = ctx.new_page()

    def on_response(resp):
        req = resp.request
        u = req.url
        keep = ('getLessonUnitLearnVo' in u or '.pdf' in u.lower() or 'pdf' in u.lower()
                or 'resource' in u.lower() or '.dwr' in u)
        if not keep:
            return
        rec = {'url': u, 'type': req.resource_type, 'method': req.method,
               'status': resp.status, 'req_body': None, 'resp_text': None}
        try:
            rec['req_body'] = req.post_data
        except Exception:
            pass
        ct = (resp.headers or {}).get('content-type', '')
        if 'pdf' in ct or 'json' in ct or 'javascript' in ct or 'text' in ct or '.dwr' in u:
            try:
                body = resp.body()
                rec['resp_text'] = body[:5000].decode('utf-8', 'replace') if isinstance(body, bytes) else str(body)[:5000]
                rec['resp_size'] = len(body)
                rec['content_type'] = ct
            except Exception as e:
                rec['resp_err'] = str(e)
        else:
            rec['content_type'] = ct
        records.append(rec)

    pg.on('response', on_response)
    pg.goto(f'https://www.icourse163.org/learn/{COURSE_PATH}?tid={TERM_ID}#/learn/content', timeout=120000, wait_until='commit')
    el = pg.locator('text=课程介绍-ppt').first
    el.wait_for(timeout=60000)
    el.click()
    time.sleep(25)
    pg.screenshot(path='shot_pdf.png')
    json.dump(records, open('pdf_net.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    for r in records:
        print(r['status'], r['type'], r['method'], r['url'][:170])
        if r.get('req_body'):
            print('   REQ:', r['req_body'][:400])
        if r.get('resp_text'):
            print('   RESP:', r['resp_text'][:400].replace('\n', ' '))
    b.close()
