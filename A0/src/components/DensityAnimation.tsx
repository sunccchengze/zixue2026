import { useEffect, useRef, useState, useCallback } from 'react';

type Mode = 'incompressible' | 'homogeneous' | 'both';

export default function DensityAnimation() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const animRef = useRef<number>(0);
  const [mode, setMode] = useState<Mode>('incompressible');
  const [isRunning, setIsRunning] = useState(true);
  const timeRef = useRef(0);

  const draw = useCallback((_timestamp: number) => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const W = canvas.width;
    const H = canvas.height;

    if (isRunning) {
      timeRef.current += 0.016;
    }
    const t = timeRef.current;

    ctx.clearRect(0, 0, W, H);

    const numCols = 8;
    const numRows = 4;
    const cellW = W / numCols;
    const cellH = (H - 40) / numRows;
    const offsetY = 20;

    // Draw grid and density
    for (let i = 0; i < numCols; i++) {
      for (let j = 0; j < numRows; j++) {
        const x = i * cellW;
        const y = j * cellH + offsetY;
        const normalizedX = i / (numCols - 1);
        const normalizedY = j / (numRows - 1);

        let density = 1.0;

        if (mode === 'incompressible') {
          // Density varies in space but each particle keeps its density
          // ∇ρ ≠ 0, but Dρ/Dt = 0
          density = 0.4 + 0.6 * normalizedX + 0.15 * Math.sin(normalizedY * Math.PI);
        } else if (mode === 'homogeneous') {
          // Density same everywhere but changes with time
          // ∇ρ = 0, but ∂ρ/∂t ≠ 0, so Dρ/Dt ≠ 0
          density = 0.5 + 0.4 * Math.sin(t * 0.8);
        } else {
          // Both: ∇ρ = 0 and Dρ/Dt = 0 → ρ = const
          density = 0.7;
        }

        // Color: lighter = less dense, darker = more dense
        const blue = Math.floor(100 + (1 - density) * 155);
        const green = Math.floor(150 + (1 - density) * 105);
        const red = Math.floor(30 + (1 - density) * 60);

        ctx.fillStyle = `rgb(${red}, ${green}, ${blue})`;
        ctx.fillRect(x + 1, y + 1, cellW - 2, cellH - 2);

        // Draw density value
        ctx.fillStyle = density > 0.6 ? '#fff' : '#1e293b';
        ctx.font = 'bold 11px monospace';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(`ρ=${density.toFixed(2)}`, x + cellW / 2, y + cellH / 2);
      }
    }

    // Draw a tracked "fluid parcel" moving through
    if (mode === 'incompressible') {
      const parcelX = ((t * 0.3) % 1.2 - 0.1) * W;
      const parcelY = H / 2;
      const normalizedPX = Math.max(0, Math.min(1, parcelX / W));
      const parcelDensity = 0.4 + 0.6 * normalizedPX;

      // Highlight the parcel
      ctx.strokeStyle = '#f59e0b';
      ctx.lineWidth = 3;
      ctx.strokeRect(parcelX - 18, parcelY - 18, 36, 36);

      ctx.fillStyle = '#f59e0b';
      ctx.font = 'bold 12px sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText(`跟踪质点: ρ=${parcelDensity.toFixed(2)}`, parcelX, parcelY - 28);
      
      // Arrow showing direction
      ctx.beginPath();
      ctx.moveTo(parcelX + 22, parcelY);
      ctx.lineTo(parcelX + 35, parcelY);
      ctx.lineTo(parcelX + 30, parcelY - 4);
      ctx.moveTo(parcelX + 35, parcelY);
      ctx.lineTo(parcelX + 30, parcelY + 4);
      ctx.strokeStyle = '#f59e0b';
      ctx.lineWidth = 2;
      ctx.stroke();
    }

    // Title
    ctx.fillStyle = '#1e293b';
    ctx.font = 'bold 13px sans-serif';
    ctx.textAlign = 'center';
    if (mode === 'incompressible') {
      ctx.fillText('不可压缩: Dρ/Dt = 0 (跟着质点走密度不变) 但 ∇ρ ≠ 0 (各处密度不同)', W / 2, 14);
    } else if (mode === 'homogeneous') {
      ctx.fillText('均质: ∇ρ = 0 (各处密度相同) 但密度随时间变 → Dρ/Dt ≠ 0', W / 2, 14);
    } else {
      ctx.fillText('均质 + 不可压缩: ∇ρ = 0 且 Dρ/Dt = 0 → ρ = 常数', W / 2, 14);
    }

    animRef.current = requestAnimationFrame(draw);
  }, [isRunning, mode]);

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
      <div className="relative w-full h-48 bg-slate-900/5 rounded-xl overflow-hidden border border-slate-200">
        <canvas ref={canvasRef} className="w-full h-full" />
      </div>
      <div className="flex flex-wrap items-center gap-2">
        <button
          onClick={() => setMode('incompressible')}
          className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${
            mode === 'incompressible'
              ? 'bg-emerald-600 text-white'
              : 'bg-slate-200 text-slate-700 hover:bg-slate-300'
          }`}
        >
          不可压缩 (Dρ/Dt=0)
        </button>
        <button
          onClick={() => setMode('homogeneous')}
          className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${
            mode === 'homogeneous'
              ? 'bg-purple-600 text-white'
              : 'bg-slate-200 text-slate-700 hover:bg-slate-300'
          }`}
        >
          均质 (∇ρ=0)
        </button>
        <button
          onClick={() => setMode('both')}
          className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${
            mode === 'both'
              ? 'bg-blue-600 text-white'
              : 'bg-slate-200 text-slate-700 hover:bg-slate-300'
          }`}
        >
          均质+不可压缩
        </button>
        <button
          onClick={() => setIsRunning(!isRunning)}
          className="ml-auto px-3 py-1.5 rounded-lg bg-slate-200 text-slate-700 font-medium hover:bg-slate-300 transition-colors text-sm"
        >
          {isRunning ? '⏸ 暂停' : '▶ 播放'}
        </button>
      </div>
    </div>
  );
}
