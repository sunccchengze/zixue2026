import { DISCIPLINES } from '../../data/disciplines.js';
export function render(){
  const d=DISCIPLINES.find(x=>x.id==='chemistry');
  const div=document.createElement('div');
  div.innerHTML=`
    <h2>🧪 ${d.name} 星系</h2>
    <p><small>${d.desc} | ${d.location} | 实验${d.teacher}</small></p>
    <div style="display:grid;grid-template-columns:1fr 340px;gap:20px">
      <div>
        <div style="background:rgba(255,92,138,0.08);border:1px solid #ff5c8a;border-radius:16px;padding:16px">
          <h3>⚗️ 化学平衡计算器 - 真实可用</h3>
          <p style="font-size:11px;opacity:0.8">ΔG=ΔH-TΔS, K=exp(-ΔG/RT), 速率v=k[A]^m[B]^n。来自你真题解剖14份，决战三卷</p>
          <canvas id="chem-canvas" style="width:100%;height:360px;background:#0a0a14;border-radius:12px;margin-top:12px"></canvas>
          <div style="display:flex;gap:8px;margin-top:12px;flex-wrap:wrap;align-items:center">
            <label style="font-size:11px">ΔH(kJ) <input type="range" id="dh" min="-200" max="200" value="-50" style="width:80px"> <span id="dh-v">-50</span></label>
            <label style="font-size:11px">ΔS(J/K) <input type="range" id="ds" min="-200" max="200" value="-100" style="width:80px"> <span id="ds-v">-100</span></label>
            <label style="font-size:11px">T(K) <input type="range" id="temp" min="200" max="800" value="298" style="width:80px"> <span id="temp-v">298</span></label>
          </div>
          <div id="chem-info" style="font-family:monospace;font-size:11px;margin-top:8px;background:rgba(0,0,0,0.3);padding:8px;border-radius:8px"></div>
        </div>
      </div>
      <div>
        <div class="discipline-card"><b>核心公式</b><br><div style="font-family:monospace;font-size:11px">${d.formulas.map(f=>`<div style="margin:2px 0;padding:4px;background:rgba(255,92,138,0.1);border-radius:4px">${f}</div>`).join('')}</div></div>
        <div class="discipline-card"><b>决战三卷</b><br><small>真题解剖14份<br>三套C档卷已就绪<br>卷一「镜中院」待作答<br>前四章=期中，后四章=期末<br>8次实验：第3,6-11,13周周一 中1-3125</small></div>
      </div>
    </div>
  `;
  setTimeout(()=>{
    const canvas=div.querySelector('#chem-canvas');
    const ctx=canvas.getContext('2d');
    const resize=()=>{ canvas.width=canvas.offsetWidth*2; canvas.height=360*2; };
    resize();
    let dH=-50, dS=-100, T=298;
    const R=8.314;
    const draw=()=>{
      const w=canvas.width,h=canvas.height;
      ctx.clearRect(0,0,w,h);
      // calc
      const dG=dH*1000 - T*dS;
      const K=Math.exp(-dG/(R*T));
      const dGkJ=dG/1000;
      // background gradient by dG
      const hue=dGkJ<0?140:0;
      ctx.fillStyle=`hsla(${hue},80%,20%,0.2)`; ctx.fillRect(0,0,w,h);
      // molecule animation
      const t=Date.now()*0.001;
      for(let i=0;i<20;i++){
        const x=(Math.sin(t+i)*0.5+0.5)*w;
        const y=(i/20)*h + Math.sin(t*2+i)*10;
        const size=10+Math.sin(t+i)*3;
        ctx.fillStyle=K>1?`hsl(140,80%,60%)`:`hsl(0,80%,60%)`;
        ctx.globalAlpha=0.6;
        ctx.beginPath(); ctx.arc(x,y,size,0,Math.PI*2); ctx.fill();
        // bond
        if(i<19){
          const x2=(Math.sin(t+i+1)*0.5+0.5)*w;
          const y2=((i+1)/20)*h + Math.sin(t*2+i+1)*10;
          ctx.strokeStyle='rgba(255,255,255,0.2)'; ctx.lineWidth=2;
          ctx.beginPath(); ctx.moveTo(x,y); ctx.lineTo(x2,y2); ctx.stroke();
        }
      }
      ctx.globalAlpha=1;
      ctx.fillStyle='white'; ctx.font='16px monospace';
      ctx.fillText(`ΔG=${dGkJ.toFixed(1)} kJ/mol, K=${K.toExponential(2)}`,10,24);
      ctx.fillText(dGkJ<0?'自发 →':'非自发 ←',10,48);
      div.querySelector('#chem-info').innerHTML=`ΔH=${dH}kJ/mol, ΔS=${dS}J/mol·K, T=${T}K<br>ΔG=ΔH-TΔS=${dH*1000} - ${T}*${dS} = ${dG.toFixed(0)} J/mol = ${dGkJ.toFixed(2)} kJ/mol<br>K=exp(-ΔG/RT)=exp(${(-dG/(R*T)).toFixed(2)})=${K.toExponential(3)}<br>${dGkJ<0?`✅ 自发，K>1，正向有利，温度${dS<0?'降低':'升高'}有利`:`❌ 非自发，K<1，需外界做功`}`;
    };
    div.querySelector('#dh').oninput=(e)=>{ dH=parseInt(e.target.value); div.querySelector('#dh-v').textContent=dH; draw(); };
    div.querySelector('#ds').oninput=(e)=>{ dS=parseInt(e.target.value); div.querySelector('#ds-v').textContent=dS; draw(); };
    div.querySelector('#temp').oninput=(e)=>{ T=parseInt(e.target.value); div.querySelector('#temp-v').textContent=T; draw(); };
    const loop=()=>{ draw(); requestAnimationFrame(loop); };
    loop();
  },100);
  return div;
}
