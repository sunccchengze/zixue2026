
import { DISCIPLINES } from '../../data/disciplines.js';
export function render(info){
  const d = info || DISCIPLINES.find(x=>x.id==='chemistry');
  const div=document.createElement('div');
  div.innerHTML=`
    <h2>${d?.emoji||'🌌'} ${d?.name||'chemistry'} 星系</h2>
    <p>${d?.desc||'探索未知'}</p>
    <div class="galaxy-detail">
      <div class="galaxy-visual"><canvas id="canvas-chemistry" style="width:100%;height:400px"></canvas></div>
      <div>
        <div class="discipline-card"><b>进度</b><div class="progress-ring" style="--p:${d?.progress||30}%"><span>${d?.progress||30}%</span></div></div>
        <div class="discipline-card"><b>今日任务</b><br><small id="tasks-chemistry">加载中...</small></div>
        <div class="game-controls">
          <button onclick="import('../../games/chemistry-toy/index.js').then(m=>document.getElementById('modal-content').appendChild(m.render()))">🎮 游乐场</button>
          <button onclick="import('./visual.js').then(m=>m.animate(document.getElementById('canvas-chemistry')))">✨ 可视化</button>
        </div>
      </div>
    </div>
    <div style="margin-top:20px;display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:12px" id="cards-chemistry"></div>
  `;
  setTimeout(()=>{
    import('./visual.js').then(m=>m.animate(div.querySelector('canvas')));
    const cards=div.querySelector('#cards-chemistry');
    for(let i=0;i<6;i++){
      const c=document.createElement('div'); c.className='discipline-card';
      c.innerHTML=`<b>${d?.emoji} 卡片 ${i+1}</b><br><small>${d?.name}的第${i+1}个秘密</small><br><canvas style="width:100%;height:60px" class="mini-canvas"></canvas>`;
      cards.appendChild(c);
    }
  },100);
  return div;
}
