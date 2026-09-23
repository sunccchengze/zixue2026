
export class FluidSim{
  constructor(canvas){ this.canvas=canvas; this.ctx=canvas.getContext('2d'); this.t=0; }
  init(){ this.resize(); window.addEventListener('resize',()=>this.resize()); }
  resize(){ this.canvas.width=innerWidth; this.canvas.height=innerHeight; }
  animate(){
    const ctx=this.ctx; const w=this.canvas.width, h=this.canvas.height;
    this.t+=0.005;
    ctx.clearRect(0,0,w,h);
    // subtle aurora waves
    ctx.globalAlpha=0.15;
    for(let i=0;i<3;i++){
      ctx.beginPath();
      ctx.strokeStyle=`hsl(${240+i*30},100%,60%)`;
      ctx.lineWidth=80;
      for(let x=0;x<w;x+=10){
        const y = h*0.5 + Math.sin(x*0.005 + this.t + i)*100 + Math.cos(x*0.002 + this.t*0.5)*50;
        if(x===0) ctx.moveTo(x,y); else ctx.lineTo(x,y);
      }
      ctx.stroke();
    }
    requestAnimationFrame(()=>this.animate());
  }
}
