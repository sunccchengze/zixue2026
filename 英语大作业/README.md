# 英语大作业｜口罩热水处理论文汇报

这是完整的独立作品包，在国际学术交流英语中登记，保留内部相对路径。

## 使用顺序
1. 成品：[Mask-Reuse-Qualification-Review.pptx](Mask-Reuse-Qualification-Review.pptx)（13页，上传原件保留）。
2. [四人协作包](four-person-kit.html)、[汇报方案](presentation-plan.html)、[选文指南](paper-selection-guide.html)。HTML可本地浏览器打开。
3. 讲稿：`roles/P1-setup.md`、`P2-procedure.md`、`P3-filtration.md`、`P4-verdict.md`；现成讲稿的页码分工需要与13页成品再对齐，不把早期12页计划当最终页码。
4. 证据：`papers/` 原论文、提取文本及原论文图；`ppt_images/` 为展示配图，不能冒充实验证据。
5. 词汇：[论文AWL](awl-in-paper.md) 与 `uploads/` 词汇手册/需求截图。

## 复现（离线构建，不覆盖上传稿）

依赖：python-pptx、Pillow、numpy；从仓库根执行 `python 英语大作业/make_deck.py`。
`build_ppt.py` 是渲染库，`animations.py` 是动画库，不是另外两套成品入口。
重建文件输出到 `英语大作业/build/Mask-Reuse-Qualification-Review.pptx`（忽略入库）。
`qa.py` 依赖LibreOffice和pdftoppm；默认检查上传稿，`--harden`会改写输入，请先备份或指向重建稿。

## 内容边界

这是对2020年特定论文的课堂分析，不是当前口罩重复使用或消毒建议。论文没有直接病毒灭活实验、也没有贴合度测试；不能由滤效数据推导普遍安全。P4稿中“works in the field”“proves”应限于原文样本和指标，尤其不能推广为人人适用的医疗建议。
本次核查ZIP/正文与素材完整性，不声称已逐页视觉验收PPT或重新查证所有论文结论。

## 2026-10-06 补查提示

原上传成品保留，不等于内容已通过验收；已发现需修订的表述。详见[逐页/时间点勘误](../维护记录/2026-10-05/第三轮补查与勘误.md)。可编辑源与成品尚未按全部勘误同步修改，不应直接作为已验收稿交付。
