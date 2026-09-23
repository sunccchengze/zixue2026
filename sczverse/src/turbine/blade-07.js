
// Turbine blade profile 7
export const BLADE_07 = {
  id:7,
  chord:0.0888,
  stagger:31.76,
  thickness:0.0471,
  camber:0.0457,
  profile: Array.from({length:100},(_,j)=>{
    const x=j/100;
    return {x, y: Math.sin(x*Math.PI)*0.0297 + Math.sin(x*Math.PI*3)*0.005};
  }),
  efficiency:0.9313,
};
export function renderBlade(ctx, x, y, scale=1){
  ctx.save(); ctx.translate(x,y); ctx.scale(scale,scale);
  ctx.strokeStyle=`hsl(236,100%,60%)`; ctx.lineWidth=2;
  ctx.beginPath(); BLADE_07.profile.forEach((p,idx)=>{ if(idx==0) ctx.moveTo(p.x*100,p.y*100); else ctx.lineTo(p.x*100,p.y*100); }); ctx.stroke();
  ctx.restore();
}
