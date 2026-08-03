import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import MathTex from './Math';

export default function AccelerationDecomposition() {
  const [localRate, setLocalRate] = useState(0);
  const [convectiveRate, setConvectiveRate] = useState(3);

  const totalAccel = localRate + convectiveRate;

  const getBarColor = (val: number) => {
    if (val > 0) return 'bg-red-500';
    if (val < 0) return 'bg-blue-500';
    return 'bg-slate-300';
  };

  const getDescription = () => {
    if (localRate === 0 && convectiveRate !== 0) {
      return {
        text: '定常流动！速度场不随时间变化，但质点移动到不同位置时速度不同，所以仍有加速度。',
        emoji: '🎯',
        color: 'text-amber-600',
      };
    }
    if (localRate !== 0 && convectiveRate === 0) {
      return {
        text: '非定常、均匀流动！各处速度相同但随时间变化。位变导数为零但当地导数不为零。',
        emoji: '⏰',
        color: 'text-purple-600',
      };
    }
    if (localRate === 0 && convectiveRate === 0) {
      return {
        text: '定常且均匀——没有加速度！质点既不因时间也不因位置变化而改变速度。',
        emoji: '😴',
        color: 'text-green-600',
      };
    }
    return {
      text: '既有当地加速度又有位变加速度。速度既随时间变也随位置变。',
      emoji: '🌊',
      color: 'text-blue-600',
    };
  };

  const desc = getDescription();

  return (
    <div className="space-y-5">
      {/* Sliders */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="space-y-2">
          <label className="flex items-center justify-between text-sm font-medium text-slate-700">
            <span>当地加速度 <MathTex tex="\\frac{\\partial \\vec{V}}{\\partial t}" /></span>
            <span className="font-mono text-lg">{localRate.toFixed(1)}</span>
          </label>
          <input
            type="range"
            min="-5"
            max="5"
            step="0.5"
            value={localRate}
            onChange={e => setLocalRate(Number(e.target.value))}
            className="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-purple-600"
          />
          <p className="text-xs text-slate-500">固定位置上，速度随时间的变化率</p>
        </div>
        <div className="space-y-2">
          <label className="flex items-center justify-between text-sm font-medium text-slate-700">
            <span>位变加速度 <MathTex tex="\\vec{V} \\cdot \\nabla \\vec{V}" /></span>
            <span className="font-mono text-lg">{convectiveRate.toFixed(1)}</span>
          </label>
          <input
            type="range"
            min="-5"
            max="5"
            step="0.5"
            value={convectiveRate}
            onChange={e => setConvectiveRate(Number(e.target.value))}
            className="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-amber-600"
          />
          <p className="text-xs text-slate-500">因为移动到不同位置带来的速度变化</p>
        </div>
      </div>

      {/* Visual bar chart */}
      <div className="bg-slate-50 rounded-xl p-4 space-y-3">
        <div className="space-y-2">
          {/* Local */}
          <div className="flex items-center gap-3">
            <span className="text-xs text-slate-500 w-16 text-right shrink-0">∂V/∂t</span>
            <div className="flex-1 h-6 bg-slate-200 rounded-full relative overflow-hidden">
              <motion.div
                className={`absolute top-0 h-full rounded-full ${getBarColor(localRate)}`}
                style={{
                  left: localRate >= 0 ? '50%' : undefined,
                  right: localRate < 0 ? '50%' : undefined,
                }}
                animate={{ width: `${Math.abs(localRate) * 10}%` }}
                transition={{ type: 'spring', stiffness: 300, damping: 30 }}
              />
              <div className="absolute left-1/2 top-0 bottom-0 w-px bg-slate-400" />
            </div>
          </div>
          {/* Convective */}
          <div className="flex items-center gap-3">
            <span className="text-xs text-slate-500 w-16 text-right shrink-0">V·∇V</span>
            <div className="flex-1 h-6 bg-slate-200 rounded-full relative overflow-hidden">
              <motion.div
                className={`absolute top-0 h-full rounded-full ${getBarColor(convectiveRate)}`}
                style={{
                  left: convectiveRate >= 0 ? '50%' : undefined,
                  right: convectiveRate < 0 ? '50%' : undefined,
                }}
                animate={{ width: `${Math.abs(convectiveRate) * 10}%` }}
                transition={{ type: 'spring', stiffness: 300, damping: 30 }}
              />
              <div className="absolute left-1/2 top-0 bottom-0 w-px bg-slate-400" />
            </div>
          </div>
          {/* Total */}
          <div className="flex items-center gap-3">
            <span className="text-xs font-bold text-slate-700 w-16 text-right shrink-0">DV/Dt</span>
            <div className="flex-1 h-8 bg-slate-200 rounded-full relative overflow-hidden">
              <motion.div
                className={`absolute top-0 h-full rounded-full ${getBarColor(totalAccel)} opacity-80`}
                style={{
                  left: totalAccel >= 0 ? '50%' : undefined,
                  right: totalAccel < 0 ? '50%' : undefined,
                }}
                animate={{ width: `${Math.abs(totalAccel) * 10}%` }}
                transition={{ type: 'spring', stiffness: 300, damping: 30 }}
              />
              <div className="absolute left-1/2 top-0 bottom-0 w-px bg-slate-400" />
              <span className="absolute inset-0 flex items-center justify-center text-xs font-bold text-slate-700">
                = {totalAccel.toFixed(1)}
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Description */}
      <AnimatePresence mode="wait">
        <motion.div
          key={desc.text}
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -10 }}
          className={`p-4 rounded-xl bg-white border-2 border-slate-200 ${desc.color}`}
        >
          <span className="text-xl mr-2">{desc.emoji}</span>
          <span className="text-sm font-medium">{desc.text}</span>
        </motion.div>
      </AnimatePresence>
    </div>
  );
}
