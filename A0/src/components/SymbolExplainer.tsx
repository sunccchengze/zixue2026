import { useState } from 'react';
import { motion } from 'framer-motion';
import MathTex from './Math';

export default function SymbolExplainer() {
  const [activeTab, setActiveTab] = useState<'coords' | 'velocity' | 'partial'>('coords');

  return (
    <div className="space-y-4">
      <div className="flex gap-2 flex-wrap">
        <button
          onClick={() => setActiveTab('coords')}
          className={`px-3 py-2 rounded-lg text-sm font-medium transition-all ${
            activeTab === 'coords' ? 'bg-blue-600 text-white' : 'bg-slate-100 hover:bg-slate-200'
          }`}
        >
          x, y, z 是什么？
        </button>
        <button
          onClick={() => setActiveTab('velocity')}
          className={`px-3 py-2 rounded-lg text-sm font-medium transition-all ${
            activeTab === 'velocity' ? 'bg-emerald-600 text-white' : 'bg-slate-100 hover:bg-slate-200'
          }`}
        >
          u, v, w 是什么？
        </button>
        <button
          onClick={() => setActiveTab('partial')}
          className={`px-3 py-2 rounded-lg text-sm font-medium transition-all ${
            activeTab === 'partial' ? 'bg-purple-600 text-white' : 'bg-slate-100 hover:bg-slate-200'
          }`}
        >
          ∂u/∂x 是什么？
        </button>
      </div>

      <motion.div
        key={activeTab}
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        className="p-5 rounded-xl bg-white border-2 border-slate-200 shadow-sm"
      >
        {activeTab === 'coords' && (
          <div className="space-y-4">
            <div className="flex items-start gap-4">
              <svg width="150" height="150" viewBox="0 0 150 150" className="shrink-0">
                {/* Origin */}
                <circle cx="40" cy="110" r="4" fill="#1e293b" />
                <text x="30" y="125" className="text-xs fill-slate-600">O</text>
                
                {/* X axis */}
                <line x1="40" y1="110" x2="130" y2="110" stroke="#ef4444" strokeWidth="2" markerEnd="url(#arrowRed)" />
                <text x="135" y="115" className="text-sm font-bold fill-red-500">x</text>
                <text x="90" y="130" className="text-xs fill-red-400">（右）</text>
                
                {/* Y axis */}
                <line x1="40" y1="110" x2="100" y2="60" stroke="#22c55e" strokeWidth="2" markerEnd="url(#arrowGreen)" />
                <text x="105" y="55" className="text-sm font-bold fill-green-500">y</text>
                <text x="85" y="75" className="text-xs fill-green-400">（前）</text>
                
                {/* Z axis */}
                <line x1="40" y1="110" x2="40" y2="20" stroke="#3b82f6" strokeWidth="2" markerEnd="url(#arrowBlue)" />
                <text x="45" y="18" className="text-sm font-bold fill-blue-500">z</text>
                <text x="15" y="60" className="text-xs fill-blue-400">（上）</text>
                
                <defs>
                  <marker id="arrowRed" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
                    <polygon points="0 0, 10 3.5, 0 7" fill="#ef4444" />
                  </marker>
                  <marker id="arrowGreen" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
                    <polygon points="0 0, 10 3.5, 0 7" fill="#22c55e" />
                  </marker>
                  <marker id="arrowBlue" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
                    <polygon points="0 0, 10 3.5, 0 7" fill="#3b82f6" />
                  </marker>
                </defs>
              </svg>
              <div>
                <h3 className="font-bold text-slate-800 mb-2">x, y, z = 三维空间的坐标轴</h3>
                <p className="text-sm text-slate-600 mb-3">
                  就像你描述一个点的位置需要说"往右走3米、往前走2米、往上走1米"，
                  数学上用 (x, y, z) 三个数字来表示空间中任意一点的位置。
                </p>
                <div className="grid grid-cols-3 gap-2 text-xs">
                  <div className="p-2 rounded bg-red-50 text-red-700">
                    <strong>x</strong>：水平向右
                  </div>
                  <div className="p-2 rounded bg-green-50 text-green-700">
                    <strong>y</strong>：水平向前
                  </div>
                  <div className="p-2 rounded bg-blue-50 text-blue-700">
                    <strong>z</strong>：垂直向上
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'velocity' && (
          <div className="space-y-4">
            <div className="flex items-start gap-4">
              <svg width="150" height="150" viewBox="0 0 150 150" className="shrink-0">
                {/* Fluid particle */}
                <circle cx="60" cy="80" r="15" fill="#bfdbfe" stroke="#3b82f6" strokeWidth="2" />
                <text x="60" y="85" textAnchor="middle" className="text-xs fill-blue-700">微团</text>
                
                {/* Velocity vector */}
                <line x1="75" y1="80" x2="130" y2="50" stroke="#f59e0b" strokeWidth="3" markerEnd="url(#arrowOrange)" />
                <text x="105" y="45" className="text-sm font-bold fill-amber-600">V⃗</text>
                
                {/* Components */}
                <line x1="75" y1="80" x2="130" y2="80" stroke="#ef4444" strokeWidth="2" strokeDasharray="4" />
                <text x="105" y="95" className="text-xs fill-red-500">u (x方向)</text>
                
                <line x1="130" y1="80" x2="130" y2="50" stroke="#3b82f6" strokeWidth="2" strokeDasharray="4" />
                <text x="135" y="68" className="text-xs fill-blue-500">w</text>
                
                <defs>
                  <marker id="arrowOrange" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
                    <polygon points="0 0, 10 3.5, 0 7" fill="#f59e0b" />
                  </marker>
                </defs>
              </svg>
              <div>
                <h3 className="font-bold text-slate-800 mb-2">u, v, w = 速度在三个方向的分量</h3>
                <p className="text-sm text-slate-600 mb-3">
                  流体微团的速度 <MathTex tex="\vec{V}" /> 是一个<strong>矢量</strong>（既有大小又有方向）。
                  我们把它拆成三个方向的分量：
                </p>
                <div className="p-3 rounded-lg bg-amber-50 border border-amber-200 mb-3">
                  <MathTex tex="\vec{V} = (u, v, w) = u\vec{i} + v\vec{j} + w\vec{k}" />
                </div>
                <div className="grid grid-cols-3 gap-2 text-xs">
                  <div className="p-2 rounded bg-red-50 text-red-700">
                    <strong>u</strong>：x方向的速度
                  </div>
                  <div className="p-2 rounded bg-green-50 text-green-700">
                    <strong>v</strong>：y方向的速度
                  </div>
                  <div className="p-2 rounded bg-blue-50 text-blue-700">
                    <strong>w</strong>：z方向的速度
                  </div>
                </div>
                <p className="text-xs text-slate-500 mt-2">
                  比如 u=3 表示微团以 3 m/s 的速度往 x 正方向（右）走
                </p>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'partial' && (
          <div className="space-y-4">
            <h3 className="font-bold text-slate-800 mb-2">
              <MathTex tex="\frac{\partial u}{\partial x}" /> = u 随 x 变化有多快
            </h3>
            <p className="text-sm text-slate-600">
              这是<strong>偏导数</strong>，意思是：如果我沿着 x 方向移动一小段距离，
              速度的 u 分量会变化多少？
            </p>
            
            <div className="p-4 rounded-lg bg-slate-50 border border-slate-200">
              <div className="text-sm text-slate-700 mb-3">
                <strong>具体例子：</strong>假设在管道里，越往右（x 增大）水流越快：
              </div>
              <div className="flex items-center gap-4">
                <div className="flex-1">
                  <svg width="100%" height="80" viewBox="0 0 300 80">
                    {/* Pipe */}
                    <rect x="20" y="25" width="260" height="30" fill="#bfdbfe" stroke="#3b82f6" strokeWidth="2" rx="4" />
                    
                    {/* Velocity arrows */}
                    <line x1="50" y1="40" x2="70" y2="40" stroke="#ef4444" strokeWidth="3" markerEnd="url(#arr1)" />
                    <text x="60" y="65" textAnchor="middle" className="text-xs fill-red-500">u=2</text>
                    
                    <line x1="140" y1="40" x2="175" y2="40" stroke="#ef4444" strokeWidth="3" markerEnd="url(#arr1)" />
                    <text x="157" y="65" textAnchor="middle" className="text-xs fill-red-500">u=4</text>
                    
                    <line x1="230" y1="40" x2="280" y2="40" stroke="#ef4444" strokeWidth="3" markerEnd="url(#arr1)" />
                    <text x="255" y="65" textAnchor="middle" className="text-xs fill-red-500">u=6</text>
                    
                    {/* X axis label */}
                    <text x="150" y="15" textAnchor="middle" className="text-xs fill-slate-500">x 方向 →</text>
                    
                    <defs>
                      <marker id="arr1" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
                        <polygon points="0 0, 8 3, 0 6" fill="#ef4444" />
                      </marker>
                    </defs>
                  </svg>
                </div>
              </div>
              <div className="mt-3 p-3 rounded bg-purple-50 text-purple-800 text-sm">
                <MathTex tex="\frac{\partial u}{\partial x} > 0" /> 表示：往右走，u 在增大（流速加快）
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs">
              <div className="p-3 rounded-lg bg-red-50 border border-red-200">
                <div className="font-bold text-red-700 mb-1"><MathTex tex="\frac{\partial u}{\partial x}" /></div>
                <div className="text-red-600">沿 x 方向，u 分量的变化率</div>
              </div>
              <div className="p-3 rounded-lg bg-green-50 border border-green-200">
                <div className="font-bold text-green-700 mb-1"><MathTex tex="\frac{\partial v}{\partial y}" /></div>
                <div className="text-green-600">沿 y 方向，v 分量的变化率</div>
              </div>
              <div className="p-3 rounded-lg bg-blue-50 border border-blue-200">
                <div className="font-bold text-blue-700 mb-1"><MathTex tex="\frac{\partial w}{\partial z}" /></div>
                <div className="text-blue-600">沿 z 方向，w 分量的变化率</div>
              </div>
            </div>
          </div>
        )}
      </motion.div>
    </div>
  );
}
