
import { Universe } from '../universe/universe.js';
import { Starfield } from '../universe/starfield.js';
import { FluidSim } from '../universe/fluid.js';
import { AudioEngine } from './audio.js';
import { NienieCompanion } from '../nienie/companion.js';
import { TurbineEngine } from '../turbine/engine.js';
import { Router } from './router.js';
import { State } from './state.js';

const loadingBar = document.getElementById('loading-bar');
const loadingSub = document.getElementById('loading-sub');
const loading = document.getElementById('loading');

function setProgress(p, text){
  loadingBar.style.width = p+'%';
  if(text) loadingSub.textContent = text;
}

setProgress(10,'加载星图数据...');
const universe = new Universe();
const starfield = new Starfield(document.getElementById('star-canvas'));
const fluid = new FluidSim(document.getElementById('fluid-canvas'));
const audio = new AudioEngine();
const nienie = new NienieCompanion(document.getElementById('nienie-container'));
const turbine = new TurbineEngine();
const router = new Router(universe);
const state = new State();

setProgress(30,'点亮学科星系...');
await universe.init();
setProgress(60,'唤醒捏捏小鹰...');
nienie.init();
setProgress(80,'启动涡轮引擎...');
turbine.init();
setProgress(90,'注入东方智慧...');

starfield.init();
fluid.init();

setProgress(100,'折叠完成，欢迎回家，承泽！');
setTimeout(()=>{
  loading.style.opacity='0';
  setTimeout(()=>loading.remove(),800);
  universe.animate();
  starfield.animate();
  fluid.animate();
  audio.playAmbient();
},600);

// UI
document.getElementById('btn-map').onclick = ()=> universe.focusMap();
document.getElementById('btn-nienie').onclick = ()=> nienie.toggle();
document.getElementById('btn-turbine').onclick = ()=> turbine.showModal();
document.getElementById('btn-zen').onclick = ()=> router.go('zen');
document.getElementById('btn-sound').onclick = ()=> audio.toggle();

document.getElementById('center-star').onclick = ()=>{
  audio.playTone(440,0.5);
  universe.explodeCenter();
  nienie.happy();
};

document.getElementById('modal-close').onclick = ()=> document.getElementById('modal').classList.add('hidden');

// Konami
let konami = [];
const code = ['ArrowUp','ArrowUp','ArrowDown','ArrowDown','ArrowLeft','ArrowRight','ArrowLeft','ArrowRight','b','a'];
window.addEventListener('keydown',e=>{
  konami.push(e.key);
  konami = konami.slice(-10);
  if(konami.join(',')===code.join(',')){
    document.body.classList.add('super-burn');
    turbine.superBurn();
    audio.playSuper();
    universe.superMode();
    alert('🚀 涡轮超燃模式已激活！推力 114514 N！承泽，冲向深空！');
  }
});

// HUD
setInterval(()=>{
  document.getElementById('hud-explored').textContent = state.explored.size;
  document.getElementById('hud-thrust').textContent = turbine.thrust;
  document.getElementById('hud-zen').textContent = state.zen;
},500);

console.log('%cSCZVERSE · 承泽宇宙已启动','font-size:20px;color:#7c5cff;font-weight:bold');
console.log('%c为孙承泽定制 · 2253710052 · 能动强基2501','color:#00f5ff');
