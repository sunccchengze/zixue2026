
import { DISCIPLINES } from '../data/disciplines.js';
import { State } from '../core/state.js';

export class Universe{
  async init(){
    this.state = new State();
    this.ring = document.getElementById('galaxy-ring');
    this.createGalaxies();
    this.bindEvents();
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
      node.innerHTML=`
        <div class="node-core" style="background:radial-gradient(circle at 30% 30%, white, ${d.color} 30%, ${d.dark} 70%)">${d.emoji}</div>
        <div class="node-label"><b>${d.name}</b><small>${d.en}</small><div class="node-progress"><i style="width:${d.progress}%"></i></div></div>
      `;
      node.onclick=()=>this.enterGalaxy(d);
      node.onmouseenter=(e)=>this.showTooltip(e,d);
      node.onmouseleave=()=>this.hideTooltip();
      this.ring.appendChild(node);
    });
  }
  showTooltip(e,d){
    const tip=document.getElementById('tooltip');
    tip.innerHTML=`<b>${d.emoji} ${d.name}</b><br>${d.desc}<br><small>进度 ${d.progress}% · ${d.tasks} 任务</small>`;
    tip.style.left=e.clientX+16+'px'; tip.style.top=e.clientY+16+'px';
    tip.classList.add('show');
  }
  hideTooltip(){ document.getElementById('tooltip').classList.remove('show'); }
  async enterGalaxy(d){
    this.state.explore(d.id);
    const modal=document.getElementById('modal');
    const content=document.getElementById('modal-content');
    modal.classList.remove('hidden');
    content.innerHTML=`<h2>${d.emoji} ${d.name} 星系</h2><p>${d.desc}</p><div class="loading-ring" style="width:40px;height:40px"></div>`;
    try{
      const mod = await import(`../galaxies/${d.id}/index.js`);
      content.innerHTML=''; content.appendChild(mod.render(d));
    }catch(err){
      console.error(err);
      // fallback generic
      const { renderGeneric } = await import('../components/galaxy-detail.js');
      content.innerHTML=''; content.appendChild(renderGeneric(d));
    }
  }
  animate(){
    let t=0;
    const anim=()=>{
      t+=0.002;
      this.ring.style.transform=`translate(-50%,-50%) rotate(${t*2}deg)`;
      // counter rotate nodes
      document.querySelectorAll('.galaxy-node').forEach(n=>{ n.style.transform=`translate(-50%,-50%) rotate(${-t*2}deg)`; });
      requestAnimationFrame(anim);
    }; anim();
  }
  focusMap(){ this.ring.scrollIntoView({behavior:'smooth'}); }
  explodeCenter(){
    const center=document.getElementById('center-star');
    center.animate([{transform:'translate(-50%,-50%) scale(1)'},{transform:'translate(-50%,-50%) scale(1.5)'},{transform:'translate(-50%,-50%) scale(1)'}],{duration:600,easing:'cubic-bezier(0.34,1.56,0.64,1)'});
  }
  superMode(){
    document.body.animate([{filter:'hue-rotate(0deg)'},{filter:'hue-rotate(360deg)'}],{duration:2000,iterations:3});
  }
  bindEvents(){
    window.addEventListener('resize',()=>this.createGalaxies());
  }
}
