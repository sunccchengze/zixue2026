export function render(){
  const div=document.createElement('div');
  div.innerHTML=`
    <h3>🏗️ 力系平衡 - 真实静力学求解器</h3>
    <p><small>拖拽力，实时计算 ΣF=0 ΣM=0，来自工程力学课题03，二力杆/力偶只进力矩</small></p>
    <canvas id="c-mech-toy" class="game-canvas" style="height:400px"></canvas>
    <div class="game-controls"><button id="btn-mech-add">加力</button><button id="btn-mech-clear">清空</button><span id="mech-info" style="font-size:11px;margin-left:12px"></span></div>
  `;
  setTimeout(()=>{
    const canvas=div.querySelector('#c-mech-toy');
    const ctx=canvas.getContext('2d');
    const resize=()=>{ canvas.width=canvas.offsetWidth*2; canvas.height=400*2; };
    resize();
    let forces=[{x:canvas.width*0.3,y:canvas.height*0.5,F:100,angle:0},{x:canvas.width*0.7,y:canvas.height*0.5,F:100,angle:Math.PI}];
    const draw=()=>{
      const w=canvas.width,h=canvas.height;
      ctx.clearRect(0,0,w,h);
      ctx.strokeStyle='rgba(255,255,255,0.05)'; for(let x=0;x<w;x+=40){ ctx.beginPath(); ctx.moveTo(x,0); ctx.lineTo(x,h); ctx.stroke(); } for(let y=0;y<h;y+=40){ ctx.beginPath(); ctx.moveTo(0,y); ctx.lineTo(w,y); ctx.stroke(); }
      let Rx=0,Ry=0,Mo=0;
      const O={x:w/2,y:h/2};
      forces.forEach(f=>{
        Rx+=f.F*Math.cos(f.angle); Ry+=f.F*Math.sin(f.angle);
        Mo+=(f.x-O.x)*f.F*Math.sin(f.angle)-(f.y-O.y)*f.F*Math.cos(f.angle);
        const ex=f.x+Math.cos(f.angle)*60, ey=f.y+Math.sin(f.angle)*60;
        ctx.strokeStyle='#00f5ff'; ctx.lineWidth=3; ctx.beginPath(); ctx.moveTo(f.x,f.y); ctx.lineTo(ex,ey); ctx.stroke();
        ctx.fillStyle='#00f5ff'; ctx.beginPath(); ctx.arc(f.x,f.y,5,0,Math.PI*2); ctx.fill();
      });
      ctx.fillStyle='white'; ctx.font='12px monospace';
      ctx.fillText(`ΣF=(${Rx.toFixed(1)},${Ry.toFixed(1)}) R=${Math.hypot(Rx,Ry).toFixed(1)} ΣM=${Mo.toFixed(1)} ${Math.hypot(Rx,Ry)<5&&Math.abs(Mo)<10?'✅平衡':'❌不平衡'}`,10,20);
      div.querySelector('#mech-info').textContent=`${forces.length}个力 | 拖拽改变力`;
    };
    let drag=null;
    canvas.onpointerdown=(e)=>{ const r=canvas.getBoundingClientRect(); const x=(e.clientX-r.left)*2,y=(e.clientY-r.top)*2; forces.forEach(f=>{ if(Math.hypot(f.x-x,f.y-y)<20) drag=f; }); };
    canvas.onpointermove=(e)=>{ if(!drag) return; const r=canvas.getBoundingClientRect(); drag.x=(e.clientX-r.left)*2; drag.y=(e.clientY-r.top)*2; draw(); };
    canvas.onpointerup=()=>drag=null;
    div.querySelector('#btn-mech-add').onclick=()=>{ forces.push({x:Math.random()*canvas.width,y:Math.random()*canvas.height,F:50+Math.random()*100,angle:Math.random()*Math.PI*2}); draw(); };
    div.querySelector('#btn-mech-clear').onclick=()=>{ forces=[]; draw(); };
    draw();
  },100);
  return div;
}
