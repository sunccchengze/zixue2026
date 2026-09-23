export function render(){
  const div=document.createElement('div');
  div.innerHTML=`
    <h3>🎲 概率瀑布 - 中心极限定理可视化</h3>
    <p><small>大量独立同分布随机变量之和近似正态分布。真实可运行，来自你课题08特征函数φ(t)=E[e^{itX}]</small></p>
    <canvas id="c-probability-toy" class="game-canvas" style="height:400px"></canvas>
    <div class="game-controls">
      <button id="btn-clt">▶️ 开始CLT实验</button>
      <button id="btn-dist">切换分布</button>
      <span style="font-size:11px;opacity:0.6">n=<span id="clt-n">1</span> 均值→正态</span>
    </div>
    <div id="clt-info" style="font-family:monospace;font-size:11px;margin-top:8px;background:rgba(0,0,0,0.3);padding:8px;border-radius:8px"></div>
  `;
  setTimeout(()=>{
    const canvas=div.querySelector('#c-probability-toy');
    const ctx=canvas.getContext('2d');
    const resize=()=>{ canvas.width=canvas.offsetWidth*2; canvas.height=400*2; };
    resize();
    let dist='uniform', n=1, samples=[];
    const randDist=()=>{
      if(dist==='uniform') return Math.random();
      if(dist==='exp') return -Math.log(1-Math.random());
      if(dist==='bernoulli') return Math.random()<0.5?0:1;
      return Math.random();
    };
    const runCLT=()=>{
      const sums=[];
      for(let i=0;i<5000;i++){
        let s=0; for(let j=0;j<n;j++) s+=randDist();
        sums.push(s/n);
      }
      samples=sums;
      draw();
      const mean=sums.reduce((a,b)=>a+b)/sums.length;
      const variance=sums.reduce((a,b)=>a+(b-mean)*(b-mean),0)/sums.length;
      div.querySelector('#clt-info').textContent=`分布=${dist}, n=${n}, 样本5000个均值, 均值=${mean.toFixed(3)}, 方差=${variance.toFixed(4)}, 理论方差=${(1/12/n).toFixed(4)} (均匀分布), 当n增大，分布趋向正态(中心极限定理)`;
    };
    const draw=()=>{
      const w=canvas.width,h=canvas.height;
      ctx.clearRect(0,0,w,h);
      // histogram
      const bins=50;
      const min=Math.min(...samples), max=Math.max(...samples);
      const hist=new Array(bins).fill(0);
      samples.forEach(s=>{ const idx=Math.floor((s-min)/(max-min)*bins); if(idx>=0&&idx<bins) hist[idx]++; });
      const maxH=Math.max(...hist);
      hist.forEach((c,i)=>{
        const x=i/bins*w, y=h - c/maxH*h*0.8;
        ctx.fillStyle=`hsl(${50+i},100%,60%)`; ctx.fillRect(x,y,w/bins-2,h-y);
      });
      // normal curve overlay
      if(n>5){
        const mean=samples.reduce((a,b)=>a+b)/samples.length;
        const variance=samples.reduce((a,b)=>a+(b-mean)*(b-mean),0)/samples.length;
        const std=Math.sqrt(variance);
        ctx.strokeStyle='#00ff88'; ctx.lineWidth=3; ctx.beginPath();
        for(let x=0;x<w;x++){
          const val=min + x/w*(max-min);
          const norm=Math.exp(-0.5*(val-mean)*(val-mean)/(std*std))/(std*Math.sqrt(2*Math.PI));
          const y=h - norm* (w*0.5) *2;
          if(x==0) ctx.moveTo(x,y); else ctx.lineTo(x,y);
        } ctx.stroke();
        ctx.fillStyle='#00ff88'; ctx.font='12px monospace'; ctx.fillText('正态拟合',10,20);
      }
    };
    div.querySelector('#btn-clt').onclick=()=>{ n=1; const iv=setInterval(()=>{ n++; div.querySelector('#clt-n').textContent=n; runCLT(); if(n>=30) clearInterval(iv); },300); };
    div.querySelector('#btn-dist').onclick=()=>{ dist=dist==='uniform'?'exp':dist==='exp'?'bernoulli':'uniform'; runCLT(); };
    runCLT();
  },100);
  return div;
}
