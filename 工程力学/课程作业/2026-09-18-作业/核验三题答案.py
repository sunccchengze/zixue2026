#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""9-18 作业三题答案 · 独立核验（只用 Python 标准库，随时随地可跑）

用法：  python3 核验三题答案.py          # 不需要任何第三方库

它做三件事：
  1. 把 2-1 / 3-1 / 3-2 的答案**从头重算一遍**（不引用任何"之前的结论"）；
  2. 与教材印刷答案逐条对照：
        教材：杨庆生等《工程力学（第三版）》部分习题参考答案
              第2章  2-1  1235N，5.53°
              第3章  3-1  -339.4N·m
              第3章  3-2  M_x=-Fcosθ(l+a)，M_y=-bFcosθ，M_z=-Fsinθ(l+a)
  3. 顺便打印"根号在哪"和"若换一种读图会得到什么"（反证用）。

任何一条对不上，脚本会直接报错退出（非零），不会"含糊过去"。
"""
import math

FAIL = []


def check(name, got, want, tol, unit=""):
    ok = abs(got - want) <= tol
    print(f"   {'✔' if ok else '✘'} {name}: 本题算得 {got:.4f}{unit}"
          f"　|　教材答案 {want:g}{unit}　|　差 {abs(got-want):.4f}")
    if not ok:
        FAIL.append(name)
    return got


print("=" * 72)
print("【2-1】三力合成（第 2 章 平面力系）")
print("-" * 72)
# 题图读法：P₁ 在轴线上方 40°；P₂ 在轴线下方 10°；35° 是从 P₂ 的作用线量起 → P₃ = −(10+35)° = −45°
P = [(+40.0, 500.0), (-10.0, 500.0), (-45.0, 500.0)]
for ang, f in P:
    print(f"   P@{ang:+6.1f}° → ({f*math.cos(math.radians(ang)):8.2f}, "
          f"{f*math.sin(math.radians(ang)):8.2f}) N")
X = sum(f * math.cos(math.radians(a)) for a, f in P)
Y = sum(f * math.sin(math.radians(a)) for a, f in P)
print(f"   ΣFx = {X:.2f} N　ΣFy = {Y:.2f} N")
print(f"   合力 R = √(ΣFx² + ΣFy²) = √({X:.2f}² + {Y:.2f}²)"
      f" = √{X*X + Y*Y:.1f} = {math.hypot(X, Y):.2f} N   ← 根号在这里")
check("2-1 合力 R", math.hypot(X, Y), 1235, 1.0, " N")
check("2-1 与轴线夹角 φ", math.degrees(math.atan2(-Y, X)), 5.53, 0.02, "°")

# 反证：若把 35° 当成"相对轴线"，会得到什么都对不上教材的数字
Xb = 500 * (math.cos(math.radians(40)) + math.cos(math.radians(-10)) + math.cos(math.radians(-35)))
Yb = 500 * (math.sin(math.radians(40)) + math.sin(math.radians(-10)) + math.sin(math.radians(-35)))
print(f"   （反证）若 P₃ 取 −35°：R = {math.hypot(Xb, Yb):.1f} N，"
      f"φ = {math.degrees(math.atan2(-Yb, Xb)):.2f}°　→ 与教材 1235 N / 5.53° 不符")
print("   结论：教材答案反证了'35° 应自 P₂ 量起、P₃ 与轴线成 45°'这一读图。")

print()
print("=" * 72)
print("【3-1】力对 z 轴之矩（第 3 章 空间力系）")
print("-" * 72)
F = 2000.0
legs = (30.0, 40.0, 50.0)
diag = math.sqrt(sum(t * t for t in legs))
print(f"   对角线长 √(30² + 40² + 50²) = √{sum(t*t for t in legs):.0f}"
      f" = 50√2 = {diag:.4f}   ← 根号在这里")
Fx, Fy, Fz = (t * F / diag for t in legs)
print(f"   F 的分解：Fx = 2000×30/√5000 = {Fx:.2f} N")
print(f"                      Fy = 2000×40/√5000 = {Fy:.2f} N")
print(f"                      Fz = 2000×50/√5000 = {Fz:.2f} N（与 z 轴平行，对 z 轴无矩）")
x, y = -0.150, 0.200          # 力作用点（m）：x 向 −150 mm、y 向 +200 mm
Mz = x * Fy - y * Fx
print(f"   Mz = x·Fy − y·Fx = ({x:.3f})×{Fy:.2f} − ({y:.3f})×{Fx:.2f}")
print(f"      = {x*Fy:.2f} − {y*Fx:.2f} = {Mz:.2f} N·m　（两项相等，因 150×40 = 200×30 = 6000）")
exact = -240 * math.sqrt(2)
print(f"   精确值：Mz = −240√2 = {exact:.4f} N·m   ← 根号也在这里")
check("3-1 Mz（数值）", Mz, -339.4, 0.2, " N·m")
check("3-1 Mz（精确式）", exact, -339.4, 0.2, " N·m")

print()
print("=" * 72)
print("【3-2】力对 x、y、z 三轴之矩（第 3 章）")
print("-" * 72)
print("   解析式：M_x = y·Fz − z·Fy，M_y = z·Fx − x·Fz，M_z = x·Fy − y·Fx")
print("   代入 D(−b, l+a, 0) 与 Fx = F sinθ、Fy = 0、Fz = −F cosθ：")
print("      M_x = (l+a)(−F cosθ) − 0     = −F(l + a)cosθ")
print("      M_y = 0 − (−b)(−F cosθ)       = −bF cosθ")
print("      M_z = 0 − (l+a)(F sinθ)       = −F(l + a)sinθ")
print("   —— 与教材答案形式逐字一致。")
# 数值抽检：任取一组数据，用向量叉乘 r×F 直接算，对比三个解析式
l, a, b, th, Fd = 1.0, 0.5, 0.8, math.radians(30), 1000.0
r = (-b, l + a, 0.0)
Fv = (Fd * math.sin(th), 0.0, -Fd * math.cos(th))
Mx_v = r[1] * Fv[2] - r[2] * Fv[1]
My_v = r[2] * Fv[0] - r[0] * Fv[2]
Mz_v = r[0] * Fv[1] - r[1] * Fv[0]
Mx_f = -Fd * (l + a) * math.cos(th)
My_f = -b * Fd * math.cos(th)
Mz_f = -Fd * (l + a) * math.sin(th)
print(f"   数值抽检（l=1, a=0.5, b=0.8, θ=30°, F=1000 N）：")
print(f"      向量叉乘 r×F : ({Mx_v:.2f}, {My_v:.2f}, {Mz_v:.2f})")
print(f"      三个解析式   : ({Mx_f:.2f}, {My_f:.2f}, {Mz_f:.2f})")
check("3-2 M_x 公式 vs 叉乘", Mx_f, Mx_v, 1e-6, " N·m")
check("3-2 M_y 公式 vs 叉乘", My_f, My_v, 1e-6, " N·m")
check("3-2 M_z 公式 vs 叉乘", Mz_f, Mz_v, 1e-6, " N·m")

print()
print("=" * 72)
if FAIL:
    raise SystemExit(f"✘ 核验未通过：{FAIL}")
print("✔ 全部核验通过：三题答案与教材印刷值逐条一致（容差见上）。")
print("=" * 72)
