import { useState, useEffect, useRef, useCallback } from 'react';

interface Particle {
  x: number;
  y: number;
  born: number;
}

export default function PipeFlow() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const animRef = useRef<number>(0);
  const [isRunning, setIsRunning] = useState(true);
  const [d1, setD1] = useState(100); // diameter 1
  const [d2, setD2] = useState(50);  // diameter 2
  const particlesRef = useRef<Particle[]>([]);
  const lastSpawnRef = useRef(0);

  // Calculate velocities from continuity: v1*A1 = v2*A2
  // A = pi * (d/2)^2, so v1 * d1^2 = v2 * d2^2
  const baseSpeed = 1;
  const v1 = baseSpeed;
  const v2 = v1 * (d1 * d1) / (d2 * d2);

  const draw = useCallback((timestamp: number) => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const W = canvas.width;
    const H = canvas.height;
    const cy = H / 2;

    ctx.clearRect(0, 0, W, H);

    // Pipe geometry
    const pipeStart = 30;
    const transitionStart = W * 0.35;
    const transitionEnd = W * 0.55;
    const pipeEnd = W - 30;

    const r1 = d1 / 2;
    const r2 = d2 / 2;

    const getRadius = (x: number) => {
      if (x < transitionStart) return r1;
      if (x > transitionEnd) return r2;
      const t = (x - transitionStart) / (transitionEnd - transitionStart);
      const smooth = t * t * (3 - 2 * t);
      return r1 - (r1 - r2) * smooth;
    };

    const getSpeed = (x: number) => {
      const r = getRadius(x);
      return v1 * (r1 * r1) / (r * r);
    };

    // Draw pipe walls
    ctx.fillStyle = '#e2e8f0';
    ctx.beginPath();
    ctx.moveTo(pipeStart, cy - r1);
    for (let x = pipeStart; x <= pipeEnd; x += 2) {
      ctx.lineTo(x, cy - getRadius(x));
    }
    ctx.lineTo(pipeEnd, 0);
    ctx.lineTo(pipeStart, 0);
    ctx.closePath();
    ctx.fill();

    ctx.beginPath();
    ctx.moveTo(pipeStart, cy + r1);
    for (let x = pipeStart; x <= pipeEnd; x += 2) {
      ctx.lineTo(x, cy + getRadius(x));
    }
    ctx.lineTo(pipeEnd, H);
    ctx.lineTo(pipeStart, H);
    ctx.closePath();
    ctx.fill();

    // Draw pipe interior
    ctx.beginPath();
    ctx.moveTo(pipeStart, cy - r1);
    for (let x = pipeStart; x <= pipeEnd; x += 2) {
      ctx.lineTo(x, cy - getRadius(x));
    }
    for (let x = pipeEnd; x >= pipeStart; x -= 2) {
      ctx.lineTo(x, cy + getRadius(x));
    }
    ctx.closePath();
    ctx.fillStyle = 'rgba(186, 230, 253, 0.5)';
    ctx.fill();

    // Draw pipe walls stroke
    ctx.beginPath();
    ctx.moveTo(pipeStart, cy - r1);
    for (let x = pipeStart; x <= pipeEnd; x += 2) {
      ctx.lineTo(x, cy - getRadius(x));
    }
    ctx.strokeStyle = '#64748b';
    ctx.lineWidth = 3;
    ctx.stroke();

    ctx.beginPath();
    ctx.moveTo(pipeStart, cy + r1);
    for (let x = pipeStart; x <= pipeEnd; x += 2) {
      ctx.lineTo(x, cy + getRadius(x));
    }
    ctx.stroke();

    // Spawn particles
    if (isRunning && timestamp - lastSpawnRef.current > 150) {
      const r = r1;
      for (let i = 0; i < 4; i++) {
        particlesRef.current.push({
          x: pipeStart,
          y: cy + (Math.random() - 0.5) * 2 * (r - 5),
          born: timestamp,
        });
      }
      lastSpawnRef.current = timestamp;
    }

    // Update and draw particles
    particlesRef.current = particlesRef.current.filter(p => {
      if (isRunning) {
        const speed = getSpeed(p.x);
        p.x += speed * 1.2;

        // Constrain y within pipe
        const r = getRadius(p.x);
        const relY = p.y - cy;
        const maxRelY = r - 4;
        if (Math.abs(relY) > maxRelY) {
          p.y = cy + Math.sign(relY) * maxRelY;
        }
      }

      if (p.x > pipeEnd + 20) return false;

      // Color by speed
      const speed = getSpeed(p.x);
      const maxSpeed = v2;
      const t = Math.min(speed / maxSpeed, 1);
      const r_c = Math.floor(59 + t * 180);
      const g_c = Math.floor(130 - t * 50);
      const b_c = Math.floor(246 - t * 200);

      ctx.beginPath();
      ctx.arc(p.x, p.y, 4, 0, Math.PI * 2);
      ctx.fillStyle = `rgb(${r_c}, ${g_c}, ${b_c})`;
      ctx.fill();

      return true;
    });

    // Draw dimension labels
    ctx.fillStyle = '#1e293b';
    ctx.font = 'bold 12px system-ui';
    ctx.textAlign = 'center';

    // D1 label
    ctx.fillText(`D₁ = ${d1}`, pipeStart + 60, cy - r1 - 15);
    // D1 dimension line
    ctx.strokeStyle = '#64748b';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(pipeStart + 60, cy - r1 - 5);
    ctx.lineTo(pipeStart + 60, cy + r1 + 5);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(pipeStart + 55, cy - r1);
    ctx.lineTo(pipeStart + 65, cy - r1);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(pipeStart + 55, cy + r1);
    ctx.lineTo(pipeStart + 65, cy + r1);
    ctx.stroke();

    // D2 label
    ctx.fillText(`D₂ = ${d2}`, pipeEnd - 60, cy - r2 - 15);
    // D2 dimension line
    ctx.beginPath();
    ctx.moveTo(pipeEnd - 60, cy - r2 - 5);
    ctx.lineTo(pipeEnd - 60, cy + r2 + 5);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(pipeEnd - 65, cy - r2);
    ctx.lineTo(pipeEnd - 55, cy - r2);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(pipeEnd - 65, cy + r2);
    ctx.lineTo(pipeEnd - 55, cy + r2);
    ctx.stroke();

    // Velocity labels
    ctx.fillStyle = '#3b82f6';
    ctx.fillText(`V₁ = ${v1.toFixed(2)}`, pipeStart + 60, cy + r1 + 25);
    ctx.fillStyle = '#ef4444';
    ctx.fillText(`V₂ = ${v2.toFixed(2)}`, pipeEnd - 60, cy + r2 + 25);

    // Formula
    ctx.fillStyle = '#1e293b';
    ctx.font = 'bold 14px system-ui';
    ctx.textAlign = 'center';
    ctx.fillText('V₁ × A₁ = V₂ × A₂  (体积流量守恒)', W / 2, 25);

    // Ratio display
    const ratio = (d1 * d1) / (d2 * d2);
    ctx.font = '12px system-ui';
    ctx.fillStyle = '#64748b';
    ctx.fillText(`面积比 A₁/A₂ = (D₁/D₂)² = ${ratio.toFixed(1)} → 速度比 V₂/V₁ = ${ratio.toFixed(1)}`, W / 2, 45);

    animRef.current = requestAnimationFrame(draw);
  }, [d1, d2, v1, v2, isRunning]);

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
      <div className="relative w-full h-56 bg-slate-50 rounded-xl overflow-hidden border border-slate-200">
        <canvas ref={canvasRef} className="w-full h-full" />
      </div>
      <div className="grid grid-cols-2 gap-4">
        <div className="space-y-2">
          <label className="flex items-center justify-between text-sm font-medium text-blue-700">
            <span>粗管直径 D₁</span>
            <span className="font-mono">{d1}</span>
          </label>
          <input
            type="range"
            min="60"
            max="120"
            value={d1}
            onChange={e => setD1(Number(e.target.value))}
            className="w-full h-2 rounded-lg appearance-none cursor-pointer accent-blue-500"
          />
        </div>
        <div className="space-y-2">
          <label className="flex items-center justify-between text-sm font-medium text-red-700">
            <span>细管直径 D₂</span>
            <span className="font-mono">{d2}</span>
          </label>
          <input
            type="range"
            min="30"
            max="100"
            value={d2}
            onChange={e => setD2(Number(e.target.value))}
            className="w-full h-2 rounded-lg appearance-none cursor-pointer accent-red-500"
          />
        </div>
      </div>
      <div className="flex gap-2 flex-wrap">
        <button
          onClick={() => { setD1(100); setD2(50); }}
          className="px-3 py-2 rounded-lg bg-blue-100 text-blue-700 font-medium hover:bg-blue-200 transition-colors text-sm"
        >
          2倍收缩
        </button>
        <button
          onClick={() => { setD1(100); setD2(100); }}
          className="px-3 py-2 rounded-lg bg-slate-100 text-slate-700 font-medium hover:bg-slate-200 transition-colors text-sm"
        >
          等径管
        </button>
        <button
          onClick={() => { setD1(60); setD2(100); }}
          className="px-3 py-2 rounded-lg bg-emerald-100 text-emerald-700 font-medium hover:bg-emerald-200 transition-colors text-sm"
        >
          扩张管
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
