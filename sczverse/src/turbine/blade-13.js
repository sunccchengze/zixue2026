
// Turbine blade profile 13
export const BLADE_13 = {
  id:13,
  chord:0.0873,
  stagger:28.48,
  thickness:0.0268,
  camber:0.0185,
  profile: Array.from({length:100},(_,j)=>{
    const x=j/100;
    return {x, y: Math.sin(x*Math.PI)*0.0219 + Math.sin(x*Math.PI*3)*0.005};
  }),
  efficiency:0.9250,
};
export function renderBlade(ctx, x, y, scale=1){
  ctx.save(); ctx.translate(x,y); ctx.scale(scale,scale);
  ctx.strokeStyle=`hsl(284,100%,60%)`; ctx.lineWidth=2;
  ctx.beginPath(); BLADE_13.profile.forEach((p,idx)=>{ if(idx==0) ctx.moveTo(p.x*100,p.y*100); else ctx.lineTo(p.x*100,p.y*100); }); ctx.stroke();
  ctx.restore();
}
