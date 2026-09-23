
export function createWidget_3(container){
  const el=document.createElement('div');
  el.className='discipline-card';
  el.innerHTML=`<b>组件 3</b><br><small>为承泽定制的小组件，灵感来自${['涡轮','小鹰','概率','禅意','力学'][3%5]}</small><br><canvas style="width:100%;height:40px"></canvas>`;
  container?.appendChild(el);
  const c=el.querySelector('canvas');
  if(c){
    const ctx=c.getContext('2d'); c.width=200; c.height=40;
    ctx.strokeStyle=`hsl(72,100%,60%)`;
    ctx.beginPath(); for(let x=0;x<200;x++){ const y=20+Math.sin(x*0.05+3)*10; if(x==0) ctx.moveTo(x,y); else ctx.lineTo(x,y); } ctx.stroke();
  }
  return el;
}
