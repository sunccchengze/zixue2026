
export const SKIN_11 = {
  id:'skin-11',
  name:'小鹰变体 11',
  hue:330,
  softness:0.62,
  bounciness:0.92,
  eyes:{x:24.4, y:26.8},
  render(ctx,x,y,s){
    ctx.fillStyle=`hsl(330,70%,70%)`;
    ctx.beginPath(); ctx.ellipse(x,y,30*s,40*s,0,0,Math.PI*2); ctx.fill();
  }
};
