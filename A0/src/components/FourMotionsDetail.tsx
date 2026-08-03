import { useState } from 'react';
import { motion } from 'framer-motion';
import MathTex from './Math';

type MotionType = 'translation' | 'rotation' | 'linear' | 'angular';

const details: Record<MotionType, {
  name: string;
  emoji: string;
  color: string;
  description: string;
  changesVolume: boolean;
  changesShape: boolean;
  mathDesc: string;
  example: string;
}> = {
  translation: {
    name: '平动',
    emoji: '➡️',
    color: 'blue',
    description: '整个微团一起往某个方向移动，每个点的速度都一样。就像一块砖头被推着走。',
    changesVolume: false,
    changesShape: false,
    mathDesc: '所有点速度相同：\\vec{V} = \\text{const}',
    example: '匀速直流的河水',
  },
  rotation: {
    name: '旋转',
    emoji: '🔄',
    color: 'purple',
    description: '微团像一个车轮一样绕某个轴旋转。注意是"自转"，不是绕着外面某个点公转。',
    changesVolume: false,
    changesShape: false,
    mathDesc: '角速度 \\omega = \\frac{1}{2}\\nabla \\times \\vec{V}',
    example: '搅拌咖啡时，咖啡跟着勺子一起转',
  },
  linear: {
    name: '线变形（伸缩）',
    emoji: '↔️',
    color: 'emerald',
    description: '微团在某个方向被拉长或压短。如果三个方向的拉伸不相互抵消，体积就会变化！',
    changesVolume: true,
    changesShape: true,
    mathDesc: '体积膨胀率 = \\nabla \\cdot \\vec{V}',
    example: '气球被吹大、海绵被压缩',
  },
  angular: {
    name: '角变形（剪切）',
    emoji: '◇',
    color: 'amber',
    description: '正方形被扭成平行四边形。直角变成非直角，但面积/体积不变！',
    changesVolume: false,
    changesShape: true,
    mathDesc: '剪切应变率 = \\frac{1}{2}\\left(\\frac{\\partial u}{\\partial y} + \\frac{\\partial v}{\\partial x}\\right)',
    example: '抹黄油时，刀把黄油一层层错开',
  },
};

export default function FourMotionsDetail() {
  const [selected, setSelected] = useState<MotionType>('translation');
  const detail = details[selected];

  const getColorClasses = (color: string) => ({
    bg: color === 'blue' ? 'bg-blue-50' :
        color === 'purple' ? 'bg-purple-50' :
        color === 'emerald' ? 'bg-emerald-50' : 'bg-amber-50',
    border: color === 'blue' ? 'border-blue-300' :
            color === 'purple' ? 'border-purple-300' :
            color === 'emerald' ? 'border-emerald-300' : 'border-amber-300',
    text: color === 'blue' ? 'text-blue-800' :
          color === 'purple' ? 'text-purple-800' :
          color === 'emerald' ? 'text-emerald-800' : 'text-amber-800',
    btn: color === 'blue' ? 'bg-blue-600' :
         color === 'purple' ? 'bg-purple-600' :
         color === 'emerald' ? 'bg-emerald-600' : 'bg-amber-500',
  });

  const colors = getColorClasses(detail.color);

  return (
    <div className="space-y-4">
      {/* Selection buttons */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
        {(Object.keys(details) as MotionType[]).map(type => {
          const d = details[type];
          const c = getColorClasses(d.color);
          return (
            <button
              key={type}
              onClick={() => setSelected(type)}
              className={`p-3 rounded-xl text-sm font-medium transition-all border-2 ${
                selected === type
                  ? `${c.btn} text-white border-transparent`
                  : `${c.bg} ${c.text} ${c.border} hover:opacity-80`
              }`}
            >
              <div className="text-xl mb-1">{d.emoji}</div>
              <div>{d.name}</div>
            </button>
          );
        })}
      </div>

      {/* Detail card */}
      <motion.div
        key={selected}
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        className={`p-5 rounded-xl ${colors.bg} border-2 ${colors.border}`}
      >
        <h3 className={`text-lg font-bold ${colors.text} mb-3`}>
          {detail.emoji} {detail.name}
        </h3>
        
        <p className={`${colors.text} mb-4`}>{detail.description}</p>

        <div className="grid grid-cols-2 gap-3 mb-4">
          <div className={`p-3 rounded-lg bg-white/70 text-center ${
            detail.changesVolume ? 'ring-2 ring-red-400' : ''
          }`}>
            <div className="text-2xl mb-1">{detail.changesVolume ? '📐' : '📦'}</div>
            <div className="text-sm font-bold">体积</div>
            <div className={`text-xs ${detail.changesVolume ? 'text-red-600 font-bold' : 'text-slate-500'}`}>
              {detail.changesVolume ? '会改变！' : '不变'}
            </div>
          </div>
          <div className={`p-3 rounded-lg bg-white/70 text-center ${
            detail.changesShape ? 'ring-2 ring-amber-400' : ''
          }`}>
            <div className="text-2xl mb-1">{detail.changesShape ? '🔷' : '⬜'}</div>
            <div className="text-sm font-bold">形状</div>
            <div className={`text-xs ${detail.changesShape ? 'text-amber-600 font-bold' : 'text-slate-500'}`}>
              {detail.changesShape ? '会改变！' : '不变'}
            </div>
          </div>
        </div>

        <div className="p-3 rounded-lg bg-white/70 mb-3">
          <div className="text-xs text-slate-500 mb-1">数学描述</div>
          <MathTex tex={detail.mathDesc} />
        </div>

        <div className="p-3 rounded-lg bg-white/70">
          <div className="text-xs text-slate-500 mb-1">生活例子</div>
          <div className={`text-sm ${colors.text}`}>💡 {detail.example}</div>
        </div>
      </motion.div>

      {/* Key insight */}
      <div className="p-4 rounded-xl bg-slate-800 text-white">
        <div className="font-bold mb-2">🎯 关键理解</div>
        <div className="text-sm space-y-2">
          <p>• <strong>只有线变形</strong>会改变体积 → 所以不可压缩流体的散度必须为0</p>
          <p>• 刚体（石头）只能平动+旋转，不能变形</p>
          <p>• 流体是软的，四种运动可以同时发生</p>
        </div>
      </div>
    </div>
  );
}
