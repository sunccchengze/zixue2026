
export function inkWash(ctx,w,h,t){
  ctx.fillStyle='rgba(10,10,10,0.04)';
  ctx.fillRect(0,0,w,h);
  for(let i=0;i<3;i++){
    const x=w*0.5+Math.sin(t+i)*100, y=h*0.5+Math.cos(t*0.7+i)*80, r=50+Math.sin(t+i)*20;
    const grad=ctx.createRadialGradient(x,y,0,x,y,r);
    grad.addColorStop(0,`hsla(${30+i*20},20%,20%,0.1)`);
    grad.addColorStop(1,'transparent');
    ctx.fillStyle=grad;
    ctx.beginPath(); ctx.arc(x,y,r,0,Math.PI*2); ctx.fill();
  }
}
