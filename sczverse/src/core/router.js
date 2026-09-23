
export class Router{
  constructor(universe){ this.universe=universe; }
  async go(id){
    const modal = document.getElementById('modal');
    const content = document.getElementById('modal-content');
    modal.classList.remove('hidden');
    try{
      const mod = await import(`../galaxies/${id}/index.js`);
      content.innerHTML = '';
      const el = mod.render();
      content.appendChild(el);
    }catch(e){
      console.error(e);
      content.innerHTML = `<h2>🌌 ${id} 星系</h2><p>正在穿越虫洞...</p><pre>${e.message}</pre>`;
      // fallback: try games
      try{
        const mod2 = await import(`../games/${id}/index.js`);
        content.innerHTML=''; content.appendChild(mod2.render());
      }catch{}
    }
  }
}
