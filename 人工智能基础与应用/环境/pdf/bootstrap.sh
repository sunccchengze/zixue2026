#!/usr/bin/env bash
# 讲义 PDF 排版环境 · 一次性准备脚本
#
# 为什么需要这个脚本：本学科的工作环境是**极简容器**，实测初始状态是
#   ✘ 没有 LaTeX（xelatex/pdflatex 全无）
#   ✘ 没有 Chromium / wkhtmltopdf / weasyprint
#   ✘ 没有一个中文字体（fc-list 返回 0 条）
#   ✘ 中国镜像源全部不可达（清华/中科大/阿里/浙大 DNS 不通）
#   ✔ 可以用：PyPI、npm
# 所以走「PyPI 版 typst + npm 版思源字体」这条路：不需要 root，不需要 apt，
# 不需要联网运行——装完一次，之后每次生成 PDF 都是**纯本地编译**。
#
# 产物（全部在 /home/user/opt/，不在学科目录里，不污染仓库）：
#   /home/user/opt/pdfenv/     Python 环境（typst / pypandoc_binary / pymupdf）
#   /home/user/opt/fonts/      字体：思源宋体、思源黑体、Noto Emoji、DejaVu
#
# 注：/home/user/opt 不在 git 仓库内；若沙箱重建，重跑本脚本即可复原。
set -euo pipefail

PYENV=/home/user/opt/pdfenv
FONTS=/home/user/opt/fonts
DL=/home/user/opt/dl
NPM_TMP=/tmp/pdf-fonts

echo "=== ① Python 排版工具链 ==="
if [ ! -x "$PYENV/bin/python" ]; then
  python3 -m venv "$PYENV"
fi
"$PYENV/bin/pip" -q install --upgrade pip
# typst        : 排版引擎（PyPI 预编译，静态链接，无需 LaTeX）
# pypandoc_binary : 备用转换器（本学科最终未采用，因为 pandoc 的数学转写有损；留作对照）
# pymupdf      : 页面渲染/文本抽取，用于自动验收（页数、标题齐备性、预览图）
"$PYENV/bin/pip" -q install typst pypandoc_binary pymupdf fonttools
"$PYENV/bin/python" -c "import typst, pymupdf, fontTools; print('  ✔ typst / pymupdf / fonttools 就绪')"

echo "=== ② 中文字体（取自 npm，无需 GFW 之外的路） ==="
mkdir -p "$FONTS" "$NPM_TMP"
cd "$NPM_TMP"
need=0
for f in NotoSerifSC-Regular.ttf NotoSansSC-Regular.ttf NotoEmoji-Regular.ttf; do
  [ -f "$FONTS/$f" ] || need=1
done
if [ "$need" = "1" ]; then
  npm pack @expo-google-fonts/noto-serif-sc --silent >/dev/null 2>&1 || true
  npm pack @expo-google-fonts/noto-sans-sc  --silent >/dev/null 2>&1 || true
  npm pack @expo-google-fonts/noto-emoji    --silent >/dev/null 2>&1 || true
  for tgz in *.tgz; do tar xzf "$tgz"; done
  cp -f package/400Regular/NotoSerifSC_400Regular.ttf "$FONTS/NotoSerifSC-Regular.ttf"
  cp -f package/700Bold/NotoSerifSC_700Bold.ttf      "$FONTS/NotoSerifSC-Bold.ttf"
  cp -f package/400Regular/NotoSansSC_400Regular.ttf "$FONTS/NotoSansSC-Regular.ttf"
  cp -f package/700Bold/NotoSansSC_700Bold.ttf       "$FONTS/NotoSansSC-Bold.ttf"
  cp -f package/400Regular/NotoEmoji_400Regular.ttf  "$FONTS/NotoEmoji-Regular.ttf"
fi
# 拉丁/等宽兜底（系统若自带就直接拷）
for f in DejaVuSans.ttf DejaVuSansMono.ttf DejaVuSansMono-Bold.ttf; do
  src="/usr/share/fonts/truetype/dejavu/$f"
  [ -f "$FONTS/$f" ] || { [ -f "$src" ] && cp "$src" "$FONTS/"; }
done
ls -1 "$FONTS" | sed 's/^/  ✔ /'

echo "=== ③ 自检（渲染一页中文 + 一条公式 + 一个 emoji）==="
cat > /tmp/font_selftest.typ <<'TYPST'
#set text(font: ("Noto Serif SC", "DejaVu Sans", "Noto Emoji"), size: 12pt)
自检：中文（思源宋体）＋ 数学 $\frac{QK^\top}{\sqrt{d_k}}$ ＋ 符号 →↦∝∈ ＋ emoji 🦙
TYPST
"$PYENV/bin/python" - <<'PY'
import typst
typst.compile("/tmp/font_selftest.typ", output="/tmp/font_selftest.pdf",
              font_paths=["/home/user/opt/fonts"])
print("  ✔ 排版自检通过（/tmp/font_selftest.pdf）")
PY

echo
echo "=== 就绪。生成讲义： ==="
echo "    cd 人工智能基础与应用 && 环境/pdf/生成讲义PDF.sh          # 每讲 + 全书"
echo "    cd 人工智能基础与应用 && 环境/pdf/生成讲义PDF.sh --charter  # 另出章程分册"
