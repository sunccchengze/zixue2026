import { useState, useEffect, useRef, useCallback } from 'react';
import MathTex from './Math';

export default function CurlExplainer() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const animRef = useRef<number>(0);
  const [mode, setMode] = useState<'shear' | 'freeVortex' | 'rigid'>('shear');
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
      timeRef.current += 0.02;
    }
    const t = timeRef.current;

    ctx.clearRect(0, 0, W, H);
    
    const cx = W / 2;
    const cy = H / 2;

    // Background
    ctx.fillStyle = mode === 'freeVortex' ? '#f0fdf4' : mode === 'rigid' ? '#fef3c7' : '#ede9fe';
    ctx.fillRect(0, 0, W, H);

    if (mode === 'shear') {
      // Shear flow: u = y, v = 0
      // Draw velocity arrows showing shear
      for (let y = 30; y < H - 20; y += 35) {
        const u = (y - cy) * 0.03; // velocity proportional to y
        const arrowLen = Math.abs(u) * 40 + 10;
        const dir = u > 0 ? 1 : -1;
        
        for (let x = 50; x < W - 50; x += 60) {
          ctx.strokeStyle = '#8b5cf6';
          ctx.lineWidth = 2;
          ctx.beginPath();
          ctx.moveTo(x, y);
          ctx.lineTo(x + dir * arrowLen, y);
          ctx.stroke();
          
          // Arrow head
          ctx.beginPath();
          ctx.moveTo(x + dir * arrowLen, y);
          ctx.lineTo(x + dir * arrowLen - dir * 6, y - 4);
          ctx.lineTo(x + dir * arrowLen - dir * 6, y + 4);
          ctx.closePath();
          ctx.fillStyle = '#8b5cf6';
          ctx.fill();
        }
      }

      // Draw a fluid element being rotated by shear
      const elemX = cx;
      const elemY = cy;
      const size = 30;
      
      // The element rotates due to velocity difference between top and bottom
      const rotation = t * 0.3;
      
      ctx.save();
      ctx.translate(elemX, elemY);
      ctx.rotate(rotation);
      
      ctx.fillStyle = '#c4b5fd';
      ctx.strokeStyle = '#7c3aed';
      ctx.lineWidth = 3;
      ctx.fillRect(-size, -size, size * 2, size * 2);
      ctx.strokeRect(-size, -size, size * 2, size * 2);
      
      // Corner markers
      ctx.fillStyle = '#ef4444';
      ctx.beginPath();
      ctx.arc(-size, -size, 5, 0, Math.PI * 2);
      ctx.fill();
      
      ctx.restore();

      // Show velocity difference explanation
      ctx.fillStyle = '#1e293b';
      ctx.font = '11px system-ui';
      ctx.textAlign = 'left';
      ctx.fillText('上面速度大 →', elemX + 40, elemY - 30);
      ctx.fillText('下面速度小 →', elemX + 40, elemY + 35);
      ctx.fillText('→ 微团被扭转！', elemX + 40, elemY + 55);

    } else if (mode === 'rigid') {
      // Rigid body rotation: everything rotates together
      // Draw circular arrows
      for (let r = 40; r < Math.min(W, H) / 2 - 20; r += 40) {
        const numArrows = Math.floor(r / 15);
        for (let i = 0; i < numArrows; i++) {
          const angle = (i / numArrows) * Math.PI * 2 + t * 0.5;
          const x = cx + r * Math.cos(angle);
          const y = cy + r * Math.sin(angle);
          
          // Tangent direction
          const tx = -Math.sin(angle);
          const ty = Math.cos(angle);
          const len = 15;
          
          ctx.strokeStyle = '#f59e0b';
          ctx.lineWidth = 2;
          ctx.beginPath();
          ctx.moveTo(x, y);
          ctx.lineTo(x + tx * len, y + ty * len);
          ctx.stroke();
          
          // Arrow head
          const endX = x + tx * len;
          const endY = y + ty * len;
          const headAngle = Math.atan2(ty, tx);
          ctx.beginPath();
          ctx.moveTo(endX, endY);
          ctx.lineTo(endX - 5 * Math.cos(headAngle - 0.5), endY - 5 * Math.sin(headAngle - 0.5));
          ctx.lineTo(endX - 5 * Math.cos(headAngle + 0.5), endY - 5 * Math.sin(headAngle + 0.5));
          ctx.closePath();
          ctx.fillStyle = '#f59e0b';
          ctx.fill();
        }
      }

      // Draw rotating fluid element
      const elemAngle = t * 0.5;
      const elemR = 60;
      const elemX = cx + elemR * Math.cos(elemAngle * 0.3);
      const elemY = cy + elemR * Math.sin(elemAngle * 0.3);
      const size = 20;
      
      ctx.save();
      ctx.translate(elemX, elemY);
      ctx.rotate(elemAngle); // Element also rotates!
      
      ctx.fillStyle = '#fde68a';
      ctx.strokeStyle = '#d97706';
      ctx.lineWidth = 3;
      ctx.fillRect(-size, -size, size * 2, size * 2);
      ctx.strokeRect(-size, -size, size * 2, size * 2);
      
      ctx.fillStyle = '#ef4444';
      ctx.beginPath();
      ctx.arc(-size, -size, 5, 0, Math.PI * 2);
      ctx.fill();
      
      ctx.restore();

      // Center point
      ctx.fillStyle = '#1e293b';
      ctx.beginPath();
      ctx.arc(cx, cy, 5, 0, Math.PI * 2);
      ctx.fill();

    } else {
      // Free vortex: v_θ = C/r (irrotational!)
      // Draw velocity arrows - faster near center
      for (let angle = 0; angle < Math.PI * 2; angle += 0.4) {
        for (let r = 35; r < Math.min(W, H) / 2 - 20; r += 35) {
          const x = cx + r * Math.cos(angle);
          const y = cy + r * Math.sin(angle);
          
          // Tangent direction, speed inversely proportional to r
          const tx = -Math.sin(angle);
          const ty = Math.cos(angle);
          const speed = 800 / r; // v = C/r
          const len = Math.min(speed, 25);
          
          ctx.strokeStyle = '#22c55e';
          ctx.lineWidth = 2;
          ctx.beginPath();
          ctx.moveTo(x, y);
          ctx.lineTo(x + tx * len, y + ty * len);
          ctx.stroke();
          
          const endX = x + tx * len;
          const endY = y + ty * len;
          const headAngle = Math.atan2(ty, tx);
          ctx.beginPath();
          ctx.moveTo(endX, endY);
          ctx.lineTo(endX - 5 * Math.cos(headAngle - 0.5), endY - 5 * Math.sin(headAngle - 0.5));
          ctx.lineTo(endX - 5 * Math.cos(headAngle + 0.5), endY - 5 * Math.sin(headAngle + 0.5));
          ctx.closePath();
          ctx.fillStyle = '#22c55e';
          ctx.fill();
        }
      }

      // Draw fluid element that orbits but doesn't rotate itself
      const orbitAngle = t * 0.4;
      const orbitR = 70;
      const elemX = cx + orbitR * Math.cos(orbitAngle);
      const elemY = cy + orbitR * Math.sin(orbitAngle);
      const size = 18;
      
      ctx.save();
      ctx.translate(elemX, elemY);
      // NO rotation! That's the key - element doesn't spin
      
      ctx.fillStyle = '#bbf7d0';
      ctx.strokeStyle = '#16a34a';
      ctx.lineWidth = 3;
      ctx.fillRect(-size, -size, size * 2, size * 2);
      ctx.strokeRect(-size, -size, size * 2, size * 2);
      
      ctx.fillStyle = '#ef4444';
      ctx.beginPath();
      ctx.arc(-size, -size, 5, 0, Math.PI * 2);
      ctx.fill();
      
      ctx.restore();

      // Center point (vortex core)
      ctx.fillStyle = '#1e293b';
      ctx.beginPath();
      ctx.arc(cx, cy, 5, 0, Math.PI * 2);
      ctx.fill();
    }

    // Title
    ctx.fillStyle = '#1e293b';
    ctx.font = 'bold 13px system-ui';
    ctx.textAlign = 'center';
    
    if (mode === 'shear') {
      ctx.fillText('剪切流：上下速度不同 → 微团被扭转 → 有旋！', cx, 18);
    } else if (mode === 'rigid') {
      ctx.fillText('刚体旋转：微团绕中心转，自己也在转 → 有旋！', cx, 18);
    } else {
      ctx.fillText('自由涡：微团绕中心转，但自己不转！→ 无旋！', cx, 18);
    }

    animRef.current = requestAnimationFrame(draw);
  }, [mode, isRunning]);

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
      <div className="p-4 rounded-xl bg-purple-50 border border-purple-200">
        <h3 className="font-bold text-purple-800 mb-3">🤔 微团为什么会自转？</h3>
        <div className="text-sm text-purple-900 space-y-2">
          <p>关键在于：微团的<strong>上下两边</strong>或<strong>左右两边</strong>受到的速度不一样！</p>
          <div className="p-3 rounded bg-white border border-purple-200 mt-2">
            <p className="mb-2">比如剪切流 u = ky（速度只有x分量，且随y增大）：</p>
            <ul className="list-disc list-inside space-y-1 text-xs">
              <li>微团上边的流体速度比下边大</li>
              <li>上边被往右拽，下边被往右拽得慢</li>
              <li>结果：微团被<strong>扭转</strong>了！→ 这就是旋转的来源</li>
            </ul>
          </div>
        </div>
      </div>

      <div className="relative w-full h-56 rounded-xl overflow-hidden border border-slate-200">
        <canvas ref={canvasRef} className="w-full h-full" />
      </div>

      <div className="text-xs text-slate-500 text-center">
        🔴 红点标记微团的一个角，观察它是否在旋转
      </div>

      <div className="flex flex-wrap gap-2">
        <button
          onClick={() => { setMode('shear'); timeRef.current = 0; }}
          className={`px-3 py-2 rounded-lg text-sm font-medium transition-all ${
            mode === 'shear' ? 'bg-purple-600 text-white' : 'bg-slate-100 hover:bg-slate-200'
          }`}
        >
          📐 剪切流 (有旋)
        </button>
        <button
          onClick={() => { setMode('rigid'); timeRef.current = 0; }}
          className={`px-3 py-2 rounded-lg text-sm font-medium transition-all ${
            mode === 'rigid' ? 'bg-amber-500 text-white' : 'bg-slate-100 hover:bg-slate-200'
          }`}
        >
          🔄 刚体旋转 (有旋)
        </button>
        <button
          onClick={() => { setMode('freeVortex'); timeRef.current = 0; }}
          className={`px-3 py-2 rounded-lg text-sm font-medium transition-all ${
            mode === 'freeVortex' ? 'bg-emerald-500 text-white' : 'bg-slate-100 hover:bg-slate-200'
          }`}
        >
          🌀 自由涡 (无旋!)
        </button>
        <button
          onClick={() => setIsRunning(!isRunning)}
          className="ml-auto px-3 py-2 rounded-lg bg-slate-200 text-slate-700 font-medium hover:bg-slate-300 transition-colors text-sm"
        >
          {isRunning ? '⏸ 暂停' : '▶ 播放'}
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="p-4 rounded-xl bg-amber-50 border border-amber-200">
          <div className="font-bold text-amber-800 mb-2">有旋流动</div>
          <div className="text-sm text-amber-700">
            <MathTex tex="\nabla \times \vec{V} \neq 0" />
            <p className="mt-2 text-xs">微团自身在旋转（像陀螺）</p>
            <p className="text-xs">例：剪切流、刚体旋转</p>
          </div>
        </div>
        <div className="p-4 rounded-xl bg-emerald-50 border border-emerald-200">
          <div className="font-bold text-emerald-800 mb-2">无旋流动（势流）</div>
          <div className="text-sm text-emerald-700">
            <MathTex tex="\nabla \times \vec{V} = 0" />
            <p className="mt-2 text-xs">微团绕某中心公转，但自己不自转</p>
            <p className="text-xs">例：自由涡（下水道漩涡）</p>
          </div>
        </div>
      </div>
    </div>
  );
}
