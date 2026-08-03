import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import MathTex from './Math';

export default function ContinuityDerivation() {
  const [step, setStep] = useState(0);

  const steps = [
    {
      title: '第1步：画一个虚拟的小盒子',
      content: (
        <div className="space-y-3">
          <p>在流场中想象一个固定不动的小长方体（控制体），边长为 dx, dy, dz。</p>
          <div className="flex justify-center">
            <svg width="200" height="150" viewBox="0 0 200 150">
              {/* 3D box */}
              <polygon points="60,100 140,100 160,70 80,70" fill="#bfdbfe" stroke="#3b82f6" strokeWidth="2" />
              <polygon points="60,100 60,50 80,20 80,70" fill="#93c5fd" stroke="#3b82f6" strokeWidth="2" />
              <polygon points="60,50 140,50 160,20 80,20" fill="#dbeafe" stroke="#3b82f6" strokeWidth="2" />
              <polygon points="140,100 140,50 160,20 160,70" fill="#60a5fa" stroke="#3b82f6" strokeWidth="2" />
              
              {/* Labels */}
              <text x="100" y="115" textAnchor="middle" className="text-xs fill-slate-600">dx</text>
              <text x="45" y="75" textAnchor="middle" className="text-xs fill-slate-600">dy</text>
              <text x="165" y="45" textAnchor="middle" className="text-xs fill-slate-600">dz</text>
            </svg>
          </div>
          <p className="text-sm text-slate-600">这个盒子是虚拟的，流体可以自由穿过它的六个面。</p>
        </div>
      ),
    },
    {
      title: '第2步：计算流入流出的质量',
      content: (
        <div className="space-y-3">
          <p>看 x 方向：左边进，右边出</p>
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div className="p-3 rounded-lg bg-green-50 border border-green-200">
              <div className="font-bold text-green-700 mb-1">左边流入</div>
              <MathTex tex="(\rho u) \cdot dy \cdot dz" />
              <div className="text-xs text-green-600 mt-1">密度×速度×面积 = 质量流量</div>
            </div>
            <div className="p-3 rounded-lg bg-red-50 border border-red-200">
              <div className="font-bold text-red-700 mb-1">右边流出</div>
              <MathTex tex="\left(\rho u + \frac{\partial(\rho u)}{\partial x}dx\right) \cdot dy \cdot dz" />
              <div className="text-xs text-red-600 mt-1">走了 dx 距离，ρu 可能变了</div>
            </div>
          </div>
          <div className="p-3 rounded-lg bg-blue-50 border border-blue-200">
            <div className="font-bold text-blue-700 mb-1">x方向净流出</div>
            <MathTex tex="\frac{\partial(\rho u)}{\partial x} dx \cdot dy \cdot dz" display />
          </div>
        </div>
      ),
    },
    {
      title: '第3步：三个方向加起来',
      content: (
        <div className="space-y-3">
          <p>同理，y方向和z方向也有净流出：</p>
          <div className="p-4 rounded-lg bg-slate-50 border border-slate-200">
            <div className="text-center">
              <MathTex tex="\text{总净流出} = \left(\frac{\partial(\rho u)}{\partial x} + \frac{\partial(\rho v)}{\partial y} + \frac{\partial(\rho w)}{\partial z}\right) dx\,dy\,dz" display />
            </div>
            <div className="text-center mt-2">
              <MathTex tex="= \nabla \cdot (\rho \vec{V}) \cdot dV" />
            </div>
          </div>
          <p className="text-sm text-slate-600">
            这里 <MathTex tex="\nabla \cdot (\rho \vec{V})" /> 就是"质量通量的散度"，表示单位体积的净流出率。
          </p>
        </div>
      ),
    },
    {
      title: '第4步：质量守恒！',
      content: (
        <div className="space-y-3">
          <p>流出的质量去哪了？肯定是盒子里存的质量变少了！</p>
          <div className="grid grid-cols-2 gap-4">
            <div className="p-3 rounded-lg bg-red-50 border border-red-200 text-center">
              <div className="text-sm font-bold text-red-700 mb-1">净流出的质量率</div>
              <MathTex tex="\nabla \cdot (\rho \vec{V}) \cdot dV" />
            </div>
            <div className="p-3 rounded-lg bg-blue-50 border border-blue-200 text-center">
              <div className="text-sm font-bold text-blue-700 mb-1">盒内质量减少率</div>
              <MathTex tex="-\frac{\partial \rho}{\partial t} \cdot dV" />
            </div>
          </div>
          <div className="text-center text-2xl my-2">↓ 相等 ↓</div>
          <div className="p-4 rounded-lg bg-emerald-100 border-2 border-emerald-300 text-center">
            <MathTex tex="\frac{\partial \rho}{\partial t} + \nabla \cdot (\rho \vec{V}) = 0" display />
            <div className="text-sm text-emerald-700 mt-2 font-bold">这就是连续方程！</div>
          </div>
        </div>
      ),
    },
    {
      title: '第5步：特殊情况简化',
      content: (
        <div className="space-y-4">
          <div className="p-4 rounded-lg bg-amber-50 border border-amber-200">
            <div className="font-bold text-amber-800 mb-2">如果是定常流动</div>
            <p className="text-sm text-amber-700 mb-2">任何位置的密度都不随时间变化：<MathTex tex="\frac{\partial \rho}{\partial t} = 0" /></p>
            <div className="text-center">
              <MathTex tex="\nabla \cdot (\rho \vec{V}) = 0" />
            </div>
            <p className="text-xs text-amber-600 mt-2">意思：进多少质量 = 出多少质量</p>
          </div>
          <div className="p-4 rounded-lg bg-blue-50 border border-blue-200">
            <div className="font-bold text-blue-800 mb-2">如果是不可压缩流动</div>
            <p className="text-sm text-blue-700 mb-2">密度 ρ 是常数，可以提出来：</p>
            <div className="text-center">
              <MathTex tex="\nabla \cdot \vec{V} = 0" />
            </div>
            <p className="text-xs text-blue-600 mt-2">意思：进多少体积 = 出多少体积（体积流量守恒）</p>
          </div>
        </div>
      ),
    },
  ];

  return (
    <div className="space-y-4">
      {/* Progress bar */}
      <div className="flex gap-1">
        {steps.map((_, i) => (
          <button
            key={i}
            onClick={() => setStep(i)}
            className={`flex-1 h-2 rounded-full transition-all ${
              i <= step ? 'bg-blue-500' : 'bg-slate-200'
            }`}
          />
        ))}
      </div>

      <AnimatePresence mode="wait">
        <motion.div
          key={step}
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          exit={{ opacity: 0, x: -20 }}
          className="p-5 rounded-xl bg-white border-2 border-slate-200 min-h-[280px]"
        >
          <div className="flex items-center gap-3 mb-4">
            <span className="flex items-center justify-center w-8 h-8 rounded-full bg-blue-100 text-blue-700 font-bold text-sm">
              {step + 1}
            </span>
            <h3 className="font-bold text-slate-800">{steps[step].title}</h3>
          </div>
          <div className="text-slate-700">
            {steps[step].content}
          </div>
        </motion.div>
      </AnimatePresence>

      <div className="flex justify-between">
        <button
          onClick={() => setStep(Math.max(0, step - 1))}
          disabled={step === 0}
          className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
            step === 0
              ? 'bg-slate-100 text-slate-400 cursor-not-allowed'
              : 'bg-slate-200 text-slate-700 hover:bg-slate-300'
          }`}
        >
          ← 上一步
        </button>
        <span className="text-sm text-slate-500 self-center">
          {step + 1} / {steps.length}
        </span>
        <button
          onClick={() => setStep(Math.min(steps.length - 1, step + 1))}
          disabled={step === steps.length - 1}
          className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
            step === steps.length - 1
              ? 'bg-slate-100 text-slate-400 cursor-not-allowed'
              : 'bg-blue-600 text-white hover:bg-blue-700'
          }`}
        >
          下一步 →
        </button>
      </div>
    </div>
  );
}
