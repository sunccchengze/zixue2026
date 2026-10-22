import requests, re, json

# 登录态仅从当前进程环境读取；不要把真实值写入源码或提交历史。
import os
COOKIE = os.environ.get('ICOURSE_COOKIE', '')
if not COOKIE:
    raise RuntimeError('请在本机环境变量 ICOURSE_COOKIE 中配置已授权的登录态；禁止写入仓库')


COURSE_ID = '1461171171'
TERM_ID = '1461946452'
COURSE_PATH = 'NJTU-1461171171'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    'Cookie': COOKIE,
    'Referer': f'https://www.icourse163.org/learn/{COURSE_PATH}?tid={TERM_ID}',
    'Origin': 'https://www.icourse163.org',
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}

SESSION = requests.Session()
SESSION.headers.update(HEADERS)

from http.cookies import SimpleCookie
_cookie_jar = SimpleCookie()
_cookie_jar.load(COOKIE)
CSRF = _cookie_jar['NTESSTUDYSI'].value if 'NTESSTUDYSI' in _cookie_jar else ''
