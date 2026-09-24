# 整理笔记 · 《Python 知识手册 V4.1》（查阅型工具书）

> **整理日期**：2026-09-23　**来源**：main 提交 `e9d74e8` 新增于 `未分类/（已压缩）Python知识手册-V4.1.pdf`（769 页）
> **出品**：微信公众号「Python 数据之道」/ 阳哥，V4.1，2022-05-06。部分文章源代码：公众号回复「code」；最新版回复「600」。

---

## 一、定位与使用方式

- **不是系统入门教材**，而是公众号文章的整合册：覆盖 Python 基础、数据分析、数据可视化、项目实践四大块；作者明示"读者最好有一些 Python 的基本功底"。
- 正确用法：**字典式查阅 + 可运行示例跟随**，而非从第一页顺读。
- **版本提醒**：V4.1 成书于 2022 年，pandas / matplotlib / plotly 等库的 API 已有演进；照抄报错时以官方文档为准。

## 二、内容地图（目录 60+ 章，按主题分组）

| 板块 | 章节范围 | 内容 |
|:---|:---:|:---|
| 导读与环境 | 1–6 | 导读；Python 语言简介（起源/历史/特点/缺点）；安装（两种方法）；第一个程序；创建 `.py` 与 `.ipynb`；VS Code 环境配置 |
| 基础数据类型 | 7–9+ | 字符串；List；字典（及后续基础主题） |
| 交互与科学计算 | 中段 | Jupyter Notebook（界面、主题美化、PDF 输出中文支持）；Numpy（ndarray、常用功能、`random` 系列函数）；Pandas（dataframe/series、groupby 等） |
| 可视化 | 约 30–53 | Matplotlib 基础与动态 gif；Seaborn（distplot/jointplot/pairplot/barplot/boxplot/LM plot/heatmap 进阶）；Plotly Express（line/area/scatter/pie/bar/box/violin/marginal/histogram/funnel/parallel/density/polar/imshow/sunburst/gantt/treemap/3D 散点/map/colors）、保存图片、股票三图（面积/蜡烛/OHLC）、疫情动态演示、文本设置；Bokeh 系列（figure、29 种基础图、ColumnDataSource、布局） |
| 拓展与实战 | 54–60+ | Manim 视频制作；财经：Tushare、投资计划表、基金收益/持仓追踪（akshare）、巴菲特持仓读取；项目实战：UFO 数据分析（清洗 → 分组统计 → 可视化全流程） |

## 三、学习建议（对接个人规划"大一学习 Python"）

1. **主线顺序**：ch3 安装 → ch4-5 第一个程序与 `.ipynb` → ch6 VS Code → ch7-9 数据类型 → Jupyter → Numpy → Pandas → Matplotlib；Seaborn/Plotly/Bokeh 按需查阅。
2. **与真实需求绑定**（避免"学完就忘"）：
   - 大物/大化实验数据处理与误差统计 → Numpy + Pandas；
   - 成绩/综测自算与可视化 → Matplotlib；
   - 将来科研数据清洗与出图 → 跟随 ch60 UFO 实战走一遍全流程。
3. **与 MATLAB 分工**：课程数值计算/仿真用 MATLAB（课程要求），数据分析、自动化、爬虫与可视化用 Python；两者语法对照记忆效率更高。
4. **验证标准**（引《学习观》）：每学一个库，用"没见过的数据"做一遍处理作为"未见泛化"自测，而非重复书里示例。
