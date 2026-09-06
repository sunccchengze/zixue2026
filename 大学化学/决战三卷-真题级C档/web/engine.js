/* 决战三卷 · 答题引擎 —— Apple design-md 风格（SF Pro 系 / Action Blue #0066cc / pill & 18px 圆角） */
(function () {
  'use strict';
  const params = new URLSearchParams(location.search);
  const pid = (params.get('p') || '1');
  const P = DATA.papers.find(x => x.id === pid) || DATA.papers[0];
  const LS = 'chem-arena-' + P.id;
  const MINUTES = 120;

  /* ---------- 规范化与判分 ---------- */
  const SUP = { '⁰':'0','¹':'1','²':'2','³':'3','⁴':'4','⁵':'5','⁶':'6','⁷':'7','⁸':'8','⁹':'9','ⁿ':'n','⁻':'-','⁺':'+','⁻':'-',
                '₀':'0','₁':'1','₂':'2','₃':'3','₄':'4','₅':'5','₆':'6','₇':'7','₈':'8','₉':'9' };
  function norm(s) {
    if (s == null) return '';
    s = String(s);
    for (const k in SUP) s = s.split(k).join(SUP[k]);
    s = s.replace(/[()（）\[\]【】]/g, m => '()（）【】'.includes(m) ? m : m)
         .replace(/（/g,'(').replace(/）/g,')').replace(/【/g,'[').replace(/】/g,']')
         .replace(/[。，、；：]/g, m => ({'。':'.','，':',','、':',','；':';','：':':'}[m]))
         .replace(/−/g,'-').replace(/×/g,'x').replace(/·/g,'.').replace(/℃/g,'度')
         .replace(/\s+/g,'').toLowerCase();
    return s;
  }
  function judge(input, rule) {
    const v = norm(input);
    if (!v) return false;
    const rules = (Array.isArray(rule) && Array.isArray(rule[0])) ? rule : [rule]; // 单规则或多规则OR
    for (const r of rules) {
      if (r[0] === 'set') { if (r[1].some(a => norm(a) === v)) return true; }
      else if (r[0] === 'has') { if (r[1].every(tok => v.includes(norm(tok)))) return true; }
      else if (r[0] === 'any') { if (r[1].some(tok => v.includes(norm(tok)))) return true; }
      else if (r[0] === 'num') { const f = parseFloat(v.replace(/[^0-9.eE+\-]/g,'')); const tgt=r[1][0], tol=(r[1][2]??0.02); if (isFinite(f) && Math.abs(f-tgt) <= Math.max(Math.abs(tgt)*tol, Math.abs(tol))) return true; }
    }
    return false;
  }

  /* ---------- 填空接受表（parse 自命题文件的每空清单，经人工矫正） ---------- */
  const FK = {
   '1': {1:[['set',['四','4','第四','第四周期']],['set',['Ⅷ','viii','8','八','第八','第8副族']],['set',['3d64s2','[ar]3d64s2','1s22s22p63s23p63d64s2']],['set',['d','d区']],['set',['金属晶体','金属']]],
         2:[['set',['sc','钪']],['num',[21,21,0]],['set',['iiib','ⅲb','3b','第三副族','Ⅲb']],['set',['d','d区']]],
         3:[['set',['cu2+','cu(ii)','铜离子','cu']],['set',['nh3','氨','氨分子']],['set',['n','氮']],['set',['平面四方','平面正方形','平面四方形','dsp2']],['any',['四氨合铜']]],
         4:[['set',['2.5']],['set',['2','2.0']],['set',['1.5']],['set',['o2-','o2⁻']],['any',['顺磁','未成对']]],
         5:[['set',['色散','色散力','范德华力','伦敦力']],[['any',['全都有','全部','四种都有','取向力、诱导力、色散力和氢键']],['has',['取向','诱导','色散','氢键']]],['set',['色散','色散力','范德华力']]],
         6:[['set',['-90','-90kj']],['set',['不能','否','不可']],['any',['物质的量','摩尔数','Δn','dn','恒压','信息不足','无法确定','缺少','题给信息']]],
         7:[['set',['h2o(l)','h2o(l)','水','液态水']],['set',['co2(g)','co2','二氧化碳']],['set',['h2o(l)','h2o','水','液态水']],['set',['so2(g)','so2','二氧化硫']]],
         8:[['set',['小','变小','减小','降低','缩小']],['set',['负','-','负号']]],
         9:[['has',['5s','4d','5p']],['set',['18','十八']],['set',['xe','氙']]],
         10:[['set',['agbr','溴化银']],['set',['nacl','氯化钠']],['any',['不等性']]] },
   '2': {1:[['set',['fe','铁']],['set',['3d64s2']],['num',[26,26,0]],['set',['4s']]],
         2:[['any',['4s3','4s^3','4s³']],['set',['3.2e-11','3.2x10-11','3.2x10^-11','3.2e−11']]],
         3:[['num',[0.744,0.744,0.03]],['num',[1.67,1.67,0.03]],['any',['离子缔合','活度','缔合','离子对','不完全']]],
         4:[['set',['2.2e6','2.2x106','2.2x10^6','2.2e+06','2190000','2.17e6']],['set',['很大','完全','极大','基本完全','进行完全','几乎完全']]],
         5:[['set',['减小','降低','变小','下降']],['any',['微增','略增','基本不变']]],
         6:[['set',['1']],['set',['pka','pka值','pka','ka的负对数']],['set',['1','±1']]],
         7:[['set',['h2o','水']],['set',['h2s','硫化氢']],['any',['氢键']]],
         8:[['num',[23,23,0.03]],['set',['1e10','1.0e10','1x1010','1.0x1010','10^10','1x10^10','1.0x10^10','1e+10','约10^10']]],
         9:[['has',['h2o','h2']],['has',['cl','cl2']]],
         10:[['any',['粒子数','质点数','溶质粒子','浓度']],['any',['本性','种类','性质']]] },
   '3': {1:[['any',['>','正','+']],['any',['>','正','+']],['any',['<','负','-']],['set',['是']]],
         2:[['set',['>','大于']],['set',['>','大于']],['any',['非键','成键','口径','重叠']]],
         3:[['set',['等性','等性sp3']],['set',['不等性','不等性sp3']],['any',['孤对','孤电子']]],
         4:[['any',['ksp']],['set',['3.5e14','3.5x1014','3.5e+14','3.5x10^14']],['set',['完全','极大','很大','基本完全','趋势很大']]],
         5:[['set',['浓','浓侧','浓度大','高浓度','浓的一']],['has',['ag','e']]],
         6:[['set',['酸','酸性']],['set',['碱','碱性']],['has',['nh4','h']]],
         7:[['set',['3','三']],['set',['抗磁','反磁','抗磁性','反磁性','抗（反）磁']],['set',['短于','短','小于','更短']]],
         8:[['any',['>','正','+']],['any',['<','负','-']],['any',['<','负','-']]],
         9:[['num',[20,20,0.02]],['num',[5,5,0.05]]],
         10:[['any',['br2(g)','br2(g)','气态溴','溴蒸气','溴气']],['any',['金刚石']]] }
  };

  /* ---------- 状态 ---------- */
  const saved = JSON.parse(localStorage.getItem(LS) || 'null');
  const state = saved || { mc:{}, fill:{}, just:{}, calcFlags:{}, start:Date.now(), elapsed:0, submitted:false, practice:false };
  const save = () => localStorage.setItem(LS, JSON.stringify(state));
  const $ = s => document.querySelector(s);
  const el = (t,c,h)=>{const e=document.createElement(t); if(c)e.className=c; if(h!=null)e.innerHTML=h; return e};
  const cem = s => s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/\*\*(.+?)\*\*/g,'<b>$1</b>').replace(/\n/g,'<br>');

  /* ---------- 计时 ---------- */
  let timer;
  function tick() {
    const now = state.submitted ? state.finalEnd : Date.now();
    const t = state.elapsed + Math.floor((now - state.start)/1000);
    const remain = MINUTES*60 - t; const m = Math.abs(Math.floor(remain/60)), s2 = Math.abs(remain%60);
    const e = $('#timer'); if (!e) return;
    e.textContent = (remain<0?'超时 ':'⏱ ')+String(m).padStart(2,'0')+':'+String(s2).padStart(2,'0');
    e.className = 'timer' + (remain<0 ? ' over' : remain<600 ? ' warn' : '');
  }

  /* ---------- 渲染 ---------- */
  function render() {
    document.title = P.title + ' · 决战三卷';
    const app = $('#app');
    app.append(el('div','hero',
      `<div class="kicker">C 档真题级 · 自动判分</div><h1>${P.title}</h1><p class="sub">${P.subtitle}</p>
       <p class="meta">选择 20×2 ＝ 40 · 填空 10×2 ＝ 20 · 计算 5×8 ＝ 40（纸面自评）· 满分 100 · 限时 ${MINUTES} 分钟</p>`));

    // 选择
    const s1 = el('section'); s1.append(el('h2',null,'一、选择题'));
    P.mc.forEach(q => {
      const card = el('div','card q'); card.id='mc'+q.num;
      card.append(el('div','qhead',`${q.num}. <span class="tag">${cem(q.tag)}</span>`));
      card.append(el('div','stem',cem(q.stem)));
      const kbd = el('div','opts');
      [...'ABCD'].forEach((L,i) => {
        const o = el('button','opt'); o.dataset.k = L;
        o.innerHTML = `<span class="lt">${L}</span><span>${cem(q.options[i])}</span>`;
        if (state.mc[q.num] === L) o.classList.add('sel');
        o.onclick = () => { if (state.submitted) return; state.mc[q.num]=L; save();
          card.querySelectorAll('.opt').forEach(b=>b.classList.remove('sel')); o.classList.add('sel');
          if (state.practice) markMC(q, card); updateNav(); };
        kbd.append(o);
      });
      card.append(kbd);
      card.append(el('div','fb'));
      s1.append(card);
    });
    app.append(s1);

    // 填空
    const s2 = el('section'); s2.append(el('h2',null,'二、填空题 <span class="hint">（多空题按顺序逐空填；支持 10⁻⁵ / 10^-5 / 1e-5 等写法）</span>'));
    P.fill.forEach(q => {
      const card = el('div','card q'); card.id='fl'+q.num;
      card.append(el('div','qhead',`${q.num}. <span class="tag">${cem(q.tag)}</span>`));
      card.append(el('div','stem',cem(q.stem)));
      const row = el('div','blanks');
      for (let i=0;i<q.nblanks;i++) {
        const w = el('div','blankw');
        const lab = el('label',null,`空 ${i+1}`);
        const inp = el('input','blank'); inp.type='text'; inp.autocomplete='off';
        inp.dataset.q = q.num; inp.dataset.b = i;
        inp.value = (state.fill[q.num]||[])[i] || '';
        inp.oninput = () => { (state.fill[q.num] = state.fill[q.num]||[])[i] = inp.value; save(); updateNav(); };
        inp.onfocus = () => kb.show(inp);
        w.append(lab); w.append(inp); row.append(w);
      }
      card.append(row);
      // 判分后显示接受样例
      card.append(el('div','fb'));
      s2.append(card);
    });
    app.append(s2);

    // 计算
    const s3 = el('section'); s3.append(el('h2',null,'三、计算题 <span class="hint">（纸面作答 → 交卷后展开解析，按采分点自评）</span>'));
    P.calc.forEach(q => {
      const card = el('div','card q calc'); card.id='ca'+q.num;
      card.append(el('div','qhead',`算 ${q.num} <span class="tag">${cem(q.tag)}</span> <span class="pts">8 分</span>`));
      card.append(el('div','stem',cem(q.stem)));
      const sol = el('details','sol'); sol.innerHTML = `<summary>交卷后点我：标准解与采分点</summary><div class="solbody">${cem(q.sol||'(解析缺失)')}</div>`;
      if (!state.submitted) sol.querySelector('summary').style.opacity=.4;
      card.append(sol);
      const self = el('div','selfrate');
      self.innerHTML = `<span>自评（交卷后填，0–8 分）：</span>`;
      for (let v=0; v<=8; v+=1) { const b=el('button','pillmini',String(v)); if((state.calcFlags||{})[q.num]===v) b.classList.add('sel');
        b.onclick=()=>{ if(!state.submitted) return; (state.calcFlags=state.calcFlags||{})[q.num]=v; save();
          self.querySelectorAll('.pillmini').forEach(x=>x.classList.remove('sel')); b.classList.add('sel'); renderReport(); };
        self.append(b); }
      card.append(self);
      s3.append(card);
    });
    app.append(s3);

    // 判分按钮
    const actions = el('div','dock');
    const practice = el('label','switch',`<input type="checkbox" id="practice" ${state.practice?'checked':''}> 练习模式（即点即判）`);
    const sub = el('button','primary', state.submitted ? '已交卷 · 查看报告' : '交卷判分');
    sub.id='submitBtn';
    sub.onclick = state.submitted ? ()=> $('#report').scrollIntoView({behavior:'smooth'}) : submit;
    const clr = el('button','ghost','清空重答');
    clr.onclick = () => { if (confirm('清空本卷全部作答并重置计时？')){ localStorage.removeItem(LS); location.reload(); } };
    actions.append(practice); actions.append(sub); actions.append(clr);
    app.append(actions);
    $('#practice').onchange = e => { state.practice = e.target.checked; save(); };

    renderReport();
    updateNav();
  }

  /* ---------- 判分 ---------- */
  function markMC(q, card) {
    [...'ABCD'].forEach((L,i) => {
      const b = card.querySelectorAll('.opt')[i];
      b.classList.toggle('ok', L === q.ans);
      b.classList.toggle('bad', state.mc[q.num] === L && L !== q.ans);
    });
    const fb = card.querySelector('.fb');
    fb.className = 'fb show';
    fb.innerHTML = `<b>答案 ${q.ans}</b> · 档位 ${q.level}${q.trap?' · 坑法 '+q.trap:''}<br>${cem(q.expl)}`;
  }
  function markFill(q, card) {
    const rules = FK[P.id][q.num] || [];
    const vals = state.fill[q.num] || [];
    let okAll = true, detail = [];
    card.querySelectorAll('.blank').forEach((inp, i) => {
      const ok = rules[i] ? judge(vals[i], rules[i]) : false;
      inp.classList.toggle('ok', ok); inp.classList.toggle('bad', !ok);
      if (!ok) okAll = false;
      detail.push(ok ? '✓' : '✗');
    });
    q._ok = okAll && (vals.filter(v=>v&&v.trim()).length>=q.nblanks);
    const fb = card.querySelector('.fb');
    fb.className = 'fb show';
    const sample = (q.rawans||'').replace(/\[(.*?)\]/g,'$1').split(/；|;/).map(s=>s.trim()).filter(Boolean).slice(0, q.nblanks).join(' ｜ ');
    fb.innerHTML = `<b>${detail.join(' ')}</b>　参考答案：<b>${cem(sample||'(见解析册)')}</b>`;
  }
  function scoreAll() {
    let mcS = 0, mcDet = {}, fillS = 0, fillDet = {}, cList = [];
    P.mc.forEach(q => {
      const ok = state.mc[q.num] === q.ans;
      if (ok) mcS += 2; mcDet[q.num] = {yours: state.mc[q.num]||'—', ans: q.ans, ok};
      if ((q.level||'').startsWith('C')) cList.push({id:'选'+q.num, ok, tag:q.tag, trap:q.trap, level:q.level});
    });
    P.fill.forEach(q => {
      const ok = !!q._ok; if (ok) fillS += 2; fillDet[q.num] = {ok, tag:q.tag};
      cList.push({id:'填'+q.num, ok, tag:q.tag, level:'B+'});
    });
    const calcS = Object.values(state.calcFlags||{}).reduce((a,b)=>a+(b||0),0);
    return {mcS, mcDet, fillS, fillDet, calcS, cList, total: mcS+fillS+calcS};
  }
  function submit() {
    if (state.submitted) return;
    if (!confirm('确定交卷？交卷后展示全部答案与解析，并可自评计算题。')) return;
    state.submitted = true; state.finalEnd = Date.now(); save();
    P.mc.forEach(q => markMC(q, $('#mc'+q.num)));
    P.fill.forEach(q => markFill(q, $('#fl'+q.num)));
    document.querySelectorAll('.sol summary').forEach(x=>x.style.opacity=1);
    $('#submitBtn').textContent='已交卷 · 查看报告';
    renderReport(); $('#report')?.scrollIntoView?.({behavior:'smooth'});
  }

  /* ---------- 报告 ---------- */
  function renderReport() {
    let box = $('#report'); if (!box) { box = el('section','reportwrap'); box.id='report'; $('#app').append(box); }
    if (!state.submitted) { box.innerHTML=''; return; }
    const R = scoreAll();
    const cOK = R.cList.filter(c=>c.ok).length, cRate = R.cList.length ? Math.round(cOK/R.cList.length*100) : 0;
    const wrong = [
      ...P.mc.filter(q=>!R.mcDet[q.num].ok).map(q=>`选${q.num}（${q.tag}${q.trap?' · '+q.trap:''}）：你选 ${R.mcDet[q.num].yours}，正确 ${q.ans}`),
      ...P.fill.filter(q=>!R.fillDet[q.num].ok).map(q=>`填${q.num}（${q.tag}）`),
    ];
    const md = buildMD(R, cRate, wrong);
    box.innerHTML = `
      <div class="repcard">
        <div class="kicker">成绩单 · 判例⑯口径</div>
        <h2>${R.total}<span class="of100">/100</span></h2>
        <div class="bars">
          <div class="bar"><span>选择 ${R.mcS}/40</span></div>
          <div class="bar"><span>填空 ${R.fillS}/20</span></div>
          <div class="bar"><span>计算（自评待复核）${R.calcS}/40</span></div>
        </div>
        <p class="crate ${cRate>=70?'pass':'fail'}">C 档水位题正确率：<b>${cRate}%</b>（及格线 70%）</p>
        <h3>${wrong.length?'错题清单（按此去账本定点复活卡片）':'客观题全对——漂亮的仗'}</h3>
        ${wrong.length?'<ol class="wrong">'+wrong.map(w=>`<li>${cem(w)}</li>`).join('')+'</ol>':''}
        <p class="hint">注意：计算题为自评分，按判例⑯仍须把纸面过程拍照给导师复核后才算数。</p>
        <div class="actions"><button class="primary" id="cp">复制 Markdown 报告</button>
        <button class="ghost" id="dl">下载 report.md</button></div>
      </div>`;
    $('#cp').onclick = () => { navigator.clipboard.writeText(md).then(()=>$('#cp').textContent='已复制 ✓'); };
    $('#dl').onclick = () => { const b=new Blob([md],{type:'text/markdown'}); const a=el('a'); a.href=URL.createObjectURL(b); a.download=`${P.slug}-report.md`; a.click(); };
  }
  function buildMD(R, cRate, wrong) {
    const t = Math.floor(((state.finalEnd||Date.now()) - state.start + (state.elapsed||0)*1000)/1000);
    const lines = [
      `# 决战卷判卷报告 · ${P.title}`,'',
      `- 用时：${Math.floor(t/60)} 分 ${t%60} 秒（限时 ${MINUTES} 分钟）`, `- 日期：${new Date().toISOString().slice(0,10)}`, '',
      `## 得分`,``,`- 选择 ${R.mcS}/40　- 填空 ${R.fillS}/20　- 计算（自评待复核）${R.calcS}/40　- **合计 ${R.total}/100**`, '',
      `## C 档水位题正确率：${cRate}%（及格线 70%）`, '', '## 错题清单', ''];
    lines.push(...(wrong.length?wrong.map(w=>'- '+w):['- （客观题全对）']));
    lines.push('', '## 选择逐题', '', '| 题 | 你的 | 正确 | 档 | 坑法 |', '|---|---|---|---|---|');
    P.mc.forEach(q=>lines.push(`| ${q.num} | ${R.mcDet[q.num].yours} | ${q.ans} | ${q.level} | ${q.trap||'—'} |`));
    lines.push('', '> 判例⑯：总分行不通，C 档 ≥70% 才算过；错题对应考点明晚进账本重考。');
    return lines.join('\n');
  }

  /* ---------- 导航点 ---------- */
  function updateNav() {
    const dots = $('#navdots'); if (!dots) return; dots.innerHTML='';
    P.mc.forEach(q=>dots.append(dot('mc'+q.num, q.num<21? tr(!!state.mc[q.num]) : '' )));
    // 简化：dots 只显示选择 20 个作答状态
  }
  function dot(id, cls) { const d=el('span','dot '+(cls||'')); if(cls)d.classList.add('done'); d.onclick=()=>document.getElementById(id)?.scrollIntoView?.({behavior:'smooth',block:'center'}); return d; }
  function tr(x){return x}

  /* ---------- 化学小键盘 ---------- */
  const kb = { bar:null, show(inp){
      if(!this.bar){ this.bar = el('div','kb');
        '₀₁₂₃₄₅₆₇₈₉ ⁰¹²³⁴⁵⁶⁷⁸⁹ ⁿ ⁺ ⁻ ⇌ → ⇋ Δ δ θ λ μ π σ ° × ⁄ √ ≈ ℃ ⅛ ½'.split(' ').forEach(ch=>{
          const b=el('button','',ch); b.onmousedown=e=>{e.preventDefault();
            const s=inp.selectionStart||inp.value.length; inp.value=inp.value.slice(0,s)+ch+inp.value.slice(inp.selectionEnd||s);
            inp.oninput(); inp.focus(); inp.selectionStart=inp.selectionEnd=s+ch.length;};
          this.bar.append(b); });
        document.body.append(this.bar); }
      this.bar.style.display='flex';
      const r=inp.getBoundingClientRect();
      this.bar.style.top=(window.scrollY+r.bottom+6)+'px'; this.bar.style.left=Math.max(12,r.left)+'px';
    }};
  document.addEventListener('click', e=>{ if(kb.bar && !e.target.closest('.kb') && !e.target.classList.contains('blank')) kb.bar.style.display='none'; });

  /* ---------- 启动 ---------- */
  render();
  if (saved) { const n = Object.keys(state.mc).length + Object.values(state.fill).flat().filter(Boolean).length;
    if (n>0) $('#resume').style.display='block', $('#resume').textContent=`已恢复你上次的 ${n} 处作答（本地自动存档）`; }
  if (state.submitted) { P.mc.forEach(q=>markMC(q,$('#mc'+q.num))); P.fill.forEach(q=>markFill(q,$('#fl'+q.num))); document.querySelectorAll('#submitBtn')[0].textContent='已交卷 · 查看报告'; renderReport(); }
  timer = setInterval(tick, 1000); tick();
})();
