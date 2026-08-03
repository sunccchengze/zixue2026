import { useState, useEffect, useRef, useCallback } from 'react';

interface Particle {
  x: number;
  y: number;
  vx: number;
  vy: number;
}

export default function ContinuityBox() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const animRef = useRef<number>(0);
  const [isRunning, setIsRunning] = useState(true);
  const [inflow, setInflow] = useState(3);
  const [outflow, setOutflow] = useState(3);
  const particlesRef = useRef<Particle[]>([]);
  const densityRef = useRef(1);
  const lastSpawnRef = useRef(0);

  const draw = useCallback((timestamp: number) => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const W = canvas.width;
    const H = canvas.height;

    ctx.clearRect(0, 0, W, H);

    // Control box dimensions
    const boxLeft = W * 0.25;
    const boxRight = W * 0.75;
    const boxTop = H * 0.2;
    const boxBottom = H * 0.8;
    const boxWidth = boxRight - boxLeft;
    const boxHeight = boxBottom - boxTop;

    // Background
    ctx.fillStyle = '#f8fafc';
    ctx.fillRect(0, 0, W, H);

    // Draw the control volume box
    ctx.strokeStyle = '#3b82f6';
    ctx.lineWidth = 3;
    ctx.setLineDash([8, 4]);
    ctx.strokeRect(boxLeft, boxTop, boxWidth, boxHeight);
    ctx.setLineDash([]);

    // Fill with density-based color
    ctx.fillStyle = `rgba(59, 130, 246, ${0.05 + densityRef.current * 0.1})`;
    ctx.fillRect(boxLeft, boxTop, boxWidth, boxHeight);

    // Draw inflow and outflow arrows
    // Left arrow (inflow)
    ctx.fillStyle = '#10b981';
    ctx.beginPath();
    ctx.moveTo(boxLeft - 30, H / 2 - 15);
    ctx.lineTo(boxLeft - 30, H / 2 + 15);
    ctx.lineTo(boxLeft - 5, H / 2);
    ctx.closePath();
    ctx.fill();
    ctx.fillStyle = '#065f46';
    ctx.font = 'bold 12px system-ui';
    ctx.textAlign = 'center';
    ctx.fillText(`流入: ${inflow}`, boxLeft - 40, H / 2 + 35);

    // Right arrow (outflow)
    ctx.fillStyle = '#ef4444';
    ctx.beginPath();
    ctx.moveTo(boxRight + 5, H / 2 - 15);
    ctx.lineTo(boxRight + 5, H / 2 + 15);
    ctx.lineTo(boxRight + 30, H / 2);
    ctx.closePath();
    ctx.fill();
    ctx.fillStyle = '#991b1b';
    ctx.fillText(`流出: ${outflow}`, boxRight + 40, H / 2 + 35);

    // Spawn particles from left
    if (isRunning && timestamp - lastSpawnRef.current > 300 / inflow) {
      for (let i = 0; i < inflow; i++) {
        particlesRef.current.push({
          x: boxLeft - 20,
          y: boxTop + (boxHeight / (inflow + 1)) * (i + 1),
          vx: 1 + Math.random() * 0.5,
          vy: (Math.random() - 0.5) * 0.3,
        });
      }
      lastSpawnRef.current = timestamp;
    }

    // Update and draw particles
    if (isRunning) {
      particlesRef.current = particlesRef.current.filter(p => {
        // Inside box: move slower, bounce around
        if (p.x > boxLeft && p.x < boxRight) {
          p.vx *= 0.99;
          p.vy *= 0.95;
          p.vy += (Math.random() - 0.5) * 0.1;
          
          // Bounce off top/bottom
          if (p.y < boxTop + 10 || p.y > boxBottom - 10) {
            p.vy *= -0.8;
          }
          
          // Only some particles escape based on outflow rate
          if (p.x > boxRight - 20 && Math.random() < outflow / 10) {
            p.vx = 1.5;
          } else if (p.x > boxRight - 20) {
            p.vx *= 0.3;
          }
        }

        p.x += p.vx;
        p.y += p.vy;

        return p.x < W + 20;
      });

      // Calculate density (particles in box)
      const inBox = particlesRef.current.filter(
        p => p.x > boxLeft && p.x < boxRight && p.y > boxTop && p.y < boxBottom
      ).length;
      densityRef.current = densityRef.current * 0.98 + (inBox / 15) * 0.02;
    }

    // Draw particles
    particlesRef.current.forEach(p => {
      ctx.beginPath();
      ctx.arc(p.x, p.y, 4, 0, Math.PI * 2);
      if (p.x < boxLeft) {
        ctx.fillStyle = '#10b981';
      } else if (p.x > boxRight) {
        ctx.fillStyle = '#ef4444';
      } else {
        ctx.fillStyle = '#3b82f6';
      }
      ctx.fill();
    });

    // Draw labels
    ctx.fillStyle = '#1e293b';
    ctx.font = 'bold 14px system-ui';
    ctx.textAlign = 'center';
    ctx.fillText('控制体 (虚拟盒子)', boxLeft + boxWidth / 2, boxTop - 10);

    // Net flow indicator
    const netFlow = inflow - outflow;
    let statusText = '';
    let statusColor = '';
    if (netFlow > 0) {
      statusText = `流入 > 流出 → 盒内质量增加 ↑`;
      statusColor = '#10b981';
    } else if (netFlow < 0) {
      statusText = `流出 > 流入 → 盒内质量减少 ↓`;
      statusColor = '#ef4444';
    } else {
      statusText = `流入 = 流出 → 质量守恒 ✓ (定常)`;
      statusColor = '#3b82f6';
    }
    ctx.fillStyle = statusColor;
    ctx.font = 'bold 13px system-ui';
    ctx.fillText(statusText, W / 2, boxBottom + 25);

    // Density indicator
    ctx.font = '12px system-ui';
    ctx.fillStyle = '#64748b';
    ctx.fillText(`盒内相对密度: ${densityRef.current.toFixed(2)}`, W / 2, boxBottom + 45);

    animRef.current = requestAnimationFrame(draw);
  }, [inflow, outflow, isRunning]);

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
      <div className="relative w-full h-64 rounded-xl overflow-hidden border border-slate-200 bg-white">
        <canvas ref={canvasRef} className="w-full h-full" />
      </div>
      <div className="grid grid-cols-2 gap-4">
        <div className="space-y-2">
          <label className="flex items-center justify-between text-sm font-medium text-emerald-700">
            <span>🟢 流入速率</span>
            <span className="font-mono">{inflow}</span>
          </label>
          <input
            type="range"
            min="1"
            max="6"
            value={inflow}
            onChange={e => setInflow(Number(e.target.value))}
            className="w-full h-2 rounded-lg appearance-none cursor-pointer accent-emerald-500"
          />
        </div>
        <div className="space-y-2">
          <label className="flex items-center justify-between text-sm font-medium text-red-700">
            <span>🔴 流出速率</span>
            <span className="font-mono">{outflow}</span>
          </label>
          <input
            type="range"
            min="1"
            max="6"
            value={outflow}
            onChange={e => setOutflow(Number(e.target.value))}
            className="w-full h-2 rounded-lg appearance-none cursor-pointer accent-red-500"
          />
        </div>
      </div>
      <div className="flex gap-2">
        <button
          onClick={() => { setInflow(3); setOutflow(3); }}
          className="px-4 py-2 rounded-lg bg-blue-100 text-blue-700 font-medium hover:bg-blue-200 transition-colors text-sm"
        >
          ⚖️ 平衡 (定常)
        </button>
        <button
          onClick={() => { setInflow(5); setOutflow(2); }}
          className="px-4 py-2 rounded-lg bg-emerald-100 text-emerald-700 font-medium hover:bg-emerald-200 transition-colors text-sm"
        >
          📈 累积
        </button>
        <button
          onClick={() => { setInflow(2); setOutflow(5); }}
          className="px-4 py-2 rounded-lg bg-red-100 text-red-700 font-medium hover:bg-red-200 transition-colors text-sm"
        >
          📉 消耗
        </button>
        <button
          onClick={() => setIsRunning(!isRunning)}
          className="ml-auto px-3 py-2 rounded-lg bg-slate-200 text-slate-700 font-medium hover:bg-slate-300 transition-colors text-sm"
        >
          {isRunning ? '⏸ 暂停' : '▶ 播放'}
        </button>
      </div>
    </div>
  );
}
