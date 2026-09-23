
export const CONSTELLATIONS = [
  {name:'涡轮座', stars:[[0,0],[20,10],[40,5],[60,15]], color:'#00f5ff'},
  {name:'小鹰座', stars:[[0,0],[10,20],[20,15],[30,25],[15,30]], color:'#e6c875'},
  {name:'概率座', stars:[[0,0],[30,10],[15,30],[45,35]], color:'#ffcc00'},
];
export function drawConstellations(ctx,w,h){
  CONSTELLATIONS.forEach(con=>{
    ctx.strokeStyle=con.color; ctx.globalAlpha=0.3; ctx.lineWidth=1;
    ctx.beginPath();
    con.stars.forEach((s,i)=>{ const x=w*0.2+s[0]*3, y=h*0.3+s[1]*3; if(i==0) ctx.moveTo(x,y); else ctx.lineTo(x,y); });
    ctx.stroke();
    con.stars.forEach(s=>{ ctx.fillStyle=con.color; ctx.beginPath(); ctx.arc(w*0.2+s[0]*3,h*0.3+s[1]*3,2,0,Math.PI*2); ctx.fill(); });
  });
}
