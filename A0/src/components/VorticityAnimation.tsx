import { useState, useEffect, useRef, useCallback } from 'react';

type FlowType = 'rotational' | 'irrotational' | 'shear';

export default function VorticityAnimation() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const animRef = useRef<number>(0);
  const [flowType, setFlowType] = useState<FlowType>('rotational');
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

    // Background
    ctx.fillStyle = flowType === 'irrotational' ? '#f0fdf4' : flowType === 'rotational' ? '#fef3c7' : '#ede9fe';
    ctx.fillRect(0, 0, W, H);

    // Draw velocity field arrows
    const arrowSpacing = 45;
    for (let x = arrowSpacing; x < W; x += arrowSpacing) {
      for (let y = arrowSpacing; y < H; y += arrowSpacing) {
        const dx = x - cx;
        const dy = y - cy;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < 30) continue;

        let vx = 0, vy = 0;

        if (flowType === 'rotational') {
          // Rigid body rotation: v proportional to r
          vx = -dy * 0.02;
          vy = dx * 0.02;
        } else if (flowType === 'irrotational') {
          // Free vortex: v inversely proportional to r (irrotational!)
          const r2 = dx * dx + dy * dy;
          vx = -dy / r2 * 500;
          vy = dx / r2 * 500;
        } else {
          // Shear flow
          vx = 0.02 * (y - cy);
          vy = 0;
        }

        const mag = Math.sqrt(vx * vx + vy * vy);
        if (mag < 0.01) continue;
        const arrowLen = Math.min(mag * 20, 20);
        const endX = x + (vx / mag) * arrowLen;
        const endY = y + (vy / mag) * arrowLen;

        ctx.beginPath();
        ctx.moveTo(x, y);
        ctx.lineTo(endX, endY);
        ctx.strokeStyle = flowType === 'rotational' ? '#f59e0b' : flowType === 'irrotational' ? '#10b981' : '#8b5cf6';
        ctx.lineWidth = 1.5;
        ctx.stroke();

        // Arrow head
        const angle = Math.atan2(vy, vx);
        ctx.beginPath();
        ctx.moveTo(endX, endY);
        ctx.lineTo(endX - 5 * Math.cos(angle - 0.5), endY - 5 * Math.sin(angle - 0.5));
        ctx.moveTo(endX, endY);
        ctx.lineTo(endX - 5 * Math.cos(angle + 0.5), endY - 5 * Math.sin(angle + 0.5));
        ctx.stroke();
      }
    }

    // Draw a fluid element (small paddle wheel) at different positions
    const drawPaddle = (px: number, py: number, selfRotation: number, size: number) => {
      ctx.save();
      ctx.translate(px, py);
      ctx.rotate(selfRotation);

      // Paddle wheel
      ctx.strokeStyle = '#1e293b';
      ctx.lineWidth = 2;
      for (let i = 0; i < 4; i++) {
        const angle = (i / 4) * Math.PI * 2;
        ctx.beginPath();
        ctx.moveTo(0, 0);
        ctx.lineTo(Math.cos(angle) * size, Math.sin(angle) * size);
        ctx.stroke();
        // Small rectangle at end
        ctx.fillStyle = i % 2 === 0 ? '#ef4444' : '#3b82f6';
        ctx.fillRect(
          Math.cos(angle) * size - 4,
          Math.sin(angle) * size - 4,
          8,
          8
        );
      }

      // Center
      ctx.beginPath();
      ctx.arc(0, 0, 4, 0, Math.PI * 2);
      ctx.fillStyle = '#1e293b';
      ctx.fill();

      ctx.restore();
    };

    // Draw paddle wheels at different positions
    const positions = [
      { x: cx - 80, y: cy - 60 },
      { x: cx + 80, y: cy },
      { x: cx, y: cy + 70 },
    ];

    positions.forEach((pos, i) => {
      let selfRotation = 0;
      if (flowType === 'rotational') {
        // In rigid body rotation, paddles rotate with the flow
        selfRotation = t * 0.8;
      } else if (flowType === 'irrotational') {
        // In irrotational flow, paddles DON'T rotate (that's the key point!)
        selfRotation = 0;
      } else {
        // In shear flow, paddles rotate
        selfRotation = t * 0.5;
      }
      drawPaddle(pos.x, pos.y, selfRotation + i * 0.5, 18);
    });

    // Labels
    ctx.fillStyle = '#1e293b';
    ctx.font = 'bold 14px system-ui';
    ctx.textAlign = 'center';

    let title = '';
    let subtitle = '';
    if (flowType === 'rotational') {
      title = '有旋流动 (∇×V ≠ 0)';
      subtitle = '刚体旋转：微团自身会转动 🔄';
    } else if (flowType === 'irrotational') {
      title = '无旋流动 / 势流 (∇×V = 0)';
      subtitle = '自由涡：整体绕圈，但微团自身不转！✨';
    } else {
      title = '剪切流 (有旋)';
      subtitle = '速度差导致微团旋转 🔄';
    }

    ctx.fillText(title, cx, 22);
    ctx.font = '12px system-ui';
    ctx.fillStyle = '#64748b';
    ctx.fillText(subtitle, cx, 42);

    // Small legend showing paddle = fluid element
    ctx.font = '11px system-ui';
    ctx.textAlign = 'left';
    ctx.fillText('🎡 = 流体微团 (观察它是否自转)', 10, H - 10);

    animRef.current = requestAnimationFrame(draw);
  }, [flowType, isRunning]);

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
      <div className="relative w-full h-60 rounded-xl overflow-hidden border border-slate-200">
        <canvas ref={canvasRef} className="w-full h-full" />
      </div>
      <div className="flex flex-wrap gap-2">
        <button
          onClick={() => { setFlowType('rotational'); timeRef.current = 0; }}
          className={`px-3 py-2 rounded-lg text-sm font-medium transition-all ${
            flowType === 'rotational' ? 'bg-amber-500 text-white' : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
          }`}
        >
          🔄 刚体旋转 (有旋)
        </button>
        <button
          onClick={() => { setFlowType('irrotational'); timeRef.current = 0; }}
          className={`px-3 py-2 rounded-lg text-sm font-medium transition-all ${
            flowType === 'irrotational' ? 'bg-emerald-500 text-white' : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
          }`}
        >
          ✨ 自由涡 (无旋!)
        </button>
        <button
          onClick={() => { setFlowType('shear'); timeRef.current = 0; }}
          className={`px-3 py-2 rounded-lg text-sm font-medium transition-all ${
            flowType === 'shear' ? 'bg-purple-500 text-white' : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
          }`}
        >
          📐 剪切流 (有旋)
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
