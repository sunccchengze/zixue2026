import { NIENIE_SKINS } from '../data/nienie-data.js';
export class NienieCompanion{
  constructor(container){ this.container=container; this.skin=0; this.mood='😊'; this.squish=0; this.x=0; this.y=0; this.vx=0; this.vy=0; }
  init(){
    this.render();
    setTimeout(()=>this.container.classList.remove('hidden'),2000);
    this.physicsLoop();
  }
  render(){
    const skin=NIENIE_SKINS[this.skin];
    this.container.innerHTML=`
      <div class="nienie-eagle" id="nienie-eagle">
        <div class="nienie-mood" id="nienie-mood">${skin.mood}</div>
        <canvas id="nienie-canvas" width="160" height="180" style="width:160px;height:180px;cursor:grab"></canvas>
        <div style="text-align:center;font-size:10px;opacity:0.6">${skin.name}<br><small>${skin.desc}</small><br><small>拖拽移动·点击换肤·按住捏</small></div>
      </div>
    `;
    const canvas=document.getElementById('nienie-canvas');
    const ctx=canvas.getContext('2d');
    const drawEagle=(squishX=1, squishY=1, eyeOffset=0)=>{
      const w=canvas.width,h=canvas.height;
      ctx.clearRect(0,0,w,h);
      ctx.save(); ctx.translate(w/2,h/2+10); ctx.scale(squishX,squishY);
      // shadow
      ctx.fillStyle='rgba(0,0,0,0.2)'; ctx.beginPath(); ctx.ellipse(0,60,40,12,0,0,Math.PI*2); ctx.fill();
      // body - soft
      const grad=ctx.createRadialGradient(-10,-20,0,0,0,50);
      grad.addColorStop(0,'#fff8dc'); grad.addColorStop(0.3,skin.color); grad.addColorStop(1,'#8a6a30');
      ctx.fillStyle=grad;
      ctx.beginPath();
      ctx.ellipse(0,0,45,55,0,0,Math.PI*2);
      ctx.fill();
      // belly
      ctx.fillStyle='rgba(255,255,255,0.6)'; ctx.beginPath(); ctx.ellipse(0,15,25,30,0,0,Math.PI*2); ctx.fill();
      // eyes
      ctx.fillStyle='white'; 
      ctx.beginPath(); ctx.ellipse(-16+eyeOffset,-18,10,13,0,0,Math.PI*2); ctx.fill();
      ctx.beginPath(); ctx.ellipse(16+eyeOffset,-18,10,13,0,0,Math.PI*2); ctx.fill();
      ctx.fillStyle='#111'; ctx.beginPath(); ctx.arc(-16+eyeOffset,-16,5,0,Math.PI*2); ctx.fill();
      ctx.beginPath(); ctx.arc(16+eyeOffset,-16,5,0,Math.PI*2); ctx.fill();
      ctx.fillStyle='white'; ctx.beginPath(); ctx.arc(-14+eyeOffset,-18,2,0,Math.PI*2); ctx.fill();
      ctx.beginPath(); ctx.arc(18+eyeOffset,-18,2,0,Math.PI*2); ctx.fill();
      // beak
      ctx.fillStyle='#ff9a3d'; ctx.beginPath(); ctx.moveTo(-6,-4); ctx.lineTo(6,-4); ctx.lineTo(0,6); ctx.closePath(); ctx.fill();
      ctx.strokeStyle='#cc6a20'; ctx.lineWidth=1; ctx.stroke();
      // wings
      ctx.fillStyle='#c49a4a';
      ctx.save(); ctx.translate(-38,5); ctx.rotate(-0.3+Math.sin(Date.now()*0.005)*0.1);
      ctx.beginPath(); ctx.ellipse(0,0,18,35,0,0,Math.PI*2); ctx.fill(); ctx.restore();
      ctx.save(); ctx.translate(38,5); ctx.rotate(0.3-Math.sin(Date.now()*0.005)*0.1);
      ctx.beginPath(); ctx.ellipse(0,0,18,35,0,0,Math.PI*2); ctx.fill(); ctx.restore();
      // feet
      ctx.fillStyle='#ff8c42'; ctx.fillRect(-14,48,6,8); ctx.fillRect(8,48,6,8);
      ctx.restore();
    };
    drawEagle();
    let isDown=false, startY=0, squish=1;
    canvas.addEventListener('pointerdown',e=>{
      isDown=true; startY=e.clientY; canvas.setPointerCapture(e.pointerId);
      canvas.style.cursor='grabbing';
      this.happy();
      const move=(ev)=>{
        if(!isDown) return;
        const dy=ev.clientY-startY;
        const sy=Math.max(0.6,Math.min(1.4,1-dy*0.01));
        const sx=2-sy;
        drawEagle(sx,sy, dy*0.05);
      };
      const up=()=>{
        isDown=false; canvas.style.cursor='grab'; drawEagle();
        canvas.removeEventListener('pointermove',move);
        canvas.removeEventListener('pointerup',up);
      };
      canvas.addEventListener('pointermove',move);
      canvas.addEventListener('pointerup',up);
    });
    canvas.addEventListener('click',()=>{ this.nextSkin(); });
    // drag container
    let dragging=false, offsetX=0, offsetY=0;
    const eagleDiv=document.getElementById('nienie-eagle');
    eagleDiv.addEventListener('pointerdown',e=>{
      if(e.target===canvas) return;
      dragging=true; offsetX=e.clientX-this.container.offsetLeft; offsetY=e.clientY-this.container.offsetTop;
      eagleDiv.setPointerCapture(e.pointerId);
    });
    window.addEventListener('pointermove',e=>{
      if(!dragging) return;
      this.container.style.left=(e.clientX-offsetX)+'px'; this.container.style.top=(e.clientY-offsetY)+'px'; this.container.style.right='auto'; this.container.style.bottom='auto';
    });
    window.addEventListener('pointerup',()=>dragging=false);
    // eye follow mouse
    window.addEventListener('pointermove',e=>{
      if(isDown) return;
      const rect=canvas.getBoundingClientRect();
      const mx=(e.clientX-rect.left-rect.width/2)/20;
      const my=(e.clientY-rect.top-rect.height/2)/20;
      drawEagle(1,1, Math.max(-3,Math.min(3,mx)));
    });
  }
  nextSkin(){ this.skin=(this.skin+1)%NIENIE_SKINS.length; this.render(); document.getElementById('hud-mood').textContent=NIENIE_SKINS[this.skin].mood; }
  toggle(){ this.container.classList.toggle('hidden'); }
  happy(){
    const moodEl=document.getElementById('nienie-mood');
    if(moodEl){ moodEl.textContent='🥰'; moodEl.animate([{transform:'scale(1)'},{transform:'scale(1.5)'},{transform:'scale(1)'}],{duration:300}); setTimeout(()=>moodEl.textContent=NIENIE_SKINS[this.skin].mood,1000); }
    this.container.animate([{transform:'scale(1)'},{transform:'scale(1.2)'},{transform:'scale(1)'}],{duration:300});
    document.getElementById('hud-mood').textContent='🥰';
    setTimeout(()=>document.getElementById('hud-mood').textContent=NIENIE_SKINS[this.skin].mood,1000);
  }
  physicsLoop(){
    // soft body spring
    setInterval(()=>{
      if(Math.random()<0.02){ // blink
        const canvas=document.getElementById('nienie-canvas');
        if(!canvas) return;
        const ctx=canvas.getContext('2d');
        // blink handled in draw
      }
    },100);
  }
}
