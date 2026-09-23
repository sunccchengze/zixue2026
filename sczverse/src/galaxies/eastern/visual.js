
export function animate(canvas){
  if(!canvas) return;
  const ctx=canvas.getContext('2d');
  const resize=()=>{ canvas.width=canvas.offsetWidth*2; canvas.height=canvas.offsetHeight*2; };
  resize();
  let t=0;
  const draw=()=>{
    t+=0.02;
    const w=canvas.width, h=canvas.height;
    ctx.clearRect(0,0,w,h);
    // unique visual per discipline
    ctx.save();
    ctx.translate(w/2,h/2);
    if(d=='probability'): ctx.fillStyle='#ffcc00'; for(let i=0;i<200;i++){const a=Math.random()*Math.PI*2; const r=Math.random()*Math.min(w,h)*0.4; const x=Math.cos(a)*r + Math.sin(t+i)*10; const y=Math.sin(a)*r; ctx.globalAlpha=0.6; ctx.beginPath(); ctx.arc(x,y,2,0,Math.PI*2); ctx.fill();}
    // generic galaxy swirl
    for(let i=0;i<180;i++){
      const angle=i*0.1 + t;
      const radius=i*1.2;
      const x=Math.cos(angle)*radius;
      const y=Math.sin(angle)*radius*0.6;
      const hue=({'probability':50,'mathphys':190,'mechanics':30,'complex':270,'physics':140,'chemistry':340,'eastern':0,'papers':180,'english':40,'ai':160}['eastern']||200);
      ctx.fillStyle=`hsl(${hue + Math.sin(t+i*0.1)*20},100%,60%)`;
      ctx.globalAlpha=0.8 - i/250;
      ctx.beginPath(); ctx.arc(x,y,2+Math.sin(t+i)*1,0,Math.PI*2); ctx.fill();
    }
    ctx.restore();
    requestAnimationFrame(draw);
  }; draw();
}
