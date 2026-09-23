export function render(){
  const div=document.createElement('div');
  div.innerHTML=`
    <h3>🤖 BPE分词器 - 真实可训练</h3>
    <p><small>Byte Pair Encoding，真实合并算法，来自AI基础课题01</small></p>
    <textarea id="ai-toy-input" style="width:100%;height:60px;background:#0a0a14;border:1px solid #00ffcc;border-radius:8px;color:white;padding:8px;font-size:12px">涡轮叶片AI优化 知行合一</textarea>
    <canvas id="c-ai-toy" class="game-canvas" style="height:200px"></canvas>
    <div class="game-controls"><button id="btn-ai-bpe">训练BPE</button><span id="ai-toy-info" style="font-size:11px;margin-left:12px"></span></div>
  `;
  setTimeout(()=>{
    const input=div.querySelector('#ai-toy-input');
    const canvas=div.querySelector('#c-ai-toy');
    const ctx=canvas.getContext('2d');
    const resize=()=>{ canvas.width=canvas.offsetWidth*2; canvas.height=200*2; };
    resize();
    const train=()=>{
      const text=input.value;
      let tokens=[...text];
      let rules=[];
      for(let i=0;i<20;i++){
        const pairs=new Map();
        for(let j=0;j<tokens.length-1;j++){ const p=tokens[j]+'|'+tokens[j+1]; pairs.set(p,(pairs.get(p)||0)+1); }
        let maxP=null,maxC=0; for(const [p,c] of pairs) if(c>maxC){ maxC=c; maxP=p; }
        if(!maxP||maxC<2) break;
        const [a,b]=maxP.split('|'); const m=a+b; rules.push({a,b,m});
        const nt=[]; for(let j=0;j<tokens.length;){ if(j<tokens.length-1&&tokens[j]===a&&tokens[j+1]===b){ nt.push(m); j+=2; } else { nt.push(tokens[j]); j++; } } tokens=nt;
      }
      ctx.clearRect(0,0,canvas.width,canvas.height);
      tokens.forEach((tok,i)=>{
        const x=i/tokens.length*canvas.width+5, w=canvas.width/tokens.length-10;
        ctx.fillStyle=`hsl(${i*30},70%,60%)`; ctx.fillRect(x,canvas.height/2-20,w,40);
        ctx.fillStyle='black'; ctx.font='12px monospace'; ctx.textAlign='center'; ctx.fillText(tok.slice(0,6),x+w/2,canvas.height/2+4);
      });
      div.querySelector('#ai-toy-info').textContent=`${[...text].length}→${tokens.length} tokens, ${rules.length} merges`;
    };
    div.querySelector('#btn-ai-bpe').onclick=train;
    train();
  },100);
  return div;
}
