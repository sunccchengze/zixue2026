
// Turbine blade profile 1
export const BLADE_01 = {
  id:1,
  chord:0.1435,
  stagger:40.08,
  thickness:0.0366,
  camber:0.0288,
  profile: Array.from({length:100},(_,j)=>{
    const x=j/100;
    return {x, y: Math.sin(x*Math.PI)*0.0376 + Math.sin(x*Math.PI*3)*0.005};
  }),
  efficiency:0.8032,
};
export function renderBlade(ctx, x, y, scale=1){
  ctx.save(); ctx.translate(x,y); ctx.scale(scale,scale);
  ctx.strokeStyle=`hsl(188,100%,60%)`; ctx.lineWidth=2;
  ctx.beginPath(); BLADE_01.profile.forEach((p,idx)=>{ if(idx==0) ctx.moveTo(p.x*100,p.y*100); else ctx.lineTo(p.x*100,p.y*100); }); ctx.stroke();
  ctx.restore();
}
