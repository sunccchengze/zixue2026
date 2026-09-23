import { DISCIPLINES } from '../../data/disciplines.js';
export function render(info){
  const d = info || DISCIPLINES.find(x=>x.id==='probability');
  const div=document.createElement('div');
  div.innerHTML=`
    <h2>🎲 ${d.name} 星系</h2>
    <p><small>${d.desc} | ${d.textbook} | ${d.exam}</small></p>
    <div style="display:grid;grid-template-columns:1fr 340px;gap:20px">
      <div>
        <div style="background:rgba(255,204,0,0.08);border:1px solid #ffcc00;border-radius:16px;padding:16px">
          <h3>📊 大数定律实验室 - 真实可运行</h3>
          <p style="font-size:12px;opacity:0.8">切比雪夫不等式: P(|X̄-μ|≥ε) ≤ σ²/(nε²) 。来自你课题09待开内容，σ²=35/12是骰子方差</p>
          <canvas id="lln-canvas" style="width:100%;height:320px;background:#0a0a14;border-radius:12px;margin-top:12px"></canvas>
          <div style="display:flex;gap:8px;margin-top:12px;flex-wrap:wrap">
            <label style="font-size:12px">n=<span id="n-val">100</span> <input type="range" id="n-slider" min="10" max="5000" value="100" step="10" style="width:120px"></label>
            <label style="font-size:12px">ε=<span id="eps-val">0.1</span> <input type="range" id="eps-slider" min="0.01" max="0.5" value="0.1" step="0.01" style="width:100px"></label>
            <button id="btn-run-lln" style="padding:4px 12px;border-radius:20px;border:1px solid #ffcc00;background:rgba(255,204,0,0.2);color:white;cursor:pointer">🎲 掷骰子实验</button>
            <button id="btn-reset-lln" style="padding:4px 12px;border-radius:20px;border:1px solid #666;background:rgba(255,255,255,0.06);color:white;cursor:pointer">重置</button>
          </div>
          <div id="lln-stats" style="font-family:monospace;font-size:11px;margin-top:8px;background:rgba(0,0,0,0.3);padding:8px;border-radius:8px"></div>
        </div>
        <div style="margin-top:16px;background:var(--card);border:1px solid var(--border);border-radius:16px;padding:16px">
          <h4>📚 已完成课题</h4>
          <div style="display:flex;flex-wrap:wrap;gap:6px;margin-top:8px">
            ${d.realProgress.done.map(k=>`<span style="background:rgba(255,204,0,0.15);border:1px solid #ffcc00;padding:2px 8px;border-radius:12px;font-size:11px">${k}</span>`).join('')}
          </div>
          <h4 style="margin-top:12px">🔜 下一步: ${d.realProgress.next}</h4>
          <p style="font-size:11px;opacity:0.7">开题批: 切比雪夫证明骨架 P(|X̄-μ|≥ε) ≤ Var(X̄)/ε² = σ²/(nε²) →0，先教切比雪夫。报数: n多大时 σ²/(nε²)<0.01? (σ²=35/12, ε=0.1) ⇒ n>2917</p>
        </div>
      </div>
      <div>
        <div class="discipline-card"><b>核心公式</b><br><div style="font-family:monospace;font-size:11px;margin-top:6px">${d.formulas.map(f=>`<div style="margin:2px 0;padding:4px;background:rgba(255,204,0,0.1);border-radius:4px">${f}</div>`).join('')}</div></div>
        <div class="discipline-card"><b>真题资产</b><br><small>学习通8章80题已解析<br>概率论课件42散件→10册合并PDF<br>9.22作业第一章奇数题<br>三层表述: 幅度1/√n缩/超界概率→0/轨迹非单调</small></div>
      </div>
    </div>
  `;
  setTimeout(()=>{
    const canvas=div.querySelector('#lln-canvas');
    const ctx=canvas.getContext('2d');
    const resize=()=>{ canvas.width=canvas.offsetWidth*2; canvas.height=320*2; };
    resize();
    let samples=[], meanHistory=[], n=100, eps=0.1;
    const dice=()=>Math.floor(Math.random()*6)+1;
    const runExperiment=()=>{
      samples=[]; meanHistory=[]; let sum=0;
      for(let i=1;i<=n;i++){ const v=dice(); samples.push(v); sum+=v; meanHistory.push(sum/i); }
      draw();
      const mu=3.5, sigma2=35/12;
      const bound=sigma2/(n*eps*eps);
      div.querySelector('#lln-stats').innerHTML=
        `n=${n}, ε=${eps}, μ=3.5, σ²=35/12≈2.917<br>`+
        `样本均值 X̄=${(sum/n).toFixed(4)} | |X̄-μ|=${Math.abs(sum/n-mu).toFixed(4)}<br>`+
        `切比雪夫上界: P(|X̄-μ|≥${eps}) ≤ ${bound.toFixed(4)} ${bound<0.01?'✅ <0.01 达标!':''}<br>`+
        `报数: σ²/(nε²)<0.01 ⇒ n>σ²/(0.01 ε²)=${(sigma2/(0.01*eps*eps)).toFixed(0)}`;
    };
    const draw=()=>{
      const w=canvas.width, h=canvas.height;
      ctx.clearRect(0,0,w,h);
      ctx.strokeStyle='rgba(255,255,255,0.05)'; ctx.lineWidth=1;
      for(let y=0;y<h;y+=40){ ctx.beginPath(); ctx.moveTo(0,y); ctx.lineTo(w,y); ctx.stroke(); }
      const yMu=h*(1-(3.5-1)/5);
      ctx.strokeStyle='#ffcc00'; ctx.setLineDash([8,4]); ctx.beginPath(); ctx.moveTo(0,yMu); ctx.lineTo(w,yMu); ctx.stroke(); ctx.setLineDash([]);
      ctx.fillStyle='#ffcc00'; ctx.font='20px monospace'; ctx.fillText('μ=3.5',10,yMu-10);
      const yEpsUp=h*(1-(3.5+eps-1)/5), yEpsDown=h*(1-(3.5-eps-1)/5);
      ctx.fillStyle='rgba(255,204,0,0.1)'; ctx.fillRect(0,yEpsUp,w,yEpsDown-yEpsUp);
      ctx.strokeStyle='#00f5ff'; ctx.lineWidth=3; ctx.beginPath();
      meanHistory.forEach((m,i)=>{ const x=i/meanHistory.length*w; const y=h*(1-(m-1)/5); if(i==0) ctx.moveTo(x,y); else ctx.lineTo(x,y); }); ctx.stroke();
      samples.forEach((s,i)=>{ if(i%Math.ceil(samples.length/200)!==0) return; const x=i/samples.length*w; const y=h*(1-(s-1)/5); ctx.fillStyle=`hsl(${40+s*10},100%,60%)`; ctx.globalAlpha=0.6; ctx.beginPath(); ctx.arc(x,y,2,0,Math.PI*2); ctx.fill(); });
      ctx.globalAlpha=1;
    };
    div.querySelector('#n-slider').oninput=(e)=>{ n=parseInt(e.target.value); div.querySelector('#n-val').textContent=n; runExperiment(); };
    div.querySelector('#eps-slider').oninput=(e)=>{ eps=parseFloat(e.target.value); div.querySelector('#eps-val').textContent=eps; draw(); };
    div.querySelector('#btn-run-lln').onclick=runExperiment;
    div.querySelector('#btn-reset-lln').onclick=()=>{ samples=[]; meanHistory=[]; ctx.clearRect(0,0,canvas.width,canvas.height); };
    runExperiment();
  },100);
  return div;
}
