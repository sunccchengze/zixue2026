
export function effect(canvas){
  if(!canvas) return;
  const ctx=canvas.getContext('2d');
  for(let i=0;i<30;i++){
    setTimeout(()=>{
      ctx.fillStyle=`hsl(${Math.random()*360},100%,60%)`;
      ctx.beginPath(); ctx.arc(Math.random()*canvas.width,Math.random()*canvas.height,Math.random()*20+5,0,Math.PI*2); ctx.fill();
    },i*50);
  }
}
export function clear(canvas){ canvas.getContext('2d').clearRect(0,0,canvas.width,canvas.height); }
