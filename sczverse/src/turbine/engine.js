
export class TurbineEngine{
  constructor(){ this.thrust=0; this.rpm=0; }
  init(){ this.thrust= 7400 + Math.floor(Math.random()*1000); this.rpm=17188; this.renderMini(); }
  renderMini(){
    // little turbine in header maybe
  }
  showModal(){
    const modal=document.getElementById('modal');
    const content=document.getElementById('modal-content');
    modal.classList.remove('hidden');
    content.innerHTML=`
      <h2>🌀 涡轮星际引擎 · Turbine Interstellar Engine</h2>
      <p>NASA Rotor 37 · 74维气动优化 · Kriging残差代理 · NSGA-II · MC Dropout UQ</p>
      <div class="turbine-stage" id="turbine-stage">
        <div class="turbine-hub"></div>
      </div>
      <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:16px">
        <div class="discipline-card"><b>转速</b><br><span id="rpm">${this.rpm}</span> RPM</div>
        <div class="discipline-card"><b>压比</b><br>2.106</div>
        <div class="discipline-card"><b>效率</b><br>87.7%</div>
      </div>
      <p style="margin-top:12px"><small>灵感来自你的 turbine-blade-ai-platform，74维设计空间，残差代理R²=0.96。点击叶片加速！</small></p>
      <div class="game-controls"><button id="btn-spin">加速！</button><button id="btn-nsga">运行NSGA-II优化</button></div>
    `;
    const stage=document.getElementById('turbine-stage');
    for(let i=0;i<36;i++){
      const b=document.createElement('div'); b.className='blade';
      b.style.transform=`translate(-50%,-100%) rotate(${i*10}deg)`;
      b.style.color=`hsl(${180+i*2},100%,60%)`;
      stage.appendChild(b);
    }
    let angle=0;
    const spin=()=>{
      angle+=2;
      stage.querySelectorAll('.blade').forEach((bl,i)=>{
        bl.style.transform=`translate(-50%,-100%) rotate(${i*10+angle}deg)`;
      });
      requestAnimationFrame(spin);
    }; spin();
    document.getElementById('btn-spin').onclick=()=>{
      this.thrust+=100; document.getElementById('rpm').textContent= this.rpm+=200;
      for(let k=0;k<5;k++){ const f=document.createElement('div'); f.className='flow-line'; f.style.top=(20+Math.random()*60)+'%'; f.style.left='0'; f.style.width='100px'; stage.appendChild(f); setTimeout(()=>f.remove(),2000); }
    };
    document.getElementById('btn-nsga').onclick=()=>{
      const btn=document.getElementById('btn-nsga'); btn.textContent='优化中...';
      setTimeout(()=>{ btn.textContent='✅ Pareto前沿已收敛！效率+3.2%'; this.thrust+=500; },1500);
    };
  }
  superBurn(){
    this.thrust=114514; this.rpm=99999;
    document.body.style.filter='hue-rotate(180deg) saturate(2)';
    setTimeout(()=>document.body.style.filter='',3000);
  }
}
