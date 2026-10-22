#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 自学工作台（训练场 · 单文件服务器 · 零依赖）
=====================================================================
免去切换文件：同一屏答闸门、读教材卷、交资产、自评、做复习卡；
进度自动落盘 训练场/progress/（progress.json / reviews.json / 工作台日志.md），
资产自动登记 资产总账.md，存疑自动登记 存疑台账.md。

启动：  python3 训练场/workbench/server.py --port 8901
"""
from __future__ import annotations

import html
import json
import os
import re
import threading
import urllib.parse
from datetime import datetime, timedelta, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # 论文精读/白皮书
TF = os.path.join(ROOT, "训练场")
UNITS = os.path.join(TF, "units")
IMG = os.path.join(ROOT, "images")
DOCS = os.path.join(ROOT, "docs")
PROG = os.path.join(TF, "progress")
LEDGER = os.path.join(TF, "资产总账.md")
DOUBT = os.path.join(TF, "存疑台账.md")
os.makedirs(PROG, exist_ok=True)
GITKEEP = os.path.join(PROG, ".gitkeep")
if not os.path.exists(GITKEEP):
    open(GITKEEP, "w").close()

TZ = timezone(timedelta(hours=8))
LOCK = threading.RLock()


def now() -> str:
    return datetime.now(TZ).strftime("%Y-%m-%d %H:%M")


# ---------------------------------------------------------------- 数据存取
def load_json(name, default):
    p = os.path.join(PROG, name)
    with LOCK:
        if not os.path.exists(p):
            return default
        try:
            with open(p, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return default


def save_json(name, data):
    p = os.path.join(PROG, name)
    with LOCK:
        with open(p, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=1)


def journal(line):
    p = os.path.join(PROG, "工作台日志.md")
    with LOCK:
        with open(p, "a", encoding="utf-8") as f:
            f.write(f"- {now()} | {line}\n")


def unit_dirs():
    out = []
    if os.path.isdir(UNITS):
        for n in sorted(os.listdir(UNITS)):
            if re.match(r"^u\d{2}(-|$)", n):
                out.append(n)
    return out


def read_or(path):
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except OSError:
        return ""


# ---------------------------------------------------------------- Markdown → HTML
BLOCK_OPEN = ("<details", "<summary")


def esc(t):
    return html.escape(t, quote=False)


def inline_md(t):
    t = re.sub(r"<!--.*?-->", "", t, flags=re.S)
    t = esc(t)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', t)

    def img(m):
        alt, src = m.group(1), m.group(2)
        name = os.path.basename(urllib.parse.unquote(src))
        return (f'<figure><img src="/images/{urllib.parse.quote(name)}" alt="{esc(alt)}"/>'
                f"<figcaption>{alt}</figcaption></figure>")
    t = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", img, t)
    return t


def md_to_html(src, idprefix=None):
    """受控 Markdown → HTML。idprefix：给标题锚点加前缀防碰撞（如 'ch0' → ch0-0.1）。"""
    lines = src.split("\n")
    out, i, n = [], 0, len(lines)
    footdefs = []
    footn = {}

    def hid(text):
        m = re.match(r"^(\d+(?:\.\d+)?)", text.strip())
        if not m:
            return ""
        base = f"{idprefix}-{m.group(1)}" if idprefix else f"sec-{m.group(1)}"
        return base

    while i < n:
        line = lines[i].rstrip()
        s = line.strip()
        if not s:
            i += 1
            continue
        if s.startswith("```"):
            buf, i = [], i + 1
            while i < n and not lines[i].strip().startswith("```"):
                buf.append(lines[i])
                i += 1
            i += 1
            out.append(f'<pre class="code">{esc(chr(10).join(buf))}</pre>')
            continue
        if s.startswith("<!--"):
            i += 1
            continue
        if any(s.startswith(t) for t in BLOCK_OPEN) or s in ("</details>", "</summary>"):
            out.append(s)
            i += 1
            continue
        m = re.match(r"^(#{1,4})\s+(.*)$", line)
        if m:
            lv = len(m.group(1)) + 1  # # → h2? 统一视觉：#=h1 太大；全部 +1
            if lv > 6:
                lv = 6
            out.append(f'<h{lv} id="{hid(m.group(2))}">{inline_md(m.group(2))}</h{lv}>')
            i += 1
            continue
        if s == "---":
            out.append("<hr/>")
            i += 1
            continue
        m = re.match(r"^\[\^([\w-]+)\]:\s*(.*)$", line)
        if m:
            footdefs.append((m.group(1), m.group(2)))
            i += 1
            continue
        if s.startswith("|"):
            buf = []
            while i < n and lines[i].strip().startswith("|"):
                buf.append(lines[i].strip())
                i += 1
            rows = []
            for ri, r in enumerate(buf):
                cells = [c.strip() for c in r.strip().strip("|").split("|")]
                if ri == 1 and all(re.match(r"^:?-{2,}:?$", c) for c in cells if c):
                    continue
                rows.append(cells)
            if rows:
                th = "".join(f"<th>{inline_md(c)}</th>" for c in rows[0])
                trs = "".join("<tr>" + "".join(f"<td>{inline_md(c)}</td>" for c in r) + "</tr>" for r in rows[1:])
                out.append(f"<table><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table>")
            continue
        m = re.match(r"^(\s*)([-*]|\d+[\.、）)])\s+(.*)$", line)
        if m:
            tag = "ul" if m.group(2) in ("-", "*") else "ol"
            buf = []
            while i < n:
                cur = lines[i].rstrip()
                if not cur.strip() or cur.strip() == "---":
                    break
                mm = re.match(r"^(\s*)([-*]|\d+[\.、）)])\s*(.*)$", cur)
                if not mm:
                    if cur.startswith(">"):  # 列表内的引用行并入上一项
                        buf[-1] = buf[-1] + " " + inline_md(re.sub(r"^>\s?", "", cur))
                        i += 1
                        continue
                    break
                sub = " class=sub" if len(mm.group(1)) >= 2 else ""
                buf.append(f"<li{sub}>{inline_md(mm.group(3))}</li>")
                i += 1
            out.append(f"<{tag}>{''.join(buf)}</{tag}>")
            continue
        if s.startswith(">"):
            buf = []
            while i < n and lines[i].startswith(">"):
                buf.append(inline_md(re.sub(r"^>\s?", "", lines[i]).rstrip()))
                i += 1
            out.append(f"<blockquote>{'<br/>'.join(buf)}</blockquote>")
            continue
        para = [line]
        i += 1
        while i < n:
            nx = lines[i].rstrip()
            ns = nx.strip()
            if not ns or ns == "---":
                break
            if re.match(r"^(#{1,4})\s", nx) or ns.startswith("```") or ns.startswith("|") or ns.startswith(">"):
                break
            if any(ns.startswith(t) for t in BLOCK_OPEN) or ns in ("</details>", "</summary>"):
                break
            if re.match(r"^(\s*)([-*]|\d+[\.、）)])\s+", nx):
                break
            para.append(nx)
            i += 1
        out.append(f"<p>{'<br/>'.join(inline_md(p) for p in para)}</p>")
    html_out = "\n".join(out)
    if footdefs:
        seq = {}
        for tag, _ in footdefs:
            if tag not in seq:
                seq[tag] = len(seq) + 1
        pat = re.compile(r"\[\^([\w-]+)\]")
        def sup(m):
            return f'<sup class="fn">[{seq.get(m.group(1), "?")}]</sup>'
        items = "".join("<li>" + pat.sub(sup, inline_md(d)) + "</li>" for _, d in footdefs)
        # 正文里的引用标记也换成上标（跳过 <pre> 代码块）
        parts = re.split(r'(<pre class="code">.*?</pre>)', html_out, flags=re.S)
        html_out = "".join(p if p.startswith("<pre") else pat.sub(sup, p) for p in parts)
        html_out += f"<details class='fns'><summary>引用出处 {len(footdefs)} 条（教材卷脚注，机器可回溯）</summary><ol>{items}</ol></details>"
    return html_out


# ---------------------------------------------------------------- 关卡卡解析
def split_card(md):
    secs, cur = {}, None
    for ln in md.split("\n"):
        m = re.match(r"^## (\d+)\.\s*(.*)$", ln)
        if m:
            cur = m.group(1)
            secs[cur] = {"head": m.group(2), "body": []}
        elif cur:
            secs[cur]["body"].append(ln)
    return secs


def parse_gates(md):
    _, s1 = md.split("## 1.", 1)
    s1 = s1.split("## 2.", 1)[0]
    gates = []
    for ln in s1.split("\n"):
        m = re.match(r"^\s*(\d+)[\.、]\s*(.+?)\s*$", ln)
        if m:
            gates.append({"n": int(m.group(1)), "text": m.group(2)})
    return gates


def parse_steps(md):
    if "## 2." not in md:
        return []
    s2 = md.split("## 2.", 1)[1].split("## 3.", 1)[0]
    rows = []
    for ln in s2.split("\n"):
        if ln.strip().startswith("|") and not re.match(r"^\|[-: |]+\|?$", ln.strip()):
            cells = [c.strip() for c in ln.strip().strip("|").split("|")]
            if len(cells) >= 3:
                rows.append(cells)
    steps = []
    for cells in rows[1:]:  # 跳过表头
        what = cells[1] if len(cells) > 1 else ""
        doc, sec = "", ""
        anchor = ""
        m = re.search(r"讲(\d{2})", what)
        if m:
            doc = f"lecture-{int(m.group(1)):02d}"
            sm = re.search(r"§(\d+)", what)
            sec = sm.group(1) if sm else ""
            anchor = f"{doc}-{sec}" if sec else doc
        elif "第零章" in what:
            doc = "chapter0"
            sm = re.search(r"0\.(\d+)", what)
            sec = sm.group(1) if sm else ""
            anchor = f"chapter0-0.{sec}" if sec else "chapter0"
        steps.append({"ord": cells[0], "what": what,
                      "time": cells[2] if len(cells) > 2 else "",
                      "doc": doc, "anchor": anchor})
    return steps


def parse_tasks(md):
    if "## 3." not in md:
        return []
    s3 = md.split("## 3.", 1)[1].split("## 4.", 1)[0]
    tasks = []
    for ln in s3.split("\n"):
        if re.match(r"^\|\s*T\d+", ln.strip()):
            cells = [c.strip() for c in ln.strip().strip("|").split("|")]
            if len(cells) >= 4:
                tasks.append({"id": cells[0], "text": cells[1], "kind": cells[2],
                              "path": cells[3], "accept": cells[4] if len(cells) > 4 else ""})
    for t in tasks:
        m = re.search(r"资产/([\w\u4e00-\u9fff-]+\.md)", t["path"])
        t["asset_file"] = m.group(1) if m else ""
        t["oral"] = ("口头" in t["path"] or "口述" in t["text"]) and not t["asset_file"]
        t["quiz"] = ("自测" in t["text"] or "试卷" in t["text"]) and not t["asset_file"]
    return tasks


def unit_lecture(md):
    m = re.search(r"〔教材卷\s*讲(\d{2})", md)
    if not m:
        m = re.search(r"讲(\d{2})", md)
    if m:
        return f"lecture-{int(m.group(1)):02d}"
    return "chapter0" if "第零章" in md else ""


def read_doc(doc):
    if doc == "chapter0":
        return read_or(os.path.join(DOCS, "chapter0.md"))
    if doc == "front":
        return read_or(os.path.join(DOCS, "front_matter.md"))
    m = re.match(r"^lecture-(\d{2})$", doc or "")
    if m:
        return read_or(os.path.join(DOCS, "lectures", f"{int(m.group(1)):02d}.md"))
    return ""


def lecture_quiz(doc):
    txt = read_doc(doc)
    qs, ans, in_q, in_a = [], [], False, False
    for ln in txt.split("\n"):
        s = ln.strip()
        if s.startswith("#### 11."):
            in_q, in_a = True, False
            continue
        if in_q and s.startswith("**答案要点**"):
            in_q, in_a = False, True
            continue
        if in_q and s.startswith("#### "):
            break
        if in_a and s.startswith("#### "):
            break
        if in_a:
            m = re.match(r"^(\d+)\.\s*(.+)$", s)
            if m:
                ans.append((int(m.group(1)), m.group(2)))
        elif in_q:
            m = re.match(r"^(\d+)\.\s*（(选|填|答)）(.+)$", s)
            if m:
                qs.append({"n": int(m.group(1)), "type": m.group(2),
                           "text": re.sub(r"\[\^[\w-]+\]", "", m.group(3))})
    return qs, "\n".join(f"{n}. {a}" for n, a in sorted(ans))


# ---------------------------------------------------------------- 台账写回
def ledger_rows():
    txt = read_or(LEDGER)
    return sum(1 for ln in txt.split("\n") if re.match(r"^\|\s*\d+\s*\|", ln))


def append_ledger(unit_dir, filename, title):
    m = re.match(r"^(u\d\d)-([A-Z])(\d+)-(.+)\.md$", filename)
    if not m:
        return False
    code, kind, num = m.group(1), m.group(2), m.group(3)
    txt = read_or(LEDGER)
    marker = "<!-- 资产行从此处续写 -->"
    if marker not in txt:
        return False
    lines = txt.split("\n")
    at = next((i for i, ln in enumerate(lines) if marker in ln), None)
    if at is None:
        return False
    row_no = ledger_rows() + 1
    line = (f"| {row_no} | {code}-{kind}{num} | {code} | {kind} | units/{unit_dir}/资产/{filename} | "
            f"{title} | 已交 | {now()} |")
    lines.insert(at, line)
    with open(LEDGER, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return True


def append_doubt(text):
    txt = read_or(DOUBT)
    marker = "<!-- 新增存疑从此处续写（给行号 D05…，并在此注释行上方插入） -->"
    if marker not in txt:
        return False
    nums = [int(x) for x in re.findall(r"^\|\s*D(\d+)\s*\|", txt, re.M)]
    nxt = (max(nums) + 1) if nums else 5
    line = f"| D{nxt:02d} | {text} | 训练期新增 | 待定 | 🔵 | {now()} |\n"
    txt = txt.replace(marker, line + marker)
    with open(DOUBT, "w", encoding="utf-8") as f:
        f.write(txt)
    return True


# ---------------------------------------------------------------- 进度
def progress():
    return load_json("progress.json", {})


def unit_prog(uid, pr=None):
    p = pr if pr is not None else progress()
    return p.setdefault(uid, {"gates": {}, "steps": {}, "oral": [], "quiz": {}, "assets": [], "status": ""})


def unit_status(uid, pg):
    if pg.get("status"):
        return pg["status"]
    if not pg.get("gates") and not pg.get("assets") and not pg.get("oral"):
        return "未开始"
    pend = any(g.get("judge", "") in ("", "pending") for g in pg.get("gates", {}).values())
    wrong = any(g.get("judge") == "wrong" for g in pg.get("gates", {}).values())
    if pend:
        return "待教练判"
    if wrong:
        return "有错题"
    if pg.get("assets") or pg.get("oral"):
        return "可过卡"
    return "进行中"


# ---------------------------------------------------------------- 复习
def review_all():
    return load_json("reviews.json", {"items": []})


def review_add(text, src):
    data = review_all()
    data["items"].append({"id": (max((i["id"] for i in data["items"]), default=0) + 1),
                          "text": text, "src": src, "stage": 0,
                          "due": now(), "add": now()})
    save_json("reviews.json", data)


def review_grade(iid, ok):
    data = review_all()
    for it in data["items"]:
        if it["id"] == iid:
            it["stage"] = 0 if not ok else it.get("stage", 0) + 1
            days = [1, 3, 7, 21][min(it["stage"], 3)]
            it["due"] = (datetime.now(TZ) + timedelta(days=days)).strftime("%Y-%m-%d %H:%M")
            save_json("reviews.json", data)
            return True
    return False


# ---------------------------------------------------------------- 页面
CSS = """
*{box-sizing:border-box}
body{margin:0;font:15px/1.75 -apple-system,'PingFang SC','Microsoft YaHei',sans-serif;background:#f2f4f8;color:#1f2937}
a{color:#3b5bdb;text-decoration:none}a:hover{text-decoration:underline}
.wrap{max-width:1040px;margin:0 auto;padding:0 16px 70px}
.top{background:#232946;color:#fff;padding:0;position:sticky;top:0;z-index:9}
.top .wrap{display:flex;gap:16px;align-items:center;padding:10px 16px}
.top .brand{color:#fff;font-weight:800;margin-right:6px}
.top a{color:#cdd7ff;font-weight:600;border-radius:6px;padding:2px 10px}
.top a.on{background:#3b5bdb;color:#fff}
h1{font-size:22px;margin:16px 0 6px}
h2{font-size:17px;margin:26px 0 8px;border-left:4px solid #3b5bdb;padding-left:8px}
h3{font-size:15px}h4{font-size:14px}
.card{background:#fff;border:1px solid #e5e7eb;border-radius:12px;padding:14px 18px;margin:12px 0}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(228px,1fr));gap:12px}
.u{background:#fff;border:1px solid #e5e7eb;border-radius:12px;padding:12px 14px}
.u .t{font-weight:700}.u .s{font-size:12px;color:#6b7280}
.chip{display:inline-block;padding:1px 9px;border-radius:999px;font-size:12px;font-weight:600}
.c0{background:#eef0f3;color:#4b5563}.c1{background:#dbe4ff;color:#2743b8}
.c2{background:#fff3bf;color:#9a6b00}.c3{background:#d3f9d8;color:#18794e}.c4{background:#ffe3e3;color:#c92a2a}
table{border-collapse:collapse;width:100%;margin:8px 0;font-size:13.5px;background:#fff}
th,td{border:1px solid #e2e6ee;padding:5px 8px;vertical-align:top;text-align:left}
th{background:#eef1f7}
img{max-width:100%;border-radius:8px}figure{margin:10px 0}figcaption{font-size:12.5px;color:#6b7280;margin-top:2px}
pre.code{background:#0f172a;color:#e2e8f0;padding:10px 12px;border-radius:8px;overflow:auto;font-size:12.5px;line-height:1.5}
code{background:#eef0f5;border-radius:4px;padding:0 4px;font-size:90%}
pre.code code{background:none;color:inherit}
blockquote{border-left:3px solid #94a3b8;margin:8px 0;padding:4px 12px;background:#fafbfd;color:#374151}
input[type=text],textarea,select{width:100%;padding:8px 10px;border:1px solid #cbd5e1;border-radius:8px;font:inherit;background:#fff}
textarea{min-height:72px}
.btn{display:inline-block;background:#3b5bdb;color:#fff;border:1px solid transparent;border-radius:8px;padding:6px 14px;font:inherit;cursor:pointer}
.btn.ghost{background:#fff;color:#3b5bdb;border-color:#3b5bdb}
.btn.green{background:#18794e}.btn.red{background:#c92a2a;color:#fff}.btn.gray{background:#6b7280;color:#fff}
.btn.sm{padding:2px 10px;font-size:13px}
small{color:#6b7280}
.q{border:1px solid #e5e7eb;border-radius:10px;padding:10px 14px;margin:10px 0;background:#fff}
.q .qt{font-weight:600}
.ok{color:#18794e;font-weight:700}.bad{color:#c92a2a;font-weight:700}.pend{color:#b58900;font-weight:700}
details{background:#f8f9fb;border:1px solid #e5e7eb;border-radius:8px;padding:6px 12px;margin:8px 0}
details.coach{border:1.5px solid #f0c000}
details.coach>summary{color:#9a6b00;font-weight:700}
summary{cursor:pointer;font-weight:600}
.hero{background:linear-gradient(135deg,#232946,#3b5bdb);color:#fff;border-radius:14px;padding:18px 22px;margin:14px 0}
.hero h1{margin:0 0 4px;color:#fff}.hero a{color:#ffe066;font-weight:700}
.steprow{display:flex;gap:10px;align-items:center;padding:6px 0;border-bottom:1px dashed #e5e7eb;flex-wrap:wrap}
.steptag{min-width:34px;font-weight:700}
.footer{color:#9aa1ad;font-size:12px;margin-top:34px;text-align:center}
.doc{background:#fff}
.doc h2{margin-top:20px}
.fn{color:#6b7280;font-size:10px}
details.fns{font-size:12px;color:#6b7280}
"""


def page(title, body, nav=""):
    navs = ""
    for u, t in (("/", "工作台"), ("/review", "复习队列"), ("/coach", "教练快照")):
        navs += f'<a href="{u}"{" class=on" if nav == u else ""}>{t}</a>'
    return f"""<!doctype html><html lang="zh"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)} · AI 自学工作台</title><style>{CSS}</style></head>
<body><div class="top"><div class="wrap"><span class="brand">🏋️ AI 自学工作台</span>{navs}
<span style="margin-left:auto;font-size:12px;color:#cdd7ff">{now()}</span></div></div>
<div class="wrap">{body}<div class="footer">数据自动落盘 训练场/progress/ · 教材卷：论文精读/白皮书 · 训练场 v3</div></div></body></html>"""


def dashboard_html():
    pr = progress()
    due_n = sum(1 for it in review_all()["items"] if it.get("due", "") <= now())
    chips = {"未开始": "c0", "进行中": "c1", "待教练判": "c2", "可过卡": "c3", "已过卡": "c3", "有错题": "c4"}
    rows = []
    for d in unit_dirs():
        uid = d[:3]
        pg = unit_prog(uid)
        card = read_or(os.path.join(UNITS, d, "关卡卡.md"))
        line1 = next((ln[2:] for ln in card.split("\n") if ln.startswith("# ")), uid)
        name = d.split("-", 1)[1] if "-" in d else ""
        st = unit_status(uid, pg)
        na = len(pg.get("assets", []))
        ng = len(pg.get("gates", {}))
        nj = sum(1 for g in pg.get("gates", {}).values() if g.get("judge") == "ok")
        rows.append(f"""<div class="u"><div class="t">{uid} · {esc(name)}</div>
<div class="s">{esc(line1[:56])}</div>
<div class="s" style="margin-top:2px">闸门对 {nj}/{ng} · 资产 {na}</div>
<div style="margin:6px 0"><span class="chip {chips.get(st,'c0')}">{st}</span></div>
<a class="btn ghost sm" href="/unit/{uid}">进入</a></div>""")
    hero = f"""<div class="hero"><h1>机器学习 × 气动外形优化 · 训练场</h1>
<div>你 = 运动员，AI = 教练 + 后勤。答题 → 读教材 → 交资产 → 进度自动记录，全在这里。</div>
<div style="margin-top:10px">▶ 下一步建议：<a href="/unit/u00">U0 地基闯关 · 快档开跑</a>
&nbsp;·&nbsp; 复习队列到期 <a href="/review">{due_n} 张</a></div></div>"""
    log = read_or(os.path.join(PROG, "工作台日志.md")).strip()
    tail = "<br/>".join(log.split("\n")[-10:]) if log else "（还没有记录——答一道闸门题试试，会立刻出现在这里）"
    body = hero + f"""<h2>训练单元（13 关）</h2><div class="grid">{''.join(rows) or '<p>还没有单元</p>'}</div>
<h2>最近动态 · 自动记录</h2><div class="card"><small>{tail}</small></div>
<h2>随手记</h2><div class="card"><form method="post" action="/doubt/add" style="display:flex;gap:8px">
<input type="text" name="text" placeholder="遇到存疑？记进 存疑台账（D 编号自动续）"/>
<button class="btn gray">存疑 +1</button></form></div>
<h2>资料直读（不用切文件）</h2><div class="card">
<a href="/read/front" target="_blank">前言 · 怎么用这本书</a> ·
<a href="/read/chapter0" target="_blank">第零章</a> ·
<a href="/read/lecture-01" target="_blank">讲 01</a> ·
<a href="/doc/训练场/README.md" target="_blank">训练场 README</a> ·
<a href="/doc/训练场/教练协议-v1.md" target="_blank">教练协议</a> ·
<a href="/doc/训练场/资产总账.md" target="_blank">资产总账</a> ·
<a href="/doc/训练场/存疑台账.md" target="_blank">存疑台账</a></div>"""
    return page("工作台", body, "/")


def unit_html(uid):
    d = next((x for x in unit_dirs() if x.startswith(uid)), None)
    if not d:
        return page(uid, "<p>该单元还没建。试点：u00 / u01。</p>", "/")
    card_md = read_or(os.path.join(UNITS, d, "关卡卡.md"))
    coach_md = read_or(os.path.join(UNITS, d, "教练脚本.md"))
    if not card_md:
        return page(uid, "<p>关卡卡缺失。</p>", "/")
    secs = split_card(card_md)
    pg = unit_prog(uid)
    gates = parse_gates(card_md)
    steps = parse_steps(card_md)
    tasks = parse_tasks(card_md)
    doc = unit_lecture(card_md)
    st = unit_status(uid, pg)
    chips = {"未开始": "c0", "进行中": "c1", "待教练判": "c2", "可过卡": "c3", "已过卡": "c3", "有错题": "c4"}

    h = [f"""<div class="card" style="display:flex;gap:14px;align-items:center;flex-wrap:wrap">
<span class="chip {chips.get(st,'c0')}" style="font-size:14px">{st}</span>
<span>档位/时间盒：{esc('　'.join(x.strip() for x in secs.get('6',{}).get('body',[])[:2]))}</span></div>"""]

    def sec_body(n):
        return "\n".join(secs.get(n, {}).get("body", []))

    h.append(f"<h1>{esc(uid)} · {esc(d.split('-',1)[1] if '-' in d else '')}</h1>")
    h.append(f"<h2>0 · {esc(secs.get('0',{}).get('head','目标与验收线'))}</h2>"
             f"<div class='card'>{md_to_html(sec_body('0'))}</div>")

    # —— 1 闸门 ——
    h.append(f"<h2>1 · 闸门（先自己答；答案信封在本页最底部，别提前开）</h2>")
    for g in gates:
        gid = f"g{g['n']}"
        rec = pg["gates"].get(str(g["n"]), {})
        ans = rec.get("answer", "")
        judge = rec.get("judge", "")
        jt = {"": '<span class="pend">● 未答</span>', "pending": '<span class="pend">● 待教练判</span>',
              "ok": '<span class="ok">✓ 判·对</span>', "half": '<span class="pend">◐ 判·半对</span>',
              "wrong": '<span class="bad">✗ 判·错 → 已入复习队</span>',
              "skip": '<span>— 口头答（教练在对话里判）</span>'}.get(judge, esc(judge))
        h.append(f"""<div class="q" id="gate-{g['n']}">
<div class="qt">闸门 {g['n']} · {inline_md(g['text'])}</div>
<div style="margin:4px 0">{jt} <small>{esc(rec.get('ts',''))}</small></div>
<form method="post" action="/unit/{uid}/gate"><input type="hidden" name="n" value="{g['n']}"/>
<textarea name="answer" rows="3" placeholder="写答案。合上书、别翻答案信封。">{esc(ans)}</textarea>
<div style="margin-top:6px;display:flex;gap:8px;flex-wrap:wrap;align-items:center">
<button class="btn">保存答案</button>
<button class="btn gray" name="v" value="pending">我口头答，等教练判</button></div></form>
<form method="post" action="/unit/{uid}/judge" style="margin-top:6px;display:flex;gap:6px;align-items:center;flex-wrap:wrap">
<input type="hidden" name="n" value="{g['n']}"/><small>已对照答案？自评：</small>
<button class="btn green sm" name="v" value="ok">对</button>
<button class="btn ghost sm" name="v" value="half">半对</button>
<button class="btn red sm" name="v" value="wrong">错</button>
<button class="btn gray sm" name="v" value="skip">跳过此题（口头）</button></form></div>""")

    # —— 2 阅读地图 + 教材卷 ——
    steps_html = []
    for s in steps:
        done = bool(pg["steps"].get(s["ord"]))
        anchor = f"#{s['anchor']}" if s.get("anchor") else "#2"
        steps_html.append(f"""<div class="steprow"><span class="steptag">{esc(s['ord'])}</span>
<span style="flex:1">{inline_md(s['what'])} <small>（{esc(s['time'])}）</small></span>
<a class="btn ghost sm" href="{anchor}">跳到原文</a>
<form method="post" action="/unit/{uid}/step" style="margin:0"><input type="hidden" name="n" value="{esc(s['ord'])}"/>
<button class="btn {'green' if done else 'ghost'} sm">{'已读 ✓' if done else '标记已读'}</button></form></div>""")
    doc_html = md_to_html(read_doc(doc), idprefix=doc) if doc else ""
    h.append(f"<h2>2 · 阅读地图</h2><div class='card'>{''.join(steps_html) or '（无）'}"
             f"<p><small>按站读，读完点「标记已读」。教材卷原文就在下方，图文同屏 ↓</small></p></div>")
    h.append(f'<div id="{doc}" class="card doc">{doc_html or "<p>（教材卷文件未就绪）</p>"}</div>')

    # —— 3 任务 ——
    h.append("<h2>3 · 输出任务（过卡线：每单元 ≥1 件资产）</h2>")
    for t in tasks:
        done_tag = ""
        if t["asset_file"]:
            owned = any(a.get("file") == t["asset_file"] for a in pg.get("assets", []))
            done_tag = '<span class="ok">已交 ✓</span>' if owned else ""
        elif t["oral"]:
            done_tag = f'<span class="ok">已记录 {len(pg.get("oral", []))} 次</span>' if pg.get("oral") else ""
        elif t["quiz"]:
            done_tag = f'<span class="ok">已答 {len(pg.get("quiz", {}))} 题</span>' if pg.get("quiz") else ""
        h.append(f"<div class='q' id='task-{esc(t['id'])}'><b>{esc(t['id'])} · {inline_md(t['text'])}</b> {done_tag}")
        if t["accept"]:
            h.append(f"<div style='font-size:13px'><small>验收线：{inline_md(t['accept'])}</small></div>")
        if t["oral"]:
            h.append(f"""<form method="post" action="/unit/{uid}/oral" style="margin-top:6px">
<textarea name="text" rows="3" placeholder="口述稿敲这里（或写：已在对话里口述给教练判，教练记档）"></textarea>
<button class="btn">记录口述</button></form>""")
        elif t["asset_file"]:
            h.append(f"""<form method="post" action="/unit/{uid}/asset" style="margin-top:6px">
<p style="margin:4px 0"><small>文件名（自动登记 资产总账）：</small>
<input type="text" name="file" style="width:min(400px,90%)" value="{esc(t['asset_file'])}"/></p>
<textarea name="body" rows="10" placeholder="资产正文写这里 → 提交 = 落盘 units/{d}/资产/ + 总账 +1 行。正文自己写（C4 禁代写）。"></textarea>
<p style="margin:4px 0"><button class="btn green">提交资产</button></p></form>""")
        elif t["quiz"]:
            qs, ans = lecture_quiz(doc) if doc else ([], "")
            if not qs:
                h.append("<p><small>（试卷题在教材卷里，本单元试点卷：U1 有 10 题）</small></p>")
            for q in qs:
                rec = pg["quiz"].get(str(q["n"]), {})
                jt = {"": "", "ok": ' <span class="ok">✓</span>', "wrong": ' <span class="bad">✗→入队</span>'}.get(rec.get("judge", ""), "")
                h.append(f"""<div class="q"><span class="tag">{q['type']}</span> <b>{q['n']}.</b> {inline_md(q['text'])}{jt}
<form method="post" action="/unit/{uid}/quiz" style="margin-top:4px"><input type="hidden" name="n" value="{q['n']}"/>
<textarea name="answer" rows="2" placeholder="作答（合上书）">{esc(rec.get("answer",""))}</textarea>
<div style="display:flex;gap:6px;margin-top:4px;flex-wrap:wrap">
<button class="btn">保存</button>
<button class="btn green sm" formaction="/unit/{uid}/quiz/judge" name="self" value="ok">自评 对</button>
<button class="btn red sm" formaction="/unit/{uid}/quiz/judge" name="self" value="wrong">自评 错</button>
</div></form></div>""")
            if ans:
                h.append(f"<details><summary>📄 试卷答案（先做完整张卷再开）</summary><pre style='white-space:pre-wrap'>{esc(ans)}</pre></details>")
        h.append("</div>")

    # —— 4/5/6 + 信封 ——
    owned = pg.get("assets", [])
    alist = "".join(f'<li><a href="/file/{urllib.parse.quote("units/" + d + "/资产/" + a["file"])}" target="_blank">{esc(a["file"])}</a> <small>{esc(a.get("ts",""))}</small></li>'
                    for a in owned) or "<li>还没有资产——在上面的任务区写一件吧</li>"
    steps_done = len(pg.get("steps", {}))
    h.append(f"""<h2>4 · 判卷与入队</h2><div class="card">{md_to_html(sec_body('4'))}
<p><small>阅读进度：{steps_done}/{len(steps)} 站已读</small></p></div>
<h2>5 · 资产槽（{len(owned)} 件）</h2><div class="card"><ul>{alist}</ul></div>
<h2>6 · 时间盒与档位</h2><div class="card">{md_to_html(sec_body('6'))}</div>
<details class="coach" id="envelope"><summary>📮 教练答案信封（先答完再开——偷看 = 21 天补考档）</summary>
{md_to_html(coach_md)}</details>""")
    return page(f"{uid} · 训练场", "\n".join(h), "/")


def review_html():
    due = [it for it in review_all()["items"] if it.get("due", "") <= now()]
    cards = ""
    if not due:
        cards = "<div class='card'>🎉 队列清空。答错/自评错的题会自动进这里（1→3→7→21 天）。</div>"
    for it in due:
        cards += f"""<div class="q"><b>#{it['id']}</b> {esc(it['text'])}
<div style="font-size:12px;color:#6b7280">来源：{esc(it.get('src',''))} · 阶段 {it.get('stage',0)}/4</div>
<form method="post" action="/review/grade" style="margin-top:6px;display:flex;gap:6px">
<input type="hidden" name="id" value="{it['id']}"/>
<button class="btn green sm" name="ok" value="1">记住了（进下一阶段）</button>
<button class="btn red sm" name="ok" value="0">没记住（重置明天）</button></form></div>"""
    allq = len(review_all()["items"])
    body = f"""<h2>复习队列（到期 {len(due)} 张 / 共 {allq} 张 · 1/3/7/21 天）</h2>{cards}
<h2>手动加卡</h2><div class="card"><form method="post" action="/review/add" style="display:flex;gap:8px">
<input type="text" name="text" placeholder="要记住的一个数/一句话/一个词"/><button class="btn">加入队列</button></form></div>"""
    return page("复习队列", body, "/review")


def coach_html():
    pr = progress()
    out = []
    for d in unit_dirs():
        uid = d[:3]
        pg = pr.get(uid, {})
        out.append(f"===== {uid}（{d.split('-',1)[1] if '-' in d else ''}） 状态：{unit_status(uid, pg)}")
        for n, g in sorted(pg.get("gates", {}).items(), key=lambda kv: int(kv[0])):
            out.append(f"闸门{n} [{g.get('judge','未判')}] {g.get('ts','')}")
            out.append(f"  答：{(g.get('answer') or '').strip()[:400]}")
        for o in pg.get("oral", []):
            out.append(f"口述 {o.get('ts','')}：{(o.get('text') or '').strip()[:300]}")
        for n, q in sorted(pg.get("quiz", {}).items(), key=lambda kv: int(kv[0])):
            out.append(f"试卷题{n} [{q.get('judge','未判')}]：{(q.get('answer') or '').strip()[:200]}")
        for a in pg.get("assets", []):
            out.append(f"资产 {a.get('file')} @ {a.get('ts','')}")
        out.append("")
    body = ("<h2>教练快照</h2><p><small>本会话 Agent 每轮开场读这里判卷；判完在对话里给结论并更新记忆。</small></p>"
            f"<pre style='white-space:pre-wrap;font:13px/1.6 ui-monospace,Menlo,monospace'>{esc(chr(10).join(out))}</pre>")
    return page("教练快照", body, "/coach")


# ---------------------------------------------------------------- HTTP
class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _send(self, code, body, ctype="text/html; charset=utf-8"):
        b = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(b)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(b)

    def _form(self):
        ln = int(self.headers.get("Content-Length", 0) or 0)
        if ln <= 0:
            return {}
        raw = self.rfile.read(ln).decode("utf-8", "replace")
        return {k: v for k, v in urllib.parse.parse_qsl(raw, keep_blank_values=True)}

    def _redirect(self, loc):
        self.send_response(303)
        self.send_header("Location", loc)
        self.send_header("Content-Length", "0")
        self.end_headers()

    def do_GET(self):
        u = urllib.parse.urlparse(self.path)
        path = urllib.parse.unquote(u.path)
        if path in ("/", "/index.html"):
            self._send(200, dashboard_html())
        elif path == "/review":
            self._send(200, review_html())
        elif path == "/coach":
            self._send(200, coach_html())
        elif re.match(r"^/unit/u\d{2}$", path):
            self._send(200, unit_html(path[-3:]))
        elif path.startswith("/images/"):
            name = os.path.basename(path[len("/images/"):])
            fp = os.path.join(IMG, name)
            if os.path.isfile(fp):
                with open(fp, "rb") as f:
                    data = f.read()
                ctype = "image/png" if name.endswith(".png") else "image/jpeg"
                self.send_response(200)
                self.send_header("Content-Type", ctype)
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)
            else:
                self._send(404, "图片不存在")
        elif path.startswith("/read/"):
            doc = path[len("/read/"):]
            txt = read_doc(doc)
            self._send(200, page("教材卷 · " + doc, f"<div class='card doc'>{md_to_html(txt, idprefix=doc)}</div>"))
        elif path.startswith("/file/"):
            rel = urllib.parse.unquote(path[len("/file/"):])
            fp = os.path.normpath(os.path.join(ROOT, rel))
            if fp.startswith(ROOT) and os.path.isfile(fp):
                body = "<pre style='white-space:pre-wrap;font:13px/1.7 ui-monospace,monospace;padding:10px'>" + esc(read_or(fp)) + "</pre>"
                self._send(200, page(os.path.basename(fp), f"<div class='card'>{body}</div>"))
            else:
                self._send(404, "无此文件")
        elif path.startswith("/doc/"):
            rel = urllib.parse.unquote(path[len("/doc/"):])
            fp = os.path.normpath(os.path.join(TF, rel))
            if fp.startswith(TF) and os.path.isfile(fp):
                self._send(200, page(os.path.basename(fp), f"<div class='card doc'>{md_to_html(read_or(fp))}</div>"))
            else:
                self._send(404, "无此文档")
        elif path == "/favicon.ico":
            self._send(204, "")
        else:
            self._send(404, "404 Not Found")

    def do_POST(self):
        u = urllib.parse.urlparse(self.path)
        path = urllib.parse.unquote(u.path)
        f = self._form()
        pr = progress()
        m = re.match(r"^/unit/(u\d{2})/gate$", path)
        if m:
            uid = m.group(1)
            n = str(int(f.get("n", 1)))
            v = f.get("v", "")
            pg = unit_prog(uid, pr)
            old = pg["gates"].get(n, {})
            rec = {"answer": f.get("answer", old.get("answer", "")), "ts": now(),
                   "judge": "pending" if v == "pending" else old.get("judge", "")}
            if v == "pending":
                rec["skip"] = True
            pg["gates"][n] = rec
            save_json("progress.json", pr)
            journal(f"{uid} | 闸门 {n} 答案已存" + ("（口头，待教练判）" if v == "pending" else ""))
            self._redirect(f"/unit/{uid}#gate-{n}")
            return
        m = re.match(r"^/unit/(u\d{2})/judge$", path)
        if m:
            uid, n = m.group(1), str(int(f.get("n", 1)))
            v = f.get("v", "")
            pg = unit_prog(uid, pr)
            g = pg["gates"].setdefault(n, {"answer": "", "ts": now()})
            g["judge"] = v if v else g.get("judge", "")
            g["ts"] = now()
            if v == "wrong":
                review_add(f"闸门 {n}（{uid}）重答到能讲清", f"{uid} 闸门{n} 自评错")
            save_json("progress.json", pr)
            journal(f"{uid} | 闸门 {n} 自评 = {v}")
            self._redirect(f"/unit/{uid}#gate-{n}")
            return
        m = re.match(r"^/unit/(u\d{2})/step$", path)
        if m:
            uid, n = m.group(1), f.get("n", "?")
            pg = unit_prog(uid, pr)
            pg["steps"][n] = now()
            save_json("progress.json", pr)
            journal(f"{uid} | 已读 第{n}站")
            self._redirect(f"/unit/{uid}#2")
            return
        m = re.match(r"^/unit/(u\d{2})/oral$", path)
        if m:
            uid = m.group(1)
            pg = unit_prog(uid, pr)
            pg.setdefault("oral", []).append({"text": f.get("text", ""), "ts": now()})
            save_json("progress.json", pr)
            journal(f"{uid} | 口述记录")
            self._redirect(f"/unit/{uid}#3")
            return
        m = re.match(r"^/unit/(u\d{2})/quiz$", path)
        if m:
            uid, n = m.group(1), str(int(f.get("n", 1)))
            pg = unit_prog(uid, pr)
            old = pg["quiz"].get(n, {})
            pg["quiz"][n] = {"answer": f.get("answer", old.get("answer", "")), "judge": old.get("judge", ""), "ts": now()}
            save_json("progress.json", pr)
            journal(f"{uid} | 试卷题 {n} 已答")
            self._redirect(f"/unit/{uid}#3")
            return
        m = re.match(r"^/unit/(u\d{2})/quiz/judge$", path)
        if m:
            uid, n = m.group(1), str(int(f.get("n", 1)))
            selfv = f.get("self", "")
            pg = unit_prog(uid, pr)
            rec = pg["quiz"].setdefault(n, {"answer": "", "ts": now()})
            rec["judge"] = selfv
            if selfv == "wrong":
                review_add(f"试卷题 {n}（{uid}）", f"{uid} 试卷 {n} 自评错")
            save_json("progress.json", pr)
            journal(f"{uid} | 试卷题 {n} 自评 = {selfv}")
            self._redirect(f"/unit/{uid}#3")
            return
        m = re.match(r"^/unit/(u\d{2})/asset$", path)
        if m:
            uid = m.group(1)
            d = next((x for x in unit_dirs() if x.startswith(uid)), None)
            name = (f.get("file") or "").strip()
            if not re.match(r"^[\w\u4e00-\u9fff-]+\.md$", name or ""):
                name = "u00-A1-资产草稿.md" if uid == "u00" else "资产.md"
            if not name.startswith(uid):
                name = f"{uid}-A1-" + name
            pg = unit_prog(uid, pr)
            folder = os.path.join(UNITS, d, "资产")
            os.makedirs(folder, exist_ok=True)
            fp = os.path.join(folder, name)
            body = f.get("body", "")
            head = (body.strip().split("\n")[0] or name)[:60]
            with open(fp, "w", encoding="utf-8") as fo:
                fo.write(f"<!-- {uid} 资产 {name} · 工作台自动落盘 {now()} -->\n\n{body}")
            if not any(a.get("file") == name for a in pg.get("assets", [])):
                pg.setdefault("assets", []).append({"file": name, "ts": now()})
                save_json("progress.json", pr)
                append_ledger(d, name, head)
            journal(f"{uid} | 资产已交：{name}")
            self._redirect(f"/unit/{uid}#5")
            return
        if path == "/review/add":
            txt = f.get("text", "").strip()
            if txt:
                review_add(txt, f.get("src", "手动"))
                journal(f"复习队列 +1：{txt[:40]}")
            self._redirect("/review")
            return
        if path == "/review/grade":
            ok = f.get("ok") == "1"
            if review_grade(int(f.get("id", 0) or 0), ok):
                journal(f"复习卡 #{f.get('id')} {'记住了' if ok else '没记住'}")
            self._redirect("/review")
            return
        if path == "/doubt/add":
            txt = f.get("text", "").strip()
            if txt and append_doubt(txt):
                journal(f"存疑台账 +1：{txt[:40]}")
            self._redirect("/")
            return
        self._send(404, "404")


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8901)
    args = ap.parse_args()
    srv = ThreadingHTTPServer(("0.0.0.0", args.port), Handler)
    print(f"AI 自学工作台已启动 → http://0.0.0.0:{args.port}")
    srv.serve_forever()


if __name__ == "__main__":
    main()
