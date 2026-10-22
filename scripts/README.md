# 通用工具与维护命令

这里只保留跨课程工具与全仓验收；课程专用工具不再堆在本目录。

## 日常维护（标准库，无联网）

```bash
python scripts/manage_repository.py refresh  # 生成课程导航/当前版本/实时索引
python scripts/manage_repository.py check    # 只读，检查唯一源与生成结果一致
python scripts/audit_repository_layout.py    # 历史原件、重定位链、导航/索引
python scripts/verify_midterm_mocks.py        # 三科AI卷选定数值/结构检查
python -m unittest discover -s scripts -p 'test_repository*.py' -v
```

`refresh`不生成题解、不替换Office成品、不更改复习完成状态；`check`不会写文件。

## 通用文档工具

- `md2docx.py`、`pptx2pdf.py`、`merge_pdf.py`：转换/合并。
- `docx_preview_pdf.py`、`docx_page_audit.py`：预览与页数检查。
- `generate_homework_sheet_docx.py`：读取任务规格的通用答题纸工具。
- `icourse/`：跨课程采集与归档安全；不自动联网或复用登录态。
- `git-sync.py`：历史同步工具，含soft-reset/恢复逻辑，**不作为默认保存命令自动运行**；按AGENTS手动检查提交和当前分支推送。

## 课程专用工具在哪里

| 用途 | 当前路径 |
|---|---|
| 物理精讲V4的生成、导出、审计 | [知识精讲工具](../大学物理/考试复习/期中/知识精讲/工具/) |
| 工程力学作业生成/验算 | [力学工具](../工程力学/工具/作业制作/) |
| B305报告/作图 | [物理实验工具](../大学物理实验/工具/B305/) |
| 概率论考试题库验算 | [综合题库](../概率论与数理统计/考试复习/综合题库/2026秋/) |
| 英语PPT构建 | [当前版本与复现](../国际学术交流英语/课程大作业/口罩重复使用研究/当前版本.md) |

## 环境

所有目录/登记/AI卷数值检查只需Python 3.10+标准库。完整历史回归与文档制作需另外的Python依赖：

```bash
python -m venv .venv
.venv/bin/pip install -r requirements.txt
```

依赖采用兼容范围而非声称已锁定全环境；每个课程工具仍以脚本头部说明为准。LaTeX、LibreOffice、RapidOCR等为专门任务的额外依赖，本轮没有安装或验证全部工具链。不要为了检查导航就安装它们。
