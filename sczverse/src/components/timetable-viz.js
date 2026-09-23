
export function renderTimetable(){
  const div=document.createElement('div');
  div.innerHTML=`
    <h2>📅 承泽的时空课表 · 2026秋</h2>
    <p><small>兴庆校区 · 夏令时 · 第1周起点 2026-09-14</small></p>
    <div style="display:grid;grid-template-columns:60px repeat(5,1fr);gap:4px;font-size:11px;margin-top:12px" id="tt-grid"></div>
    <canvas id="tt-canvas" style="width:100%;height:200px;margin-top:16px;background:rgba(255,255,255,0.03);border-radius:12px"></canvas>
  `;
  const courses=[
    {day:1,slot:'1-2',name:'数理方程',color:'#00f5ff'},
    {day:1,slot:'3-4',name:'大化实验',color:'#ff5c8a'},
    {day:1,slot:'5-6',name:'复变',color:'#7c5cff'},
    {day:2,slot:'1-2',name:'大物',color:'#00ff88'},
    {day:2,slot:'3-4',name:'力学',color:'#ff8a00'},
    {day:2,slot:'5-6',name:'体育',color:'#88ff00'},
    {day:2,slot:'7-8',name:'概率',color:'#ffcc00'},
    {day:3,slot:'1-2',name:'大化',color:'#ff5c8a'},
    {day:3,slot:'3-4',name:'复变/数理',color:'#7c5cff'},
    {day:3,slot:'9-10',name:'AI',color:'#00ffcc'},
    {day:4,slot:'1-2',name:'英语',color:'#ffaa00'},
    {day:4,slot:'3-4',name:'概率',color:'#ffcc00'},
    {day:4,slot:'5-6',name:'大物',color:'#00ff88'},
    {day:4,slot:'7-8',name:'毛概',color:'#ff5555'},
    {day:5,slot:'1-2',name:'力学',color:'#ff8a00'},
    {day:5,slot:'3-4',name:'大化',color:'#ff5c8a'},
    {day:5,slot:'5-8',name:'测控实习',color:'#00aaff'},
    {day:5,slot:'9-10',name:'AI',color:'#00ffcc'},
  ];
  setTimeout(()=>{
    const grid=div.querySelector('#tt-grid');
    grid.innerHTML='<div></div><div>周一</div><div>周二</div><div>周三</div><div>周四</div><div>周五</div>';
    const slots=['1-2','3-4','5-6','7-8','9-10'];
    slots.forEach(slot=>{
      grid.innerHTML+=`<div style="opacity:0.5">${slot}</div>`;
      for(let d=1;d<=5;d++){
        const c=courses.find(x=>x.day===d&&x.slot===slot);
        grid.innerHTML+= c? `<div style="background:${c.color}22;border:1px solid ${c.color}66;border-radius:8px;padding:4px;text-align:center">${c.name}</div>` : `<div style="background:rgba(255,255,255,0.02);border-radius:8px"></div>`;
      }
    });
    const canvas=div.querySelector('#tt-canvas');
    const ctx=canvas.getContext('2d');
    canvas.width=600; canvas.height=200;
    let t=0;
    function loop(){
      t+=0.02;
      ctx.clearRect(0,0,canvas.width,canvas.height);
      ctx.fillStyle='rgba(124,92,255,0.1)';
      courses.forEach((c,i)=>{
        const x=(c.day-1)*100+20+Math.sin(t+i*0.3)*5;
        const y=slots.indexOf(c.slot)*35+20;
        ctx.fillStyle=c.color;
        ctx.globalAlpha=0.6+Math.sin(t+i)*0.4;
        ctx.beginPath(); ctx.arc(x,y,6,0,Math.PI*2); ctx.fill();
      });
      requestAnimationFrame(loop);
    }loop();
  },100);
  return div;
}
