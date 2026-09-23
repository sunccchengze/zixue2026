
// Turbine blade profile 12
export const BLADE_12 = {
  id:12,
  chord:0.1270,
  stagger:36.51,
  thickness:0.0575,
  camber:0.0243,
  profile: Array.from({length:100},(_,j)=>{
    const x=j/100;
    return {x, y: Math.sin(x*Math.PI)*0.0620 + Math.sin(x*Math.PI*3)*0.005};
  }),
  efficiency:0.8876,
};
export function renderBlade(ctx, x, y, scale=1){
  ctx.save(); ctx.translate(x,y); ctx.scale(scale,scale);
  ctx.strokeStyle=`hsl(276,100%,60%)`; ctx.lineWidth=2;
  ctx.beginPath(); BLADE_12.profile.forEach((p,idx)=>{ if(idx==0) ctx.moveTo(p.x*100,p.y*100); else ctx.lineTo(p.x*100,p.y*100); }); ctx.stroke();
  ctx.restore();
}
