
// Turbine blade profile 9
export const BLADE_09 = {
  id:9,
  chord:0.1200,
  stagger:45.90,
  thickness:0.0247,
  camber:0.0316,
  profile: Array.from({length:100},(_,j)=>{
    const x=j/100;
    return {x, y: Math.sin(x*Math.PI)*0.0505 + Math.sin(x*Math.PI*3)*0.005};
  }),
  efficiency:0.8565,
};
export function renderBlade(ctx, x, y, scale=1){
  ctx.save(); ctx.translate(x,y); ctx.scale(scale,scale);
  ctx.strokeStyle=`hsl(252,100%,60%)`; ctx.lineWidth=2;
  ctx.beginPath(); BLADE_09.profile.forEach((p,idx)=>{ if(idx==0) ctx.moveTo(p.x*100,p.y*100); else ctx.lineTo(p.x*100,p.y*100); }); ctx.stroke();
  ctx.restore();
}
