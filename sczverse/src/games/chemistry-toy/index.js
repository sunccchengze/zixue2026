export function render(){
  const div=document.createElement('div');
  div.innerHTML=`
    <h3>🧪 化学平衡 - ΔG真实计算</h3>
    <p><small>ΔG=ΔH-TΔS, K=exp(-ΔG/RT)，真实自发判断，来自大学化学决战三卷</small></p>
    <canvas id="c-chem-toy" class="game-canvas" style="height:300px"></canvas>
    <div class="game-controls">
      <label>ΔH<input type="range" id="dh2" min="-200" max="200" value="-50" style="width:80px"> <span id="dh2-v">-50</span></label>
      <label>T<input type="range" id="T2" min="200" max="800" value="298" style="width:80px"> <span id="T2-v">298</span></label>
      <span id="chem-toy-info" style="font-size:11px;margin-left:12px"></span>
    </div>
  `;
  setTimeout(()=>{
    const canvas=div.querySelector('#c-chem-toy');
    const ctx=canvas.getContext('2d');
    const resize=()=>{ canvas.width=canvas.offsetWidth*2; canvas.height=300*2; };
    resize();
    let dH=-50, T=298, dS=-100;
    const draw=()=>{
      const w=canvas.width,h=canvas.height;
      ctx.clearRect(0,0,w,h);
      const dG=dH*1000 - T*dS;
      const K=Math.exp(-dG/(8.314*T));
      ctx.fillStyle=dG<0?'rgba(0,255,136,0.2)':'rgba(255,0,80,0.2)'; ctx.fillRect(0,0,w,h);
      ctx.fillStyle='white'; ctx.font='20px monospace'; ctx.fillText(`ΔG=${(dG/1000).toFixed(1)}kJ K=${K.toExponential(2)} ${dG<0?'自发':''}`,10,30);
      for(let i=0;i<20;i++){ const x=Math.random()*w, y=Math.random()*h; ctx.fillStyle=`hsl(${dG<0?140:0},80%,60%)`; ctx.beginPath(); ctx.arc(x,y,5,0,Math.PI*2); ctx.fill(); }
      div.querySelector('#chem-toy-info').textContent=`ΔG=${(dG/1000).toFixed(1)}kJ, K=${K.toExponential(1)}`;
    };
    div.querySelector('#dh2').oninput=(e)=>{ dH=parseInt(e.target.value); div.querySelector('#dh2-v').textContent=dH; draw(); };
    div.querySelector('#T2').oninput=(e)=>{ T=parseInt(e.target.value); div.querySelector('#T2-v').textContent=T; draw(); };
    const loop=()=>{ draw(); requestAnimationFrame(loop); }; loop();
  },100);
  return div;
}
