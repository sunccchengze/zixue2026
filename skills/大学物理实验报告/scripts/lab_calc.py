#!/usr/bin/env python3
"""大学物理实验通用数据处理工具（任意实验可用）。

功能：重复测量统计、线性拟合、误差传递（数值微分）、百分误差、
结果格式化（末位对齐）、度分秒互换。
用法：直接运行看演示，或 import 后在自己的数据上调用各函数。
"""
import math

# ---------- 重复测量 ----------
def repeated_stats(values):
    """返回 dict：平均值、标准偏差 S、平均值标准偏差 S_mean。"""
    n = len(values)
    mean = sum(values) / n
    if n < 2:
        return {"n": n, "mean": mean, "S": 0.0, "S_mean": 0.0}
    s = math.sqrt(sum((v - mean) ** 2 for v in values) / (n - 1))
    return {"n": n, "mean": mean, "S": s, "S_mean": s / math.sqrt(n)}

def combine_uncertainty(s_mean, delta_b):
    """A 类（平均值标准偏差）与 B 类（仪器允差）方和根合成。"""
    return math.sqrt(s_mean ** 2 + delta_b ** 2)

def percent_error(measured, standard):
    return abs(measured - standard) / abs(standard) * 100

# ---------- 线性拟合 y = a + b x ----------
def linear_fit(x, y):
    """最小二乘。返回斜率 b、截距 a、相关系数 r、斜率/截距标准偏差。"""
    n = len(x)
    mx = sum(x) / n; my = sum(y) / n
    sxx = sum((v - mx) ** 2 for v in x)
    sxy = sum((x[i] - mx) * (y[i] - my) for i in range(n))
    syy = sum((v - my) ** 2 for v in y)
    b = sxy / sxx; a = my - b * mx
    r = sxy / math.sqrt(sxx * syy) if syy > 0 else float("nan")
    resid2 = sum((y[i] - a - b * x[i]) ** 2 for i in range(n))
    sy = math.sqrt(resid2 / (n - 2)) if n > 2 else 0.0
    sb = sy / math.sqrt(sxx)
    sa = sy * math.sqrt(1 / n + mx ** 2 / sxx)
    return {"slope": b, "intercept": a, "r": r, "s_slope": sb, "s_intercept": sa}

# ---------- 误差传递（数值微分，任意 f 都能用） ----------
def propagate(func, values, deltas):
    """func(*values) 的值与合成不确定度（各量独立，方和根）。
    values/deltas 为等长列表。返回 (y, Δy)。"""
    y0 = func(*values)
    tot = 0.0
    for i, (v, d) in enumerate(zip(values, deltas)):
        if d == 0:
            continue
        h = max(abs(v) * 1e-6, 1e-9)
        vp = list(values); vm = list(values)
        vp[i] += h; vm[i] -= h
        deriv = (func(*vp) - func(*vm)) / (2 * h)
        tot += (deriv * d) ** 2
    return y0, math.sqrt(tot)

# ---------- 结果格式化 ----------
def format_result(value, uncertainty, unit=""):
    """不确定度取 1 位有效数字，结果末位与之对齐。返回字符串。"""
    if uncertainty <= 0:
        return f"{value} {unit}".strip()
    exp = math.floor(math.log10(uncertainty))
    u = round(uncertainty, -exp)
    if u >= 10 * 10 ** exp:  # 进位修正，如 0.96 -> 1
        exp += 1; u = round(uncertainty, -exp)
    decimals = max(-exp, 0)
    rel = uncertainty / abs(value) * 100 if value else float("nan")
    return f"({value:.{decimals}f} ± {u:.{decimals}f}) {unit}，E≈{rel:.2g}%".strip()

# ---------- 度分秒 ----------
def dms_to_deg(d, m=0, s=0):
    return d + m / 60 + s / 3600

def deg_to_dms(x):
    d = int(x); mf = (x - d) * 60; m = int(mf); sec = round((mf - m) * 60, 1)
    if sec == 60: sec = 0; m += 1
    if m == 60: m = 0; d += 1
    return f"{d}°{m:02d}′{sec:04.1f}″"

if __name__ == "__main__":
    print("演示1 重复测量（如单摆周期、长度多次测量）：")
    data = [2.01, 2.03, 2.00, 2.02, 2.01]  # 换成你的原始读数
    st = repeated_stats(data)
    delta = combine_uncertainty(st["S_mean"], 0.01)  # B 类 0.01 换成仪器分度
    print(f"  x̄={st['mean']:.4f}  S={st['S']:.4f}  S_x̄={st['S_mean']:.4f}  合成Δ={delta:.4f}")
    print(f"  表达：{format_result(st['mean'], delta, 's')}")

    print("\n演示2 线性拟合（如 U-I 求电阻、标定曲线）：")
    xs = [1.0, 2.0, 3.0, 4.0, 5.0]; ys = [2.1, 3.9, 6.2, 7.8, 10.1]  # 换成你的 (x,y)
    fit = linear_fit(xs, ys)
    print(f"  斜率 b={fit['slope']:.3f}±{fit['s_slope']:.3f}  截距 a={fit['intercept']:.3f}  r={fit['r']:.4f}")

    print("\n演示3 误差传递（任意公式，如 ρ=m/(l·b·h)、g=4π²L/T²）：")
    y, dy = propagate(lambda L, T: 4 * math.pi ** 2 * L / T ** 2,
                      [1.000, 2.014], [0.001, 0.02])  # L±ΔL, T±ΔT 换成你的
    print(f"  g={y:.3f}  Δg={dy:.3f}  表达：{format_result(y, dy, 'm/s²')}")

    print("\n演示4 百分误差与度分秒：")
    print(f"  E={percent_error(548.2, 546.07):.2f}%  9.4653°={deg_to_dms(9.4653)}")
