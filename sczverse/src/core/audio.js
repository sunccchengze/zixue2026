
export class AudioEngine{
  constructor(){
    this.ctx = null; this.enabled = false; this.ambientNode = null;
  }
  init(){
    if(this.ctx) return;
    this.ctx = new (window.AudioContext||window.webkitAudioContext)();
  }
  playTone(freq, dur=0.3, type='sine'){
    if(!this.enabled) return;
    this.init();
    const o = this.ctx.createOscillator();
    const g = this.ctx.createGain();
    o.type = type; o.frequency.value = freq;
    o.connect(g); g.connect(this.ctx.destination);
    g.gain.setValueAtTime(0.3,this.ctx.currentTime);
    g.gain.exponentialRampToValueAtTime(0.001,this.ctx.currentTime+dur);
    o.start(); o.stop(this.ctx.currentTime+dur);
  }
  playAmbient(){
    if(!this.enabled) return;
    this.init();
    // gentle drone
  }
  toggle(){
    this.enabled = !this.enabled;
    document.getElementById('btn-sound').textContent = this.enabled?'🔊':'🔇';
    if(this.enabled){ this.init(); this.playTone(220,0.6); this.playTone(330,0.6); }
  }
  playSuper(){
    [261,330,392,523].forEach((f,i)=>setTimeout(()=>this.playTone(f,0.4,'sawtooth'),i*120));
  }
}
