# 论文精读 · 伴读白皮书 一键入口
#
#   make scan        # 刷新语料统计（承重榜 / 盲区 0 命中），写 corpus/facts/scan-results.md
#   make whitepaper  # 由 docs/ 装配白皮书（讲稿缺失的讲次会公开挂牌「待重建」）
#   make checks      # code/ 每个模块跑一遍，输出 images/selftest-report.txt
#   make verify      # 全项验收（A 引用可回溯 / B 图表号 / C 图片 / D 结构 / E 零 Emoji 图注 / F 自足性）
#   make all         # scan + whitepaper + checks + verify
#   make help        # 看这份清单
#
# 约定：白皮书 md 是**产物**，不要手改；改 docs/lectures/NN.md 后重跑 make whitepaper。

PYTHON ?= python3

.PHONY: all scan whitepaper checks verify clean help

help:
	@grep -E '^#   make ' Makefile | sed 's/^#   //'

scan:
	$(PYTHON) tools/scan_corpus.py

whitepaper:
	$(PYTHON) tools/build_whitepaper.py

checks:
	@mkdir -p images; \
	for f in code/*.py; do echo "--- $$f"; $(PYTHON) "$$f" | tail -4; echo; done > images/selftest-report.txt; \
	tail -20 images/selftest-report.txt

verify:
	$(PYTHON) tools/verify_all.py

all: scan whitepaper checks verify

clean:
	rm -f images/selftest-report.txt
