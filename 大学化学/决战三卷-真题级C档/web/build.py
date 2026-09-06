#!/usr/bin/env python3
# 从三套卷的 md 题目/答案文件生成 data.js（parse→校验→派发）
import re, json, os
BASE = os.path.dirname(os.path.abspath(__file__)) + '/..'
PAPERS = [
    ('1', '期中检测-卷一-镜中院', '卷一 · 镜中院', '真题原型换皮重演——在陌生的壳里认出老对手'),
    ('2', '期中检测-卷二-雾中行', '卷二 · 雾中行', '烟雾弹数据、条件帽子、反推链的主场'),
    ('3', '期中检测-卷三-回头枪', '卷三 · 回头枪', '冷知识正面确认、考古坑复活、超物理结果讨论'),
]

def load(pid, kind):
    return open(f'{BASE}/{PAPERS[int(pid)-1][1]}-{kind}.md', encoding='utf-8').read()

def sections(txt, a, b):
    i, j = txt.find(a), txt.find(b)
    return txt[i:j]

def parse_mc(qtxt):
    out = []
    for m in re.finditer(r'\*\*(\d+)\.\*\*(.*?)(?=\n\*\*\d+\.\*\*|\Z)', qtxt, re.S):
        num, body = int(m.group(1)), m.group(2)
        parts = re.split(r'\n\s*A\.', body, maxsplit=1)
        if len(parts) < 2: continue
        stem = parts[0].strip()
        opt_raw = 'A.' + parts[1]
        opts = {}
        for om in re.finditer(r'([A-D])\.\s*(.*?)(?=\n?\s*[A-D]\.\s|\Z)', opt_raw, re.S):
            opts[om.group(1)] = re.sub(r'\s+', ' ', om.group(2)).strip().strip('　')
        if len(opts) == 4:
            tag = re.search(r'（考点：(.+?)）', body)
            out.append(dict(num=num, stem=re.sub(r'\s*\n\s*', '\n', stem),
                            options=[opts[k] for k in 'ABCD'],
                            tag=tag.group(1) if tag else ''))
    return out

def parse_fill(qtxt):
    out = []
    sec = sections(qtxt, '## 二、填空题', '## 三、计算题')
    for m in re.finditer(r'\*\*(\d+)\.\*\*(.*?)(?=\n\*\*\d+\.\*\*|\Z)', sec, re.S):
        num, body = int(m.group(1)), m.group(2).strip()
        blanks = re.findall(r'_{2,}', body)
        tag = re.search(r'（(.+?)）', body)
        body_disp = re.sub(r'_{2,}', '＿＿＿', body)
        out.append(dict(num=num, stem=body_disp, nblanks=len(blanks),
                        tag=tag.group(1) if tag else ''))
    return out

def parse_calc(qtxt):
    out = []
    i = qtxt.find('## 三、计算题')
    j = qtxt.find('\n---', i + 10)
    sec = qtxt[i:(j if j > 0 else len(qtxt))]
    for m in re.finditer(r'\*\*(\d+)\.\*\*(.*?)(?=\n\*\*\d+\.\*\*|\n---|\Z)', sec, re.S):
        num, body = int(m.group(1)), m.group(2).strip()
        tag = re.search(r'（(.+?)）', body)
        out.append(dict(num=num, stem=body, tag=tag.group(1) if tag else ''))
    return out

def parse_keys(ktxt):
    # 选择答案表
    tbl = re.search(r'## 一、选择题答案总表(.*?)## 二', ktxt, re.S).group(1)
    mca = {}
    for row in re.findall(r'\|\s*(\d+)\s*\|\s*([A-D])\s*', tbl):
        mca[int(row[0])] = row[1]
    # 解析块
    expl = {}
    for m in re.finditer(r'\*\*(\d+)\.\s*([A-D])\*\*(.*?)(?=\n\*\*\d+\.|\n## |\Z)', ktxt, re.S):
        n = int(m.group(1))
        body = re.sub(r'\s*\n\s*', ' ', m.group(3)).strip()
        lvl = re.search(r'档位[:：]?\s*([A-C][+−\-]?)', body)
        trap = re.search(r'（(N\d|R\d|T\d|G\d|A\d|S\d|X\d|K\d|B\d|P\d)[）]', body)
        expl[n] = dict(ans=m.group(2), text=body[:600],
                       level=(lvl.group(1) if lvl else 'B'),
                       trap=(trap.group(1) if trap else ''))
    # 填空标准答案块
    fill = {}
    fsec = re.search(r'## 三、填空答案(.*?)## 四', ktxt, re.S)
    if fsec:
        for m in re.finditer(r'\*\*(\d+)\.\*\*(.*?)(?=\n\*\*\d+\.\*\*|\Z)', fsec.group(1), re.S):
            fill[int(m.group(1))] = re.sub(r'\s*\n\s*', ' ', m.group(2)).strip()
    # 计算解析块
    calc = {}
    csec = re.search(r'## 四、计算题标准解(.*?)(## 五|\Z)', ktxt, re.S)
    if csec:
        for m in re.finditer(r'### 算(\d+)（\d+ 分[^）)]*[）)](.*?)(?=\n### 算|\n## |\Z)', csec.group(1), re.S):
            calc[int(m.group(1))] = m.group(2).strip()
    return mca, expl, fill, calc

data = {'papers': []}
for pid, slug, title, sub in PAPERS:
    q = load(pid, '题目'); k = load(pid, '答案与解析')
    mc = parse_mc(sections(q, '## 一、选择题', '## 二、填空题'))
    fl = parse_fill(q); ca = parse_calc(q)
    mca, expl, fill_ans, calc_ans = parse_keys(k)
    assert len(mc) == 20, f'卷{pid} 选择数 {len(mc)}'
    assert len(fl) == 10, f'卷{pid} 填空数 {len(fl)}'
    assert len(ca) == 5, f'卷{pid} 计算数 {len(ca)}'
    letters = [expl[q['num']]['ans'] for q in mc]
    from collections import Counter
    dist = Counter(letters)
    assert dist == Counter({'A': 5, 'B': 5, 'C': 5, 'D': 5}), f'卷{pid}答案分布异常 {dist}'
    for q in mc:
        q['ans'] = expl[q['num']]['ans']; q['expl'] = expl[q['num']]['text']
        q['level'] = expl[q['num']]['level']; q['trap'] = expl[q['num']]['trap']
    for q in fl:
        q['rawans'] = fill_ans.get(q['num'], '')
    for q in ca:
        q['sol'] = calc_ans.get(q['num'], '')
    assert all(c['sol'].strip() for c in ca), f'卷{pid} 计算解析有空洞'
    data['papers'].append(dict(id=pid, slug=slug, title=title, subtitle=sub,
                               mc=mc, fill=fl, calc=ca))
    print(f'卷{pid} 解析完成： MC20 Fill{[(f["num"],f["nblanks"]) for f in fl]} Calc5 答案分布OK')

os.makedirs(BASE + '/web', exist_ok=True)
open(BASE + '/web/data.js', 'w', encoding='utf-8').write(
    'const DATA = ' + json.dumps(data, ensure_ascii=False, indent=1) + ';\n')
print('data.js 写出', len(json.dumps(data, ensure_ascii=False)), '字')
