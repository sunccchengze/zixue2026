
// Turbine blade profile 3
export const BLADE_03 = {
  id:3,
  chord:0.0635,
  stagger:25.14,
  thickness:0.0631,
  camber:0.0313,
  profile: Array.from({length:100},(_,j)=>{
    const x=j/100;
    return {x, y: Math.sin(x*Math.PI)*0.0599 + Math.sin(x*Math.PI*3)*0.005};
  }),
  efficiency:0.9465,
};
export function renderBlade(ctx, x, y, scale=1){
  ctx.save(); ctx.translate(x,y); ctx.scale(scale,scale);
  ctx.strokeStyle=`hsl(204,100%,60%)`; ctx.lineWidth=2;
  ctx.beginPath(); BLADE_03.profile.forEach((p,idx)=>{ if(idx==0) ctx.moveTo(p.x*100,p.y*100); else ctx.lineTo(p.x*100,p.y*100); }); ctx.stroke();
  ctx.restore();
}
