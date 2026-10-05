import json, re, time
from playwright.sync_api import sync_playwright
from common import COOKIE, TERM_ID, COURSE_PATH

cookies = []
for part in COOKIE.split('; '):
    if '=' in part:
        k, v = part.split('=', 1)
        cookies.append({'name': k, 'value': v, 'domain': 'www.icourse163.org', 'path': '/'})

reqs = []

def on_request(req):
    u = req.url
    if any(x in u for x in ['.rpc', '.dwr', 'pdf', 'Pdf', '.pdf', 'nos', 'resource', 'token', 'doc']):
        reqs.append((req.resource_type, req.method, u))

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=['--no-sandbox'])
    ctx = b.new_context(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
                        viewport={'width': 1440, 'height': 900})
    ctx.add_cookies(cookies)
    pg = ctx.new_page()
    pg.on('request', on_request)
    pg.goto(f'https://www.icourse163.org/learn/{COURSE_PATH}?tid={TERM_ID}#/learn/content', timeout=60000, wait_until='domcontentloaded')
    time.sleep(8)
    pg.screenshot(path='shot1.png')
    # find outline items
    items = pg.eval_on_selector_all('span, div, a', 'els => els.map(e => e.textContent.trim()).filter(t => t && t.length < 60).slice(0, 200)')
    open('dom_texts.json', 'w', encoding='utf-8').write(json.dumps(items, ensure_ascii=False, indent=1))
    print('texts:', len(items))
    # try clicking a pdf unit: look for an element containing '课程介绍-ppt'
    try:
        el = pg.locator('text=课程介绍-ppt').first
        el.wait_for(timeout=15000)
        el.click()
        time.sleep(10)
        pg.screenshot(path='shot2.png')
    except Exception as e:
        print('click fail:', e)
    print('=== captured requests')
    for t, m, u in reqs:
        print(t, m, u[:180])
    # dump page state
    open('page_url.txt', 'w').write(pg.url)
    b.close()
