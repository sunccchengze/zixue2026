import { useState, useEffect, useRef, useCallback } from 'react';

type DivType = 'positive' | 'zero' | 'negative';

export default function DivergenceAnimation() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const animRef = useRef<number>(0);
  const [divType, setDivType] = useState<DivType>('positive');
  const [isRunning, setIsRunning] = useState(true);
  const timeRef = useRef(0);

  const draw = useCallback(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const W = canvas.width;
    const H = canvas.height;
    const cx = W / 2;
    const cy = H / 2;

    if (isRunning) {
      timeRef.current += 0.02;
    }
    const t = timeRef.current;

    ctx.clearRect(0, 0, W, H);

    // Background gradient
    const gradient = ctx.createRadialGradient(cx, cy, 0, cx, cy, Math.max(W, H) / 2);
    if (divType === 'positive') {
      gradient.addColorStop(0, '#fef3c7');
      gradient.addColorStop(1, '#fef9c3');
    } else if (divType === 'negative') {
      gradient.addColorStop(0, '#dbeafe');
      gradient.addColorStop(1, '#eff6ff');
    } else {
      gradient.addColorStop(0, '#f0fdf4');
      gradient.addColorStop(1, '#f0fdf4');
    }
    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, W, H);

    // Draw velocity arrows showing the flow field
    const arrowSpacing = 50;
    for (let x = arrowSpacing; x < W; x += arrowSpacing) {
      for (let y = arrowSpacing; y < H; y += arrowSpacing) {
        const dx = x - cx;
        const dy = y - cy;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < 20) continue;

        let vx = 0, vy = 0;
        const speed = 0.5;

        if (divType === 'positive') {
          // Outward flow (source)
          vx = (dx / dist) * speed;
          vy = (dy / dist) * speed;
        } else if (divType === 'negative') {
          // Inward flow (sink)
          vx = -(dx / dist) * speed;
          vy = -(dy / dist) * speed;
        } else {
          // Zero divergence (circular flow)
          vx = (-dy / dist) * speed;
          vy = (dx / dist) * speed;
        }

        const arrowLen = 18;
        const endX = x + vx * arrowLen;
        const endY = y + vy * arrowLen;

        ctx.beginPath();
        ctx.moveTo(x, y);
        ctx.lineTo(endX, endY);
        ctx.strokeStyle = divType === 'positive' ? '#f59e0b' : divType === 'negative' ? '#3b82f6' : '#10b981';
        ctx.lineWidth = 1.5;
        ctx.stroke();

        // Arrow head
        const angle = Math.atan2(vy, vx);
        ctx.beginPath();
        ctx.moveTo(endX, endY);
        ctx.lineTo(endX - 6 * Math.cos(angle - 0.5), endY - 6 * Math.sin(angle - 0.5));
        ctx.moveTo(endX, endY);
        ctx.lineTo(endX - 6 * Math.cos(angle + 0.5), endY - 6 * Math.sin(angle + 0.5));
        ctx.stroke();
      }
    }

    // Draw the fluid element
    let scale = 1;
    if (divType === 'positive') {
      scale = 1 + 0.3 * (1 - Math.exp(-t * 0.5));
      if (scale > 1.5) {
        timeRef.current = 0;
        scale = 1;
      }
    } else if (divType === 'negative') {
      scale = 1 - 0.3 * (1 - Math.exp(-t * 0.5));
      if (scale < 0.5) {
        timeRef.current = 0;
        scale = 1;
      }
    }

    const baseSize = 40;
    const size = baseSize * scale;

    // Draw element with slight rotation for zero-div case
    let rotation = 0;
    if (divType === 'zero') {
      rotation = t * 0.5;
    }

    ctx.save();
    ctx.translate(cx, cy);
    ctx.rotate(rotation);

    // Draw the square element
    ctx.fillStyle = divType === 'positive' ? '#fbbf2450' : divType === 'negative' ? '#60a5fa50' : '#34d39950';
    ctx.strokeStyle = divType === 'positive' ? '#f59e0b' : divType === 'negative' ? '#3b82f6' : '#10b981';
    ctx.lineWidth = 3;
    ctx.fillRect(-size, -size, size * 2, size * 2);
    ctx.strokeRect(-size, -size, size * 2, size * 2);

    // Corner dots
    const corners = [[-size, -size], [size, -size], [size, size], [-size, size]];
    corners.forEach(([x, y], i) => {
      ctx.beginPath();
      ctx.arc(x, y, 5, 0, Math.PI * 2);
      ctx.fillStyle = i === 0 ? '#ef4444' : (divType === 'positive' ? '#f59e0b' : divType === 'negative' ? '#3b82f6' : '#10b981');
      ctx.fill();
    });

    ctx.restore();

    // Draw volume indicator
    const volume = (scale * scale).toFixed(2);
    ctx.fillStyle = '#1e293b';
    ctx.font = 'bold 14px system-ui';
    ctx.textAlign = 'center';

    let title = '';
    let subtitle = '';
    if (divType === 'positive') {
      title = '∇·V > 0 (散度为正)';
      subtitle = `体积膨胀中... 相对体积: ${volume}`;
    } else if (divType === 'negative') {
      title = '∇·V < 0 (散度为负)';
      subtitle = `体积收缩中... 相对体积: ${volume}`;
    } else {
      title = '∇·V = 0 (不可压缩!)';
      subtitle = '体积不变，但可以旋转变形';
    }

    ctx.fillText(title, cx, 22);
    ctx.font = '12px system-ui';
    ctx.fillStyle = '#64748b';
    ctx.fillText(subtitle, cx, 42);

    animRef.current = requestAnimationFrame(draw);
  }, [divType, isRunning]);

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
      <div className="relative w-full h-56 rounded-xl overflow-hidden border border-slate-200">
        <canvas ref={canvasRef} className="w-full h-full" />
      </div>
      <div className="flex flex-wrap gap-2">
        <button
          onClick={() => { setDivType('positive'); timeRef.current = 0; }}
          className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
            divType === 'positive' ? 'bg-amber-500 text-white' : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
          }`}
        >
          💥 膨胀 (∇·V &gt; 0)
        </button>
        <button
          onClick={() => { setDivType('negative'); timeRef.current = 0; }}
          className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
            divType === 'negative' ? 'bg-blue-500 text-white' : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
          }`}
        >
          🌀 收缩 (∇·V &lt; 0)
        </button>
        <button
          onClick={() => { setDivType('zero'); timeRef.current = 0; }}
          className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
            divType === 'zero' ? 'bg-emerald-500 text-white' : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
          }`}
        >
          💧 不可压缩 (∇·V = 0)
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
