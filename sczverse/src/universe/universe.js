import { DISCIPLINES } from '../data/disciplines.js';
import { State } from '../core/state.js';

export class Universe{
  async init(){
    this.state = new State();
    this.ring = document.getElementById('galaxy-ring');
    this.createGalaxies();
    this.bindEvents();
    this.t=0;
  }
  createGalaxies(){
    this.ring.innerHTML='';
    const count = DISCIPLINES.length;
    const radius = Math.min(window.innerWidth, window.innerHeight)*0.38;
    DISCIPLINES.forEach((d,i)=>{
      const angle = (i/count)*Math.PI*2 - Math.PI/2;
      const x = Math.cos(angle)*radius;
      const y = Math.sin(angle)*radius;
      const node = document.createElement('div');
      node.className='galaxy-node';
      node.style.left=`calc(50% + ${x}px)`;
      node.style.top=`calc(50% + ${y}px)`;
      node.style.color=d.color;
      node.dataset.id=d.id;
      node.innerHTML=`
        <div class="node-core" style="background:radial-gradient(circle at 30% 30%, white, ${d.color} 30%, ${d.dark} 70%)">${d.emoji}</div>
        <div class="node-label"><b>${d.name}</b><small>${d.en}</small><div class="node-progress"><i style="width:${d.progress}%"></i></div><small style="opacity:0.6">${d.progress}%</small></div>
      `;
      node.onclick=()=>this.enterGalaxy(d);
      node.onmouseenter=(e)=>this.showTooltip(e,d);
      node.onmouseleave=()=>this.hideTooltip();
      this.ring.appendChild(node);
    });
  }
  showTooltip(e,d){
    const tip=document.getElementById('tooltip');
    tip.innerHTML=`<b>${d.emoji} ${d.name}</b><br>${d.desc}<br><small>进度 ${d.progress}% · ${d.tasks}任务<br>${d.realProgress.next}</small><br><small style="opacity:0.6">点击进入真实实验室</small>`;
    tip.style.left=e.clientX+16+'px'; tip.style.top=e.clientY+16+'px';
    tip.classList.add('show');
  }
  hideTooltip(){ document.getElementById('tooltip').classList.remove('show'); }
  async enterGalaxy(d){
    this.state.explore(d.id);
    document.getElementById('hud-explored').textContent=this.state.explored.size;
    const modal=document.getElementById('modal');
    const content=document.getElementById('modal-content');
    modal.classList.remove('hidden');
    content.innerHTML=`<h2>${d.emoji} ${d.name} 星系</h2><p>${d.desc}</p><div class="loading-ring" style="width:40px;height:40px"></div>`;
    try{
      const mod = await import(`../galaxies/${d.id}/index.js`);
      content.innerHTML=''; content.appendChild(mod.render(d));
    }catch(err){
      console.error(err);
      const { renderGeneric } = await import('../components/galaxy-detail.js');
      content.innerHTML=''; content.appendChild(renderGeneric(d));
    }
  }
  animate(){
    let t=0;
    const anim=()=>{
      t+=0.002;
      this.ring.style.transform=`translate(-50%,-50%) rotate(${t*2}deg)`;
      document.querySelectorAll('.galaxy-node').forEach(n=>{ n.style.transform=`translate(-50%,-50%) rotate(${-t*2}deg)`; });
      requestAnimationFrame(anim);
    }; anim();
  }
  focusMap(){ this.ring.scrollIntoView({behavior:'smooth'}); }
  explodeCenter(){
    const center=document.getElementById('center-star');
    center.animate([{transform:'translate(-50%,-50%) scale(1)'},{transform:'translate(-50%,-50%) scale(1.5)'},{transform:'translate(-50%,-50%) scale(1)'}],{duration:600,easing:'cubic-bezier(0.34,1.56,0.64,1)'});
    // particle explosion
    for(let i=0;i<30;i++){
      const p=document.createElement('div');
      p.style.position='fixed'; p.style.left='50%'; p.style.top='50%';
      p.style.width='6px'; p.style.height='6px'; p.style.background=`hsl(${Math.random()*60+250},100%,60%)`;
      p.style.borderRadius='50%'; p.style.pointerEvents='none'; p.style.zIndex='100';
      document.body.appendChild(p);
      const angle=Math.random()*Math.PI*2, dist=100+Math.random()*200;
      p.animate([{transform:'translate(-50%,-50%)', opacity:1},{transform:`translate(calc(-50% + ${Math.cos(angle)*dist}px), calc(-50% + ${Math.sin(angle)*dist}px))`, opacity:0}],{duration:800+Math.random()*400, easing:'cubic-bezier(0.25,1,0.5,1)'}).onfinish=()=>p.remove();
    }
  }
  superMode(){
    document.body.animate([{filter:'hue-rotate(0deg)'},{filter:'hue-rotate(360deg)'}],{duration:2000,iterations:3});
  }
  bindEvents(){
    window.addEventListener('resize',()=>this.createGalaxies());
  }
}
