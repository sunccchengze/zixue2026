#!/usr/bin/env python3
"""【仅光栅实验示例】光栅测波长复算脚本（分光计双游标法）。通用计算请用 lab_calc.py，勿把本脚本套到其它实验。

用法：python3 calc_grating.py
换数据时只改下面 DATA / STD / D_NM 三处（角度按 度、分 分开填）。
脚本会自动做：θ 复算、λ 计算、百分误差、双游标 180° 检查、两侧 2θ 检查、
绿光（重复测量）不确定度、氦光思考题。
"""
import math

# ---------------- 只改这里 ----------------
D_NM = 1e6 / 300          # 光栅常数 d，单位 nm。1/300 mm = 3333.33 nm
K = 1                     # 测的级次
# 每行顺序固定为：A游标+级, A游标-级, B游标+级, B游标-级；每项是 (度, 分)
DATA = {
    "蓝光":   [(59, 59), (44, 56), (240, 0),  (224, 59)],
    "绿光-1": [(61, 54), (42, 59), (241, 56), (223, 0)],
    "绿光-2": [(61, 55), (43, 0),  (241, 56), (223, 0)],
    "绿光-3": [(61, 55), (42, 59), (241, 56), (222, 59)],
    "黄1":    [(62, 26), (42, 27), (242, 26), (222, 29)],
    "黄2":    [(62, 29), (42, 25), (242, 30), (222, 26)],
}
GREEN_KEYS = ["绿光-1", "绿光-2", "绿光-3"]   # 重复测量的组（算平均与不确定度）
STD = {"蓝光": 435.83, "绿光": 546.07, "黄1": 576.96, "黄2": 579.07}  # nm
DELTA_INSTRUMENT_ARCMIN = 1.0   # 分光计分度（分），老师另有规定就改这里
# ------------------------------------------

def deg(dm):
    d, m = dm
    return d + m / 60.0

def fmt(x):
    d = int(x); mf = (x - d) * 60; m = int(mf); s = (mf - m) * 60
    if round(s) == 60:  # 进位保护，避免 10°01′60″
        s = 0; m += 1
    if m == 60:
        m = 0; d += 1
    return f"{d}°{m:02d}′{s:04.1f}″"

def theta_of(vals):
    ap, am, bp, bm = [deg(v) for v in vals]
    return 0.25 * (abs(ap - am) + abs(bp - bm)), ap, am, bp, bm

def lam_of(theta_deg):
    return D_NM * math.sin(math.radians(theta_deg)) / K

print(f"d = {D_NM:.2f} nm, k = {K}\n")
green_thetas = []
for name, vals in DATA.items():
    th, ap, am, bp, bm = theta_of(vals)
    lam = lam_of(th)
    # 一致性检查：B-A 应 ≈180°；两游标的 |+-- | 都应 ≈2θ
    chk1 = (bp - ap) % 360; chk2 = (bm - am) % 360
    warn = ""
    if abs(chk1 - 180) > 0.1 or abs(chk2 - 180) > 0.1:
        warn += "  ⚠ 180°检查异常!"
    if abs(abs(ap - am) - abs(bp - bm)) > 10 / 60:
        warn += "  ⚠ 两侧2θ不一致!"
    print(f"{name}: θ={fmt(th)}  λ={lam:.1f} nm  (B-A: {chk1:.2f}°/{chk2:.2f}°){warn}")
    if name in GREEN_KEYS:
        green_thetas.append(th)

# 汇总百分误差
print("\n百分误差:")
summary = {"蓝光": lam_of(theta_of(DATA['蓝光'])[0]),
           "黄1": lam_of(theta_of(DATA['黄1'])[0]),
           "黄2": lam_of(theta_of(DATA['黄2'])[0])}
if green_thetas:
    gmean = sum(green_thetas) / len(green_thetas)
    summary["绿光"] = lam_of(gmean)
    print(f"绿光平均 θ̄={fmt(gmean)}")
for name in ["蓝光", "绿光", "黄1", "黄2"]:
    if name in summary:
        e = abs(summary[name] - STD[name]) / STD[name] * 100
        print(f"  {name}: λ测={summary[name]:.1f}  λ标={STD[name]}  E={e:.2f}%")

# 绿光不确定度：E = cotθ·Δθ，Δθ = √(S²+Δ仪²)
if len(green_thetas) >= 2:
    n = len(green_thetas); mean = sum(green_thetas) / n
    s_mean = math.sqrt(sum((t - mean) ** 2 for t in green_thetas) / (n * (n - 1)))  # 度
    s_arcmin = s_mean * 60
    dtheta_arcmin = math.sqrt(s_arcmin ** 2 + DELTA_INSTRUMENT_ARCMIN ** 2)
    dtheta_rad = math.radians(dtheta_arcmin / 60)
    e_rel = (1 / math.tan(math.radians(mean))) * dtheta_rad
    lam_mean = lam_of(mean)
    print(f"\n绿光不确定度: S_θ̄={s_arcmin:.2f}′  Δθ={dtheta_arcmin:.2f}′={dtheta_rad:.2e} rad")
    print(f"  E_λ=cotθ·Δθ={e_rel*100:.2f}%  Δλ={e_rel*lam_mean:.1f} nm")
    print(f"  结果表达: λ绿 = ({lam_mean:.0f} ± {e_rel*lam_mean:.0f}) nm")

# 思考题示例：氦黄光 587.6 nm，5000 条/cm
print("\n思考题（氦黄光）: d=1/5000 cm=2000 nm")
for k in (1, 2):
    th = math.degrees(math.asin(k * 587.6 / 2000))
    print(f"  k={k}: sinθ={k*587.6/2000:.4f}  θ={th:.2f}° = {fmt(th)}")
