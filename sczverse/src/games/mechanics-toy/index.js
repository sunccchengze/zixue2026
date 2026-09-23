
export function render(){
  const div=document.createElement('div');
  div.className='game-card';
  div.innerHTML=`
    <h3>🏗️ 力系平衡</h3>
    <p><small>拖拽力箭头，寻找平衡</small></p>
    <canvas id="c-mechanics-toy" class="game-canvas"></canvas>
    <div class="game-controls">
      <button onclick="import('./physics.js').then(m=>m.start(document.getElementById('c-mechanics-toy')))">▶️ 开始</button>
      <button onclick="import('./render.js').then(m=>m.effect(document.getElementById('c-mechanics-toy')))">✨ 特效</button>
      <button onclick="document.getElementById('c-mechanics-toy').getContext('2d').clearRect(0,0,9999,9999)">🧹 清空</button>
    </div>
    <div style="margin-top:12px;font-size:11px;opacity:0.6">为孙承泽定制 · mechanics-toy · 点击画布交互</div>
  `;
  setTimeout(()=>{ import('./physics.js').then(m=>m.start(div.querySelector('canvas'))); },100);
  return div;
}
