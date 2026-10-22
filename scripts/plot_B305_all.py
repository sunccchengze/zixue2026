#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
B305 金属电子逸出功与荷质比 - 全部作图脚本
按《大学物理实验（第三版）》实验3.6 及板书要求
生成：Fig1 lgIa-sqrtUa (表3), Fig2 Richardson (表4), Fig3 Ia-Is (表5), Fig4 Ua-Ic2
数据来自教师签字的表3-6-2、表3-6-5原始记录
"""
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 9

# ---------- 原始数据 ----------
Ua_vals = [16.0,25.0,36.0,49.0,64.0,81.0,100.0]
sqrtUa = [4.0,5.0,6.0,7.0,8.0,9.0,10.0]
If_vals = [0.600,0.625,0.650,0.675,0.700,0.725,0.750]
T_vals = [1.88,1.92,1.96,2.00,2.04,2.08,2.12]  # 10^3 K
Ia_data = {
 0.600: [8,8,9,9,9,8,10],
 0.625: [10,11,12,12,11,12,13],
 0.650: [15,15,16,16,16,16,17],
 0.675: [23,23,24,24,25,25,26],
 0.700: [33,34,36,36,37,37,39],
 0.725: [55,55,58,58,60,60,63],
 0.750: [82,91,94,95,97,98,102],
}
mag_data = {
 10: [(0.100,84),(0.340,83),(0.350,79),(0.360,67),(0.370,47),(0.380,27),(0.390,13),(0.400,9)],
 15: [(0.100,85),(0.410,85),(0.420,83),(0.430,79),(0.440,68),(0.450,40),(0.460,25),(0.470,10),(0.480,9)],
 20: [(0.100,86),(0.480,86),(0.490,83),(0.500,78),(0.510,67),(0.520,44),(0.530,25),(0.540,14),(0.550,9)],
 25: [(0.100,87),(0.540,87),(0.550,84),(0.560,79),(0.570,61),(0.580,49),(0.590,27),(0.600,15),(0.610,10),(0.620,8)],
 30: [(0.100,88),(0.590,87),(0.600,85),(0.610,82),(0.620,71),(0.630,57),(0.640,37),(0.650,22),(0.660,13),(0.670,10),(0.680,9)],
}

def linear_fit(x,y):
    n=len(x)
    sx=sum(x); sy=sum(y)
    sxx=sum(v*v for v in x); sxy=sum(x[i]*y[i] for i in range(n))
    denom=n*sxx - sx*sx
    b=(n*sxy - sx*sy)/denom if denom!=0 else 0
    a=(sy - b*sx)/n
    # R2
    y_mean=sy/n
    ss_tot=sum((yi-y_mean)**2 for yi in y)
    ss_res=sum((y[i]-(a+b*x[i]))**2 for i in range(n))
    r2=1-ss_res/ss_tot if ss_tot!=0 else 0
    return a,b,r2

# ---------- Fig1: lg Ia - sqrtUa ----------
print("Generating Fig1...")
colors = plt.cm.tab10.colors
plt.figure(figsize=(8,6))
lgI_zero = []
for idx, If in enumerate(If_vals):
    Ia = Ia_data[If]
    lgIa = [math.log10(v*1e-6) for v in Ia]
    a,b,r2 = linear_fit(sqrtUa, lgIa)
    lgI_zero.append(a)
    plt.scatter(sqrtUa, lgIa, color=colors[idx%10], s=35, zorder=5)
    x_fit = [4,10]
    y_fit = [a+b*x for x in x_fit]
    plt.plot(x_fit, y_fit, color=colors[idx%10], linestyle='--', linewidth=1.2, label=f'If={If:.3f}A T={T_vals[idx]:.2f}kK  lgI0={a:.3f}')
    # 标注截距点
    plt.scatter([0], [a], color=colors[idx%10], marker='|', s=120, linewidths=1.5)
plt.xlabel(r'$\sqrt{U_a}$ / V$^{1/2}$')
plt.ylabel(r'lg $I_a$ / lg(A)')
plt.title('Fig.1 lg $I_a$ - $\sqrt{U_a}$ (Table 3-6-3)\nSeven filament temps, intercept at $\sqrt{U_a}=0$ gives lg I (zero-field)')
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend(fontsize=6.5, ncol=1, loc='upper left', bbox_to_anchor=(1.02, 1.0), framealpha=0.95, borderpad=0.4)
plt.xlim(0,10.5)
plt.tight_layout(rect=[0, 0, 0.78, 1])
plt.savefig('大物实验预习/assets/B305_plot1_lgIa_sqrtUa.png', dpi=300, bbox_inches='tight')
plt.savefig('/tmp/B305_plot1_lgIa_sqrtUa.png', dpi=300, bbox_inches='tight')
plt.close()
print("Fig1 saved, intercepts:", ["{:.4f}".format(v) for v in lgI_zero])

# ---------- Fig2: Richardson ----------
print("Generating Fig2...")
T_K = [t*1e3 for t in T_vals]
invT = [1/t for t in T_K]
lg_I_T2 = [lgI_zero[i] -2*math.log10(T_K[i]) for i in range(len(T_K))]
a2,b2,r2 = linear_fit(invT, lg_I_T2)
k=1.381e-23; e=1.602e-19
phi = -b2*2.303*k/e
print(f"Richardson fit: lg(I/T2) = {a2:.4f} + {b2:.1f}*(1/T), R2={r2:.4f}, phi={phi:.3f}eV")
plt.figure(figsize=(7,5.2))
plt.scatter([x*1e4 for x in invT], lg_I_T2, color='red', s=60, zorder=5, edgecolors='k', linewidths=0.5)
x_fit = [min(invT), max(invT)]
y_fit = [a2 + b2*x for x in x_fit]
plt.plot([x*1e4 for x in x_fit], y_fit, color='blue', linestyle='--', linewidth=1.5, label=f'Fit: lg(I/T2) = {a2:.2f} {b2:+.0f}*(1/T)\nR2={r2:.4f}  Slope={b2:.0f}K')
for i in range(len(T_vals)):
    plt.annotate(f'{T_vals[i]:.2f}kK', (invT[i]*1e4, lg_I_T2[i]), xytext=(6,6), textcoords="offset points", fontsize=7,
                 bbox=dict(boxstyle="round,pad=0.2", fc="yellow", alpha=0.3))
plt.xlabel(r'1/T (10$^{-4}$ K$^{-1}$)')
plt.ylabel(r'lg(I/T$^2$) / lg(A/K$^2$)')
plt.title('Fig.2 Richardson plot lg(I/T2) vs 1/T (Table 3-6-4)\nSlope = -eφ/(2.303k) → φ = {:.2f} eV'.format(phi))
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend(fontsize=8, loc='upper right')
plt.tight_layout()
plt.savefig('大物实验预习/assets/B305_plot2_Richardson.png', dpi=300)
plt.savefig('/tmp/B305_plot2_Richardson.png', dpi=300)
plt.close()

# ---------- Fig3: Ia - Is ----------
print("Generating Fig3...")
plt.figure(figsize=(8,6))
for idx, Ua in enumerate(sorted(mag_data)):
    lst = sorted(mag_data[Ua])
    xs = [p[0] for p in lst]
    ys = [p[1] for p in lst]
    plt.plot(xs, ys, marker='o', markersize=5, markerfacecolor='white', markeredgecolor=colors[idx%10], markeredgewidth=1.2,
             color=colors[idx%10], linewidth=1.5, label=f'Ua={Ua}V')
    max_Ia = max(ys)
    target = max_Ia/4
    for i in range(len(lst)-1):
        Is1,Ia1 = lst[i]
        Is2,Ia2 = lst[i+1]
        if Ia1 >= target >= Ia2:
            Is_c = Is1 + (target - Ia1)*(Is2-Is1)/(Ia2-Ia1)
            plt.scatter([Is_c], [target], color=colors[idx%10], s=100, marker='x', linewidths=2, zorder=6)
            plt.annotate(f'Ic={Is_c:.3f}A', (Is_c, target), xytext=(7,7), textcoords="offset points", fontsize=7, color=colors[idx%10],
                         bbox=dict(boxstyle="round,pad=0.2", fc="white", alpha=0.8))
            break
plt.xlabel(r'Excitation current $I_s$ / A')
plt.ylabel(r'Anode current $I_a$ / $\mu$A')
plt.title('Fig.3 $I_a$ - $I_s$ curves for different $U_a$ (Table 3-6-5)\nCross = critical point Q ( $I_a$ = $I_{a0}$/4 )')
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend(fontsize=8, loc='upper right')
plt.tight_layout()
plt.savefig('大物实验预习/assets/B305_plot3_Ia_Is.png', dpi=300)
plt.savefig('/tmp/B305_plot3_Ia_Is.png', dpi=300)
plt.close()

# ---------- Fig4: Ua - Ic2 ----------
print("Generating Fig4...")
Ics = []
Uas = sorted(mag_data.keys())
for Ua in Uas:
    lst = mag_data[Ua]
    max_Ia = max(v for _,v in lst)
    target = max_Ia/4
    lst_sorted = sorted(lst)
    Ic = None
    for i in range(len(lst_sorted)-1):
        Is1,Ia1 = lst_sorted[i]
        Is2,Ia2 = lst_sorted[i+1]
        if Ia1 >= target >= Ia2:
            Ic = Is1 + (target - Ia1)*(Is2-Is1)/(Ia2-Ia1)
            break
    Ics.append(Ic)
Ic2 = [x**2 for x in Ics]
aM,bM,r2 = linear_fit(Ic2, Uas)
Kp=1.445e-2; a_val=4.0e-3
K=bM
e_m = 8*K/(a_val**2 * Kp**2)
e_m0 = 8*(sum(u*c2 for u,c2 in zip(Uas,Ic2))/sum(c2*c2 for c2 in Ic2))/(a_val**2*Kp**2)
print(f"Ua-Ic2 fit: Ua = {aM:.3f} + {bM:.2f}*Ic2, R2={r2:.5f}, e/m={e_m:.3e} (free), {e_m0:.3e} (through origin)")

plt.figure(figsize=(7,5.2))
plt.scatter(Ic2, Uas, color='darkgreen', s=80, zorder=5, edgecolors='k', linewidths=0.5)
x_fit = [min(Ic2)*0.9, max(Ic2)*1.05]
y_fit = [aM + bM*x for x in x_fit]
plt.plot(x_fit, y_fit, color='red', linestyle='--', linewidth=1.5, label=f'Fit: Ua = {aM:.2f} + {bM:.1f}·Ic²\nR²={r2:.4f}  K={bM:.1f} V/A²')
# 强制过原点
K0 = sum(u*c2 for u,c2 in zip(Uas,Ic2))/sum(c2*c2 for c2 in Ic2)
y0_fit = [K0*x for x in x_fit]
plt.plot(x_fit, y0_fit, color='orange', linestyle=':', linewidth=1.2, label=f'Through origin K0={K0:.1f}')
for i in range(len(Uas)):
    plt.annotate(f'{Uas[i]}V\nIc²={Ic2[i]:.3f}', (Ic2[i], Uas[i]), xytext=(8,5), textcoords="offset points", fontsize=7,
                 bbox=dict(boxstyle="round,pad=0.2", fc="lightyellow", alpha=0.7))
plt.xlabel(r'$I_c^2$ / A$^2$')
plt.ylabel(r'Anode voltage $U_a$ / V')
plt.title('Fig.4 $U_a$ - $I_c^2$ linear relation (Table 3-6-5)\n$K$ = slope → e/m = 8K/(a²K\'²) = {:.2e} C/kg'.format(e_m))
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend(fontsize=7.5, loc='upper left')
plt.tight_layout()
plt.savefig('大物实验预习/assets/B305_plot4_Ua_Ic2.png', dpi=300)
plt.savefig('/tmp/B305_plot4_Ua_Ic2.png', dpi=300)
plt.close()

print("All 4 plots generated successfully!")
print(f"Results: phi={phi:.3f} eV, e/m={e_m:.3e} C/kg (1.76e11 error {abs(e_m-1.76e11)/1.76e11*100:.2f}%)")
