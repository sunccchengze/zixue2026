#!/usr/bin/env python3
"""Build readable A4 homework sheet and answer PDF from the checked Markdown sources."""
from pathlib import Path
import re, html
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, PageBreak,
                                Table, TableStyle, KeepTogether)

ROOT=Path(__file__).resolve().parent
QMD=ROOT/'第二章偶数题-题面.md'
AMD=ROOT/'第二章偶数题-参考答案.md'
QPDF=ROOT/'第二章偶数题-答题纸.pdf'
APDF=ROOT/'第二章偶数题-完整解析.pdf'
pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
base=ParagraphStyle('base',fontName='STSong-Light',fontSize=10,leading=15,spaceAfter=4,wordWrap='CJK')
small=ParagraphStyle('small',parent=base,fontSize=9,leading=12)
h1=ParagraphStyle('h1',parent=base,fontSize=17,leading=23,alignment=1,spaceAfter=9)
h2=ParagraphStyle('h2',parent=base,fontSize=13,leading=18,spaceBefore=7,spaceAfter=5)
h3=ParagraphStyle('h3',parent=base,fontSize=11,leading=15,spaceBefore=5,spaceAfter=3)
sol=ParagraphStyle('sol',parent=base,fontSize=9.7,leading=14.5,spaceAfter=5)
cell=ParagraphStyle('cell',parent=base,fontSize=8.8,leading=12)

# Basic human-readable math fallback for PDF output; the full source remains Markdown with LaTeX.
def latex_plain(s):
    s=s.replace(r'\(', '').replace(r'\)', '').replace(r'\[','').replace(r'\]','')
    s=s.replace(r'\begin{cases}', '〔分段〕').replace(r'\end{cases}', '')
    s=re.sub(r'\\begin\{array\}\{[^}]*\}', '', s).replace(r'\end{array}', '')
    s=s.replace(r'\begin{aligned}', '').replace(r'\end{aligned}', '')
    # Convert LaTeX arguments (including unbraced forms such as \frac12) to readable text.
    def argument(src, pos):
        while pos < len(src) and src[pos].isspace(): pos += 1
        if pos >= len(src): return '', pos
        if src[pos] == '{':
            depth=1; j=pos+1
            while j<len(src) and depth:
                if src[j]=='{': depth+=1
                elif src[j]=='}': depth-=1
                j+=1
            return src[pos+1:j-1], j
        if src[pos]=='\\':
            j=pos+1
            while j<len(src) and src[j].isalpha(): j+=1
            return src[pos:j], j
        return src[pos], pos+1
    for _ in range(50):
        m=re.search(r'\\(?:dfrac|tfrac|frac|binom|sqrt)(?![A-Za-z])',s)
        if not m: break
        cmd=m.group(0); a,p1=argument(s,m.end())
        if cmd.endswith('frac') or cmd.endswith('binom'):
            b,p2=argument(s,p1)
            val=f'C({latex_plain(a)},{latex_plain(b)})' if cmd.endswith('binom') else f'({latex_plain(a)})/({latex_plain(b)})'
        else:
            p2=p1; val=f'√({latex_plain(a)})'
        s=s[:m.start()]+val+s[p2:]
    s=re.sub(r'\\(?:mathrm|text|operatorname)\{([^{}]*)\}', r'\1', s)
    s=s.replace(r'\left','').replace(r'\right','')
    s=re.sub(r'_\{([^{}]+)\}',r'_(\1)',s)
    s=re.sub(r'\^\{([^{}]+)\}',r'^(\1)',s)
    s=s.replace(r'\lfloor','⌊').replace(r'\rfloor','⌋')
    repl={r'\leq':'≤',r'\geq':'≥',r'\le':'≤',r'\ge':'≥',r'\ne':'≠',r'\infty':'∞',r'\pi':'π',r'\lambda':'λ',r'\mu':'μ',r'\sigma':'σ',r'\Phi':'Φ',r'\phi':'φ',r'\Theta':'Θ',r'\theta':'θ',r'\cos':'cos',r'\sin':'sin',r'\max':'max',r'\min':'min',r'\arctan':'arctan',r'\arcsin':'arcsin',r'\int':'∫',r'\sum':'Σ',r'\sim':'∼',r'\cdot':'·',r'\times':'×',r'\in':'∈',r'\quad':'  ',r'\qquad':'  ',r'\,':' ',r'\;':' ',r'\!':'',r'\%':'%'}
    for a,b in repl.items(): s=s.replace(a,b)
    s=s.replace(r'\{','@@LBR@@').replace(r'\}','@@RBR@@').replace(r'\_','_')
    s=s.replace('\\\\', ' <BR> ').replace('&','  |  ')
    s=re.sub(r'\\[a-zA-Z]+', '', s)
    s=s.replace('{','').replace('}','')
    s=s.replace('@@LBR@@','{').replace('@@RBR@@','}')
    return s

def rich_text(s):
    s=s.strip()
    s=re.sub(r'\*\*(.*?)\*\*',r'@@B@@\1@@/B@@',s)
    s=re.sub(r'`([^`]*)`',r'\1',s)
    s=latex_plain(s)
    s=html.escape(s,quote=False)
    s=s.replace('@@B@@','<b>').replace('@@/B@@','</b>').replace('&lt;BR&gt;','<br/>')
    return s

def footer(canvas,doc):
    canvas.saveState(); canvas.setFont('STSong-Light',8); canvas.setFillColor(colors.HexColor('#666666'))
    canvas.drawCentredString(A4[0]/2,8*mm,f'{doc.page}')
    canvas.restoreState()

def read_question_blocks():
    text=QMD.read_text(encoding='utf-8')
    found=[]
    current=None; buf=[]
    for line in text.splitlines():
        if line.startswith('### '):
            if current: found.append((current,'\n'.join(buf).strip()))
            current=line[4:].strip(); buf=[]
        elif current and (line.startswith('## ') or line.startswith('---')):
            found.append((current,'\n'.join(buf).strip())); current=None; buf=[]
        elif current: buf.append(line)
    if current: found.append((current,'\n'.join(buf).strip()))
    return found

# Print-friendly question sheet. Selected tasks are grouped to preserve hand-writing space.
blocks=dict(read_question_blocks())
# 用户硬性要求（2026-10-01 复核重申）：答题纸严格 4 页 A4。16 题按书写量均摊到 4 页。
groups=[['A2','A4','A6','A8'],['A10','A12','A14','A16'],['A18','A20','A22','A24'],['A26','B2','B4','B6']]
qs=[Paragraph('《概率论与数理统计（第二版）》第二章作业',h1),
    Paragraph('姓名：孙承泽　　学号：2253710052　　班级：能动强基2501',small),
    Paragraph('截止日期：10月13日　｜　习题2 A、B两部分偶数号',h2),
    Paragraph('请按题号完整作答；公式和证明写清关键步骤。题目依据第二版印刷页50–53誊录。',small),Spacer(1,5*mm)]
for gi,group in enumerate(groups):
    if gi: qs.append(PageBreak())
    for label in group:
        body=blocks[label]
        # Question statements in Markdown contain display-math delimiters; PDF uses readable plain notation.
        qs.append(Paragraph(rich_text(f'**{label}**　{body.replace(chr(10)," ")}'),h3))
        line_count={'A2':6,'A4':6,'A6':6,'A8':7,'A10':8,'A12':8,'A14':8,'A16':8,'A18':8,'A20':7,'A22':10,'A24':7,'A26':7,'B2':9,'B4':8,'B6':7}[label]
        blank=Table([[''] for _ in range(line_count)],colWidths=[176*mm],rowHeights=[5.6*mm]*line_count)
        blank.setStyle(TableStyle([('LINEBELOW',(0,0),(-1,-1),.28,colors.HexColor('#b7b7b7'))]))
        qs += [blank,Spacer(1,3*mm)]
SimpleDocTemplate(str(QPDF),pagesize=A4,rightMargin=17*mm,leftMargin=17*mm,topMargin=13*mm,bottomMargin=13*mm).build(qs,onFirstPage=footer,onLaterPages=footer)

def _page_count(path):
    try:
        import pymupdf
        with pymupdf.open(str(path)) as d:
            return d.page_count
    except Exception:
        return len(re.findall(rb'/Type\s*/Page[^s]', Path(path).read_bytes()))

NP=_page_count(QPDF)
print(f'[gate] 答题纸页数={NP}（用户硬性要求：严格4页）')
assert NP==4, f'答题纸页数门禁失败：实际{NP}页 != 4页'

# Markdown-to-PDF layout for full worked solutions.
def build_answer_story():
    lines=AMD.read_text(encoding='utf-8').splitlines()
    story=[]; para=[]; i=0
    def flush():
        nonlocal para
        if para:
            txt=' '.join(x.strip() for x in para)
            story.append(Paragraph(rich_text(txt),sol)); para=[]
    while i<len(lines):
        line=lines[i]
        if not line.strip(): flush(); i+=1; continue
        if line.startswith('# '): flush(); story.append(Paragraph(rich_text(line[2:]),h1)); i+=1; continue
        if line.startswith('## '): flush(); story.append(Paragraph(rich_text(line[3:]),h2)); i+=1; continue
        if line.startswith('### '): flush(); story.append(Paragraph(rich_text(line[4:]),h3)); i+=1; continue
        if line.startswith('|'):
            flush(); rows=[]
            while i<len(lines) and lines[i].startswith('|'):
                cells=[c.strip() for c in lines[i].strip().strip('|').split('|')]
                if not all(re.fullmatch(r':?-{2,}:?',c or '-') for c in cells): rows.append(cells)
                i+=1
            if rows:
                n=max(map(len,rows)); data=[]
                for row in rows:
                    row=row+['']*(n-len(row))
                    data.append([Paragraph(rich_text(c.replace('\\\\','')),cell) for c in row])
                widths=[(A4[0]-36*mm)/n]*n
                t=Table(data,colWidths=widths,repeatRows=1,hAlign='LEFT')
                t.setStyle(TableStyle([('FONTNAME',(0,0),(-1,-1),'STSong-Light'),('GRID',(0,0),(-1,-1),.35,colors.HexColor('#999999')),('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e8edf2')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),4),('RIGHTPADDING',(0,0),(-1,-1),4),('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4)]))
                story.extend([t,Spacer(1,3)])
            continue
        if line.strip()=='>': flush(); i+=1; continue
        if line.startswith('> '): flush(); story.append(Paragraph(rich_text(line[2:]),small)); i+=1; continue
        if line.startswith('- '): flush(); story.append(Paragraph('•　'+rich_text(line[2:]),sol)); i+=1; continue
        if line.strip()=='---': flush(); story.append(Spacer(1,4)); i+=1; continue
        para.append(line); i+=1
    flush()
    return story
SimpleDocTemplate(str(APDF),pagesize=A4,rightMargin=18*mm,leftMargin=18*mm,topMargin=15*mm,bottomMargin=14*mm).build(build_answer_story(),onFirstPage=footer,onLaterPages=footer)
print('Built',QPDF.name,APDF.name)
