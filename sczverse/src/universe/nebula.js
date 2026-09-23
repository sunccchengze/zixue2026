
export function createNebula(container){
  const colors=['#7c5cff','#00f5ff','#ff5c8a','#ffcc00'];
  for(let i=0;i<6;i++){
    const el=document.createElement('div'); el.className='nebula';
    el.style.width=(200+Math.random()*400)+'px'; el.style.height=(200+Math.random()*400)+'px';
    el.style.left=Math.random()*100+'%'; el.style.top=Math.random()*100+'%';
    el.style.background=`radial-gradient(circle,${colors[i%colors.length]}40,transparent)`;
    container.appendChild(el);
  }
}
