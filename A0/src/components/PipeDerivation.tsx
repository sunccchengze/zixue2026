import { useState, useEffect, useRef, useCallback } from 'react';
import MathTex from './Math';

export default function PipeDerivation() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const animRef = useRef<number>(0);
  const [isRunning, setIsRunning] = useState(true);
  const timeRef = useRef(0);

  const draw = useCallback(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const W = canvas.width;
    const H = canvas.height;
    const cy = H / 2;

    if (isRunning) {
      timeRef.current += 0.02;
    }
    const t = timeRef.current;

    ctx.clearRect(0, 0, W, H);
    ctx.fillStyle = '#f8fafc';
    ctx.fillRect(0, 0, W, H);

    // Pipe geometry
    const r1 = 50;
    const r2 = 25;
    const pipeStart = 40;
    const section1 = W * 0.35;
    const section2 = W * 0.65;
    const pipeEnd = W - 40;

    // Draw pipe
    ctx.fillStyle = '#e2e8f0';
    // Top wall
    ctx.beginPath();
    ctx.moveTo(pipeStart, cy - r1);
    ctx.lineTo(section1, cy - r1);
    ctx.lineTo(section2, cy - r2);
    ctx.lineTo(pipeEnd, cy - r2);
    ctx.lineTo(pipeEnd, 0);
    ctx.lineTo(pipeStart, 0);
    ctx.closePath();
    ctx.fill();
    // Bottom wall
    ctx.beginPath();
    ctx.moveTo(pipeStart, cy + r1);
    ctx.lineTo(section1, cy + r1);
    ctx.lineTo(section2, cy + r2);
    ctx.lineTo(pipeEnd, cy + r2);
    ctx.lineTo(pipeEnd, H);
    ctx.lineTo(pipeStart, H);
    ctx.closePath();
    ctx.fill();

    // Pipe interior
    ctx.fillStyle = '#bfdbfe';
    ctx.beginPath();
    ctx.moveTo(pipeStart, cy - r1);
    ctx.lineTo(section1, cy - r1);
    ctx.lineTo(section2, cy - r2);
    ctx.lineTo(pipeEnd, cy - r2);
    ctx.lineTo(pipeEnd, cy + r2);
    ctx.lineTo(section2, cy + r2);
    ctx.lineTo(section1, cy + r1);
    ctx.lineTo(pipeStart, cy + r1);
    ctx.closePath();
    ctx.fill();

    // Pipe walls stroke
    ctx.strokeStyle = '#64748b';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(pipeStart, cy - r1);
    ctx.lineTo(section1, cy - r1);
    ctx.lineTo(section2, cy - r2);
    ctx.lineTo(pipeEnd, cy - r2);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(pipeStart, cy + r1);
    ctx.lineTo(section1, cy + r1);
    ctx.lineTo(section2, cy + r2);
    ctx.lineTo(pipeEnd, cy + r2);
    ctx.stroke();

    // Draw cross sections
    ctx.setLineDash([5, 3]);
    ctx.strokeStyle = '#3b82f6';
    ctx.lineWidth = 2;
    
    // Section 1
    const s1x = pipeStart + 60;
    ctx.beginPath();
    ctx.moveTo(s1x, cy - r1);
    ctx.lineTo(s1x, cy + r1);
    ctx.stroke();
    
    // Section 2
    const s2x = pipeEnd - 60;
    ctx.beginPath();
    ctx.moveTo(s2x, cy - r2);
    ctx.lineTo(s2x, cy + r2);
    ctx.stroke();
    
    ctx.setLineDash([]);

    // Draw animated fluid block showing conservation
    const blockWidth = 30;
    const cycleLength = 4; // seconds for full cycle
    const progress = (t % cycleLength) / cycleLength;
    
    // Block at section 1
    if (progress < 0.5) {
      const alpha = 1 - progress * 2;
      ctx.fillStyle = `rgba(34, 197, 94, ${alpha})`;
      ctx.strokeStyle = `rgba(22, 163, 74, ${alpha})`;
      ctx.lineWidth = 2;
      const bx = s1x - blockWidth / 2;
      ctx.fillRect(bx, cy - r1 + 5, blockWidth, r1 * 2 - 10);
      ctx.strokeRect(bx, cy - r1 + 5, blockWidth, r1 * 2 - 10);
    }
    
    // Block at section 2 (taller to show same volume needs more height)
    if (progress > 0.5) {
      const alpha = (progress - 0.5) * 2;
      ctx.fillStyle = `rgba(34, 197, 94, ${alpha})`;
      ctx.strokeStyle = `rgba(22, 163, 74, ${alpha})`;
      ctx.lineWidth = 2;
      // Same volume, smaller area → need longer length
      const volumeRatio = (r1 * r1) / (r2 * r2); // A1/A2
      const newBlockWidth = blockWidth * volumeRatio;
      const bx = s2x - newBlockWidth / 2;
      ctx.fillRect(bx, cy - r2 + 3, newBlockWidth, r2 * 2 - 6);
      ctx.strokeRect(bx, cy - r2 + 3, newBlockWidth, r2 * 2 - 6);
    }

    // Labels
    ctx.fillStyle = '#1e293b';
    ctx.font = 'bold 12px system-ui';
    ctx.textAlign = 'center';
    
    ctx.fillText('截面1', s1x, cy - r1 - 10);
    ctx.fillText('截面2', s2x, cy - r2 - 10);

    // Area labels
    ctx.font = '11px system-ui';
    ctx.fillStyle = '#3b82f6';
    ctx.fillText('A₁ (大)', s1x, cy + r1 + 15);
    ctx.fillText('A₂ (小)', s2x, cy + r2 + 15);

    // Velocity arrows
    const v1 = 20;
    const v2 = v1 * (r1 * r1) / (r2 * r2);
    
    ctx.strokeStyle = '#ef4444';
    ctx.fillStyle = '#ef4444';
    ctx.lineWidth = 3;
    
    // V1 arrow
    ctx.beginPath();
    ctx.moveTo(s1x + 5, cy);
    ctx.lineTo(s1x + 5 + v1, cy);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(s1x + 5 + v1, cy);
    ctx.lineTo(s1x + v1 - 3, cy - 5);
    ctx.lineTo(s1x + v1 - 3, cy + 5);
    ctx.closePath();
    ctx.fill();
    ctx.font = '10px system-ui';
    ctx.fillText('V₁', s1x + 15, cy - 10);

    // V2 arrow (longer!)
    ctx.beginPath();
    ctx.moveTo(s2x + 5, cy);
    ctx.lineTo(s2x + 5 + Math.min(v2, 60), cy);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(s2x + 5 + Math.min(v2, 60), cy);
    ctx.lineTo(s2x + Math.min(v2, 60) - 3, cy - 5);
    ctx.lineTo(s2x + Math.min(v2, 60) - 3, cy + 5);
    ctx.closePath();
    ctx.fill();
    ctx.fillText('V₂', s2x + 35, cy - 10);

    animRef.current = requestAnimationFrame(draw);
  }, [isRunning]);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const resizeObserver = new ResizeObserver(entries => {
      for (const entry of entries) {
        const { width, height } = entry.contentRect;
        canvas.width = width;
        canvas.height = height;
      }
    });
    resizeObserver.observe(canvas.parentElement!);

    animRef.current = requestAnimationFrame(draw);
    return () => {
      cancelAnimationFrame(animRef.current);
      resizeObserver.disconnect();
    };
  }, [draw]);

  return (
    <div className="space-y-4">
      <div className="p-4 rounded-xl bg-blue-50 border border-blue-200">
        <h3 className="font-bold text-blue-800 mb-3">🤔 V₁A₁ = V₂A₂ 是怎么来的？</h3>
        <div className="text-sm text-blue-900 space-y-2">
          <p><strong>前提：</strong>不可压缩 + 定常流动</p>
          <p><strong>原理：</strong>同一时间内，通过截面1的体积 = 通过截面2的体积</p>
          <div className="p-3 rounded bg-white/70 mt-2">
            <p className="text-xs text-slate-600 mb-2">体积 = 速度 × 面积 × 时间，取单位时间：</p>
            <div className="text-center">
              <MathTex tex="Q_1 = Q_2 \implies V_1 \cdot A_1 = V_2 \cdot A_2" display />
            </div>
          </div>
        </div>
      </div>

      <div className="relative w-full h-48 rounded-xl overflow-hidden border border-slate-200">
        <canvas ref={canvasRef} className="w-full h-full" />
      </div>
      
      <div className="text-xs text-center text-slate-500">
        🟢 绿色块表示同一团水 —— 通过细管时必须拉长，所以速度变快
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="p-4 rounded-xl bg-slate-50 border border-slate-200">
          <div className="text-center mb-2">
            <MathTex tex="A_1 > A_2" display />
          </div>
          <div className="text-center">
            <MathTex tex="\Rightarrow V_1 < V_2" display />
          </div>
          <p className="text-xs text-center text-slate-600 mt-2">
            面积变小 → 速度变大
          </p>
        </div>
        <div className="p-4 rounded-xl bg-slate-50 border border-slate-200">
          <div className="text-sm text-slate-700 mb-2"><strong>圆管直径关系：</strong></div>
          <div className="text-center">
            <MathTex tex="A = \pi \left(\frac{D}{2}\right)^2 \propto D^2" display />
          </div>
          <div className="text-center mt-2">
            <MathTex tex="V_2 = V_1 \times \left(\frac{D_1}{D_2}\right)^2" />
          </div>
        </div>
      </div>

      <button
        onClick={() => setIsRunning(!isRunning)}
        className="px-4 py-2 rounded-lg bg-slate-200 text-slate-700 font-medium hover:bg-slate-300 transition-colors text-sm"
      >
        {isRunning ? '⏸ 暂停' : '▶ 播放'}
      </button>
    </div>
  );
}
