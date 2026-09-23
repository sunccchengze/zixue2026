
export const SKIN_05 = {
  id:'skin-05',
  name:'小鹰变体 5',
  hue:150,
  softness:0.89,
  bounciness:0.56,
  eyes:{x:35.5, y:30.2},
  render(ctx,x,y,s){
    ctx.fillStyle=`hsl(150,70%,70%)`;
    ctx.beginPath(); ctx.ellipse(x,y,30*s,40*s,0,0,Math.PI*2); ctx.fill();
  }
};
