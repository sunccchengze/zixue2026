
export const SKIN_00 = {
  id:'skin-00',
  name:'小鹰变体 0',
  hue:0,
  softness:0.62,
  bounciness:0.54,
  eyes:{x:25.8, y:26.9},
  render(ctx,x,y,s){
    ctx.fillStyle=`hsl(0,70%,70%)`;
    ctx.beginPath(); ctx.ellipse(x,y,30*s,40*s,0,0,Math.PI*2); ctx.fill();
  }
};
