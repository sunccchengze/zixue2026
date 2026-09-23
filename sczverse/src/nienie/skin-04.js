
export const SKIN_04 = {
  id:'skin-04',
  name:'小鹰变体 4',
  hue:120,
  softness:0.66,
  bounciness:0.48,
  eyes:{x:35.5, y:34.1},
  render(ctx,x,y,s){
    ctx.fillStyle=`hsl(120,70%,70%)`;
    ctx.beginPath(); ctx.ellipse(x,y,30*s,40*s,0,0,Math.PI*2); ctx.fill();
  }
};
