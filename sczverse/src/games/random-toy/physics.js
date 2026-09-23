
// 随机游走 physics
export function start(canvas){
  if(!canvas) return;
  const ctx=canvas.getContext('2d');
  const resize=()=>{ canvas.width=canvas.offsetWidth*2; canvas.height=canvas.offsetHeight*2; };
  resize();
  let t=0, particles=[];
  canvas.onpointermove = (e)=>{
    const rect=canvas.getBoundingClientRect();
    const x=(e.clientX-rect.left)*2, y=(e.clientY-rect.top)*2;
    for(let i=0;i<3;i++) particles.push({x,y,vx:(Math.random()-0.5)*6,vy:(Math.random()-0.5)*6,life:1,color:`hsl(${Math.random()*60+262},100%,60%)`});
  };
  canvas.onclick = (e)=>{
    const rect=canvas.getBoundingClientRect();
    const x=(e.clientX-rect.left)*2, y=(e.clientY-rect.top)*2;
    for(let i=0;i<20;i++) particles.push({x,y,vx:(Math.random()-0.5)*10,vy:(Math.random()-0.5)*10,life:1,color:`hsl(${Math.random()*360},100%,60%)`});
  };
  function loop(){
    t+=0.02;
    const w=canvas.width, h=canvas.height;
    ctx.fillStyle='rgba(10,10,20,0.1)'; ctx.fillRect(0,0,w,h);
    // 随机游走 specific
    ctx.save(); ctx.translate(w/2,h/2);
    for(let i=0;i<50;i++){ const a=i*0.2+t; const r=100+Math.sin(t+i*0.1)*20; ctx.fillStyle=`hsl({(i*5+t*20)%360},100%,60%)`; ctx.beginPath(); ctx.arc(Math.cos(a)*r,Math.sin(a)*r,3,0,Math.PI*2); ctx.fill(); }
    
    
    ctx.restore();
    particles=particles.filter(p=>p.life>0);
    for(const p of particles){
      p.x+=p.vx; p.y+=p.vy; p.vy+=0.1; p.life-=0.015;
      ctx.globalAlpha=p.life; ctx.fillStyle=p.color;
      ctx.beginPath(); ctx.arc(p.x,p.y,4,0,Math.PI*2); ctx.fill();
    }
    requestAnimationFrame(loop);
  } loop();
}
