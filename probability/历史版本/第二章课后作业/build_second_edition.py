"""由第二版人工校对的 Markdown 题单和答案生成 A4 PDF（非 OCR 原稿）。
依赖 reportlab；执行 python build_second_edition.py。
"""
from pathlib import Path
import re,html
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,KeepTogether,PageBreak

ROOT=Path(__file__).resolve().parent
pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
base=ParagraphStyle('body',fontName='STSong-Light',fontSize=10,leading=16,spaceAfter=5)
head=ParagraphStyle('head',parent=base,fontSize=13,leading=19,spaceBefore=9,spaceAfter=4,keepWithNext=True)
title=ParagraphStyle('title',parent=base,fontSize=17,leading=24,alignment=TA_CENTER,spaceAfter=9)
small=ParagraphStyle('small',parent=base,fontSize=8.4,leading=12)

def P(s,st=base):
 s=html.escape(s).replace('**','').replace('−','-').replace('²','^2').replace('³','^3').replace('·','*')
 s=s.replace('∈','属于').replace('Σ','求和').replace('⌊λ⌋','floor(lambda)').replace('⌊X⌋','floor(X)').replace('⌊x⌋','floor(x)').replace('⇔','等价于').replace('→','对应').replace('～','~')
 for i,x in enumerate('₀₁₂₃₄₅₆₇₈₉'):s=s.replace(x,'_'+str(i))
 s=s.replace('⁻¹','^(-1)')
 return Paragraph(s,st)

def foot(c,d):
 c.saveState();c.setFont('STSong-Light',8);c.drawCentredString(A4[0]/2,9*mm,f'第 {d.page} 页 · 第二版 习题2（A）（B）');c.restoreState()

def build(name,flow):
 SimpleDocTemplate(str(ROOT/name),pagesize=A4,leftMargin=18*mm,rightMargin=18*mm,
                   topMargin=16*mm,bottomMargin=16*mm,title=name,author='孙承泽').build(flow,onFirstPage=foot,onLaterPages=foot)

q=(ROOT/'作业02-第二版第二章AB偶数题.md').read_text()
qs=re.findall(r'^### ([AB]\d+)\n(.*?)(?=^### [AB]\d+|^## |\Z)',q,re.M|re.S)
assert [x for x,_ in qs]==[f'A{i}' for i in range(2,27,2)]+['B2','B4','B6']
flow=[P('第二版概率论｜第二章习题（A）（B）偶数题',title),P('孙承泽　2253710052　能动强基2501　｜　截止10月13日',small),
      P('题源：第二版教材印刷页50—53（上传PDF第4—7页）；A组13题，B组3题。',small)]
for n,body in qs:
 body=re.sub(r'\| X \|.*?\| P \|[^\n]+\|','X取值：-2,-1,0,1,2,3；相应概率：1/15,1/10,1/6,1/3,3/10,1/30。',body,flags=re.S)
 block=[P(n+' 题',head),P(' '.join(t.strip() for t in body.splitlines() if t.strip()))]
 rows=14 if n in ['A22','B2','B4'] else 11 if n in ['A8','A16','A18','A24'] else 8
 t=Table([['']]*rows,colWidths=[170*mm],rowHeights=[6.0*mm]*rows)
 t.setStyle(TableStyle([('LINEBELOW',(0,0),(-1,-1),.26,colors.HexColor('#aaa'))]))
 block.extend([t,Spacer(1,5*mm)]);flow.append(KeepTogether(block))
build('第二版-第二章AB偶数题-答题卷.pdf',flow)

ans=(ROOT/'作业02-第二版第二章AB偶数题-参考答案.md').read_text()
flow=[P('第二版概率论｜第二章习题参考答案',title),P('孙承泽　2253710052　能动强基2501　｜　A组13题 + B组3题',small)]
for line in ans.splitlines()[3:]:
 line=line.strip()
 if not line or line.startswith('# '):continue
 if line.startswith('## '):
  if line=='## B 组': flow.append(PageBreak())
  flow.append(P(line[3:],head))
 elif line.startswith('### '):flow.append(P(line[4:],head))
 elif line.startswith('|'):
  cells=[s.strip() for s in line.strip('|').split('|')]
  if all(re.fullmatch(r'[-: ]+',x) for x in cells):continue
  flow.append(P('  ·  '.join(cells),small))
 else:flow.append(P(line))
build('第二版-第二章AB偶数题-完整解析.pdf',flow)
print('built',len(qs),'questions')
