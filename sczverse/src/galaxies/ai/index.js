import { DISCIPLINES } from '../../data/disciplines.js';
export function render(){
  const d=DISCIPLINES.find(x=>x.id==='ai');
  const div=document.createElement('div');
  div.innerHTML=`
    <h2>🤖 ${d.name} 星系</h2>
    <p><small>${d.desc} | ${d.location} | ${d.teacher}</small></p>
    <div style="display:grid;grid-template-columns:1fr 340px;gap:20px">
      <div>
        <div style="background:rgba(0,255,204,0.08);border:1px solid #00ffcc;border-radius:16px;padding:16px">
          <h3>🔤 BPE分词器实验室 - 真实可运行</h3>
          <p style="font-size:11px;opacity:0.8">Byte Pair Encoding，来自你课题01待开，唐杰2026清华作业清单</p>
          <div style="margin-top:12px">
            <textarea id="bpe-input" style="width:100%;height:80px;background:#0a0a14;border:1px solid #00ffcc;border-radius:8px;color:white;padding:8px;font-family:monospace;font-size:12px" placeholder="输入句子，例如：涡轮叶片AI优化 74维设计">涡轮叶片AI优化 74维设计 知行合一</textarea>
            <div style="display:flex;gap:8px;margin-top:8px;flex-wrap:wrap">
              <button id="btn-bpe-train" style="padding:4px 12px;border-radius:20px;border:1px solid #00ffcc;background:rgba(0,255,204,0.2);color:white;cursor:pointer">训练BPE</button>
              <button id="btn-bpe-encode" style="padding:4px 12px;border-radius:20px;border:1px solid #00ffcc;background:rgba(0,255,204,0.2);color:white;cursor:pointer">编码</button>
              <label style="font-size:11px">合并次数 <input type="range" id="bpe-merges" min="5" max="100" value="30" style="width:80px"> <span id="bpe-merges-val">30</span></label>
            </div>
            <div id="bpe-output" style="margin-top:12px;font-family:monospace;font-size:11px;background:rgba(0,0,0,0.3);padding:12px;border-radius:8px;min-height:120px;white-space:pre-wrap"></div>
          </div>
          <canvas id="ai-canvas" style="width:100%;height:200px;background:#0a0a14;border-radius:12px;margin-top:12px"></canvas>
        </div>
      </div>
      <div>
        <div class="discipline-card"><b>核心公式</b><br><div style="font-family:monospace;font-size:11px">${d.formulas.map(f=>`<div style="margin:2px 0;padding:4px;background:rgba(0,255,204,0.1);border-radius:4px">${f}</div>`).join('')}</div></div>
        <div class="discipline-card"><b>三轨合一</b><br><small>课程轨: CORE100299 陈炜煌 1-8周<br>实训轨: 唐杰2026清华7条本地化 16周11课题 零预算Kaggle 2×T4 30h/周<br>知识轨: M0-M9知识地图 22项资源<br>大论文70%+平时30%</small></div>
        <div class="discipline-card"><b>唐杰作业清单</b><br><small>1. BPE分词器(本实验)<br>2. N-gram<br>3. Transformer<br>4. BERT<br>5. GPT<br>6. RAG<br>7. AI for Science(叶片)</small></div>
      </div>
    </div>
  `;
  setTimeout(()=>{
    const input=div.querySelector('#bpe-input');
    const output=div.querySelector('#bpe-output');
    const mergesSlider=div.querySelector('#bpe-merges');
    const mergesVal=div.querySelector('#bpe-merges-val');
    let merges=30, vocab=new Map(), mergeRules=[];
    mergesSlider.oninput=(e)=>{ merges=parseInt(e.target.value); mergesVal.textContent=merges; };
    const getTokens=(text)=>{ return [...text]; };
    const trainBPE=(text, numMerges)=>{
      let tokens=getTokens(text);
      const vocabCount=new Map();
      tokens.forEach(t=>vocabCount.set(t,(vocabCount.get(t)||0)+1));
      let currentTokens=tokens;
      const rules=[];
      for(let i=0;i<numMerges;i++){
        const pairs=new Map();
        for(let j=0;j<currentTokens.length-1;j++){ const pair=currentTokens[j]+'|'+currentTokens[j+1]; pairs.set(pair,(pairs.get(pair)||0)+1); }
        if(pairs.size===0) break;
        let maxPair=null, maxCount=0;
        for(const [p,c] of pairs){ if(c>maxCount){ maxCount=c; maxPair=p; } }
        if(!maxPair||maxCount<2) break;
        const [a,b]=maxPair.split('|');
        const merged=a+b;
        rules.push({from:[a,b], to:merged, count:maxCount});
        // merge
        const newTokens=[];
        for(let j=0;j<currentTokens.length;){
          if(j<currentTokens.length-1 && currentTokens[j]===a && currentTokens[j+1]===b){ newTokens.push(merged); j+=2; } else { newTokens.push(currentTokens[j]); j++; }
        }
        currentTokens=newTokens;
      }
      return {tokens:currentTokens, rules, vocab:vocabCount};
    };
    const encode=(text, rules)=>{
      let tokens=getTokens(text);
      for(const rule of rules){
        const newTokens=[];
        for(let j=0;j<tokens.length;){
          if(j<tokens.length-1 && tokens[j]===rule.from[0] && tokens[j+1]===rule.from[1]){ newTokens.push(rule.to); j+=2; } else { newTokens.push(tokens[j]); j++; }
        }
        tokens=newTokens;
      }
      return tokens;
    };
    div.querySelector('#btn-bpe-train').onclick=()=>{
      const text=input.value;
      const result=trainBPE(text, merges);
      mergeRules=result.rules;
      output.textContent=`训练完成! 原始长度: ${getTokens(text).length}, 合并后: ${result.tokens.length}\n`+
        `词表大小: ${result.vocab.size}\n`+
        `合并规则(${result.rules.length}):\n`+
        result.rules.slice(0,20).map((r,i)=>`${i+1}. ${r.from[0]}+${r.from[1]}→${r.to} (count=${r.count})`).join('\n')+
        `\n\n编码结果: [${result.tokens.join(' | ')}]`;
      drawTokens(result.tokens);
    };
    div.querySelector('#btn-bpe-encode').onclick=()=>{
      if(mergeRules.length===0){ output.textContent='请先训练!'; return; }
      const tokens=encode(input.value, mergeRules);
      output.textContent+=`\n\n---重新编码---\n[${tokens.join(' | ')}] 长度=${tokens.length}`;
      drawTokens(tokens);
    };
    const canvas=div.querySelector('#ai-canvas');
    const ctx=canvas.getContext('2d');
    const resize=()=>{ canvas.width=canvas.offsetWidth*2; canvas.height=200*2; };
    resize();
    const drawTokens=(tokens)=>{
      const w=canvas.width,h=canvas.height;
      ctx.clearRect(0,0,w,h);
      tokens.forEach((tok,i)=>{
        const x=(i/tokens.length)*w+10, y=h/2, ww=w/tokens.length-20;
        ctx.fillStyle=`hsl(${(i*30)%360},70%,60%)`; ctx.fillRect(x,y-20,ww,40);
        ctx.fillStyle='black'; ctx.font='12px monospace'; ctx.textAlign='center';
        ctx.fillText(tok.slice(0,8),x+ww/2,y+4);
      });
    };
    // auto train
    div.querySelector('#btn-bpe-train').click();
  },100);
  return div;
}
