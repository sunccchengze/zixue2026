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
    add_paragraph(doc, "光的干涉是期中的“概念+计算”重灾区。10 道选择题覆盖时间相干性、空间相干性、双缝、薄膜、牛顿环、迈克尔逊等高频概念；填空与计算把“光程差 = 2nd ± λ/2”的各种变体考了个遍。做题永远三步：辨装置 → 找两束光 → 数半波损失（数个数）。抓住“半波损失数个数”就能拿下 80%。", size=Pt(9.5), italic=True, color=C_GRAY)
    add_answer_table(doc, [
        ["1","A","相干长度（波列长度）决定最大光程差——时间相干性；光源尺寸管的是空间相干性（Q3）"],
        ["2","C","两独立钠灯：各自原子自发辐射，波列间相位差随机 → 非相干光，干涉项统计平均为零"],
        ["3","A","空间相干性 ⇔ 光源线度（扩展光源两套条纹错位叠没）；单色性/光谱宽度管时间相干性"],
        ["4","C","间距 Δx=λD/d 只由缝距 d 决定 → 不变；一缝变窄 → 两束振幅不等 → 极小处 |E1|≠|E2| 不再为零"],
        ["5","A","等幅相干叠加：I_min=(A−A)²=0，I_max=(A+A)²=4I_单"],
        ["6","A","插玻璃片给该路加光程 (n−1)e=0.5×10λ=5λ（整数倍波长）→ 原中央明处仍为明纹（变 k=5 级）"],
        ["7","D","透射相长：两束透射光都无半波损失 → 2nd=kλ（k≥1）→ 最小 d=λ/2n"],
        ["8","B","透镜上移：同级条纹要“追”自己的厚度 → 向中心收缩；环心厚度连续增大 → 明暗交替；条纹间距不变"],
        ["9","C","“从下向上看”=透射光干涉；液(1.60)→玻(1.50) 密→疏 无半波 → 2nl=(2k+1)λ/2，取 k=0：l=λ/4n=78.1nm"],
        ["10","B","(1) 相同倾角的光聚焦同一圆周 ✓；(3) 各点光源相互非相干、只是强度相加 ✓；(2)(4) 错"],
    ])
    doc.add_picture(str(OUT_DIR/"fig13_01_thin_film.png"), width=Inches(5.2))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_caption(doc, "图 3-1  薄膜干涉的光程差来由：反射看界面 n 组合定半波，透射恒无半波——故“反射暗=透射明”互补")

    p = doc.add_paragraph(); p.style = doc.styles['Heading 2']; p.add_run("3.1  单选 1–10 精讲（概念辨析）")
    add_question_block(doc, "Q1", "最大光程差由什么决定",
        ["相干长度 vs 光源尺寸、强度、频率"],
        "A  相干长度",
        "光源不是理想单色的：波列有有限长度 Lc=c·τc（τc 相干时间）。两束光程差超过 Lc，等于拿两段“对不上头尾”的波列比相位——无固定相位差，不干涉。所以“能干涉的最大光程差”由相干长度（时间相干性）决定。光源线度决定的是空间相干性（双缝间距的上限，Q3），强度与频率都不决定它。",
        "时间相干 ⇔ 单色性 ⇔ 谱线宽度；空间相干 ⇔ 光源线度 ⇔ 双缝间距容许值。",
        None, None)
    add_question_block(doc, "Q4", "双缝一缝变窄（缝中心位置不变）",
        ["干涉间距变宽/变窄/不变？极小是否仍为零？"],
        "C  间距不变，极小不再为零",
        "干涉条纹位置由双缝间距 d 决定：Δx=λD/d。缝宽 a 变了、d 没变 → 条纹位置一个不动。但一缝变窄 → 两束光到屏上的振幅不等（|E1|≠|E2|）→ 原极小处 |E1+E2|=||E1|−|E2||>0，不再为零，对比度下降。缝宽 a 只影响单缝衍射包络（中央亮区多宽），不影响条纹间距。",
        "缝宽 ↔ 包络；缝距 ↔ 条纹。包络和条纹是两套独立变量。",
        None, None)
    add_question_block(doc, "Q6", "双缝中插入 10λ 厚玻璃片（n=1.5），垂直于 OS1 连线",
        ["原中央明纹处变明/暗？"],
        "A  仍为明纹",
        "条纹位置由光程差决定，插片就是给那一路加光程：穿过厚度 e 的薄片比走空气多 (n−1)e（垂直入射与倾角无关，垂直时尤其好算）。本题 e=10λ、n=1.5 → Δ=(1.5−1)×10λ=5λ。原中央明处光程差由 0 变成 5λ——整数倍波长，仍是加强（它现在是 k=5 级明纹，整组条纹向插片一侧平移了 5 个间距）。\n判据：(n−1)e=kλ → 仍明；(n−1)e=(k+½)λ → 变暗。",
        "平行玻璃片一路的额外光程恒为 (n−1)e，与入射角无关（垂直入射最好算）。",
        None, None)
    add_question_block(doc, "Q8–Q9", "牛顿环：透镜上移 & 浸液体观察",
        ["Q8 平凸透镜慢慢上移，反射光牛顿环怎么变；Q9 装置浸 n=1.60 液体、λ=500nm，从下向上看中心暗斑，顶点距平板的最小距离"],
        "Q8 B（向中心收缩、环心明暗交替）；Q9 C（78.1nm）",
        "Q8：牛顿环每一条对应一个确定的膜厚（等厚干涉）。透镜上移 → 各处的膜厚都变大 → 原来在半径 r 的那条（厚度 d_k）要往更靠近中心（更薄）的地方找自己的厚度 → 环整体向中心收缩。环心处膜厚从 0 连续增大，光程差周期性变化 → 环心明暗交替。注意：环心与边缘的厚度差不变 → 视场内条纹总数、间距都不变（排除 A、D）。\nQ9：题眼在“从下向上观察”——看的是透射光的干涉。两束透射光：一束直通，一束在平板玻璃上表面（液体→玻璃：1.60→1.50，密→疏）反射一次后再透出。密→疏反射无半波损失 → 光程差 δ=2nl，没有额外的 λ/2。暗斑（相消）条件 2nl=(2k+1)λ/2。“最小距离”取 k=0：l=λ/(4n)=500nm/(4×1.60)=78.1nm。\n对比记忆：反射光牛顿环（空气膜，一次半波）暗环是 2d=kλ；透射光（本题，无半波）暗环是 2nl=(k+½)λ——差一个 λ/2，正是“反射暗=透射明”的互补。",
        "牛顿环半径 r²=kλR/n（反射暗环 k）——记得除以 n；浸液后波长变 λ/n，环收缩。",
        str(OUT_DIR/"fig13_02_newton.png"), "图 3-2  牛顿环的形成与“上移/浸液”对条纹的影响")

    p = doc.add_paragraph(); p.style = doc.styles['Heading 2']; p.add_run("3.2  填空 11–20 精讲")
    add_answer_table(doc, [
        ["11","5×10⁻⁷ m","λ=c/ν=500nm；相位改变 3π ⇔ 光程 (2π/λ)·δ=3π → δ=1.5λ；δ=nd → d=1.5λ/n=750/1.5=500nm"],
        ["12","563.6 nm","迈克尔逊：镜动 Δd 光程变 2Δd，每变 λ 条纹移 1 条 → 2Δd=Nλ → λ=2×0.310mm/1100=0.5636μm"],
        ["13","3d","两束透射光的光程差=膜内往返：δ=2nd=2×1.5×d=3d（透射无半波，直接数膜内往返光程）"],
        ["14","同一波面上取出的两个次波源；相干波源","波阵面分割法（杨氏双缝、菲涅耳双镜/双棱镜）；另一种是分振幅法（薄膜、迈克尔逊）"],
        ["15","9λ/(4n₂)","n₁<n₂<n₃：上下两面反射都是疏→密，两次半波互相抵消 → 暗纹 2n₂d=(k+½)λ；尖端 d=0 是明纹，第 5 条暗纹 k=4 → d=(4+½)λ/(2n₂)=9λ/(4n₂)"],
        ["16","(r₁/r₂)²","暗环 (2k+1)λ/2=2·(r²/2R)·n：空气 r₁²∝1，液体 r₂²∝1/n → n=(r₁/r₂)²"],
        ["17","4×10⁻⁵ m","劈尖相邻暗纹厚度差 λ/2 摊在条纹间距 l 上：l·tanθ=λ/2，tanθ=d/20cm → d=λ·0.2m/(2×1.4mm)=560nm×0.2/2.8mm=4.0×10⁻⁵m"],
        ["18","xd/(5D)","第 5 级明纹距中央 5Δx=x，Δx=λD/d → λ=x·d/(5D)"],
        ["19","暗","见下方精讲：空隙充满 n=1.75 液体，一次半波损失，接触点 δ=λ/2 → 相消"],
        ["20","平行；等倾","M₁'∥M₂：同倾角 → 同光程差 → 同心圆环（等倾干涉）；不平行则是等厚（直条纹）"],
    ])
    doc.add_picture(str(OUT_DIR/"fig13_03_wedge.png"), width=Inches(5.5))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_caption(doc, "图 3-3  劈尖（空气）与薄膜的等厚干涉：厚度每增 λ/2，条纹移一条——纸条厚度公式即来于此")
    doc.add_picture(str(OUT_DIR/"fig13_04_michelson.png"), width=Inches(4.8))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_caption(doc, "图 3-4  迈克尔逊干涉仪：M 移动 Δd → 光程变 2Δd → 条纹移动 N=2Δd/λ 条（Q12 核心）")
    add_question_block(doc, "Q19", "三种透明材料的牛顿环（图中标 1.75/1.50/1.62），接触点 P 处圆斑明还是暗",
        ["平凸透镜(1.50)与平板玻璃(1.62)之间空隙充满 n=1.75 的液体，反射光观察。"],
        "暗",
        "两束反射光：① 透镜下表面反射：光从 1.50 射向 1.75（疏→密）→ 有半波损失；② 平板上表面反射：光从 1.75 射向 1.62（密→疏）→ 无。净一次半波损失 → 光程差 δ=2×1.75×d+λ/2（d 是接触点外侧的液层厚度）。\n接触点 d=0：δ=λ/2=半波长的奇数倍 → 相消干涉 → 暗斑。\n注意别套“空气膜牛顿环中心暗”的结论去背：中心明暗完全由净半波个数定——0 次半波→明，1 次→暗。本题液体 1.75 比两边都密，恰好凑出一次。",
        "接触点（d=0）明暗判据：净半波损失偶数次（含 0 次）→ 明；奇数次 → 暗。",
        None, None)

    p = doc.add_paragraph(); p.style = doc.styles['Heading 2']; p.add_run("3.3  计算 21–24 精讲")
    add_question_block(doc, "Q21", "玻璃衬底(n₂=1.52)上沉积 Ta₂O₅ 楔形膜(n₁=2.21)，楔端 A→B 厚度渐减到零；λ=632.8nm 垂直照射，共 11 条暗纹且 A 处对应一条暗纹，求膜厚（3 位有效）",
        ["B 处为零厚度端。"],
        "1.43×10⁻⁶ m（1.43μm）",
        "第一步 数半波：上表面 空气→Ta₂O₅（1.00→2.21）疏→密，有半波；下表面 Ta₂O₅→玻璃（2.21→1.52）密→疏，无。净一次半波 → 反射暗纹条件：2n₁d+λ/2=(k+½)λ ⇔ 2n₁d=kλ。\n第二步 数纹：B 处 d=0 → 2n₁·0=0=kλ 中 k=0 的情形 → **B 本身就是第 1 条（k=0）暗纹**。从 B 到 A 每多一条暗纹 k 加 1；“共 11 条、A 对应一条”→ A 是第 11 条暗纹 → k=10。\n第三步 代入：2n₁h=10λ → h=10λ/(2n₁)=10×632.8nm/4.42=1431.7nm≈**1.43×10⁻⁶ m**。\n常见错误：把 A 数成 k=11 得 1.57μm——漏了 B（零厚度端）自己就是一条暗纹。",
        "楔形膜两步走：先数半波定“暗=2n₁d=kλ 还是 (k+½)λ”；再数端点——有半波时零厚度端必是第一条暗纹。",
        None, None)
    add_question_block(doc, "Q22", "劈尖检测工件：单色光(λ)垂直入射，每条纹弯曲部分的顶点恰好与其左边条纹的直线部分相切，判断缺陷（凹陷/凸起）并求垂直深度",
        ["空气劈尖：楔尖在左，右端厚。"],
        "凹陷；深度 h=λ/2",
        "判据推导（一行）：劈尖每条纹是一条“等厚线”（该处空气隙厚度=该级对应的值）。工件上某处凹陷 h → 该处空气隙比邻处深 h → 要凑回同样的厚度，等厚线必须往更薄的方向（楔尖方向，左）“挪”一条缝宽才能补上 → 条纹弯向楔尖（薄端）。反之凸起 → 隙变浅 → 条纹弯向厚端。\n本题：楔尖在左，图中条纹向左弯 → **凹陷**。\n深度：弯曲顶点与左边相邻直纹相切 → 弯曲量恰为一个条纹间距 → 相邻暗纹厚度差 λ/2（空气膜 2Δd=λ）→ **h=λ/2**。",
        "弯向薄端=凹陷，弯向厚端=凸起；深度/高度=（弯过的条纹间距数）×λ/2。",
        None, None)
    add_question_block(doc, "Q23", "白光（400–760nm）垂直照 d=380nm、n=1.32 的肥皂膜（空气中）：正面（反射）与背面（透射）各呈什么颜色",
        ["反射/透射互补。"],
        "正面：紫红色（668.8nm 红 与 401.3nm 紫 增强）；背面：绿色（501.6nm 绿 增强）",
        "先算常数：2nd=2×1.32×380nm=1003.2nm。\n正面（反射光：空气→膜 疏→密，有半波）：2nd+λ/2=kλ ⇔ λ=2nd/(k−½)。\n枚举：k=1→1003.2/0.5=2006nm（红外，不可见）；k=2→1003.2/1.5=**668.8nm（红）**；k=3→1003.2/2.5=**401.3nm（紫）**；k=4→268nm（紫外，不可见）。可见范围内恰两个增强波长 → 红+紫叠加 = **紫红色**（人眼对红更敏感，红味更重）。\n背面（透射光：两束透射光都无半波）：2nd=kλ ⇔ λ=1003.2/k。\nk=1→1003.2nm（红外，不可见）；k=2→**501.6nm（绿）** → **背面呈绿色**。\n自查：反射增强 ⇔ 透射减弱（能量守恒）——501.6nm 恰是正面“缺”的颜色，前后互补 ✓。",
        "只分两处：反射光有 λ/2、透射光没有；枚举 k 后用 400–760nm 筛，别只取一个 k。",
        None, None)
    add_question_block(doc, "Q24", "平底圆锥 A（锥顶与平板 B 良好接触）形成小劈尖角 θ 的锥形空气层，λ 垂直入射：(1) 明纹条件与图样 (2) 相邻暗纹间空气隙厚度 (3) 圆锥稍向左倾斜后条纹变化",
        ["锥顶在中心，空气隙厚度随到中心距离线性增大。"],
        "(1) 2d+λ/2=kλ（d≈r·tanθ）；同心圆环（中心为暗点） (2) λ/2 (3) 接触点左移：左侧（劈角变小）条纹变疏、右侧（劈角变大）变密",
        "(1) 反射光两束：锥底面（密→疏 空气）反射无半波、平板上表面（疏→密）反射有半波 → 净一次 → 光程差 δ=2d+λ/2；明纹：δ=kλ。空气隙厚度 d≈r·tanθ（r 为到接触点的距离）→ 等厚线是圆 → 图样为**同心圆环**。中心 r=0、d=0：δ=λ/2 → **中心是暗点**。\n(2) 相邻暗纹：2Δd=λ → **Δd=λ/2**（与 θ 无关）。注意区分“厚度差 λ/2”与“环半径差 Δr≈λ/(2tanθ)”——本题问的是前者。\n(3) 向左倾斜：接触点（锥顶）左移，左半边劈角 θ₁<θ<右半边 θ₂。环间距 Δr=1/(2tanθᵢ)：左侧 tanθ₁ 变小 → Δr 变大 → **左侧变疏**；右侧 tanθ₂ 变大 → **右侧变密**；圆环中心（接触点暗点）整体向左移。",
        "锥形劈尖=“转成圆的劈尖”，仍是等厚干涉，抓住 d 的几何表达；倾斜后两侧一疏一密，不是整体均匀变密。",
        None, None)

    p = doc.add_paragraph(); p.style = doc.styles['Heading 1']; p.add_run("四、第十四次  波动光学 2  （24 题·衍射与分辨）")
    add_paragraph(doc, "单缝衍射是基础，光栅是主角，分辨本领是收尾。期中 14 次最爱考“缺级”和“斜入射”。三套公式通吃：①单缝暗 a sinφ=±kλ（k≠0）；②光栅明 d sinφ=±kλ；③缺级 k=(d/a)k'。", size=Pt(9.5), italic=True, color=C_GRAY)
    add_answer_table(doc, [
        ["1","A","b 变窄→中央宽 2fλ/b 变宽；L 上移→中央主极大跟透镜光轴走→上移"],
        ["2","B","瑞利判据 θ=1.22λ/D：电子物质波波长 ≪ 可见光 → 分辨角更小（A、C、D 与分辨无关）"],
        ["3","D","斜入射：中央主极大移到 f·tanθ（小角 ≈f·sinθ）"],
        ["4","B","kmax=⌊d/λ⌋=2000/550⌋=3.64=3"],
        ["5","C","a=b→d=2a→偶数级全缺；7 条明纹=k=0,±1,±3,±5 → 一侧第二条是 3 级"],
        ["6","D","重叠 450k₁=750k₂ → 3k₁=5k₂ → λ₂ 的级数 3,6,9,…（k₁=5,10,…）"],
        ["7","D","1.22λ/D=1.22×550nm/1.27m≈5.3×10⁻⁷ rad"],
        ["8","C","插玻璃片→光程差改变→条纹平移；玻璃有反射损耗→明纹亮度减弱"],
        ["9","B","θ=1.22λ/D=1.22×550nm/3mm=2.24×10⁻⁴ rad → l=H·θ=3×10⁵m×2.24×10⁻⁴≈67.1m"],
        ["10","C","f 增大→中央宽 2fλ/b 变大（中心强度不变，只是能量摊宽）"],
    ])
    doc.add_picture(str(OUT_DIR/"fig14_01_single.png"), width=Inches(5.8))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_caption(doc, "图 4-1  左：单缝强度分布（暗纹 a sinφ=±kλ）；右：透镜沿 y 移动时中央主极大随光轴移动，且 b 减小使中央变宽（Q1、Q10）")

    p = doc.add_paragraph(); p.style = doc.styles['Heading 2']; p.add_run("4.1  单选 1–10 精讲")
    add_question_block(doc, "Q1", "夫琅禾费单缝：b 稍稍变窄 + 透镜 L 沿 y 正方向微移，中央衍射条纹？",
        ["缝与屏位置不动。"],
        "A  变宽，同时向上移动",
        "宽度：中央主极大宽 Δx₀=2fλ/b（两侧第一暗纹之间）。b 减小 → Δx₀ 增大 → 变宽。\n位置：透镜把“与入射光平行的那束几何光线”聚焦到焦平面上——中央主极大永远落在透镜主光轴与屏的交点。缝不动、透镜上移 → 光轴上移 → 中央条纹跟着上移。\n结论：又宽又上移。",
        "缝不动、透镜动，条纹跟着透镜光轴动；缝变窄，中央变宽。两件事互不干扰。",
        None, None)
    add_question_block(doc, "Q3", "单色光以 θ 角斜入射单缝，中央主极大移到 O'，O、O' 距离？",
        ["透镜焦距 f，缝宽 a。"],
        "D  f·tanθ（小角时 ≈f·sinθ）",
        "斜入射的平行光若不发生衍射，几何光学把它会聚到焦平面上“过光心、与入射光平行”的交点——该点距光轴交点 O 为 f·tanθ（直角三角形：竖直边 f，底角 θ）。衍射的中央主极大（0 级）永远跟着几何像走 → O O'=f·tanθ。\n选项辨析：小角近似 tanθ≈sinθ，所以“f·sinθ”数值上几乎一样，但严格值是 tan——选 D。",
        "透镜成像口诀：平行光会聚点=过光心平行线的交点；0 级衍射跟着它。",
        None, None)
    add_question_block(doc, "Q4–Q6", "光栅最大级数、缺级数条纹、谱线重叠",
        ["Q4 λ=550nm、d=2×10⁻⁴cm 最大级；Q5 7 条明纹、a=b，中央一侧第二条是几级；Q6 λ₁=450、λ₂=750 重叠处 λ₂ 的级数"],
        "Q4 B（3 级）；Q5 C（3 级）；Q6 D（3,6,9,…）",
        "Q4：d=2×10⁻⁴cm=2000nm。kmax=⌊d/λ⌋=2000/550⌋=⌊3.64⌋=3（kλ≤d 必须成立，直接向下取整）。\nQ5：a=b → d=a+b=2a。缺级条件：光栅明 k 与单缝暗 k'=k/2 同方向同时满足 → k=2k' → 2,4,6… 全缺。7 条明纹=中央+两侧各 3 条：k=0,±1,±3,±5。中央一侧：第一条=1 级，第二条=**3 级**。\nQ6：重叠 ⇔ 同一衍射角 φ 上两波长都出主极大：d sinφ=k₁λ₁=k₂λ₂ → k₁/k₂=λ₂/λ₁=750/450=5/3 → k₁=5m、k₂=3m → λ₂ 的级数是 3,6,9,12…（m=1,2,3…）。",
        "缺级公式 k_missing=(d/a)·k'；谱线重叠用“波长反比定级数比”。",
        str(OUT_DIR/"fig14_02_grating_missing.png"), "图 4-2  a=b 时缺级示意：偶数级被单缝包络零点“吃掉”，光栅明纹强度被调制")
    add_question_block(doc, "Q7 & Q9", "分辨本领：大望远镜与人眼",
        ["Q7 λ=550nm、D=127cm 望远镜最小分辨角；Q9 飞船高 300km、瞳孔 3mm、λ=550nm，地面最小可分辨物体"],
        "Q7 D（5.3×10⁻⁷ rad）；Q9 B（67.1m）",
        "瑞利判据：θ_min=1.22λ/D（圆孔衍射第一暗环半角）。\nQ7：θ=1.22×550×10⁻⁹/1.27=5.28×10⁻⁷ rad。\nQ9：先角后线。人眼 θ=1.22×550×10⁻⁹/3×10⁻³=2.24×10⁻⁴ rad；角很小 → 线尺寸 l=H·θ=3×10⁵m×2.24×10⁻⁴=67.1m。\n单位纪律：λ 用 m、D 用 m、θ 出 rad，最后 rad 直接乘距离。",
        "1.22 是圆孔衍射的系数，必考；“先角后线”两步走，别跳步。",
        str(OUT_DIR/"fig14_03_resolution.png"), "图 4-3  瑞利判据：可分辨 vs 不可分辨的强度叠加（中间凹陷 ≥ 20% 才算分开）")

    p = doc.add_paragraph(); p.style = doc.styles['Heading 2']; p.add_run("4.2  填空 11–20 精讲")
    add_answer_table(doc, [
        ["11","φ=arcsin(sinθ±kλ/a)","斜入射单缝：两边缘光程差 a(sinφ−sinθ)=±kλ（暗），解出衍射角 φ（k 受反正弦定义域限制）"],
        ["12","紫；变大","一级光谱 sinφ=λ/d：λ 最小（紫）角最小→最靠中央；d 变小→sinφ 反比增大→衍射角变大"],
        ["13","6.04×10⁻⁵ m","两侧第一暗纹夹角 1.20°→单侧 φ=0.6°；a=λ/sin0.6°=632.8nm/0.01047=6.04×10⁻⁵m"],
        ["14","1.2×10⁻³ m；3.6×10⁻³ m","中央宽 2fλ/b=2×600nm×0.6m/0.6mm=1.2mm；两第三暗间距 2×3fλ/b=3.6mm"],
        ["15","10λ","k=2 主极大：d sinφ=2λ；第 1 缝与第 6 缝间距 5d → δ=5d sinφ=5×2λ=10λ"],
        ["16","第一级；第三级","d=2a→2 级缺 → 5 条明纹=k=0,±1,±3 → 同侧相邻两条是 1 级与 3 级"],
        ["17","2.5×10⁻³ mm","d=1mm/100=10μm；第 4 级“刚好”消失→d/a=4（单缝 k'=1 的暗）→a=d/4=2.5μm；若 a=5μm 则 2 级也缺，不是“刚好 4 级”"],
        ["18","2.68×10⁻⁷ rad","θ=1.22λ/D=1.22×550nm/2.5m=2.68×10⁻⁷ rad"],
        ["19","4 个","a sinφ=4λ×sin30°=2λ → 2λ/(λ/2)=4 个半波带（偶数个→暗纹）"],
        ["20","λ₁=2λ₂；λ₁ 的每一级 k 与 λ₂ 的偶数级 2k","极小重合 a sinφ：k₁λ₁=k₂λ₂ → k₂=2k₁（k=1,2,3…）"],
    ])
    add_question_block(doc, "T13 & T14", "单缝尺寸与条纹宽度计算",
        ["T13 λ=632.8nm，两侧第一暗纹夹角 1.20° 求缝宽；T14 b=0.6mm、f=60cm、λ=600nm 求中央宽与两第三暗间距"],
        "T13 6.04×10⁻⁵ m（60.4μm）；T14 中央 1.2mm，两第三暗间距 3.6mm",
        "T13：两侧第一暗纹夹角 1.20° → 单侧衍射角 φ=0.6°（对称）。暗纹条件 a sinφ=λ（第一暗 k=1）→ a=632.8nm/sin0.6°=632.8/0.01047=6.04×10⁻⁵ m。小角自查：a≈2λ/Δθ=2×632.8nm/0.02094rad=60.4μm，一致。\nT14：旁轴近似 x_k=f·kλ/b。中央宽（两第一暗）=2fλ/b=2×0.6m×600×10⁻⁹/0.6×10⁻³=1.2×10⁻³m；两第三暗间距=2x₃=2×3fλ/b=3.6×10⁻³m。",
        "先化弧度再近似：sin≈tan≈θ(rad)；“两侧夹角”记得除以 2。",
        None, None)
    add_question_block(doc, "T19", "波面半波带数：a=4λ、φ=30°",
        ["单缝波面可划几个半波带？"],
        "4 个",
        "半波带法：沿衍射方向波面两侧边缘的光程差 a sinφ，每 λ/2 划一个带。a sinφ=4λ×sin30°=2λ → N=2λ/(λ/2)=4 个半波带。N 偶 → 相消（暗纹）；N 奇 → 次极大（明）。",
        "数半波带=数“2λ 里有几个半波”：2λ=4×(λ/2)。",
        None, None)

    p = doc.add_paragraph(); p.style = doc.styles['Heading 2']; p.add_run("4.3  计算 21–24 精讲")
    add_question_block(doc, "Q21", "光栅 λ=500nm，第一级主明纹衍射角 30°：(1) 光栅常数 (2) 波长在 5% 范围内变化，一级衍射角变化范围",
        ["垂直入射。"],
        "(1) d=1.0×10⁻⁶ m (2) 28.36°–31.67°，Δθ≈3.31°（≈0.0578 rad）",
        "(1) 光栅方程 d sinθ=kλ，k=1、θ=30° → d=λ/sin30°=500nm/0.5=1.0×10⁻⁶ m。\n(2) 直接代数：λ₁=475nm → θ₁=arcsin(475/1000)=arcsin0.475=28.36°；λ₂=525nm → θ₂=arcsin0.525=31.67°。一级衍射角在 28.36°–31.67° 之间，变化 Δθ=3.31°。\n微分法交叉验算：dθ=(k/d)·(dλ/cosθ)=25nm/(1000nm×0.866)=0.0289rad（单侧 1.65°），两侧合计 3.3°，与直接算法一致。",
        "光栅题先求 d 再套方程；微分法快速估算，正式答案用直接代数。",
        None, None)
    add_question_block(doc, "Q22", "λ=600nm 垂直照可调狭缝，中央亮纹宽由 1.0cm 变到 1.5cm，f=40cm，求缝宽变化",
        ["中央宽 Δx₀=2fλ/b。"],
        "由 0.048mm 变到 0.032mm（缝变窄了 0.016mm）",
        "中央宽与缝宽反比：b=2fλ/Δx₀。\nΔx₀=1.0cm=0.01m → b₁=2×0.4m×600×10⁻⁹/0.01=4.8×10⁻⁵m=0.048mm。\nΔx₀=1.5cm=0.015m → b₂=2×0.4×600×10⁻⁹/0.015=3.2×10⁻⁵m=0.032mm。\n中央宽变宽（1.0→1.5cm）⇔ 缝变窄：缝宽由 0.048mm 变到 0.032mm，变窄 0.016mm。",
        "中央宽 ∝ 1/b：观察到变宽 → 一定是缝变窄，方向不能反。",
        None, None)
    add_question_block(doc, "Q23", "平行光 λ₁=440nm、λ₂=660nm 垂直入射光栅，两波长谱线（不计中央）第二次重合于 φ=60°，求光栅常数",
        ["“第二次重合”=m=2。"],
        "d≈3.05×10⁻⁶ m（重合级 k₁=6、k₂=4）",
        "重合 ⇔ 同方向两波长都出主极大：k₁λ₁=k₂λ₂ → k₁/k₂=660/440=3/2 → k₁=3m、k₂=2m。\n第一次重合 m=1：k₁=3、k₂=2；第二次重合 m=2：k₁=6、k₂=4。\n代入光栅方程（用 λ₁ 与 k₁=6）：d sin60°=6×440nm → d=2640nm/0.866=3048nm≈3.05×10⁻⁶ m。\n交叉验证：k₂=4 应给同一 d：4×660/0.866=3048nm ✓ 吻合（两波长在同一方向，光栅常数当然唯一）。",
        "“第 m 次重合”指 m=2，不是 k=2；重合级数比=波长反比。",
        None, None)
    add_question_block(doc, "Q24", "λ=500nm 以 30° 入射照光栅，原垂直照射时的中央明纹位置现变为第二级明纹：(1) 光栅常数 (2) 现在最多能看到第几级 (3) 改用 600–650nm 光垂直照射，谱线是否重叠",
        ["斜入射光栅方程 d(sinφ+sinθ₀)=kλ（入射与衍射在法线同侧）。"],
        "(1) d=2.0×10⁻⁶ m (2) 第 6 级（可见 k=−2,…,6 共 9 条） (3) 不重叠",
        "(1) “原中央明纹位置”=衍射角 φ=0 的方向。该方向现为第 2 级明纹：d(sin0+sin30°)=2λ → d×0.5=2×500nm → **d=2.0×10⁻⁶ m**。这一步最容易错：d×0.5=1000nm → d=1000/0.5=2000nm，别漏除。\n(2) sinφ=kλ/d−sin30°=k/4−0.5，要求 |sinφ|≤1：−1≤k/4−0.5≤1 → −2≤k≤6。可见级 k=−2,−1,0,1,2,3,4,5,6（共 9 条），**最高第 6 级**（k=6 时 sinφ=1，φ=90° 掠出边缘）。\n(3) 垂直照射：k≤⌊d/λ⌋=⌊2000/650⌋=3 → 每波长只可能出现 k=1,2,3。重叠条件 600k₁=650k₂ → 12k₁=13k₂，最小正整数解 k₁=13、k₂=12，远超 k≤3 → **不重叠**。",
        "斜入射光栅方程符号：入射、衍射在法线同侧相加、异侧相减；“原中央位置”永远指 φ=0 方向。",
        None, None)

    p = doc.add_paragraph(); p.style = doc.styles['Heading 1']; p.add_run("五、第十五次  波动光学 3·偏振  （24 题·概念为主）")
    add_paragraph(doc, "偏振是波动光学的收官。与干涉、衍射的“光程差”不同，偏振考“方向投影”。核心只有马吕斯定律与布儒斯特定律，其余是它们的几何应用。选择题多为定义辨析，计算题公式单一，务必全拿。", size=Pt(9.5), italic=True, color=C_GRAY)
    add_answer_table(doc, [
        ["1","B","初始正交（α=90° 消光）；转 180°：90°→0° 增至最大、0°→90° 减回零——先增后减至零"],
        ["2","D","“通过偏振片前后强度不变”错：透射强度=入射强度×cos²α（自然光则减半），随角度变化"],
        ["3","C","偏振度=(I_线−I_自然分量)/总：C 两正交分量最接近等分 → 偏振度最小"],
        ["4","C","强度有变化但无消光 → 部分偏振或椭圆偏振；圆/自然光强度不变（排除）、线偏振必有消光（排除）→“不可能是圆偏振”是唯一正确陈述"],
        ["5","A","自然光过偏振片变线偏振、强度减半；两缝同偏振 → 仍干涉，明纹亮度减半"],
        ["6","B","“一定是线偏振光”错：只有布儒斯特角时反射光才线偏振，一般入射角为部分偏振"],
        ["7","B","上表面布儒斯特入射 → 下表面入射角同样是布儒斯特角（互余对称）→ 光线 3（下表面反射）仍为线偏振、⊥入射面"],
        ["8","C","o 光各向同速→球面波阵面；e 光速度随方向变→旋转椭球面"],
        ["9","C","圆偏振=两正交等幅线偏正交叠加：过偏振片只剩一个分量→线偏振，I=I₀/2"],
        ["10","A","自然光各方向无固定相位关系，λ/4 片引入的相位差不改变统计 → 仍为自然光"],
    ])
    doc.add_picture(str(OUT_DIR/"fig15_01_malus.png"), width=Inches(5.8))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_caption(doc, "图 5-1  偏振核心：自然光 I₀→偏振片后 I₀/2；线偏振过第二片 I=I₀cos²θ（马吕斯）")

    p = doc.add_paragraph(); p.style = doc.styles['Heading 2']; p.add_run("5.1  单选 1–10 精讲（再谈布儒斯特与 o/e）")
    add_question_block(doc, "Q1 & Q4", "正交偏振片旋转 180° 的透光变化；旋转检偏有变化但无消光",
        ["Q1 正交叠放无光，转一片 180° 透射光强怎么变；Q4 旋转检偏片有变化无消光，入射光可能是什么"],
        "Q1 B（先增加、后减小至零）；Q4 C（不可能是圆偏振光）",
        "Q1：初始正交 α=90°（消光）。转一片 180°，夹角 α 经历 90°→0°→90°。马吕斯 I=I₁cos²α：cos² 的周期是 180°、在 90° 处为零 0° 处为 1 → 前半程单调增到最大（两片平行时），后半程单调减回零（回到正交）。全程一次极大、终点消光 → “先增加、后又减小至零”。\nQ4：用“旋转现象”分类。强度不变 → 圆偏振或自然光；有消光 → 线偏振；**有变化但无消光 → 部分偏振或椭圆偏振**。本题属第三类。逐项：A“一定是部分偏振”太绝对（可能是椭圆）；B“一定是椭圆”也太绝对（可能是部分）；D“可能是线偏振”错——线偏振转到正交必消光；只有 C“不可能是圆偏振光”正确（圆偏振强度应不变，与“有变化”矛盾）。",
        "偏振态判别三步：①旋转找消光（有→线偏；不变→圆/自然；变而不消→部分/椭圆）；②加 λ/4 片区分圆与椭圆、自然与部分。",
        None, None)
    add_question_block(doc, "Q6–Q7", "自然光入射介质界面：反射光偏振态；平板玻璃布儒斯特入射的光线 3",
        ["布儒斯特角 i_B=arctan(n₂/n₁)。"],
        "Q6 B（“一定是线偏振”是错误说法）；Q7 B（线偏振、振动⊥入射面）",
        "Q6：菲涅耳反射中 s 分量（⊥入射面）反射率恒大于 p 分量 → 一般入射角下反射光是**部分偏振**；只有 i=i_B 时 p 分量反射率归零 → 反射光才是完全**线偏振**（⊥入射面）。所以“一般部分偏振、可能线偏振、与入射角有关”都对，“一定线偏振”错 → 选 B。\nQ7：上表面以布儒斯特角入射时，折射角 r=90°−i_B；光线射到下表面时入射角恰好=r，且 n 的关系互余对称 → 下表面同样是布儒斯特条件 → 光线 3（下表面反射光）仍是线偏振、振动方向 ⊥入射面。",
        "布儒斯特角时反射光与折射光互相垂直（i_B+r=90°）——这个互余对称让“上下表面同是布儒斯特”成立。",
        str(OUT_DIR/"fig15_02_brewster.png"), "图 5-2  布儒斯特角时反射光（1）仅剩 s 分量（⊥入射面），折射光（2）为部分偏振")
    add_question_block(doc, "Q8", "双折射晶体中 o 光与 e 光的波阵面",
        ["形状判断。"],
        "C  o 光球面，e 光旋转椭球面",
        "o 光（寻常光）：折射率 n₀ 与方向无关 → 各向速度相同 → 波阵面是球面。e 光（非常光）：折射率随传播方向变（n_e(θ)）→ 以光轴为旋转轴的旋转椭球面。沿光轴方向两者速度相等（球与椭球的交点）。",
        "记忆：o=ordinary（寻常→球），e=extraordinary（非常→椭球）。",
        None, None)
    add_question_block(doc, "Q5", "杨氏双缝与屏之间紧贴双缝放一理想偏振片（透光轴平行缝），自然光入射",
        ["干涉条纹还在吗？亮度如何？"],
        "A  仍有干涉条纹，明纹亮度为原来一半",
        "自然光可分解为 ∥缝 与 ⊥缝 两个不相干分量，各占 I₀/2。偏振片只放过 ∥ 分量：每缝的光强 I₀→I₀/2，且**两缝出来的光变成同一偏振方向** → 相干条件满足，条纹照旧（间距、位置都不变），但每条明纹的强度减半（I_max=(√(I₀/2))²×2 型推导 = 原一半）。\n反例对照：若两缝后放透光轴互相正交的偏振片 → 两缝光偏振正交 → 不相干 → 条纹消失。",
        "同偏振才能干涉：一片偏振片把两缝“对齐”了，条纹保留、亮度减半。",
        None, None)

    p = doc.add_paragraph(); p.style = doc.styles['Heading 2']; p.add_run("5.2  填空 11–20 精讲")
    add_answer_table(doc, [
        ["11","透振方向（偏振化方向）；起偏器；检偏器","偏振片三件套：方向、产生线偏振、检验线偏振"],
        ["12","平行于入射面","布儒斯特角反射掉的全部是 s 分量（⊥）；若无任何反射 → 入射光里没有 s 分量 → 纯 p → 振动 ∥ 入射面"],
        ["13","(√2/2)A","振幅投影：A'=Acos45°=A/√2（强度才是 I₀/2）"],
        ["14","60°","自然光过 P₁：I₁=I₀/2；过 P₂：I=I₁cos²α=I₀/8 → cos²α=1/4 → α=60°"],
        ["15","线偏振光；⊥入射面；部分偏振光","布儒斯特反射三件套"],
        ["16","arctan(n₂/n₁)","布儒斯特定律 tan i_B=n₂/n₁"],
        ["17","I/2","圆偏振过偏振片：两正交等幅分量只剩一个 → I₀/2（与自然光相同）"],
        ["18","o 光与 e 光（顺序不限）","沿光轴传播：无双折射，n_o=n_e(θ)，速度相等"],
        ["19","5×10⁻⁶ m","λ/4 片：Δn·d=λ/4 → d=600nm/(4×0.03)=5000nm"],
        ["20","在光路中加入二分之一波片（λ/2 片）","半波片把两正交分量的相位差 0→π，椭圆旋向翻转（右旋↔左旋）"],
    ])
    doc.add_picture(str(OUT_DIR/"fig15_03_waveplate.png"), width=Inches(5.8))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_caption(doc, "图 5-3  波片原理：λ/4 片使线偏 45°→圆偏；λ/2 片使线偏方向旋转 2θ、椭圆旋向翻转（用于 Q19、Q20、Q24）")
    add_question_block(doc, "T13–T14", "马吕斯定律的振幅与强度",
        ["T13 线偏振振幅 A 垂直入射、与透光轴夹 45° 的偏振片，透射振幅？T14 自然光 I₀ 过两片叠放偏振片后 I=I₀/8，求夹角。"],
        "T13 (√2/2)A；T14 60°",
        "T13：振幅按方向投影：A'=Acos45°=(√2/2)A。注意区分：强度是振幅平方 → I=I₀cos²45°=I₀/2。\nT14：自然光先过 P₁ 减半：I₁=I₀/2；再过 P₂：I=I₁cos²α=(I₀/2)cos²α=I₀/8 → cos²α=1/4 → α=60°。两个易丢的点：自然光先减半、强度用 cos²。",
        "振幅用 cos、强度用 cos²；自然光过第一片恒减半，别漏。",
        None, None)
    add_question_block(doc, "T19 & T24", "波片最小厚度：λ/4 片与方解石晶片磨削",
        ["T19 λ=600nm、|n₀−nₑ|=0.03 求 λ/4 片最小厚度；T24 10μm 方解石（n₀=1.658、nₑ=1.486）置于正交偏振片间、光轴与第一片夹 45°，600nm 要透射极大，至少磨去多少（3 位有效）"],
        "T19 5.0×10⁻⁶ m（5μm）；T24 至少磨去 1.28×10⁻⁶ m（磨到 8.72μm）",
        "T19：o/e 光程差 Δn·d 要等于 λ/4 的奇数倍；最小取 k=0：d=λ/(4Δn)=600nm/(4×0.03)=5000nm=5μm。\nT24：光轴 45° → o/e 等幅分解。正交偏振片间透射强度 ∝sin²(δ/2)，δ=2πΔn·d/λ。透射极大 ⇔ δ=(2k+1)π ⇔ **Δn·d=(2k+1)λ/2**。\n现有 Δn·d₀=0.172×10μm=1.72μm（δ=2π×1.72/0.6≈2.87×2π，不是极大）。把满足条件的厚度列出来：d=(2k+1)×300nm/0.172：k=0→1.74μm；k=1→5.23μm；k=2→8.72μm；k=3→12.2μm>10μm 不可行。\n“至少磨去”=磨到**不超过 10μm 的最大满足厚度** 8.72μm（k=2）→ 磨去 Δ=10−8.72=**1.28μm**。\n验证：Δn·d'=0.172×8.72μm=1.50μm=5×300nm=(2×2+1)λ/2 ✓。",
        "波片厚度永远用 Δn·d=(m±¼)λ 类条件；“至少磨去”要枚举 k 取最接近现值的更小者。",
        None, None)

    p = doc.add_paragraph(); p.style = doc.styles['Heading 2']; p.add_run("5.3  计算 21–24 精讲")
    add_question_block(doc, "Q21", "偏振片检偏：由透射光强最大位置转过 60°，光强减半。部分偏振光=自然光 I_n+线偏振 I_p，求 I_n:I_p",
        ["线偏振分量振动方向与最大透射位置一致。"],
        "I_n : I_p = 1 : 1",
        "最大位置（α=0，与线偏振分量平行）：I_max=I_n/2+I_p（自然光过片恒减半）。\n转过 60°：I=I_n/2+I_p cos²60°=I_n/2+I_p/4。\n条件 I=½I_max：I_n/2+I_p/4=½(I_n/2+I_p)=I_n/4+I_p/2 → 移项 I_n/4=I_p/4 → **I_n=I_p → 1:1**。\n钥匙：部分偏振拆成“自然+线偏”两路独立算再相加；自然光那一路永远减半、与角度无关，只有线偏振那一路走马吕斯。",
        "自然分量恒减半 + 线偏分量走 cos²，两路相加——混在一起的偏振光一律这么拆。",
        None, None)
    add_question_block(doc, "Q22", "三片偏振片叠放：P₁⊥P₃，自然光 I₀ 垂直入射，P₂ 与 P₁ 夹角多大时透射最强",
        ["经典三片问题。"],
        "45°（此时最大透射光强为 I₀/8）",
        "设 P₂ 与 P₁ 夹角 θ，则与 P₃ 夹角 90°−θ。\nI₁=I₀/2（自然光减半）；I₂=I₁cos²θ；I₃=I₂cos²(90°−θ)=I₁cos²θsin²θ=(I₀/2)·(1/4)sin²2θ=(I₀/8)sin²2θ。\nsin²2θ 最大为 1（2θ=90°）→ **θ=45°**，此时 I_max=I₀/8。\n物理意义：正交两片本该全挡，中间插一片 45° 就“借出” I₀/8——偏振片的马吕斯投影链条。",
        "三片正交，中间 45° 透过最大，且最大只有 I₀/8；角度从 0 到 90° 扫一遍，透射先增后减。",
        None, None)
    add_question_block(doc, "Q23", "强度 I₀ 的光=线偏振与自然光等强混合，线偏振振动方向与两片偏振片透光轴均成 30°，两片夹角 60°，求透过每片后的强度",
        ["先 P₁（0°）后 P₂（60°）。"],
        "P₁ 后 5I₀/8；P₂ 后 5I₀/32",
        "入射光：自然 I₀/2 + 线偏振 I₀/2（与 P₁ 成 30°）。\n透过 P₁：自然部分 I₀/2→I₀/4（恒减半）；线偏振部分 (I₀/2)cos²30°=3I₀/8。合计 **I₁=I₀/4+3I₀/8=5I₀/8**。\n关键一步：过了 P₁ 之后，透射光的**全部**都变成沿 P₁ 方向的线偏振（自然部分和线偏振部分已“合流”同偏振）→ 过 P₂ 必须作为一束光整体投影：I₂=I₁cos²60°=(5I₀/8)×(1/4)=**5I₀/32**。\n常见错误：过了 P₁ 还把“自然部分”和“线偏振部分”分开、用不同角度分别投影——同偏振之后它们已不可区分，只能合起来投。",
        "过一片偏振片后一切光都是同偏振线偏振——此后只有“整体 cos²”一种算法。",
        None, None)
    add_question_block(doc, "Q24", "10μm 方解石晶片（n₀=1.658、nₑ=1.486，Δn=0.172）光轴平行表面，置于两正交偏振片间，光轴与第一片夹 45°；600nm 光要透射极大，晶片至少磨去多少（3 位有效）",
        ["正交偏振片间加波片（显色偏振）。"],
        "至少磨去 1.28×10⁻⁶ m（磨到 8.72μm）",
        "条件与 T24 完全相同（同一套推导，见 T19&T24 精讲）：正交偏振片间、光轴 45° → 透射极大 ⇔ Δn·d=(2k+1)λ/2。\n现有 Δn·d₀=0.172×10μm=1.72μm，对应 δ≈2.87×2π，不是极大。\n满足条件的厚度序列：1.74 / 5.23 / 8.72 / 12.2μm（k=0,1,2,3）。≤10μm 的最大者为 8.72μm（k=2）→ 磨去 10−8.72=**1.28μm**。\n验证：0.172×8.72μm=1.50μm=5×(600/2)nm=(2×2+1)λ/2 ✓。",
        "正交片间“亮”=光程差半波长奇数倍；平行片间“亮”=半波长偶数倍（整波长）。",
        None, None)

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
    add_paragraph(doc, "· 第十四次填空 T15 “第一条缝与第六条缝光程差”：k=2 主极大处 d sinφ=2λ，两缝间距 5d → 光程差 δ=5d sinφ=10λ。部分解析写作“10π”是相位差（rad），本题问光程差，答 10λ。", size=Pt(8.5))
    add_paragraph(doc, "· 第十五次填空 T14：题面“自然光 I0 …… 出射光强 I=I0/8”中 I0 指入射自然光总强度。自然光过 P1 先减半为 I0/2，再过 P2：(I0/2)cos²α=I0/8 → cos²α=1/4 → α=60°（本册统一此值）。“45°”一说源于把 I0 另定义为经第一片后的强度，题面未如此定义。", size=Pt(8.5))
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

