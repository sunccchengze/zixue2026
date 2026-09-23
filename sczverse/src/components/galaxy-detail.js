
export function renderGeneric(d){
  const div=document.createElement('div');
  div.innerHTML=`
    <h2>${d.emoji} ${d.name}</h2>
    <p>${d.desc}</p>
    <div class="galaxy-detail">
      <div class="galaxy-visual" id="visual-${d.id}"><canvas style="width:100%;height:100%"></canvas></div>
      <div>
        <div class="discipline-card"><b>进度</b> ${d.progress}%<div class="progress-ring" style="--p:${d.progress}%"><span>${d.progress}%</span></div></div>
        <div class="discipline-card"><b>任务</b> ${d.tasks} 个待完成</div>
        <div class="discipline-card"><b>关联</b> 与其他学科的纠缠</div>
        <button onclick="import('../games/${d.id}-toy/index.js').then(m=>{document.getElementById('modal-content').appendChild(m.render())})">🎮 进入游乐场</button>
      </div>
    </div>
  `;
  return div;
}
