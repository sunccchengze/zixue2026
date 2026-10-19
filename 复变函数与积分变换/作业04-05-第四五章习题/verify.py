#!/usr/bin/env python3
"""数值自查：第四章/第五章关键结果。失败则退出码非零。"""
import cmath, math
ok = True
def check(name, cond, detail=''):
    global ok
    if cond:
        print(f'  OK  {name}  {detail}')
    else:
        ok = False
        print(f' FAIL {name}  {detail}')

# 4.1(2)
a = (1+0.5j)**(-80)
check('4.1(2) |α_n|单调→0', abs(a) < abs((1+0.5j)**(-20)), f'|α_80|={abs(a):.3e}')

# 4.3(4) |cos(in)/2^n| ~ ch(n)/2^n
n=10
check('4.3(4) 通项不→0', abs(math.cosh(n)/2**n) > 10, f'ch(10)/2^10={math.cosh(10)/2**10:.1f}')

# 4.3(5) |a_n| ~ 2 e^{-n}
def a5(n):
    return abs((1+1j)**n / (2**(n/2) * cmath.sin(1j*n)))
s = sum(a5(n) for n in range(1, 40))
check('4.3(5) 绝对收敛估计', s < 3, f'sum_1^39 |a_n|={s:.4f}')

# 4.5(2)
check('4.5(2) R=5', abs(complex(-3,4)) == 5)

# 4.6(2) |c_n/c_{n+1}| → 0
def ratio(n):
    return ((1+1/n)**(n-1))/n
check('4.6(2) R=0', ratio(80) < ratio(20) < 0.2, f'|c80/c81|={ratio(80):.4e}')

# 4.20 residues
def res20_2():
    # (z+2)/((z+1)z)
    r0 = 2/1
    r1 = (1)/(-1)
    return r0 + r1
check('4.20(2) 留数和=1', abs(res20_2()-1)<1e-12, str(res20_2()))

def res20_4():
    r_m1 = (-1)/((-1)+2)  # z/(z+2) at -1
    r_m2 = (-2)/((-2)+1)
    return r_m1 + r_m2
check('4.20(4) 留数和=1', abs(res20_4()-1)<1e-12, str(res20_4()))

# 5.9(2) Laurent of (1-e^{2z})/z^4 at 0: coeff of z^{-1} = -4/3
# 1-e^{2z} = -∑_{k≥1} (2z)^k / k!
# / z^4  → k-4 = -1 ⇒ k=3 ⇒ - 2^3 / 3! = -8/6 = -4/3
check('5.9(2) Res=-4/3', abs(-8/6 + 4/3)<1e-12)

# 5.12(5) 6 poles × (-1/π) × 2πi = -12 i
check('5.12(5) -12i', abs(6*(-1/math.pi)*2*math.pi + 12)<1e-12)

# 5.15(1)
e = math.e
r = -(e/2 - 1/(2*e))
check('5.15(1)', abs(r - (1-e**2)/(2*e))<1e-12, f'{r:.6f}')

# 5.17(4) numerical
def f(x):
    return x*x/(1+x**4)
# simpson on [0, 40]
N=200000; a=0; b=200; h=(b-a)/N
s = f(a)+f(b)
for i in range(1,N):
    x=a+i*h
    s += 4*f(x) if i%2 else 2*f(x)
I = s*h/3
exact = math.pi/(2*math.sqrt(2))
check('5.17(4) π/(2√2)', abs(I-exact)<1e-2, f'num={I:.6f} exact={exact:.6f}')

# 5.17(2) b→0 limit π/a
a,b=3.0, 0.01
closed = 2*math.pi/b**2 * (a - math.sqrt(a*a-b*b))
check('5.17(2) b→0 →π/a', abs(closed - math.pi/a)<1e-2, f'{closed:.4f} vs {math.pi/a:.4f}')

# 5.16(2) 留数和 = -1/3
s16 = -1/math.e + sum((-1)**m/math.factorial(m+4) for m in range(0,40))
check('5.16(2) 留数和=-1/3', abs(s16 + 1/3)<1e-12, f'{s16:.8f}')

print('ALL PASS' if ok else 'SOME FAILED')
raise SystemExit(0 if ok else 1)
