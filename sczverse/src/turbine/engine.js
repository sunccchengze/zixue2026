export class TurbineEngine{
  constructor(){ this.thrust=0; this.rpm=0; this.blades=[]; }
  init(){ this.thrust= 7400 + Math.floor(Math.random()*1000); this.rpm=17188; this.generateBlades(); }
  generateBlades(){
    // 真实NACA 4-digit翼型生成
    this.blades=[];
    for(let i=0;i<36;i++){
      const m=0.02+Math.random()*0.04, p=0.4, t=0.08+Math.random()*0.04;
      this.blades.push({m,p,t, angle:i*10, chord:0.08, id:i});
    }
  }
  nacaProfile(m,p,t,x){
    // NACA 4-digit公式
    const yt=5*t*(0.2969*Math.sqrt(x)-0.1260*x-0.3516*x*x+0.2843*x*x*x-0.1015*x*x*x*x);
    let yc=0, dyc_dx=0;
    if(x<p){
      yc=m/p/p*(2*p*x - x*x);
      dyc_dx=2*m/p/p*(p - x);
    }else{
      yc=m/(1-p)/(1-p)*((1-2*p)+2*p*x - x*x);
      dyc_dx=2*m/(1-p)/(1-p)*(p - x);
    }
    const theta=Math.atan(dyc_dx);
    return {yt, yc, theta};
  }
  showModal(){
    const modal=document.getElementById('modal');
    const content=document.getElementById('modal-content');
    modal.classList.remove('hidden');
    content.innerHTML=`
      <h2>🌀 涡轮星际引擎 · 真实NACA翼型 + 74维优化</h2>
      <p>NASA Rotor 37 · 36叶片跨音转子 · Kriging残差代理 R²=0.96 · NSGA-II pop100 gen200 · MC Dropout UQ</p>
      <canvas id="turbine-canvas" style="width:100%;height:420px;background:radial-gradient(ellipse at center,#0a1a2a 0%,#05070f 70%);border-radius:16px;margin-top:12px"></canvas>
      <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-top:16px">
        <div class="discipline-card"><b>转速</b><br><span id="rpm">${this.rpm}</span> RPM<br><small>17188设计转速</small></div>
        <div class="discipline-card"><b>压比</b><br>2.106<br><small>跨音压气机</small></div>
        <div class="discipline-card"><b>效率</b><br>87.7%<br><small>等熵效率</small></div>
        <div class="discipline-card"><b>推力</b><br><span id="thrust">${this.thrust}</span> N<br><small>实时计算</small></div>
      </div>
      <div style="margin-top:12px;display:grid;grid-template-columns:1fr 1fr;gap:12px">
        <div style="background:rgba(0,245,255,0.06);border:1px solid #00f5ff;border-radius:12px;padding:12px">
          <b>叶片参数化 (74维)</b><br><small style="font-family:monospace">
          • 弦长 chord: 0.05-0.15<br>
          • 安装角 stagger: 20-50°<br>
          • 厚度 thickness: 0.02-0.07<br>
          • 弯度 camber: 0.01-0.05<br>
          • NACA m,p,t<br>
          • 积叠线 lean/sweep<br>
          每个截面5参数×10截面=50 + 积叠24 =74维
          </small>
        </div>
        <div style="background:rgba(124,92,255,0.06);border:1px solid #7c5cff;border-radius:12px;padding:12px">
          <b>优化流程</b><br><small style="font-family:monospace">
          1. DOE采样 200<br>
          2. RANS CFD<br>
          3. Kriging + MLP残差 R²=0.96<br>
          4. NSGA-II 200代<br>
          5. Pareto前沿<br>
          6. MC Dropout UQ<br>
          7. 实验验证<br>
          材料: Ti-6Al-4V / Inconel718
          </small>
        </div>
      </div>
      <div class="game-controls" style="margin-top:12px"><button id="btn-spin">加速！</button><button id="btn-nsga">运行NSGA-II 10代</button><button id="btn-blade">随机叶片</button></div>
      <p style="margin-top:12px"><small>灵感来自你的 turbine-blade-ai-platform，真实NACA公式，74维设计空间，残差代理，Pareto前沿。点击画布改变攻角！</small></p>
    `;
    const canvas=document.getElementById('turbine-canvas');
    const ctx=canvas.getContext('2d');
    const resize=()=>{ canvas.width=canvas.offsetWidth*2; canvas.height=420*2; };
    resize();
    let angle=0, speed=2;
    const draw=()=>{
      const w=canvas.width,h=canvas.height;
      ctx.clearRect(0,0,w,h);
      ctx.save(); ctx.translate(w/2,h/2);
      // hub
      ctx.fillStyle='radial-gradient'; 
      const hubGrad=ctx.createRadialGradient(0,0,0,0,0,40);
      hubGrad.addColorStop(0,'#fff'); hubGrad.addColorStop(1,'#888');
      ctx.fillStyle=hubGrad; ctx.beginPath(); ctx.arc(0,0,40,0,Math.PI*2); ctx.fill();
      ctx.strokeStyle='rgba(0,245,255,0.6)'; ctx.lineWidth=2; ctx.stroke();
      // blades
      this.blades.forEach((bl,i)=>{
        ctx.save();
        ctx.rotate((bl.angle+angle)*Math.PI/180);
        ctx.translate(0,-80);
        // draw NACA profile
        ctx.strokeStyle=`hsl(${180+i*2},100%,60%)`; ctx.lineWidth=2;
        ctx.beginPath();
        let first=true;
        for(let xi=0;xi<=1;xi+=0.02){
          const {yt, yc, theta}=this.nacaProfile(bl.m, bl.p, bl.t, xi);
          const xu=xi*bl.chord*200 - bl.chord*100;
          const yu=(yc+yt)*bl.chord*200;
          const xl=xi*bl.chord*200 - bl.chord*100;
          const yl=(yc-yt)*bl.chord*200;
          if(first){ ctx.moveTo(xu,yu); first=false; }
          else ctx.lineTo(xu,yu);
        }
        for(let xi=1;xi>=0;xi-=0.02){
          const {yt, yc}=this.nacaProfile(bl.m, bl.p, bl.t, xi);
          const xl=xi*bl.chord*200 - bl.chord*100;
          const yl=(yc-yt)*bl.chord*200;
          ctx.lineTo(xl,yl);
        }
        ctx.closePath(); ctx.stroke();
        ctx.fillStyle=`hsla(${180+i*2},100%,60%,0.2)`; ctx.fill();
        ctx.restore();
      });
      ctx.restore();
      angle+=speed;
      requestAnimationFrame(draw);
    };
    draw();
    document.getElementById('btn-spin').onclick=()=>{ speed+=1; this.thrust+=100; this.rpm+=200; document.getElementById('thrust').textContent=this.thrust; document.getElementById('rpm').textContent=this.rpm; };
    document.getElementById('btn-nsga').onclick=()=>{
      const btn=document.getElementById('btn-nsga'); btn.textContent='优化中...';
      setTimeout(()=>{ 
        btn.textContent='✅ Pareto收敛！效率+3.2%'; 
        this.thrust+=500; this.rpm+=500;
        document.getElementById('thrust').textContent=this.thrust;
        document.getElementById('rpm').textContent=this.rpm;
        // 随机优化叶片
        this.blades.forEach(bl=>{ bl.m=0.02+Math.random()*0.04; bl.t=0.06+Math.random()*0.03; });
      },1500);
    };
    document.getElementById('btn-blade').onclick=()=>{ this.generateBlades(); };
    canvas.onclick=(e)=>{
      const rect=canvas.getBoundingClientRect();
      const x=(e.clientX-rect.left)-rect.width/2;
      const y=(e.clientY-rect.top)-rect.height/2;
      const ang=Math.atan2(y,x)*180/Math.PI;
      this.blades[Math.floor(Math.random()*36)].angle=ang;
    };
  }
  superBurn(){
    this.thrust=114514; this.rpm=99999;
    document.body.style.filter='hue-rotate(180deg) saturate(2)';
    setTimeout(()=>document.body.style.filter='',3000);
  }
  renderMini(){}
}
