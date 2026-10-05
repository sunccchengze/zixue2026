#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 mindmap_data.py 编译成一个单文件、全离线、可交互的 HTML 知识地图"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mindmap_data import DATA

HERE = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.join(HERE, "理论力学知识地图.html")

# 继承状态：挂在「待发布」章节下的叶子自动标记为 pending
def inherit(n, st=None):
    if n.get("st"): st = n["st"]
    elif st: n["st"] = st
    for k in n.get("c", []):
        inherit(k, st)
inherit(DATA)

# 统计
def walk(n, acc):
    if "c" in n:
        for k in n["c"]:
            walk(k, acc)
    else:
        acc.append(n)
leaves = []
walk(DATA, leaves)
n_leaf = len(leaves)
n_branch = 0
def cnt(n):
    global n_branch
    if "c" in n:
        n_branch += 1
        for k in n["c"]:
            cnt(k)
cnt(DATA)
top_done = sum(1 for k in DATA["c"] if k.get("st") == "done")
top_pend = sum(1 for k in DATA["c"] if k.get("st") == "pending")

payload = json.dumps(DATA, ensure_ascii=False).replace("</", "<\\/")

HTML = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>理论力学 · 知识地图</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
:root{
  --bg:#0e1117; --bg2:#161b22; --bg3:#1c2230; --line:#2a3140;
  --fg:#e6edf3; --fg2:#9aa7b8; --fg3:#6e7d92;
  --acc:#2f6fed; --pur:#7c5cff; --grn:#00a86b; --org:#e8590c; --red:#e5484d; --yel:#d9a300;
}
html,body{height:100%}
body{
  background:var(--bg);color:var(--fg);
  font:15px/1.7 -apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif;
  display:flex;flex-direction:column;overflow:hidden;
}
/* ---------- header ---------- */
header{
  padding:16px 22px;background:linear-gradient(100deg,#161b22 0%,#1a2338 55%,#20182e 100%);
  border-bottom:1px solid var(--line);flex:none;
}
.h1{display:flex;align-items:baseline;gap:14px;flex-wrap:wrap}
h1{font-size:21px;font-weight:700;letter-spacing:.5px}
h1 .em{background:linear-gradient(92deg,#4d8bff,#a78bfa);-webkit-background-clip:text;background-clip:text;color:transparent}
.sub{font-size:12.5px;color:var(--fg2);margin-top:5px;line-height:1.6}
.stats{display:flex;gap:8px;margin-top:12px;flex-wrap:wrap}
.stat{background:var(--bg3);border:1px solid var(--line);border-radius:7px;padding:5px 11px;font-size:12px;color:var(--fg2)}
.stat b{color:var(--fg);font-size:13.5px;font-weight:650}
/* ---------- toolbar ---------- */
.bar{
  display:flex;gap:9px;align-items:center;padding:10px 22px;
  background:var(--bg2);border-bottom:1px solid var(--line);flex:none;flex-wrap:wrap;
}
#q{
  flex:1;min-width:190px;background:var(--bg);border:1px solid var(--line);color:var(--fg);
  padding:7px 12px;border-radius:7px;font-size:13.5px;outline:none;font-family:inherit;
}
#q:focus{border-color:var(--acc);box-shadow:0 0 0 3px rgba(47,111,237,.16)}
#q::placeholder{color:var(--fg3)}
.btn{
  background:var(--bg3);border:1px solid var(--line);color:var(--fg2);
  padding:7px 13px;border-radius:7px;font-size:12.5px;cursor:pointer;
  font-family:inherit;transition:.15s;white-space:nowrap;
}
.btn:hover{background:#232b3a;color:var(--fg);border-color:#3a4456}
.btn.on{background:var(--acc);border-color:var(--acc);color:#fff}
/* ---------- layout ---------- */
main{flex:1;display:flex;min-height:0}
#tree{
  width:355px;flex:none;overflow-y:auto;padding:12px 10px 40px;
  border-right:1px solid var(--line);background:var(--bg2);
}
#detail{flex:1;overflow-y:auto;padding:26px 34px 60px}
#tree::-webkit-scrollbar,#detail::-webkit-scrollbar{width:9px}
#tree::-webkit-scrollbar-thumb,#detail::-webkit-scrollbar-thumb{background:#2c3444;border-radius:5px}
#tree::-webkit-scrollbar-track,#detail::-webkit-scrollbar-track{background:transparent}
/* ---------- tree ---------- */
.nd{user-select:none}
.row{
  display:flex;align-items:flex-start;gap:7px;padding:5px 8px;border-radius:6px;
  cursor:pointer;font-size:13.5px;line-height:1.5;transition:.1s;
}
.row:hover{background:#212838}
.row.sel{background:rgba(47,111,237,.19);box-shadow:inset 2px 0 0 var(--acc)}
.row.hit{background:rgba(217,163,0,.15)}
.arw{
  width:14px;flex:none;color:var(--fg3);font-size:9px;text-align:center;
  transition:transform .16s;margin-top:5px;
}
.arw.op{transform:rotate(90deg)}
.arw.leaf{opacity:0}
.dot{width:7px;height:7px;border-radius:50%;flex:none;margin-top:8px}
.nm{flex:1;word-break:break-word}
.nm.pend{color:var(--fg3);font-style:italic}
.cnt2{font-size:10.5px;color:var(--fg3);background:var(--bg);border:1px solid var(--line);
      border-radius:9px;padding:0 6px;margin-top:3px;flex:none}
.kids{margin-left:15px;border-left:1px dashed #2b3342;padding-left:7px;display:none}
.kids.op{display:block}
.top{margin-bottom:3px}
.top>.row{font-size:14.5px;font-weight:600}
/* ---------- detail ---------- */
.ph{color:var(--fg3);text-align:center;margin-top:90px;font-size:14px;line-height:2.1}
.ph .big{font-size:40px;display:block;margin-bottom:12px;opacity:.55}
.crumb{font-size:12px;color:var(--fg3);margin-bottom:9px}
.crumb span{color:var(--acc)}
h2.dt{font-size:22px;font-weight:700;margin-bottom:5px;line-height:1.4}
.tags{display:flex;gap:7px;flex-wrap:wrap;margin-bottom:18px}
.tag{font-size:11.5px;padding:2px 9px;border-radius:20px;border:1px solid;font-weight:600}
.t-概念{color:#5aa9ff;border-color:#25507d;background:rgba(47,111,237,.13)}
.t-公式{color:#b39bff;border-color:#4b3d8f;background:rgba(124,92,255,.13)}
.t-方法{color:#3ddb9b;border-color:#1d6b4f;background:rgba(0,168,107,.13)}
.t-易错{color:#ff7b7f;border-color:#7d2b2e;background:rgba(229,72,77,.13)}
.t-概念0{color:#5aa9ff;border-color:#25507d;background:rgba(47,111,237,.13)}
.card{background:var(--bg2);border:1px solid var(--line);border-radius:11px;padding:15px 18px;margin-bottom:13px}
.card h3{font-size:11.5px;font-weight:700;letter-spacing:1.3px;margin-bottom:9px;text-transform:uppercase}
.c-d h3{color:#5aa9ff} .c-f h3{color:#b39bff} .c-w h3{color:#ff7b7f}
.c-d,.c-f{font-size:14.5px;line-height:1.85;color:#dbe4ee}
.c-d b,.c-f b{color:#fff;font-weight:650}
.c-d u{text-decoration-color:#5aa9ff;text-underline-offset:2px}
.c-w{font-size:14px;line-height:1.8;color:#ffd0d1}
.c-w b{color:#ff9a9d}
.fml{
  font-family:"Cambria Math","Latin Modern Math","STIX Two Math",Georgia,"Times New Roman",serif;
  font-size:16.5px;line-height:2.15;background:var(--bg);border:1px solid var(--line);
  border-left:3px solid var(--pur);border-radius:8px;padding:13px 17px;color:#e8e2ff;
  overflow-x:auto;
}
.fml br{line-height:2.15}
.fml sub{font-size:.68em} .fml sup{font-size:.68em}
.src{
  font-size:12.5px;color:var(--fg2);display:flex;align-items:center;gap:8px;
  padding:9px 14px;background:rgba(0,168,107,.07);border:1px solid rgba(0,168,107,.25);
  border-radius:8px;margin-top:3px;
}
.src .ic{color:var(--grn);font-weight:700}
.pill{
  display:inline-block;font-size:11.5px;padding:2px 10px;border-radius:20px;
  background:rgba(217,163,0,.14);border:1px solid rgba(217,163,0,.4);color:#f0c33c;font-weight:600;
}
.note{
  background:linear-gradient(96deg,rgba(47,111,237,.11),rgba(124,92,255,.07));
  border:1px solid rgba(47,111,237,.26);border-radius:9px;padding:11px 16px;
  font-size:13.5px;color:#b9c7db;margin-bottom:15px;
}
.note b{color:#8fb8ff}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(215px,1fr));gap:11px;margin-bottom:16px}
.gc{background:var(--bg2);border:1px solid var(--line);border-radius:10px;padding:13px 15px;font-size:13.5px}
.gc .gn{font-weight:650;margin-bottom:5px}
.gc .gd{font-size:12.5px;color:var(--fg2);line-height:1.65}
.gc .gd.pend{color:var(--fg3);font-style:italic}
.nomatch{padding:30px 8px;color:var(--fg3);font-size:13px;text-align:center}
@media(max-width:820px){
  main{flex-direction:column}
  #tree{width:100%;height:46%;border-right:none;border-bottom:1px solid var(--line)}
  #detail{padding:18px}
}
</style>
</head>
<body>

<header>
  <div class="h1">
    <h1><span class="em">理论力学</span> · 交互式知识地图</h1>
  </div>
  <div class="sub">__META__</div>
  <div class="stats">
    <div class="stat">章节 <b>__NC__</b></div>
    <div class="stat">知识点 <b>__NL__</b></div>
    <div class="stat">已发布 <b style="color:#3ddb9b">__ND__</b></div>
    <div class="stat">待发布 <b style="color:#f0c33c">__NP__</b></div>
    <div class="stat">讲义 <b>23</b> 份 / <b>339</b> 页</div>
  </div>
</header>

<div class="bar">
  <input id="q" placeholder="搜索知识点、公式、易错点…（如：科氏、自锁、桁架、动量）">
  <button class="btn" id="bAll">全部</button>
  <button class="btn" id="bDone">已发布</button>
  <button class="btn" id="bPend">待发布</button>
  <button class="btn" id="bExp">展开全部</button>
  <button class="btn" id="bCol">折叠全部</button>
</div>

<main>
  <nav id="tree"></nav>
  <section id="detail">
    <div class="ph"><span class="big">🗺️</span>
      左侧点开任意节点查看内容<br>顶部搜索框可全文检索知识点<br><br>
      <span style="font-size:12.5px">
        🟢 静力学　🔵 运动学　🟠 动力学　　虚线 = 讲义尚未发布
      </span>
    </div>
  </section>
</main>

<script>
const DATA = __PAYLOAD__;
const $ = s => document.querySelector(s);
const esc = s => String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');

/* ---------- 构建树 ---------- */
const tree = $('#tree');
let uid = 0;
let FLAT = [];          // {node, el, row, parentId, depth}
let mode = 'all';       // all | done | pending
let query = '';

function build(node, host, depth, parentId, chain){
  const id = ++uid;
  const isBranch = Array.isArray(node.c);
  const wrap = document.createElement('div');
  wrap.className = 'nd' + (depth === 1 ? ' top' : '');

  const row = document.createElement('div');
  row.className = 'row';
  const col = node.color || (node.st === 'pending' ? '#6e7d92' : (isBranch ? '#8fa3bf' : '#4a9eff'));

  let arw = '<div class="arw' + (isBranch ? '' : ' leaf') + '">▶</div>';
  let cntBadge = isBranch ? '<div class="cnt2">' + countLeaves(node) + '</div>' : '';
  row.innerHTML = arw
    + '<div class="dot" style="background:' + col + '"></div>'
    + '<div class="nm' + (node.st === 'pending' ? ' pend' : '') + '">' + esc(node.n) + '</div>'
    + cntBadge;
  wrap.appendChild(row);

  const kids = document.createElement('div');
  kids.className = 'kids';
  if (isBranch){
    const ch = chain.concat([node.n]);
    node.c.forEach(k => build(k, kids, depth + 1, id, ch));
    wrap.appendChild(kids);
  }
  host.appendChild(wrap);

  FLAT.push({node, el: wrap, row, kids, parentId, depth, chain, id, isBranch});

  row.onclick = e => {
    e.stopPropagation();
    if (isBranch){
      kids.classList.toggle('op');
      row.querySelector('.arw').classList.toggle('op');
    }
    document.querySelectorAll('.row.sel').forEach(r => r.classList.remove('sel'));
    row.classList.add('sel');
    render(node, chain);
  };
  return id;
}

function countLeaves(n){
  if (!Array.isArray(n.c)) return 0;
  let t = 0;
  n.c.forEach(k => { t += Array.isArray(k.c) ? countLeaves(k) : 1; });
  return t;
}

function lineageOf(targetId){
  const byId = {};
  FLAT.forEach(f => byId[f.id] = f);
  const out = [];
  let cur = byId[targetId];
  while (cur){ out.unshift(cur); cur = byId[cur.parentId]; }
  return out;
}
function openAncestors(targetId){
  lineageOf(targetId).forEach(f => {
    if (f.isBranch){
      f.kids.classList.add('op');
      const a = f.row.querySelector('.arw');
      if (a) a.classList.add('op');
    }
  });
}

/* ---------- 详情面板 ---------- */
function render(n, chain){
  const d = $('#detail');
  if (Array.isArray(n.c)){
    const kids = n.c;
    const cards = kids.map(k => {
      const t = k.t ? '<span class="tag t-' + k.t + '">' + k.t + '</span>' : '';
      const dd = k.d ? '<div class="gd' + (k.st === 'pending' ? ' pend' : '') + '">' + k.d + '</div>'
                     : '<div class="gd pend">共 ' + countLeaves(k) + ' 个知识点</div>';
      return '<div class="gc"><div class="gn">' + esc(k.n) + ' ' + t + '</div>' + dd + '</div>';
    }).join('');
    d.innerHTML =
      '<div class="crumb">' + chain.concat([n.n]).map(x => '<span>' + esc(x) + '</span>').join(' › ') + '</div>'
      + '<h2 class="dt">' + esc(n.n) + '</h2>'
      + (n.st === 'pending' ? '<div style="margin:12px 0 4px"><span class="pill">📅 讲义尚未发布 · 按课程大纲预告</span></div>' : '')
      + (n.note ? '<div class="note">💡 ' + n.note + '</div>' : '')
      + '<div class="grid">' + cards + '</div>';
    return;
  }
  let h = '<div class="crumb">' + chain.map(x => '<span>' + esc(x) + '</span>').join(' › ') + '</div>'
        + '<h2 class="dt">' + esc(n.n) + '</h2>';
  const tags = [];
  if (n.t) tags.push('<span class="tag t-' + n.t + '">' + n.t + '</span>');
  if (n.st === 'pending') tags.push('<span class="pill">📅 待发布</span>');
  if (tags.length) h += '<div class="tags">' + tags.join('') + '</div>';
  if (n.d) h += '<div class="card c-d"><h3>要点</h3>' + n.d + '</div>';
  if (n.f) h += '<div class="card c-f"><h3>公式</h3><div class="fml">' + n.f + '</div></div>';
  if (n.w) h += '<div class="card c-w"><h3>⚠ 易错点</h3>' + n.w + '</div>';
  if (n.s) h += '<div class="src"><span class="ic">📄</span> 出处：' + esc(n.s) + '</div>';
  d.innerHTML = h;
  d.scrollTop = 0;
}

/* ---------- 过滤 / 搜索 ---------- */
function modeOK(n){
  if (mode === 'done')    return n.st !== 'pending';
  if (mode === 'pending') return n.st === 'pending';
  return true;
}
function matches(n){
  if (!modeOK(n)) return false;
  if (!query) return true;
  const blob = (n.n + ' ' + (n.d || '') + ' ' + (n.f || '') + ' ' + (n.w || '') + ' ' + (n.s || '')).toLowerCase();
  return blob.indexOf(query) >= 0;
}
function apply(){
  const selfM = new Map(), subM = new Map(), vis = new Map();
  FLAT.forEach(f => selfM.set(f.id, matches(f.node)));

  // 自底向上：自身命中 或 任一后代命中
  function sub(id){
    if (subM.has(id)) return subM.get(id);
    let v = selfM.get(id);
    FLAT.filter(g => g.parentId === id).forEach(g => { if (sub(g.id)) v = true; });
    subM.set(id, v); return v;
  }
  FLAT.forEach(f => sub(f.id));

  // 自顶向下：祖先命中 → 后代一并显示
  function v(id, parentVisible){
    const val = subM.get(id) || parentVisible;
    vis.set(id, val);
    FLAT.filter(g => g.parentId === id).forEach(g => v(g.id, val));
  }
  FLAT.filter(f => f.parentId === 0).forEach(f => v(f.id, false));

  FLAT.forEach(f => {
    f.el.style.display = vis.get(f.id) ? '' : 'none';
    f.row.classList.toggle('hit', !!query && selfM.get(f.id) && !f.isBranch);
  });

  if (query) FLAT.filter(f => selfM.get(f.id)).forEach(f => openAncestors(f.id));

  const n = FLAT.filter(f => vis.get(f.id) && !f.isBranch).length;
  let t = $('#hitTip');
  if (query){
    if (!t){ t = document.createElement('div'); t.id = 'hitTip'; t.className = 'nomatch'; tree.insertBefore(t, tree.firstChild); }
    t.textContent = n ? '🔍 匹配到 ' + n + ' 个知识点' : '🔍 没有匹配的知识点';
  } else if (t) t.remove();
}

/* ---------- 事件 ---------- */
let timer;
$('#q').oninput = e => { clearTimeout(timer); timer = setTimeout(() => { query = e.target.value.trim().toLowerCase(); apply(); }, 140); };
function setMode(m){
  mode = m;
  $('#bAll').classList.toggle('on', m === 'all');
  $('#bDone').classList.toggle('on', m === 'done');
  $('#bPend').classList.toggle('on', m === 'pending');
  apply();
}
$('#bAll').onclick  = () => setMode('all');
$('#bDone').onclick = () => setMode('done');
$('#bPend').onclick = () => setMode('pending');
$('#bExp').onclick  = () => FLAT.forEach(f => { if (f.isBranch){ f.kids.classList.add('op'); const a = f.row.querySelector('.arw'); if (a) a.classList.add('op'); } });
$('#bCol').onclick  = () => FLAT.forEach(f => { if (f.isBranch && f.depth > 1){ f.kids.classList.remove('op'); const a = f.row.querySelector('.arw'); if (a) a.classList.remove('op'); } });

/* ---------- init ---------- */
DATA.c.forEach(k => build(k, tree, 1, 0, []));
// 默认展开第一层
FLAT.filter(f => f.depth === 1).forEach(f => { f.kids.classList.add('op'); const a = f.row.querySelector('.arw'); if (a) a.classList.add('op'); });
render(DATA, []);
</script>
</body>
</html>"""

HTML = (HTML
    .replace("__META__", DATA["meta"])
    .replace("__PAYLOAD__", payload)
    .replace("__NC__", str(len(DATA["c"])))
    .replace("__NL__", str(n_leaf))
    .replace("__ND__", str(top_done))
    .replace("__NP__", str(top_pend)))

open(OUT, "w", encoding="utf-8").write(HTML)
print(f"✅ {OUT}")
print(f"   章节 {len(DATA['c'])} | 知识点叶子 {n_leaf} | 分支节点 {n_branch}")
print(f"   已发布章节 {top_done} | 待发布章节 {top_pend} | 大小 {os.path.getsize(OUT)/1024:.1f} KB")
