
export class ParticleSystem{
  constructor(canvas){
    this.canvas=canvas; this.ctx=canvas.getContext('2d'); this.particles=[];
    this.resize(); window.addEventListener('resize',()=>this.resize());
  }
  resize(){ this.canvas.width=innerWidth; this.canvas.height=innerHeight; }
  add(x,y,color){ this.particles.push({x,y,vx:(Math.random()-0.5)*4,vy:(Math.random()-0.5)*4,life:1,color}); }
  update(){
    this.ctx.clearRect(0,0,this.canvas.width,this.canvas.height);
    this.particles=this.particles.filter(p=>p.life>0);
    for(const p of this.particles){
      p.x+=p.vx; p.y+=p.vy; p.life-=0.01; p.vy+=0.05;
      this.ctx.globalAlpha=p.life;
      this.ctx.fillStyle=p.color;
      this.ctx.beginPath(); this.ctx.arc(p.x,p.y,3,0,Math.PI*2); this.ctx.fill();
    }
    requestAnimationFrame(()=>this.update());
  }
}
