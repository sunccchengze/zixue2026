import { DISCIPLINES } from '../../data/disciplines.js';
export function render(){
  const d=DISCIPLINES.find(x=>x.id==='english');
  const div=document.createElement('div');
  div.innerHTML=`
    <h2>🌍 ${d.name} 星系</h2>
    <p><small>${d.desc} | ${d.location} | ${d.teacher}</small></p>
    <div style="display:grid;grid-template-columns:1fr 340px;gap:20px">
      <div>
        <div style="background:rgba(255,170,0,0.08);border:1px solid #ffaa00;border-radius:16px;padding:16px">
          <h3>📝 学术英语写作助手 - 真实可用</h3>
          <p style="font-size:11px;opacity:0.8">治国理政语料库第二卷150词摘抄，Research Presentation期末口试</p>
          <textarea id="eng-input" style="width:100%;height:100px;background:#0a0a14;border:1px solid #ffaa00;border-radius:8px;color:white;padding:8px;font-size:12px" placeholder="输入你的英文摘要，例如：Turbine blade aerodynamic optimization using surrogate model">Turbine blade aerodynamic optimization using Kriging surrogate model and NSGA-II algorithm. Efficiency improved by 3.2%.</textarea>
          <div style="display:flex;gap:8px;margin-top:8px">
            <button id="btn-eng-check" style="padding:4px 12px;border-radius:20px;border:1px solid #ffaa00;background:rgba(255,170,0,0.2);color:white;cursor:pointer">检查学术写作</button>
            <button id="btn-eng-vocab" style="padding:4px 12px;border-radius:20px;border:1px solid #ffaa00;background:rgba(255,170,0,0.2);color:white;cursor:pointer">词汇星系</button>
          </div>
          <div id="eng-output" style="margin-top:12px;font-size:11px;background:rgba(0,0,0,0.3);padding:12px;border-radius:8px;white-space:pre-wrap"></div>
          <canvas id="eng-canvas" style="width:100%;height:200px;background:#0a0a14;border-radius:12px;margin-top:12px"></canvas>
        </div>
      </div>
      <div>
        <div class="discipline-card"><b>16周课程表</b><br><small>blended learning: 4/6/8/13周线上SPOC<br>15-16周 research presentation=期末口试<br>第二课堂15分：词汇测试10-01~11-30唯一机会，听写，治国理政摘抄12-20前</small></div>
        <div class="discipline-card"><b>核心公式</b><br><div style="font-size:11px">${d.formulas.map(f=>`<div style="margin:2px 0;padding:4px;background:rgba(255,170,0,0.1);border-radius:4px">${f}</div>`).join('')}</div></div>
      </div>
    </div>
  `;
  setTimeout(()=>{
    const input=div.querySelector('#eng-input');
    const output=div.querySelector('#eng-output');
    const canvas=div.querySelector('#eng-canvas');
    const ctx=canvas.getContext('2d');
    const resize=()=>{ canvas.width=canvas.offsetWidth*2; canvas.height=200*2; };
    resize();
    const academicWords=['aerodynamic','optimization','surrogate','efficiency','turbine','algorithm','framework','methodology','analysis','validation','robust','novel','significant','demonstrate','investigate'];
    const checkWriting=()=>{
      const text=input.value;
      const words=text.split(/\s+/);
      let score=0, suggestions=[];
      if(text.length>50) score+=20;
      if(/[A-Z][a-z]+ [a-z]+/.test(text)) score+=10;
      const hasAcademic=academicWords.filter(w=>text.toLowerCase().includes(w)).length;
      score+=hasAcademic*5;
      if(text.includes('using')||text.includes('based on')) score+=10;
      if(text.split('.').length>1) score+=10;
      suggestions.push(`词汇: ${words.length}词, 学术词${hasAcademic}/${academicWords.length}`);
      suggestions.push(`被动语态: ${(text.match(/is|are|was|were|be|been/g)||[]).length}处`);
      suggestions.push(`建议: ${hasAcademic<3?'多用学术词汇如 aerodynamic/optimization/surrogate': '学术词汇丰富✅'}`);
      suggestions.push(`分数: ${Math.min(100,score)}/100 ${score>60?'✅':'需改进'}`);
      output.textContent=suggestions.join('\n');
      // vocab galaxy
      ctx.clearRect(0,0,canvas.width,canvas.height);
      words.forEach((w,i)=>{
        const x=(i/words.length)*canvas.width+20, y=canvas.height/2 + Math.sin(i)*30;
        const isAcademic=academicWords.includes(w.toLowerCase().replace(/[^a-z]/g,''));
        ctx.fillStyle=isAcademic?'#ffaa00':'rgba(255,255,255,0.3)';
        ctx.font=isAcademic?'bold 14px monospace':'12px monospace';
        ctx.fillText(w,x,y);
        if(isAcademic){
          ctx.beginPath(); ctx.arc(x,y-10,20,0,Math.PI*2); ctx.strokeStyle='rgba(255,170,0,0.3)'; ctx.stroke();
        }
      });
    };
    div.querySelector('#btn-eng-check').onclick=checkWriting;
    div.querySelector('#btn-eng-vocab').onclick=()=>{
      const vocab=['turbine','aerodynamic','surrogate','Kriging','NSGA-II','efficiency','pressure ratio','Pareto','UQ','RANS','optimization','blade','Rotor37','residual','MC Dropout'];
      output.textContent='词汇星系 (来自你的论文):\n'+vocab.map((v,i)=>`${i+1}. ${v} ${academicWords.includes(v.toLowerCase())?'⭐':''}`).join('\n');
    };
    checkWriting();
  },100);
  return div;
}
