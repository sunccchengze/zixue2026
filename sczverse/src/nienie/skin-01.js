
export const SKIN_01 = {
  id:'skin-01',
  name:'小鹰变体 1',
  hue:30,
  softness:0.61,
  bounciness:0.35,
  eyes:{x:38.2, y:25.2},
  render(ctx,x,y,s){
    ctx.fillStyle=`hsl(30,70%,70%)`;
    ctx.beginPath(); ctx.ellipse(x,y,30*s,40*s,0,0,Math.PI*2); ctx.fill();
  }
};
