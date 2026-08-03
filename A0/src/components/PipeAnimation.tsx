import { useEffect, useRef, useState, useCallback } from 'react';


interface Particle {
  id: number;
  x: number;
  y: number;
  born: number;
}

export default function PipeAnimation() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const animRef = useRef<number>(0);
  const [isRunning, setIsRunning] = useState(true);
  const [trackedParticle, setTrackedParticle] = useState<{x: number; speed: number} | null>(null);
  const particlesRef = useRef<Particle[]>([]);
  const nextIdRef = useRef(0);
  const lastSpawnRef = useRef(0);

  // Pipe geometry
  const getPipeRadius = (x: number, width: number) => {
    const normalizedX = x / width;
    // Wide on left, narrow on right
    const maxR = 80;
    const minR = 30;
    if (normalizedX < 0.3) return maxR;
    if (normalizedX > 0.7) return minR;
    // Smooth transition
    const t = (normalizedX - 0.3) / 0.4;
    const smooth = t * t * (3 - 2 * t); // smoothstep
    return maxR - (maxR - minR) * smooth;
  };

  const getSpeed = (x: number, width: number) => {
    const r = getPipeRadius(x, width);
    // v * A = const (continuity), A ~ r^2
    const maxR = 80;
    const baseSpeed = 1.2;
    return baseSpeed * (maxR * maxR) / (r * r);
  };

  const draw = useCallback((time: number) => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const W = canvas.width;
    const H = canvas.height;
    const centerY = H / 2;

    ctx.clearRect(0, 0, W, H);

    // Draw pipe walls
    ctx.beginPath();
    ctx.moveTo(0, centerY - getPipeRadius(0, W));
    for (let x = 0; x <= W; x += 2) {
      ctx.lineTo(x, centerY - getPipeRadius(x, W));
    }
    ctx.strokeStyle = '#64748b';
    ctx.lineWidth = 3;
    ctx.stroke();

    ctx.beginPath();
    ctx.moveTo(0, centerY + getPipeRadius(0, W));
    for (let x = 0; x <= W; x += 2) {
      ctx.lineTo(x, centerY + getPipeRadius(x, W));
    }
    ctx.stroke();

    // Fill pipe interior with light blue
    ctx.beginPath();
    ctx.moveTo(0, centerY - getPipeRadius(0, W));
    for (let x = 0; x <= W; x += 2) {
      ctx.lineTo(x, centerY - getPipeRadius(x, W));
    }
    for (let x = W; x >= 0; x -= 2) {
      ctx.lineTo(x, centerY + getPipeRadius(x, W));
    }
    ctx.closePath();
    ctx.fillStyle = 'rgba(186, 230, 253, 0.4)';
    ctx.fill();

    // Spawn new particles
    if (isRunning && time - lastSpawnRef.current > 200) {
      const r = getPipeRadius(0, W);
      for (let i = 0; i < 3; i++) {
        particlesRef.current.push({
          id: nextIdRef.current++,
          x: 0,
          y: centerY + (Math.random() - 0.5) * 2 * (r - 6),
          born: time,
        });
      }
      lastSpawnRef.current = time;
    }

    // Update and draw particles
    let tracked: {x: number; speed: number} | null = null;
    const dt = 16; // ~60fps step

    particlesRef.current = particlesRef.current.filter(p => {
      if (isRunning) {
        const speed = getSpeed(p.x, W);
        p.x += speed * dt * 0.06;

        // Constrain y within pipe
        const r = getPipeRadius(p.x, W);
        const relY = (p.y - centerY);
        const maxRelY = r - 6;
        if (Math.abs(relY) > maxRelY) {
          p.y = centerY + Math.sign(relY) * maxRelY;
        }
      }

      if (p.x > W) return false;

      const speed = getSpeed(p.x, W);
      const normalizedSpeed = speed / getSpeed(W, W);
      
      // Color by speed: blue (slow) -> red (fast)
      const r_c = Math.floor(50 + normalizedSpeed * 205);
      const b_c = Math.floor(255 - normalizedSpeed * 200);
      const g_c = Math.floor(80 + (1 - Math.abs(normalizedSpeed - 0.5) * 2) * 100);

      ctx.beginPath();
      ctx.arc(p.x, p.y, 4, 0, Math.PI * 2);
      ctx.fillStyle = `rgb(${r_c}, ${g_c}, ${b_c})`;
      ctx.fill();

      // Track the first particle that's in the middle area
      if (!tracked && p.x > 20 && p.x < W - 20) {
        tracked = { x: p.x, speed };
      }

      return true;
    });

    // Draw speed arrows at fixed positions
    const arrowPositions = [0.15, 0.35, 0.5, 0.65, 0.85];
    arrowPositions.forEach(pos => {
      const x = pos * W;
      const speed = getSpeed(x, W);
      const arrowLen = Math.min(speed * 15, 60);
      const y = centerY;
      
      ctx.beginPath();
      ctx.moveTo(x - arrowLen / 2, y);
      ctx.lineTo(x + arrowLen / 2, y);
      ctx.lineTo(x + arrowLen / 2 - 8, y - 5);
      ctx.moveTo(x + arrowLen / 2, y);
      ctx.lineTo(x + arrowLen / 2 - 8, y + 5);
      ctx.strokeStyle = `rgba(239, 68, 68, ${0.3 + speed * 0.08})`;
      ctx.lineWidth = 2;
      ctx.stroke();

      // Speed label
      ctx.fillStyle = '#ef4444';
      ctx.font = '11px sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText(`v=${speed.toFixed(1)}`, x, centerY - getPipeRadius(x, W) - 8);
    });

    // Labels
    ctx.fillStyle = '#334155';
    ctx.font = 'bold 13px sans-serif';
    ctx.textAlign = 'left';
    ctx.fillText('粗管 (慢)', 10, 20);
    ctx.textAlign = 'right';
    ctx.fillText('细管 (快)', W - 10, 20);

    if (tracked) {
      setTrackedParticle(tracked);
    }

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
    <div className="space-y-3">
      <div className="relative w-full h-52 bg-slate-900/5 rounded-xl overflow-hidden border border-slate-200">
        <canvas
          ref={canvasRef}
          className="w-full h-full"
        />
      </div>
      <div className="flex items-center gap-4">
        <button
          onClick={() => setIsRunning(!isRunning)}
          className="px-4 py-2 rounded-lg bg-blue-600 text-white font-medium hover:bg-blue-700 transition-colors text-sm"
        >
          {isRunning ? '⏸ 暂停' : '▶ 播放'}
        </button>
        <button
          onClick={() => {
            particlesRef.current = [];
            setTrackedParticle(null);
          }}
          className="px-4 py-2 rounded-lg bg-slate-200 text-slate-700 font-medium hover:bg-slate-300 transition-colors text-sm"
        >
          🔄 重置
        </button>
        {trackedParticle && (
          <span className="text-sm text-slate-600">
            位置: {trackedParticle.x.toFixed(0)}px | 速度: {trackedParticle.speed.toFixed(2)}
          </span>
        )}
      </div>
    </div>
  );
}
