import { useState, useEffect, useRef, useCallback } from 'react';
import MathTex from './Math';

export default function DivergenceExplainer() {
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

    if (isRunning) {
      timeRef.current += 0.015;
    }
    const t = timeRef.current;

    ctx.clearRect(0, 0, W, H);

    // Background
    ctx.fillStyle = '#fefce8';
    ctx.fillRect(0, 0, W, H);

    const cx = W / 2;
    const cy = H / 2;

    // Draw expanding cube demonstration
    const baseSize = 40;
    const expansion = 1 + 0.3 * Math.sin(t);
    
    // Calculate expansion in each direction
    const dx = baseSize * expansion;
    const dy = baseSize * (1 + 0.2 * Math.sin(t + 1));
    const dz = baseSize * (1 + 0.1 * Math.sin(t + 2));

    // Draw 2D representation of 3D cube (isometric-ish)
    const drawCube = (x: number, y: number, sx: number, sy: number, sz: number, alpha: number) => {
      ctx.globalAlpha = alpha;
      
      // Front face
      ctx.fillStyle = '#fbbf24';
      ctx.strokeStyle = '#d97706';
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.rect(x - sx, y - sy, sx * 2, sy * 2);
      ctx.fill();
      ctx.stroke();

      // Top face (parallelogram)
      ctx.fillStyle = '#fcd34d';
      ctx.beginPath();
      ctx.moveTo(x - sx, y - sy);
      ctx.lineTo(x - sx + sz * 0.5, y - sy - sz * 0.5);
      ctx.lineTo(x + sx + sz * 0.5, y - sy - sz * 0.5);
      ctx.lineTo(x + sx, y - sy);
      ctx.closePath();
      ctx.fill();
      ctx.stroke();

      // Right face (parallelogram)
      ctx.fillStyle = '#f59e0b';
      ctx.beginPath();
      ctx.moveTo(x + sx, y - sy);
      ctx.lineTo(x + sx + sz * 0.5, y - sy - sz * 0.5);
      ctx.lineTo(x + sx + sz * 0.5, y + sy - sz * 0.5);
      ctx.lineTo(x + sx, y + sy);
      ctx.closePath();
      ctx.fill();
      ctx.stroke();

      ctx.globalAlpha = 1;
    };

    // Draw original cube (ghost)
    drawCube(cx, cy, baseSize, baseSize, baseSize * 0.6, 0.3);
    
    // Draw expanding cube
    drawCube(cx, cy, dx, dy, dz * 0.6, 0.8);

    // Draw expansion arrows
    const drawExpansionArrow = (x1: number, y1: number, x2: number, y2: number, color: string, label: string) => {
      ctx.strokeStyle = color;
      ctx.fillStyle = color;
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.moveTo(x1, y1);
      ctx.lineTo(x2, y2);
      ctx.stroke();

      // Arrow head
      const angle = Math.atan2(y2 - y1, x2 - x1);
      ctx.beginPath();
      ctx.moveTo(x2, y2);
      ctx.lineTo(x2 - 8 * Math.cos(angle - 0.4), y2 - 8 * Math.sin(angle - 0.4));
      ctx.lineTo(x2 - 8 * Math.cos(angle + 0.4), y2 - 8 * Math.sin(angle + 0.4));
      ctx.closePath();
      ctx.fill();

      // Label
      ctx.font = 'bold 11px system-ui';
      ctx.textAlign = 'center';
      ctx.fillText(label, (x1 + x2) / 2 + (y2 > y1 ? 0 : 15), (y1 + y2) / 2 + (x2 > x1 ? 15 : 0));
    };

    // X direction expansion (∂u/∂x > 0 means stretching in x)
    if (expansion > 1) {
      drawExpansionArrow(cx + baseSize + 5, cy, cx + dx + 15, cy, '#ef4444', '∂u/∂x > 0');
      drawExpansionArrow(cx - baseSize - 5, cy, cx - dx - 15, cy, '#ef4444', '');
    }

    // Y direction
    const yExp = 1 + 0.2 * Math.sin(t + 1);
    if (yExp > 1) {
      drawExpansionArrow(cx, cy + baseSize + 5, cx, cy + dy + 10, '#22c55e', '∂v/∂y > 0');
    }

    // Labels
    ctx.fillStyle = '#1e293b';
    ctx.font = 'bold 13px system-ui';
    ctx.textAlign = 'center';
    ctx.fillText('微团在各方向被拉伸 → 体积膨胀', cx, 20);

    // Volume calculation
    const volume = (dx / baseSize) * (dy / baseSize) * (dz / baseSize);
    ctx.font = '12px system-ui';
    ctx.fillStyle = '#64748b';
    ctx.fillText(`相对体积: ${volume.toFixed(2)}`, cx, H - 10);

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
      <div className="p-4 rounded-xl bg-amber-50 border border-amber-200">
        <h3 className="font-bold text-amber-800 mb-3">🤔 为什么散度 = 体积膨胀率？</h3>
        <div className="text-sm text-amber-900 space-y-2">
          <p>想象一个微小的立方体流体微团，边长分别是 dx, dy, dz：</p>
          <ul className="list-disc list-inside space-y-1 ml-2">
            <li>
              如果 <MathTex tex="\frac{\partial u}{\partial x} > 0" />，
              说明右边的流体跑得比左边快 → 微团在 x 方向被<strong>拉长</strong>
            </li>
            <li>
              如果 <MathTex tex="\frac{\partial v}{\partial y} > 0" />，
              说明前边的流体跑得比后边快 → 微团在 y 方向被<strong>拉长</strong>
            </li>
            <li>
              如果 <MathTex tex="\frac{\partial w}{\partial z} > 0" />，
              说明上边的流体跑得比下边快 → 微团在 z 方向被<strong>拉长</strong>
            </li>
          </ul>
          <p className="mt-2">三个方向的拉伸加起来 = 总的体积膨胀率！</p>
        </div>
      </div>

      <div className="relative w-full h-48 rounded-xl overflow-hidden border border-slate-200">
        <canvas ref={canvasRef} className="w-full h-full" />
      </div>

      <div className="p-4 rounded-xl bg-white border-2 border-emerald-300">
        <div className="text-center mb-3">
          <MathTex 
            tex="\nabla \cdot \vec{V} = \frac{\partial u}{\partial x} + \frac{\partial v}{\partial y} + \frac{\partial w}{\partial z} = \frac{1}{V}\frac{dV}{dt}"
            display 
          />
        </div>
        <div className="grid grid-cols-3 gap-2 text-xs text-center">
          <div className="p-2 rounded bg-red-50 text-red-700">
            <MathTex tex="\frac{\partial u}{\partial x}" />
            <div className="mt-1">x方向拉伸率</div>
          </div>
          <div className="p-2 rounded bg-green-50 text-green-700">
            <MathTex tex="\frac{\partial v}{\partial y}" />
            <div className="mt-1">y方向拉伸率</div>
          </div>
          <div className="p-2 rounded bg-blue-50 text-blue-700">
            <MathTex tex="\frac{\partial w}{\partial z}" />
            <div className="mt-1">z方向拉伸率</div>
          </div>
        </div>
      </div>

      <div className="flex gap-2">
        <button
          onClick={() => setIsRunning(!isRunning)}
          className="px-4 py-2 rounded-lg bg-slate-200 text-slate-700 font-medium hover:bg-slate-300 transition-colors text-sm"
        >
          {isRunning ? '⏸ 暂停' : '▶ 播放'}
        </button>
        <button
          onClick={() => { timeRef.current = 0; }}
          className="px-4 py-2 rounded-lg bg-slate-200 text-slate-700 font-medium hover:bg-slate-300 transition-colors text-sm"
        >
          🔄 重置
        </button>
      </div>
    </div>
  );
}
