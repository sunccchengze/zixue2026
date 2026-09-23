
export const SKIN_09 = {
  id:'skin-09',
  name:'小鹰变体 9',
  hue:270,
  softness:0.65,
  bounciness:0.85,
  eyes:{x:34.1, y:25.6},
  render(ctx,x,y,s){
    ctx.fillStyle=`hsl(270,70%,70%)`;
    ctx.beginPath(); ctx.ellipse(x,y,30*s,40*s,0,0,Math.PI*2); ctx.fill();
  }
};
