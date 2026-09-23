
// Turbine blade profile 8
export const BLADE_08 = {
  id:8,
  chord:0.1242,
  stagger:35.51,
  thickness:0.0394,
  camber:0.0390,
  profile: Array.from({length:100},(_,j)=>{
    const x=j/100;
    return {x, y: Math.sin(x*Math.PI)*0.0688 + Math.sin(x*Math.PI*3)*0.005};
  }),
  efficiency:0.8910,
};
export function renderBlade(ctx, x, y, scale=1){
  ctx.save(); ctx.translate(x,y); ctx.scale(scale,scale);
  ctx.strokeStyle=`hsl(244,100%,60%)`; ctx.lineWidth=2;
  ctx.beginPath(); BLADE_08.profile.forEach((p,idx)=>{ if(idx==0) ctx.moveTo(p.x*100,p.y*100); else ctx.lineTo(p.x*100,p.y*100); }); ctx.stroke();
  ctx.restore();
}
