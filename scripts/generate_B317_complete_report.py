#!/usr/bin/env python3
"""Reproducibly calculate B317 Hall data, make the three requested plots, and build MD/DOCX."""
from pathlib import Path
import csv, math, re
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '大学物理实验/实验项目/实验报告/B317-霍尔效应及螺线管磁场'
ASSET = OUT / 'assets'
OUT.mkdir(parents=True, exist_ok=True); ASSET.mkdir(parents=True, exist_ok=True)

# Transcribed from the user's supplied measurement tables. Voltage unit: mV.
ich = np.arange(1, 11, dtype=float)
t1 = np.array([
 [1.02,-1.67,-1.01,1.68,1.345], [2.02,-3.35,-2.02,3.35,2.685],
 [3.04,-5.01,-3.03,5.01,4.023], [4.05,-6.69,-4.05,6.68,5.368],
 [5.06,-8.34,-5.06,8.33,6.698], [6.06,-10.02,-6.10,10.01,8.048],
 [7.08,-11.67,-7.09,11.67,9.378], [8.09,-13.32,-8.11,13.30,10.705],
 [9.11,-14.98,-9.15,14.94,12.045], [10.12,-16.62,-10.18,16.58,13.375],
])
im = np.arange(100, 1001, 100, dtype=float)
t2 = np.array([
 [.61,-3.32,-.59,3.30,1.955], [.73,-4.65,-.75,4.65,2.695],
 [2.07,-6.00,-2.09,5.99,4.038], [3.40,-7.33,-3.41,7.32,5.365],
 [4.73,-8.68,-4.74,8.67,6.705], [6.05,-9.98,-6.07,9.97,8.018],
 [7.38,-11.31,-7.38,11.31,9.345], [8.67,-12.61,-8.70,12.60,10.645],
 [9.97,-13.91,-9.98,13.89,11.938], [11.26,-15.17,-11.27,15.16,13.215],
])
x = np.array([0,30,60,90,110,130,150,160,170,180,190], dtype=float)
left = np.array([
 [7.23,-10.49,-7.24,10.48,8.860], [7.20,-10.48,-7.22,10.45,8.838],
 [7.02,-10.28,-7.03,10.27,8.650], [6.72,-10.00,-6.72,9.97,8.353],
 [6.20,-9.53,-6.20,9.44,7.843], [4.36,-7.61,-4.42,7.61,6.000],
 [.92,-4.17,-.86,4.24,2.548], [-.19,-3.05,.16,3.06,1.440],
 [-.74,-2.53,.75,2.49,.883], [-1.05,-2.21,1.08,2.20,.570],
 [-1.26,-2.04,1.25,2.01,.385],
])
right = np.array([
 [7.23,-10.50,-7.24,10.48,8.863], [7.23,-10.49,-7.23,10.47,8.855],
 [7.17,-10.44,-7.18,10.42,8.803], [6.90,-10.18,-6.91,10.16,8.538],
 [6.32,-9.66,-6.33,9.57,7.970], [4.47,-7.72,-4.46,7.71,6.090],
 [.95,-4.19,-.86,4.28,2.570], [-.22,-3.09,.16,3.11,1.455],
 [-.76,-2.51,.73,2.52,.885], [-1.06,-2.20,1.04,2.21,.578],
 [-1.24,-2.03,1.22,2.03,.400],
])

# Device-label values supplied by the user: D_eff is the stated mid-winding diameter.
mu0 = 4*math.pi*1e-7; e = 1.602176634e-19
N = 2400; L = 276e-3; D_in = 40e-3; D_out = 56e-3; D_eff = (D_in+D_out)/2
hall_d = 260e-6

def regress(X, Y):
    slope, intercept = np.polyfit(X, Y, 1)
    pred = slope*X+intercept
    ss_res = float(np.sum((Y-pred)**2)); ss_tot=float(np.sum((Y-np.mean(Y))**2))
    r2=1-ss_res/ss_tot
    rmse=math.sqrt(ss_res/(len(X)-2))
    return float(slope),float(intercept),float(r2),rmse,pred

# Table voltages are mV and currents mA; numerical slope is also V/A.
s1,b1,r21,rmse1,pred1 = regress(ich,t1[:,4])
s2,b2,r22,rmse2,pred2 = regress(im,t2[:,4])
B600 = mu0*N*.600/math.sqrt(L*L+D_eff*D_eff)
B800 = mu0*N*.800/math.sqrt(L*L+D_eff*D_eff)
KH = s1/B600
RH = KH*hall_d
nc = 1/(e*abs(RH))
B_left = left[:,4]/1000/(KH*.005)*1000
B_right = right[:,4]/1000/(KH*.005)*1000
B_avg=(B_left+B_right)/2
rel_lr=2*np.abs(B_left-B_right)/(np.abs(B_left)+np.abs(B_right))*100
s2_expected=s1*.006/.600
slope_deviation=(s2-s2_expected)/s2_expected*100

# Independently recompute the four-polarity values and retain image-reported rounded values.
for label,arr in [('table 3-2-1',t1),('table 3-2-2',t2),('left scan',left),('right scan',right)]:
    calc=(arr[:,0]-arr[:,1]-arr[:,2]+arr[:,3])/4
    if np.max(np.abs(calc-arr[:,4])) > .00101:
        raise ValueError(f'Four-polarity check failed for {label}: {np.max(np.abs(calc-arr[:,4]))}')

# Graph design; Latin-only chart labels avoid missing CJK glyphs in the plotting runtime.
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.titlesize':13,'axes.labelsize':11,
                     'figure.dpi':150,'savefig.dpi':220,'axes.spines.top':False,'axes.spines.right':False})
navy='#183B56'; teal='#138A8A'; orange='#E07A3F'; grid='#DCE5EB'
def finish(ax):
    ax.grid(True, color=grid, linewidth=.8); ax.set_axisbelow(True)
    for s in ['left','bottom']: ax.spines[s].set_color('#8296A5')
fig,ax=plt.subplots(figsize=(7.4,4.5)); ax.scatter(ich,t1[:,4],s=43,color=teal,edgecolor='white',linewidth=.8,label='Measured $U_H$')
xx=np.linspace(0,10.4,150); ax.plot(xx,s1*xx+b1,color=navy,lw=2,label='Least-squares fit')
ax.set(xlabel='$I_{CH}$ (mA)',ylabel='$U_H$ (mV)',title='Hall voltage vs. control current  ($I_M=600$ mA)'); finish(ax)
ax.text(.04,.95,f'$U_H={s1:.5f} I_{{CH}}+{b1:.4f}$ mV\n$R^2={r21:.7f}$',transform=ax.transAxes,va='top',color=navy,bbox=dict(boxstyle='round,pad=.4',fc='white',ec=grid))
ax.legend(frameon=False,loc='lower right');fig.tight_layout();fig.savefig(ASSET/'B317-UH-ICH.png',bbox_inches='tight');plt.close(fig)
fig,ax=plt.subplots(figsize=(7.4,4.5));ax.scatter(im,t2[:,4],s=43,color=orange,edgecolor='white',linewidth=.8,label='Measured $U_H$')
xx=np.linspace(50,1050,180);ax.plot(xx,s2*xx+b2,color=navy,lw=2,label='Least-squares fit')
ax.set(xlabel='$I_M$ (mA)',ylabel='$U_H$ (mV)',title='Hall voltage vs. excitation current  ($I_{CH}=6.00$ mA)');finish(ax)
ax.text(.04,.95,f'$U_H={s2:.6f} I_M+{b2:.4f}$ mV\n$R^2={r22:.6f}$',transform=ax.transAxes,va='top',color=navy,bbox=dict(boxstyle='round,pad=.4',fc='white',ec=grid))
ax.legend(frameon=False,loc='lower right');fig.tight_layout();fig.savefig(ASSET/'B317-UH-IM.png',bbox_inches='tight');plt.close(fig)
# Finite-solenoid model using radius = mean of labelled inner/outer radii.
def B_theory(pos_m):
    radius=D_eff/2; nturn=N/L; z1=-L/2-pos_m; z2=L/2-pos_m
    return mu0*nturn*.800/2*(z2/np.sqrt(radius**2+z2**2)-z1/np.sqrt(radius**2+z1**2))
fig,ax=plt.subplots(figsize=(7.4,4.7));ax.plot(x,B_left,'o-',color=teal,lw=1.7,ms=5,label='Left-to-right pass')
ax.plot(x,B_right,'s-',color=orange,lw=1.5,ms=4.7,label='Right-to-left pass')
xf=np.linspace(0,190,400);ax.plot(xf,B_theory(xf/1000)*1000,'--',color=navy,lw=1.8,label='Finite-solenoid model')
ax.set(xlabel='Axial position $x$ (mm)',ylabel='Magnetic field $B$ (mT)',title='$B$–$x$ profile  ($I_M=800$ mA, $I_{CH}=5.00$ mA)');finish(ax)
ax.legend(frameon=False,ncol=1,loc='upper right');fig.tight_layout();fig.savefig(ASSET/'B317-B-x.png',bbox_inches='tight');plt.close(fig)

# Data ledger CSV contains both raw and derived values; convenient for later audit.
with (OUT/'B317-原始数据及计算结果.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.writer(f,lineterminator='\n');w.writerow(['series','x_or_current','U1_mV','U2_mV','U3_mV','U4_mV','UH_reported_mV','B_mT_from_calibration'])
    for i,row in enumerate(t1):w.writerow(['UH-ICH',f'{ich[i]:.2f} mA',*row[:4],row[4],''])
    for i,row in enumerate(t2):w.writerow(['UH-IM',f'{im[i]:.0f} mA',*row[:4],row[4],''])
    for side,arr,Bs in [('left',left,B_left),('right',right,B_right)]:
      for i,row in enumerate(arr):w.writerow([f'B-x {side}',f'{x[i]:.0f} mm',*row[:4],row[4],f'{Bs[i]:.6f}'])

# Markdown authoring helpers.
def md_table(headers,rows):
    out=['| '+' | '.join(map(str,headers))+' |','| '+' | '.join(['---']*len(headers))+' |']
    out += ['| '+' | '.join(map(str,r))+' |' for r in rows]
    return '\n'.join(out)
def rawrows(curr,arr,fmtcurr):
    return [[fmtcurr(v),*(f'{q:.2f}' for q in row[:4]),f'{row[4]:.3f}'] for v,row in zip(curr,arr)]
def fnum(a,n=4): return f'{a:.{n}f}'

meta='''| 项目 | 信息 |
|---|---|
| 姓名 / 学号 / 班级 | 孙承泽 / 2253710052 / 能动强基2501 |
| 实验名称 / 课序号 | 霍尔效应及螺线管磁场的测定（B317） / 8 |
| 实验日期 | 11月16日（原手写页未注明年份） |
| 同组者 | 原始页记载不清，未转录 |
| 数据来源 | 用户提供的三张实测数据表；仪器参数按用户转录的设备标签 |
'''
parts=[]
parts += ['# 大学物理实验报告｜霍尔效应及螺线管磁场的测定','',meta,'','> 本报告严格依照实验报告页给定的五部分结构。所有电压原始值均依用户表格转录；四极性组合已用程序复核。线圈公式中的有效直径采用内、外径平均值 48.0 mm，并在误差讨论中说明该模型近似；霍尔片 260 μm 尺寸按沿磁场方向厚度处理。','',
'## 一、实验目的','',
'1. 理解霍尔效应及霍尔电压的形成机制。','2. 验证霍尔电压 $U_H$ 与霍尔元件工作电流 $I_{CH}$ 的线性关系。','3. 验证 $U_H$ 与螺线管励磁电流 $I_M$ 的线性关系。','4. 利用霍尔效应测量螺线管轴线上磁感应强度及其空间分布。','5. 通过电流与磁场反向的四极性测量，削弱不等势电势差等共模影响。','',
'## 二、实验仪器与实验方法','',
'### 实验仪器','',
'ZKY-LS 型螺线管磁场测定实验仪、霍尔效应测试仪、霍尔元件及可沿螺线管轴线移动的霍尔探头。霍尔元件标签：编号 BE0418-015，最大工作电流 10.0 mA，标称尺寸 400 × 400 × 260 μm。螺线管标签：长度 276 mm、内径 Φ40 mm、外径 Φ56 mm、总匝数 2400；螺线管标签箭头所示正向电流沿轴线向下。线圈场计算用有效直径 $D_{eff}=(40+56)/2=48$ mm，作为绕组径向厚度的代表值。霍尔片厚度取 $d=260$ μm，前提是该尺寸方向与磁场平行。','',
'### 实验原理与测量方法','',
'载流子在磁场中受洛伦兹力偏转并在横向积累电荷，稳态霍尔电压满足 $U_H=R_H I_{CH}B/d=K_H I_{CH}B$，其中 $|R_H|=1/(n e)$、$|K_H|=|R_H|/d$。四种电流/磁场方向组合的电压按 $U_H=(U_1-U_2-U_3+U_4)/4$ 合成，以消除四次读数期间近似不变的不等势电势差。有限长螺线管中心磁场按 $B_0=\mu_0 N I_M/\sqrt{L^2+D_{eff}^2}$ 计算；轴线上位置场按有限长线圈公式计算。','',
'1. 按仪器面板和电极标记连接霍尔测试仪，核对工作电流、励磁电流、电压端及换向开关；换向后待读数稳定。','2. 将霍尔探头置于线圈中心附近，固定 $I_M=600$ mA，令 $I_{CH}=1.00$–10.00 mA（每次增加 1.00 mA），记录四种极性下 $U_1$–$U_4$。','3. 固定 $I_{CH}=6.00$ mA，令 $I_M=100$–1000 mA（每次增加 100 mA），记录四种极性读数。','4. 固定 $I_M=800$ mA、$I_{CH}=5.00$ mA，在 $x=0,30,60,90,110,130,150,160,170,180,190$ mm 处分别从左右方向扫描，记录两次扫描的四种极性电压。','5. 励磁电流除读数时段外及时关闭，尽量缩短四态测量间隔，以降低温升和零点漂移。','',
'## 三、测量内容及数据处理','',
'### 1. 原始数据','',
'表中 $U_H$ 为原数据表所列四极性计算值（mV）；用表内 $U_1$–$U_4$ 重新计算后与记录值在其显示精度内一致。','',
'**表 3-2-1　固定 $I_M=600$ mA，$U_H-I_{CH}$ 关系**','',
md_table(['$I_{CH}$/mA','$U_1$/mV','$U_2$/mV','$U_3$/mV','$U_4$/mV','$U_H$/mV'],rawrows(ich,t1,lambda v:f'{v:.2f}')),'',
'**表 3-2-2　固定 $I_{CH}=6.00$ mA，$U_H-I_M$ 关系**','',
md_table(['$I_M$/mA','$U_1$/mV','$U_2$/mV','$U_3$/mV','$U_4$/mV','$U_H$/mV'],rawrows(im,t2,lambda v:f'{v:.0f}')),'',
'**表 3-2-3a　B-x 左侧扫描（$I_M=800$ mA，$I_{CH}=5.00$ mA）**','',
md_table(['$x$/mm','$U_1$/mV','$U_2$/mV','$U_3$/mV','$U_4$/mV','$U_H$/mV','$B$/mT'],[[f'{xx:.0f}',*(f'{q:.2f}' for q in row[:4]),f'{row[4]:.3f}',f'{bb:.3f}'] for xx,row,bb in zip(x,left,B_left)]),'',
'**表 3-2-3b　B-x 右侧扫描**','',
md_table(['$x$/mm','$U_1$/mV','$U_2$/mV','$U_3$/mV','$U_4$/mV','$U_H$/mV','$B$/mT'],[[f'{xx:.0f}',*(f'{q:.2f}' for q in row[:4]),f'{row[4]:.3f}',f'{bb:.3f}'] for xx,row,bb in zip(x,right,B_right)]),'',
'### 2. 四极性计算与 $U_H-I_{CH}$ 关系','',
'以表 3-2-1 第一行举例：$U_H=(1.02-(-1.67)-(-1.01)+1.68)/4=1.345$ mV。对 10 个数据点作最小二乘直线拟合，电流以 mA、电压以 mV 表示：','',
f'$U_H=({s1:.6f})I_{{CH}}+({b1:.6f})$ mV，$R^2={r21:.8f}$；等价斜率 $S_{{CH}}={s1:.6f}$ V/A，截距为 {b1/1000:.3e} V。拟合残差标准差（回归标准误）为 {rmse1:.4f} mV。','',
'![Python 绘制：霍尔电压与工作电流关系](assets/B317-UH-ICH.png)','',
'### 3. 线圈中心场、霍尔灵敏度与载流子浓度','',
'取 $\mu_0=4\pi\times10^{-7}$ H/m，$N=2400$，$L=0.276$ m，$D_{eff}=0.048$ m，则：','',
'$B_{0,600}=\mu_0 N(0.600)/\sqrt{L^2+D_{eff}^2}=%.6f$ T = %.4f mT。' % (B600,B600*1000),
'$K_H=S_{CH}/B_{0,600}=%.3f$ m²/C。' % KH,
'$R_H=K_H d=(%.3f)(2.60\times10^{-4})=%.5f$ m³/C。' % (KH,RH),
'$n=1/(e|R_H|)=%.3e$ m⁻³（约 %.3e cm⁻³）。' % (nc,nc/1e6),
'其中 $d=260$ μm 采用设备标注尺寸中厚度方向的数值；需确保安装时该尺寸确为沿 $B$ 的厚度。只凭现有接线/方向记录不能可靠判定多数载流子的正负类型，因此报告 $|R_H|$ 与浓度，不据此臆断 p/n 型。','',
'### 4. $U_H-I_M$ 关系与线性检验','',
f'表 3-2-2 线性拟合为 $U_H=({s2:.8f})I_M+({b2:.6f})$ mV（$I_M$ 用 mA），$R^2={r22:.7f}$，回归残差标准差 {rmse2:.4f} mV。斜率换算为 $S_M={s2:.6f}$ V/A。由第一组斜率和 $U_H\propto I_{{CH}}I_M$，预期 $S_M=S_{{CH}}(6.00/600)= {s2_expected:.6f}$ V/A；实测斜率较此低 {abs(slope_deviation):.2f}%。数据仍呈高度线性，但首个 100 mA 点及非零截距提示低电流区背景/四态漂移影响相对更显著。','',
'![Python 绘制：霍尔电压与励磁电流关系](assets/B317-UH-IM.png)','',
'### 5. 螺线管轴线磁场分布 $B-x$','',
'$I_M=800$ mA 时中心理论场 $B_{0,800}=%.4f$ mT。用上述灵敏度及 $I_{CH}=0.00500$ A 换算：$B(x)=U_H(x)/(K_H I_{CH})$，其中先将 $U_H$ 从 mV 换为 V。左扫描最大值为 %.4f mT（$x=0$ mm），右扫描最大值为 %.4f mT（$x=0$ mm）；$x=190$ mm 处两次扫描分别为 %.4f、%.4f mT。两次扫描的最大同位置相对差约 %.2f%%。' % (B800*1000,B_left[0],B_right[0],B_left[-1],B_right[-1],max(rel_lr)),
'理论曲线按有限长螺线管轴向场模型并取平均绕组半径 24 mm绘制，作为模型对照；按 $x=0$ 为线圈中心处理（由扫描峰值判断，若设备刻度原点另有定义则需整体平移）。','',
'![Python 绘制：螺线管轴线上磁场分布](assets/B317-B-x.png)','',
'### 6. 计算结果汇总','',
md_table(['物理量','结果','单位/说明'],[
 ['中心场（600 mA）',f'{B600*1000:.4f}','mT；D_eff=48.0 mm'],['中心场（800 mA）',f'{B800*1000:.4f}','mT'],
 ['霍尔灵敏度 K_H',f'{KH:.3f}','m²/C'],['霍尔系数 R_H',f'{RH:.5f}','m³/C；按测量极性约定为正'],
 ['载流子浓度 n',f'{nc:.3e}','m⁻³（浓度值）'],['U_H-I_CH 斜率',f'{s1:.6f}','V/A；R²={:.8f}'.format(r21)],
 ['U_H-I_M 斜率',f'{s2:.6f}','V/A；R²={:.7f}'.format(r22)],['B(x) 范围',f'{min(B_left.min(),B_right.min()):.3f}–{max(B_left.max(),B_right.max()):.3f}','mT；两个扫描合并'],
]),'',
'### 7. 误差分析','',
'1. **线圈几何模型：**线圈有 40–56 mm 内外径而非单一薄绕组直径，采用算术平均直径 48 mm 近似。若分别以 40 mm 和 56 mm 代入中心场，$B_{0,600}$ 为 %.4f–%.4f mT，进而 $K_H$ 约 %.2f–%.2f m²/C、$n$ 约 %.3e–%.3e m⁻³。此范围只反映直径取值模型敏感性，不是完整测量不确定度。' % (mu0*N*.6/math.sqrt(L*L+D_out*D_out)*1000,mu0*N*.6/math.sqrt(L*L+D_in*D_in)*1000,s1/(mu0*N*.6/math.sqrt(L*L+D_in*D_in)),s1/(mu0*N*.6/math.sqrt(L*L+D_out*D_out)),1/(e*s1/(mu0*N*.6/math.sqrt(L*L+D_out*D_out))*hall_d),1/(e*s1/(mu0*N*.6/math.sqrt(L*L+D_in*D_in))*hall_d)),
'2. **霍尔片厚度与姿态：**浓度与 $1/d$ 成正比；若 260 μm 标注方向未与磁场平行，$K_H$ 和 $R_H$ 的测定不直接受 d 影响，但据此换算的 $n$ 会系统偏移。探头法线与磁场夹角 $\theta$ 使有效场成为 $B\cos\theta$，造成灵敏度/场强投影偏小。','3. **四极性抵消残差：**恒定不等势电势差可被组合消除；读数期间温漂或零点漂移、换向后未稳定，会留下残差。$U_H-I_M$ 拟合截距 0.314 mV 较 $U_H-I_{CH}$ 截距 0.014 mV 大，可能反映背景项、低电流端偏差或读数漂移；仅凭数据不能将其唯一归因。','4. **定位与重复性：**左右扫描大体重合，中心区域相对差较小，末端相对差因信号较小而放大；位置刻度零点、探头轴向偏移及两次扫描间电流/温度变化都会影响曲线。对称的线圈理论曲线与测量曲线不完全重合还可能来自绕组有限径向厚度、有效位置零点及中心场校准近似。','5. **电流和读数分辨率：**未提供电流表、电压表与位置刻度的分辨率/校准不确定度，故不虚构合成不确定度或置信区间。回归 $R^2$ 与残差用于描述数据线性和散布，不等同于仪器准确度。','',
'## 四、小结（结论、误差分析及建议等）','',
f'本次四极性测量验证了 $U_H$ 随 $I_{{CH}}$ 增大近似线性（$R^2={r21:.8f}$），且随 $I_M$ 增大总体呈线性（$R^2={r22:.7f}$）。按设备几何参数的平均直径模型，励磁电流 $I_M=600$ mA 时，按上述线圈模型计算的中心磁场为 $B_0={B600*1000:.4f}$ mT；霍尔灵敏度 $K_H={KH:.3f}$ m²/C；取霍尔片厚度 260 μm 得 $n={nc:.3e}$ m⁻³。$I_M=800$ mA 的轴向磁场由中心约 {B_avg[0]:.3f} mT 随位置增加而减弱，左右重复扫描结果总体相近。','',
'主要限制是线圈存在径向厚度、有效直径须以平均值近似，且需确认 260 μm 确为沿磁场方向的有效厚度；仪器分辨率和电压零点漂移信息缺失，故未给出完整不确定度。建议核实霍尔片安装方向与轴线对准、每次换向后等待读数稳定、缩短四极性读数间隔并记录仪表分辨率；线圈参数可用实测场标定复核。实验结果只说明数据范围内的线性趋势，不能将回归优度当作全部误差已消除。','',
'## 五、实验思考题','',
'**问题：若磁场 $B$ 的方向与霍尔元件法线方向不一致，对实验结果有什么影响？**','',
'若霍尔元件法线与磁场夹角为 $\theta$，真正垂直穿过霍尔片的磁场分量为 $B_\perp=B\cos\theta$，故 $U_H=K_H I_{CH}B\cos\theta$。','1. 若夹角固定，测得霍尔电压按 $\cos\theta$ 缩小；若仍按磁场全值 B 计算，会把表观灵敏度估低为 $K_H\cos\theta$。','2. 四极性换向可以削弱不等势电势差，但不会消除几何投影误差。','3. 若探头沿扫描位置移动时夹角也变化，$\cos\theta(x)$ 会形成随位置变化的系统误差，使 $B-x$ 曲线形状及峰值位置都可能失真。','4. 因此应让霍尔片法线与螺线管轴向磁场平行，并保持探头姿态不变；比较两侧重复扫描可辅助发现对准与定位问题。','',
'---','**资料依据：**《大学物理实验（第三版）》实验 3.2（印刷页 257–264）；用户提供的原始实测表、评分标准/报告页照片及 ZKY-LS 与霍尔元件设备标签参数转录。']
md='\n'.join(parts)+'\n'
md=md.replace(chr(9),chr(92)+'t')
while chr(92)*2 in md: md=md.replace(chr(92)*2,chr(92))
mdpath=OUT/'实验报告-霍尔效应及螺线管磁场的测定-完整版.md'
mdpath.write_text(md,encoding='utf-8')

# Markdown -> formatted Word document (tables, images, headings and page breaks supported).
def shade(cell, fill):
    tcPr=cell._tc.get_or_add_tcPr(); shd=OxmlElement('w:shd'); shd.set(qn('w:fill'),fill); tcPr.append(shd)
def set_cell_text(cell,text,bold=False,color=None,size=8):
    cell.text=''; p=cell.paragraphs[0]; p.paragraph_format.space_after=Pt(0); p.paragraph_format.space_before=Pt(0)
    r=p.add_run(str(text));r.bold=bold;r.font.name='Arial';r._element.rPr.rFonts.set(qn('w:eastAsia'),'宋体');r.font.size=Pt(size)
    if color:r.font.color.rgb=RGBColor(*color)
    cell.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER

def add_inline(p,text):
    # Render common TeX notation as readable Unicode/plain text for Word.
    text=text.replace(chr(92)+'mu_0','μ₀').replace(chr(92)+'pi','π').replace(chr(92)+'times','×')
    text=text.replace(chr(92)+'theta','θ').replace(chr(92)+'propto','∝').replace(chr(92)+'cos','cos')
    text=text.replace(chr(92)+'sqrt{L^2+D_{eff}^2}','√(L²+D_eff²)').replace(chr(92)+'mathrm{mA}','mA')
    text=re.sub(re.escape(chr(92)+'sqrt{')+r'([^{}]+)'+re.escape('}'),r'√(\1)',text)
    text=re.sub(re.escape(chr(92)+'mathrm{')+r'([^{}]+)'+re.escape('}'),r'\1',text)
    text=re.sub(r'\$([^$]+)\$',r'\1',text)
    chunks=re.split(r'(\*\*.*?\*\*|`[^`]+`)',text)
    for ch in chunks:
        if not ch:continue
        isbold=ch.startswith('**') and ch.endswith('**')
        val=ch[2:-2] if isbold else (ch[1:-1] if ch.startswith('`') and ch.endswith('`') else ch)
        rr=p.add_run(val);rr.bold=isbold;rr.font.name='Arial';rr._element.rPr.rFonts.set(qn('w:eastAsia'),'宋体');rr.font.size=Pt(10)

doc=Document();sec=doc.sections[0];sec.top_margin=Cm(1.7);sec.bottom_margin=Cm(1.7);sec.left_margin=Cm(2.0);sec.right_margin=Cm(2.0)
normal=doc.styles['Normal'];normal.font.name='Arial';normal._element.rPr.rFonts.set(qn('w:eastAsia'),'宋体');normal.font.size=Pt(10);normal.paragraph_format.line_spacing=1.25;normal.paragraph_format.space_after=Pt(5)
for st,size,col in [('Title',20,'163B5C'),('Heading 1',16,'163B5C'),('Heading 2',12,'167D8D'),('Heading 3',11,'167D8D')]:
 s=doc.styles[st];s.font.name='Arial';s._element.rPr.rFonts.set(qn('w:eastAsia'),'黑体');s.font.size=Pt(size);s.font.bold=True;s.font.color.rgb=RGBColor.from_string(col)
# Header/footer
header=sec.header.paragraphs[0];header.alignment=WD_ALIGN_PARAGRAPH.RIGHT;rr=header.add_run('B317  霍尔效应及螺线管磁场的测定');rr.font.size=Pt(8);rr.font.color.rgb=RGBColor(110,125,138)
footer=sec.footer.paragraphs[0];footer.alignment=WD_ALIGN_PARAGRAPH.CENTER
r=footer.add_run('大学物理实验报告  ·  ');r.font.size=Pt(8)
fld=OxmlElement('w:fldSimple');fld.set(qn('w:instr'),'PAGE');footer._p.append(fld)
lines=md.splitlines();i=0;first_title=True
while i<len(lines):
    line=lines[i].rstrip()
    if not line.strip():i+=1;continue
    if line.strip()=='---':i+=1;continue
    if line.startswith('# '):
        p=doc.add_paragraph(style='Title' if first_title else 'Heading 1');p.alignment=WD_ALIGN_PARAGRAPH.CENTER if first_title else WD_ALIGN_PARAGRAPH.LEFT;add_inline(p,line[2:]);first_title=False;i+=1;continue
    if line.startswith('## '):
        p=doc.add_paragraph(style='Heading 1');add_inline(p,line[3:]);i+=1;continue
    if line.startswith('### '):
        p=doc.add_paragraph(style='Heading 2');add_inline(p,line[4:]);i+=1;continue
    if line.startswith('!['):
        m=re.match(r'!\[(.*?)\]\((.*?)\)',line)
        if m:
            img=OUT/m.group(2)
            if img.exists():
                p=doc.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER;p.add_run().add_picture(str(img),width=Inches(5.9))
                cap=doc.add_paragraph(m.group(1));cap.alignment=WD_ALIGN_PARAGRAPH.CENTER
        i+=1;continue
    if line.startswith('|'):
        tablelines=[]
        while i<len(lines) and lines[i].strip().startswith('|'):
            cells=[c.strip() for c in lines[i].strip().strip('|').split('|')]
            if not all(re.fullmatch(r':?-{2,}:?',c or '---') for c in cells):tablelines.append(cells)
            i+=1
        if not tablelines:continue
        cols=max(map(len,tablelines));t=doc.add_table(rows=0,cols=cols);t.alignment=WD_TABLE_ALIGNMENT.CENTER;t.style='Table Grid'
        for ri,row in enumerate(tablelines):
            cells=t.add_row().cells
            for ci in range(cols):
                txt=row[ci] if ci<len(row) else ''
                set_cell_text(cells[ci],txt,bold=(ri==0),color=(255,255,255) if ri==0 else None,size=7.5 if cols>=7 else 8)
                if ri==0:shade(cells[ci],'244F73')
                elif ri%2==0:shade(cells[ci],'F1F5F8')
        doc.add_paragraph().paragraph_format.space_after=Pt(1)
        continue
    if line.startswith('> '):
        p=doc.add_paragraph();p.paragraph_format.left_indent=Cm(.45);add_inline(p,line[2:]);
        for r in p.runs:r.font.color.rgb=RGBColor(75,91,103)
        i+=1;continue
    if re.match(r'^\d+\.\s+',line):
        p=doc.add_paragraph(style='List Number');add_inline(p,re.sub(r'^\d+\.\s+','',line));i+=1;continue
    if line.startswith('- '):
        p=doc.add_paragraph(style='List Bullet');add_inline(p,line[2:]);i+=1;continue
    p=doc.add_paragraph();add_inline(p,line);i+=1

docxpath=OUT/'实验报告-霍尔效应及螺线管磁场的测定-完整版.docx';doc.save(docxpath)
print('Created:',mdpath,docxpath)
print(f'B600={B600*1e3:.6f}mT B800={B800*1e3:.6f}mT KH={KH:.6f} RH={RH:.8f} n={nc:.6e}')
print(f'fit1 slope={s1:.9f} intercept_mV={b1:.9f} R2={r21:.9f}; fit2 slope={s2:.9f} intercept_mV={b2:.9f} R2={r22:.9f}')
