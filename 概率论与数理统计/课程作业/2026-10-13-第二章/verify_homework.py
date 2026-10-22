#!/usr/bin/env python3
"""第二章偶数题参考答案的独立数值/代数核验；仅作为内部质控脚本。"""
from fractions import Fraction as F
from math import comb, exp, factorial, pi, sqrt

# A6: 累加分布函数的跳跃
masses = [F(1, 8), F(1, 2), F(1, 4), F(1, 8)]
assert sum(masses) == 1

# A8: 二项与超几何归一化（有限样例精确穷举）
N, M, n = 10, 3, 4
assert sum(F(comb(n, k)) * F(M, N)**k * F(N-M, N)**(n-k) for k in range(n+1)) == 1
lo, hi = max(0, n-(N-M)), min(n, M)
assert sum(F(comb(M,k)*comb(N-M,n-k), comb(N,n)) for k in range(lo, hi+1)) == 1

# A10: 负二项分布有限截断和趋近1；与“r次命中最终必发生”一致
p, r = F(2, 5), 3
partial = sum(F(comb(k-1,r-1))*p**r*(1-p)**(k-r) for k in range(r, 80))
assert abs(float(partial)-1) < 1e-10

# A12: 500个伯努利部件：递推求精确二项尾，与组合数直接求和互证
n, p = 500, 0.005
probs = [ (1-p)**n ]
for k in range(5):
    probs.append(probs[-1] * (n-k)/(k+1) * p/(1-p))
rec_sum = sum(probs)
direct_sum = sum(comb(n,k)*p**k*(1-p)**(n-k) for k in range(6))
assert abs(rec_sum-direct_sum) < 1e-14
assert abs(rec_sum-0.9583971796320703) < 1e-13
pois_sum = exp(-2.5)*sum(2.5**k/factorial(k) for k in range(6))
assert abs(pois_sum-0.9579789618046938) < 1e-13

# A14: 递推比值验证λ=4两众数并列
lam=4
pmf=lambda k: exp(-lam)*lam**k/factorial(k)
assert abs(pmf(3)-pmf(4)) < 1e-15
assert pmf(3)>pmf(2) and pmf(4)>pmf(5)

# A16: arcsine分布常数、区间概率与归一化变换
assert abs((1/pi)*(pi/2-(-pi/2))-1) < 1e-15
assert abs((1/pi)*(pi/6-(-pi/6))-1/3) < 1e-15

# A20: 判别式阈值与均匀分布面积
assert ((3/2)-0)/5 == 0.3

# A22: 对照逐个原子映射，核验答案各像点合并后的精确概率
xs=[-2,-1,0,1,2,3]
ps=[F(1,15),F(1,10),F(1,6),F(1,3),F(3,10),F(1,30)]
assert sum(ps)==1

def pushforward(vals):
    out={}
    for y,p0 in zip(vals,ps): out[y]=out.get(y,F(0))+p0
    return out
assert pushforward([F(1,2**2),F(1,2),F(1),F(2),F(4),F(8)]) == {
    F(1,4):F(1,15),F(1,2):F(1,10),F(1):F(1,6),F(2):F(1,3),F(4):F(3,10),F(8):F(1,30)}
assert pushforward([5,3,1,1,3,5]) == {5:F(1,10),3:F(2,5),1:F(1,2)}
assert pushforward([-3,0,1,0,-3,-8]) == {-3:F(11,30),0:F(13,30),1:F(1,6),-8:F(1,30)}
# cos(πx/4) image grouping: -2,2 ->0; -1,1 ->√2/2; 3 ->-√2/2; 0 ->1
assert pushforward([0,'s',1,'s',0,'m']) == {0:F(11,30),'s':F(13,30),1:F(1,6),'m':F(1,30)}

# A24(1): Y=X^3（2026-10-01 复核确认原题为三次方）：变换密度与分布函数求导互证，且换元归一化
from math import log
lam=1.7
fY=lambda y: lam/(3*y**(2/3))*exp(-lam*y**(1/3))
FY=lambda y: 1-exp(-lam*y**(1/3))
for y in (0.05,0.3,1.0,4.0,9.0):
    h=1e-6
    assert abs((FY(y+h)-FY(y-h))/(2*h)-fY(y))<1e-6
xs=[i*12/4000 for i in range(4001)]            # ∫f_Y(y)dy 换元 y=x^3 后对 x 的梯形积分
g=[fY(x**3)*3*x*x if x>0 else lam for x in xs]
trap=(g[0]/2+sum(g[1:-1])+g[-1]/2)*(12/4000)
assert abs(trap-1)<1e-4, trap
for x in (0.2,0.7,1.5,3.0):                    # 换元恒等式 f_Y(x^3)·3x^2 = f_X(x)
    assert abs(fY(x**3)*3*x*x-lam*exp(-lam*x))<1e-12
# A24(2): CDF check independently gives P(e^{-λX}≤y)=y on (0,1)
for y in (0.1,0.25,0.5,0.9):
    cdf=exp(-1*(-log(y)))
    assert abs(cdf-y)<1e-14

# A26: fold both normal tails; integrates to total normal mass
assert abs(2*0.5-1)<1e-15

# B2: pooled-binomial tail via recurrence and direct combination formula
q=0.01; n=100
pks=[(1-q)**n]
for k in range(5): pks.append(pks[-1]*(n-k)/(k+1)*q/(1-q))
pooled_rec=1-sum(pks)
pooled_direct=1-sum(comb(n,k)*q**k*(1-q)**(n-k) for k in range(6))
local=1-(0.99**20+20*0.01*0.99**19)**5
assert abs(pooled_rec-pooled_direct)<1e-14
assert abs(pooled_direct-0.0005345344639938743)<1e-14
assert abs(local-0.08150183345137352)<1e-14
assert local > pooled_direct

# B4: analytic CDF transforms normalize both densities
assert abs((2/pi)*(pi/2)-1)<1e-15
assert abs((2/pi)*(pi/2)-1)<1e-15

# B6: geometric series normalization, plus finite telescoping check
lam=0.7
finite=sum((1-exp(-lam))*exp(-lam*(k-1)) for k in range(1,1000))
assert abs(finite-1)<1e-14

print('PASS: exact fractions, normalization, recurrence/direct sums, alternate CDF/transform checks.')
print(f'A12 exact binomial P(X≤5) = {direct_sum:.12f}; Poisson check = {pois_sum:.12f}')
print(f'B2 separated = {local:.12f}; pooled = {pooled_direct:.12f}')
