from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib import colors
from reportlab.lib.units import mm
import os
pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
OUT=os.path.dirname(__file__)
base=ParagraphStyle('base',fontName='STSong-Light',fontSize=9.2,leading=13,spaceAfter=2)
h1=ParagraphStyle('h1',parent=base,fontSize=18,leading=24,alignment=1,spaceAfter=5)
h2=ParagraphStyle('h2',parent=base,fontSize=13,leading=18,spaceBefore=4,spaceAfter=4)
small=ParagraphStyle('small',parent=base,fontSize=8,leading=10)
sol=ParagraphStyle('sol',parent=base,fontSize=9.5,leading=14,spaceAfter=5)

def footer(canvas,doc):
 canvas.saveState(); canvas.setFont('STSong-Light',8); canvas.drawCentredString(A4[0]/2,9*mm,f'第 {doc.page} 页'); canvas.restoreState()

def P(s,sty=base): return Paragraph(s,sty)
qs=[
('1','写出下列随机试验的样本空间：<br/>(1) 袋中有5个球（3白2黑），任取1个观察颜色；(2) 从该袋中不放回取两球并依次观察颜色；(3) 任取3球，记录黑球个数；(4) 给5球编号1—5，任取1球观察号码；(5) 生产某产品直到有10件正品为止，记录总件数；(6) 检查产品，合格记正品、不合格记次品，连续查出2件次品或查满4件即停止，记录结果；(7) 射击半径为R的圆盘，记录弹着点位置。'),
('3','从某班学生中任选一名，A={男生}，B={数学爱好者}，C={班干部}。分别说明下列事件的含义：<br/>(1) A∩B∩C<super>c</super>；　(2) A<super>c</super>∩B∩C<super>c</super>；　(3) (A∪C)<super>c</super>；　(4) A-(B∪C)。'),
('5','化简：<br/>(1) (A∩B)∪(A-B)∪A<super>c</super>；<br/>(2) (A∪B)∩[(A-B)∪(B-A)]<super>c</super>-B。'),
('7','一块表面都涂成红色的正方体被锯成1000个同样大小的小正方体。将小正方体混匀后任取一个，求其两面涂有红色的概率。'),
('9','两艘船停靠同一码头，到达时刻在一昼夜内独立且均匀；停靠时间分别为1 h和2 h。求至少一艘船需要等待一段时间的概率。'),
('11','设P(A)=P(B)=P(C)=1/4，P(A∩B)=P(B∩C)=1/8，P(A∩C)=0。求：(1) A、B、C都发生；(2) 至少一个发生；(3) 都不发生的概率。'),
('13','设A<sub>1</sub>, A<sub>2</sub>, …, A<sub>n</sub>为任意n个事件，用数学归纳法证明容斥公式。'),
('15','从分别标有1,2,…,10的10张卡片中任取3张，求：(1) 最大号码为5；(2) 最小号码为5；(3) 最大号码小于5；(4) 最大号码大于5的概率。'),
('17','100件产品中有80件一等品、15件二等品、5件三等品，任取10件，求其中有7件一等品、2件二等品、1件三等品的概率。'),
('19','从一副52张扑克牌（去掉大、小王）中任取4张，求：(1) 4张同花色；(2) 4张不同花色；(3) 至少有2张同花色；(4) 至少有1张是A。'),
('21','将3个球随机放入4个盒子，求盒中球的最大个数分别为1、2、3的概率。'),
('23','从15双不同的鞋子中任取10只，求：(1) 恰有两双配对；(2) 至少有两双配对的概率。'),
('25','已知P(A)=1/4，P(B|A)=1/3，P(A|B)=1/2，求P(A∪B)。'),
('27','100件中7件次品、93件合格品，每次任取一件且不放回，求第三次才取到合格品的概率。'),
('29','射击小组20人：一级4人、二级8人、三级7人、四级1人；命中10环概率依次为0.9、0.7、0.5、0.2。任选一人，求一次射击命中10环的概率。'),
('31','某地区运营商A、B、C用户比例4:3:2，好评率分别80%、60%、70%。随机抽取一位用户的评价：(1) 好评概率；(2) 已知是好评，求该用户属于B的概率。'),
('33','证明：若A、B、C相互独立，则A∪B、A∩B及A-B都与C相互独立。'),
('35','8张同形卡片：1,2,3,4涂红；1,2,3,5涂白；1,6,7,8涂黑。任取一张，A、B、C分别表示有红、白、黑色。验证P(A∩B∩C)=P(A)P(B)P(C)，但A、B、C不两两独立。'),
('37','三人独立射击同一目标，命中概率分别为4/5、2/3、3/4，求目标被击中的概率。'),
('39','A与B相互独立，且“仅A发生”与“仅B发生”的概率均为1/4，求P(A)、P(B)。')]
# exact four-page grouping (5 questions/page)
groups=[qs[i:i+5] for i in range(0,20,5)]
story=[]
for gi,g in enumerate(groups):
 if gi==0:
  story += [P('《9.22  概率论作业-孙承泽》',h1),P('姓名：孙承泽　学号：2253710052　班级：能动强基2501',small),P('第一章　随机事件与概率　｜　奇数题',h2)]
 else: story += [P('《9.22  概率论作业-孙承泽》（续）',h2)]
 for n,t in g:
  story.append(P(f'<b>{n}.</b> {t}'))
  # answer ruled space, adaptive
  lines=4 if n in {'1','13','19','23','33','35'} else 5
  data=[[''] for _ in range(lines)]
  tab=Table(data,colWidths=[176*mm],rowHeights=[5.7*mm]*lines)
  tab.setStyle(TableStyle([('LINEBELOW',(0,0),(-1,-1),0.25,colors.HexColor('#aaaaaa'))]))
  story.append(tab); story.append(Spacer(1,1.5*mm))
 if gi<3: story.append(PageBreak())
SimpleDocTemplate(os.path.join(OUT,'9.22概率论作业-孙承泽-试卷.pdf'),pagesize=A4,rightMargin=16*mm,leftMargin=16*mm,topMargin=12*mm,bottomMargin=14*mm).build(story,onFirstPage=footer,onLaterPages=footer)

S=[
('1','(1) {白,黑}。 (2) {白白,白黑,黑白,黑黑}。 (3) {0,1,2}。 (4) {1,2,3,4,5}。 (5) {10,11,12,…}。 (6) {次次, 正次次, 正正正正, 正正正次, 正正次正, 正正次次, 正次正正, 正次正次, 次正正正, 次正正次, 次正次正, 次正次次}；即首次出现“次次”便停止，或查满4件且前三次中未出现“次次”。 (7) 样本空间={(x,y):x<super>2</super>+y<super>2</super>≤R<super>2</super>}。'),
('3','直接按“交=且、横线=不”翻译：(1) 是男生、爱好数学且不是班干部；(2) 不是男生、爱好数学且不是班干部；(3) 由德摩根律，既不是男生也不是班干部；(4) 是男生，但既不爱好数学也不是班干部。'),
('5','(1) (A∩B)∪(A-B)=A，故再并A<super>c</super>得全集。 (2) 令D=(A-B)∪(B-A)（A、B恰有一个发生）。在A∪B内，D<super>c</super>表示A、B同时发生，所以(A∪B)∩D<super>c</super>=A∩B；再减去B，得空集。'),
('7','1000=10<super>3</super>，故每条棱被分成10段。恰有两面涂红的是12条棱上除去角块的小块，共12(10-2)=96个。因此P=96/1000=12/125。'),
('9','设两船到达时刻为x、y。直接计算“发生等待”的两条对角带：当x≤y时，需x＜y＜x+1，面积为23×1+1×1/2=47/2；当y＜x时，需y＜x＜y+2，面积为22×2+2×2/2=46。两区域不相交，故总面积为47/2+46=139/2。因此P(等待)=(139/2)/24<super>2</super>=139/1152。注意第一条带末端是半个1×1三角形，不能按面积24计算。'),
('11','因A∩C为空集，故A∩B∩C也为空集，(1) 0。容斥：(2) 3/4-1/8-1/8-0+0=1/2。(3) 1-1/2=1/2。'),
('13','当n=2时，结论就是加法公式，成立。假设n个事件时结论成立，记<br/>U<sub>n</sub>=A<sub>1</sub>∪A<sub>2</sub>∪…∪A<sub>n</sub>。<br/>加入事件A<sub>n+1</sub>，由加法公式：<br/>P(U<sub>n</sub>∪A<sub>n+1</sub>)=P(U<sub>n</sub>)+P(A<sub>n+1</sub>)-P(U<sub>n</sub>∩A<sub>n+1</sub>)。<br/>其中<br/>U<sub>n</sub>∩A<sub>n+1</sub>=(A<sub>1</sub>∩A<sub>n+1</sub>)∪…∪(A<sub>n</sub>∩A<sub>n+1</sub>)。<br/>分别对P(U<sub>n</sub>)和上式右端的并事件使用归纳假设，再按交集中所含事件的个数合并，正好得到n+1个事件的容斥公式。因此结论对任意n成立。'),
('15','样本数C(10,3)。(1) 必含5，另2张从1—4选：C(4,2)/C(10,3)=1/20。(2) 必含5，另2张从6—10选：C(5,2)/120=1/12。(3) 三张均从1—4选：C(4,3)/120=1/30。(4) 用补事件：1-C(5,3)/120=11/12。'),
('17','多项超几何分布：P=C(80,7)C(15,2)C(5,1)/C(100,10)。'),
('19','总数为C(52,4)。(1) 先选花色，再从该花色13张中选4张：P=4C(13,4)/C(52,4)。(2) 四种花色各取1张：P=13<super>4</super>/C(52,4)。(3) “至少有2张同花色”的对立事件是“四张花色各不相同”，恰好就是第(2)问。因此P=1-13<super>4</super>/C(52,4)=18628/20825。(4) 用补事件：P=1-C(48,4)/C(52,4)。'),
('21','把3个可区分球独立放入4盒，共4<super>3</super>种。(最大=1)：4·3·2=24，P=3/8。(最大=3)：4种，P=1/16。(最大=2)：余下64-24-4=36，P=9/16。'),
('23','总数C(30,10)。若恰有k双：先选k双，再从余下15-k双中选10-2k双，并从每双取1只，数为C(15,k)C(15-k,10-2k)2^(10-2k)。(1) k=2，除以C(30,10)。(2) 对k=2,3,4,5求和后除以C(30,10)。'),
('25','P(A∩B)=P(A)P(B|A)=1/12。由P(A|B)=1/2得P(B)=P(A∩B)/(1/2)=1/6。故P(A∪B)=1/4+1/6-1/12=1/3。'),
('27','第三次才合格意味着前两次均次品、第三次合格：P=(7/100)(6/99)(93/98)=217/53900≈0.004026。'),
('29','全概率：P=4/20·0.9+8/20·0.7+7/20·0.5+1/20·0.2=0.645。'),
('31','(1) P(好)=4/9·0.8+3/9·0.6+2/9·0.7=32/45。(2) 贝叶斯：P(B|好)=(3/9·0.6)/(32/45)=9/32。'),
('33','由相互独立，P((A∪B)C)=P(AC)+P(BC)-P(ABC)=P(C)[P(A)+P(B)-P(AB)]=P(C)P(A∪B)。又P(ABC)=P(AB)P(C)。最后P((A-B)C)=P(AC)-P(ABC)=P(C)[P(A)-P(AB)]=P(C)P(A-B)。故三者均与C独立。'),
('35','A={1,2,3,4}，B={1,2,3,5}，C={1,6,7,8}，各概率均1/2；ABC={1}，P(ABC)=1/8=(1/2)<super>3</super>。但AB={1,2,3}，P(AB)=3/8≠1/4=P(A)P(B)，故至少A、B不独立，三事件不两两独立。'),
('37','用补事件：P(至少一人命中)=1-(1-4/5)(1-2/3)(1-3/4)=1-1/60=59/60。'),
('39','令x=P(A), y=P(B)。独立性给x(1-y)=1/4，y(1-x)=1/4。两式相减得x=y。于是x(1-x)=1/4，即(x-1/2)<super>2</super>=0，故P(A)=P(B)=1/2。')]
story=[P('9.22 概率论作业—完整解析',h1),P('孙承泽　2253710052　能动强基2501',small),P('记号：∩表示交，∪表示并，A<super>c</super>表示A的对立事件，C(n,k)表示组合数。',small)]
for n,t in S: story += [P(f'<b>第{n}题</b>',h2),P(t,sol)]
SimpleDocTemplate(os.path.join(OUT,'9.22概率论作业-孙承泽-完整解析.pdf'),pagesize=A4,rightMargin=18*mm,leftMargin=18*mm,topMargin=14*mm,bottomMargin=14*mm).build(story,onFirstPage=footer,onLaterPages=footer)

report=[P('9.22 概率论作业题质量分析报告',h1),P('分析对象：第一章“随机事件与概率”习题1的奇数题（1—39）',small),P('一、总体结论',h2),P('题组覆盖样本空间、事件运算、古典概型、几何概型、组合计数、条件概率、全概率与贝叶斯公式、独立性等第一章主干。20道题由概念辨析逐步过渡到综合计算与证明，覆盖面较完整，适合作为章节作业；但题量较大，且部分表述依赖教材排版，扫描质量会影响补集横线辨认。',sol),P('二、知识点与难度结构',h2)]
rows=[['模块','对应题号','难度'],['样本空间与事件运算','1,3,5','基础—中等'],['古典/几何概型与组合计数','7,9,15,17,19,21,23,27','中等'],['概率性质与容斥','11,13','中等—较难'],['条件概率、全概率、贝叶斯','25,29,31','中等'],['独立性及证明','33,35,37,39','中等—较难']]
t=Table(rows,colWidths=[48*mm,82*mm,35*mm]);t.setStyle(TableStyle([('FONTNAME',(0,0),(-1,-1),'STSong-Light'),('FONTSIZE',(0,0),(-1,-1),9),('GRID',(0,0),(-1,-1),.4,colors.grey),('BACKGROUND',(0,0),(-1,0),colors.HexColor('#dddddd')),('VALIGN',(0,0),(-1,-1),'MIDDLE')]))
report += [t,P('三、优点',h2),P('1. 覆盖链条完整：从集合语言到概率模型，再到条件概率和独立性。<br/>2. 计算题与证明题并存，既检查操作熟练度，也检查逻辑表达。<br/>3. 15、17、19、21、23题形成组合计数梯度；29、31题形成全概率—贝叶斯衔接；33、35、39题能纠正常见的独立性误区。',sol),P('四、主要风险与易错点',h2),P('第1题须区分“试验结果”与数值记录；第3、5题补集横线容易误读；第9题需明确24小时边界模型；第11题要利用A∩C为空集推出A∩B∩C为空集；第15、19、23题易重复计数；第31题后验概率分母须用全概率；第35题展示“三者乘积等式成立”不等于两两独立；第39题须把“仅A/仅B”翻译为A∩B的补集部分与A的补集∩B。',sol),P('五、工作量与建议',h2),P('预计熟练学生完成题面约150—210分钟，完整规范书写约210—300分钟。四面答题纸只能提供“关键过程”空间，复杂证明和组合题建议另附草稿纸。建议评分时将题3、5的集合符号识读与数学推理分开；第9题若学生说明采用环形24小时模型，应按其模型复核，而不应仅按单一数值判错。',sol),P('六、质量评级',h2),P('知识覆盖：A；难度梯度：A-；表述清晰度：B+（扫描补集横线与第9题边界存在歧义）；计算训练价值：A；概念诊断价值：A。综合评价：A-。',sol)]
SimpleDocTemplate(os.path.join(OUT,'9.22概率论作业-题目质量分析报告.pdf'),pagesize=A4,rightMargin=18*mm,leftMargin=18*mm,topMargin=14*mm,bottomMargin=14*mm).build(report,onFirstPage=footer,onLaterPages=footer)
print('done')
