#!/usr/bin/env bash
# LaTeX 通道一键重建 · Agent 维护 · B7
#
# 做什么：从 npm 取 glyphtex-engine（Tectonic wasm 版 XeTeX + TeX Live 宏包树），
#         解到 /home/user/opt/tex/glyphtex，叠加全部可选宏包包，再把中文字体放进去，
#         最后编译一份自检 .tex（中文 + 数学 + 代码块 + emoji）确认能出 PDF。
#
# 为什么走 npm：本环境实测 ctan.org / tug.org / conda / GitHub release 资产全不可达，
#               PyPI 的 tectonic 是空壳包；npm 是唯一能拿到真 LaTeX 引擎的通道。
#
# 用法： bash 环境/pdf/latex/bootstrap_latex.sh
set -euo pipefail

PKG="glyphtex-engine@0.1.0"
DEST="${TEX_DIR:-/home/user/opt/tex/glyphtex}"
FONT_DIR="${FONT_DIR:-/home/user/opt/fonts}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_FONT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)/字体"   # 可选：仓库内字体副本（不入库，见 README）
PY="${PY:-/home/user/opt/.venv/bin/python}"

echo "==> 1/5 取 npm 包（$PKG）"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
cd "$TMP"
npm pack "$PKG" --silent >/dev/null
TARBALL="$(ls *.tgz | head -1)"
tar xzf "$TARBALL"
PKG_DIR="$TMP/package"

echo "==> 2/5 安装引擎与宏包树到 $DEST"
mkdir -p "$DEST/wasm" "$DEST/bundle" "$DEST/dist"
cp "$PKG_DIR/wasm/tectonic_wasm.wasm" "$DEST/wasm/"
cp -r "$PKG_DIR/wasm/packs" "$DEST/wasm/" 2>/dev/null || true
cp -r "$PKG_DIR/dist/." "$DEST/dist/"
tar xzf "$PKG_DIR/wasm/tectonic-bundle.tar.gz" -C "$DEST/bundle"

echo "==> 3/5 叠加可选宏包包（fonts-latinmodern 含数学的物理字模，必需）"
for p in "$DEST"/wasm/packs/*.tar.gz; do
  [ -e "$p" ] || continue
  tar xzf "$p" -C "$DEST/bundle" 2>/dev/null || true
done
echo "    bundle 现有 $(ls "$DEST/bundle" | wc -l) 个文件"

echo "==> 4/5 字体（思源宋/黑 + DejaVu + Noto Emoji）"
# 字体不入库（体积 + 可重建）：优先用 $FONT_DIR，其次是仓库内的副本（如果存在）
if [ ! -e "$FONT_DIR/NotoSerifSC-Regular.ttf" ]; then
  if [ -d "$REPO_FONT_DIR" ] && [ -n "$(ls -A "$REPO_FONT_DIR" 2>/dev/null)" ]; then
    mkdir -p "$FONT_DIR"
    cp -f "$REPO_FONT_DIR"/*.ttf "$FONT_DIR/" 2>/dev/null || true
  else
    echo "    字体缺失，先跑 环境/pdf/bootstrap.sh 取字体…"
    bash "$SCRIPT_DIR/../bootstrap.sh" >/dev/null 2>&1 || true
  fi
fi
if [ ! -e "$FONT_DIR/NotoSerifSC-Regular.ttf" ]; then
  echo "    ✘ 仍缺中文字体：请先运行 环境/pdf/bootstrap.sh" >&2
  exit 1
fi
for f in "$FONT_DIR"/*.ttf; do
  cp -f "$f" "$DEST/bundle/"          # 引擎从虚拟文件系统根目录读字体
done
ls "$FONT_DIR" | sed 's/^/    /'

echo "==> 5/5 自检：中文 + 数学 + 代码块 + emoji"
CHECK="$TMP/check.tex"
cat > "$CHECK" <<'TEX'
\documentclass[11pt,a4paper]{article}
\usepackage{lmodern}
\usepackage{amsmath}
\usepackage{listings}
\usepackage[T1]{fontenc}
\font\zhfont="[NotoSerifSC-Regular.ttf]:script=hani" at 10.5pt
\font\emofont="[NotoEmoji-Regular.ttf]" at 10.5pt
\def\zh#1{{\zhfont #1}}
\def\emo#1{{\emofont #1}}
\def\zhglue{\hskip0pt plus .06em minus .01em}
\lstset{basicstyle=\zhfont, escapeinside={(*@}{@*)}, frame=single}
\begin{document}
Check: \zh{自\zhglue 检\zhglue ：\zhglue 中\zhglue 文} $\frac{a}{b}+\sqrt{c}$ emoji \emo{⭐} \zh{。}
\begin{lstlisting}
# 代码块中文 + (*@{\emo{⭐}}@*)
\end{lstlisting}
\end{document}
TEX
node "$SCRIPT_DIR/编译LaTeX.mjs" "$CHECK=${TMP}/check.pdf"
test -s "$TMP/check.pdf" && echo "==> 完成：引擎可用（自检 PDF $(stat -c%s "$TMP/check.pdf") 字节）"
