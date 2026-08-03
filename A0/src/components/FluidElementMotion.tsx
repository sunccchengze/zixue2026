import { useState, useEffect, useRef, useCallback } from 'react';

type MotionType = 'translation' | 'rotation' | 'linear' | 'shear' | 'combined';

const motionLabels: Record<MotionType, { name: string; desc: string; emoji: string; color: string }> = {
  translation: { name: '平动', desc: '整体移动，形状不变', emoji: '➡️', color: '#3b82f6' },
  rotation: { name: '旋转', desc: '像车轮一样转圈', emoji: '🔄', color: '#8b5cf6' },
  linear: { name: '线变形', desc: '被拉长或压扁', emoji: '↔️', color: '#10b981' },
  shear: { name: '角变形', desc: '正方形变成平行四边形', emoji: '◇', color: '#f59e0b' },
  combined: { name: '组合运动', desc: '四种动作同时发生', emoji: '🌊', color: '#ef4444' },
};

export default function FluidElementMotion() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const animRef = useRef<number>(0);
  const [motionType, setMotionType] = useState<MotionType>('translation');
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
      timeRef.current += 0.025;
    }
    const t = timeRef.current;

    ctx.clearRect(0, 0, W, H);

    // Draw grid background
    ctx.strokeStyle = '#e2e8f0';
    ctx.lineWidth = 1;
    const gridSize = 30;
    for (let x = 0; x < W; x += gridSize) {
      ctx.beginPath();
      ctx.moveTo(x, 0);
      ctx.lineTo(x, H);
      ctx.stroke();
    }
    for (let y = 0; y < H; y += gridSize) {
      ctx.beginPath();
      ctx.moveTo(0, y);
      ctx.lineTo(W, y);
      ctx.stroke();
    }

    // Define original square corners (relative to center)
    const size = 50;
    let corners = [
      { x: -size, y: -size },
      { x: size, y: -size },
      { x: size, y: size },
      { x: -size, y: size },
    ];

    // Center position
    let centerX = cx;
    let centerY = cy;

    // Apply transformations based on motion type
    switch (motionType) {
      case 'translation': {
        // Simple translation - move in a figure-8 pattern
        centerX = cx + Math.sin(t) * 80;
        centerY = cy + Math.sin(t * 2) * 40;
        break;
      }
      case 'rotation': {
        // Pure rotation
        const angle = t;
        corners = corners.map(c => ({
          x: c.x * Math.cos(angle) - c.y * Math.sin(angle),
          y: c.x * Math.sin(angle) + c.y * Math.cos(angle),
        }));
        break;
      }
      case 'linear': {
        // Linear deformation (stretch and compress)
        const scaleX = 1 + 0.4 * Math.sin(t);
        const scaleY = 1 - 0.3 * Math.sin(t); // Compress in y when stretch in x
        corners = corners.map(c => ({
          x: c.x * scaleX,
          y: c.y * scaleY,
        }));
        break;
      }
      case 'shear': {
        // Shear deformation (angular deformation)
        const shear = Math.sin(t) * 0.5;
        corners = corners.map(c => ({
          x: c.x + c.y * shear,
          y: c.y,
        }));
        break;
      }
      case 'combined': {
        // All combined
        centerX = cx + Math.sin(t * 0.5) * 60;
        centerY = cy + Math.cos(t * 0.7) * 30;
        const angle = t * 0.3;
        const scaleX = 1 + 0.2 * Math.sin(t * 1.5);
        const scaleY = 1 - 0.15 * Math.sin(t * 1.5);
        const shear = Math.sin(t * 0.8) * 0.2;
        corners = corners.map(c => {
          // Apply shear
          let x = c.x + c.y * shear;
          let y = c.y;
          // Apply scale
          x *= scaleX;
          y *= scaleY;
          // Apply rotation
          const rx = x * Math.cos(angle) - y * Math.sin(angle);
          const ry = x * Math.sin(angle) + y * Math.cos(angle);
          return { x: rx, y: ry };
        });
        break;
      }
    }

    // Draw the deformed shape
    ctx.beginPath();
    ctx.moveTo(centerX + corners[0].x, centerY + corners[0].y);
    for (let i = 1; i < corners.length; i++) {
      ctx.lineTo(centerX + corners[i].x, centerY + corners[i].y);
    }
    ctx.closePath();
    ctx.fillStyle = `${motionLabels[motionType].color}30`;
    ctx.fill();
    ctx.strokeStyle = motionLabels[motionType].color;
    ctx.lineWidth = 3;
    ctx.stroke();

    // Draw corner dots
    corners.forEach((c, i) => {
      ctx.beginPath();
      ctx.arc(centerX + c.x, centerY + c.y, 6, 0, Math.PI * 2);
      ctx.fillStyle = i === 0 ? '#ef4444' : motionLabels[motionType].color;
      ctx.fill();
    });

    // Draw center point
    ctx.beginPath();
    ctx.arc(centerX, centerY, 4, 0, Math.PI * 2);
    ctx.fillStyle = '#1e293b';
    ctx.fill();

    // Draw reference square (ghost)
    ctx.strokeStyle = '#cbd5e1';
    ctx.lineWidth = 1;
    ctx.setLineDash([5, 5]);
    ctx.strokeRect(cx - size, cy - size, size * 2, size * 2);
    ctx.setLineDash([]);

    // Draw motion indicators
    if (motionType === 'rotation') {
      // Draw rotation arrow
      ctx.beginPath();
      ctx.arc(centerX, centerY, 70, -0.5, 1);
      ctx.strokeStyle = '#8b5cf6';
      ctx.lineWidth = 2;
      ctx.stroke();
      // Arrow head
      const endX = centerX + 70 * Math.cos(1);
      const endY = centerY + 70 * Math.sin(1);
      ctx.beginPath();
      ctx.moveTo(endX, endY);
      ctx.lineTo(endX - 10, endY - 8);
      ctx.moveTo(endX, endY);
      ctx.lineTo(endX + 5, endY - 10);
      ctx.stroke();
    }

    if (motionType === 'linear') {
      // Draw stretch arrows
      const scaleX = 1 + 0.4 * Math.sin(t);
      ctx.strokeStyle = '#10b981';
      ctx.lineWidth = 2;
      // Horizontal arrows
      const arrowX = size * scaleX + 15;
      ctx.beginPath();
      ctx.moveTo(centerX - arrowX, centerY);
      ctx.lineTo(centerX - arrowX - 15, centerY);
      ctx.moveTo(centerX + arrowX, centerY);
      ctx.lineTo(centerX + arrowX + 15, centerY);
      ctx.stroke();
    }

    // Label
    ctx.fillStyle = '#1e293b';
    ctx.font = 'bold 14px system-ui';
    ctx.textAlign = 'center';
    ctx.fillText(`${motionLabels[motionType].emoji} ${motionLabels[motionType].name}`, cx, 25);
    ctx.font = '12px system-ui';
    ctx.fillStyle = '#64748b';
    ctx.fillText(motionLabels[motionType].desc, cx, 45);

    animRef.current = requestAnimationFrame(draw);
  }, [motionType, isRunning]);

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
      <div className="relative w-full h-64 bg-white rounded-xl overflow-hidden border border-slate-200 shadow-inner">
        <canvas ref={canvasRef} className="w-full h-full" />
      </div>
      <div className="flex flex-wrap gap-2">
        {(Object.keys(motionLabels) as MotionType[]).map(type => (
          <button
            key={type}
            onClick={() => {
              setMotionType(type);
              timeRef.current = 0;
            }}
            className={`px-3 py-2 rounded-lg text-sm font-medium transition-all ${
              motionType === type
                ? 'text-white shadow-md'
                : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
            }`}
            style={{
              backgroundColor: motionType === type ? motionLabels[type].color : undefined,
            }}
          >
            {motionLabels[type].emoji} {motionLabels[type].name}
          </button>
        ))}
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
