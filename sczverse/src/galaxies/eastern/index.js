import { DISCIPLINES } from '../../data/disciplines.js';
import { ZEN_QUOTES, randomQuote } from '../../zen/quotes.js';
export function render(){
  const d=DISCIPLINES.find(x=>x.id==='eastern');
  const div=document.createElement('div');
  const q=randomQuote();
  div.innerHTML=`
    <h2>☯️ ${d.name} 星系</h2>
    <p><small>${d.desc} | ${d.method} | 3/20已完成</small></p>
    <div style="display:grid;grid-template-columns:1fr 340px;gap:20px">
      <div>
        <div style="background:rgba(255,255,255,0.06);border:1px solid #fff;border-radius:16px;padding:16px;position:relative;overflow:hidden">
          <div style="position:absolute;inset:0;background:radial-gradient(ellipse at 30% 20%,rgba(255,255,255,0.08),transparent)"></div>
          <div style="position:relative;z-index:1">
            <h3>🍃 禅意打脸实验室</h3>
            <p style="font-size:12px;opacity:0.8">预测→实验→打脸→修正→记录 = 知行合一实验室。来自你的Track 5</p>
            <div style="margin:16px 0;padding:20px;background:rgba(0,0,0,0.3);border-radius:12px;border-left:3px solid #fff">
              <div style="font-size:24px">${q.mood} ${q.text}</div>
              <div style="font-size:12px;opacity:0.6;margin-top:8px">——《${q.from}》${q.author}</div>
            </div>
            <canvas id="zen-canvas" style="width:100%;height:300px;background:#0a0a0a;border-radius:12px;margin-top:12px;cursor:crosshair"></canvas>
            <div style="display:flex;gap:8px;margin-top:12px;flex-wrap:wrap">
              <button id="btn-ripple" style="padding:4px 12px;border-radius:20px;border:1px solid #fff;background:rgba(255,255,255,0.1);color:white;cursor:pointer">💧 涟漪</button>
              <button id="btn-stone" style="padding:4px 12px;border-radius:20px;border:1px solid #fff;background:rgba(255,255,255,0.1);color:white;cursor:pointer">🪨 落石</button>
              <button id="btn-quote" style="padding:4px 12px;border-radius:20px;border:1px solid #fff;background:rgba(255,255,255,0.1);color:white;cursor:pointer">📜 换一句</button>
            </div>
            <div style="margin-top:16px;display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px">
              <div style="background:rgba(255,255,255,0.04);padding:12px;border-radius:12px"><b>主题01</b><br><small>传习录·知行合一<br>8.8/10封档<br>三天实验：Zotero论文卡</small></div>
              <div style="background:rgba(255,255,255,0.04);padding:12px;border-radius:12px"><b>主题02</b><br><small>道德经·无为<br>实践输出验收<br>无为而无不为</small></div>
              <div style="background:rgba(255,255,255,0.04);padding:12px;border-radius:12px"><b>主题03</b><br><small>六祖坛经·本来无一物<br>两偈对比修正<br>空杯行动</small></div>
            </div>
          </div>
        </div>
      </div>
      <div>
        <div class="discipline-card"><b>打脸链路</b><br><small>①预测：我以为...<br>②实验：去做...<br>③打脸：结果是...<br>④修正：原来是...<br>⑤记录：写进MEMORY<br><br>这是知行合一的实验室</small></div>
        <div class="discipline-card"><b>核心公式</b><br><div style="font-size:11px">${d.formulas.map(f=>`<div style="margin:2px 0;padding:4px;background:rgba(255,255,255,0.06);border-radius:4px">${f}</div>`).join('')}</div></div>
        <div class="discipline-card"><b>记忆锚三件套</b><br><small>故事/口诀/位置法<br>概念块≤150字<br>生图出图，禁ASCII</small></div>
      </div>
    </div>
  `;
  setTimeout(()=>{
    const canvas=div.querySelector('#zen-canvas');
    const ctx=canvas.getContext('2d');
    const resize=()=>{ canvas.width=canvas.offsetWidth*2; canvas.height=300*2; };
    resize();
    let ripples=[], stones=[];
    const addRipple=(x,y)=>{ ripples.push({x,y,r:0,maxR:200+Math.random()*200,alpha:1}); };
    const addStone=(x,y)=>{ stones.push({x,y,r:10+Math.random()*20}); addRipple(x,y); };
    for(let i=0;i<5;i++) stones.push({x:Math.random()*canvas.width, y:Math.random()*canvas.height, r:15+Math.random()*25});
    const draw=()=>{
      const w=canvas.width,h=canvas.height;
      ctx.fillStyle='#0a0a0a'; ctx.fillRect(0,0,w,h);
      // sand texture
      ctx.strokeStyle='rgba(255,255,255,0.03)'; ctx.lineWidth=1;
      for(let y=0;y<h;y+=20){ ctx.beginPath(); for(let x=0;x<w;x+=10){ const yy=y+Math.sin(x*0.01)*5; if(x==0) ctx.moveTo(x,yy); else ctx.lineTo(x,yy); } ctx.stroke(); }
      // stones
      stones.forEach(s=>{
        const grad=ctx.createRadialGradient(s.x-s.r*0.3,s.y-s.r*0.3,0,s.x,s.y,s.r);
        grad.addColorStop(0,'#555'); grad.addColorStop(1,'#222');
        ctx.fillStyle=grad; ctx.beginPath(); ctx.arc(s.x,s.y,s.r,0,Math.PI*2); ctx.fill();
        ctx.fillStyle='rgba(0,0,0,0.3)'; ctx.beginPath(); ctx.ellipse(s.x,s.y+s.r*0.5,s.r*0.8,s.r*0.3,0,0,Math.PI*2); ctx.fill();
      });
      // ripples
      ripples=ripples.filter(r=>r.alpha>0);
      ripples.forEach(r=>{
        r.r+=1.5; r.alpha=1-r.r/r.maxR;
        ctx.strokeStyle=`rgba(255,255,255,${r.alpha*0.3})`; ctx.lineWidth=1;
        ctx.beginPath(); ctx.arc(r.x,r.y,r.r,0,Math.PI*2); ctx.stroke();
      });
      requestAnimationFrame(draw);
    };
    canvas.onclick=(e)=>{ const rect=canvas.getBoundingClientRect(); const x=(e.clientX-rect.left)*2, y=(e.clientY-rect.top)*2; addStone(x,y); };
    div.querySelector('#btn-ripple').onclick=()=>{ addRipple(Math.random()*canvas.width, Math.random()*canvas.height); };
    div.querySelector('#btn-stone').onclick=()=>{ addStone(Math.random()*canvas.width, Math.random()*canvas.height); };
    div.querySelector('#btn-quote').onclick=()=>{
      const nq=randomQuote();
      div.querySelector('div[style*="font-size:24px"]').innerHTML=`${nq.mood} ${nq.text}<div style="font-size:12px;opacity:0.6;margin-top:8px">——《${nq.from}》${nq.author}</div>`;
    };
    draw();
  },100);
  return div;
}
