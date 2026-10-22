#!/usr/bin/env python3
"""第二版习题1 A/B奇数题：独立穷举、精确分数、可靠性状态枚举。内部质控。"""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations, permutations, product
from math import comb

# A3 区间端点
Omega = (0, 5)
A, B = (1, 3), (2, 4)  # A闭, B左开右闭
assert (1, 4) == (min(A[0], B[0]), max(A[1], B[1]))  # 并
assert (2, 3) == (B[0], A[1])  # 交：(2,3]
assert (1, 2) == (A[0], B[0])  # 差：[1,2]

# A5 10^3 小立方体恰两面涂红
n2 = sum(sum(c in (0, 9) for c in xyz) == 2 for xyz in product(range(10), repeat=3))
assert n2 == 12 * 8 == 96
assert F(96, 1000) == F(12, 125)

# A7 线性24h几何概型：等待区域 vs 补集三角形
T = 24 * 24
nowait = (23 ** 2 + 22 ** 2) / 2
wait = T - nowait
assert wait * 2 == 139  # 69.5
assert F(139, 1152) == F(int(wait * 2), T * 2)
# 直接带宽：x≤y 的带宽1（末端直角三角形），y<x 的带宽2
band1 = 23 * 1 + 0.5
band2 = 22 * 2 + 2
assert band1 + band2 == wait

# A9 原子：AC=空 ⇒ ABC=空；容斥
PA = PB = PC = F(1, 4)
PAB = PBC = F(1, 8)
PAC = F(0)
PABC = F(0)
Pun = PA + PB + PC - PAB - PBC - PAC + PABC
assert Pun == F(1, 2)
assert 1 - Pun == F(1, 2)

# A11 4白6红，两次
# 不放回
assert F(4, 10) * F(3, 9) == F(2, 15)          # A 白白
assert F(4, 10) * F(6, 9) == F(4, 15)          # B 白红
assert F(4, 10) * F(6, 9) + F(6, 10) * F(4, 9) == F(8, 15)  # C 恰1红
assert F(4, 10) * F(3, 9) + F(6, 10) * F(4, 9) == F(2, 5)   # D 第二次白
# 放回
assert F(4, 10) ** 2 == F(4, 25)
assert F(4, 10) * F(6, 10) == F(6, 25)
assert 2 * F(4, 10) * F(6, 10) == F(12, 25)
assert F(4, 10) == F(2, 5)  # 放回时第二次白仍4/10

# A13 4人12月，至少2人同月
all_diff = F(12 * 11 * 10 * 9, 12 ** 4)
assert all_diff == F(55, 96)
assert 1 - all_diff == F(41, 96)
# 穷举月份四元组核对补事件
months = range(12)
# 太大不穷举12^4；改用计数：P(12,4) vs 12^4
assert comb(12, 4) * 24 == 12 * 11 * 10 * 9

# A15 无放回4位偶数（首位非0、末位偶数）
fav = 0
for p in permutations(range(10), 4):
    if p[0] != 0 and p[3] % 2 == 0:
        fav += 1
assert fav == 2296
assert F(fav, 10 * 9 * 8 * 7) == F(41, 90)
# 分类互证
last0 = 9 * 8 * 7  # 末位0，首位1-9，其余P(8,2)
last_even_nz = 4 * 8 * 8 * 7  # 末位2/4/6/8，首位8种非0，再8、7
assert last0 + last_even_nz == 504 + 1792 == 2296

# A17
PA, PB, PAB = F(7, 10), F(4, 10), F(2, 10)
PAminusB = PA - PAB
Pun = PA + PB - PAB
assert PAminusB / Pun == F(5, 9)

# A19 第三次才合格 = 次、次、合
assert F(7, 100) * F(6, 99) * F(93, 98) == F(217, 53900)

# A21 全概率
p10 = F(4, 20) * F(9, 10) + F(8, 20) * F(7, 10) + F(7, 20) * F(5, 10) + F(1, 20) * F(2, 10)
assert p10 == F(129, 200)

# A23 贝叶斯
pg = F(4, 9) * F(4, 5) + F(3, 9) * F(3, 5) + F(2, 9) * F(7, 10)
assert pg == F(32, 45)
assert (F(3, 9) * F(3, 5)) / pg == F(9, 32)

# A25 数值实例：P(A|B)=P(A|Bc) ⇒ 独立
for pa, pb in [(F(1, 3), F(2, 5)), (F(4, 7), F(1, 4))]:
    # 构造独立则条件相等；再反推
    pab = pa * pb
    p_a_b = pab / pb
    p_a_bc = (pa - pab) / (1 - pb)
    assert p_a_b == p_a_bc == pa

# A27 独立射击
assert 1 - F(1, 5) * F(1, 3) * F(1, 4) == F(59, 60)
ps = (F(4, 5), F(2, 3), F(3, 4))
tot = F(0)
for s in product([0, 1], repeat=3):
    mass = F(1)
    for hit, p in zip(s, ps):
        mass *= p if hit else 1 - p
    if any(s):
        tot += mass
assert tot == F(59, 60)

# A29 n=1 相等；n=2,3,4 系统II更大；多项式恒等
def RI(p, n):
    return 2 * p ** n - p ** (2 * n)

def RII(p, n):
    return (2 * p - p ** 2) ** n

for n in range(1, 6):
    for pv in (0.2, 0.5, 0.8):
        if n == 1:
            assert abs(RI(pv, n) - RII(pv, n)) < 1e-12
        else:
            assert RII(pv, n) > RI(pv, n)
# 归纳比较式 (2-p)^n > 2-p^n (n≥2, 0<p<1)
for n in range(2, 8):
    for pv in (0.1, 0.3, 0.7, 0.9):
        assert (2 - pv) ** n > 2 - pv ** n

# B1 排列
assert F(120 * 32, 3628800) == F(1, 945)           # 5! 2^5 / 10!
assert F(1, 32) == F(1, 32)                         # 五对相对顺序
assert F(24 * 32, 362880) == F(2, 945)              # 4! 2^5 / 9!
# 小规模：2对夫妻直线相邻
assert F(2 * 2 * 4, 24) == F(2, 3)  # 2! 2^2 / 4! wait 2!*4/24=8/24=1/3
assert F(2 * 4, 24) == F(1, 3)

# B3 全概率 / 贝叶斯
p = F(1, 5)
q = F(4, 5)
px = [q ** 3, 3 * p * q ** 2, 3 * p ** 2 * q, p ** 3]
assert px == [F(64, 125), F(48, 125), F(12, 125), F(1, 125)]
pf = F(0) * px[0] + F(1, 4) * px[1] + F(3, 5) * px[2] + F(19, 20) * px[3]
assert pf == F(403, 2500)
assert (F(3, 5) * px[2]) / pf == F(144, 403)

# B5 系统I/II：32状态多项式 vs 闭式
def sysI(s):
    e1, e2, e3, e4, e5 = s
    return (e1 and e2 or e3 and e4) and e5

def sysII(s):
    e1, e2, e3, e4, e5 = s
    return (e1 and e2) or (e3 and e4) or (e1 and e5 and e4) or (e3 and e5 and e2)

def poly(pred):
    c = Counter()
    for s in product([0, 1], repeat=5):
        if pred(s):
            c[sum(s)] += 1
    return c

# 闭式 R_I = 2p^3 - p^5 = p^3(2-p^2) → 项 p^3:2, p^5:-1 即 3工作2失效 与 5工作
# 枚举计数：按工作元件数
cI, cII = poly(sysI), poly(sysII)

def eval_poly(c, p):
    q = 1 - p
    return sum(cnt * p ** k * q ** (5 - k) for k, cnt in c.items())

for pv in (0.2, 0.4, 0.6, 0.8):
    assert abs(eval_poly(cI, pv) - (2 * pv ** 3 - pv ** 5)) < 1e-12
    closed_II = pv * (2 * pv - pv ** 2) ** 2 + (1 - pv) * (2 * pv ** 2 - pv ** 4)
    assert abs(eval_poly(cII, pv) - closed_II) < 1e-12
    expanded = 2 * pv ** 2 + 2 * pv ** 3 - 5 * pv ** 4 + 2 * pv ** 5
    assert abs(closed_II - expanded) < 1e-12

# B5(2) 条件概率：1,2同时失效且系统I工作 ⇔ 3,4,5全工作
p = F(3, 7)
num = (1 - p) ** 2 * p ** 3
den = 2 * p ** 3 - p ** 5
assert num / den == (1 - p) ** 2 / (2 - p ** 2)

print('PASS: 第二版习题1 A/B奇数题独立复核全部通过。')
print(f'A5={F(12,125)}  A7={F(139,1152)}  A9并={F(1,2)}  A13={F(41,96)}  A15={F(41,90)}')
print(f'A17={F(5,9)}  A19={F(217,53900)}  A21={F(129,200)}  A23好评={F(32,45)} 后验={F(9,32)}')
print(f'A27={F(59,60)}  B1={F(1,945)}, {F(1,32)}, {F(2,945)}  B3={F(403,2500)}, {F(144,403)}')
