
export const CYCLE_06 = {
  name:["卡诺","布雷顿","朗肯","奥托","狄塞尔"][6%5]+"循环 6",
  efficiency:0.663,
  render(ctx,w,h,t){
    ctx.strokeStyle=`hsl(216,100%,60%)`; ctx.lineWidth=2;
    ctx.beginPath();
    for(let a=0;a<Math.PI*2;a+=0.05){
      const r=80+Math.sin(a*2+t)*20;
      const x=w/2+Math.cos(a)*r, y=h/2+Math.sin(a)*r;
      if(a==0) ctx.moveTo(x,y); else ctx.lineTo(x,y);
    } ctx.closePath(); ctx.stroke();
  }
};
