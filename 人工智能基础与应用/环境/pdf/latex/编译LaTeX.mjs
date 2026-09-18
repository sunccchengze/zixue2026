#!/usr/bin/env node
/**
 * LaTeX 编译器（Tectonic wasm 引擎）· Agent 维护 · B7
 *
 * 用法：
 *   node 编译LaTeX.mjs a.tex [b.tex ...]            # 每个 .tex 编译成同名 .pdf
 *   node 编译LaTeX.mjs a.tex=out.pdf [b.tex=...]    # 指定输出（导出器用这种）
 *   node 编译LaTeX.mjs --check a.tex          # 只报告状态，不写文件
 *
 * 引擎与宏包来源（npm 包 glyphtex-engine，MIT）：
 *   /home/user/opt/tex/glyphtex/wasm/tectonic_wasm.wasm   Tectonic（XeTeX 内核）wasm
 *   /home/user/opt/tex/glyphtex/bundle/*                  TeX Live 宏包与字体（1242 个文件）
 * 本仓库不带二进制，重装见 环境/pdf/latex/bootstrap_latex.sh（约 1 分钟，npm 通道）。
 *
 * 为什么自己写驱动而不是装 TeX Live：本环境 apt/CTAN/conda 均不可达（实测），
 * 只有 PyPI 与 npm 通。wasm 版引擎是唯一能真正跑起来的 LaTeX 实现。
 */
import fs from 'node:fs';
import path from 'node:path';

const ENGINE_DIR = '/home/user/opt/tex/glyphtex';
const BUNDLE = path.join(ENGINE_DIR, 'bundle');
const WASM = path.join(ENGINE_DIR, 'wasm', 'tectonic_wasm.wasm');
const FONT_DIRS = ['/home/user/opt/fonts',
                   '/home/user/zixue2026/人工智能基础与应用/环境/pdf/字体'];

async function loadEngine() {
  const { TexEngine } = await import(path.join(ENGINE_DIR, 'dist', 'index.js'));
  const engine = await TexEngine.load(fs.readFileSync(WASM));
  let n = 0;
  for (const f of fs.readdirSync(BUNDLE)) {
    const p = path.join(BUNDLE, f);
    if (fs.statSync(p).isFile()) { engine.addFile(f, fs.readFileSync(p)); n++; }
  }
  // 中文字体与拉丁兜底（按基名注册，.tex 里用 [文件名] 引用）
  for (const dir of FONT_DIRS) {
    if (!fs.existsSync(dir)) continue;
    for (const f of fs.readdirSync(dir)) {
      if (!/\.(ttf|otf|ttc)$/i.test(f)) continue;
      engine.addFile(f, fs.readFileSync(path.join(dir, f)));
      n++;
    }
  }
  return { engine, n };
}

const args = process.argv.slice(2);
const checkOnly = args[0] === '--check';
const files = (checkOnly ? args.slice(1) : args).filter(f => f.endsWith('.tex') || /=\S+\.pdf$/.test(f));
if (files.length === 0) {
  console.error('用法: node 编译LaTeX.mjs [--check] file1.tex [file2.tex ...]   # PDF 输出同名同目录');
  process.exit(2);
}

const { engine, n } = await loadEngine();
let failed = 0;

for (const arg of files) {
  // 支持 `源.tex=输出.pdf` 形式；不给输出名时用同名 .pdf
  const [texPath, explicitOut] = arg.includes('=') ? arg.split('=') : [arg, null];
  const outPdf = explicitOut || texPath.replace(/\.tex$/, '.pdf');
  const src = fs.readFileSync(texPath, 'utf8');
  engine.clearFiles?.();
  // 重新装字体与宏包（clearFiles 会清空）
  for (const f of fs.readdirSync(BUNDLE)) {
    const p = path.join(BUNDLE, f);
    if (fs.statSync(p).isFile()) engine.addFile(f, fs.readFileSync(p));
  }
  for (const dir of FONT_DIRS) {
    if (!fs.existsSync(dir)) continue;
    for (const f of fs.readdirSync(dir)) {
      if (/\.(ttf|otf|ttc)$/i.test(f)) engine.addFile(f, fs.readFileSync(path.join(dir, f)));
    }
  }
  engine.addFile('main.tex', src);
  const res = engine.compile({ entry: 'main.tex', minPasses: 2 });
  const log = engine.log() || '';
  const missing = log.split('\n').filter(l => /Missing character/.test(l));
  const errors = log.split('\n').filter(l => /^!/.test(l));
  const pdf = engine.pdf();
  const ok = res.status !== 'failed' && pdf && pdf.length > 1000;
  if (!ok && res.status === 'spotless') console.log('   log 尾部:', log.split('\n').slice(-6).join(' | ').slice(0, 300));
  const status = ok ? '✔' : '✘';
  const kb = pdf ? (pdf.length / 1024).toFixed(0) : 0;
  console.log(`${status} ${path.basename(texPath)}  ${kb} KB  缺字:${missing.length} 错误:${errors.length}` +
              (res.message ? `  ${res.message.slice(0, 90)}` : ''));
  if (missing.length) console.log('   ' + missing.slice(0, 3).join('\n   '));
  if (errors.length) console.log('   ' + errors.slice(0, 3).join('\n   '));
  if (!ok) failed++;
  if (ok && !checkOnly) fs.writeFileSync(outPdf, pdf);
  else if (outPdf !== texPath && fs.existsSync(outPdf)) fs.unlinkSync(outPdf);
}

process.exit(failed ? 1 : 0);
