#!/usr/bin/env bash
# 判分入口（脚手架区 B4）。用法：
#   环境/judge/judge.sh 01            # 完整判分（课题01 = BPE）
#   环境/judge/judge.sh 01 --quick    # 快速档（频繁自测用）
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV="$HERE/../.venv"

if [ ! -d "$VENV" ]; then
  echo "❌ 环境未就绪。先跑：环境/bootstrap_cpu.sh"
  exit 1
fi
# shellcheck disable=SC1091
source "$VENV/bin/activate"

# tiktoken 离线缓存（避免每次会话都联网下载 GPT-2 词表；不存在则尝试预热，失败不阻断）
export TIKTOKEN_CACHE_DIR="${TIKTOKEN_CACHE_DIR:-$HERE/../tiktoken-cache}"
if [ ! -d "$TIKTOKEN_CACHE_DIR" ] || [ -z "$(ls -A "$TIKTOKEN_CACHE_DIR" 2>/dev/null)" ]; then
  python "$HERE/prefetch_tiktoken.py" >/dev/null 2>&1 || \
    echo "ℹ️  tiktoken 词表预热未完成（网络受限）——涉及 tiktoken 对齐的测试会失败，其余照常"
fi

exec python "$HERE/run_judge.py" "$@"
