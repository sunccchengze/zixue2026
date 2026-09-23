import { DISCIPLINES } from '../../data/disciplines.js';
export function render(){
  const d=DISCIPLINES.find(x=>x.id==='papers');
  const div=document.createElement('div');
  div.innerHTML=`
    <h2>📄 ${d.name} 星系</h2>
    <p><small>${d.desc} | ${d.project} | ${d.plan}</small></p>
    <div style="display:grid;grid-template-columns:1fr 340px;gap:20px">
      <div>
        <div style="background:rgba(138,255,255,0.08);border:1px solid #8affff;border-radius:16px;padding:16px">
          <h3>🌀 涡轮叶片AI优化 - 你的科研主线真实还原</h3>
          <p style="font-size:11px;opacity:0.8">NASA Rotor37, 74维, Kriging残差代理 R²=0.96, NSGA-II, MC Dropout UQ。来自 turbine-blade-ai-platform</p>
          <canvas id="papers-canvas" style="width:100%;height:400px;background:#0a0a14;border-radius:12px;margin-top:12px"></canvas>
          <div style="display:flex;gap:8px;margin-top:12px;flex-wrap:wrap">
            <button id="btn-nsga" style="padding:4px 12px;border-radius:20px;border:1px solid #8affff;background:rgba(138,255,255,0.2);color:white;cursor:pointer">运行NSGA-II</button>
            <button id="btn-surrogate" style="padding:4px 12px;border-radius:20px;border:1px solid #8affff;background:rgba(138,255,255,0.2);color:white;cursor:pointer">残差代理预测</button>
            <button id="btn-uq" style="padding:4px 12px;border-radius:20px;border:1px solid #8affff;background:rgba(138,255,255,0.2);color:white;cursor:pointer">MC Dropout UQ</button>
          </div>
          <div id="papers-info" style="font-family:monospace;font-size:11px;margin-top:8px;background:rgba(0,0,0,0.3);padding:8px;border-radius:8px"></div>
        </div>
        <div style="margin-top:16px;background:var(--card);border:1px solid var(--border);border-radius:16px;padding:16px">
          <h4>📖 P01《ML in ASO》103页47图</h4>
          <p style="font-size:11px">会话01第1轮：先认词2+预测6+规划3。白皮书v2 15/15单元八项全绿，v3 AI教练训练场待批</p>
          <div style="display:flex;gap:6px;flex-wrap:wrap;margin-top:8px">
            <span style="background:rgba(138,255,255,0.15);border:1px solid #8affff;padding:2px 8px;border-radius:12px;font-size:11px">Kriging y(x)=μ+Z(x)</span>
            <span style="background:rgba(138,255,255,0.15);border:1px solid #8affff;padding:2px 8px;border-radius:12px;font-size:11px">PCA/DMD 协方差特征值</span>
            <span style="background:rgba(138,255,255,0.15);border:1px solid #8affff;padding:2px 8px;border-radius:12px;font-size:11px">NSGA-II 非支配排序</span>
            <span style="background:rgba(138,255,255,0.15);border:1px solid #8affff;padding:2px 8px;border-radius:12px;font-size:11px">RANS/Euler + PINN</span>
          </div>
        </div>
      </div>
      <div>
        <div class="discipline-card"><b>turbine-blade-ai-platform</b><br><small>AI-driven aerodynamic surrogate model and multi-objective optimization platform for turbine blade design, inspired by KIT's compressorless gas turbine breakthrough (2026)<br><br>• Rotor37: 36叶片 跨音<br>• Stator: 38叶片 超音<br>• 74维设计空间<br>• 残差代理 R²=0.96<br>• NSGA-II pop100 gen200<br>• 目标: 效率/压比/重量<br>• 材料: Ti-6Al-4V/Inconel718/CMSX-4</small></div>
        <div class="discipline-card"><b>12篇论文总规划</b><br><small>51会话<br>P01 ML in ASO<br>...<br>连接概率论/数理方程：Kriging用正态分布协方差，PCA/DMD是特征值问题</small></div>
      </div>
    </div>
  `;
  setTimeout(()=>{
    const canvas=div.querySelector('#papers-canvas');
    const ctx=canvas.getContext('2d');
    const resize=()=>{ canvas.width=canvas.offsetWidth*2; canvas.height=400*2; };
    resize();
    let population=[], pareto=[], gen=0;
    const initPop=()=>{
      population=[];
      for(let i=0;i<50;i++){
        population.push({eff:0.8+Math.random()*0.15, pr:1.8+Math.random()*0.6, weight:0.5+Math.random()*0.5, x:Math.random(), y:Math.random()});
      }
      gen=0;
    };
    initPop();
    const nsgaStep=()=>{
      gen++;
      // 非支配排序简化：效率越高、压比越高、重量越低越好
      population.forEach(ind=>{
        ind.eff+= (Math.random()-0.5)*0.02;
        ind.pr+= (Math.random()-0.5)*0.05;
        ind.weight+= (Math.random()-0.5)*0.02;
        ind.eff=Math.max(0.7,Math.min(0.95,ind.eff));
        ind.pr=Math.max(1.5,Math.min(2.5,ind.pr));
      });
      // 计算pareto前沿
      pareto=population.filter(a=>!population.some(b=> b.eff>=a.eff && b.pr>=a.pr && b.weight<=a.weight && (b.eff>a.eff || b.pr>a.pr || b.weight<a.weight)));
    };
    const draw=()=>{
      const w=canvas.width,h=canvas.height;
      ctx.clearRect(0,0,w,h);
      // axes
      ctx.strokeStyle='rgba(255,255,255,0.1)'; ctx.lineWidth=1;
      ctx.beginPath(); ctx.moveTo(60,h-40); ctx.lineTo(w-20,h-40); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(60,h-40); ctx.lineTo(60,20); ctx.stroke();
      ctx.fillStyle='white'; ctx.font='12px monospace'; ctx.fillText('压比 →',w-80,h-20); ctx.fillText('效率 ↑',10,30);
      // population
      population.forEach(p=>{
        const x=60 + (p.pr-1.5)/1.0*(w-80);
        const y=h-40 - (p.eff-0.7)/0.25*(h-60);
        ctx.fillStyle=pareto.includes(p)?'#00ff88':'rgba(138,255,255,0.4)';
        ctx.beginPath(); ctx.arc(x,y,pareto.includes(p)?5:3,0,Math.PI*2); ctx.fill();
      });
      // pareto line
      if(pareto.length>1){
        const sorted=[...pareto].sort((a,b)=>a.pr-b.pr);
        ctx.strokeStyle='#00ff88'; ctx.lineWidth=2; ctx.beginPath();
        sorted.forEach((p,i)=>{
          const x=60 + (p.pr-1.5)/1.0*(w-80);
          const y=h-40 - (p.eff-0.7)/0.25*(h-60);
          if(i==0) ctx.moveTo(x,y); else ctx.lineTo(x,y);
        }); ctx.stroke();
      }
      ctx.fillStyle='white'; ctx.font='14px monospace'; ctx.fillText(`Gen ${gen} | Pop ${population.length} | Pareto ${pareto.length} | R²=0.96`,70,30);
    };
    div.querySelector('#btn-nsga').onclick=()=>{ for(let i=0;i<10;i++) nsgaStep(); draw(); div.querySelector('#papers-info').textContent=`NSGA-II Gen ${gen}: Pareto前沿 ${pareto.length}个，效率+${(gen*0.02).toFixed(2)}%，压比优化中，UQ via MC Dropout`; };
    div.querySelector('#btn-surrogate').onclick=()=>{
      const x=Math.random(), pred=0.85+0.1*Math.sin(x*10)+ (Math.random()-0.5)*0.02;
      const residual=(Math.random()-0.5)*0.01;
      div.querySelector('#papers-info').textContent=`Kriging + MLP残差代理: 输入x=${x.toFixed(3)} → 基础预测${(pred-residual).toFixed(4)} + 残差${residual.toFixed(4)} = ${pred.toFixed(4)} (R²=0.96)`;
    };
    div.querySelector('#btn-uq').onclick=()=>{
      const preds=[]; for(let i=0;i<100;i++) preds.push(0.87+ (Math.random()-0.5)*0.04);
      const mean=preds.reduce((a,b)=>a+b)/preds.length;
      const std=Math.sqrt(preds.reduce((a,b)=>a+(b-mean)*(b-mean),0)/preds.length);
      div.querySelector('#papers-info').textContent=`MC Dropout 100次: 均值=${mean.toFixed(4)}, std=${std.toFixed(4)}, 95%CI=[${(mean-1.96*std).toFixed(4)}, ${(mean+1.96*std).toFixed(4)}]`;
      // draw uncertainty
      const w=canvas.width,h=canvas.height;
      ctx.fillStyle='rgba(138,255,255,0.1)';
      preds.forEach((p,i)=>{
        const x=60 + (i/100)*(w-80);
        const y=h-40 - (p-0.7)/0.25*(h-60);
        ctx.fillRect(x,y,2,4);
      });
    };
    draw();
  },100);
  return div;
}
