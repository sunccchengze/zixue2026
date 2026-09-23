
// Turbine blade profile 14
export const BLADE_14 = {
  id:14,
  chord:0.0570,
  stagger:34.33,
  thickness:0.0523,
  camber:0.0465,
  profile: Array.from({length:100},(_,j)=>{
    const x=j/100;
    return {x, y: Math.sin(x*Math.PI)*0.0570 + Math.sin(x*Math.PI*3)*0.005};
  }),
  efficiency:0.8735,
};
export function renderBlade(ctx, x, y, scale=1){
  ctx.save(); ctx.translate(x,y); ctx.scale(scale,scale);
  ctx.strokeStyle=`hsl(292,100%,60%)`; ctx.lineWidth=2;
  ctx.beginPath(); BLADE_14.profile.forEach((p,idx)=>{ if(idx==0) ctx.moveTo(p.x*100,p.y*100); else ctx.lineTo(p.x*100,p.y*100); }); ctx.stroke();
  ctx.restore();
}
