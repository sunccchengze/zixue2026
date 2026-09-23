import { DISCIPLINES } from '../data/disciplines.js';
export function generateCertificate(){
  const div=document.createElement('div');
  const explored=JSON.parse(localStorage.getItem('scz-explored')||'[]');
  const total=DISCIPLINES.length;
  div.innerHTML=`
    <div style="background:linear-gradient(135deg,#1a1a3a,#0a0a2a);border:2px solid #7c5cff;border-radius:20px;padding:40px;text-align:center;color:white;position:relative;overflow:hidden">
      <div style="position:absolute;inset:0;background:radial-gradient(circle at 30% 20%,rgba(124,92,255,0.2),transparent)"></div>
      <div style="position:relative;z-index:1">
        <div style="font-size:48px">🌌</div>
        <h1 style="font-size:28px;margin:16px 0;letter-spacing:4px">SCZVERSE 宇宙探索证书</h1>
        <p style="opacity:0.8">兹证明</p>
        <h2 style="font-size:36px;color:#00f5ff;margin:12px 0">孙承泽</h2>
        <p style="font-family:monospace;opacity:0.6">2253710052 · 能动强基2501 · 西安交通大学</p>
        <p style="margin:20px 0;line-height:1.8">已成功探索承泽宇宙 ${explored.length}/${total} 大星系<br>掌握真实实验室：大数定律/力系平衡/复平面/简谐振动/化学平衡/BPE分词/涡轮NACA/小鹰软体<br>驱动涡轮引擎推力 ${localStorage.getItem('scz-thrust')||'7400'} N，捏捏小鹰好感度 MAX</p>
        <div style="display:flex;justify-content:center;gap:10px;margin:20px 0;flex-wrap:wrap">
          ${DISCIPLINES.map(d=>`<span style="background:${explored.includes(d.id)?d.color+'40':'rgba(255,255,255,0.05)'};border:1px solid ${d.color};padding:4px 8px;border-radius:12px;font-size:11px">${d.emoji} ${d.name.slice(0,2)} ${explored.includes(d.id)?'✅':''}</span>`).join('')}
        </div>
        <div style="font-family:monospace;font-size:11px;background:rgba(0,0,0,0.3);padding:12px;border-radius:8px;text-align:left;margin-top:20px">
          <b>真实可用功能清单：</b><br>
          ✅ 概率：大数定律切比雪夫真实计算 n>2917<br>
          ✅ 力学：ΣF=0 ΣM=0真实平衡，主矢主矩<br>
          ✅ 复变：e^{iθ}旋转，共轭，棣莫弗，x³=1等边三角形<br>
          ✅ 物理：m x''+b x'+k x=0真实求解，能量守恒<br>
          ✅ 数理：波动u_tt=a²u_xx有限差分，热传导<br>
          ✅ 化学：ΔG=ΔH-TΔS, K=exp(-ΔG/RT)真实计算<br>
          ✅ 东方：涟漪枯山水，真实打脸链路<br>
          ✅ AI：BPE分词器真实训练合并<br>
          ✅ 英语：学术写作检查，词汇星系<br>
          ✅ 涡轮：真实NACA 4-digit公式，74维<br>
          ✅ 小鹰：软体挤压，眼球跟随，拖拽物理<br>
        </div>
        <p style="font-size:11px;opacity:0.5;margin-top:30px">签发于 2026-09-23 · SCZVERSE v2.0真实可用版 · 涡轮驱动 · 小鹰见证 · 禅意加持<br>已探索: ${explored.join(', ')||'无'}</p>
        <button onclick="window.print()" style="margin-top:20px;padding:8px 20px;border-radius:20px;border:1px solid #7c5cff;background:rgba(124,92,255,0.2);color:white;cursor:pointer">🖨️ 打印证书</button>
      </div>
    </div>
  `;
  return div;
}
