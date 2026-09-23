import { DISCIPLINES } from '../../data/disciplines.js';
export function render(){
  const d=DISCIPLINES.find(x=>x.id==='mathphys');
  const div=document.createElement('div');
  div.innerHTML=`
    <h2>🌊 ${d.name} 星系</h2>
    <p><small>${d.desc} | ${d.location}</small></p>
    <div style="display:grid;grid-template-columns:1fr 340px;gap:20px">
      <div>
        <div style="background:rgba(0,245,255,0.08);border:1px solid #00f5ff;border-radius:16px;padding:16px">
          <h3>🌊 波动方程求解器 - 分离变量法可视化</h3>
          <p style="font-size:11px;opacity:0.8">u_tt = a² u_xx, 定解=方程+初值+边值, u=XT。来自你定解问题校准</p>
          <canvas id="wave-canvas" style="width:100%;height:400px;background:#0a0a14;border-radius:12px;margin-top:12px;cursor:crosshair"></canvas>
          <div style="display:flex;gap:8px;margin-top:12px;flex-wrap:wrap">
            <button id="btn-pluck" style="padding:4px 12px;border-radius:20px;border:1px solid #00f5ff;background:rgba(0,245,255,0.2);color:white;cursor:pointer">拨弦</button>
            <button id="btn-heat" style="padding:4px 12px;border-radius:20px;border:1px solid #ff8a00;background:rgba(255,138,0,0.2);color:white;cursor:pointer">热传导模式</button>
            <label style="font-size:11px">a=<span id="a-val">1</span> <input type="range" id="a-slider" min="0.2" max="3" value="1" step="0.1" style="width:80px"></label>
          </div>
          <div id="wave-info" style="font-family:monospace;font-size:11px;margin-top:8px;background:rgba(0,0,0,0.3);padding:8px;border-radius:8px"></div>
        </div>
      </div>
      <div>
        <div class="discipline-card"><b>核心公式</b><br><div style="font-family:monospace;font-size:11px">${d.formulas.map(f=>`<div style="margin:2px 0;padding:4px;background:rgba(0,245,255,0.1);border-radius:4px">${f}</div>`).join('')}</div></div>
        <div class="discipline-card"><b>定解问题</b><br><small>• 波动: 弦振动, 声波, 需初位移+初速度<br>• 热传导: 温度扩散, 需初温<br>• 拉普拉斯: 稳态, 需边界<br>• 分离变量: 设u=X(x)T(t), 得常微分方程</small></div>
      </div>
    </div>
  `;
  setTimeout(()=>{
    const canvas=div.querySelector('#wave-canvas');
    const ctx=canvas.getContext('2d');
    const resize=()=>{ canvas.width=canvas.offsetWidth*2; canvas.height=400*2; };
    resize();
    let mode='wave', a=1, t=0, u=new Array(200).fill(0), ut=new Array(200).fill(0);
    const L=1, dx=L/u.length, c2=a*a;
    const initPluck=()=>{ for(let i=0;i<u.length;i++){ const x=i/u.length; u[i]=Math.sin(Math.PI*x)*0.8 + 0.3*Math.sin(2*Math.PI*x); ut[i]=0; } };
    initPluck();
    const step=()=>{
      t+=0.01;
      if(mode==='wave'){
        // 有限差分波动方程
        const unew=[...u];
        for(let i=1;i<u.length-1;i++){
          const lap=(u[i+1]-2*u[i]+u[i-1])/(dx*dx);
          unew[i]=2*u[i]- (u[i]||0) + c2*lap*0.0001; // 简化，实际需存两步
          // 更稳定：用速度
          ut[i]+=c2*lap*0.001;
          unew[i]+=ut[i]*0.01;
        }
        unew[0]=0; unew[unew.length-1]=0;
        u=unew;
      }else{
        // 热传导 u_t = a² u_xx
        const unew=[...u];
        for(let i=1;i<u.length-1;i++){
          const lap=(u[i+1]-2*u[i]+u[i-1])/(dx*dx);
          unew[i]=u[i]+a*lap*0.001;
        }
        u=unew;
      }
    };
    const draw=()=>{
      const w=canvas.width,h=canvas.height;
      ctx.clearRect(0,0,w,h);
      ctx.strokeStyle='rgba(255,255,255,0.05)';
      for(let y=0;y<h;y+=40){ ctx.beginPath(); ctx.moveTo(0,y); ctx.lineTo(w,y); ctx.stroke(); }
      // draw u
      ctx.strokeStyle=mode==='wave'?'#00f5ff':'#ff8a00'; ctx.lineWidth=3; ctx.beginPath();
      u.forEach((val,i)=>{ const x=i/u.length*w; const y=h/2 - val*h*0.4; if(i==0) ctx.moveTo(x,y); else ctx.lineTo(x,y); }); ctx.stroke();
      // fill
      ctx.lineTo(w,h/2); ctx.lineTo(0,h/2); ctx.closePath(); ctx.fillStyle=mode==='wave'?'rgba(0,245,255,0.1)':'rgba(255,138,0,0.1)'; ctx.fill();
      ctx.fillStyle='white'; ctx.font='14px monospace'; ctx.fillText(`${mode==='wave'?'波动 u_tt=a²u_xx':'热传导 u_t=a²u_xx'} a=${a.toFixed(1)} t=${t.toFixed(2)}`,10,20);
      div.querySelector('#wave-info').textContent=`L=1, ${u.length}点有限差分, ${mode==='wave'?'固定端 u=0':'Dirichlet'}边界, 当前max|u|=${Math.max(...u.map(Math.abs)).toFixed(3)}`;
    };
    const loop=()=>{ step(); draw(); requestAnimationFrame(loop); };
    div.querySelector('#btn-pluck').onclick=()=>{ mode='wave'; initPluck(); };
    div.querySelector('#btn-heat').onclick=()=>{ mode='heat'; for(let i=0;i<u.length;i++){ const x=i/u.length; u[i]=x<0.5?1:0; } };
    div.querySelector('#a-slider').oninput=(e)=>{ a=parseFloat(e.target.value); div.querySelector('#a-val').textContent=a; };
    canvas.onclick=(e)=>{ const rect=canvas.getBoundingClientRect(); const x=(e.clientX-rect.left)/rect.width; const idx=Math.floor(x*u.length); u[idx]+=0.5; };
    loop();
  },100);
  return div;
}
