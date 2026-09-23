
// Turbine blade profile 10
export const BLADE_10 = {
  id:10,
  chord:0.1125,
  stagger:25.20,
  thickness:0.0571,
  camber:0.0222,
  profile: Array.from({length:100},(_,j)=>{
    const x=j/100;
    return {x, y: Math.sin(x*Math.PI)*0.0221 + Math.sin(x*Math.PI*3)*0.005};
  }),
  efficiency:0.8014,
};
export function renderBlade(ctx, x, y, scale=1){
  ctx.save(); ctx.translate(x,y); ctx.scale(scale,scale);
  ctx.strokeStyle=`hsl(260,100%,60%)`; ctx.lineWidth=2;
  ctx.beginPath(); BLADE_10.profile.forEach((p,idx)=>{ if(idx==0) ctx.moveTo(p.x*100,p.y*100); else ctx.lineTo(p.x*100,p.y*100); }); ctx.stroke();
  ctx.restore();
}
