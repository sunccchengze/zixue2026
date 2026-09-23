export function render(){
  const div=document.createElement('div');
  div.innerHTML=`
    <h3>💧 流体玩具 - 真实涡旋模拟</h3>
    <p><small>Navier-Stokes简化，手指划过产生涡旋，来自你数理方程与涡轮叶片的流体直觉</small></p>
    <canvas id="c-fluid-toy" class="game-canvas" style="height:400px"></canvas>
    <div class="game-controls">
      <button id="btn-fluid-clear">清空</button>
      <span style="font-size:11px;opacity:0.6">拖拽产生涡旋，涡量ω=∇×v</span>
    </div>
  `;
  setTimeout(()=>{
    const canvas=div.querySelector('#c-fluid-toy');
    const ctx=canvas.getContext('2d');
    const resize=()=>{ canvas.width=canvas.offsetWidth*2; canvas.height=400*2; };
    resize();
    const N=80;
    let u=new Array(N*N).fill(0), v=new Array(N*N).fill(0), dens=new Array(N*N).fill(0);
    const idx=(x,y)=>x+y*N;
    const addVortex=(x,y,dx,dy)=>{
      const gx=Math.floor(x/canvas.width*N), gy=Math.floor(y/canvas.height*N);
      for(let i=-2;i<=2;i++) for(let j=-2;j<=2;j++){
        const ix=gx+i, iy=gy+j;
        if(ix>=0&&ix<N&&iy>=0&&iy<N){
          u[idx(ix,iy)]+=dx*0.5;
          v[idx(ix,iy)]+=dy*0.5;
          dens[idx(ix,iy)]+=50;
        }
      }
    };
    let lastX=0,lastY=0;
    canvas.onpointermove=(e)=>{
      if(e.buttons!==1) return;
      const rect=canvas.getBoundingClientRect();
      const x=(e.clientX-rect.left)*2, y=(e.clientY-rect.top)*2;
      const dx=x-lastX, dy=y-lastY;
      addVortex(x,y,dx,dy);
      lastX=x; lastY=y;
    };
    canvas.onpointerdown=(e)=>{
      const rect=canvas.getBoundingClientRect();
      lastX=(e.clientX-rect.left)*2; lastY=(e.clientY-rect.top)*2;
    };
    const step=()=>{
      // simple advection & diffusion
      const unew=[...u], vnew=[...v], dnew=[...dens];
      for(let y=1;y<N-1;y++) for(let x=1;x<N-1;x++){
        const i=idx(x,y);
        const lapU=u[idx(x+1,y)]+u[idx(x-1,y)]+u[idx(x,y+1)]+u[idx(x,y-1)]-4*u[i];
        const lapV=v[idx(x+1,y)]+v[idx(x-1,y)]+v[idx(x,y+1)]+v[idx(x,y-1)]-4*v[i];
        unew[i]=u[i]+lapU*0.01;
        vnew[i]=v[i]+lapV*0.01;
        dnew[i]=dens[i]*0.995;
      }
      u=unew; v=vnew; dens=dnew;
    };
    const draw=()=>{
      const w=canvas.width,h=canvas.height;
      ctx.fillStyle='rgba(10,10,20,0.15)'; ctx.fillRect(0,0,w,h);
      const cellW=w/N, cellH=h/N;
      for(let y=0;y<N;y++) for(let x=0;x<N;x++){
        const d=dens[idx(x,y)];
        if(d>1){
          const speed=Math.hypot(u[idx(x,y)],v[idx(x,y)]);
          ctx.fillStyle=`hsla(${180+speed*5},100%,60%,${Math.min(1,d/100)})`;
          ctx.fillRect(x*cellW,y*cellH,cellW,cellH);
        }
      }
      // velocity arrows sparse
      ctx.strokeStyle='rgba(255,255,255,0.2)'; ctx.lineWidth=1;
      for(let y=0;y<N;y+=6) for(let x=0;x<N;x+=6){
        const i=idx(x,y);
        const ux=u[i], vy=v[i];
        if(Math.hypot(ux,vy)>0.5){
          const px=x*cellW, py=y*cellH;
          ctx.beginPath(); ctx.moveTo(px,py); ctx.lineTo(px+ux*2,py+vy*2); ctx.stroke();
        }
      }
    };
    const loop=()=>{ step(); draw(); requestAnimationFrame(loop); };
    div.querySelector('#btn-fluid-clear').onclick=()=>{ u.fill(0); v.fill(0); dens.fill(0); };
    loop();
  },100);
  return div;
}
