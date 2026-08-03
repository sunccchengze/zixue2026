import { motion } from 'framer-motion';
import { ReactNode } from 'react';

interface SectionProps {
  id: string;
  number: string;
  title: string;
  subtitle?: string;
  children: ReactNode;
  color?: string;
}

export default function Section({ id, number, title, subtitle, children, color = 'from-blue-500 to-indigo-600' }: SectionProps) {
  return (
    <motion.section
      id={id}
      initial={{ opacity: 0, y: 40 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: '-50px' }}
      transition={{ duration: 0.6, ease: 'easeOut' }}
      className="scroll-mt-20"
    >
      <div className="bg-white rounded-2xl shadow-lg shadow-slate-200/50 border border-slate-100 overflow-hidden">
        <div className={`bg-gradient-to-r ${color} px-6 py-4`}>
          <div className="flex items-center gap-3">
            <span className="flex items-center justify-center w-9 h-9 rounded-full bg-white/20 text-white font-bold text-lg">
              {number}
            </span>
            <div>
              <h2 className="text-xl font-bold text-white">{title}</h2>
              {subtitle && <p className="text-sm text-white/80 mt-0.5">{subtitle}</p>}
            </div>
          </div>
        </div>
        <div className="p-6 space-y-5">
          {children}
        </div>
      </div>
    </motion.section>
  );
}
