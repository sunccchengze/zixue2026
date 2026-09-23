
export const SKIN_03 = {
  id:'skin-03',
  name:'小鹰变体 3',
  hue:90,
  softness:0.94,
  bounciness:0.58,
  eyes:{x:33.8, y:32.2},
  render(ctx,x,y,s){
    ctx.fillStyle=`hsl(90,70%,70%)`;
    ctx.beginPath(); ctx.ellipse(x,y,30*s,40*s,0,0,Math.PI*2); ctx.fill();
  }
};
