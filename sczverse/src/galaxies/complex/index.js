import { DISCIPLINES } from '../../data/disciplines.js';
export function render(){
  const d=DISCIPLINES.find(x=>x.id==='complex');
  const div=document.createElement('div');
  div.innerHTML=`
    <h2>🌀 ${d.name} 星系</h2>
    <p><small>${d.desc} | ${d.homework}</small></p>
    <div style="display:grid;grid-template-columns:1fr 340px;gap:20px">
      <div>
        <div style="background:rgba(124,92,255,0.08);border:1px solid #7c5cff;border-radius:16px;padding:16px">
          <h3>📐 复平面实验室 - 欧拉公式可视化</h3>
          <p style="font-size:11px;opacity:0.8">e^{iθ}=cosθ+i sinθ，乘以e^{iθ}是旋转θ。x³=1三根成等边三角形</p>
          <canvas id="complex-canvas" style="width:100%;height:400px;background:#0a0a14;border-radius:12px;margin-top:12px;cursor:crosshair"></canvas>
          <div style="display:flex;gap:8px;margin-top:12px;flex-wrap:wrap;align-items:center">
            <label style="font-size:12px">θ=<span id="theta-val">45°</span> <input type="range" id="theta-slider" min="0" max="360" value="45" style="width:120px"></label>
            <button id="btn-mul-i" style="padding:4px 12px;border-radius:20px;border:1px solid #7c5cff;background:rgba(124,92,255,0.2);color:white;cursor:pointer">× i (旋转90°)</button>
            <button id="btn-conj" style="padding:4px 12px;border-radius:20px;border:1px solid #7c5cff;background:rgba(124,92,255,0.2);color:white;cursor:pointer">共轭</button>
            <button id="btn-de-moivre" style="padding:4px 12px;border-radius:20px;border:1px solid #7c5cff;background:rgba(124,92,255,0.2);color:white;cursor:pointer">棣莫弗 n=3</button>
          </div>
          <div id="complex-info" style="font-family:monospace;font-size:11px;margin-top:8px;background:rgba(0,0,0,0.3);padding:8px;border-radius:8px"></div>
        </div>
      </div>
      <div>
        <div class="discipline-card"><b>核心公式</b><br><div style="font-family:monospace;font-size:11px">${d.formulas.map(f=>`<div style="margin:2px 0;padding:4px;background:rgba(124,92,255,0.1);border-radius:4px">${f}</div>`).join('')}</div></div>
        <div class="discipline-card"><b>几何意义</b><br><small>• 乘i = 旋转90°<br>• 乘e^{iθ} = 旋转θ<br>• 共轭 = 关于实轴镜像<br>• |z| = 到原点距离<br>• z·z̄=|z|²<br>• x³=1 三根成等边三角形: 1, ω, ω², ω=e^{2πi/3}</small></div>
      </div>
    </div>
  `;
  setTimeout(()=>{
    const canvas=div.querySelector('#complex-canvas');
    const ctx=canvas.getContext('2d');
    const resize=()=>{ canvas.width=canvas.offsetWidth*2; canvas.height=400*2; };
    resize();
    let z={x:100,y:50};
    let theta=45;
    const toScreen=(zx,zy)=>{ const w=canvas.width,h=canvas.height; return {x:w/2+zx, y:h/2-zy}; };
    const draw=()=>{
      const w=canvas.width,h=canvas.height;
      ctx.clearRect(0,0,w,h);
      ctx.strokeStyle='rgba(255,255,255,0.06)'; ctx.lineWidth=1;
      for(let x=0;x<w;x+=40){ ctx.beginPath(); ctx.moveTo(x,0); ctx.lineTo(x,h); ctx.stroke(); }
      for(let y=0;y<h;y+=40){ ctx.beginPath(); ctx.moveTo(0,y); ctx.lineTo(w,y); ctx.stroke(); }
      ctx.strokeStyle='rgba(255,255,255,0.3)'; ctx.lineWidth=2;
      ctx.beginPath(); ctx.moveTo(0,h/2); ctx.lineTo(w,h/2); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(w/2,0); ctx.lineTo(w/2,h); ctx.stroke();
      ctx.fillStyle='white'; ctx.font='16px monospace'; ctx.fillText('Re',w-30,h/2-10); ctx.fillText('Im',w/2+10,20);
      ctx.strokeStyle='rgba(124,92,255,0.3)'; ctx.setLineDash([6,6]); ctx.beginPath(); ctx.arc(w/2,h/2,100,0,Math.PI*2); ctx.stroke(); ctx.setLineDash([]);
      const s=toScreen(z.x,z.y);
      ctx.strokeStyle='#00f5ff'; ctx.lineWidth=3; ctx.beginPath(); ctx.moveTo(w/2,h/2); ctx.lineTo(s.x,s.y); ctx.stroke();
      ctx.fillStyle='#00f5ff'; ctx.beginPath(); ctx.arc(s.x,s.y,6,0,Math.PI*2); ctx.fill();
      const r=Math.hypot(z.x,z.y), ang=Math.atan2(z.y,z.x)*180/Math.PI;
      ctx.fillStyle='white'; ctx.font='12px monospace'; ctx.fillText(`z = ${ (z.x/100).toFixed(2)} + ${(z.y/100).toFixed(2)}i`,s.x+10,s.y-10);
      const rad=theta*Math.PI/180;
      const rot={x: z.x*Math.cos(rad)-z.y*Math.sin(rad), y: z.x*Math.sin(rad)+z.y*Math.cos(rad)};
      const sr=toScreen(rot.x,rot.y);
      ctx.strokeStyle='#ffcc00'; ctx.lineWidth=2; ctx.setLineDash([4,4]); ctx.beginPath(); ctx.moveTo(w/2,h/2); ctx.lineTo(sr.x,sr.y); ctx.stroke(); ctx.setLineDash([]);
      ctx.fillStyle='#ffcc00'; ctx.beginPath(); ctx.arc(sr.x,sr.y,5,0,Math.PI*2); ctx.fill();
      div.querySelector('#complex-info').innerHTML=`z = ${(z.x/100).toFixed(3)} + ${(z.y/100).toFixed(3)}i<br>|z| = ${(r/100).toFixed(4)}, arg(z)=${ang.toFixed(2)}°<br>z̄ = ${(z.x/100).toFixed(3)} - ${(z.y/100).toFixed(3)}i, z·z̄=|z|²=${(r*r/10000).toFixed(4)}<br>e^{iθ}=cos${theta}°+i sin${theta}°=${Math.cos(rad).toFixed(3)}+${Math.sin(rad).toFixed(3)}i<br>旋转后: ${(rot.x/100).toFixed(3)}+${(rot.y/100).toFixed(3)}i`;
    };
    canvas.onpointermove=(e)=>{ if(e.buttons!==1) return; const rect=canvas.getBoundingClientRect(); const x=(e.clientX-rect.left)*2 - canvas.width/2; const y=-((e.clientY-rect.top)*2 - canvas.height/2); z={x,y}; draw(); };
    canvas.onclick=(e)=>{ const rect=canvas.getBoundingClientRect(); const x=(e.clientX-rect.left)*2 - canvas.width/2; const y=-((e.clientY-rect.top)*2 - canvas.height/2); z={x,y}; draw(); };
    div.querySelector('#theta-slider').oninput=(e)=>{ theta=parseInt(e.target.value); div.querySelector('#theta-val').textContent=theta+'°'; draw(); };
    div.querySelector('#btn-mul-i').onclick=()=>{ z={x:-z.y, y:z.x}; draw(); };
    div.querySelector('#btn-conj').onclick=()=>{ z={x:z.x, y:-z.y}; draw(); };
    div.querySelector('#btn-de-moivre').onclick=()=>{ const r=Math.hypot(z.x,z.y)/100; const ang=Math.atan2(z.y,z.x); const r3=Math.pow(r,3); const ang3=ang*3; z={x: Math.cos(ang3)*r3*100, y: Math.sin(ang3)*r3*100}; draw(); };
    draw();
  },100);
  return div;
}
