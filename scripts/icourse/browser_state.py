import json, time
from playwright.sync_api import sync_playwright
from common import COOKIE, TERM_ID, COURSE_PATH

cookies = []
for part in COOKIE.split('; '):
    if '=' in part:
        k, v = part.split('=', 1)
        cookies.append({'name': k, 'value': v, 'domain': 'www.icourse163.org', 'path': '/'})

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=['--no-sandbox'])
    ctx = b.new_context(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
                        viewport={'width': 1440, 'height': 900})
    ctx.add_cookies(cookies)
    pg = ctx.new_page()
    pg.goto(f'https://www.icourse163.org/learn/{COURSE_PATH}?tid={TERM_ID}#/learn/content', timeout=60000, wait_until='domcontentloaded')
    time.sleep(10)
    print('URL:', pg.url)
    print('TITLE:', pg.title())
    txt = pg.evaluate('document.body ? document.body.innerText.slice(0, 600) : ""')
    print('BODY:', txt)
    pg.screenshot(path='shot_state.png', full_page=False)
    b.close()
