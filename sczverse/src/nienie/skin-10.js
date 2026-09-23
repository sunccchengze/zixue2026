
export const SKIN_10 = {
  id:'skin-10',
  name:'小鹰变体 10',
  hue:300,
  softness:0.88,
  bounciness:0.40,
  eyes:{x:23.7, y:33.5},
  render(ctx,x,y,s){
    ctx.fillStyle=`hsl(300,70%,70%)`;
    ctx.beginPath(); ctx.ellipse(x,y,30*s,40*s,0,0,Math.PI*2); ctx.fill();
  }
};
