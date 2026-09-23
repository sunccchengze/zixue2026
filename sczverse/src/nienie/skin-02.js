
export const SKIN_02 = {
  id:'skin-02',
  name:'小鹰变体 2',
  hue:60,
  softness:0.66,
  bounciness:0.86,
  eyes:{x:21.3, y:33.5},
  render(ctx,x,y,s){
    ctx.fillStyle=`hsl(60,70%,70%)`;
    ctx.beginPath(); ctx.ellipse(x,y,30*s,40*s,0,0,Math.PI*2); ctx.fill();
  }
};
