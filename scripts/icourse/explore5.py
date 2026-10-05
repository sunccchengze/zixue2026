import re
from common import SESSION, TERM_ID, COURSE_PATH

r = SESSION.get(f'https://www.icourse163.org/learn/{COURSE_PATH}?tid={TERM_ID}', timeout=30)
open('learn_page.html', 'w', encoding='utf-8').write(r.text)
urls = re.findall(r'src=["\']([^"\']+\.js[^"\']*)["\']', r.text)
urls = [u for u in urls if 'mooc' in u or 'course' in u or 'learn' in u or 'static' in u]
urls = list(dict.fromkeys(urls))
print(len(urls))
for u in urls:
    print(u)
open('js_urls.txt', 'w').write('\n'.join(urls))
