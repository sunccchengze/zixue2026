
// Turbine blade profile 11
export const BLADE_11 = {
  id:11,
  chord:0.1026,
  stagger:41.08,
  thickness:0.0689,
  camber:0.0306,
  profile: Array.from({length:100},(_,j)=>{
    const x=j/100;
    return {x, y: Math.sin(x*Math.PI)*0.0321 + Math.sin(x*Math.PI*3)*0.005};
  }),
  efficiency:0.8065,
};
export function renderBlade(ctx, x, y, scale=1){
  ctx.save(); ctx.translate(x,y); ctx.scale(scale,scale);
  ctx.strokeStyle=`hsl(268,100%,60%)`; ctx.lineWidth=2;
  ctx.beginPath(); BLADE_11.profile.forEach((p,idx)=>{ if(idx==0) ctx.moveTo(p.x*100,p.y*100); else ctx.lineTo(p.x*100,p.y*100); }); ctx.stroke();
  ctx.restore();
}
