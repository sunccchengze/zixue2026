
export const SKIN_08 = {
  id:'skin-08',
  name:'小鹰变体 8',
  hue:240,
  softness:0.96,
  bounciness:0.71,
  eyes:{x:21.5, y:36.3},
  render(ctx,x,y,s){
    ctx.fillStyle=`hsl(240,70%,70%)`;
    ctx.beginPath(); ctx.ellipse(x,y,30*s,40*s,0,0,Math.PI*2); ctx.fill();
  }
};
