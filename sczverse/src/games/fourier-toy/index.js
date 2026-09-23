export function render(){
  const div=document.createElement('div');
  div.innerHTML=`
    <h3>✏️ 傅里叶画画 - 用圆周画出任意图形</h3>
    <p><small>傅里叶级数: f(t)=Σ c_n e^{int}, 来自你复变与数理方程的积分变换。点击画布绘制路径</small></p>
    <canvas id="c-fourier-toy" class="game-canvas" style="height:500px"></canvas>
    <div class="game-controls">
      <button id="btn-draw">✏️ 绘制模式</button>
      <button id="btn-fourier">▶️ 傅里叶分解</button>
      <label style="font-size:11px">圆数 <input type="range" id="fourier-n" min="1" max="100" value="20" style="width:80px"> <span id="fourier-n-v">20</span></label>
      <button id="btn-clear">清空</button>
    </div>
    <div id="fourier-info" style="font-family:monospace;font-size:11px;margin-top:8px;background:rgba(0,0,0,0.3);padding:8px;border-radius:8px"></div>
  `;
  setTimeout(()=>{
    const canvas=div.querySelector('#c-fourier-toy');
    const ctx=canvas.getContext('2d');
    const resize=()=>{ canvas.width=canvas.offsetWidth*2; canvas.height=500*2; };
    resize();
    let path=[], drawing=false, coeffs=[], t=0, drawingMode=true;
    canvas.onpointerdown=(e)=>{
      if(!drawingMode) return;
      drawing=true; path=[];
      const rect=canvas.getBoundingClientRect();
      const x=(e.clientX-rect.left)*2, y=(e.clientY-rect.top)*2;
      path.push({x,y});
    };
    canvas.onpointermove=(e)=>{
      if(!drawing||!drawingMode) return;
      const rect=canvas.getBoundingClientRect();
      const x=(e.clientX-rect.left)*2, y=(e.clientY-rect.top)*2;
      path.push({x,y});
      drawPath();
    };
    canvas.onpointerup=()=>{ drawing=false; if(path.length>10) computeFourier(); };
    const drawPath=()=>{
      const w=canvas.width,h=canvas.height;
      ctx.clearRect(0,0,w,h);
      ctx.strokeStyle='#00f5ff'; ctx.lineWidth=3; ctx.beginPath();
      path.forEach((p,i)=>{ if(i==0) ctx.moveTo(p.x,p.y); else ctx.lineTo(p.x,p.y); }); ctx.stroke();
    };
    const computeFourier=()=>{
      const N=path.length;
      const numCoeffs=parseInt(div.querySelector('#fourier-n').value);
      coeffs=[];
      for(let k=-numCoeffs;k<=numCoeffs;k++){
        let re=0, im=0;
        for(let n=0;n<N;n++){
          const angle=-2*Math.PI*k*n/N;
          re+=path[n].x*Math.cos(angle)-path[n].y*Math.sin(angle);
          im+=path[n].x*Math.sin(angle)+path[n].y*Math.cos(angle);
        }
        re/=N; im/=N;
        coeffs.push({k, re, im, amp:Math.hypot(re,im), phase:Math.atan2(im,re)});
      }
      coeffs.sort((a,b)=>b.amp-a.amp);
      div.querySelector('#fourier-info').textContent=`路径点数=${N}, 傅里叶系数${coeffs.length}个, 最大振幅=${coeffs[0]?.amp.toFixed(1)}, 基频对应圆`;
      t=0;
    };
    const animateFourier=()=>{
      if(coeffs.length===0) return;
      const w=canvas.width,h=canvas.height;
      ctx.clearRect(0,0,w,h);
      // original path faint
      ctx.strokeStyle='rgba(255,255,255,0.1)'; ctx.lineWidth=1; ctx.beginPath();
      path.forEach((p,i)=>{ if(i==0) ctx.moveTo(p.x,p.y); else ctx.lineTo(p.x,p.y); }); ctx.stroke();
      // epicycles
      let x=w/2, y=h/2;
      const num=parseInt(div.querySelector('#fourier-n').value);
      for(let i=0;i<Math.min(num,coeffs.length);i++){
        const c=coeffs[i];
        const angle=c.k*t + c.phase;
        const nx=x + c.amp*Math.cos(angle);
        const ny=y + c.amp*Math.sin(angle);
        ctx.strokeStyle=`hsla(${(i*20)%360},80%,60%,0.3)`; ctx.lineWidth=1;
        ctx.beginPath(); ctx.arc(x,y,c.amp,0,Math.PI*2); ctx.stroke();
        ctx.strokeStyle=`hsl(${(i*20)%360},100%,60%)`; ctx.lineWidth=2;
        ctx.beginPath(); ctx.moveTo(x,y); ctx.lineTo(nx,ny); ctx.stroke();
        x=nx; y=ny;
      }
      ctx.fillStyle='#00ff88'; ctx.beginPath(); ctx.arc(x,y,4,0,Math.PI*2); ctx.fill();
      t+=0.02;
      if(!drawingMode) requestAnimationFrame(animateFourier);
    };
    div.querySelector('#btn-draw').onclick=()=>{ drawingMode=true; };
    div.querySelector('#btn-fourier').onclick=()=>{ drawingMode=false; t=0; animateFourier(); };
    div.querySelector('#btn-clear').onclick=()=>{ path=[]; coeffs=[]; ctx.clearRect(0,0,canvas.width,canvas.height); };
    div.querySelector('#fourier-n').oninput=(e)=>{ div.querySelector('#fourier-n-v').textContent=e.target.value; if(coeffs.length>0) computeFourier(); };
    // default star path
    const w=600,h=500;
    for(let a=0;a<Math.PI*2;a+=0.1){ const r=100+30*Math.sin(a*5); path.push({x:w+Math.cos(a)*r, y:h+Math.sin(a)*r}); }
    drawPath(); computeFourier();
  },100);
  return div;
}
