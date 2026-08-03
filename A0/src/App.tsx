import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import MathTex from './components/Math';
import Section from './components/Section';
import SymbolExplainer from './components/SymbolExplainer';
import FluidElementMotion from './components/FluidElementMotion';
import FourMotionsDetail from './components/FourMotionsDetail';
import DivergenceExplainer from './components/DivergenceExplainer';
import DivergenceAnimation from './components/DivergenceAnimation';
import CurlExplainer from './components/CurlExplainer';
import ContinuityDerivation from './components/ContinuityDerivation';
import ContinuityBox from './components/ContinuityBox';
import PipeDerivation from './components/PipeDerivation';
import PipeFlow from './components/PipeFlow';

function KeyPoint({ children, emoji = '🔑' }: { children: React.ReactNode; emoji?: string }) {
  return (
    <div className="flex gap-3 p-4 rounded-xl bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200">
      <span className="text-xl shrink-0">{emoji}</span>
      <div className="text-sm text-blue-900">{children}</div>
    </div>
  );
}

function FormulaCard({ children, label }: { children: React.ReactNode; label?: string }) {
  return (
    <div className="flex flex-col items-center gap-2 p-5 rounded-xl bg-slate-50 border border-slate-200">
      {label && <span className="text-xs font-medium text-slate-500 uppercase tracking-wider">{label}</span>}
      <div className="text-center">{children}</div>
    </div>
  );
}

const navItems = [
  { id: 'symbols', label: '符号解释' },
  { id: 'motion', label: '四种动作' },
  { id: 'divergence', label: '散度' },
  { id: 'curl', label: '旋度' },
  { id: 'continuity', label: '连续方程' },
  { id: 'pipe', label: '管道公式' },
  { id: 'quiz', label: '检验题' },
];

export default function App() {
  const [activeNav, setActiveNav] = useState('symbols');

  const scrollTo = (id: string) => {
    setActiveNav(id);
    document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-50 via-cyan-50/30 to-slate-50">
      {/* Hero Header */}
      <header className="relative overflow-hidden bg-gradient-to-br from-cyan-900 via-blue-900 to-indigo-900 text-white">
        <div className="absolute inset-0 opacity-10">
          <div className="absolute top-10 left-10 w-72 h-72 bg-cyan-400 rounded-full blur-3xl" />
          <div className="absolute bottom-10 right-10 w-96 h-96 bg-blue-400 rounded-full blur-3xl" />
        </div>
        <div className="relative max-w-4xl mx-auto px-6 py-16 text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-white/10 backdrop-blur text-sm mb-6">
              <span>🌊</span>
              <span>第3章 · 流体运动学</span>
            </div>
            <h1 className="text-4xl md:text-5xl font-bold mb-4 leading-tight">
              流体微团运动<br className="md:hidden" />与连续性原理
            </h1>
            <p className="text-lg text-cyan-200 max-w-2xl mx-auto">
              从零开始，彻底搞懂每一个符号、每一个公式的来龙去脉
            </p>
          </motion.div>
        </div>
      </header>

      {/* Navigation */}
      <nav className="sticky top-0 z-50 bg-white/80 backdrop-blur-xl border-b border-slate-200 shadow-sm">
        <div className="max-w-4xl mx-auto px-4">
          <div className="flex gap-1 overflow-x-auto py-2 scrollbar-hide">
            {navItems.map(item => (
              <button
                key={item.id}
                onClick={() => scrollTo(item.id)}
                className={`px-3 py-2 rounded-lg text-xs md:text-sm font-medium whitespace-nowrap transition-colors ${
                  activeNav === item.id
                    ? 'bg-cyan-100 text-cyan-700'
                    : 'text-slate-600 hover:bg-slate-100'
                }`}
              >
                {item.label}
              </button>
            ))}
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-4xl mx-auto px-4 py-10 space-y-8">
        
        {/* Section 0: Symbol Explanation */}
        <Section
          id="symbols"
          number="0"
          title="先搞清楚这些符号"
          subtitle="x, y, z 和 u, v, w 到底是啥？"
          color="from-slate-600 to-slate-700"
        >
          <div className="p-4 rounded-xl bg-amber-50 border border-amber-200 mb-4">
            <p className="text-amber-800 text-sm">
              <strong>⚠️ 重要提醒：</strong>如果你看到公式里的 u, v, w, x, y, z 感到困惑，
              先把这一节看明白！这些是流体力学最基础的符号。
            </p>
          </div>
          <SymbolExplainer />
        </Section>

        {/* Section 1: Four types of motion */}
        <Section
          id="motion"
          number="3.4"
          title="流体微团的四种基本动作"
          subtitle="刚体只会平移和旋转，但流体是软的"
          color="from-cyan-600 to-blue-600"
        >
          <p className="text-slate-700 leading-relaxed mb-4">
            想象一个<strong>果冻做的小方块</strong>飘在水里。水流动时，这个小方块会发生什么变化？
          </p>
          
          <div className="p-4 rounded-xl bg-slate-100 border border-slate-200 mb-4">
            <p className="text-slate-700">
              <strong>对比：</strong>刚体（比如一块石头）运动时只有两种动作：<strong>平移</strong>和<strong>旋转</strong>，
              它绝不会变形。但流体微团很软，它有<strong>四种动作</strong>可以同时发生！
            </p>
          </div>

          <h3 className="font-bold text-slate-800 mb-3">👇 动画演示：四种基本动作</h3>
          <FluidElementMotion />
          
          <h3 className="font-bold text-slate-800 mt-6 mb-3">📖 每种动作详解</h3>
          <FourMotionsDetail />
        </Section>

        {/* Section 2: Divergence */}
        <Section
          id="divergence"
          number="①"
          title="线变形与散度 ∇·V"
          subtitle="为什么散度表示体积膨胀率？"
          color="from-amber-500 to-orange-500"
        >
          <p className="text-slate-700 leading-relaxed mb-4">
            现在来彻底搞懂散度公式里的每一项是什么意思：
          </p>

          <FormulaCard label="散度公式">
            <MathTex
              tex="\nabla \cdot \vec{V} = \frac{\partial u}{\partial x} + \frac{\partial v}{\partial y} + \frac{\partial w}{\partial z}"
              display
            />
          </FormulaCard>

          <DivergenceExplainer />

          <h3 className="font-bold text-slate-800 mt-6 mb-3">👇 三种散度情况的可视化</h3>
          <DivergenceAnimation />

          <KeyPoint emoji="⭐">
            <strong>核心结论：</strong>如果流体是<strong>不可压缩</strong>的（比如水），微团体积不能变，
            所以必须满足：
            <div className="mt-2 p-3 rounded bg-white text-center">
              <MathTex tex="\nabla \cdot \vec{V} = 0" display />
            </div>
            <div className="mt-2 text-xs">这就是判断流动是否不可压缩的数学条件！</div>
          </KeyPoint>
        </Section>

        {/* Section 3: Curl */}
        <Section
          id="curl"
          number="②"
          title="旋转与旋度 ∇×V"
          subtitle="微团自己会不会像陀螺一样转？"
          color="from-purple-600 to-violet-600"
        >
          <p className="text-slate-700 leading-relaxed mb-4">
            旋度描述的是流体微团的<strong>自转</strong>角速度。注意：是微团自己转，不是绕着外面某个点公转！
          </p>

          <FormulaCard label="微团角速度">
            <MathTex tex="\vec{\omega} = \frac{1}{2} \nabla \times \vec{V}" display />
          </FormulaCard>

          <CurlExplainer />

          <KeyPoint emoji="💡">
            <strong>最容易搞混的地方：</strong>
            <div className="mt-2 space-y-2">
              <p>• <strong>刚体旋转</strong>（整个池子像洗衣机一样转）→ 微团跟着转，<strong>有旋</strong></p>
              <p>• <strong>自由涡</strong>（下水道漩涡）→ 微团绕中心公转但<strong>自己不转</strong>，所以是<strong>无旋</strong>！</p>
            </div>
          </KeyPoint>

          <div className="p-4 rounded-xl bg-violet-50 border border-violet-200">
            <div className="font-bold text-violet-800 mb-2">🎯 无旋流动（势流）</div>
            <div className="text-sm text-violet-700">
              满足 <MathTex tex="\nabla \times \vec{V} = 0" /> 的流动叫无旋流动或势流。
              这是第8章的核心内容！很多简化的流动分析都假设流动是无旋的。
            </div>
          </div>
        </Section>

        {/* Section 4: Continuity Equation */}
        <Section
          id="continuity"
          number="3.5"
          title="连续性方程的推导"
          subtitle="质量守恒如何写成数学公式？"
          color="from-blue-600 to-indigo-600"
        >
          <p className="text-slate-700 leading-relaxed text-lg font-medium mb-4">
            🗣️ <strong>核心思想：水不会凭空产生，也不会凭空消失。</strong>
          </p>

          <h3 className="font-bold text-slate-800 mb-3">📖 一步步推导连续方程</h3>
          <ContinuityDerivation />

          <h3 className="font-bold text-slate-800 mt-6 mb-3">👇 交互演示：控制体的质量变化</h3>
          <ContinuityBox />

          <div className="p-4 rounded-xl bg-slate-800 text-white mt-4">
            <div className="font-bold mb-2">📝 连续方程的三种形式</div>
            <div className="space-y-3 text-sm">
              <div className="p-3 rounded bg-white/10">
                <div className="text-slate-300 text-xs mb-1">一般形式（适用于所有情况）</div>
                <MathTex tex="\frac{\partial \rho}{\partial t} + \nabla \cdot (\rho \vec{V}) = 0" />
              </div>
              <div className="p-3 rounded bg-white/10">
                <div className="text-slate-300 text-xs mb-1">定常流动</div>
                <MathTex tex="\nabla \cdot (\rho \vec{V}) = 0" />
              </div>
              <div className="p-3 rounded bg-white/10">
                <div className="text-slate-300 text-xs mb-1">不可压缩流动</div>
                <MathTex tex="\nabla \cdot \vec{V} = 0" />
              </div>
            </div>
          </div>
        </Section>

        {/* Section 5: Pipe Flow */}
        <Section
          id="pipe"
          number="★"
          title="一维管道公式"
          subtitle="V₁A₁ = V₂A₂ 是怎么来的？"
          color="from-emerald-600 to-teal-600"
        >
          <PipeDerivation />

          <h3 className="font-bold text-slate-800 mt-6 mb-3">👇 交互演示：改变管径看速度变化</h3>
          <PipeFlow />

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
            <div className="p-4 rounded-xl bg-blue-50 border-2 border-blue-300">
              <div className="font-bold text-blue-800 mb-2">💧 不可压缩流体（水）</div>
              <div className="text-center py-2">
                <MathTex tex="V_1 A_1 = V_2 A_2" display />
              </div>
              <p className="text-xs text-blue-700">
                体积流量守恒。捏住水管出口，水喷得更快！
              </p>
            </div>
            <div className="p-4 rounded-xl bg-amber-50 border-2 border-amber-300">
              <div className="font-bold text-amber-800 mb-2">💨 可压缩流体（高速空气）</div>
              <div className="text-center py-2">
                <MathTex tex="\rho_1 V_1 A_1 = \rho_2 V_2 A_2" display />
              </div>
              <p className="text-xs text-amber-700">
                质量流量守恒。密度也可能变化！
              </p>
            </div>
          </div>

          <KeyPoint emoji="🛫">
            <strong>航空应用：</strong>发动机进气道、压气机、喷管的设计都要用 ρVA = 常数。
            这个公式决定了截面积该怎么变化。
          </KeyPoint>
        </Section>

        {/* Summary */}
        <motion.div
          initial={{ opacity: 0, y: 40 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl p-6 text-white shadow-xl"
        >
          <h2 className="text-xl font-bold mb-4 text-center">📋 本章核心总结</h2>
          <div className="space-y-4 text-sm">
            <div className="p-4 rounded-lg bg-white/10">
              <div className="font-bold text-cyan-300 mb-2">符号速查</div>
              <div className="grid grid-cols-2 gap-2 text-xs">
                <div>x, y, z = 空间坐标</div>
                <div>u, v, w = 速度分量</div>
                <div>∂u/∂x = u沿x的变化率</div>
                <div>∇·V = 散度（体积膨胀率）</div>
                <div>∇×V = 旋度（与自转有关）</div>
                <div>ρ = 密度</div>
              </div>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div className="p-3 rounded-lg bg-white/10">
                <div className="font-bold text-emerald-300 mb-1">不可压缩</div>
                <div className="text-slate-300">∇·V = 0</div>
              </div>
              <div className="p-3 rounded-lg bg-white/10">
                <div className="font-bold text-purple-300 mb-1">无旋流动</div>
                <div className="text-slate-300">∇×V = 0</div>
              </div>
            </div>
            <div className="p-4 rounded-lg bg-white/5 border border-white/10">
              <div className="font-bold text-blue-300 mb-2">🔧 计算题必备</div>
              <div className="grid grid-cols-2 gap-4 text-xs">
                <div>
                  <div className="text-slate-400">不可压管流：</div>
                  <div className="font-mono">V₁A₁ = V₂A₂</div>
                </div>
                <div>
                  <div className="text-slate-400">可压管流：</div>
                  <div className="font-mono">ρ₁V₁A₁ = ρ₂V₂A₂</div>
                </div>
              </div>
            </div>
          </div>
        </motion.div>

        {/* Quiz Section */}
        <Section
          id="quiz"
          number="🎯"
          title="检验题（7道）"
          subtitle="做完这些题，本章就过关了！"
          color="from-rose-500 to-pink-600"
        >
          <div className="space-y-4">
            <QuizItem
              number={1}
              type="选择"
              question="流体微团运动有四种基本形式，其中哪一种会使微团的体积发生变化？"
              options={['A. 平动', 'B. 旋转', 'C. 线变形', 'D. 角变形']}
              answer="C"
              explanation="线变形（伸缩变形）会使微团在某个方向拉长或压缩。如果三个方向的拉伸不相互抵消，体积就会变化。散度 ∇·V 正是描述这个变化的。平动和旋转不改变形状，角变形只是把正方形扭成平行四边形，面积/体积不变。"
            />
            <QuizItem
              number={2}
              type="判断"
              question="如果一个流动是不可压缩流动，那么散度 ∇·V 必须等于 0。"
              options={['对', '错']}
              answer="对"
              explanation="不可压缩意味着流体微团的体积不能变化。散度 ∇·V = ∂u/∂x + ∂v/∂y + ∂w/∂z 描述的正是相对体积膨胀率。体积不变 ⟺ 膨胀率为零 ⟺ ∇·V = 0。"
            />
            <QuizItem
              number={3}
              type="选择"
              question="在流体力学中，连续方程的本质是什么物理定律的体现？"
              options={['A. 能量守恒定律', 'B. 动量守恒定律', 'C. 质量守恒定律', 'D. 牛顿第二定律']}
              answer="C"
              explanation="连续方程 ∂ρ/∂t + ∇·(ρV) = 0 说的就是：流入控制体的质量 - 流出的质量 = 控制体内质量的增加。这正是质量守恒定律的数学表达。"
            />
            <QuizItem
              number={4}
              type="计算"
              question="有一根通水的自来水管。管子前半段直径是 10 cm，水流速度是 2 m/s。管子后半段变细了，直径变成了 5 cm。请问：细管子里的水流速度是多少？"
              options={['A. 2 m/s', 'B. 4 m/s', 'C. 8 m/s', 'D. 16 m/s']}
              answer="C"
              explanation="由连续方程 V₁A₁ = V₂A₂。面积 A = π(D/2)² ∝ D²。所以 V₂ = V₁ × (A₁/A₂) = V₁ × (D₁/D₂)² = 2 × (10/5)² = 2 × 4 = 8 m/s。直径变成一半，面积变成1/4，速度就要变成4倍。"
            />
            <QuizItem
              number={5}
              type="判断"
              question="洗车时，你用手捏扁出水软管的管口，水喷得更远了。这是因为截面积减小导致流速增加了，这个现象是基于连续方程解释的。"
              options={['对', '错']}
              answer="对"
              explanation="完全正确！这是连续方程 V₁A₁ = V₂A₂ 的典型生活应用。你捏住管口让出口面积 A 减小，根据体积流量守恒，流速 V 就必须增大。喷得更快所以更远。"
            />
            <QuizItem
              number={6}
              type="填空"
              question="如果管道里流的是可以被压缩的高速空气，我们不能再用 V₁A₁ = V₂A₂。我们必须保证前后两个截面相等的是什么流量？"
              options={['体积流量', '质量流量']}
              answer="质量流量"
              explanation="可压缩流体的密度 ρ 会变化，体积可能被压缩变小，所以体积流量 VA 不守恒。但不管怎么压缩，质量不会凭空消失，所以质量流量 ρVA 必须守恒。公式是 ρ₁V₁A₁ = ρ₂V₂A₂。"
            />
            <QuizItem
              number={7}
              type="判断"
              question="无旋流动（势流）的意思是，水不能沿着圆形的弯道流。"
              options={['对', '错']}
              answer="错"
              explanation="无旋流动指的是微团自身不旋转（不像陀螺一样自转），但整体流动完全可以沿着弯道走！典型例子是自由涡：水绕着中心流动（公转），但每一小团水自己并不自转。这是整体拐弯和自身旋转的区别。看动画里红点的运动轨迹可以帮助理解。"
            />
          </div>
        </Section>

        {/* Footer */}
        <div className="text-center py-8 text-sm text-slate-400">
          <p>流体微团运动与连续性原理 · 彻底讲透版</p>
          <p className="mt-1">每个符号、每个公式都有来龙去脉 🌊</p>
        </div>
      </main>
    </div>
  );
}

interface QuizItemProps {
  number: number;
  type: string;
  question: string;
  options: string[];
  answer: string;
  explanation: string;
}

function QuizItem({ number, type, question, options, answer, explanation }: QuizItemProps) {
  const [selected, setSelected] = useState<string | null>(null);
  const [showAnswer, setShowAnswer] = useState(false);

  const isCorrect = selected === answer;
  const typeColor = type === '选择' ? 'bg-blue-100 text-blue-700' :
                    type === '判断' ? 'bg-purple-100 text-purple-700' :
                    type === '计算' ? 'bg-amber-100 text-amber-700' :
                    'bg-emerald-100 text-emerald-700';

  const getOptionKey = (opt: string) => {
    const firstChar = opt.charAt(0);
    if (['A', 'B', 'C', 'D'].includes(firstChar)) {
      return firstChar;
    }
    return opt;
  };

  return (
    <div className="p-4 rounded-xl bg-white border border-slate-200 shadow-sm">
      <div className="flex items-start gap-3 mb-3">
        <span className="flex items-center justify-center w-7 h-7 rounded-full bg-slate-100 text-slate-700 font-bold text-sm shrink-0">
          {number}
        </span>
        <div className="flex-1">
          <span className={`inline-block px-2 py-0.5 rounded text-xs font-medium ${typeColor} mb-2`}>
            {type}题
          </span>
          <p className="text-slate-800 font-medium">{question}</p>
        </div>
      </div>

      <div className="ml-10 space-y-2">
        {options.map((opt, i) => {
          const optKey = getOptionKey(opt);
          const isSelected = selected === optKey;
          const isAnswer = answer === optKey;
          
          return (
            <button
              key={i}
              onClick={() => !showAnswer && setSelected(optKey)}
              disabled={showAnswer}
              className={`w-full text-left px-4 py-2 rounded-lg text-sm transition-all ${
                showAnswer
                  ? isAnswer
                    ? 'bg-emerald-100 border-emerald-300 text-emerald-800'
                    : isSelected
                      ? 'bg-red-100 border-red-300 text-red-800'
                      : 'bg-slate-50 border-slate-200 text-slate-500'
                  : isSelected
                    ? 'bg-blue-100 border-blue-300 text-blue-800'
                    : 'bg-slate-50 border-slate-200 text-slate-700 hover:bg-slate-100'
              } border`}
            >
              {opt}
            </button>
          );
        })}
      </div>

      <div className="ml-10 mt-3">
        {!showAnswer ? (
          <button
            onClick={() => setShowAnswer(true)}
            disabled={!selected}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
              selected
                ? 'bg-blue-600 text-white hover:bg-blue-700'
                : 'bg-slate-100 text-slate-400 cursor-not-allowed'
            }`}
          >
            确认答案
          </button>
        ) : (
          <AnimatePresence>
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              className={`p-3 rounded-lg text-sm ${
                isCorrect ? 'bg-emerald-50 text-emerald-800' : 'bg-amber-50 text-amber-800'
              }`}
            >
              <div className="font-bold mb-1">
                {isCorrect ? '✅ 正确！' : `❌ 正确答案是：${answer}`}
              </div>
              <div className="text-xs opacity-90 leading-relaxed">{explanation}</div>
            </motion.div>
          </AnimatePresence>
        )}
      </div>
    </div>
  );
}
