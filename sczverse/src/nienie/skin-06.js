
export const SKIN_06 = {
  id:'skin-06',
  name:'小鹰变体 6',
  hue:180,
  softness:0.88,
  bounciness:0.94,
  eyes:{x:32.2, y:38.0},
  render(ctx,x,y,s){
    ctx.fillStyle=`hsl(180,70%,70%)`;
    ctx.beginPath(); ctx.ellipse(x,y,30*s,40*s,0,0,Math.PI*2); ctx.fill();
  }
};
