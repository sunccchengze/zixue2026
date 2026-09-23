import { DISCIPLINES } from '../../data/disciplines.js';
export function render(){
  const d=DISCIPLINES.find(x=>x.id==='mechanics');
  const div=document.createElement('div');
  div.innerHTML=`
    <h2>🏗️ ${d.name} 星系</h2>
    <p><small>${d.desc} | ${d.textbook} | ${d.location}</small></p>
    <div style="display:grid;grid-template-columns:1fr 340px;gap:20px">
      <div>
        <div style="background:rgba(255,138,0,0.08);border:1px solid #ff8a00;border-radius:16px;padding:16px">
          <h3>⚖️ 平面任意力系平衡计算器 - 真实可用</h3>
          <p style="font-size:11px;opacity:0.8">ΣF=0, ΣM=0。来自你课题03攻关中，A卷计算2真题：AB+CD+BCE，M=Fa，F在销钉B。口诀：力偶只管转，无力争</p>
          <canvas id="mech-canvas" style="width:100%;height:360px;background:#0a0a14;border-radius:12px;margin-top:12px;cursor:crosshair"></canvas>
          <div style="display:flex;gap:8px;margin-top:12px;flex-wrap:wrap">
            <button id="btn-add-force" style="padding:4px 12px;border-radius:20px;border:1px solid #ff8a00;background:rgba(255,138,0,0.2);color:white;cursor:pointer">➕ 加力 F</button>
            <button id="btn-add-couple" style="padding:4px 12px;border-radius:20px;border:1px solid #ff8a00;background:rgba(255,138,0,0.2);color:white;cursor:pointer">🌀 加力偶 M</button>
            <button id="btn-calc" style="padding:4px 12px;border-radius:20px;border:1px solid #00ff88;background:rgba(0,255,136,0.2);color:white;cursor:pointer">🧮 计算平衡</button>
            <button id="btn-clear" style="padding:4px 12px;border-radius:20px;border:1px solid #666;background:rgba(255,255,255,0.06);color:white;cursor:pointer">清空</button>
          </div>
          <div id="mech-result" style="font-family:monospace;font-size:11px;margin-top:8px;background:rgba(0,0,0,0.3);padding:8px;border-radius:8px;white-space:pre-wrap"></div>
        </div>
      </div>
      <div>
        <div class="discipline-card"><b>核心公式</b><br><div style="font-family:monospace;font-size:11px">${d.formulas.map(f=>`<div style="margin:2px 0;padding:4px;background:rgba(255,138,0,0.1);border-radius:4px">${f}</div>`).join('')}</div></div>
        <div class="discipline-card"><b>作业线</b><br><small>${d.homework}<br><br>易错：力偶只进力矩方程，永不进力的方程！</small></div>
        <div class="discipline-card"><b>真题</b><br><small>2024A卷计算2: BCE杆，CD二力杆，F_CD=F, F_Bx=F, F_By=0<br>固定端A: F_Ax=F, F_Ay=F, M_A=Fa顺时针</small></div>
      </div>
    </div>
  `;
  setTimeout(()=>{
    const canvas=div.querySelector('#mech-canvas');
    const ctx=canvas.getContext('2d');
    const resize=()=>{ canvas.width=canvas.offsetWidth*2; canvas.height=360*2; };
    resize();
    let forces=[], couples=[], mode='force';
    div.querySelector('#btn-add-force').onclick=()=>mode='force';
    div.querySelector('#btn-add-couple').onclick=()=>mode='couple';
    div.querySelector('#btn-clear').onclick=()=>{ forces=[]; couples=[]; draw(); updateResult(); };
    canvas.onclick=(e)=>{
      const rect=canvas.getBoundingClientRect();
      const x=(e.clientX-rect.left)*2, y=(e.clientY-rect.top)*2;
      if(mode==='force'){ forces.push({x,y,F:100+Math.random()*100, angle:Math.random()*Math.PI*2, id:forces.length}); }
      else{ couples.push({x,y,M:(Math.random()-0.5)*200, id:couples.length}); }
      draw(); updateResult();
    };
    const updateResult=()=>{
      let Rx=0,Ry=0,Mo=0;
      const origin={x:canvas.width/2,y:canvas.height/2};
      forces.forEach(f=>{ Rx+=f.F*Math.cos(f.angle); Ry+=f.F*Math.sin(f.angle); const r={x:f.x-origin.x, y:f.y-origin.y}; Mo+= r.x*(f.F*Math.sin(f.angle)) - r.y*(f.F*Math.cos(f.angle)); });
      couples.forEach(c=>Mo+=c.M);
      const R=Math.hypot(Rx,Ry);
      div.querySelector('#mech-result').textContent=`主矢: Rx=${Rx.toFixed(1)}N, Ry=${Ry.toFixed(1)}N, R=${R.toFixed(1)}N ∠${(Math.atan2(Ry,Rx)*180/Math.PI).toFixed(1)}°\n主矩(对中心): Mo=${Mo.toFixed(1)}N·m\n平衡: ${R<1&&Math.abs(Mo)<1?'✅ 平衡! ΣF=0 ΣM=0':'❌ 不平衡，需加约束反力'}\n力偶检查: 力偶只贡献Mo，不贡献Rx,Ry ✅`;
    };
    const draw=()=>{
      const w=canvas.width,h=canvas.height;
      ctx.clearRect(0,0,w,h);
      ctx.strokeStyle='rgba(255,255,255,0.05)'; ctx.lineWidth=1;
      for(let x=0;x<w;x+=40){ ctx.beginPath(); ctx.moveTo(x,0); ctx.lineTo(x,h); ctx.stroke(); }
      for(let y=0;y<h;y+=40){ ctx.beginPath(); ctx.moveTo(0,y); ctx.lineTo(w,y); ctx.stroke(); }
      ctx.fillStyle='#ff8a00'; ctx.beginPath(); ctx.arc(w/2,h/2,4,0,Math.PI*2); ctx.fill();
      ctx.fillStyle='white'; ctx.font='16px monospace'; ctx.fillText('O',w/2+8,h/2-8);
      forces.forEach(f=>{
        const len=60; const ex=f.x+Math.cos(f.angle)*len, ey=f.y+Math.sin(f.angle)*len;
        ctx.strokeStyle='#00f5ff'; ctx.lineWidth=3; ctx.beginPath(); ctx.moveTo(f.x,f.y); ctx.lineTo(ex,ey); ctx.stroke();
        ctx.save(); ctx.translate(ex,ey); ctx.rotate(f.angle); ctx.beginPath(); ctx.moveTo(0,0); ctx.lineTo(-10,-5); ctx.lineTo(-10,5); ctx.closePath(); ctx.fillStyle='#00f5ff'; ctx.fill(); ctx.restore();
        ctx.fillStyle='white'; ctx.font='12px monospace'; ctx.fillText(`F${f.id}=${f.F.toFixed(0)}N`,f.x+6,f.y-6);
      });
      couples.forEach(c=>{
        ctx.strokeStyle='#ff5c8a'; ctx.lineWidth=2; ctx.beginPath(); ctx.arc(c.x,c.y,20,0,Math.PI*1.5); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(c.x,c.y-20); ctx.lineTo(c.x-6,c.y-14); ctx.lineTo(c.x+6,c.y-14); ctx.closePath(); ctx.fillStyle='#ff5c8a'; ctx.fill();
        ctx.fillStyle='white'; ctx.font='12px monospace'; ctx.fillText(`M${c.id}=${c.M.toFixed(0)}`,c.x+24,c.y);
      });
    };
    div.querySelector('#btn-calc').onclick=updateResult;
    draw(); updateResult();
  },100);
  return div;
}
