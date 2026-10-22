# 仓库工具索引

此处保留通用工具与已有仓库级生成脚本；课程工作包内依赖同目录素材的脚本就地保留。

| 用途 | 工具 |
|---|---|
| 文档转换 | `md2docx.py`、`pptx2pdf.py`、`merge_pdf.py` |
| 文档预览/页数 | `docx_preview_pdf.py`、`docx_page_audit.py` |
| 仓库整理验收 | `audit_repository_layout.py`、`test_repository_layout.py` |
| 原有维护回归 | `test_repository_maintenance.py`、`test_presentation_evidence.py` |
| 课件合并验收 | `audit_course_bundles.py` |
| 工程力学作业 | `generate_mechanics_homework_*`、`verify_mechanics_homework_*`、`generate_homework_sheet_docx.py` |
| 物理复习卷 | `generate_physics_midterm_docx*`、`audit_physics_midterm_v4.py`、`patch_*` |
| B305 实验 | `plot_B305_all.py`、`generate_complete_report_B305.py`（路径已改至大学物理实验） |
| 采集归档 | [icourse](icourse/) |
| 同步工具 | `git-sync.py`（历史工具；分支操作须服从当前会话限制，不自动运行） |

整理验收（标准库，无联网）：`python scripts/audit_repository_layout.py`。
这仅验证文件、导航与原件保存，不替代学术内容审查或 Office 实际渲染。
