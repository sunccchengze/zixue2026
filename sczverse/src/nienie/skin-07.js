
export const SKIN_07 = {
  id:'skin-07',
  name:'小鹰变体 7',
  hue:210,
  softness:0.65,
  bounciness:0.67,
  eyes:{x:35.6, y:26.6},
  render(ctx,x,y,s){
    ctx.fillStyle=`hsl(210,70%,70%)`;
    ctx.beginPath(); ctx.ellipse(x,y,30*s,40*s,0,0,Math.PI*2); ctx.fill();
  }
};
