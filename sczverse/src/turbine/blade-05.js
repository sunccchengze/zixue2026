
// Turbine blade profile 5
export const BLADE_05 = {
  id:5,
  chord:0.0802,
  stagger:35.89,
  thickness:0.0230,
  camber:0.0160,
  profile: Array.from({length:100},(_,j)=>{
    const x=j/100;
    return {x, y: Math.sin(x*Math.PI)*0.0627 + Math.sin(x*Math.PI*3)*0.005};
  }),
  efficiency:0.8275,
};
export function renderBlade(ctx, x, y, scale=1){
  ctx.save(); ctx.translate(x,y); ctx.scale(scale,scale);
  ctx.strokeStyle=`hsl(220,100%,60%)`; ctx.lineWidth=2;
  ctx.beginPath(); BLADE_05.profile.forEach((p,idx)=>{ if(idx==0) ctx.moveTo(p.x*100,p.y*100); else ctx.lineTo(p.x*100,p.y*100); }); ctx.stroke();
  ctx.restore();
}
