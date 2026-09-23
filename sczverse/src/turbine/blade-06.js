
// Turbine blade profile 6
export const BLADE_06 = {
  id:6,
  chord:0.1432,
  stagger:27.54,
  thickness:0.0309,
  camber:0.0174,
  profile: Array.from({length:100},(_,j)=>{
    const x=j/100;
    return {x, y: Math.sin(x*Math.PI)*0.0354 + Math.sin(x*Math.PI*3)*0.005};
  }),
  efficiency:0.8164,
};
export function renderBlade(ctx, x, y, scale=1){
  ctx.save(); ctx.translate(x,y); ctx.scale(scale,scale);
  ctx.strokeStyle=`hsl(228,100%,60%)`; ctx.lineWidth=2;
  ctx.beginPath(); BLADE_06.profile.forEach((p,idx)=>{ if(idx==0) ctx.moveTo(p.x*100,p.y*100); else ctx.lineTo(p.x*100,p.y*100); }); ctx.stroke();
  ctx.restore();
}
