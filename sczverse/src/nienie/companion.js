
import { NIENIE_SKINS } from '../data/nienie-data.js';
export class NienieCompanion{
  constructor(container){ this.container=container; this.skin=0; this.mood='😊'; this.squish=0; }
  init(){
    this.render();
    // auto show after 2s
    setTimeout(()=>this.container.classList.remove('hidden'),2000);
  }
  render(){
    const skin=NIENIE_SKINS[this.skin];
    this.container.innerHTML=`
      <div class="nienie-eagle" id="nienie-eagle">
        <div class="nienie-mood">${skin.mood}</div>
        <div class="nienie-body" style="background:radial-gradient(ellipse at 30% 20%, #fff8dc, ${skin.color} 30%, #8a6a30 70%)">
          <div class="nienie-eye left"></div>
          <div class="nienie-eye right"></div>
          <div class="nienie-beak"></div>
          <div class="nienie-wing left"></div>
          <div class="nienie-wing right"></div>
        </div>
        <div style="text-align:center;font-size:10px;opacity:0.6">${skin.name}<br><small>${skin.desc}</small></div>
      </div>
    `;
    const eagle=document.getElementById('nienie-eagle');
    let isDown=false, startY=0;
    eagle.addEventListener('pointerdown',e=>{ isDown=true; startY=e.clientY; eagle.setPointerCapture(e.pointerId); this.squish=1; eagle.querySelector('.nienie-body').classList.add('squished'); this.happy(); });
    eagle.addEventListener('pointerup',e=>{ isDown=false; eagle.querySelector('.nienie-body').classList.remove('squished'); this.squish=0; });
    eagle.addEventListener('pointermove',e=>{
      if(!isDown) return;
      const dy=e.clientY-startY;
      const body=eagle.querySelector('.nienie-body');
      body.style.transform=`scaleY(${1-dy*0.005}) scaleX(${1+dy*0.005})`;
    });
    eagle.addEventListener('click',()=>{ this.nextSkin(); });
    // drag to move container
    let dragging=false, offsetX=0, offsetY=0;
    eagle.addEventListener('pointerdown',e=>{
      if(e.target.closest('.nienie-body')) return;
      dragging=true; offsetX=e.clientX-this.container.offsetLeft; offsetY=e.clientY-this.container.offsetTop;
    });
    window.addEventListener('pointermove',e=>{
      if(!dragging) return;
      this.container.style.left=(e.clientX-offsetX)+'px'; this.container.style.top=(e.clientY-offsetY)+'px'; this.container.style.right='auto'; this.container.style.bottom='auto';
    });
    window.addEventListener('pointerup',()=>dragging=false);
  }
  nextSkin(){ this.skin=(this.skin+1)%NIENIE_SKINS.length; this.render(); document.getElementById('hud-mood').textContent=NIENIE_SKINS[this.skin].mood; }
  toggle(){ this.container.classList.toggle('hidden'); }
  happy(){
    this.container.animate([{transform:'scale(1)'},{transform:'scale(1.2)'},{transform:'scale(1)'}],{duration:300});
    document.getElementById('hud-mood').textContent='🥰';
    setTimeout(()=>document.getElementById('hud-mood').textContent=NIENIE_SKINS[this.skin].mood,1000);
  }
}
