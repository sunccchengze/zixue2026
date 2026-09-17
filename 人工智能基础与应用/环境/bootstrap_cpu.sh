#!/usr/bin/env bash
# 环境引导 · T0 档（纯 CPU / 零 GPU）
# 用途：把判分环境装好，让 `环境/judge/judge.sh` 能直接跑。
# 作者：Agent（脚手架区 B1）；用户不需要改这个文件。
#
# 用法：
#   bash 环境/bootstrap_cpu.sh              # 轻量档：够跑课题01 判分（默认，秒装）
#   bash 环境/bootstrap_cpu.sh --with-torch # 加装 torch（课题02 起需要；约 555MB）
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV="$HERE/.venv"
PY="${PYTHON:-python3}"
WITH_TORCH=0
[ "${1:-}" = "--with-torch" ] && WITH_TORCH=1

echo "=============================================="
echo " 大模型实训 · 环境引导（T0/CPU）"
echo " 模式：$([ $WITH_TORCH -eq 1 ] && echo '含 torch' || echo '轻量档（不含 torch）')"
echo "=============================================="

command -v "$PY" >/dev/null 2>&1 || { echo "❌ 找不到 python3"; exit 1; }
"$PY" -c 'import sys; assert sys.version_info >= (3,10)' || { echo "❌ 需要 Python ≥3.10"; exit 1; }
PV="$("$PY" -c 'import sys;print(f"{sys.version_info.major}.{sys.version_info.minor}")')"
echo "✅ Python: $PV"

# 版本提示：CS336 2026 官方 conftest 需 3.12+
"$PY" - <<'PY' || true
import sys
v = sys.version_info
if v < (3, 12):
    print(f"ℹ️  当前 Python {v.major}.{v.minor} < 3.12：官方 conftest.py 用 PEP 695 语法无法解析，")
    print("   judge.sh 会自动改用【等价轻量 conftest】（保留同一 snapshot 夹具语义），并在日志中如实声明。")
    print("   若想用官方 conftest 原文：升级到 Python 3.12 或 3.13 后重跑本脚本。")
else:
    print(f"✅ Python {v.major}.{v.minor} ≥ 3.12：judge.sh 将使用官方 conftest 原文。")
PY

[ -d "$VENV" ] || { echo "→ 创建虚拟环境"; "$PY" -m venv "$VENV"; }
# shellcheck disable=SC1091
source "$VENV/bin/activate"
python -m pip install --upgrade pip -q

echo "→ 安装轻量依赖（pytest / tiktoken / psutil / numpy / jaxtyping）…"
python -m pip install -q -r "$HERE/requirements.txt"

if [ $WITH_TORCH -eq 1 ]; then
  echo "→ 安装 torch（先试 CPU 专用源，失败则退回 PyPI）…"
  if ! python -m pip install -q torch --index-url https://download.pytorch.org/whl/cpu 2>/dev/null; then
    echo "  ⚠️ CPU 专用源不可达（沙箱网络常见），退回 PyPI（体积较大，约 555MB）"
    python -m pip install -q torch
  fi
else
  echo "ℹ️  跳过 torch（课题01 判分不需要）。课题02 起执行：bash 环境/bootstrap_cpu.sh --with-torch"
fi

echo "→ 自检："
python - <<'PY'
import numpy, pytest, tiktoken, psutil
print(f"   numpy={numpy.__version__}  pytest={pytest.__version__}  tiktoken={tiktoken.__version__}  psutil={psutil.__version__}")
try:
    import torch
    print(f"   torch={torch.__version__}  CUDA={torch.cuda.is_available()}")
except ImportError:
    print("   torch=未安装（课题01 不需要）")
PY

echo
echo "✅ 环境就绪。下一步："
echo "   环境/judge/judge.sh 01          # 判课题01（BPE）"
echo "   环境/judge/judge.sh 01 --quick  # 快速档，频繁自测用"
