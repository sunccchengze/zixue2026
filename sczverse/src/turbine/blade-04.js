
// Turbine blade profile 4
export const BLADE_04 = {
  id:4,
  chord:0.0664,
  stagger:40.51,
  thickness:0.0482,
  camber:0.0332,
  profile: Array.from({length:100},(_,j)=>{
    const x=j/100;
    return {x, y: Math.sin(x*Math.PI)*0.0626 + Math.sin(x*Math.PI*3)*0.005};
  }),
  efficiency:0.8291,
};
export function renderBlade(ctx, x, y, scale=1){
  ctx.save(); ctx.translate(x,y); ctx.scale(scale,scale);
  ctx.strokeStyle=`hsl(212,100%,60%)`; ctx.lineWidth=2;
  ctx.beginPath(); BLADE_04.profile.forEach((p,idx)=>{ if(idx==0) ctx.moveTo(p.x*100,p.y*100); else ctx.lineTo(p.x*100,p.y*100); }); ctx.stroke();
  ctx.restore();
}
