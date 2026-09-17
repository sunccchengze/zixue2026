#!/usr/bin/env bash
# 一键生成讲义 PDF · 人工智能基础与应用
#
#   ./生成讲义PDF.sh                  # 默认：每讲各出一份 + 全书（含封面/目录/版权页）
#   ./生成讲义PDF.sh --charter        # 另出《章程与地图》分册
#   ./生成讲义PDF.sh --one M2         # 只重做 M2
#   ./生成讲义PDF.sh --check          # 只体检（公式逐条编译），不产出 PDF
#   ./生成讲义PDF.sh --book --preview 3   # 出全书并导出第 3 页 PNG 供肉眼检查
#
# 产物：
#   讲义/pdf/*.pdf          （M0–M3 讲义 + README + 大纲 + 全书）
#   章程与地图/pdf/*.pdf    （宪法层九份章程合订）
set -euo pipefail

cd "$(dirname "$0")"

PY="${PDF_PY:-/home/user/opt/pdfenv/bin/python}"
if [ ! -x "$PY" ]; then
  cat <<'EOF'
✘ 排版环境未就绪（找不到 typst 版 Python 环境）。

  一次性准备（约 1 分钟，之后完全离线）：
      bash 环境/pdf/bootstrap.sh

  说明：本学科不依赖系统 LaTeX/Chromium。排版引擎用 PyPI 的 typst 包，
       中文字体用 npm 的思源宋体/黑体，全部落在 /home/user/opt/ 下。
EOF
  exit 1
fi

if [ "$#" -eq 0 ]; then
  set -- --all --book
fi

exec "$PY" md2typst.py "$@"
