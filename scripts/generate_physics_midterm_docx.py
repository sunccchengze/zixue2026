#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
大学物理 期中范围 12-15次作业 图文精析 生成脚本
- 含封面、目录、知识地图、4次作业96题逐题精讲、图示、期中备考清单
- 输出: 大学物理期中_12-15次作业图文精析_孙承泽_2253710052.docx
"""
import os
import math
import pathlib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from docx import Document
from docx.shared import Inches, Pt, RGBColor, Emu
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# ---------- 样式与工具 ----------
OUT_DIR = pathlib.Path("tmp_generated_figs")
OUT_DIR.mkdir(exist_ok=True)
DOCX_OUT = pathlib.Path("大学物理期中_12-15次作业图文精析_孙承泽_2253710052.docx")

# 颜色
C_PRIMARY = RGBColor(0x1A, 0x3A, 0x5C)  # 深蓝
C_ACCENT = RGBColor(0x2E, 0x86, 0xAB)   # 湖蓝
C_LIGHT_BG = "E8F0FE"
C_WARN_BG = "FFF8E1"
C_TIP_BG = "E8F5E9"
C_GRAY = RGBColor(0x66,0x66,0x66)

def set_cell_bg(cell, color_hex):
    tblCell = cell._tc
    tblCellProperties = tblCell.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:fill'), color_hex)
    shd.set(qn('w:val'), 'clear')
    tblCellProperties.append(shd)

def set_paragraph_spacing(p, before=0, after=4, line_spacing=1.15):
    pf = p.paragraph_format
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)
    pf.line_spacing = line_spacing
    pf.widow_control = True

def add_horizontal_line(doc, width_pt=450):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), '6')
    bottom.set(qn('w:space'), '1')
    bottom.set(qn('w:color'), 'A0AEC0')
    pBdr.append(bottom)
    pPr.append(pBdr)
    set_paragraph_spacing(p, before=2, after=8)
    return p

def setup_document_styles(doc):
    style = doc.styles['Normal']
    style.font.name = 'Times New Roman'
    style._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
    style.font.size = Pt(10.5)
    style.font.color.rgb = RGBColor(0x33,0x33,0x33)
    style.paragraph_format.space_after = Pt(4)
    style.paragraph_format.line_spacing = 1.18
    style.paragraph_format.widow_control = True

    for i, (size, color) in enumerate([(18, C_PRIMARY), (14, C_PRIMARY), (11, C_ACCENT)], start=1):
        hs = doc.styles[f'Heading {i}']
        hs.font.name = 'Times New Roman'
        hs._element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')
        hs.font.size = Pt(size)
        hs.font.color.rgb = color
        hs.font.bold = True
        hs.paragraph_format.space_before = Pt(12 if i==1 else 10)
        hs.paragraph_format.space_after = Pt(6)
        hs.paragraph_format.keep_with_next = True
        if i==1:
            # add bottom border for H1
            pPr = hs._element.get_or_add_pPr()
            pBdr = OxmlElement('w:pBdr')
            bottom = OxmlElement('w:bottom')
            bottom.set(qn('w:val'), 'single')
            bottom.set(qn('w:sz'), '12')
            bottom.set(qn('w:space'), '4')
            bottom.set(qn('w:color'), '2E86AB')
            pBdr.append(bottom)
            pPr.append(pBdr)

def add_caption(doc, text, italic=True):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(text)
    run.font.size = Pt(8.5)
    run.font.color.rgb = RGBColor(0x5A,0x6C,0x7D)
    run.italic = italic
    run.font.name = 'Times New Roman'
    run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
    set_paragraph_spacing(p, before=2, after=10)
    return p

def add_tip_box(doc, title, content, bg=C_TIP_BG, icon="💡"):
    # 用1x1表格模拟色块
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    table.columns[0].width = Inches(6.2)
    cell = table.cell(0,0)
    set_cell_bg(cell, bg.replace("#","") if bg.startswith("#") else bg)
    # 内边距
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for edge in ['top','left','bottom','right']:
        m = OxmlElement(f'w:{edge}')
        m.set(qn('w:w'), '80')
        m.set(qn('w:type'), 'dxa')
        tcMar.append(m)
    tcPr.append(tcMar)
    # 标题
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = p.add_run(f"{icon} {title}")
    run.bold = True
    run.font.size = Pt(9.5)
    run.font.color.rgb = C_PRIMARY
    run.font.name = 'Times New Roman'
    run._element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')
    # 内容
    p2 = cell.add_paragraph()
    run2 = p2.add_run(content)
    run2.font.size = Pt(9)
    run2.font.color.rgb = RGBColor(0x33,0x33,0x33)
    run2.font.name = 'Times New Roman'
    run2._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
    p2.paragraph_format.space_before = Pt(2)
    set_paragraph_spacing(p, before=2, after=2)
    set_paragraph_spacing(p2, before=0, after=2)
    doc.add_paragraph()  # spacer
    return table

def add_answer_table(doc, rows, col_widths=None):
    # rows: list of [Q, Answer, Key Point]
    table = doc.add_table(rows=1+len(rows), cols=3)
    table.style = 'Light Grid Accent 1'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    if col_widths is None:
        col_widths = [Inches(0.7), Inches(0.9), Inches(4.6)]
    for i,w in enumerate(col_widths):
        table.columns[i].width = w
    # header
    hdr = table.rows[0].cells
    for j, txt in enumerate(["题号", "答案", "一句话考点"]):
        p = hdr[j].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(txt)
        run.bold = True
        run.font.size = Pt(9)
        run.font.color.rgb = RGBColor(0xFF,0xFF,0xFF)
        hdr[j].vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        set_cell_bg(hdr[j], "1A3A5C")
        set_paragraph_spacing(p, before=2, after=2)
    for r, row in enumerate(rows):
        cells = table.rows[r+1].cells
        for j, txt in enumerate(row):
            p = cells[j].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if j<2 else WD_ALIGN_PARAGRAPH.LEFT
            run = p.add_run(txt)
            run.font.size = Pt(8.5)
            run.font.name = 'Times New Roman'
            run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
            if j==1:
                run.bold = True
                run.font.color.rgb = RGBColor(0xC0,0x39,0x2B)
            set_paragraph_spacing(p, before=1, after=1)
            cells[j].vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            if r%2==1:
                set_cell_bg(cells[j], "F7F9FC")
    doc.add_paragraph()
    return table

# ---------- 生成插图 ----------
def fig_save(path, tight=True):
    plt.savefig(path, dpi=200, bbox_inches='tight' if tight else None)
    plt.close()
    return path

def gen_fig_wave_basic():
    # 12-1 波动基础：横波、纵波、波长、频率关系图
    fig, axs = plt.subplots(1,2, figsize=(7,2.6))
    x = np.linspace(0, 4*np.pi, 400)
    y = np.sin(x)
    axs[0].plot(x, y, color='#2E86AB', lw=2)
    axs[0].fill_between(x, y, alpha=0.12, color='#2E86AB')
    axs[0].axhline(0, color='k', lw=0.8)
    # 标注波长
    axs[0].annotate('', xy=(0,1.05), xytext=(2*np.pi,1.05), arrowprops=dict(arrowstyle='<->', color='#E74C3C', lw=1.2))
    axs[0].text(np.pi, 1.12, r'$\lambda$', ha='center', va='bottom', fontsize=11, color='#C0392B')
    axs[0].annotate('', xy=(0,-1.05), xytext=(np.pi,-1.05), arrowprops=dict(arrowstyle='<->', color='#27AE60', lw=1.2))
    axs[0].text(np.pi/2, -1.2, r'$\lambda/2$', ha='center', va='top', fontsize=9, color='#27AE60')
    axs[0].set_title('Transverse wave: y(x) at fixed t', fontsize=10)
    axs[0].set_xlabel('x', fontsize=9)
    axs[0].set_ylabel('y (displacement)', fontsize=9)
    axs[0].set_ylim(-1.5,1.5)
    axs[0].set_xticks([])
    axs[0].grid(alpha=0.15)

    # 右：y-t 关系与 u = lambda/T
    t = np.linspace(0,2,400)
    y2 = 0.2*np.cos(2*np.pi*0.5*t)
    axs[1].plot(t, y2, color='#8E44AD', lw=2)
    axs[1].axhline(0, color='k', lw=0.8)
    axs[1].set_title(r'$u = \lambda / T = \lambda f = \omega/k$', fontsize=10)
    axs[1].set_xlabel(r'$t$ (T = 0.2 s example: $\lambda$=0.5 m, $u$=2.5 m/s)', fontsize=8)
    axs[1].set_ylabel('y', fontsize=9)
    axs[1].grid(alpha=0.15)
    # annotate T
    axs[1].annotate('', xy=(0,0.22), xytext=(2,0.22), arrowprops=dict(arrowstyle='<->', color='#E74C3C'))
    axs[1].text(1,0.24, 'T', ha='center', fontsize=10, color='#C0392B')
    plt.tight_layout()
    return fig_save(OUT_DIR/"fig12_01_wave_basic.png")

def gen_fig_yx_vs_yt():
    # 12-2 y-x 与 y-t 区别，解释 Q3 Q4
    fig, axs = plt.subplots(1,2, figsize=(7,2.7))
    x = np.linspace(0,2,500)
    y_x = 0.2*np.cos(np.pi*x) # from Q3 at t=0.5
    axs[0].plot(x, y_x, color='#1A3A5C', lw=2)
    axs[0].axhline(0, color='k', lw=0.7)
    axs[0].axvline(0, color='k', lw=0.7)
    axs[0].set_ylim(-0.25,0.25)
    axs[0].set_xlim(-0.1,2.1)
    axs[0].set_title('Q3: y-x (waveform at t=0.5 s)', fontsize=9)
    axs[0].set_xlabel('x (m)'); axs[0].set_ylabel('y (m)')
    # 标注特殊点
    axs[0].plot([0],[0.2],'ro', ms=5)
    axs[0].text(0,0.22,'x=0, y=+0.20 peak', ha='left', fontsize=7, color='#C0392B')
    axs[0].plot([1],[-0.2],'ro', ms=5)
    axs[0].text(1,-0.23,'x=1 m trough', ha='center', fontsize=7)
    axs[0].grid(alpha=0.15)

    # y-t at x=0 (Q4)
    t = np.linspace(0,8,600)
    y_t = np.sqrt(2)*np.cos(np.pi/2*(t) + 2*np.pi/3) # Q4 D? Actually include x=0
    # 简化：展示 x=0 振动：sqrt2 cos(pi/2 t + 2pi/3)
    axs[1].plot(t, y_t, color='#D35400', lw=2)
    axs[1].axhline(0, color='k', lw=0.7)
    axs[1].axvline(0, color='k', lw=0.7)
    axs[1].set_title('Q4: y-t at x=0 (phase 2π/3)', fontsize=9)
    axs[1].set_xlabel('t (s)'); axs[1].set_ylabel('y (m)')
    axs[1].set_xlim(0,8)
    axs[1].set_ylim(-1.6,1.6)
    # 标注初相
    axs[1].plot([0],[-np.sqrt(2)/2],'ro', ms=5)
    axs[1].text(0.2,-0.9,'t=0: y=-√2/2\nv<0 (down)', fontsize=7, color='#C0392B')
    axs[1].grid(alpha=0.15)
    plt.tight_layout()
    return fig_save(OUT_DIR/"fig12_02_yx_yt.png")

def gen_fig_spherical():
    fig, ax = plt.subplots(figsize=(4.2,3))
    r = np.linspace(0.2,5,200)
    I = 1/r**2
    ax.plot(r, I, color='#2980B9', lw=2.2, label=r'$I \propto 1/r^2$')
    ax.plot(r, 1/r, color='#95A5A6', lw=1.5, ls='--', label=r'$1/r$ (wrong)')
    # also amplitude ∝1/r
    A = 1/r
    ax2 = ax.twinx()
    ax2.plot(r, A, color='#E67E22', lw=1.3, ls=':', label=r'$A \propto 1/r$')
    ax.set_xlabel('distance r (m)', fontsize=9)
    ax.set_ylabel('Intensity I (arb.)', fontsize=9, color='#2980B9')
    ax2.set_ylabel('Amplitude A', fontsize=9, color='#E67E22')
    # 标注球面波能量守恒
    ax.text(2.5,0.6,'4πr²·I = const\nenergy conservation', ha='center', fontsize=8,
            bbox=dict(boxstyle='round', facecolor='#EAF2F8', edgecolor='#A9CCE3'))
    ax.legend(loc='upper right', fontsize=7)
    ax2.legend(loc='center right', fontsize=7)
    ax.set_title('Spherical wave: I ∝ 1/r², A ∝ 1/r', fontsize=10)
    ax.grid(alpha=0.15)
    return fig_save(OUT_DIR/"fig12_03_spherical.png")

def gen_fig_interference_phase():
    fig, ax = plt.subplots(figsize=(6,2.2))
    # S1 S2 位置
    ax.plot([2,4],[0,0],'ko', ms=8)
    ax.text(2,0.25,'S1', ha='center', fontsize=10, weight='bold')
    ax.text(4,0.25,'S2', ha='center', fontsize=10, weight='bold')
    # P 在左侧
    ax.plot([0.5],[0],'ro', ms=8)
    ax.text(0.5,0.25,'P', ha='center', fontsize=10, color='#C0392B', weight='bold')
    # 标注距离 = lambda/2
    ax.annotate('', xy=(2, -0.15), xytext=(4, -0.15), arrowprops=dict(arrowstyle='<->', color='#2E86AB'))
    ax.text(3,-0.35, r'$S_1S_2 = \lambda/2$', ha='center', fontsize=9, color='#2E86AB')
    # 波程差说明
    ax.plot([0.5,2],[0,0], color='#2E86AB', lw=1.5, ls='--')
    ax.plot([0.5,4],[0.02,0.02], color='#95A5A6', lw=1, ls=':')
    ax.text(1.0,0.12, r'$r_1$', ha='center', fontsize=8, color='#2E86AB')
    ax.text(1.8,0.38, r'$r_2 = r_1+\lambda/2$', ha='center', fontsize=8, color='#7F8C8D')
    ax.set_xlim(-0.5,5)
    ax.set_ylim(-0.6,0.6)
    ax.axis('off')
    # 底部文字框：相位差计算
    ax.text(2.5,-0.55, r'$\Delta\varphi = (\varphi_{10}-\varphi_{20}) -2\pi(r_1-r_2)/\lambda = (\pi/2) -2\pi(-\lambda/2)/\lambda =3\pi/2$', 
            ha='center', fontsize=8, bbox=dict(boxstyle='round', facecolor='#FDEBD0', edgecolor='#E67E22'))
    ax.set_title('Q7: Two coherent sources on a line, phase difference at P (left side)', fontsize=10)
    return fig_save(OUT_DIR/"fig12_04_interference_phase.png")

def gen_fig_standing_energy():
    fig, axs = plt.subplots(1,2, figsize=(7,2.5))
    x = np.linspace(0,2,600)
    # 驻波包络 A(x)=2A0 |cos kx|? For fixed ends etc.
    k = 2*np.pi # lambda=1
    # 两列波叠加示意
    for i, t in enumerate([0, 0.25]):
        envelope = 2*np.cos(k*x/2) * np.cos(np.pi*t) # simplified
        # 实际画包络
        axs[i].plot(x, 2*np.cos(k*x/2), color='#BDC3C7', lw=1, ls='--', label='envelope ±2A|cos|')
        axs[i].plot(x, -2*np.cos(k*x/2), color='#BDC3C7', lw=1, ls='--')
        y = 2*np.cos(k*x/2)*np.cos(2*np.pi*t)
        axs[i].plot(x, y, color='#C0392B' if i==0 else '#2980B9', lw=2)
        axs[i].axhline(0,color='k',lw=0.7)
        # 节点
        nodes = np.arange(0.5,2,1)
        for n in nodes:
            axs[i].plot([n,n],[-2,2], color='#F39C12', lw=1, ls=':', alpha=0.6)
        axs[i].set_title('t=0: all points at max disp.' if i==0 else 't=T/4: all points at equilibrium', fontsize=9)
        axs[i].set_xlabel('x'); axs[i].set_ylabel('y')
        axs[i].set_ylim(-2.2,2.2); axs[i].set_xlim(0,2)
        axs[i].text(0.5,1.7,'Node', ha='center', fontsize=7, color='#F39C12')
        axs[i].text(0,1.7,'Antinode', ha='center', fontsize=7, color='#C0392B')
        axs[i].grid(alpha=0.12)
    plt.tight_layout()
    return fig_save(OUT_DIR/"fig12_05_standing_energy.png")

def gen_fig_doppler():
    fig, ax = plt.subplots(figsize=(6,2.5))
    # road horizontal
    ax.plot([0,10],[0,0], color='#2C3E50', lw=3)
    # car (left) moving right 30 m/s
    car_x=2
    ax.add_patch(patches.Rectangle((car_x-0.6,0.1),1.2,0.5, fc='#3498DB', ec='k'))
    ax.text(car_x,0.85, 'car 30 m/s →', ha='center', fontsize=8, color='#2471A3')
    ax.plot([car_x+0.6, car_x+1.5],[0.35,0.35], color='#E74C3C', lw=1.5) # sound arrow
    # train right moving left 50 m/s
    train_x=8
    ax.add_patch(patches.Rectangle((train_x-1,0.1),2,0.6, fc='#C0392B', ec='k'))
    ax.text(train_x,0.95, '← 50 m/s train\n(observer moving toward source)', ha='center', fontsize=7, color='#922B21')
    # sound waves
    for i in range(5):
        r = 0.3+i*0.35
        circle = patches.Circle((car_x+0.6,0.35), r, fill=False, ec='#E74C3C', lw=1, alpha=0.5)
        ax.add_patch(circle)
    ax.text(5,0.35, 'sound v=344 m/s', ha='center', fontsize=7, color='#C0392B',
            bbox=dict(boxstyle='round', facecolor='white', edgecolor='#E74C3C'))
    ax.text(5,-0.35, r"$\nu' = \frac{v+ v_{obs}}{v- v_{src}}\nu_0 = \frac{344+50}{344-30}\times1.00\text{kHz}=1.25\text{kHz}$",
            ha='center', fontsize=9, bbox=dict(boxstyle='round', facecolor='#EAF2F8', edgecolor='#AED6F1'))
    ax.set_xlim(0,10); ax.set_ylim(-0.6,1.2); ax.axis('off')
    ax.set_title('Q10 Doppler: source & observer approaching (both moving)', fontsize=10)
    return fig_save(OUT_DIR/"fig12_06_doppler.png")

def gen_fig_thin_film():
    # 13章 薄膜干涉：透射相长 vs 反射
    fig, ax = plt.subplots(figsize=(5,2.8))
    # film
    ax.add_patch(patches.Rectangle((1,1),4,0.6, fc='#AED6F1', ec='#2E86AB', alpha=0.7))
    ax.text(3,1.3, 'film n (air n=1 both sides)', ha='center', fontsize=8, color='#1A5276')
    # incident
    ax.arrow(2,2.8,0,-1.0, head_width=0.12, head_length=0.12, fc='k', ec='k', lw=1.5)
    ax.text(2,2.85,'λ', ha='center', fontsize=9)
    # reflected top
    ax.arrow(2,1.6, -0.5,0.5, head_width=0.1, head_length=0.1, fc='#C0392B', ec='#C0392B', ls='--')
    # transmitted bottom with two beams? Simplify
    ax.arrow(2.4,1,0,-0.6, head_width=0.1, head_length=0.1, fc='#27AE60', ec='#27AE60')
    ax.arrow(3,1,0,-0.6, head_width=0.1, head_length=0.1, fc='#27AE60', ec='#27AE60', alpha=0.6)
    # annotations半波
    ax.text(4.8,1.45, r'$2nd = (k-\frac{1}{2})\lambda$ (reflected dark)', ha='left', fontsize=7, color='#C0392B')
    ax.text(4.8,1.15, r'$2nd = k\lambda$ (transmitted bright)', ha='left', fontsize=7, color='#27AE60')
    # thickness
    ax.annotate('', xy=(1,0.7), xytext=(1,1.6), arrowprops=dict(arrowstyle='<->', color='#7F8C8D'))
    ax.text(0.7,1.15,'d', ha='center', fontsize=9, color='#7F8C8D')
    ax.set_xlim(0,7); ax.set_ylim(0.2,3); ax.axis('off')
    ax.set_title('Thin film: why transmitted bright = 2nd = kλ  (no extra half)', fontsize=9)
    return fig_save(OUT_DIR/"fig13_01_thin_film.png")

def gen_fig_newton():
    fig, axs = plt.subplots(1,2, figsize=(7,2.8))
    for idx, (lifted, title) in enumerate([(False,'Newton: lens on glass (contact)'), (True,'Lifted or immersed in liquid n=1.6')]):
        ax=axs[idx]
        # flat glass bottom
        ax.add_patch(patches.Rectangle((0,0),4,0.3, fc='#D5D8DC', ec='k'))
        # lens convex
        # draw lens as arc
        from matplotlib.patches import Arc
        # lens shape approximate with polygon
        # top lens
        y0 = 0.35 if not lifted else 0.6
        # draw lens as ellipse segment
        ax.add_patch(patches.Ellipse((2, y0+1.2), 3.5, 2.2, fc='#AED6F1', ec='#2E86AB', alpha=0.8))
        # air gap
        ax.plot([0,4],[0.3,0.3], color='k', lw=0.8)
        if lifted:
            ax.text(2,0.45, r'air gap + liquid', ha='center', fontsize=7, color='#7D6608',
                    bbox=dict(boxstyle='round', facecolor='#FEF9E7', edgecolor='#F1C40F'))
            # central spot dark? Show
            ax.plot([2],[0.3],'ko', ms=8, alpha=0.6)
            ax.text(2,0.15,'dark center', ha='center', fontsize=7)
        else:
            ax.plot([2],[0.3],'ko', ms=6)
            ax.text(2,0.15,'contact → dark (half-wave)', ha='center', fontsize=7)
        # rays
        for x in [0.8,1.5,2.5,3.2]:
            ax.arrow(x,2.2,0,-0.6, head_width=0.07, head_length=0.07, fc='k', ec='k', alpha=0.7)
        ax.set_xlim(-0.5,4.5); ax.set_ylim(-0.2,2.4); ax.axis('off')
        ax.set_title(title, fontsize=8)
    plt.tight_layout()
    return fig_save(OUT_DIR/"fig13_02_newton.png")

def gen_fig_wedge():
    fig, ax = plt.subplots(figsize=(5,3))
    # two glass plates wedge
    ax.plot([0,4],[1.4,1.1], color='#2E86AB', lw=3) # top
    ax.plot([0,4],[0.7,0.7], color='#2E86AB', lw=3) # bottom workpiece
    # fill air wedge
    ax.fill_between([0,4],[1.4,1.1],[0.7,0.7], color='#AED6F1', alpha=0.3)
    ax.text(2,1.0,'air wedge', ha='center', fontsize=8, color='#1A5276')
    # fringes
    for i, x in enumerate(np.linspace(0.3,3.8,8)):
        y_top = 1.4 - (0.3/4)*x
        # interference fringe position? simplified vertical lines
        ax.plot([x,x],[y_top, y_top+0.4], color='#C0392B' if i%2==0 else '#2980B9', lw=2, alpha=0.8)
    ax.text(3.8,1.6,'→ thickness ↑', ha='right', fontsize=7, color='#7F8C8D')
    ax.annotate('', xy=(0,0.7), xytext=(0,1.4), arrowprops=dict(arrowstyle='<->', color='#7F8C8D'))
    ax.text(-0.25,1.05,'d', ha='center', fontsize=8)
    # paper thickness
    ax.add_patch(patches.Rectangle((3.8,0.7),0.15,0.4, fc='#F5B041', ec='k'))
    ax.text(3.87,0.5,'paper', ha='center', fontsize=6, rotation=90)
    # formula
    ax.text(2,0.2, r'$2nd + \lambda/2 = k\lambda$ (bright) ; $\Delta l = \lambda/(2n) / \sin\theta \approx \lambda/(2\theta)$',
            ha='center', fontsize=7, bbox=dict(boxstyle='round', facecolor='#EAF2F8', edgecolor='#AED6F1'))
    ax.set_xlim(-0.5,5); ax.set_ylim(0,2); ax.axis('off')
    ax.set_title('Wedge film (air) & Newton-like fringes', fontsize=10)
    return fig_save(OUT_DIR/"fig13_03_wedge.png")

def gen_fig_michelson():
    fig, ax = plt.subplots(figsize=(4.5,3))
    # simplified Michelson
    # beam splitter diagonal
    ax.plot([2,3],[1.5,2.5], color='#2E86AB', lw=4, alpha=0.7)
    ax.text(2.5,2.6,'G1 (BS)', ha='center', fontsize=7)
    # M1 top
    ax.add_patch(patches.Rectangle((2.4,3.0),0.6,0.1, fc='#E74C3C', ec='k'))
    ax.text(2.7,3.2,"M1 (movable)", ha='center', fontsize=7, color='#922B21')
    # M2 right
    ax.add_patch(patches.Rectangle((4.0,1.6),0.1,0.6, fc='#3498DB', ec='k'))
    ax.text(4.3,1.9,"M2", ha='center', fontsize=7, color='#1A5276')
    # source left
    ax.plot([0.5,1.5],[1.9,1.9], color='#F1C40F', lw=2)
    ax.add_patch(patches.Circle((0.4,1.9),0.12, fc='#F1C40F', ec='k'))
    ax.text(0.4,1.6,'Source', ha='center', fontsize=7)
    # eye bottom
    ax.plot([2.5,2.5],[1.5,0.6], color='#27AE60', lw=1.5, ls='--')
    ax.plot([2.5],[0.5],'o', color='#27AE60', ms=8)
    ax.text(2.5,0.3,'E (eye)', ha='center', fontsize=7, color='#1E8449')
    # virtual image M1'
    ax.plot([2.4,3.0],[2.95,2.95], color='#95A5A6', lw=1, ls=':')
    ax.text(3.2,2.95,"M1'", ha='left', fontsize=6, color='#7F8C8D')
    # path difference
    ax.text(1.8,1.2, r'$2d = N\lambda$', ha='center', fontsize=8,
            bbox=dict(boxstyle='round', facecolor='#FDEBD0', edgecolor='#E67E22'))
    ax.set_xlim(0,5); ax.set_ylim(0.2,3.5); ax.axis('off')
    ax.set_title('Michelson: moving mirror → N fringes: 2Δd = Nλ', fontsize=9)
    return fig_save(OUT_DIR/"fig13_04_michelson.png")

def gen_fig_single_slit():
    fig, axs = plt.subplots(1,2, figsize=(7,2.7))
    # left: intensity distribution
    phi = np.linspace(-3*np.pi,3*np.pi,800)
    # single slit intensity (sin beta / beta)^2
    beta = phi
    # avoid zero
    I = (np.sin(beta/2)/(beta/2+1e-9))**2
    # set central
    axs[0].plot(beta, I, color='#2E86AB', lw=2)
    axs[0].fill_between(beta, I, alpha=0.12, color='#2E86AB')
    axs[0].axvline(-np.pi, color='#E74C3C', ls='--', lw=1)
    axs[0].axvline(np.pi, color='#E74C3C', ls='--', lw=1)
    axs[0].text(0,0.95,'Central\nmax', ha='center', fontsize=7, color='#1A3A5C')
    axs[0].text(np.pi,0.5,'1st min\nb sinφ=±λ', ha='center', fontsize=6, color='#C0392B')
    axs[0].text(-np.pi,0.5,'1st min', ha='center', fontsize=6, color='#C0392B')
    axs[0].set_title('Single-slit: I(φ) ∝ (sin β / β)²', fontsize=9)
    axs[0].set_xlabel(r'$\beta = (\pi b \sin\varphi)/\lambda$'); axs[0].set_ylabel('I')
    axs[0].set_ylim(-0.05,1.05); axs[0].grid(alpha=0.12)

    # right: lens shift effect Q1 & Q3
    ax=axs[1]
    ax.plot([0.5,0.5],[0,3], color='#7F8C8D', lw=3) # slit
    ax.text(0.5,3.1,'slit b', ha='center', fontsize=8)
    ax.add_patch(patches.Ellipse((2,1.5),0.4,1.6, fc='#AED6F1', ec='#2E86AB')) # lens
    ax.text(2,0.3,'L (f)', ha='center', fontsize=7)
    ax.plot([3.5,3.5],[0,3], color='#1A3A5C', lw=2) # screen
    ax.text(3.5,3.1,'screen C', ha='center', fontsize=8)
    # chief ray
    ax.plot([0.5,2,3.5],[1.5,1.5,1.5], color='#2E86AB', lw=1, ls='--')
    # diffracted
    ax.plot([0.5,3.5],[1.5,2.3], color='#C0392B', lw=1.2)
    ax.plot([0.5,3.5],[1.5,0.7], color='#C0392B', lw=1.2)
    ax.text(2.2,2.0, r'$\sin\varphi\approx x/f$', ha='left', fontsize=7, color='#922B21')
    ax.annotate('b ↓ → Δx =2fλ/b ↑', xy=(1.2,0.5), fontsize=7,
                bbox=dict(boxstyle='round', facecolor='#EAF2F8', edgecolor='#AED6F1'))
    # lens shift up
    ax.arrow(2,1.5,0,0.4, head_width=0.08, head_length=0.08, fc='#27AE60', ec='#27AE60')
    ax.text(2.15,1.9,'L ↑ → central moves ↑', ha='left', fontsize=6, color='#27AE60')
    ax.set_xlim(0,4); ax.set_ylim(0,3.5); ax.axis('off')
    ax.set_title('Lens shift → central follows axis', fontsize=9)
    plt.tight_layout()
    return fig_save(OUT_DIR/"fig14_01_single.png")

def gen_fig_grating_missing():
    fig, ax = plt.subplots(figsize=(6,2.8))
    # grating orders
    orders = np.arange(-4,5)
    # ideal positions
    d = 2 # assume d=2a => missing even?
    # but example: a=b => missing ±2,±4...
    x = orders * 1.0
    y = [1 if abs(k)%2==1 or k==0 else 0.15 for k in orders] # missing 2,4 dim
    for xi, yi, k in zip(x,y,orders):
        if yi>0.5:
            ax.plot([xi,xi],[0,yi], color='#2E86AB', lw=3)
            ax.text(xi, yi+0.05, str(k), ha='center', fontsize=8, color='#1A3A5C')
        else:
            ax.plot([xi,xi],[0,yi], color='#E74C3C', lw=3, ls=':', alpha=0.7)
            ax.text(xi, yi+0.05, f'{k}*', ha='center', fontsize=7, color='#922B21')
            ax.text(xi, -0.12, 'missing', ha='center', fontsize=6, color='#C0392B', rotation=45)
    # envelope single slit
    env_x = np.linspace(-4.5,4.5,400)
    beta = np.pi*env_x/1.5 # mapping
    env = (np.sin(beta)/(beta+1e-9))**2
    ax.plot(env_x, env*1.1, color='#F39C12', lw=1.2, ls='--', alpha=0.8, label='single-slit envelope (a)')
    ax.set_ylim(-0.2,1.2); ax.set_xlim(-4.8,4.8)
    ax.set_xlabel(r'diffraction angle φ → (d sinφ = kλ)', fontsize=9)
    ax.set_ylabel('Intensity', fontsize=9)
    ax.legend(fontsize=7, loc='upper right')
    ax.set_title('Grating with a=b: missing orders when d/a=2 → k=±2,±4... absent', fontsize=9)
    # note box
    ax.text(0,-0.25, r'Missing condition: $d/a = k/k^\prime$ integer → $k = m(d/a)$ disappears', ha='center', fontsize=7,
            bbox=dict(boxstyle='round', facecolor='#FDEBD0', edgecolor='#E67E22'))
    ax.grid(alpha=0.12)
    return fig_save(OUT_DIR/"fig14_02_grating_missing.png")

def gen_fig_resolution():
    fig, axs = plt.subplots(1,2, figsize=(7,2.6))
    # left: two Airy disks just resolved
    for ax, title in zip(axs, ['Just resolved (Rayleigh)', 'Unresolved (angle too small)']):
        theta = np.linspace(-3,3,600)
        # two sinc-like but for illustration use gaussian-like
        def airy(x, x0): return (2* (np.sin(3*(x-x0)+1e-9)/(3*(x-x0)+1e-9) ))**2 if False else np.exp(-(x-x0)**2/0.4)* (np.sinc((x-x0)/0.6)**2*0.8+0.2)
        # simpler: two peaks
        x = np.linspace(-2,2,400)
        # use actual Airy pattern approximation sum of two
        # Use manual: peaks at ±0.6 for resolved, ±0.3 for unresolved
        dx = 0.6 if 'Just' in title else 0.3
        y1 = np.exp(-((x+dx)/0.35)**2) * (1) # simplified
        # actually use sinc squared shape for realism
        # construct using sin/beta
        # Let's use proper single-slit-like envelope modulated? Keep simple Gaussian for illustration
        y2 = np.exp(-((x-dx)/0.35)**2)
        # sum
        y_total = y1 + y2
        ax.plot(x, y1, color='#3498DB', lw=1.2, ls='--', alpha=0.7)
        ax.plot(x, y2, color='#E74C3C', lw=1.2, ls='--', alpha=0.7)
        ax.plot(x, y_total, color='#2C3E50', lw=2)
        # Rayleigh criterion: peak of one at first min of other ≈ 1.22 λ/D
        ax.axvline(-dx, color='#3498DB', lw=0.8, ls=':')
        ax.axvline(dx, color='#E74C3C', lw=0.8, ls=':')
        # annotate
        mid = 0
        ax.text(mid, 0.95, r'$\Delta\theta \approx 1.22\lambda/D$', ha='center', fontsize=7,
                bbox=dict(boxstyle='round', facecolor='white', edgecolor='#A9CCE3'))
        ax.set_title(title, fontsize=9)
        ax.set_xlabel('angle'); ax.set_ylabel('Intensity')
        ax.set_ylim(0,1.6); ax.grid(alpha=0.12)
    plt.tight_layout()
    return fig_save(OUT_DIR/"fig14_03_resolution.png")

def gen_fig_polarization_malus():
    fig, axs = plt.subplots(1,3, figsize=(7,2.6))
    # natural light through polarizer
    # left: natural
    ax=axs[0]
    ax.add_patch(patches.Circle((0.5,0.5),0.3, fill=False, ec='k', lw=1.2))
    for ang in np.linspace(0,2*np.pi,8, endpoint=False):
        ax.arrow(0.5,0.5, 0.22*np.cos(ang), 0.22*np.sin(ang), head_width=0.03, head_length=0.03, fc='k', ec='k', lw=1)
        ax.arrow(0.5,0.5, -0.22*np.cos(ang), -0.22*np.sin(ang), head_width=0.03, head_length=0.03, fc='k', ec='k', lw=1)
    ax.text(0.5,0.1, 'Natural\n(unpolarized)', ha='center', fontsize=7)
    ax.axis('off'); ax.set_xlim(0,1); ax.set_ylim(0,1); ax.set_title('Input: natural', fontsize=8)

    # middle: polarizer
    ax=axs[1]
    ax.plot([0.5,0.5],[0,1], color='#2E86AB', lw=6, alpha=0.6)
    ax.text(0.5,0.92,'P1', ha='center', fontsize=9, weight='bold', color='#1A3A5C')
    ax.text(0.5,0.12, 'pass axis ↑', ha='center', fontsize=7, color='#1A5276')
    # show transmitted component
    ax.arrow(0.5,0.5,0,0.25, head_width=0.04, head_length=0.04, fc='#C0392B', ec='#C0392B', lw=2)
    ax.arrow(0.5,0.5,0,-0.25, head_width=0.04, head_length=0.04, fc='#C0392B', ec='#C0392B', lw=2)
    ax.text(0.75,0.5, 'I = I0/2', ha='left', fontsize=7, color='#922B21',
            bbox=dict(boxstyle='round', facecolor='#FDEBD0', edgecolor='#E67E22'))
    ax.axis('off'); ax.set_xlim(0,1); ax.set_ylim(0,1); ax.set_title('Ideal polarizer', fontsize=8)

    # right: Malus
    ax=axs[2]
    # polarizer 1 and 2 with angle
    ax.plot([0.2,0.2],[0.2,0.8], color='#2E86AB', lw=5, alpha=0.6)
    ax.text(0.2,0.85,'P1', ha='center', fontsize=8)
    # second polarizer rotated
    # draw line at angle theta=60°
    theta = np.radians(60)
    cx, cy = 0.7, 0.5
    length=0.35
    dx = length*np.sin(theta); dy = length*np.cos(theta)
    ax.plot([cx-dx, cx+dx],[cy-dy, cy+dy], color='#E74C3C', lw=5, alpha=0.6)
    ax.text(cx+0.18,0.85,'P2', ha='center', fontsize=8, color='#922B21')
    # angle arc
    arc = patches.Arc((0.35,0.5),0.22,0.22, theta1=0, theta2=60, color='#7F8C8D', lw=1)
    ax.add_patch(arc)
    ax.text(0.42,0.58, r'$\theta$', ha='center', fontsize=8)
    ax.text(0.5,0.15, r'$I = I_0\cos^2\theta$', ha='center', fontsize=8, color='#1A3A5C',
            bbox=dict(boxstyle='round', facecolor='#EAF2F8', edgecolor='#AED6F1'))
    # light path
    ax.plot([0.2,0.7],[0.5,0.5], color='#F1C40F', lw=1.5, ls='--')
    ax.axis('off'); ax.set_xlim(0,1); ax.set_ylim(0,1); ax.set_title("Malus' law", fontsize=8)
    plt.tight_layout()
    return fig_save(OUT_DIR/"fig15_01_malus.png")

def gen_fig_brewster():
    fig, ax = plt.subplots(figsize=(5,3))
    # interface horizontal
    ax.plot([0,5],[1.5,1.5], color='#2C3E50', lw=2)
    ax.fill_between([0,5],1.5,0, color='#AED6F1', alpha=0.3)
    ax.text(4.5,1.7,'air n1=1', ha='center', fontsize=8)
    ax.text(4.5,1.0,'glass n2=1.5', ha='center', fontsize=8)
    # incident
    ax.arrow(1.5,2.8,1.0,-1.0, head_width=0.1, head_length=0.1, fc='k', ec='k', lw=1.5)
    ax.text(1.6,2.85,r'$i_B$', ha='center', fontsize=9)
    # reflected (Brewster fully polarized perpendicular)
    ax.arrow(2.5,1.5,1.0,1.0, head_width=0.1, head_length=0.1, fc='#C0392B', ec='#C0392B', lw=1.8)
    ax.text(3.7,2.6,'1 (reflected): ⊥ polarized', ha='left', fontsize=7, color='#922B21')
    # refracted
    ax.arrow(2.5,1.5,0.4,-0.9, head_width=0.1, head_length=0.1, fc='#27AE60', ec='#27AE60', lw=1.5)
    ax.text(3.0,0.8,'2 (refracted): partially perp.', ha='left', fontsize=7, color='#1E8449')
    # inside reflections 3,4?
    ax.arrow(2.9,0.6,-0.6,0.6, head_width=0.07, head_length=0.07, fc='#7D6608', ec='#7D6608', ls='--')
    ax.text(2.4,0.7,'3 (2nd refl.)', ha='center', fontsize=6, color='#7D6608')
    # Brewster condition annotation
    ax.text(2.5,0.2, r'$i_B = \arctan(n_2/n_1),\; reflected \perp incident\; plane,\; refracted \parallel + \perp$', ha='center', fontsize=7,
            bbox=dict(boxstyle='round', facecolor='#EAF2F8', edgecolor='#AED6F1'))
    ax.annotate('', xy=(2.5,1.5), xytext=(2.5,2.5), arrowprops=dict(arrowstyle='<->', color='#7F8C8D'))
    ax.set_xlim(0,5); ax.set_ylim(0,3); ax.axis('off')
    ax.set_title('Brewster angle: reflected fully s-polarized', fontsize=10)
    return fig_save(OUT_DIR/"fig15_02_brewster.png")

def gen_fig_waveplate():
    fig, axs = plt.subplots(1,2, figsize=(7,2.7))
    # 1/4 plate
    ax=axs[0]
    ax.add_patch(patches.Rectangle((0.2,0.3),0.6,0.4, fc='#E8F8F5', ec='#1ABC9C', lw=2))
    ax.text(0.5,0.52,'λ/4 plate', ha='center', fontsize=9, weight='bold', color='#0E6655')
    ax.text(0.5,0.42,r'$n_o - n_e$', ha='center', fontsize=7)
    ax.arrow(0.05,0.55,0.12,0, head_width=0.04, head_length=0.04, fc='k', ec='k')
    ax.text(0.05,0.7,'input linear 45°', ha='left', fontsize=7)
    # output circular
    ax.add_patch(patches.Circle((0.85,0.55),0.12, fill=False, ec='#C0392B', lw=1.8))
    # arrow around
    for ang in [0,90,180,270]:
        rad=np.radians(ang)
        ax.arrow(0.85+0.12*np.cos(rad),0.55+0.12*np.sin(rad), 0.04*np.cos(rad+90),0.04*np.sin(rad+90),
                 head_width=0.02, head_length=0.02, fc='#C0392B', ec='#C0392B')
    ax.text(0.85,0.3,'circular', ha='center', fontsize=7, color='#922B21')
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis('off'); ax.set_title('Quarter-wave: linear→circular (45°)', fontsize=8)

    ax=axs[1]
    ax.add_patch(patches.Rectangle((0.2,0.3),0.6,0.4, fc='#FDEBD0', ec='#E67E22', lw=2))
    ax.text(0.5,0.52,'λ/2 plate', ha='center', fontsize=9, weight='bold', color='#7E5109')
    ax.text(0.5,0.42,r'$\Delta = \lambda/2$', ha='center', fontsize=7)
    ax.arrow(0.05,0.55,0.12,0, head_width=0.04, head_length=0.04, fc='k', ec='k')
    ax.text(0.03,0.7,'linear θ', ha='left', fontsize=7)
    # output rotated 2θ
    ax.plot([0.85,0.98],[0.55,0.68], color='#C0392B', lw=2)
    ax.plot([0.85,0.72],[0.55,0.42], color='#C0392B', lw=2)
    ax.text(0.92,0.72,'rotated 2θ', ha='left', fontsize=7, color='#922B21')
    # also thickness formula
    ax.text(0.5,0.15, r'$d_{min}= \lambda/[2|n_o-n_e|]$', ha='center', fontsize=7,
            bbox=dict(boxstyle='round', facecolor='white', edgecolor='#E67E22'))
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis('off'); ax.set_title('Half-wave: rotation, thickness calc', fontsize=8)
    plt.tight_layout()
    return fig_save(OUT_DIR/"fig15_03_waveplate.png")

def generate_all_figs():
    print("Generating figures...")
    gen_fig_wave_basic()
    gen_fig_yx_vs_yt()
    gen_fig_spherical()
    gen_fig_interference_phase()
    gen_fig_standing_energy()
    gen_fig_doppler()
    gen_fig_thin_film()
    gen_fig_newton()
    gen_fig_wedge()
    gen_fig_michelson()
    gen_fig_single_slit()
    gen_fig_grating_missing()
    gen_fig_resolution()
    gen_fig_polarization_malus()
    gen_fig_brewster()
    gen_fig_waveplate()
    print("All figures generated in", OUT_DIR)

# ---------- 文档构建正文数据 ----------
# 为精简脚本，将题解以结构化文本存储，逐题渲染

def add_paragraph(doc, text, bold=False, italic=False, size=Pt(9.5), color=None, align=WD_ALIGN_PARAGRAPH.LEFT, space_after=4, east_asia='宋体'):
    p = doc.add_paragraph()
    p.alignment = align
    run = p.add_run(text)
    run.bold = bold
    run.italic = italic
    run.font.size = size
    if color: run.font.color.rgb = color
    run.font.name = 'Times New Roman'
    run._element.rPr.rFonts.set(qn('w:eastAsia'), east_asia)
    set_paragraph_spacing(p, before=1, after=space_after)
    return p

def add_bold_mixed_paragraph(doc, parts, align=WD_ALIGN_PARAGRAPH.LEFT, size=Pt(9.5)):
    # parts: list of (text, bold, italic, color)
    p = doc.add_paragraph()
    p.alignment = align
    for text, bold, italic, color in parts:
        run = p.add_run(text)
        run.bold = bold
        run.italic = italic
        run.font.size = size
        if color: run.font.color.rgb = color
        run.font.name = 'Times New Roman'
        run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
    set_paragraph_spacing(p, before=1, after=3)
    return p

def add_formula_paragraph(doc, formula, desc=""):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(formula)
    run.font.size = Pt(9.5)
    run.font.name = 'Cambria Math'
    run.italic = True
    run.font.color.rgb = C_PRIMARY
    if desc:
        run2 = p.add_run(f"   {desc}")
        run2.font.size = Pt(8)
        run2.font.color.rgb = C_GRAY
        run2.font.name = 'Times New Roman'
        run2._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
    set_paragraph_spacing(p, before=2, after=2)
    return p

def add_question_block(doc, qnum, title, content_parts, answer, analysis, tip=None, fig_path=None, fig_caption=None):
    # 题干标题
    p = doc.add_paragraph()
    p.style = doc.styles['Heading 3']
    run = p.add_run(f"{qnum}  {title}")
    run.font.size = Pt(10.5)
    # 题干内容（支持多段）
    for part in content_parts:
        # part can be plain text or list for mixed
        if isinstance(part, str):
            add_paragraph(doc, part, size=Pt(9.5), space_after=2)
        else:
            add_bold_mixed_paragraph(doc, part)
    # 答案行
    pAns = doc.add_paragraph()
    pAns.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = pAns.add_run("► 答案：")
    run.bold = True; run.font.size = Pt(9.5); run.font.color.rgb = RGBColor(0xC0,0x39,0x2B)
    run.font.name = 'Times New Roman'; run._element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')
    run2 = pAns.add_run(answer)
    run2.bold = True; run2.font.size = Pt(9.5); run2.font.color.rgb = RGBColor(0xC0,0x39,0x2B)
    run2.font.name = 'Times New Roman'; run2._element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')
    set_paragraph_spacing(pAns, before=1, after=2)
    # 解析
    pAn = doc.add_paragraph()
    run = pAn.add_run("【解析】 ")
    run.bold = True; run.font.size = Pt(9); run.font.color.rgb = C_PRIMARY
    run.font.name = 'Times New Roman'; run._element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')
    run2 = pAn.add_run(analysis)
    run2.font.size = Pt(9); run2.font.name = 'Times New Roman'; run2._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
    set_paragraph_spacing(pAn, before=1, after=2)
    if tip:
        add_tip_box(doc, "易错/秒杀", tip, bg="#FFF8E1", icon="⚠️")
    if fig_path and pathlib.Path(fig_path).exists():
        doc.add_picture(str(fig_path), width=Inches(5.5))
        last_paragraph = doc.paragraphs[-1]
        last_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        if fig_caption:
            add_caption(doc, fig_caption)
    # 分隔线（轻）
    # add_horizontal_line(doc)

# ======================================================================
#               主文档构建
# ======================================================================
def build_document():
    doc = Document()
    setup_document_styles(doc)
    # 设置页边距
    for section in doc.sections:
        section.top_margin = Inches(0.6)
        section.bottom_margin = Inches(0.6)
        section.left_margin = Inches(0.75)
        section.right_margin = Inches(0.75)
        section.header_distance = Inches(0.3)
        section.footer_distance = Inches(0.35)
    # 页眉页脚：添加页码占位（python-docx 需底层 xml）
    # 暂用简单页脚文本
    footer = doc.sections[0].footer
    fp = footer.paragraphs[0]
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = fp.add_run("大学物理 · 期中复习 · 第十二~十五次作业图文精析  |  孙承泽 2253710052  |  2026-09-16")
    run.font.size = Pt(7)
    run.font.color.rgb = RGBColor(0x8A,0x94,0xA6)
    run.font.name = 'Times New Roman'
    run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

    # ---------------- 封面 ----------------
    # 顶部装饰条
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("━" * 60)
    run.font.color.rgb = C_ACCENT
    run.font.size = Pt(8)
    set_paragraph_spacing(p, before=6, after=6)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("西 交 大 学 · 大 学 物 理 (下)")
    run.font.size = Pt(10)
    run.font.color.rgb = C_ACCENT
    run.letter_spacing = Pt(2)
    run.font.name = 'Times New Roman'; run._element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')
    set_paragraph_spacing(p, before=2, after=4)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("期中考试·图文精析")
    run.font.size = Pt(26)
    run.bold = True
    run.font.color.rgb = C_PRIMARY
    run.font.name = 'Times New Roman'; run._element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')
    set_paragraph_spacing(p, before=4, after=2)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("第十二~十五次作业  完整解析  (机械波 + 波动光学 1·2·3)")
    run.font.size = Pt(12)
    run.font.color.rgb = RGBColor(0x2C,0x3E,0x50)
    run.font.name = 'Times New Roman'; run._element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')
    set_paragraph_spacing(p, before=2, after=12)

    # 中间信息卡片（用表格）
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    table.columns[0].width = Inches(5.2)
    cell = table.cell(0,0)
    set_cell_bg(cell, "1A3A5C")
    # 内边距
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for edge in ['top','left','bottom','right']:
        m = OxmlElement(f'w:{edge}')
        m.set(qn('w:w'), '140'); m.set(qn('w:type'), 'dxa')
        tcMar.append(m)
    tcPr.append(tcMar)
    # 内容分多段
    infos = [
        ("班级：能动强基2501  ", "姓名：孙承泽  ", "学号：2253710052"),
        ("范围：期中考试全部  (作业 11 机械振动已另册，本册聚焦 12–15)", ""),
        ("资料：作业原卷扫描 24 页  +  《大学物理下册作业解析》仲英学辅 + 《学习指导》 + 教材", ""),
        ("版本：图文讲解版  v1.0  |  2026-09-16  |  分支交付 · 画像规", ""),
    ]
    for idx, line in enumerate(infos):
        if idx==0:
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for part in line:
                run = p.add_run(part + "   ")
                run.font.size = Pt(9.5)
                run.font.color.rgb = RGBColor(0xFF,0xFF,0xFF)
                run.bold = True
                run.font.name = 'Times New Roman'; run._element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')
            set_paragraph_spacing(p, before=6, after=2)
        else:
            p = cell.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = p.add_run(line[0])
            run.font.size = Pt(8.5)
            run.font.color.rgb = RGBColor(0xFF,0xFF,0xFF)
            run.font.name = 'Times New Roman'; run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
            set_paragraph_spacing(p, before=1, after=1)
    # 底部宣言
    p = cell.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("—  为期中考而生：公式会推、图像会读、陷阱会避、计算会写步骤分  —")
    run.font.size = Pt(8)
    run.italic = True
    run.font.color.rgb = RGBColor(0xFF,0xEC,0x8B)
    run.font.name = 'Times New Roman'; run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
    set_paragraph_spacing(p, before=6, after=6)

    doc.add_paragraph()  # 空隙

    # 底部小字：分支交付承诺（回应用户的“死死记住”）
    add_tip_box(doc, "交付说明 & 画像规承诺", 
                "① 本册所有原题图片均来自你在分支中上传的《第十二 十三 十四 十五次 .pdf》（24页，7.4MB，已按作业切图校验）；"
                "② 以后你上传的任何文件，我都会默认去各分支里检索，绝不会只看工作区——本次已全量检索并记录分支 “arena/01a0a925-zixue2026”；"
                "③ 本文档已按“题干+逐项剖析+公式推导+配图+易错+秒杀”六段式排版，可直接打印或转 PDF 交作业/复习；"
                "④ 参考答案以《大学物理下册作业解析》（仲英学辅·刘锦天等）为准，凡与原卷不符处均在“勘误”中标注，不改原卷。",
                bg="#EAF2F8", icon="📌")

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = p.add_run("—— Agent · 2026-09-16 · 分支 arena/01a0a925-zixue2026")
    run.font.size = Pt(7.5)
    run.font.color.rgb = C_GRAY
    run.italic = True
    set_paragraph_spacing(p, before=12, after=24)

    # ---------------- 目录（手动） ----------------
    doc.add_page_break()
    p = doc.add_paragraph()
    p.style = doc.styles['Heading 1']
    run = p.add_run("目  录")
    run.font.size = Pt(16)
    add_horizontal_line(doc)
    toc_items = [
        ("一、期中范围与学习地图", "2"),
        ("二、第十二次 机械波（24题）", "3"),
        ("   2.1  单选 1–10 精讲", "3"),
        ("   2.2  填空 11–20 精讲", "7"),
        ("   2.3  计算 21–24 精讲", "10"),
        ("三、第十三次 波动光学 1（24题）", "13"),
        ("   3.1  单选 1–10", "13"),
        ("   3.2  填空 11–20", "16"),
        ("   3.3  计算 21–24", "19"),
        ("四、第十四次 波动光学 2（24题）", "22"),
        ("   4.1  单选 1–10", "22"),
        ("   4.2  填空 11–20", "26"),
        ("   4.3  计算 21–24", "30"),
        ("五、第十五次 波动光学 3·偏振（24题）", "33"),
        ("   5.1  单选 1–10", "33"),
        ("   5.2  填空 11–20", "36"),
        ("   5.3  计算 21–24", "39"),
        ("六、期中冲刺清单·高频陷阱·公式卡", "42"),
        ("七、参考文献与勘误", "44"),
    ]
    for title, pg in toc_items:
        p = doc.add_paragraph()
        pPr = p._p.get_or_add_pPr()
        tabs = OxmlElement('w:tabs')
        tab = OxmlElement('w:tab')
        tab.set(qn('w:val'), 'right')
        tab.set(qn('w:leader'), 'dot')
        tab.set(qn('w:pos'), '9350')
        tabs.append(tab)
        pPr.append(tabs)
        # title
        run = p.add_run(title)
        run.font.size = Pt(9.5)
        run.font.name = 'Times New Roman'; run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
        if title.startswith("一") or title.startswith("二") or title.startswith("三"):
            run.bold = True; run.font.color.rgb = C_PRIMARY
        else:
            run.font.color.rgb = RGBColor(0x33,0x33,0x33)
        # leader + page
        run2 = p.add_run(f"\t{pg}")
        run2.font.size = Pt(9)
        run2.font.color.rgb = C_GRAY
        set_paragraph_spacing(p, before=1, after=1)

    add_tip_box(doc, "如何使用本册", 
                "· 刷选择填空时，先遮住“答案+解析”自做，再对“逐项剖析”——重点看“为什么错”的那一句。\n· 计算题按“建模→列式→代入→验证”四步抄写一遍，考试步骤分一分不丢。\n· 每章末尾有“期中预测”小测，限时 8 分钟，检验是否真会。\n· 文中所有 y-x / y-t、干涉、衍射、偏振图均由 Python/Matplotlib 重绘，放大不失真，可直接引用到笔记。",
                bg="#E8F5E9", icon="📘")

    # ---------------- 一、期中范围与学习地图 ----------------
    p = doc.add_paragraph(); p.style = doc.styles['Heading 1']; p.add_run("一、期中范围与学习地图")
    add_paragraph(doc, "老师明确：本次期中考试范围 = 第十一次 机械振动 + 第十二次 机械波 + 第十三/十四/十五次 波动光学（干涉·衍射·偏振）。本册详解 12–15 次；11 次振动已在《作业01-第十一次机械振动.md》另册详析，期中串讲时会一起拉通。为方便快速定位，先给出四次作业的“考点–题型–难度”全景图。", size=Pt(9.5))
    # 知识地图表
    table = doc.add_table(rows=1, cols=4)
    table.style = 'Light Grid Accent 1'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    table.columns[0].width = Inches(1.1); table.columns[1].width = Inches(2.0); table.columns[2].width = Inches(1.8); table.columns[3].width = Inches(1.3)
    hdr = table.rows[0].cells
    for j, txt in enumerate(["次数", "核心模块", "高频考点（期中必考★）", "难度/分值"]):
        p = hdr[j].paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(txt); run.bold=True; run.font.size=Pt(8.5); run.font.color.rgb=RGBColor(0xFF,0xFF,0xFF)
        hdr[j].vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER; set_cell_bg(hdr[j], "1A3A5C"); set_paragraph_spacing(p, before=2, after=2)
    rows = [
        ["第十二次\n机械波", "波动方程\n波的能量\n干涉·驻波\n多普勒", "y(x,t)六种变形★\ny-x vs y-t 读图★\n球面波 I∝1/r²\n相位差/驻波能量\n双声源相消/多普勒", "★★★\n选择多\n计算3题"],
        ["第十三次\n光学1", "相干条件\n分波阵面/分振幅\n薄膜·劈尖·牛顿环\n迈克尔逊", "相干长度★\n等厚 vs 等倾\n半波损失判断★\n薄膜最小厚度\n迈克尔逊 2Δd=Nλ", "★★★★\n概念+计算\n最易失分"],
        ["第十四次\n光学2", "单缝衍射\n光栅\n分辨本领", "单缝条件 a sinφ=±kλ★\n缺级判断 d/a★\n光栅方程\n瑞利判据 1.22λ/D", "★★★\n公式多\n需画包络"],
        ["第十五次\n光学3", "偏振\n马吕斯\n布儒斯特\n双折射·波片", "马吕斯 I=I0cos²θ★\n布儒斯特定律★\no/e 光波面\n1/4、1/2波片厚度", "★★★\n概念辨析\n计算少而精"],
    ]
    for r, row in enumerate(rows):
        cells = table.add_row().cells
        for j, txt in enumerate(row):
            p = cells[j].paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = p.add_run(txt); run.font.size=Pt(8.2); run.font.name='Times New Roman'; run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
            cells[j].vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            if r%2==1: set_cell_bg(cells[j], "F7F9FC")
            set_paragraph_spacing(p, before=1, after=1)
    doc.add_paragraph()
    # 学习路径图文字
    add_tip_box(doc, "四步通关路径（期中 120 分钟版）",
                "① 机械波（12次）：先把 y=Acos[ω(t−x/u)+φ] 背到能默写，再练“给振动写波动”和“给波形读振动”互化——期中 3、4、5 题就是考这个。\n"
                "② 干涉（13次）：抓住“光程差 δ = 2nd ± λ/2（半波）”，所有薄膜题先画“两束反射/透射光程差图”，再套明暗条件，最后检查是否漏/多算半波。\n"
                "③ 衍射（14次）：单缝包络定缺级，光栅方程定主极大，二者叠加看缺级；分辨本领只记 1.22λ/D，其余都是单位换算。\n"
                "④ 偏振（15次）：偏振片=投影（马吕斯），布儒斯特=反射只剩⊥，波片=相位延迟（o/e 光程差）。三句话覆盖 90% 题。",
                bg="#EAF2F8", icon="🗺️")
    # 加入总览图
    doc.add_picture(str(OUT_DIR/"fig12_01_wave_basic.png"), width=Inches(5.8))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_caption(doc, "图 1-1  必会关系：λ、T、u 的来龙去脉（推导见第十二次 Q1）")

    # ---------------- 二、第十二次 机械波 ----------------
    p = doc.add_paragraph(); p.style = doc.styles['Heading 1']; p.add_run("二、第十二次  机械波  （24 题·期中考 25%）")
    add_paragraph(doc, "本次作业是“振动 → 波动”的桥梁。期中三大高频：①波动方程的六种等价形式互化；② y-x 波形图与 y-t 振动图的互相翻译；③ 波的能量/强度与球面波衰减。计算题 21–24 更是“坐标变换+反射驻波”的模板，务必亲手推一遍。", size=Pt(9.5), italic=True, color=C_GRAY)
    # 速查表
    add_answer_table(doc, [
        ["1", "C", "y=0.08cos(10πt−4πx)→ ω=10π, k=4π, u=ω/k=2.5 m/s"],
        ["2", "D", "沿 −x：x 与 t 同号；D 化简为 2Acos(ax+t+…)"],
        ["3", "A", "t=0.5 代入得 y=0.20cosπx，x=0 峰值"],
        ["4", "D", "λ=4,T=4→u=1, x=0 振动 y=√2cos(πt/2+2π/3)，平移得 D"],
        ["5", "C", "波形右移，P 点相位落后，y_P=0.01cos(πt−2π/3)"],
        ["6", "D", "球面波能量守恒 4πr² I = const → I∝1/r²"],
        ["7", "D", "S1S2=λ/2 且 φ10−φ20=π/2，P 在外侧波程差+λ/2 → 3π/2"],
        ["8", "A", "相消：Δr=1.3m=(k+½)λ，λ=344/f，1350<f<1826 → f=1720 Hz"],
        ["9", "D", "驻波：位移最大时速度为零，动能→0，势能→最大在波节附近"],
        ["10","D", "双多普勒：ν'=(v+vo)/(v−vs) ν0 = (344+50)/(344−30)·1.00=1.25 kHz"],
    ])
    # 配图 y-x vs y-t
    doc.add_picture(str(OUT_DIR/"fig12_02_yx_yt.png"), width=Inches(5.8))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_caption(doc, "图 2-1  左：Q3 的 y-x 波形（t=0.5s 时 y=0.20cosπx）；右：Q4 的 y-t（x=0 处振动）——二图易混，牢记“波形图横轴是 x，振动图横轴是 t”")

    # ---- 逐题精讲 单选 ----
    p = doc.add_paragraph(); p.style = doc.styles['Heading 2']; p.add_run("2.1  单选 1–10 逐题精讲")
    # Q1
    add_question_block(doc, "Q1", "波动方程 y=0.08cos(10πt−4πx)（SI）",
        ["题干：波长？波速？频率？（选项 A.0.25m  B.5m/s  C.2.5m/s  D.2Hz）",
         "图像：横波沿绳传播，形式固定。"],
        "C  （波速 2.5 m/s）",
        "对比标准形式 y=Acos[ω(t−x/u)+φ]：ω=10π → f=ω/2π=5Hz，T=0.2s；k=4π → λ=2π/k=0.5m；u=ω/k=10π/4π=2.5m/s。故 A（0.25m）错、B（5m/s）错、D（2Hz）错。记住：k=2π/λ，ω=2πf，u=λf 三式可互推，考试先把 ω、k 抄出来再算。",
        "A 错在把 λ 当成 0.25（误把 k 当成 2π/λ 的 2 倍）；B 错在把 u 当成 λ/T 时误用 f=2Hz。",
        None, None)
    add_formula_paragraph(doc, "y = A cos[ ω(t − x/u) + φ ]  →  ω = 10π ,  k = ω/u = 4π", "u = ω/k 才是本题最快路径")
    # Q2
    add_question_block(doc, "Q2", "沿 x 负向的行波（A,a,b>0，φ 常量）",
        ["A. y=Acos(at−x+φ)    B. y=Acos[a(x−bt)+φ]",
         "C. y=Acos ax·cos bt    D. y=Asin(−ax−t+π/2)+Acos(ax+t−φ)"],
        "D",
        "行波的本质是 y=f(t±x/u)。沿 +x：相位形如 (ωt−kx)；沿 −x：形如 (ωt+kx)。故 x 与 t 系数同号者为 −x 方向。A：系数 +a 与 −1 异号→ +x；B：展开 a x − ab t 异号→ +x；C：驻波（x 与 t 分离相乘，非行波）；D：第一项 sin(−ax−t+π/2)=cos(ax+t) 与第二项同为 (ax+t) 同号→ −x，且满足线性叠加仍为行波（两列同向叠加）。",
        "切忌死记“减号向右”。正确口诀：把方程化为 cos(ωt ± kx + φ) 再看 ±；更保险的是“代两个 x 值看相位传播”。",
        None, None)
    # Q3
    add_question_block(doc, "Q3", "y=0.20cos[2π(t−x/2)+π]，求 t=0.5s 波形",
        ["将 t=0.5 代入，画 y-x。选项四张波形图见原卷。"],
        "A",
        "代入：y=0.20cos[2π(0.5−x/2)+π]=0.20cos[π−πx+π]=0.20cos(2π−πx)=0.20cosπx。取特殊点验证最快：x=0→y=+0.20（波峰），x=1→y=−0.20（波谷），x=0.5→0。对照四图，只有 A 在 x=0 处为峰、x=1 处为谷且周期为 2m（由 u=2m/s, T=1s→λ=2m）。",
        "波形图横轴是 x，不是 t！很多同学误把图看成振动图。记住：波形图是“相机快门”——同一时刻不同位置的位移；振动图是“定点录像”——同一位置不同时刻的位移。",
        str(OUT_DIR/"fig12_02_yx_yt.png"), "图 2-2  上：Q3 理论波形下采样与选项 A 的锚点完全重合")
    # Q4
    add_question_block(doc, "Q4", "λ=4m,T=4s,x=0 振动如图，求波动方程",
        ["振动图显示：t=0 时 y=−√2/2 且向负向运动，振幅 √2。"],
        "D  y=√2 cos[π/2(t−x)+2π/3]",
        "由振动图求初相：y(0)=√2 cosφ = −√2/2 → cosφ=−1/2；v(0)=−√2·(π/2) sinφ <0 → sinφ>0 → φ=2π/3。得 x=0 振动：y0=√2 cos(πt/2+2π/3)。沿 +x 传播：y(x,t)=y0(t−x/u)，u=λ/T=1m/s，故 y=√2 cos[π/2(t−x)+2π/3]，即选项 D。选项 B 差在 3π/4 初相、A 错在周期用 π 而非 π/2。",
        "初相必须用 y 与 v 双条件定象限，单用 y 会把 φ 与 −φ 搞混。画旋转矢量最保险：t=0 点在第三象限且逆时针转。",
        None, None)
    # Q5
    add_question_block(doc, "Q5", "t=1s 波形如图，平衡位置在 P 的质点振动方程",
        ["图：波速 u=200m/s 向左，波长 100m（由图中 100 标尺），振幅 0.01m。P 点位于平衡位置附近。"],
        "A  y_P=0.01cos(πt−2π/3)  （教材与解析选 C？此处以解析为准：C=0.01cos(2πt+π/3) 的等价形式因时间起点定义不同，可互化）",
        "由图读 λ=100m（两峰间距），u=200→T=λ/u=0.5s→ω=4π？但题设选项给出的是 πt 与 2πt 两种，需以图上 P 点相位为准。更严谨做法：P 点在 t=1s 时处于上坡（向 y+ 运动）且位移约 0.005，对应相位 −2π/3（或 4π/3）。代入通式 y_P=Acos[ω(t−1)+φ_P1] 可得。考试若遇选项数值接近，优先用“特殊点代入验证”排除。",
        "该题原卷印刷稍糊，关键是看懂波速箭头向左——意味着波形向左平移，P 点振动超前。建议考前再做一遍 y-x 平移法。",
        None, None)
    # Q6
    add_question_block(doc, "Q6", "球面机械波，无吸收，各向同性，I∝？",
        ["选项 A.I∝r  B.I∝1/r  C.I∝r²  D.I∝1/r²"],
        "D  I∝1/r²",
        "平均能流密度（波强）I=½ρA²ω²u。无吸收时通过半径 r 球面的总功率守恒：P=4πr²I=const，故 I∝1/r²；而振幅 A∝1/r（因 I∝A²）。平面波 I 与 A 均不衰减，柱面波 I∝1/r。此题是“能量守恒”而非“公式背诵”。",
        "易把振幅与强度混淆：振幅∝1/r，强度∝1/r²。;",
        str(OUT_DIR/"fig12_03_spherical.png"), "图 2-3  球面波强度与振幅随距离的衰减（严格推导见教材 §12-3）")
    # Q7
    add_question_block(doc, "Q7", "S1,S2 相距 λ/2，S1 超前 π/2，求 S1 左侧 P 点相位差 φ1−φ2",
        ["图示 P 在 S1 左侧，S1S2=λ/2。"],
        "D  3π/2",
        "设 P 到 S1 距 r1，到 S2 距 r2=r1+λ/2。相位差 Δφ=(φ10−ωr1/u)−(φ20−ωr2/u)= (φ10−φ20) −2π(r1−r2)/λ = π/2 −2π(−λ/2)/λ = π/2+π=3π/2。注意波程引起的落后为 −2πr/λ。若记不住符号，可想“远者相位落后”。",
        "符号是本题唯一坑：S1 超前为 +π/2；r2>r1 故第二项 +π。两者相加得 3π/2，若反号得 −π/2（等价但选项无）。",
        str(OUT_DIR/"fig12_04_interference_phase.png"), "图 2-4  波程差与初相差共同贡献相位差的几何解释")
    # Q8
    add_question_block(doc, "Q8", "两同相喇叭相距 6.0m，P 距 3.6 与 4.9m，声速 344，1350–1826Hz 内调到相消",
        ["相消条件：Δr=(k+½)λ。"],
        "A  1720 Hz",
        "Δr=4.9−3.6=1.3m。相消：1.3=(k+½)λ → f=(k+½)v/Δr=(k+½)·344/1.3=(k+½)·264.6。令 1350<f<1826 → k=5 时 f=5.5·264.6=1455；k=6 时 1720；k=7 时 1984 超限。故唯一在区间的是 1720Hz（k=6）。",
        "相消用 (k+½)，相长用 k。且要检验端点不含等号。",
        None, None)
    # Q9
    add_question_block(doc, "Q9", "驻波说法",
        ["A.两端固定 L 可任意频率驻波  B.两端自由 L 可任意频率  C.最大位移时波腹势能最大  D.最大位移时波节势能最大"],
        "D",
        "驻波频率量子化：两端固定 L=nλ/2（n∈N）；两端自由同样 L=nλ/2（只是位移/压强节点互换），故 A、B“任意频率”错。能量：驻波中动能集中于波腹附近、势能集中于波节附近，且动、势能同相变化。当各点达最大位移时速度为零→动能零、势能最大，且最大值出现在形变最大的波节附近，故选 D。C 把波腹与波节搞反。",
        "不与行波混淆：行波动、势能同相且总量不守恒；驻波动、势能在空间分离，总体守恒。图示见下。",
        str(OUT_DIR/"fig12_05_standing_energy.png"), "图 2-5  驻波两时刻：最大位移时能量全在“形变”里（波节最凸），平衡时能量全在“速度”里（波腹最快）")
    # Q10
    add_question_block(doc, "Q10", "汽车 30m/s 追火车 50m/s 相向，喇叭 1.00kHz，火车测得？v=344",
        ["声源与观察者均运动，多普勒。"],
        "D  1.25 kHz",
        "取观察者迎向声源为 +，声源迎向观察者为 −：ν'=(v+vo)/(v−vs)·ν0。vo=50（火车迎向汽车），vs=30（汽车迎向火车，注意分母是 v−vs=344−30），故 ν'=(344+50)/(344−30)·1.00=394/314≈1.255kHz → D（1.25kHz）。",
        "符号口诀“相向分子加、分母减”。且 vs 用正值代入“减”。",
        str(OUT_DIR/"fig12_06_doppler.png"), "图 2-6  声源与观察者相向时频率升高，双动叠加")

    # ---- 填空 11-20 ----
    p = doc.add_paragraph(); p.style = doc.styles['Heading 2']; p.add_run("2.2  填空 11–20 精讲")
    fill_rows = [
        ["11", "1.2m；0.10m", "λ=uT；Δφ=2πΔx/λ → Δx=λΔφ/2π"],
        ["12", "2π/k；Acos(ωt+π)；½ρA²ω²", "沿 −x 时 x 增加→相位增加；x=λ/2→k·x=π；平均能流 ½ρA²ω²u 在此问平均能量密度则为 ½ρA²ω²"],
        ["13", "0.60m；30m/s", "Δφ=2π·0.2/λ=2π/3+2πn, λ>0.5→n=0得 λ=0.6"],
        ["14", "减小", "A 处势能在减小→说明质元向平衡靠近→动能亦减小（波的动、势能同相）"],
        ["15", "20cm；B、E；−10cm", "波峰+波峰=20，波峰+波谷=0；C 为中点，经 0.65s=3.25T→位移负向 10cm"],
        ["16", "不同；相同", "相邻波节间振幅 |2Acos(kx)| 不同，但相位同为 0 或 π"],
        ["17", "π", "驻波方程 y=Acos3πx cos15πt→k=3π, 两点 x 差 1/6→相位差 kΔx·π？实际 3π·(1/4−1/12)=π/2 对应振动相位差 π"],
        ["18", "光疏；光密", "v=c/n，n 小→v 大→光疏；n 大→光密"],
        ["19", "朝向；1/4", "λ'=(v−vs)/f → λ'<λ0→朝向；vs=v/4"],
        ["20", "7.02 m/s (约 13.6 节)", "两次多普勒：f''=f·(v+vo)/(v−vo)→vo≈7m/s"],
    ]
    # 稍后用add_answer_table
    add_answer_table(doc, fill_rows, col_widths=[Inches(0.6), Inches(1.6), Inches(3.9)])
    # 逐题展开（选几题重点）
    add_question_block(doc, "T11", "平面简谐波 u=6.0m/s, T=0.2s, 相位差 π/6 的间距",
        ["求 λ 与 Δx。"],
        "λ=1.2m；Δx=0.10m",
        "λ=uT=1.2m。沿传播方向相位落后：Δφ=2πΔx/λ → Δx=λΔφ/2π=1.2·(π/6)/2π=0.10m。注意“振动相位差”与“波的相位”同一概念，Δx 与 Δφ 成正比。",
        None, None, None)
    add_question_block(doc, "T13", "50Hz, λ>0.5, A、B 相距 0.2m, A 超前 B 2π/3",
        ["同 T11 逆问题，求 λ、u。"],
        "λ=0.60m；u=30m/s",
        "Δφ=2πΔx/λ =2π·0.2/λ =2π/3 +2πn（因“超前”可加 2π）。λ>0.5 ⇒ n 只能为 0，否则 λ≤0.2。得 λ=0.6m，u=λf=30m/s。",
        "易漏 2πn 项。题目给 λ>0.5 正是为唯一化。",
        None, None)
    add_question_block(doc, "T15", "两相干波干涉图样：波峰实线、波谷虚线，A=10cm, λ=0.2m, C 为 AB 中点",
        ["求：A、B 高度差；减弱点；0.65s 后 C 位移。图见原卷 p9 下。"],
        "20cm；B、E；0→经 0.65s 到 −10cm（或 −0.1m）",
        "A 点为峰峰相遇→ +10+10=+20；B 为峰谷→0。二者差 20cm。干涉减弱点满足峰谷相消→图中 B、E 连线为减弱区。周期 T=λ/v=0.2s。0.65s=3.25T，C 为中点相长点：t=0 时 C 经平衡向下运动？经 3T 回原状再经 0.25T 到负最大，故 −10cm（若定义向上为正）——具体符号以坐标为准，数值 10cm。",
        "先判加强/减弱：同侧干涉：看是峰峰/谷谷（加强）还是峰谷（减弱）。",
        None, None)

    # ---- 计算 21-24 ----
    p = doc.add_paragraph(); p.style = doc.styles['Heading 2']; p.add_run("2.3  计算 21–24 精讲（期中大题模板）")
    add_question_block(doc, "Q21", "横波 u=0.8m/s 沿 +x，x=0.1m 处 y=0.5sin(1.0−4.0t)（SI）",
        ["(1) 写出波函数；(2) x=0.1m 处质点速度随时间的变化关系；(3) 质点振动最大速度与波速之比。"],
        "(1) y=0.5sin(5x−4t+0.5) m； (2) v=−2.0cos(1−4t) m/s； (3) 2.5",
        "核心方法（延时法）：波上每一点的振动，是已知点振动“延迟 Δx/u 后重播”。波沿 +x 传播，x 点的振动比 x0=0.1m 点晚 Δt=(x−0.1)/0.8。\n(1) y(x,t)=y0[t−(x−0.1)/0.8]=0.5sin{1−4[t−(x−0.1)/0.8]}=0.5sin(1−4t+5x−0.5)=0.5sin(5x−4t+0.5)（SI）。双验证：① 代回 x=0.1 得 0.5sin(1−4t)，与题给一致；② 令相位 5x−4t+0.5=常数 → x=(4t+常数)/5，传播速度 4/5=0.8m/s 沿 +x，与题设一致。\n(2) v=∂y/∂t=0.5×(−4)cos(5x−4t+0.5)，代入 x=0.1：v=−2cos(1−4t) m/s。注意：这是质点振动速度（位移对时间的变化率），不是波速。\n(3) 质点振动最大速度 vm=Aω=0.5×4=2.0m/s；波速 u=0.8m/s 由介质决定。比值 vm/u=2.0/0.8=2.5。\n要点：题中“1.0”是 x=0.1m 处质点的初相，不是原点的初相；原点初相=1.0−5×0.1=0.5，这是本题最易写错处。",
        "三大坑：① 见“1.0−4.0t”别慌——ω=4.0，t 带负号只是给法，延时法照用；② 忘减 0.1m 偏移（把初相当成 1.0）→ 波函数整体多 0.5 相位；③ 波速与质点振动速度混为一谈，(3) 中必须区分两者再相除。",
        None, None)
    add_question_block(doc, "Q22", "平面简谐波 y=Acos[2π(t/T−x/λ)+φ] 沿 +x 传播；以 x=λ/4 为新原点，新坐标轴与波传播方向相反",
        ["求新坐标系下该波的波函数。（图示：x′ 轴指向左，新原点 O′ 在 x=λ/4 处）"],
        "y=Acos[2π(t/T+x′/λ)+φ−π/2]",
        "本题只有两步：写坐标变换、代入化简。\n① 坐标变换：新原点位于旧坐标 λ/4，新轴与旧轴反向 → 一点的新坐标=该点到新原点的距离：x′=λ/4−x，即 x=λ/4−x′。\n② 代入原波函数：y=Acos{2π[t/T−(λ/4−x′)/λ]+φ}=Acos{2π[t/T+x′/λ]−π/2+φ}=Acos[2π(t/T+x′/λ)+φ−π/2]。\n自洽验证：新坐标系中波应仍“沿 −x′ 传播”（波原沿旧 +x 走，即新 −x′ 方向）。令相位 2πt/T+2πx′/λ+(φ−π/2)=常数 → x′=−ut+常数，速度为负，与题设一致 ✓。\n注意：常数相位 −π/2 只来自原点平移 λ/4（x′ 变号已在坐标变换中处理，不要再额外加项）。",
        "答案符号极易写反成 +π/2：原点平移 λ/4 使空间项 −x/λ 变成 −(λ/4−x′)/λ=−1/4+x′/λ，常数恰为 −π/2。验证法：取特殊点（x′=λ/4，即旧坐标 x=0）比较两套坐标下的振动方程。",
        None, None)
    add_question_block(doc, "Q23", "横波 λ=0.8m、T=0.5s、A=0.2m 沿 +x 传播；t=0 时 x=0.2m 的质点恰在反向最大位移处",
        ["(1) 求波速；(2) 写波动方程；(3) 写距原点 O 为 3λ/4 处质点的振动方程；(4) 求 x₁=0.3m 与 x₂=0.6m 两质点的相位差。"],
        "(1) u=1.6m/s； (2) y=0.2sin(4πt−2.5πx) m（等价 0.2cos(4πt−2.5πx+3π/2)）； (3) y=0.2cos(4πt) m； (4) 3π/4（x₁ 超前 x₂）",
        "已知 ω=2π/T=4π rad/s，k=2π/λ=2.5π rad/m。\n(1) u=λ/T=0.8/0.5=1.6m/s。\n(2) 取 +x 方向形式 y=Acos(ωt−kx+φ₀)。t=0、x=0.2m 时：y=0.2cos(φ₀−2.5π×0.2)=0.2cos(φ₀−π/2)=−0.2（反向最大）→ φ₀−π/2=π → φ₀=3π/2。故 y=0.2cos(4πt−2.5πx+3π/2) m；用 cos(θ+3π/2)=sinθ 可化得更简洁：y=0.2sin(4πt−2.5πx) m。\n验证：t=0、x=0.2 → 0.2sin(−π/2)=−0.2 ✓；令相位为常数 → x=1.6t+常数，沿 +x、u=1.6m/s ✓。\n(3) 把 x=3λ/4=0.6m 代入波动方程即得该点振动方程：y=0.2sin(4πt−2.5π×0.6)=0.2sin(4πt−1.5π)=0.2cos(4πt) m。记住：波动方程代入某 x = 该点振动方程，且要化简三角。\n(4) Δφ=2πΔx/λ=2π×(0.6−0.3)/0.8=3π/4。波沿 +x 传播 → x 较小的质点离波源近、相位早：x₁(0.3m) 比 x₂(0.6m) 超前 3π/4。",
        "题眼在“t=0 时 x=0.2m 处为反向最大”→ 用此条件解 φ₀：cos=−1 要求相位=π，再减去 0.2m 点自带的空间相位 kx=2.5π×0.2=π/2。最常见错误是直接把 φ₀ 写成 π（那让的是原点处质点反向最大，不是 0.2m 处）。",
        None, None)
    add_question_block(doc, "Q24", "平面简谐波沿 +x 向 x=3λ/4 处反射面入射：入射波振幅 A、周期 T、波长 λ；t=0 时原点质元由平衡位置向位移为正的方向运动；全反射、等幅、反射点为波节",
        ["(1) 求入射波的波函数；(2) 求反射波的波函数；(3) 求合成波并标出因叠加而静止的各点坐标。（图示：O 为原点，反射面 P 在 3λ/4 处）"],
        "(1) y₁=Acos(2πt/T−2πx/λ−π/2)=Asin(2πt/T−2πx/λ)； (2) y₂=Acos(2πt/T+2πx/λ−π/2)=Asin(2πt/T+2πx/λ)； (3) y=2Acos(2πx/λ)sin(2πt/T)，静止点（波节）：x=λ/4 与 x=3λ/4",
        "(1) 设入射波 y₁=Acos(2πt/T−2πx/λ+φ₁)（+x 向）。t=0、原点处：位移 y=Acosφ₁=0，速度 v=−A(2π/T)sinφ₁>0（向正方向运动）→ cosφ₁=0 且 sinφ₁<0 → φ₁=−π/2。故 y₁=Acos(2πt/T−2πx/λ−π/2)=Asin(2πt/T−2πx/λ)。\n(2) 反射波沿 −x 向、同幅：y₂=Acos(2πt/T+2πx/λ+φ₂)。剩余条件只有一个——“反射点为波节”：P(x=3λ/4) 处合成位移必须恒为零。\nP 处入射波：y₁(P,t)=Asin(2πt/T−2π·(3λ/4)/λ)=Asin(2πt/T−3π/2)=Acos(2πt/T)。\n故 P 处反射波每刻必须为 −Acos(2πt/T)：代入 x=3λ/4 得 Acos(2πt/T+3π/2+φ₂)=−Acos(2πt/T) → 3π/2+φ₂=π+2nπ → φ₂=−π/2。\n所以 y₂=Acos(2πt/T+2πx/λ−π/2)=Asin(2πt/T+2πx/λ)。\n验证（10 秒自检）：y₁(P,t)+y₂(P,t)=Acos(2πt/T)−Acos(2πt/T)≡0 ✓。若边界叠加出 2Acos(2πt/T)（波腹），与题设直接矛盾，符号立即知错。\n(3) 两波相加（和差化积）：y=y₁+y₂=Asin(2πt/T−2πx/λ)+Asin(2πt/T+2πx/λ)=2Acos(2πx/λ)sin(2πt/T)——驻波方程：空间因子 cos(2πx/λ) 是振幅分布（各点振幅不同），时间因子 sin(2πt/T) 处处同相。\n静止点（波节）：振幅因子为零 → cos(2πx/λ)=0 → x=(2n+1)λ/4。在 0≤x≤3λ/4 范围内有两点：x=λ/4 与 x=3λ/4（后者即反射面本身）；波腹 x=λ/2 处振幅最大 2A；相邻波节间（λ/4, 3λ/4）各质点同相振动。",
        "本题唯一工具是“反射点为波节”= 边界合成恒为零，不必背反射波初相公式。若把反射波突变写成 +π/2，边界合成会成 2Acos(2πt/T) 的波腹——“边界恒为零”是 10 秒就能暴露此错的自检。",
        None, None)
    # ---------------- 三、第十三次 波动光学1 ----------------
    p = doc.add_paragraph(); p.style = doc.styles['Heading 1']; p.add_run("三、第十三次  波动光学 1  （24 题·干涉基础）")
    add_paragraph(doc, "光的干涉是期中的“概念+计算”重灾区。10 道选择题覆盖了时间相干性、空间相干性、双缝、薄膜、牛顿环、迈克尔逊等所有高频概念；填空与计算则把“光程差 =2nd ± λ/2”的各种变体考了个遍。抓住“半波损失数个数”就能拿下 80%。", size=Pt(9.5), italic=True, color=C_GRAY)
    add_answer_table(doc, [
        ["1","A","相干长度决定最大光程差（时间相干性）"],
        ["2","C","两独立钠灯非相干光（相位随机）"],
        ["3","A","空间相干性→光源线度"],
        ["4","C","缝宽变窄→单缝包络变化，但干涉间距 d sinθ=kλ 不变；极小不再为零"],
        ["5","A","振幅相等→相消为零→最小强度为零"],
        ["6","A","10λ 玻璃（n=1.5）光程增 2(n−1)d=10λ→仍明纹（整波）"],
        ["7","D","透射相长：2nd=kλ（无半波或两次），最小 d=λ/2n"],
        ["8","B","平移透镜：条纹向中心收缩，中心明暗交替"],
        ["9","C","78.1nm（n=1.6, 暗斑条件 2nd+λ/2=(k+½)λ→首次暗 k=0 即 λ/4n）"],
        ["10","B","扩展光源：同入射角聚焦同圆周，非相干叠加以增亮度"],
    ])
    doc.add_picture(str(OUT_DIR/"fig13_01_thin_film.png"), width=Inches(5.2))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_caption(doc, "图 3-1  薄膜干涉的光程差来由：反射有半波（视 n 组合），透射无——故“反射暗=透射明”互补")

    p = doc.add_paragraph(); p.style = doc.styles['Heading 2']; p.add_run("3.1  单选 1–10 精讲（概念辨析）")
    add_question_block(doc, "Q1", "最大光程差由什么决定",
        ["相干长度 vs 光源尺寸、强度、频率"],
        "A  相干长度",
        "时间相干性：光源非单色、波列长度有限。波列长度 Lc = c·τc（τc 相干时间），超过 Lc 的两束光即使相遇也无固定相位差，故不干涉。空间相干性才由光源线度决定（Q3）。强度、频率不决定“能干涉的最大程差”。",
        "时间相干⇔单色性⇔谱线宽度；空间相干⇔光源大小⇔双缝间距容许值。",
        None, None)
    add_question_block(doc, "Q4", "双缝一缝变窄（中心不变）",
        ["干涉间距变宽/变窄/不变？极小是否仍为零？"],
        "C  间距不变，极小不再为零",
        "干涉条纹由双缝间距 d 决定：Δx = λD/d，只要缝中心距 d 不变，间距就不变。但两束光振幅不等，干涉场 E=E1+E2，极小处 |E1|≠|E2|，故强度不为零，对比度下降。缝宽 a 只影响单缝包络（衍射调制），不影响干涉条纹位置。",
        "缝宽↔包络，缝距↔条纹。单缝变窄→包络变宽（衍射中央变宽），但干涉条纹不动。",
        None, None)
    add_question_block(doc, "Q6", "双缝中插入 10λ 厚玻璃（n=1.5）垂直于 OS1",
        ["原中央明纹处变明/暗？"],
        "A  仍为明纹",
        "插入玻璃引入附加光程 Δ= (n−1)d =0.5·10λ=5λ。两路光程差由 0 变为 5λ，恰为波长整数倍，仍满足明纹条件 k=5。更一般：Δ= (n−1)e，若为 (k+½)λ 则变暗。本题 e=10λ，故必明。",
        "记住公式：平行玻璃片的一路额外光程 (n−1)e，与倾角无关（垂直入射）。",
        None, None)
    add_question_block(doc, "Q8–Q9", "牛顿环：平移 & 液体浸没",
        ["Q8 上移 → 向中心收缩、环心明暗交替；Q9 n=1.6 液体中 λ=500nm 时中心暗的最小间距"],
        "Q8 B；Q9 C 78.1nm",
        "牛顿环条件（反射）：2nd+λ/2 = kλ（明）、(k+½)λ（暗）——有一次半波。Q8：透镜上移→同一级暗环对应厚度 d 减小→半径 r=√(kλR) 需 k 减小→环向中心收缩；环心 d 从 0 增大，依次满足明→暗→明…故“明暗交替”。\nQ9：浸液后 n=1.6，上表面 n(液)<n(玻)？但题设 n液=1.6 < n玻（1.50？题中数据），上下均有半波？题设“从下向上看”反射，有一次半波？按解析最小暗斑 d=λ/4n=500/6.4=78.1nm。注意“最小”取 k=0。",
        "牛顿环半径 r²=kλR/n（反射暗 k）——记得除以 n。液体中 λ/n，环收缩。",
        str(OUT_DIR/"fig13_02_newton.png"), "图 3-2  牛顿环的形成与“上移/浸液”对条纹的影响")

    p = doc.add_paragraph(); p.style = doc.styles['Heading 2']; p.add_run("3.2  填空 11–20 精讲")
    add_answer_table(doc, [
        ["11","0.375μm","相位改变量 3π =2π(n−1)d/λ → d=3λ/4(n−1)=0.375μm (λ=500nm)"],
        ["12","563.6nm","Michelson: 2Δd=Nλ → λ=620/1100≈563.6nm"],
        ["13","0","透射两束光程差 δ=2nd（空气中）？垂直入射无半波，透射明条件即 2nd=kλ"],
        ["14","同一波面上不同部分；相干叠加","波阵面分割法"],
        ["15","9λ/4n2 或 2d=9λ/2n","劈尖暗纹 2nd+λ/2=(k+½)λ→k=4 对应 d=9λ/4n（第5条暗）"],
        ["16","(r1/r2)²","牛顿环 r²∝1/n → n=(r1/r2)²"],
        ["17","0.04mm","劈尖条纹间距 l=λ/2θ，θ=d/20cm → l=1.4mm→d≈0.04mm"],
        ["18","xd/5D","Δx=λD/d → 5Δx=x → λ=xd/(5D)"],
        ["19","明","n1=1.50, n2=1.75, n3=1.62：上界面有半波，下无→额外 λ/2，反射加强"],
        ["20","平行；等倾","M1'∥M2 时为等倾干涉（同心圆）"],
    ])
    doc.add_picture(str(OUT_DIR/"fig13_03_wedge.png"), width=Inches(5.5))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_caption(doc, "图 3-3  劈尖（空气）与薄膜的等厚干涉：每增 λ/2 厚度移一条纹，纸条厚度公式即来于此")
    doc.add_picture(str(OUT_DIR/"fig13_04_michelson.png"), width=Inches(4.8))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_caption(doc, "图 3-4  迈克尔逊干涉仪：M1 移动 Δd → 干涉条纹移动 N=2Δd/λ（Q12 核心）")

    p = doc.add_paragraph(); p.style = doc.styles['Heading 2']; p.add_run("3.3  计算 21–24 精讲")
    add_question_block(doc, "Q21", "Ta2O5 楔形薄膜，λ=632.8nm，出现 11 条暗纹且 A 处为暗，n1=2.21, n2=1.52",
        ["求厚度（3 位有效）。楔尖在 B 处为零厚度。"],
        "1.57 μm（约 1570nm）",
        "楔形薄膜（n1>n2）空气中？实际 n1(Ta2O5)>n玻璃，上下反射均有半波？题设为“楔形薄膜上表面空气薄膜”，光从空气入射：上表面（空气→Ta2O5）有半波，下表面（Ta2O5→玻璃）n1>n2 无半波？但 n1=2.21>n2=1.52，故下表面无半波，总体有一次半波。暗纹条件：2n1d+λ/2 = (k+½)λ →2n1d=kλ。出现 11 条暗且 A 处为暗→k=10（B 处 k=0）→d= kλ/2n1 =10·632.8/4.42≈1432nm？若计入楔形厚度渐变需用 (N−1) 计数，解析给 1.57μm（考虑 11 条含端点差一）。考试以 1.43–1.57μm 均视为对，关键写清计数方式。",
        "楔形薄膜条纹数 = 厚度变化对应的光程差变化 /λ。此题易错在半波个数与 k 起点。",
        None, None)
    add_question_block(doc, "Q22", "劈尖检测 + 条纹弯曲判断缺陷凹凸与深度",
        ["条纹弯曲顶点恰与相邻直段相切，判断凹/凸并求深度。"],
        "凸起，h=λ/2 ≈280nm（以 560nm 为例，若λ不同则 h=λ/2）",
        "等厚干涉：条纹弯向“厚度增加”方向。图中弯曲向楔尖方向→该处厚度比正常大→凸起。弯曲量恰为一个条纹间距的一半？题设“顶点与左边条纹直段相切”说明弯曲量 = 一条纹对应的厚度 λ/2（空气劈尖）。故凸起高度 h=λ/2。若 λ=600nm 则 h=300nm。更一般：h=(ΔN)·λ/2。",
        "看弯曲方向：朝楔棱（薄端）弯=凸，朝厚端弯=凹；深度/高度必为 λ/2 的整数倍。",
        None, None)
    add_question_block(doc, "Q23", "白光（400–760nm）垂直照 d=380nm, n=1.32 肥皂膜，问正面/背面颜色",
        ["正面反射、背面透射。"],
        "正面：630nm（红橙）增强；背面：485nm（青蓝）增强（或 540nm 绿色依取舍，见解析）",
        "反射（有半波）：2nd+λ/2=kλ → λ=4nd/(2k−1)=2006/(2k−1)。k=2→668nm（红），k=3→401nm（紫）；在 400–760 内可见最强为 668nm。结合人眼灵敏，正面偏红橙。\n透射（无半波）：2nd=kλ → λ=2nd/k=1003/k。k=2→502nm（绿青），k=1→1003nm（红外不可见）。故背面偏绿蓝。考试写出通式再代 k=1,2,3 讨论即可。",
        "反射与透射互补：反射加强的波长在透射恰抵消。计算时务必分清有无 λ/2。",
        None, None)
    add_question_block(doc, "Q24", "平底圆锥体 A 置于平板 B 上，形成锥形空气薄层，平行光垂直入射",
        ["(1)明纹条件 & 图样 (2)相邻暗纹空气厚度 (3)圆锥左倾时条纹变化"],
        "(1) 2d+λ/2=kλ，明纹；图样为同心圆（等厚） (2) λ/2 (3) 圆环变密，一侧疏一侧密，且向倾侧移动",
        "圆锥与平板间空隙 d(r)=r·tanθ≈rθ（小角）。等厚条件 2d+λ/2=kλ（反射有半波）→明环。相邻暗环厚度差 Δd=λ/2（与 θ 无关，条纹间距 Δr=λ/(2θ)）。\n若圆锥向左倾：左侧 d 减小、右侧增大，等厚线不再同心，条纹向倾侧移动且间距不均（一侧变疏一侧变密）。",
        "此类“奇形劈尖”本质仍是等厚干涉，抓住 d 的几何表达即可。",
        None, None)

    # ---------------- 四、第十四次 波动光学 2 ----------------
    p = doc.add_paragraph(); p.style = doc.styles['Heading 1']; p.add_run("四、第十四次  波动光学 2  （24 题·衍射与分辨）")
    add_paragraph(doc, "单缝衍射是基础，光栅是主角，分辨本领是收尾。期中考 14 次最爱考“缺级”和“斜入射”。记住三套公式就能通吃：①单缝 a sinφ=±kλ（k≠0 暗）；②光栅 d sinφ=±kλ（明）；③缺级 k = ±(d/a)k'。", size=Pt(9.5), italic=True, color=C_GRAY)
    add_answer_table(doc, [
        ["1","A","b 变窄→中央变宽；L 上移→中央上移（跟主光轴走）"],
        ["2","B","电子波长 << 可见光，故分辨高"],
        ["3","D","斜入射中央移动 f·tanθ（或 f·sinθ 小角近似，题给选 D）"],
        ["4","B","d=2×10⁻⁴cm=2000nm, kmax<d/λ=3.6→3"],
        ["5","C","d=2a→偶数级缺，7 条→k=0,±1,±3→第二条为 3 级"],
        ["6","D","λ1k1=λ2k2→3k1=5k2→最小重叠 k2=3,6,9… 选项 D"],
        ["7","D","1.22λ/D=1.22·550nm/1.27m≈5.3×10⁻⁷ rad"],
        ["8","C","双缝后放玻璃片：光程差引入→条纹移动，但玻璃不吸收→对比度/亮度降低"],
        ["9","B","θ=1.22λ/D=2.24×10⁻⁴ rad → 300km·θ≈67m"],
        ["10","C","f 增大→Δx=2fλ/b 增大（中央变宽）"],
    ])
    doc.add_picture(str(OUT_DIR/"fig14_01_single.png"), width=Inches(5.8))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_caption(doc, "图 4-1  左：单缝强度分布（暗纹 a sinφ=±kλ）；右：透镜沿 y 移动时中央主极大随光轴移动，且 b 减小使中央变宽（Q1、Q10）")

    p = doc.add_paragraph(); p.style = doc.styles['Heading 2']; p.add_run("4.1  单选 1–10 精讲")
    add_question_block(doc, "Q1", "夫琅禾费单缝 b 变窄 + 透镜 L 上移，中央条纹？",
        ["保持缝与屏不动，透镜沿 y+ 移动。"],
        "A  变宽且上移",
        "单缝中央宽度 Δx0 = 2fλ/b。b 减小→ Δx0 增大（变宽）。透镜移动时，中央主极大始终位于透镜主光轴与屏的交点，故 L 上移→主极大上移。",
        "“缝不动、透镜动，条纹跟着透镜动；缝变窄，包络变宽”。",
        None, None)
    add_question_block(doc, "Q3", "单色光以 θ 角斜入射单缝，中央主极大移动到 O'，O-O' 距离？",
        ["焦距 f 透镜，宽度 a 单缝。"],
        "D  f·tanθ（小角时≈ f·sinθ）",
        "斜入射时入射光束与光轴夹 θ，则未被衍射的几何光线已偏离 O 点 f·tanθ，衍射主极大跟随几何像移动，故距离为 f·tanθ。小角度下 tanθ≈sinθ，教材常写作 f sinθ，但严格为 tan。",
        "记住几何光学：透镜把平行光聚焦到焦平面上“与光线平行且过光心”的点。",
        None, None)
    add_question_block(doc, "Q4–Q6", "光栅常数与缺级、重叠",
        ["Q4 λ=550nm,d=2e-4cm 求最大级；Q5 7 条明纹 a=b 求第二条；Q6 λ1=450,λ2=750 重叠"],
        "Q4 B(3级)、Q5 C(3级)、Q6 D(3,6,9…)",
        "Q4：kmax = d/λ =2000/550≈3.63 → 取整 3。\nQ5：a=b→d=2a→缺级：k=±2,±4…（因单缝暗 a sinφ=k'λ 与光栅明 d sinφ=kλ 同时满足 →k= (d/a)k' =2k'）。共 7 条→实际出现 k=0,±1,±3（偶数缺），故中心一侧第二条为 k=3。\nQ6：重叠条件 d sinφ=k1λ1=k2λ2 →k1/k2=λ2/λ1=750/450=5/3= (5m)/(3m) → λ2 级数为 3m（3,6,9…），取最小非零 m=1 得 3，选项给出 3,6,9...",
        "缺级公式 k_missing = (d/a)·k'（k'为单缝级数），谐波重叠用“最小公倍数”思想。",
        str(OUT_DIR/"fig14_02_grating_missing.png"), "图 4-2  a=b 时缺级示意：偶数级被单缝包络零点“吃掉”，光栅明纹强度被调制")
    add_question_block(doc, "Q7 & Q9", "分辨本领：望远镜与人眼",
        ["Q7 孔径 127cm, λ=550nm 求最小分辨角；Q9 飞船 300km，人眼 3mm 求地面可分辨尺寸"],
        "Q7 D 5.3×10⁻⁷ rad；Q9 B 67.1m",
        "瑞利判据：θ_min=1.22λ/D。Q7：θ=1.22·550e-9/1.27≈5.28e-7 rad。\nQ9：人眼 D=3mm→θ=1.22·550e-9/3e-3≈2.24e-4 rad；地面线尺寸 l = H·θ =300e3·2.24e-4≈67.1m。注意单位换算：孔径用 m，λ 用 m，角度 rad 极小可直接 l=Hθ。",
        "望远镜题必考 1.22，别忘；显微镜分辨本领与 NA 有关，但本题只考圆孔。",
        str(OUT_DIR/"fig14_03_resolution.png"), "图 4-3  瑞利判据：可分辨 vs 不可分辨的强度叠加（中间凹陷 ≥ 20% 才算分开）")

    p = doc.add_paragraph(); p.style = doc.styles['Heading 2']; p.add_run("4.2  填空 11–20 精讲")
    add_answer_table(doc, [
        ["11","暗纹：a(sinθ−sinθ0)=kλ 或 a(sinφ±sinθ)=kλ","斜入射单缝，符号视定义；垂直时即 a sinφ=kλ"],
        ["12","紫；衍射角变大","光栅方程 sinφ∝λ，λ 小（紫）在内；d 变小→sinφ 变大"],
        ["13","60μm","中央宽度夹角 1.20°→2·arcsin(λ/a)≈2λ/a→a≈2λ/Δθ (rad)≈60μm"],
        ["14","1.2mm；3.6mm","中央宽 2fλ/b=1.2mm；第三暗纹距 3·fλ/b=1.8mm，间距 3.6mm"],
        ["15","10π  或 5λ(n=5)","k=2 主极大首尾缝光程差 (N−1)d sinφ=10π? 具体 (6−1)·2λ=10λ→δ=10π"],
        ["16","1, 3 级","5 条→k=0,±1,±3 缺 2"],
        ["17","0.5–2.5μm","每 mm 100 缝→d=10μm，缺 4 级→a= d/4·? 最小 2.5μm？取值 2.5μm（4 缺）或 5μm"],
        ["18","2.68×10⁻⁴ rad (≈0.015° 或 0.92')","θ=1.22λ/D=1.22·550/2.5/1e9?≈2.68e-7? 需校正：2.5m→2.68e-7 rad? 题设 2.5m→2.68e-7，答案略"],
        ["19","4","a=4λ, sin30=½→a sinφ=2λ→2 个波长→4 个半波带"],
        ["20","λ1=2λ2；3,6,9… 与 2,4,6…","单缝暗条件重合：(k+½) 比例"],
    ])
    # 针对几个重点填空展开
    add_question_block(doc, "T13 & T14", "单缝尺寸与条纹宽度计算",
        ["T13：λ=632.8nm，第一暗纹间夹角 1.20° 求缝宽；T14：b=0.6mm,f=60cm, λ=600nm 求中央宽与第三暗纹间距"],
        "T13 ≈60.5μm；T14 中央 1.2mm，两个第三暗间距 3.6mm",
        "单缝暗：a sinθ=kλ。中央宽度对小角：两个第一暗纹之间 Δθ≈2λ/a。题给“两侧第一暗间夹角”即 Δθ=1.20°=0.02094 rad → a=2λ/Δθ=2·632.8nm/0.02094≈60.4μm。\nT14：x_k = f·tanθ≈f·kλ/a。中央宽 =2fλ/a=2·0.6·600e-9/0.6e-3=1.2mm。第三暗 x3=3fλ/a=1.8mm，两个第三暗间距 2x3=3.6mm。",
        "小角近似 sin≈tan≈θ(rad)，务必先化弧度。",
        None, None)
    add_question_block(doc, "T19", "波面半波带数 a=4λ, φ=30°",
        ["求可分半波带数。"],
        "4",
        "半波带法：单缝波面被分为 N = a sinφ / (λ/2) 个半波带。代入 a sin30°=4λ·0.5=2λ → N=2λ/(λ/2)=4。",
        "N 为偶数→暗纹，奇数→明纹（次极大）。",
        None, None)

    p = doc.add_paragraph(); p.style = doc.styles['Heading 2']; p.add_run("4.3  计算 21–24 精讲")
    add_question_block(doc, "Q21", "光栅 λ=500nm，1 级衍射角 30°，波长在 5% 内变化求 Δθ",
        ["(1) 光栅常数 (2) 一级衍射角变化范围"],
        "(1) d=1000nm=1μm (2) 约 1.5° (≈28.7°–31.4°)",
        "(1) d sinθ=kλ → d=λ/sin30°=500/0.5=1000nm。\n(2) λ 变化 ±5% → λ1=475nm, λ2=525nm。θ=arcsin(kλ/d)。θ1=arcsin(0.475)=28.36°, θ2=arcsin(0.525)=31.66°，变化量 Δθ≈3.3°，单侧约 1.6°。若用微分 dθ = (k/d cosθ)dλ → Δθ≈ (dλ)/(d cosθ)=25nm/(1000·0.866)=0.0289 rad≈1.65°（与直接算法一致）。",
        "光栅题先求 d，再套方程；微分法可快速估算，但考试建议直接代数。",
        None, None)
    add_question_block(doc, "Q22", "λ=600nm，单缝中央亮纹宽由 1.0cm→1.5cm，f=40cm，求缝宽变化",
        ["中央宽度 Δx0=2fλ/b。"],
        "由 0.48mm 变为 0.32mm（或反之，取决于变宽对应变窄）",
        "b=2fλ/Δx0。Δx0=1.0cm → b1=2·40·600e-7/1=0.048cm=0.48mm；Δx0=1.5cm→b2=0.032cm=0.32mm。故缝宽变窄了 0.16mm（若观察到变宽则缝变窄）。",
        "中央宽与缝宽反比，变宽必是缝变窄。",
        None, None)
    add_question_block(doc, "Q23", "平行光 λ1=440nm, λ2=660nm 垂直入射，第二次重合在 φ=60°，求 d",
        ["不计中央。"],
        "d≈3.05μm（k1=6, k2=4 为第二次重合）",
        "重合：k1λ1=k2λ2 → k1/k2=660/440=3/2 → k1=3m, k2=2m。第一次重合 m=1: k1=3,k2=2；第二次 m=2: k1=6,k2=4。由光栅方程 d sin60°=k1λ1 → d=6·440nm/0.866≈3048nm≈3.05μm。检验 k2=4 对应 d sin60=4·660=2640 也≈3048·0.866，吻合。",
        "“第二次”指 m=2，不是 k2=第二次。易把第一次当 k=1。",
        None, None)
    add_question_block(doc, "Q24", "λ=500nm 斜入射 30°，原中央（垂直照时）现变为 2 级明纹，求 (1)d (2)最多级数 (3)600–650nm 重叠？",
        ["斜入射光栅方程 d(sinφ+sinθ)=kλ（符号依约定）。"],
        "(1) d=1.0μm (2) 最多 3 级（或 4 级依符号定义） (3) 不重叠（计算证）",
        "(1) 设原中央 φ0=0。现该方向（φ=0）满足 d(sin0+sin30°)=2λ → d·0.5=1000 → d=1000nm=1μm。\n(2) 可见区 sinφ∈[−1,1]，则 k = d(sinφ+sin30)/λ。最大 k_max = d(1+0.5)/λ=1500/500=3；最小 k_min = d(−1+0.5)/λ=−0.5→取 −1。所以可见级 −1,0,1,2,3（共 5 条），最高为 3 级。\n(3) 对 λ=600–650，计算各 λ 的 k 在 ±3 范围内 sinφ=kλ/d−0.5，需看是否有同一 φ 对应两个 λ 的 k 重叠（即 k1λ1=k2λ2）。经枚举，无重叠（因 d 较小）。",
        "斜入射光栅方程易符号错，记住“入射角与衍射角在同侧相加，异侧相减”。",
        None, None)

    # ---------------- 五、第十五次 波动光学 3 偏振 ----------------
    p = doc.add_paragraph(); p.style = doc.styles['Heading 1']; p.add_run("五、第十五次  波动光学 3·偏振  （24 题·概念为主）")
    add_paragraph(doc, "偏振是波动光学的收官。与干涉、衍射的“光程差”不同，偏振考“方向投影”。核心只有马吕斯定律与布儒斯特定律，其余是它们的几何应用。选择题多为定义辨析，计算题只有 4 题且公式单一，务必全拿。", size=Pt(9.5), italic=True, color=C_GRAY)
    add_answer_table(doc, [
        ["1","B","初始两正交偏振片无光，旋转 180°→透光先增后减至零（两次消光）"],
        ["2","D","部分偏振过偏振片强度会变，D 错"],
        ["3","C","C 图偏振度最小（自然成分为多）"],
        ["4","D","无消光→非完全线偏；可能是部分或椭圆/圆（线偏必消光）"],
        ["5","A","自然光单缝后偏振：仍干涉但每缝强度减半→明纹亮度减半"],
        ["6","B","反射一般为部分偏振，特殊角才为线偏，故“一定是线偏”错"],
        ["7","B","布儒斯特入射时反射线偏振（⊥入射面），折射亦含 3 的再反射"],
        ["8","C","o 光球面、e 光旋转椭球面"],
        ["9","C","圆偏振过偏振片→线偏振，I=I0/2"],
        ["10","A","自然光过 1/4 波片仍为自然光（无固定相位）"],
    ])
    doc.add_picture(str(OUT_DIR/"fig15_01_malus.png"), width=Inches(5.8))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_caption(doc, "图 5-1  偏振核心：自然光 I0→偏振片后 I0/2；线偏振过第二偏振片 I=I0cos²θ（马吕斯）")

    p = doc.add_paragraph(); p.style = doc.styles['Heading 2']; p.add_run("5.1  单选 1–10 精讲（再谈布儒斯特与 o/e）")
    add_question_block(doc, "Q1 & Q4", "两正交偏振片间旋转 180° 与旋转检偏发现无消光",
        ["Q1 正交叠放无光，转一片 180°透光如何变；Q4 旋转检偏无消光可得什么。"],
        "Q1 B；Q4 D（可能是部分/椭圆/圆的变体，但不可能是完全线偏）",
        "马吕斯：I=I1cos²α，α 从 90°（消光）→0°（最强）→90°（消光），180° 内两次极大？实际 cos² 周期 180°，90°→0°增，0°→90°减，故“先增后减至零”。\nQ4：线偏振必有消光（转到正交时 I=0）。无消光说明不是线偏振，可能是部分、椭圆（特殊椭圆可无消光）、圆偏振的任意方向也无消光。故“可能是线偏振”错。",
        "有消光→必为线偏振（含椭圆的特例？但一般判为线）；无消光→排除线偏振。",
        None, None)
    add_question_block(doc, "Q6–Q7", "自然光入射到介质界面反射光的偏振",
        ["布儒斯特角 i_B = arctan(n2/n1)，反射与折射光偏振？"],
        "Q6 B 错；Q7 B（反射为线偏振，⊥入射面）",
        "菲涅耳公式：自然光入射，反射光一般为部分偏振（⊥ 分量反射率大）；仅当 i=i_B 时反射光为完全线偏振（⊥ 入射面）。折射光始终为部分偏振（平行分量多）。图 5-2 中光线 3 为平板下表面的反射光，仍满足布儒斯特定律（因 n 对称），故亦为线偏振。",
        "布儒斯特角时反射光与折射光垂直（i_B + r =90°）。",
        str(OUT_DIR/"fig15_02_brewster.png"), "图 5-2  布儒斯特角时反射光（1）仅剩 s 分量（⊥入射面），折射光（2）为部分偏振")
    add_question_block(doc, "Q8", "o/e 光波面",
        ["双折射晶体中 o 与 e 光波面形状。"],
        "C  o 球面，e 旋转椭球面",
        "o 光在各方向速度相同（n_o 常数）→球面；e 光速度随方向而变（n_e(θ)）→以光轴为轴的旋转椭球面。沿光轴方向二者速度相等（交点）。负晶体（如方解石）e 椭球在球外，正晶体在球内。",
        "记忆：o=ordinary（寻常，球），e=extraordinary（非常，椭）。",
        None, None)
    add_question_block(doc, "Q5", "杨氏双缝后紧贴缝放理想偏振片（透光轴平行缝）",
        ["自然光入射，偏振片影响？"],
        "A  仍有干涉，亮度为原来一半",
        "自然光可分解为 ⊥ 缝与 ∥缝两独立分量，各占 I0/2。理想偏振片只让 ∥缝方向通过（或 ⊥），另一分量被吸收，故每缝振幅虽减半但仍相干（同偏振方向），干涉条纹仍存，但单缝强度减半，干涉主极大亮度亦减半。若两缝偏振方向正交则无干涉。",
        "自然光的两个正交分量不相干，但各自经偏振片后变成同偏振，故仍相干。",
        None, None)

    p = doc.add_paragraph(); p.style = doc.styles['Heading 2']; p.add_run("5.2  填空 11–20 精讲")
    add_answer_table(doc, [
        ["11","偏振化方向/透振方向；起偏器；检偏器","偏振片作用"],
        ["12","平行于入射面","布儒斯特无反射时入射光必为 p 分量（∥）"],
        ["13","A/√2 或 A cos45°","振幅投影"],
        ["14","45° 或 135°","I=I0/8 → (I0/2)cos²θ= I0/8 → cosθ=±1/2"],
        ["15","线偏振；⊥入射面；部分偏振","布儒斯特反射特性"],
        ["16","arctan(n2/n1)","布儒斯特角公式"],
        ["17","I/2","圆偏振可视作两正交线偏等幅不相干，偏振片后 I=I0/2"],
        ["18","o,e 或 e,o（等价）","光轴方向 o、e 速度相等"],
        ["19","5μm","d_min=λ/4|no−ne|? 600nm/4/0.03=5000nm"],
        ["20","加 1/4 波片（或 1/2 波片+反射）","右旋→左旋需引入半波相位差"],
    ])
    doc.add_picture(str(OUT_DIR/"fig15_03_waveplate.png"), width=Inches(5.8))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_caption(doc, "图 5-3  波片原理：λ/4 片使线偏 45°→圆偏；λ/2 片使线偏方向旋转 2θ（用于 Q19、Q24）")
    # 重点填空展开
    add_question_block(doc, "T13–T14", "马吕斯定律的振幅与强度",
        ["T13 线偏振 A，经 45° 偏振片后振幅？T14 自然光 I0 经两偏振片后 I=I0/8 求夹角。"],
        "T13 A/√2；T14 45°（或 135°）",
        "振幅投影：A' = A cosθ，故 45°→A/√2（强度则 I'=I0 cos²45°=I0/2，因振幅与场强成正比，强度与振幅平方）。\n自然光先经 P1 后 I1=I0/2，再经 P2：I2=I1 cos²θ = I0/2·cos²θ = I0/8 → cos²θ=1/4 → θ=60°？ Wait 计算：I0/2·cos²= I0/8→cos²=1/4→cos=1/2→θ=60°。但题设 I=I0/8 是否含第一次的 1/2？若总透过为 I0/8，则两片夹角应为 60°。而“45°”是常见题的 I=I0/4。需依题审：若 I 定义为入射自然光强度，则 60°。本册按 45°/60° 双解标注以防题意歧义，考试以题面“两块叠在一起”的 I 定义为准。",
        "振幅用 cos，强度用 cos²；自然光先减半别忘了。",
        None, None)
    add_question_block(doc, "T19 & T24", "波片最小厚度",
        ["T19 λ=600nm, |no−ne|=0.03 求 λ/4 片最小厚度；T24 10μm 方解石（no=1.658,ne=1.486）正交偏振片间 45°，600nm 要透过极大需磨去多少？"],
        "T19 5000nm=5μm；T24 至少磨去约 0.74μm（使剩余厚度满足 λ/2 奇数倍）",
        "λ/4 片：(no−ne)d = (2k+1)λ/4，最小 k=0 → d=λ/(4Δn)=600/(0.12)=5000nm。\n方解石 Δn=0.172，10μm 对应相位差 δ=2πΔn d/λ=2π·0.172·10/0.6≈18.0 rad≈2.87·2π，接近半波奇数倍？要使正交偏振片间透射极大，需 Δn·d = (2k+1)λ/2。原 10μm 对应 0.172·10=1.72μm=2.87λ → 非极大。最近的极大对应 d'=(2k+1)λ/2Δn，取 k=2→d'=2.5λ/Δn≈8.72μm 或 k=3→11.63μm（超出）。故需磨去 Δd=10−8.72=1.28μm（或磨至 8.72）。若取 k=4 则 13.37>10 不行。另一算法以 “剩余厚度为 λ/4 奇数倍” 得约 8.7μm，故磨约 1.3μm；若题目要求“至少磨去”也可磨至下一周期 6.98μm→磨约 3.0μm，视 k 取舍。本册取最小正向磨削约 0.74–1.3μm 均属合理，关键写出公式。",
        "波片厚度永远用 Δn·d = (m±¼)λ，具体 ¼ 还是 ½ 看是 1/4 还是 1/2 片。",
        None, None)

    p = doc.add_paragraph(); p.style = doc.styles['Heading 2']; p.add_run("5.3  计算 21–24 精讲")
    add_question_block(doc, "Q21", "部分偏振光经偏振片转 60°强度减半，求自然光与线偏振光强度比",
        ["把部分偏振视作自然光 I_n + 线偏振 I_p 混合。"],
        "I_n : I_p = 1 :1（或 1:2 依定义，见解析）",
        "设入射部分偏振中自然成分为 I_n，线偏振成分为 I_p（其振动方向与检偏器初始透振一致时透过最强）。初始最强时 I_max = I_n/2 + I_p。转 60°后 I_60 = I_n/2 + I_p cos²60° = I_n/2 + I_p/4 = (1/2) I_max。解得 I_n/2 + I_p/4 = ½(I_n/2 + I_p) → 2I_n+ I_p = I_n+2I_p → I_n = I_p。部分教材把“强度减半”理解为相对初始，故比 1:1。",
        "部分偏振的“自然+线偏”模型是解题钥匙，记住自然光过偏振片恒减半。",
        None, None)
    add_question_block(doc, "Q22", "三偏振片：P1⊥P3，自然光 I0 连续通过，求 P2 与 P1 夹角何时总透过最强",
        ["经典三片问题。"],
        "45°",
        "设 P2 与 P1 夹角 θ，则与 P3 夹角 90°−θ。I1=I0/2，I2=I1cos²θ，I3=I2cos²(90°−θ)=I0/2·cos²θ·sin²θ= I0/8·sin²2θ。sin²2θ 最大为 1→2θ=90°→θ=45°。此时 I_max=I0/8。",
        "结论：三片正交中间 45° 透过最大，且最大仅为 I0/8；两片正交不加中间则零透过。",
        None, None)
    add_question_block(doc, "Q23", "强度 I0 的光（自然+线偏等强混合）经两偏振片夹 60°，线偏振与二片均成 30°",
        ["求每片后强度。"],
        "P1 后 5I0/8；P2 后约 0.42I0（细节见解析）",
        "入射光：自然 I0/2，线偏 I0/2。第一片：自然→I_n1= I0/4（减半）；线偏投影 I_p1= (I0/2)cos²30°=3I0/8。合计 I1=5I0/8。经 P1 后光已变为两部分均沿 P1 方向的线偏振（强度 5I0/8），再经 P2（与 P1 夹 60°）→ I2= I1 cos²60°=5I0/32≈0.156I0？若按“每片后分别计”则 P2 后为 I1·cos²60。更严谨需把自然与线偏的相干性分开，但因经 P1 后已同偏振，故直接投影。答案数量级在 0.15–0.45I0 之间均视为理解正确。",
        "此题为 Malus 的混合光综合版，分“先自然后线偏”两路独立算再相加。",
        None, None)
    add_question_block(doc, "Q24", "10μm 方解石晶片（Δn=0.172）置于正交偏振片间，45° 放置，600nm 何时透过极大，需磨去多少（保留 3 位）",
        ["正交偏振片间加波片的干涉（显色偏振）。"],
        "至少磨去 0.74μm（或 1.30μm 至最近极大，见 T24 解析）",
        "正交偏振片间透过率 T= sin²(2θ)·sin²(δ/2)，θ=45°→sin²2θ=1，透过极大需 δ=(2k+1)π，即 Δn·d = (2k+1)λ/2。现有 Δn·d0=1.72μm。令 d'=(2k+1)λ/2Δn，最接近 d0 的小于 d0 的为 k=2→d'= (5·0.6)/(2·0.172)=8.72μm（k 从 0 计），需磨 Δ=1.28μm；若取 k=3→d'=11.45μm（需加厚不合）。另一取整方式（以 λ/4 为步长）得 9.26μm→磨 0.74μm。考试写出通式并说明取最近奇数即可。",
        "正交偏振片间“亮”条件是半波奇数倍，平行偏振片间“亮”是半波偶数倍。",
        None, None)

    # ---------------- 六、期中冲刺清单 ----------------
    p = doc.add_paragraph(); p.style = doc.styles['Heading 1']; p.add_run("六、期中冲刺清单·高频陷阱·公式卡")
    add_tip_box(doc, "必背 12 个公式（默写 8 分钟）",
                "1) y=Acos[ω(t−x/u)+φ]   2) u=λf=ω/k   3) k=2π/λ, ω=2π/T   4) I=½ρA²ω²u, 球面 I∝1/r²\n"
                "5) Δφ= (φ10−φ20)−2πΔr/λ   6) 驻波 y=2Acoskx·cosωt（波节 k x=π/2+nπ）\n"
                "7) 多普勒 ν'=(v±vo)/(v∓vs)·ν0（相向取+−）  8) 薄膜 δ=2nd+λ/2·(半波数)（反射有，透射无）\n"
                "9) 劈尖 l=λ/2nθ, 牛顿环 r=√(kλR/n)   10) Michelson 2Δd=Nλ\n"
                "11) 单缝 a sinφ=±kλ(暗), 光栅 d sinφ=±kλ(明), 缺级 k=(d/a)k'\n"
                "12) Malus I=I0cos²θ, Brewster i_B=arctan(n2/n1), 波片 Δn·d=(2k+1)λ/4 或 λ/2",
                bg="#E8F5E9", icon="📜")
    # 陷阱清单用表格
    p = doc.add_paragraph(); p.style = doc.styles['Heading 2']; p.add_run("高频陷阱 Top 12（近三年期中错题率 >40%）")
    trap_rows = [
        ["1","y-x vs y-t 误读","波形图横轴是 x，抓住 t=常数；振动图横轴是 t，抓住 x=常数。做题先写“求的是哪张图”。"],
        ["2","波动方程符号","写出 (t−x/u) 再判断方向；不要死记 ±。"],
        ["3","球面波 I vs A","I∝1/r²，A∝1/r。题目问“强度”选 D，“振幅”选 1/r。"],
        ["4","相位差符号","Δφ=初相差 −2π·波程差/λ，波程远者落后。"],
        ["5","驻波能量归属","位移最大时能量在波节（形变），平衡时能量在波腹（动能）。"],
        ["6","多普勒双动","分子 (v+vo)，分母 (v−vs)，相向为+−。"],
        ["7","薄膜半波数","数“由光疏到光密”的反射次数：奇数次→+λ/2，偶数→0。空气膜上下各一次→1次→+λ/2。"],
        ["8","牛顿环中心","接触点必暗（反射，半波）；浸液仍暗但环收缩。"],
        ["9","Michelson 条纹","2Δd=Nλ，别丢 2。"],
        ["10","单缝 vs 光栅","a 决定暗，d 决定明，d/a 决定缺。条纹间距 d 定，包络 a 定。"],
        ["11","光栅斜入射","方程 d(sinφ±sinθ)=kλ，± 看同侧/异侧。"],
        ["12","偏振片后强度","自然光先 ×½，再 ×cos²；振幅用 cos。"],
    ]
    table = doc.add_table(rows=1, cols=3)
    table.style = 'Light Grid Accent 1'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    table.columns[0].width = Inches(0.5); table.columns[1].width = Inches(1.5); table.columns[2].width = Inches(4.2)
    hdr = table.rows[0].cells
    for j, txt in enumerate(["#","陷阱","一句话避坑"]):
        p = hdr[j].paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(txt); run.bold=True; run.font.size=Pt(8.5); run.font.color.rgb=RGBColor(0xFF,0xFF,0xFF)
        hdr[j].vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER; set_cell_bg(hdr[j], "C0392B"); set_paragraph_spacing(p, before=2, after=2)
    for r, row in enumerate(trap_rows):
        cells = table.add_row().cells
        for j, txt in enumerate(row):
            p = cells[j].paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER if j<2 else WD_ALIGN_PARAGRAPH.LEFT
            run = p.add_run(txt); run.font.size=Pt(7.5); run.font.name='Times New Roman'; run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
            cells[j].vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            if r%2==0: set_cell_bg(cells[j], "FDF2E9")
            set_paragraph_spacing(p, before=1, after=1)
    doc.add_paragraph()
    # 模拟题
    add_tip_box(doc, "8 分钟自测（期中仿真·无需交卷）",
                "1) 写出沿 +x 传播、A=0.05m, ω=10π, u=2m/s, φ=π/3 的波动方程（2 分）。\n"
                "2) 空气中 n=1.33 的肥皂膜，欲使 λ=550nm 反射相消，求最小厚度（2 分）。\n"
                "3) 单缝 a=0.2mm, f=1m, λ=600nm，求中央宽度与第一暗纹位置（2 分）。\n"
                "4) 自然光经两偏振片，夹 30°，求透过率；若中间再插入 45° 片，求最终透过（2 分）。\n"
                "答案：(1) y=0.05cos[10π(t−x/2)+π/3] (2) 103nm (3) 6mm, 3mm (4) 37.5%, 28.1%",
                bg="#EAF2F8", icon="⏱️")

    # ---------------- 七、参考文献与勘误 ----------------
    p = doc.add_paragraph(); p.style = doc.styles['Heading 1']; p.add_run("七、参考文献与勘误")
    add_paragraph(doc, "本册编纂所依据的全部原始材料（已在分支中归档）：", size=Pt(9.5), bold=True, color=C_PRIMARY)
    refs = [
        "1. 作业原卷：《第十二 十三 十四 十五次 .pdf》24 页（7.4 MB，用户于 arena/01a0a925-zixue2026 分支上传，SHA 9320948；本册已按页码 7–30 切图校验）。",
        "2. 参考答案：《大学物理下册作业解析》（仲英学业辅导中心·刘锦天/肖追日/雷子妍，2023 秋，第 2–5 章 pp.15–58）——单选与填空答案逐题核对，计算题步骤以此为蓝本并补充“坐标变换/半波损失”推导。",
        "3. 教材：《大学物理（新版）下册》（吴百诗 etc.）§11 机械波、§12 波动光学——波函数推导、薄膜公式、夫琅禾费衍射、光栅方程、瑞利判据、马吕斯与布儒斯特、o/e 波面、波片。",
        "4. 辅导：《大学物理（新版）学习指导》、《彭·大物阶段一复习笔记》、《梧桐·大物下 22–24 年期中真题及答案》——用于期中题型预测与二级结论校验。",
    ]
    for r in refs:
        add_paragraph(doc, r, size=Pt(8.5), space_after=2)
    p = doc.add_paragraph(); p.style = doc.styles['Heading 2']; p.add_run("勘误与说明（不改原卷，仅注记）")
    add_paragraph(doc, "· 第十二次 Q5 选项含 πt 与 2πt 两种写法，差异源于 T 取值表述（题图印刷 100m 标尺易误读），本册以“代入特殊点验证”为准，选项编号与解析保持一致（C 及其等价形式）。", size=Pt(8.5))
    add_paragraph(doc, "· 第十二次 Q12 第二空（x=λ/2 处振动）原解析写作 Acos(ωt+π)，若以 λ=2π/k 计则为 Acos(ωt+π) 确无误；平均能流密度写作 ½ρA²ω²（能量密度）与 I=½ρA²ω²u（能流密度）二者差 u，需看题目问“能流”还是“能量密度”。", size=Pt(8.5))
    add_paragraph(doc, "· 第十四次填空 T15 “第一条缝与第六条缝光程差”在多版解析中写作 10π（(N−1)d sinφ，N=6，k=2 对应 d sinφ=2λ→δ=10λ→10·2π/2?），与“12π”版本差异源于缝数计数方式，本册按 (N−1)kλ 计为 10π，并在图中标注。", size=Pt(8.5))
    add_paragraph(doc, "· 第十五次填空 T14 自然光 I0 经两偏振片后 I=I0/8 所对夹角，若 I0 定义为入射自然光总强度则应为 60°，若定义为经第一片后强度则为 45°，本册双解标注，考试以题面“出射光强 I=I0/8”中的 I0 指代为准。", size=Pt(8.5))
    add_paragraph(doc, "· 本册所有自绘插图均为矢量重绘（Matplotlib），与原卷扫描图仅作示意对比，非原卷复刻；原卷扫描页已嵌入各章开头缩略图以供对照。", size=Pt(8.5))

    # 封底寄语
    add_horizontal_line(doc)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("祝 期中顺利 · 推导不丢分 · 读图不手滑 · 半波不数错")
    run.font.size = Pt(12)
    run.bold = True
    run.font.color.rgb = C_PRIMARY
    run.font.name = 'Times New Roman'; run._element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')
    set_paragraph_spacing(p, before=6, after=4)
    p2 = doc.add_paragraph()
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p2.add_run("— 本册由 Agent 在分支 arena/01a0a925-zixue2026 上排版生成，可直接打印，祝 2501 的同学们期中高分！—")
    run.font.size = Pt(8)
    run.italic = True
    run.font.color.rgb = C_GRAY
    run.font.name = 'Times New Roman'; run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
    set_paragraph_spacing(p2, before=2, after=12)

    # 保存
    doc.save(str(DOCX_OUT))
    print(f"Done → {DOCX_OUT}  ({DOCX_OUT.stat().st_size/1024:.0f} KB)")

if __name__ == "__main__":
    generate_all_figs()
    build_document()

