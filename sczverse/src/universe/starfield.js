
export class Starfield{
  constructor(canvas){ this.canvas=canvas; this.ctx=canvas.getContext('2d'); this.stars=[]; }
  init(){
    this.resize(); this.createStars(400);
    window.addEventListener('resize',()=>{ this.resize(); this.createStars(400); });
  }
  resize(){ this.canvas.width=innerWidth; this.canvas.height=innerHeight; }
  createStars(n){
    this.stars=[];
    for(let i=0;i<n;i++){
      this.stars.push({x:Math.random()*this.canvas.width,y:Math.random()*this.canvas.height,r:Math.random()*1.5,tw:Math.random()*Math.PI*2,speed:Math.random()*0.02+0.005,alpha:Math.random()*0.5+0.5});
    }
  }
  animate(){
    const ctx=this.ctx; const w=this.canvas.width, h=this.canvas.height;
    ctx.clearRect(0,0,w,h);
    for(const s of this.stars){
      s.tw+=s.speed;
      const a=s.alpha*(0.6+0.4*Math.sin(s.tw));
      ctx.globalAlpha=a; ctx.fillStyle='white';
      ctx.beginPath(); ctx.arc(s.x,s.y,s.r,0,Math.PI*2); ctx.fill();
      // occasional shooting star
      if(Math.random()<0.0005){
        ctx.strokeStyle='rgba(255,255,255,'+a+')'; ctx.lineWidth=1;
        ctx.beginPath(); ctx.moveTo(s.x,s.y); ctx.lineTo(s.x-20,s.y-10); ctx.stroke();
      }
    }
    requestAnimationFrame(()=>this.animate());
  }
}
