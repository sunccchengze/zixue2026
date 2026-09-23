
export const ZEN_13 = {
  id:13,
  koan:["本来无一物","知行合一","无为而无不为","见素抱朴","上善若水"][13%5],
  stones:3,
  ripples:2,
  render(canvas){
    const ctx=canvas.getContext('2d');
    ctx.fillStyle='#0a0a0a'; ctx.fillRect(0,0,canvas.width,canvas.height);
    for(let s=0;s<this.stones;s++){
      const x=Math.random()*canvas.width, y=Math.random()*canvas.height, r=10+Math.random()*30;
      const grad=ctx.createRadialGradient(x-r*0.3,y-r*0.3,0,x,y,r);
      grad.addColorStop(0,'#555'); grad.addColorStop(1,'#222');
      ctx.fillStyle=grad; ctx.beginPath(); ctx.arc(x,y,r,0,Math.PI*2); ctx.fill();
    }
  }
};
