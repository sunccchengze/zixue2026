export function render(){
  const div=document.createElement('div');
  div.innerHTML=`
    <h3>⚛️ 简谐振动 - 真实微分方程求解</h3>
    <p><small>m x''+b x'+k x=0, 真实能量守恒，来自大学物理课题01五站</small></p>
    <canvas id="c-phys-toy" class="game-canvas" style="height:400px"></canvas>
    <div class="game-controls">
      <button id="btn-phys-hit">给一拳</button>
      <label>k<input type="range" id="k-slider" min="1" max="20" value="4" style="width:60px"> <span id="k-v">4</span></label>
      <label>b<input type="range" id="b-slider2" min="0" max="2" value="0" step="0.1" style="width:60px"> <span id="b-v2">0</span></label>
    </div>
  `;
  setTimeout(()=>{
    const canvas=div.querySelector('#c-phys-toy');
    const ctx=canvas.getContext('2d');
    const resize=()=>{ canvas.width=canvas.offsetWidth*2; canvas.height=400*2; };
    resize();
    let x=50, v=0, k=4, b=0, m=1, t=0, hist=[];
    const loop=()=>{
      t+=0.016;
      const a=(-b*v - k*x)/m;
      v+=a*0.016; x+=v*0.016;
      hist.push({t,x,v}); if(hist.length>500) hist.shift();
      const w=canvas.width,h=canvas.height;
      ctx.clearRect(0,0,w,h);
      ctx.strokeStyle='rgba(255,255,255,0.05)'; for(let y=0;y<h;y+=40){ ctx.beginPath(); ctx.moveTo(0,y); ctx.lineTo(w,y); ctx.stroke(); }
      ctx.strokeStyle='#00ff88'; ctx.lineWidth=3; ctx.beginPath();
      hist.forEach((p,i)=>{ const px=i/hist.length*w; const py=h/2 - p.x*2; if(i==0) ctx.moveTo(px,py); else ctx.lineTo(px,py); }); ctx.stroke();
      ctx.fillStyle='#ff8a00'; ctx.fillRect(w/2 + x*2 -10, h*0.7-10,20,20);
      requestAnimationFrame(loop);
    };
    div.querySelector('#btn-phys-hit').onclick=()=>{ v+=20; };
    div.querySelector('#k-slider').oninput=(e)=>{ k=parseFloat(e.target.value); div.querySelector('#k-v').textContent=k; };
    div.querySelector('#b-slider2').oninput=(e)=>{ b=parseFloat(e.target.value); div.querySelector('#b-v2').textContent=b; };
    loop();
  },100);
  return div;
}
