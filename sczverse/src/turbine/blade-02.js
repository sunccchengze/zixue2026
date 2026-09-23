
// Turbine blade profile 2
export const BLADE_02 = {
  id:2,
  chord:0.1289,
  stagger:26.89,
  thickness:0.0541,
  camber:0.0351,
  profile: Array.from({length:100},(_,j)=>{
    const x=j/100;
    return {x, y: Math.sin(x*Math.PI)*0.0399 + Math.sin(x*Math.PI*3)*0.005};
  }),
  efficiency:0.9107,
};
export function renderBlade(ctx, x, y, scale=1){
  ctx.save(); ctx.translate(x,y); ctx.scale(scale,scale);
  ctx.strokeStyle=`hsl(196,100%,60%)`; ctx.lineWidth=2;
  ctx.beginPath(); BLADE_02.profile.forEach((p,idx)=>{ if(idx==0) ctx.moveTo(p.x*100,p.y*100); else ctx.lineTo(p.x*100,p.y*100); }); ctx.stroke();
  ctx.restore();
}
