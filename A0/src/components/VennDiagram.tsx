import { useState } from 'react';
import { motion } from 'framer-motion';

type Region = 'incompressible' | 'homogeneous' | 'both' | null;

export default function VennDiagram() {
  const [hovered, setHovered] = useState<Region>(null);

  const getInfo = (region: Region) => {
    switch (region) {
      case 'incompressible':
        return {
          title: '仅不可压缩',
          formula: 'Dρ/Dt = 0，但 ∇ρ ≠ 0',
          desc: '跟着质点走密度不变，但空间各处密度不同。比如分层的海水——上层淡水密度小，下层咸水密度大，但每团水自身密度不变。',
          color: 'border-emerald-500',
        };
      case 'homogeneous':
        return {
          title: '仅均质',
          formula: '∇ρ = 0，但 Dρ/Dt ≠ 0',
          desc: '任何时刻各处密度都一样，但整体密度随时间变化。比如一个密封容器中的气体被均匀加热——处处密度相同但都在减小。',
          color: 'border-purple-500',
        };
      case 'both':
        return {
          title: '均质 + 不可压缩',
          formula: 'ρ = 常数',
          desc: '各处密度相同，且不随时间变化。这是最简单的情况，密度就是一个常数！大多数水力学问题都属于这种情况。',
          color: 'border-blue-500',
        };
      default:
        return {
          title: '将鼠标移到圆上查看',
          formula: '',
          desc: '左边绿色圆代表"不可压缩"，右边紫色圆代表"均质"，中间交叉区域代表两者都满足。',
          color: 'border-slate-300',
        };
    }
  };

  const info = getInfo(hovered);

  return (
    <div className="space-y-4">
      <div className="flex justify-center py-4">
        <svg width="380" height="220" viewBox="0 0 380 220">
          {/* Incompressible circle */}
          <motion.circle
            cx="140"
            cy="110"
            r="90"
            fill={hovered === 'incompressible' || hovered === 'both' ? 'rgba(16, 185, 129, 0.25)' : 'rgba(16, 185, 129, 0.1)'}
            stroke="rgb(16, 185, 129)"
            strokeWidth="2.5"
            onMouseEnter={() => setHovered('incompressible')}
            onMouseLeave={() => setHovered(null)}
            style={{ cursor: 'pointer' }}
            whileHover={{ scale: 1.02 }}
          />
          {/* Homogeneous circle */}
          <motion.circle
            cx="240"
            cy="110"
            r="90"
            fill={hovered === 'homogeneous' || hovered === 'both' ? 'rgba(147, 51, 234, 0.25)' : 'rgba(147, 51, 234, 0.1)'}
            stroke="rgb(147, 51, 234)"
            strokeWidth="2.5"
            onMouseEnter={() => setHovered('homogeneous')}
            onMouseLeave={() => setHovered(null)}
            style={{ cursor: 'pointer' }}
            whileHover={{ scale: 1.02 }}
          />
          {/* Intersection area - invisible clickable rect */}
          <rect
            x="150"
            y="30"
            width="80"
            height="160"
            fill="transparent"
            onMouseEnter={() => setHovered('both')}
            onMouseLeave={() => setHovered(null)}
            style={{ cursor: 'pointer' }}
          />
          
          {/* Labels */}
          <text x="95" y="105" textAnchor="middle" className="fill-emerald-700 text-sm font-bold">不可压缩</text>
          <text x="95" y="125" textAnchor="middle" className="fill-emerald-600 text-xs">Dρ/Dt = 0</text>
          
          <text x="285" y="105" textAnchor="middle" className="fill-purple-700 text-sm font-bold">均质</text>
          <text x="285" y="125" textAnchor="middle" className="fill-purple-600 text-xs">∇ρ = 0</text>
          
          <text x="190" y="105" textAnchor="middle" className="fill-blue-700 text-xs font-bold">ρ = const</text>
          <text x="190" y="120" textAnchor="middle" className="fill-blue-600 text-xs">两者都满足</text>
        </svg>
      </div>

      <motion.div
        key={info.title}
        initial={{ opacity: 0, y: 5 }}
        animate={{ opacity: 1, y: 0 }}
        className={`p-4 rounded-xl bg-white border-2 ${info.color} transition-colors`}
      >
        <div className="font-bold text-slate-800 mb-1">{info.title}</div>
        {info.formula && <div className="font-mono text-sm text-slate-600 mb-2">{info.formula}</div>}
        <div className="text-sm text-slate-600">{info.desc}</div>
      </motion.div>
    </div>
  );
}
