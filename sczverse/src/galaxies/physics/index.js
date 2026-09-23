import { DISCIPLINES } from '../../data/disciplines.js';
export function render(){
  const d=DISCIPLINES.find(x=>x.id==='physics');
  const div=document.createElement('div');
  div.innerHTML=`
    <h2>⚛️ ${d.name} 星系</h2>
    <p><small>${d.desc} | ${d.location} | ${d.teacher}</small></p>
    <div style="display:grid;grid-template-columns:1fr 340px;gap:20px">
      <div>
        <div style="background:rgba(0,255,136,0.08);border:1px solid #00ff88;border-radius:16px;padding:16px">
          <h3>🌀 简谐振动实验室 - 真实方程求解</h3>
          <p style="font-size:11px;opacity:0.8">x=A cos(ωt+φ), v=-Aω sin, a=-Aω² cos, ω=√(k/m)。来自你课题01五站：胡克→微分方程→猜解验证→管辖权→旋转矢量→合成与拍</p>
          <canvas id="phys-canvas" style="width:100%;height:380px;background:#0a0a14;border-radius:12px;margin-top:12px"></canvas>
          <div style="display:flex;gap:8px;margin-top:12px;flex-wrap:wrap;align-items:center">
            <label style="font-size:11px">A=<span id="A-val">5</span> <input type="range" id="A-slider" min="1" max="10" value="5" step="0.5" style="width:80px"></label>
            <label style="font-size:11px">ω=<span id="w-val">2</span> <input type="range" id="w-slider" min="0.2" max="5" value="2" step="0.2" style="width:80px"></label>
            <label style="font-size:11px">阻尼 b=<span id="b-val">0</span> <input type="range" id="b-slider" min="0" max="1" value="0" step="0.05" style="width:80px"></label>
            <button id="btn-hit" style="padding:4px 12px;border-radius:20px;border:1px solid #00ff88;background:rgba(0,255,136,0.2);color:white;cursor:pointer">给一拳</button>
          </div>
          <div id="phys-info" style="font-family:monospace;font-size:11px;margin-top:8px;background:rgba(0,0,0,0.3);padding:8px;border-radius:8px"></div>
        </div>
      </div>
      <div>
        <div class="discipline-card"><b>核心公式</b><br><div style="font-family:monospace;font-size:11px">${d.formulas.map(f=>`<div style="margin:2px 0;padding:4px;background:rgba(0,255,136,0.1);border-radius:4px">${f}</div>`).join('')}</div></div>
        <div class="discipline-card"><b>五站攻关</b><br><small>①胡克定律→微分方程 F=ma<br>②猜解验证 cos现身 A/ω/φ<br>③管辖权 ★ω与A无关 最大考点<br>④旋转矢量 2022期中T1-2提速<br>⑤合成与拍 真题实战</small></div>
        <div class="discipline-card"><b>校准批4题</b><br><small>1.落体0.5s理想化<br>2.x=5cos2πt求v,a相位<br>3.弹簧下拉10cm松手会停吗？为什么最远只到上方10cm？(惯性+能量)<br>4.期末考到哪章？</small></div>
      </div>
    </div>
  `;
  setTimeout(()=>{
    const canvas=div.querySelector('#phys-canvas');
    const ctx=canvas.getContext('2d');
    const resize=()=>{ canvas.width=canvas.offsetWidth*2; canvas.height=380*2; };
    resize();
    let A=5, omega=2, b=0, t=0, history=[], v=0, x=A;
    const k=omega*omega, m=1;
    const dt=0.016;
    let running=true;
    const loop=()=>{
      if(!running) return;
      t+=dt;
      // 真实阻尼振动方程: m x'' + b x' + k x =0
      const a=(-b*v - k*x)/m;
      v+=a*dt;
      x+=v*dt;
      history.push({t,x,v,a});
      if(history.length>600) history.shift();
      draw();
      requestAnimationFrame(loop);
    };
    const draw=()=>{
      const w=canvas.width,h=canvas.height;
      ctx.clearRect(0,0,w,h);
      // grid
      ctx.strokeStyle='rgba(255,255,255,0.05)'; ctx.lineWidth=1;
      for(let y=0;y<h;y+=40){ ctx.beginPath(); ctx.moveTo(0,y); ctx.lineTo(w,y); ctx.stroke(); }
      // center line
      ctx.strokeStyle='rgba(255,255,255,0.2)'; ctx.beginPath(); ctx.moveTo(0,h/2); ctx.lineTo(w,h/2); ctx.stroke();
      // x(t)
      ctx.strokeStyle='#00ff88'; ctx.lineWidth=3; ctx.beginPath();
      history.forEach((p,i)=>{ const px=i/history.length*w; const py=h/2 - p.x*20; if(i==0) ctx.moveTo(px,py); else ctx.lineTo(px,py); }); ctx.stroke();
      // v(t)
      ctx.strokeStyle='#00f5ff'; ctx.lineWidth=2; ctx.beginPath();
      history.forEach((p,i)=>{ const px=i/history.length*w; const py=h/2 - p.v*8; if(i==0) ctx.moveTo(px,py); else ctx.lineTo(px,py); }); ctx.stroke();
      // current mass-spring
      const springX=w*0.15, massX=w*0.15 + x*20;
      ctx.strokeStyle='#ff8a00'; ctx.lineWidth=2;
      ctx.beginPath();
      for(let sx=springX;sx<massX;sx+=10){ const sy=h*0.75 + Math.sin((sx-springX)*0.2 + t*5)*10; if(sx==springX) ctx.moveTo(sx,sy); else ctx.lineTo(sx,sy); } ctx.stroke();
      ctx.fillStyle='#ff8a00'; ctx.fillRect(massX-12,h*0.75-12,24,24);
      ctx.fillStyle='white'; ctx.font='12px monospace';
      ctx.fillText(`x=${x.toFixed(2)}cm v=${v.toFixed(2)}`,massX+16,h*0.75);
      // info
      const E=0.5*k*x*x+0.5*m*v*v;
      div.querySelector('#phys-info').innerHTML=`t=${t.toFixed(2)}s, x=A cos(ωt+φ), 当前: x=${x.toFixed(3)}, v=${v.toFixed(3)}, a=${((-b*v - k*x)/m).toFixed(3)}<br>能量 E=½kx²+½mv²=${E.toFixed(3)} (阻尼时衰减) | ω=√(k/m)=${omega.toFixed(2)}, k=${k.toFixed(2)}, b=${b}<br><span style="color:#00ff88">绿=x(t)</span> <span style="color:#00f5ff">青=v(t)</span> | 平衡位置速度最大加速度0，端点相反`;
    };
    div.querySelector('#A-slider').oninput=(e)=>{ A=parseFloat(e.target.value); div.querySelector('#A-val').textContent=A; x=A; v=0; };
    div.querySelector('#w-slider').oninput=(e)=>{ omega=parseFloat(e.target.value); div.querySelector('#w-val').textContent=omega; };
    div.querySelector('#b-slider').oninput=(e)=>{ b=parseFloat(e.target.value); div.querySelector('#b-val').textContent=b; };
    div.querySelector('#btn-hit').onclick=()=>{ v+=5; };
    loop();
  },100);
  return div;
}
