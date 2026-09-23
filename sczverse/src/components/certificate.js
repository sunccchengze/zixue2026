
export function generateCertificate(){
  const div=document.createElement('div');
  div.innerHTML=`
    <div style="background:linear-gradient(135deg,#1a1a3a,#0a0a2a);border:2px solid #7c5cff;border-radius:20px;padding:40px;text-align:center;color:white;position:relative;overflow:hidden">
      <div style="position:absolute;inset:0;background:radial-gradient(circle at 30% 20%,rgba(124,92,255,0.2),transparent)"></div>
      <div style="position:relative;z-index:1">
        <div style="font-size:48px">🌌</div>
        <h1 style="font-size:28px;margin:16px 0;letter-spacing:4px">SCZVERSE 宇宙探索证书</h1>
        <p style="opacity:0.8">兹证明</p>
        <h2 style="font-size:36px;color:#00f5ff;margin:12px 0">孙承泽</h2>
        <p style="font-family:monospace;opacity:0.6">2253710052 · 能动强基2501 · 西安交通大学</p>
        <p style="margin:20px 0;line-height:1.8">已成功探索承泽宇宙全部10大星系<br>掌握概率、力学、复变、物理、化学、东方智慧、AI等<br>驱动涡轮引擎推力 114514 N，捏捏小鹰好感度 MAX</p>
        <div style="display:flex;justify-content:center;gap:20px;margin:20px 0">
          <span>🎲 概率</span><span>🌊 数理</span><span>🏗️ 力学</span><span>🌀 复变</span><span>⚛️ 物理</span>
        </div>
        <p style="font-size:11px;opacity:0.5;margin-top:30px">签发于 2026-09-23 · SCZVERSE v1.0 · 涡轮驱动 · 小鹰见证 · 禅意加持</p>
        <button onclick="window.print()" style="margin-top:20px;padding:8px 20px;border-radius:20px;border:1px solid #7c5cff;background:rgba(124,92,255,0.2);color:white;cursor:pointer">🖨️ 打印证书</button>
      </div>
    </div>
  `;
  return div;
}
