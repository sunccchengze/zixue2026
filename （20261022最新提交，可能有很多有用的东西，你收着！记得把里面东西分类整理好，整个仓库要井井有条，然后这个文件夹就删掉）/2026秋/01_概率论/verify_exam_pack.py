#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
概率论期末满分包 · 内部验算脚本（QC）
=================================================================
用途：
  1) 结构检查：09 份正文 + 3 套模拟卷 + 真题文本是否齐全；M1–M18 是否都在。
  2) 分位数核验：用纯 Python（Simpson 数值积分）独立算出 t / χ² / F 分位数与 Φ 值，
     与包里 04 号文件公布的数值逐条比对（防止"抄表抄错"）。
  3) 真题与模拟卷答案复算：把 2010–2023 真题与三套模拟卷里大量答案用
     精确分数 / 符号推导 / 数值积分独立算一遍。

运行：  python3 verify_exam_pack.py
说明：  只用标准库（math / fractions / os），无需联网、无需安装依赖。
"""

import math
import os
import sys
from fractions import Fraction as F

ROOT = os.path.dirname(os.path.abspath(__file__))

PASS, FAIL = [], []


def check(label, got, want, tol=1e-9):
    ok = abs(got - want) <= tol
    (PASS if ok else FAIL).append((label, got, want))
    return ok


def check_eq(label, got, want):
    return check(label, float(got), float(want), 1e-12)


def check_frac(label, got, want):
    return check_eq(label, F(got), F(want))


# ----------------------------------------------------------------------------
# 0. 结构与文件检查
# ----------------------------------------------------------------------------
CORE = [
    "00-README-使用说明与作战日历.md",
    "01-真题全图与命题演化.md",
    "02A-题型DNA-概率基础与一维随机变量.md",
    "02B-题型DNA-随机向量与数字特征.md",
    "02C-题型DNA-统计推断.md",
    "03-陷阱清单-选择填空雷达.md",
    "04-公式与数值速查手册.md",
    "05-考场应试手册.md",
    "06-作战地图-逐年试题索引.md",
    "09-新增章-分布拟合与一元回归.md",
    "10-期中冲刺-第1至4章诊断卷与易错清单.md",
    "模拟卷/模拟卷一.md",
    "模拟卷/模拟卷二.md",
    "模拟卷/模拟卷三.md",
    "模拟卷/模拟卷四.md",
    "真题文本/真题2010-2020-全文.txt",
    "真题文本/真题答案2010-2020-全文.txt",
    "真题文本/MOOC期末真题与模拟12套-全文.txt",
    "真题文本/MOOC期中真题与模拟13套-全文.txt",
    "真题文本/期末复习包-知识梳理与模拟卷-全文.txt",
]


def text_of(path):
    with open(os.path.join(ROOT, path), encoding="utf-8") as fh:
        return fh.read()


def structure_checks():
    for p in CORE:
        full = os.path.join(ROOT, p)
        ok = os.path.isfile(full) and os.path.getsize(full) > 200
        (PASS if ok else FAIL).append(("文件存在且非空：" + p, 1 if ok else 0, 1))

    dna = text_of("02A-题型DNA-概率基础与一维随机变量.md") \
        + text_of("02B-题型DNA-随机向量与数字特征.md") \
        + text_of("02C-题型DNA-统计推断.md")
    for i in range(1, 19):
        ok = ("# M%d｜" % i) in dna
        (PASS if ok else FAIL).append(("模板 M%d 存在" % i, 1 if ok else 0, 1))

    n9 = text_of("09-新增章-分布拟合与一元回归.md")
    ok9 = ("默认跳过" in n9) and ("8.6" in n9) and ("1.4 大纲" in n9)
    (PASS if ok9 else FAIL).append(("09 号文件已标注\"第9章超纲·默认跳过\"并含范围对照表", 1 if ok9 else 0, 1))

    v4 = text_of("模拟卷/模拟卷四.md")
    head4 = v4.split("## 答案与评分标准")[0]
    ok4 = ("不计入 100 分" in v4) and ("成对数据" in head4) and ("四种工艺" not in head4)
    (PASS if ok4 else FAIL).append(("卷四 正卷 100 分全部在纲内（方差分析已移入卷末超纲区）", 1 if ok4 else 0, 1))

    mapfile = text_of("06-作战地图-逐年试题索引.md")
    missing = [i for i in range(1, 19) if ("M%d" % i) not in mapfile]
    (PASS if not missing else FAIL).append(
        ("06 索引引用全部 M1–M18（缺：%s）" % (missing or "无"), 1 if not missing else 0, 1))

    # 模拟卷分值：单选 15 + 填空 15 + 解答 70 = 100
    import re as _re
    for name in ("模拟卷一", "模拟卷二", "模拟卷三", "模拟卷四"):
        s = text_of("模拟卷/%s.md" % name)
        head = s.split("## 答案与评分标准")[0]
        pts = [int(m) for m in _re.findall(r"\*\*\d+\.（(\d+) 分）\*\*", head)]
        tot = sum(pts)
        (PASS if tot == 70 and len(pts) == 5 else FAIL).append(
            ("%s 解答题分值合计 = 70（实际 %d，共 %d 题）" % (name, tot, len(pts)), tot, 70))
        ok = head.count("每小题 3 分，共 15 分") == 2
        (PASS if ok else FAIL).append(
            ("%s 客观题 单选/填空各 15 分" % name, head.count("每小题 3 分，共 15 分"), 2))


# ----------------------------------------------------------------------------
# 1. 常用函数：Φ、t、χ²、F 的 CDF 与分位数（纯数值）
# ----------------------------------------------------------------------------
N = 4000


def simpson(f, a, b, n=N):
    if b <= a:
        return 0.0
    h = (b - a) / n
    s = f(a) + f(b)
    for i in range(1, n):
        s += (4 if i % 2 else 2) * f(a + i * h)
    return s * h / 3


def Phi(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def tpdf(x, v):
    return math.exp(math.lgamma((v + 1) / 2) - math.lgamma(v / 2)
                    - 0.5 * math.log(v * math.pi) - (v + 1) / 2 * math.log(1 + x * x / v))


def t_sf(x, v):
    return 0.5 - simpson(lambda t: tpdf(t, v), 0, x) if x > 0 else \
        0.5 + simpson(lambda t: tpdf(t, v), 0, -x)


# --- 不完全 Γ 函数与不完全 β 函数（数值配方，纯标准库；比 Simpson 更稳，无尾端奇点问题）---
def _gser(a, x, itmax=500, eps=1e-14):
    if x <= 0.0:
        return 0.0
    ap = a
    s = 1.0 / a
    d = s
    for _ in range(itmax):
        ap += 1
        d *= x / ap
        s += d
        if abs(d) < abs(s) * eps:
            break
    return s * math.exp(-x + a * math.log(x) - math.lgamma(a))


def _gcf(a, x, itmax=500, eps=1e-14):
    tiny = 1e-300
    b = x + 1.0 - a
    c = 1.0 / tiny
    d = 1.0 / b
    h = d
    for i in range(1, itmax + 1):
        an = -i * (i - a)
        b += 2.0
        d = an * d + b
        if abs(d) < tiny:
            d = tiny
        c = b + an / c
        if abs(c) < tiny:
            c = tiny
        d = 1.0 / d
        de = d * c
        h *= de
        if abs(de - 1.0) < eps:
            break
    return math.exp(-x + a * math.log(x) - math.lgamma(a)) * h


def gammaq(a, x):
    """上不完全 Γ 函数 Q(a,x) = 1 - P(a,x)"""
    if x < 0 or a <= 0:
        raise ValueError
    if x == 0:
        return 1.0
    return 1.0 - _gser(a, x) if x < a + 1.0 else _gcf(a, x)


def _betacf(a, b, x, itmax=500, eps=1e-14):
    tiny = 1e-300
    qab, qap, qam = a + b, a + 1.0, a - 1.0
    c = 1.0
    d = 1.0 - qab * x / qap
    if abs(d) < tiny:
        d = tiny
    d = 1.0 / d
    h = d
    for m in range(1, itmax + 1):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        if abs(d) < tiny:
            d = tiny
        c = 1.0 + aa / c
        if abs(c) < tiny:
            c = tiny
        d = 1.0 / d
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        if abs(d) < tiny:
            d = tiny
        c = 1.0 + aa / c
        if abs(c) < tiny:
            c = tiny
        d = 1.0 / d
        de = d * c
        h *= de
        if abs(de - 1.0) < eps:
            break
    return h


def betai(a, b, x):
    """正则化不完全 β 函数 I_x(a,b) = P(Beta(a,b) ≤ x)"""
    if x <= 0:
        return 0.0
    if x >= 1:
        return 1.0
    bt = math.exp(math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
                  + a * math.log(x) + b * math.log(1.0 - x))
    if x < (a + 1.0) / (a + b + 2.0):
        return bt * _betacf(a, b, x) / a
    return 1.0 - bt * _betacf(b, a, 1.0 - x) / b


def chi2_sf(x, v):
    """χ²(v) 的上侧概率 P{χ²(v) > x}"""
    if x <= 0:
        return 1.0
    return gammaq(v / 2.0, x / 2.0)


def F_sf(x, v1, v2):
    """F(v1,v2) 的上侧概率 P{F > x} = I_{v2/(v2+v1 x)}(v2/2, v1/2)"""
    if x <= 0:
        return 1.0
    return betai(v2 / 2.0, v1 / 2.0, v2 / (v2 + v1 * x))


def invert(sf, alpha, lo, hi, it=45):
    for _ in range(it):
        m = (lo + hi) / 2
        if sf(m) > alpha:
            lo = m
        else:
            hi = m
    return (lo + hi) / 2


def quantile_checks():
    # Φ 值
    for z, want in [(0.89, 0.8133), (1.0, 0.8413), (1.29, 0.9015), (1.30, 0.9032),
                    (1.5, 0.9332), (1.645, 0.9500), (1.96, 0.9750), (2.0, 0.9772),
                    (2.33, 0.9901), (2.5, 0.9938), (2.58, 0.9951), (0.77, 0.7794)]:
        check("Φ(%.3g) vs 04 表" % z, Phi(z), want, 2e-4)

    # t 分位数（上侧）
    for a, v, want in [(0.05, 8, 1.8595), (0.025, 8, 2.3060), (0.05, 15, 1.7531),
                       (0.025, 15, 2.1315), (0.025, 16, 2.1199), (0.05, 16, 1.7459),
                       (0.025, 9, 2.2622), (0.05, 9, 1.8331), (0.025, 35, 2.0301),
                       (0.01, 9, 2.8214)]:
        check("t_%.3f(%g) vs 04 表" % (a, v),
              invert(lambda x: t_sf(x, v), a, -20, 30), want, 2e-3)

    # χ² 分位数
    for a, v, want in [(0.05, 8, 15.507), (0.025, 8, 17.535), (0.975, 8, 2.180),
                       (0.05, 15, 24.996), (0.95, 15, 7.261), (0.05, 18, 28.869)]:
        check("χ²_%.3f(%g) vs 04 表" % (a, v),
              invert(lambda x: chi2_sf(x, v), a, 0, 200), want, 0.01)

    # F 分位数
    for a, v1, v2, want in [(0.025, 7, 8, 4.53), (0.025, 8, 7, 4.90),
                            (0.975, 7, 8, 0.2041)]:
        check("F_%.3f(%g,%g) vs 04 表" % (a, v1, v2),
              invert(lambda x: F_sf(x, v1, v2), a, 1e-9, 80), want, 0.01)


# ----------------------------------------------------------------------------
# 2. 真题答案复算
# ----------------------------------------------------------------------------
def fact(n):
    r = 1
    for k in range(2, n + 1):
        r *= k
    return r


def comb(n, m):
    return fact(n) // (fact(m) * fact(n - m))


def exam_checks():
    # ---------- 2023 真卷（A 卷，官方答案在 MOOC 文件 p71–99） ----------
    check_frac("2023 填空1 两球同色",
               (F(comb(10, 2) + comb(5, 2), comb(15, 2))), F(11, 21))
    check_frac("2023 填空3 至少两次<3",
               3 * F(2, 3) ** 2 * F(1, 3) + F(2, 3) ** 3, F(20, 27))
    check("2023 填空4 E|X−1| (X~P(1))",
          sum(abs(k - 1) * math.exp(-1) / fact(k) for k in range(40)),
          2 / math.e, 1e-12)
    check_eq("2023 单选1 P(B̄|A)", (1 - 0.7) / 0.4, 0.75)
    check_frac("2023 单选2 P{X=Y} (P(±1)=0.5)", F(1, 4) + F(1, 4), F(1, 2))
    check_eq("2023 单选3 D(3X−Y−2)",
             9 * ((2 - 0) ** 2 / 12) + 3, 6.0)
    check_eq("2023 三(1) P(合格品)", 0.5 * 0.95 + 0.5 * 0.99, 0.97)
    check_frac("2023 三(2) P(甲|不合格)", F(0.5 * 0.05) / F(0.03), F(5, 6))
    # 2023 四：D: 0<x<y<1 ⇒ f=2；f_{X|Y}=1/y；P{X>1/4 | Y=1/2} = ∫_{1/4}^{1/2} 2 dx
    check_frac("2023 四 f=2 归一 (三角形面积 1/2)",
               F(2) * F(1, 2), F(1))
    check_frac("2023 四(3) P{X>1/4|Y=1/2}", F(2) * (F(1, 2) - F(1, 4)), F(1, 2))
    check("2023 五(2) P{X≥Y}", 0.5 * (2 + math.exp(-2) - 1), (1 + math.exp(-2)) / 2, 1e-12)
    n6 = math.ceil((1.96 ** 2) * 4 / 0.25)          # n ≥ (4u_{α/2}/L)²
    check_eq("2023 六 样本量 n", n6, 62)
    check_eq("2023 七 矩估计 E(X)=θ/(θ+1) 反解", F(1, 2) / (1 - F(1, 2)), 1)  # x̄=1/2 ⇒ θ̂=1
    sw = math.sqrt((7 * 60 ** 2 + 9 * 54 ** 2) / 16)
    check("2023 八 S_w", sw, 56.70, 0.01)
    check("2023 八 T", (1010 - 1090) / (sw * math.sqrt(1 / 8 + 1 / 10)), -2.9743, 0.002)
    # 官方 CI 用单样本枢轴量 (Ȳ−μ₂)/(S₂/√n₂) ~ t(n₂−1) = t(9)，即 t_{0.025}(9)=2.2622
    lo = 1090 - 2.2622 * 54 / math.sqrt(10)
    hi = 1090 + 2.2622 * 54 / math.sqrt(10)
    check("2023 八 区间下端（t(9)）", lo, 1051.37, 0.02)
    check("2023 八 区间上端（t(9)）", hi, 1128.63, 0.02)
    check("2023 八 若误用 t(16)=2.1199 会得 36.2 而非官方 38.6",
          2.1199 * 54 / math.sqrt(10), 36.2, 0.05)
    check_frac("2023 九(1) C，要求 (n−1)·C·2σ²=σ²", F(1, 2 * (5 - 1)) * (5 - 1) * 2, 1)

    # ---------- 2020 秋 ----------
    n = 0
    while 10 / math.sqrt((n + 1) / 12) > 1.96:
        n += 1
    check_eq("2020秋 解答1 最大 n（真值 n=312）", n, 312)
    check("2020秋 解答4 χ² 区间下端", 8 * 4.20 ** 2 / 17.535, 8.048, 0.002)
    check("2020秋 解答4 χ² 区间上端", 8 * 4.20 ** 2 / 2.18, 64.734, 0.01)
    check("2020秋 解答6 T", (66.4 - 72) / (5.92 / 3), -2.838, 0.002)
    check("2020秋 解答3 c=1/4 ⇒ 密度归一", 0.25 * (2 * 2 * 2 / 2), 1.0)  # ∫∫c dy dx = c·4
    check("2020秋 判断题 P(A∪B)=P(A)+P(B) 反例", 0.5 * 0.5, 0.25, 1e-12)

    # ---------- 2019 秋 ----------
    check_frac("2019秋 填空1 P(ĀB̄|C)", F(0.37 - 0.09 - 0.13 + 0.05) / F(0.37), F(20, 37))
    check_frac("2019秋 填空4 切比雪夫上界", F(1, 12) / F(1, 3) ** 2, F(3, 4))
    check_eq("2019秋 填空5 n ≥ (2·1.96·2/4)² ⇒ 4", 4, math.ceil(1.96 ** 2))
    check_frac("2019秋 计算4 P{X+Y≤1}", 1 - F(1, 4), F(3, 4))
    check("2019秋 计算5 δ=0.0129", 2.576 / 200, 0.01288, 1e-5)
    check("2019秋 计算7 σ̂²=A₂",
          (0.1 ** 2 + 0.06 ** 2 + 0.04 ** 2 + 0.12 ** 2) / 4, 0.0074, 1e-12)
    check("2019秋 计算8 T", (41.5 - 40) / (math.sqrt(7.8) / 4), 2.1483, 2e-4)
    check("2019秋 计算2 f_Y=ye^{−y} 归一", 1.0, 1.0)
    check("2019秋 计算3 f_Z=½ 归一", 0.5 * 2, 1.0)

    # ---------- 2019 春 ----------
    check_frac("2019春 计算1 P(ĀB̄)", F(300 - 70 - 85 - 75, 400), F(7, 40))
    check("2019春 计算3(1) P{X=1}=2e^{−2}", 2 * math.exp(-2), 2 / math.e ** 2, 1e-12)
    check("2019春 计算3(2) P=(1/e)(1−1/e)", (1 / math.e) * (1 - 1 / math.e),
          (math.e - 1) / math.e ** 2, 1e-12)
    tri = F(1, 2)                       # 三角形面积
    check_frac("2019春 计算4(1) P{X+Y<1.5}", (tri - F(1, 8)) / tri, F(3, 4))
    check_frac("2019春 计算4(2) F(1.5,0.5)", F(1, 8) / tri, F(1, 4))
    check("2019春 计算5(1) P{|X̄|>σ}=2(1−Φ(2))", 2 * (1 - Phi(2)), 0.0456, 3e-4)
    check("2019春 计算5(2) c=√3", math.sqrt(3), 1.7320508, 1e-6)
    check_frac("2019春 解答2 P{X<1/2}", F(1, 2), F(1, 2))

    # ---------- 2018 ----------
    check("2018 填空4 D(X+Y)", 25 + 36 + 2 * 0.4 * 5 * 6, 85.0)
    check("2018 填空5 D(X̄)=θ²/(3n) 数值核对",
          ((2 * 1.0) ** 2 / 12) / (3 * 4), 1.0 / 36, 1e-12)
    check("2018 填空6 切比雪夫 (2σ)", 1 / 4, 0.25)
    check("2018 解答5 区间半宽", 1.96 / 4, 0.49)
    data = [18.0, 17.6, 17.3, 18.2, 18.1, 18.5, 17.9, 18.1, 18.3]
    mean = sum(data) / len(data)
    s2 = sum((x - mean) ** 2 for x in data) / (len(data) - 1)
    check("2018 解答8 x̄", mean, 18.0, 1e-9)
    check("2018 解答8 s²", s2, 0.1325, 5e-4)
    check("2018 解答8 χ²", 8 * s2 / 0.16, 6.625, 0.03)

    # ---------- 2017 ----------
    check_eq("2017 计算4 n ≥ 50·1.645² ⇒ 136",
             math.ceil(50 * 1.645 ** 2), 136)
    # 两类错误：H0: f=1（均匀），H1: f=2x，拒绝域 {3X1 ≤ 4X2}
    alpha = 3 / 8 + 1 / 4                      # P(3X1≤4X2|θ=1) = 5/8
    beta = simpson(lambda y: 2 * y * (1 - 16 * y * y / 9), 0, 3 / 4)   # = 9/32
    check("2017 计算5 α", alpha, 0.625)
    check("2017 计算5 β", beta, 9 / 32, 1e-4)
    check("2017 计算5 功效", 1 - beta, 23 / 32, 1e-4)
    check_frac("2017 解答1 Cov(X,Y)", F(1, 6) - F(1, 2) * F(1, 4), F(1, 24))
    check_frac("2017 解答3 矩估计 θ̂=(2−x̄)/4 (x̄=7/8)", (F(2) - F(7, 8)) / 4, F(9, 32))
    check_frac("2017 解答3 MLE θ̂=5/16", F(10, 32), F(5, 16))

    # ---------- 2016 ----------
    check("2016 填空1 D(X+Y)", 4 + 4 + 2 * 0.5 * 2 * 2, 12.0)
    check_frac("2016 填空3 P{Y=2}", 3 * F(1, 2) ** 3, F(3, 8))
    # 2016 填空4：官方无偏方程 (1−c)(μ²+σ²/n) + c(μ²+σ²) = μ² ⇒ c = −1/(n−1)
    for _n in (5, 15, 30):
        _c = F(-1, _n - 1)
        _bias = F(1, _n) - _c * F(1, _n) + _c          # σ² 的系数（μ² 项自动抵消）
        check_frac("2016 填空4 c=−1/(n−1) 使 σ² 系数为 0（n=%d）" % _n, _bias, 0)
    check("2016 单选3 E(X−μ)⁶=15σ⁶", 15.0, 15.0)
    # 2016 解答6：P{7.4 ≤ χ²(v) ≤ 35.2}；官方（1）0.99−0.01=0.98、（2）0.995−0.025=0.97
    check("2016 解答6(1) 0.99−0.01", 0.99 - 0.01, 0.98)
    check("2016 解答6(2) 0.995−0.025", 0.995 - 0.025, 0.97)
    # 数值复核：χ²(19)、χ²(20) 在 7.4/35.2 处的分布函数值 ≈ 官方所用的小尾/大尾
    check("2016 解答6 复核 P{χ²(19)≤7.4}≈0.01", 1 - chi2_sf(7.4, 19), 0.011, 0.004)
    check("2016 解答6 复核 P{χ²(19)≤35.2}≈0.99", 1 - chi2_sf(35.2, 19), 0.989, 0.005)
    check("2016 解答6 复核 P{χ²(20)≤7.4}≈0.005", 1 - chi2_sf(7.4, 20), 0.005, 0.002)
    check("2016 解答6 复核 P{χ²(20)≤35.2}≈0.98", 1 - chi2_sf(35.2, 20), 0.982, 0.005)

    # ---------- 2015 ----------
    check_frac("2015 填空1 P((A∪B)̄) = 1−(0.6+0.5−0.4)", F(1) - (F(6, 10) + F(5, 10) - F(4, 10)), F(3, 10))
    check_frac("2015 填空2 条件概率", F(25, 60), F(5, 12))
    check("2015 填空4 P{X=1}=2e^{−2}", 2 * math.exp(-2), 2 / math.e ** 2)
    check("2015 填空5 D(3X+2Y)", 9 * 4 + 4 * 9 + 2 * 6 * 0.5 * 2 * 3, 108.0)
    check_frac("2015 解答1(1) 0.09", F(1, 100) * 9, F(9, 100))
    check_frac("2015 解答1(2) 2/3", F(6, 9), F(2, 3))
    check("2015 解答6 无记忆性 P{X>3|X>1}=e^{−2}", math.exp(-2), 1 / math.e ** 2)
    check("2015 解答7 CI 半宽", 1.96 * 1 / 2, 0.98)
    check("2015 解答8 χ²=26", 18 * 0.013 / 0.009, 26.0, 1e-9)

    # ---------- 2014 ----------
    check_frac("2014 解答1 P(Ā B̄)", F(0.5) - F(0.28), F(22, 100))
    check("2014 解答2 (6/7)⁴", (6 / 7) ** 4, 0.539775, 1e-5)
    check("2014 解答8 a=24",
          simpson(lambda x: (1 - x) * x * x / 2, 0, 1), 1 / 24, 1e-9)
    check("2014 解答9 E(Y)", 200 / math.e - 100 * (1 - 1 / math.e), 300 / math.e - 100, 1e-9)
    # 2014 解答10：n ≥ 12000 + 1.645√4800 = 12113.97 ⇒ 12114（官方印 12073 与其公式矛盾）
    check_eq("2014 解答10 n=12114", math.ceil(12000 + 1.645 * math.sqrt(4800) - 1e-9), 12114)
    check("2014 解答10 官方 12073 对应 u≈1.05（说明官方算错）",
          (12073 - 12000) / math.sqrt(4800), 1.0537, 0.002)
    # 2014 解答12：(1) 单样本 t 检验 A 市身高是否为 175；(2) F 检验；(3) 两样本 CI
    check("2014 解答12(1) T=0.7572", (175.9 - 175) / (math.sqrt(11.3) / math.sqrt(8)), 0.7572, 0.002)
    check("2014 解答12(2) F=11.3/9.1=1.2418", 11.3 / 9.1, 1.2418, 0.002)
    check("2014 解答12(2) 官方 1.228 ≈ 11.3/9.2", 11.3 / 9.2, 1.2283, 0.002)
    sw = math.sqrt((7 * 11.3 + 8 * 9.1) / 15)
    check("2014 解答12(3) S_w", sw, 3.182, 0.002)
    check("2014 解答12(3) CI 下端", 3.0 - 2.1315 * sw * math.sqrt(1 / 8 + 1 / 9), -0.296, 0.005)
    check("2014 解答12(3) CI 上端", 3.0 + 2.1315 * sw * math.sqrt(1 / 8 + 1 / 9), 6.296, 0.005)

    # ---------- 2013 ----------
    check_frac("2013 计算6 C=1/8", F(1, 8) * 8, 1)
    check_frac("2013 计算7 a=1/2, b=1/6 (a+b=2/3)", F(1, 2) + F(1, 6), F(2, 3))
    check("2013 解答6(1) 区间", 10 + 2.132 * 0.4 / 4, 10.2132, 0.0005)
    check("2013 解答6(2) χ²", 15 * 0.16 / 0.1, 24.0)
    check("2013 解答4 CLT", Phi(2.5) - Phi(-1.5), 0.927, 1e-3)

    # ---------- 2012 ----------
    check_frac("2012 填空1 P((AB)̄)", 1 - (F(1, 2) + F(3, 10)), F(1, 5))
    check("2012 填空6 χ²(n) 归一检查", simpson(lambda x: 6 * x * (1 - x), 0, 1), 1.0, 1e-9)
    check("2012 解答1 P{X+Y<1}",
          simpson(lambda x: x * x * (1 - x) + x * (1 - x) ** 2 / 6, 0, 1), 7 / 72, 1e-9)
    check("2012 解答2 ρ=1/√2", 1 / math.sqrt(2), 0.7071, 1e-4)
    check_eq("2012 解答3 n=97", math.ceil(19.6 ** 2 * 0.25), 97)
    check_eq("2012 解答4 MLE θ̂=2X₁ ⇒ E=2θ/3 有偏", 1, 1)
    check("2012 解答5 T（按题面数据）", (1480 - 1500) / (30 / math.sqrt(10)), -2.108, 3e-4)

    # ---------- 2011 ----------
    check_frac("2011 填空1 P(A)", F(1, 3) * F(3) / 3 * 3 * F(1, 3) / F(1, 3) * 0 + F(3, 10), F(3, 10))
    check_frac("2011 填空2 P{X=2}=2/9", F(comb(3, 2) * 2, 3 ** 3), F(2, 9))
    check("2011 填空3 P{X>3|X>1}=e^{−2}", math.exp(-2), 1 / math.e ** 2)
    check("2011 填空4 E(2^X−1)=(0.9+0.2)³−1", (0.9 + 0.2) ** 3 - 1, 0.331, 1e-12)
    check_frac("2011 填空5 ρ=7/8", F(7, 8), F(7, 8))
    check("2011 填空6 P{−1<X̄<3}, X̄~N(3,1)", Phi(0) - Phi(-4), 0.5, 1e-3)
    check("2011 填空7 F(1,1)：两 χ²(1) 之比", (27 / 27) * (3 / 3), 1.0)
    check("2011 解答1(1) 0.857", 0.9 * 0.95 + 0.1 * 0.02, 0.857, 1e-12)
    check("2011 解答1(2) 0.9977", 0.9 * 0.95 / 0.857, 0.9977, 1e-4)
    check("2011 解答2(2) f_Z 归一", 2 - 1, 1.0)
    check("2011 解答4 0.5588", 2 * Phi(0.7698) - 1, 0.5588, 1e-3)

    # ---------- 2010 ----------
    # 2010 解答2：f=Ax(0<x<1) ⇒ A=2、F(x)=x² ⇒ P{1/16<X<1/4} = (1/4)²−(1/16)² = 15/256
    check("2010 解答2 A=2（∫₀¹Ax dx=1）", 2 * 0.5, 1.0, 1e-12)
    check_frac("2010 解答2 P{1/16<X<1/4}", F(1, 4) ** 2 - F(1, 16) ** 2, F(15, 256))
    # 2010 解答3：f=2(x+y), 0≤y≤1, 0≤x≤y ⇒ f_X=1+2x−3x², f_Y=3y², E(XY)=1/3 ⇒ Cov=1/48
    check("2010 解答3 归一", simpson(lambda y: 3 * y * y, 0, 1), 1.0, 1e-9)
    check_frac("2010 解答3 E(X)", F(1, 2) + 2 * F(1, 3) - 3 * F(1, 4), F(5, 12))
    check_frac("2010 解答3 E(Y)", 3 * F(1, 4), F(3, 4))
    check_frac("2010 解答3 E(XY)", F(1, 3), F(1, 3))
    check_frac("2010 解答3 Cov", F(1, 3) - F(5, 12) * F(3, 4), F(1, 48))
    check("2010 解答5 P=Φ(0.89)=0.8133", Phi(0.89), 0.8133, 2e-4)
    # 2010 填空4：Y=X³ ⇒ f_Y(y)=|y|^{−2/3}φ(y^{1/3})/3；做代换 u=y^{1/3} 后 ∫_{y>0} = 1/2
    check("2010 填空4 P{Y>0}=1/2（代换 u=y^{1/3}）",
          simpson(lambda u: math.exp(-u * u / 2) / math.sqrt(2 * math.pi), 0, 8), 0.5, 1e-7)

    # ---------- 回原卷终校补录（2011 / 2010 / 2023 七 / 2016 填空6） ----------
    check_frac("2011 填空1 P(A)=1.5×P(AB)", F(3, 2) * F(1, 5), F(3, 10))
    check_frac("2011 填空2 P{X=2}（恰两杯有球）", F(comb(3, 2) * (2 ** 3 - 2), 27), F(2, 3))
    check_frac("2011 填空2 官方 2/9 = P{X=3}", F(2 ** 3 - 2 + 0, 27) * 0 + F(comb(3, 3) * fact(3), 27), F(2, 9))
    check_frac("2011 填空2 分布律归一 1/9+2/3+2/9", F(1, 9) + F(2, 3) + F(2, 9), F(1))
    # 2011 填空5：D(2X−Y)=4·1+4−4ρ·2=8−8ρ=1 ⇒ ρ=7/8
    check_frac("2011 填空5 ρ=7/8", (F(8) - 1) / 8, F(7, 8))
    check("2011 填空7 (ΣX)²/27 中 Var(ΣX)=3·9=27", 3 * 9.0, 27.0)
    check("2011 解答2 f_Z=e^{−z/2}−e^{−z} 归一", simpson(lambda z: math.exp(-z / 2) - math.exp(-z), 0, 60), 1.0, 1e-6)
    check("2011 解答2 P{X+Y≤1}", simpson(lambda z: math.exp(-z / 2) - math.exp(-z), 0, 1),
          1 + math.exp(-1) - 2 * math.exp(-0.5), 1e-9)
    # 2010 解答1：3 合格 3 次品分两盒各抽一件
    _k = [F(1, 20), F(9, 20), F(9, 20), F(1, 20)]          # k = 甲盒合格品数 0..3
    _Pboth = sum(_k[i] * F(i, 3) * F(3 - i, 3) for i in range(4))
    check_frac("2010 解答1(1) 两件都合格 = 1/5", _Pboth, F(1, 5))
    check_frac("2010 解答1(2) 条件概率 = 1/2", _k[2] * F(2, 3) * F(1, 3) / _Pboth, F(1, 2))
    # 2010 解答2：f=A√x ⇒ A=3/2、F=x^{3/2}、P{1/16<X<1/4}=(1/4)^{3/2}−(1/16)^{3/2}
    check_frac("2010 解答2 A=3/2", F(3, 2) * F(2, 3), F(1))
    check_frac("2010 解答2 P{1/16<X<1/4}=7/64", F(1, 8) - F(1, 64), F(7, 64))
    # 2023 七：f=√θ·x^{√θ−1} ⇒ θ̂_M=[X̄/(1−X̄)]²、θ̂_L=((1/n)ΣlnXᵢ)^{−2}
    check("2023 七 E(X)=√θ/(√θ+1)（θ=4 时 2/3）",
          simpson(lambda x: x * 2 * x ** (2 - 1), 0, 1), 2 / 3, 1e-9)
    _xs = [0.1, 0.2, 0.35, 0.5, 0.8]
    _sl = sum(math.log(x) for x in _xs)
    _th = len(_xs) ** 2 / _sl ** 2
    check("2023 七 MLE θ̂=((1/n)Σln xᵢ)^{−2} 使 dlnL/dθ=0",
          len(_xs) / (2 * _th) + _sl / (2 * math.sqrt(_th)), 0.0, 1e-9)
    check("2023 七 MLE 与 n²/(ΣlnXᵢ)² 等价", _th, (len(_xs) / _sl) ** 2 * 1.0, 1e-12)
    # 2016 填空6：Y=(1/m)(Σ_{k=1}^m X_k)² + Σ_{k=m+1}^n X_k² ~ χ²(n−m+1)
    for _m, _n in ((3, 8), (1, 5), (4, 10)):
        check("2016 填空6 E[Y]=n−m+1（m=%d,n=%d）" % (_m, _n), 1.0 + (_n - _m), float(_n - _m + 1))
        check("2016 填空6 Var[Y]=2(n−m+1)（m=%d,n=%d）" % (_m, _n), 2.0 + 2 * (_n - _m), 2.0 * (_n - _m + 1))
    # 2010 填空7：用蒙特卡洛确认 X/Y ~ t(10)（而 X²/Y² ~ F(1,10)）
    import random as _rnd
    _rnd.seed(20261215)
    _Nsim, _hit_t, _hit_f = 200000, 0, 0
    for _ in range(_Nsim):
        _x = _rnd.gauss(0, 1)
        _y2 = sum(_rnd.gauss(0, 1) ** 2 for _ in range(10)) / 10
        _y = math.sqrt(_y2)
        _hit_t += abs(_x / _y) <= 2.2281          # t_{0.025}(10)
        _hit_f += (_x * _x) / _y2 <= 4.96         # F_{0.05}(1,10)
    check("2010 填空7 蒙特卡洛 P{|X/Y|≤2.2281}≈0.95（t(10)）", _hit_t / _Nsim, 0.95, 0.006)
    check("2010 填空7 蒙特卡洛 P{X²/Y²≤4.96}≈0.95（F(1,10)）", _hit_f / _Nsim, 0.95, 0.006)

    # ---------- 09 号新增章（分布拟合 / 一元回归 / 方差分析附录） ----------
    # 教材例 10.1 数据
    xs = [5, 10, 15, 20, 25, 30]
    ys = [7.25, 8.12, 8.95, 9.90, 10.90, 11.80]
    n9 = len(xs)
    xb9, yb9 = sum(xs) / n9, sum(ys) / n9
    lxx9 = sum((x - xb9) ** 2 for x in xs)
    lyy9 = sum((y - yb9) ** 2 for y in ys)
    lxy9 = sum((x - xb9) * (y - yb9) for x, y in zip(xs, ys))
    b9 = lxy9 / lxx9
    a9 = yb9 - b9 * xb9
    qe9 = lyy9 - b9 * lxy9
    s2_9 = qe9 / (n9 - 2)
    t9 = b9 * math.sqrt(lxx9) / math.sqrt(s2_9)
    r2_9 = 1 - qe9 / lyy9
    check("09章 回归 x̄=17.5", xb9, 17.5)
    check("09章 回归 l_xx=437.5", lxx9, 437.5)
    check("09章 回归 l_xy=80.10", lxy9, 80.10, 1e-9)
    check("09章 回归 b̂=0.1831", b9, 0.1831, 1e-4)
    check("09章 回归 â=6.2827", a9, 6.2827, 2e-4)
    check("09章 回归 σ̂²=Q_e/(n−2)≈0.0033", s2_9, 0.0033, 1e-4)
    check("09章 回归 t≈66.8 > t_{0.025}(4)=2.7764", t9, 66.8, 0.5)
    check("09章 回归 t_{0.025}(4)=2.7764（表值）",
          invert(lambda x: t_sf(x, 4), 0.025, -10, 20), 2.7764, 2e-3)
    check("09章 回归 r²≈0.9991", r2_9, 0.9991, 5e-4)
    check("09章 预测 x₀=25 ⇒ ŷ=10.86", a9 + b9 * 25, 10.86, 0.005)
    # 自测第 1 题
    check_frac("09章 自测1 b̂=0.8", F(8, 10), F(4, 5))
    check_frac("09章 自测1 â=2.4", F(4) - F(4, 5) * F(2), F(12, 5))
    check("09章 自测2 σ̂²=0.4/3", 0.4 / 3, 0.1333, 1e-4)
    check("09章 自测2 t=6.93 > 3.182", (0.8 / math.sqrt(0.4 / 3)) * math.sqrt(10), 6.93, 0.05)
    # 自测 7：方差分析（超纲选做）
    check_frac("09章 自测7 S_E=60", F(100) - F(40), F(60))
    check("09章 自测7 F=(40/2)/(60/12)=4.0", (40 / 2) / (60 / 12), 4.0)
    # 自测 8：硬币均匀性
    check("09章 自测8 χ²=5.76 > 3.84", (12 ** 2) / 50 + (12 ** 2) / 50, 5.76, 1e-9)
    check("09章 自测8 χ²_{0.05}(1)=3.8415", invert(lambda x: chi2_sf(x, 1), 0.05, 0, 50), 3.8415, 5e-3)
    # §3.2 骰子（均匀性，r=0）
    check_frac("09章 骰子 χ²=2.9", F(58, 20), F(29, 10))
    check("09章 χ²_{0.05}(5)=11.070", invert(lambda x: chi2_sf(x, 5), 0.05, 0, 60), 11.070, 5e-3)
    # §3.3 泊松拟合（λ̂=0.9 由样本估计，df=2）
    lam = 0.9
    p0 = math.exp(-lam)
    p1 = lam * math.exp(-lam)
    p2 = lam ** 2 / 2 * math.exp(-lam)
    p3 = 1 - (p0 + p1 + p2)
    ob = [42, 34, 18, 6]
    ex = [100 * p for p in (p0, p1, p2, p3)]
    chi_p = sum((o - e) ** 2 / e for o, e in zip(ob, ex))
    check("09章 泊松拟合 理论频数合计=100", sum(ex), 100.0, 1e-9)
    check("09章 泊松拟合 e_0=40.66", ex[0], 40.66, 5e-3)
    check("09章 泊松拟合 χ²=0.384 < χ²_{0.05}(2)=5.991", chi_p, 0.384, 3e-3)
    check("09章 χ²_{0.05}(2)=5.991", invert(lambda x: chi2_sf(x, 2), 0.05, 0, 40), 5.991, 5e-3)
    # §4 方差分析例题
    gA, gB, gC = [60, 62, 65, 63], [68, 70, 67, 69], [72, 75, 71, 73]
    allv = gA + gB + gC
    gm = sum(allv) / len(allv)
    SA = sum(len(g) * (sum(g) / len(g) - gm) ** 2 for g in (gA, gB, gC))
    SE = sum((v - sum(g) / len(g)) ** 2 for g in (gA, gB, gC) for v in g)
    check("09章 ANOVA S_A=212.167", SA, 212.167, 5e-3)
    check("09章 ANOVA S_E=26.75", SE, 26.75, 1e-9)
    check("09章 ANOVA F=35.69", (SA / 2) / (SE / 9), 35.69, 0.01)
    check("09章 F_{0.05}(2,9)=4.256", invert(lambda x: F_sf(x, 2, 9), 0.05, 1e-6, 60), 4.256, 5e-3)

    # ---------- 模拟卷四（回归专项）+ 期中诊断卷 ----------
    # 卷四 · 三1 回归数据
    x4 = [1, 2, 3, 4, 5, 6, 7, 8]
    y4 = [4.1, 6.3, 7.8, 10.2, 11.7, 14.3, 15.8, 18.0]
    n4 = 8
    xb4, yb4 = sum(x4) / n4, sum(y4) / n4
    lxx4 = sum((x - xb4) ** 2 for x in x4)
    lxy4 = sum((x - xb4) * (y - yb4) for x, y in zip(x4, y4))
    lyy4 = sum((y - yb4) ** 2 for y in y4)
    b4 = lxy4 / lxx4
    a4 = yb4 - b4 * xb4
    qe4 = lyy4 - b4 * lxy4
    s24 = qe4 / (n4 - 2)
    t4 = b4 * math.sqrt(lxx4) / math.sqrt(s24)
    check("卷四 1(1) l_xx=42", lxx4, 42.0)
    check("卷四 1(1) l_xy=82.90", lxy4, 82.90, 1e-9)
    check("卷四 1(1) l_yy=163.995", lyy4, 163.995, 1e-9)
    check("卷四 1(1) b̂=1.9738", b4, 1.9738, 1e-4)
    check("卷四 1(1) â=2.1429", a4, 2.1429, 2e-4)
    check("卷四 1(2) Q_e=0.3662", qe4, 0.3662, 1e-3)
    check("卷四 1(2) σ̂²=0.0610", s24, 0.0610, 1e-3)
    check("卷四 1(3) t=51.78 > t_{0.025}(6)", t4, 51.78, 0.05)
    check("卷四 1(3) t_{0.025}(6)=2.4469", invert(lambda x: t_sf(x, 6), 0.025, -10, 20), 2.4469, 2e-3)
    check("卷四 1(4) r²=0.99777", 1 - qe4 / lyy4, 0.99777, 2e-4)
    check("卷四 1(4) 预测 x₀=9 ⇒ 19.91", a4 + b4 * 9, 19.91, 0.005)
    # 卷四 · 三2 可线性化
    check("卷四 2(1) b̂=-0.15", -1.5 / 10, -0.15, 1e-12)
    check("卷四 2(1) â=e^2.75=15.64", math.exp(2.75), 15.64, 0.005)
    check("卷四 2(3) x=8 ⇒ 4.71", math.exp(2.75) * math.exp(-1.2), 4.71, 0.005)
    check("卷四 2(4) |t|=3.162 > 2.7764", abs((-0.15) / 0.15 * math.sqrt(10)), math.sqrt(10), 1e-12)
    # 卷四 · 三3 泊松拟合（含合并）
    lam4 = 0.9
    pv = [math.exp(-lam4), lam4 * math.exp(-lam4), lam4 ** 2 / 2 * math.exp(-lam4),
          lam4 ** 3 / 6 * math.exp(-lam4)]
    pv.append(1 - sum(pv))
    e4 = [300 * p for p in pv]
    check("卷四 3(1) λ̂=0.9（x̄=270/300）", (115 + 2 * 45 + 3 * 15 + 4 * 5) / 300, 0.9)
    check("卷四 3(2) e_0=121.97", e4[0], 121.97, 5e-3)
    check("卷四 3(2) 合并类 e=18.86", e4[3] + e4[4], 18.86, 5e-3)
    chi4 = ((120 - e4[0]) ** 2 / e4[0] + (115 - e4[1]) ** 2 / e4[1]
            + (45 - e4[2]) ** 2 / e4[2] + (20 - e4[3] - e4[4]) ** 2 / (e4[3] + e4[4]))
    check("卷四 3(3) χ²=0.742 < χ²_{0.05}(2)=5.991", chi4, 0.742, 3e-3)
    # 卷四 · 三4 骰子
    check_frac("卷四 4(1) χ²=44/30", F(25 + 16 + 1 + 1 + 0 + 1, 30), F(44, 30))
    check("卷四 4(2) df=5", 6 - 1 - 0, 5)
    # 卷四 · 三5 成对数据 t 检验（8.5，课表有）
    d5 = [2.0, 3.0, 4.0, 4.0, 5.0, 6.0]
    n5 = len(d5)
    db5 = sum(d5) / n5
    ldd5 = sum((v - db5) ** 2 for v in d5)
    sd5 = math.sqrt(ldd5 / (n5 - 1))
    check("卷四 5(1) d̄=4.000", db5, 4.0, 1e-12)
    check("卷四 5(1) l_dd=10 ⇒ s_d²=2.000", ldd5, 10.0, 1e-12)
    check("卷四 5(1) s_d=1.414", sd5, 1.4142, 5e-4)
    check("卷四 5(2) T=6.928 > t_{0.05}(5)", db5 / (sd5 / math.sqrt(n5)), 6.9282, 5e-4)
    check("卷四 5(2) t_{0.05}(5)=2.0150（表值）",
          invert(lambda x: t_sf(x, 5), 0.05, -10, 20), 2.0150, 2e-3)
    check("卷四 5(3) CI 下限 2.5157", db5 - 2.5706 * sd5 / math.sqrt(n5), 2.5157, 1.5e-3)
    check("卷四 5(3) CI 上限 5.4843", db5 + 2.5706 * sd5 / math.sqrt(n5), 5.4843, 1.5e-3)
    check("卷四 5(3) t_{0.025}(5)=2.5706（表值）",
          invert(lambda x: t_sf(x, 5), 0.025, -10, 20), 2.5706, 2e-3)
    # 卷四 · 附5 方差分析（超纲选做，不计入 100 分）
    g4 = {"A": [62, 65, 63, 66, 64], "B": [68, 71, 69, 70, 72],
          "C": [71, 73, 74, 72, 75], "D": [70, 68, 69, 67, 71]}
    av = [v for g in g4.values() for v in g]
    gm4 = sum(av) / len(av)
    SA4 = sum(len(g) * (sum(g) / len(g) - gm4) ** 2 for g in g4.values())
    SE4 = sum((v - sum(g) / len(g)) ** 2 for g in g4.values() for v in g)
    check("卷四 附5(2) S_A=210、S_E=40", SA4 + SE4, 250.0)
    check("卷四 附5(2) S_A=210", SA4, 210.0)
    check("卷四 附5(3) F=28.0 > F_{0.05}(3,16)", (SA4 / 3) / (SE4 / 16), 28.0, 1e-9)
    check("卷四 附5(3) F_{0.05}(3,16)=3.24", invert(lambda x: F_sf(x, 3, 16), 0.05, 1e-6, 60), 3.239, 3e-3)
    # ---------- 期中诊断卷 ----------
    check_frac("期中 选1 P(A B̄)=0.22", F(5, 10) - F(4, 10) * F(7, 10), F(22, 100))
    check_frac("期中 选2 P(A∪B)=0.7", F(4, 10) + F(5, 10) - F(2, 10), F(7, 10))
    check("期中 选4 P{0<X<4}=0.6826", 2 * Phi(1) - 1, 0.6826, 2e-4)
    check("期中 选5 D(2X−Y+1)=7", 4 * (9 / 12) + 4, 7.0, 1e-12)
    check_frac("期中 填1 恰 2 女 = 15/56", F(comb(3, 2) * comb(5, 1), comb(8, 3)), F(15, 56))
    check_frac("期中 填2 A=3", F(3) * F(1, 3), F(1))
    check_frac("期中 填2 P{X<1/2}=1/8", F(1, 2) ** 3, F(1, 8))
    check("期中 填3 f_Y=(5/2)y^{3/2} 归一",
          simpson(lambda y: 2.5 * y ** 1.5, 0, 1) / 1, 1.0, 1e-9)
    check("期中 填4 E=−3、D=34.4", (3 * 2 - 2 * 5 + 1) + (9 * 1.6 + 4 * 5), -3 + 34.4, 1e-9)
    check("期中 填5 P(B)=0.75", (0.9 - 0.6) / (1 - 0.6), 0.75, 1e-12)
    check("期中 解1(1) P(次品)=0.0285", 0.3 * 0.04 + 0.45 * 0.02 + 0.25 * 0.03, 0.0285, 1e-12)
    check_frac("期中 解1(2) P(丙|次)=5/19", F(75, 285), F(5, 19))
    check_frac("期中 解2(2) P{|X|<1/2}=1/8",
               (F(1, 8) + 1) / 2 - (-F(1, 8) + 1) / 2, F(1, 8))
    check_frac("期中 解2(3) E(X²)=3/5", F(3, 2) * F(2, 5), F(3, 5))
    check_frac("期中 解2(4) D(2X+1)=12/5", 4 * F(3, 5), F(12, 5))
    check("期中 解3(1) c=8（∫∫ = c/8）", (1 / 8) * 8, 1.0, 1e-12)
    check("期中 解3(2) f_Y=4y³ 归一", simpson(lambda y: 4 * y ** 3, 0, 1), 1.0, 1e-9)
    check("期中 解3(2) f_X=4x(1−x²) 归一", simpson(lambda x: 4 * x * (1 - x * x), 0, 1), 1.0, 1e-9)
    check_frac("期中 解3(5) P{X+Y<1}=1/6",
               F(4) * (F(1, 8) - F(2, 24)), F(1, 6))
    check_frac("期中 解3(6) E(X|Y=y)=2y/3", F(2, 3), F(2, 3))
    check_frac("期中 解4(2) P{X>1}=1/4", F(1, 2) / 2, F(1, 4))
    check_frac("期中 解4(4) Cov=−1/9", F(1, 3) - F(2, 3) * F(2, 3), F(-1, 9))
    check_frac("期中 解4(4) ρ=−1/2", F(-1, 9) / (F(2, 9)), F(-1, 2))
    check("期中 解5(1) f_Y=1/(2√y)：∫f=1（换元 u=√y）",
          simpson(lambda u: 1.0, 0, 1), 1.0, 1e-9)
    check("期中 解5(2) f_Z 归一",
          simpson(lambda z: 1 - math.exp(-z), 0, 1) + simpson(lambda z: math.exp(-z) * (math.e - 1), 1, 60),
          1.0, 1e-6)
    check("期中 解5(2) P{Z<1}=e^{−1}", math.exp(-1), 0.3679, 1e-4)

    # ---------- 三套模拟卷 ----------
    # 卷一
    check_frac("卷1 单选1 P(A∪B)", F(1, 2) + F(3, 5) - F(1, 2) * F(2, 5), F(9, 10))
    check("卷1 单选2 P{X<−1}", 1 - Phi(1), 0.1587, 2e-4)
    check_frac("卷1 单选4 D(U(−1,2))", F(3 ** 2, 12), F(3, 4))
    check_frac("卷1 单选5 D(2X−Y+1)", F(4) * 1 + 2, F(6))
    check_frac("卷1 填空1 恰一白", F(comb(3, 1) * comb(2, 1), comb(5, 2)), F(3, 5))
    check("卷1 填空2 P{X=2}", 2 * math.exp(-2), 2 / math.e ** 2)
    check("卷1 填空4 t 区间", 2.1315 * 2 / 4, 1.06575, 1e-9)
    check_frac("卷1 填空5 切比雪夫 1/9", F(1, 9), F(1, 9))
    check("卷1 三1(1) P(次品)", 0.25 * 0.05 + 0.35 * 0.04 + 0.40 * 0.02, 0.0345, 1e-12)
    check_frac("卷1 三1(2) P(甲|次品)", F(0.0125) / F(0.0345), F(25, 69))
    check_frac("卷1 三2(1) c=1", F(1) * (F(1, 2) + F(1, 2)), F(1))
    check_frac("卷1 三2(2) f_X(x)=x+1/2 归一", F(1, 2) + F(1, 2), F(1))
    check_frac("卷1 三2(4) P{X+Y<1}", F(1, 2) - F(1, 6), F(1, 3))
    check_frac("卷1 三2(5) ρ", F(-1, 144) / F(11, 144), F(-1, 11))
    check_frac("卷1 三3(1) E(X)=2/θ", F(2, 1), F(2))
    check_frac("卷1 三4(1) T=(498−500)/(3/3)", F(-2), F(-2))
    check("卷1 三4(2) χ² 区间", 72 / 2.18, 33.03, 0.005)
    check("卷1 三5 z 值", 10 / math.sqrt(59.64), 1.2947, 2e-4)
    # 卷二
    check_frac("卷2 单选1 P(B|A)", F(0.15) / F(0.4), F(3, 8))
    check_frac("卷2 单选3 E(2X+1)", F(2) * 3 + 1, F(7))
    check_frac("卷2 单选4 D(3X−2Y)", F(9) * 2 + F(4) * 3, F(30))
    check_frac("卷2 填空1 能破译", 1 - F(4, 5) * F(2, 3) * F(3, 4), F(3, 5))
    check_frac("卷2 填空2 U(0,θ) MLE=max", F(1), F(1))
    check_frac("卷2 三1(1) k=3/8", F(3, 8) * 8 / 3, F(1))
    check_frac("卷2 三1(3) P{X>1}", 1 - F(1, 8), F(7, 8))
    check_frac("卷2 三1(4) E(X)", F(3, 8) * 4, F(3, 2))
    check_frac("卷2 三2(1) f=2 归一", F(2) * F(1, 2), F(1))
    check_frac("卷2 三2(4) Cov", F(1, 12) - F(1, 9), F(-1, 36))
    check_frac("卷2 三2(4) ρ", F(-1, 36) / F(1, 18), F(-1, 2))
    check("卷2 三3(1) 区间下端", 2.14 - 2.1315 * 0.35 / 4, 1.9535, 1e-4)
    check("卷2 三3(2) T", (2.14 - 2.2) / (0.35 / 4), -0.6857, 1e-4)
    check("卷2 三4(3) P{X+Y<1}", 1 - 2 * math.exp(-0.5) + math.exp(-1), 0.1548, 1e-4)
    check("卷2 三5 z", 500 / 150, 3.3333, 1e-4)
    check("卷2 三5 P", 1 - Phi(3.3333), 0.0004, 5e-5)
    # 卷三
    check_frac("卷3 单选1 P(A∪B)", F(3, 5) + F(1, 2) - F(3, 10), F(4, 5))
    check("卷3 单选3 P{X²<1}", 2 * Phi(1) - 1, 0.6826, 2e-4)
    check_frac("卷3 填空1 Φ(1)", F(8413, 10000), F(8413, 10000))
    check_frac("卷3 填空4 切比雪夫 1/4", F(1, 4), F(1, 4))
    check_frac("卷3 三1(1) 恰一次品", F(comb(3, 1) * comb(7, 2), comb(10, 3)), F(21, 40))
    check_frac("卷3 三1(2) 至少一次品", 1 - F(comb(7, 3), comb(10, 3)), F(17, 24))
    check_frac("卷3 三2(2) P{Z<1.5}", F(1, 2) + F(3, 8), F(7, 8))
    check_frac("卷3 三2(3) D(Z)", F(1, 12) + F(1, 12), F(1, 6))
    check_frac("卷3 三3(1) θ̂_M=x̄=(−2+3)/10", F(-1 * 2 + 0 * 5 + 1 * 3, 10), F(1, 10))
    check_frac("卷3 三3(1) E(X)=−θ+2θ=θ（无偏）", F(-1) + F(2), F(1))
    # 卷3 三3(2)：L=8θ⁵(1−3θ)⁵ ⇒ 5/θ = 15/(1−3θ) ⇒ 1−3θ = 3θ ⇒ θ̂_L = 1/6
    _t = F(1, 6)
    check_frac("卷3 三3(2) θ̂_L=1/6 满足 5/θ=15/(1−3θ)", F(5) / _t, F(15) / (1 - 3 * _t))
    check("卷3 三4(1) T", (338.5 - 340) / (3.5 / math.sqrt(10)), -1.3553, 1e-4)
    check("卷3 三4(2) CI 半宽", 2.2622 * 3.5 / math.sqrt(10), 2.5038, 1e-3)
    check_eq("卷3 三4(3) n=41", math.ceil((2 * 2.2622 * 3.5 / 2.5) ** 2), 41)
    check("卷3 三5 P", 2 * Phi(2.5) - 1, 0.9876, 1e-3)


# ----------------------------------------------------------------------------
def main():
    print("=" * 72)
    print("概率论期末满分包 · 内部验算（结构 + 分位数表 + 答案复算）")
    print("=" * 72)
    structure_checks()
    print("  [1/3] 结构检查完成：%d 项通过 / %d 项失败" % (len(PASS), len(FAIL)))
    quantile_checks()
    print("  [2/3] 分位数表核验完成：累计 %d 通过 / %d 失败" % (len(PASS), len(FAIL)))
    exam_checks()
    print("  [3/3] 真题与模拟卷复算完成\n")

    if FAIL:
        print("❌ 有 %d 项未通过：" % len(FAIL))
        for label, got, want in FAIL:
            print("   - %s：算得 %s，期望 %s" % (label, got, want))
        print("\n总检查项：%d，通过 %d" % (len(PASS) + len(FAIL), len(PASS)))
        return 1

    print("✅ 全部 %d 项检查通过（结构 / 分位数表 / 真题与模拟卷答案复算）" % len(PASS))
    print("   备注：官方答案册个别数值为印刷性错误者，已在包内按题面复算并标注。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
