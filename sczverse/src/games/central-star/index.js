
export function render(){
  const div=document.createElement('div');
  div.innerHTML=`
    <h2>🌟 承泽星 · 你的本命星</h2>
    <p>孙承泽，2253710052，能动强基2501，西安交大</p>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:16px">
      <div class="discipline-card"><b>🔥 热爱</b><br>涡轮叶片AI、软体小鹰、解压玩具、游戏、东方哲学</div>
      <div class="discipline-card"><b>🎯 主线</b><br>turbine-blade-ai-platform · 74维优化 · NASA Rotor 37</div>
      <div class="discipline-card"><b>📚 并行</b><br>10学科并行学习，多线程大脑</div>
      <div class="discipline-card"><b>🧠 MBTI</b><br>INTJ · 用作品表达情感 · 打脸链路</div>
    </div>
    <canvas id="central-canvas" style="width:100%;height:300px;margin-top:16px;background:radial-gradient(circle,#1a1a3a,transparent);border-radius:16px"></canvas>
  `;
  setTimeout(()=>{
    const c=div.querySelector('#central-canvas');
    const ctx=c.getContext('2d');
    c.width=600; c.height=300;
    let t=0;
    function loop(){
      t+=0.01;
      ctx.clearRect(0,0,c.width,c.height);
      ctx.save(); ctx.translate(c.width/2,c.height/2);
      for(let i=0;i<10;i++){
        const a=i/10*Math.PI*2 + t;
        const r=80 + Math.sin(t*2+i)*10;
        ctx.fillStyle=`hsl(${260+i*10},100%,60%)`;
        ctx.beginPath(); ctx.arc(Math.cos(a)*r, Math.sin(a)*r, 4,0,Math.PI*2); ctx.fill();
      }
      ctx.fillStyle='white'; ctx.font='bold 32px serif'; ctx.textAlign='center'; ctx.fillText('泽',0,10);
      ctx.restore();
      requestAnimationFrame(loop);
    }loop();
  },100);
  return div;
}
