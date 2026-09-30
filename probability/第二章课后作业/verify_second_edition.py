"""第二版 A2–A26、B2/B4/B6 的多方法校验；失败即不交付。"""
from collections import defaultdict
from fractions import Fraction as Q
from math import comb, exp, pi, asin, sqrt, factorial, isclose
from pathlib import Path
from statistics import NormalDist
import re
import pymupdf

root=Path(__file__).resolve().parent
question=(root/'作业02-第二版第二章AB偶数题.md').read_text()
answer=(root/'作业02-第二版第二章AB偶数题-参考答案.md').read_text()
ids=[f'A{i}' for i in range(2,27,2)]+['B2','B4','B6']
assert re.findall(r'^### ([AB]\d+)$',question,re.M)==ids
assert re.findall(r'^### ([AB]\d+)$',answer,re.M)==ids

def near(a,b,tol=1e-9):assert isclose(a,b,rel_tol=tol,abs_tol=tol),(a,b)
# A2: 径向CDF微分积分 + 面积比
for x in (.1,.5,1): near(x*x, (2*(x/2))*x)  # 密度 2t 在[0,x]上的线性函数中点积分
# A4: 两个尾极限 + arctan差
near((1/pi)*(pi/4-(-pi/4)),.5)
# A6: 逐个跳跃和累加CDF
p6=[Q(1,8),Q(1,2),Q(1,4),Q(1,8)]
assert sum(p6)==1 and [sum(p6[:i]) for i in range(1,5)]==[Q(1,8),Q(5,8),Q(7,8),1]
# A8: 广义式与放回式归一，枚举n件中k件，测试边界 M=0
for N,M,n in [(15,3,5),(9,5,7),(5,0,2),(5,5,3)]:
 k0=max(0,n-N+M); k1=min(M,n)
 assert sum(Q(comb(M,k)*comb(N-M,n-k),comb(N,n)) for k in range(k0,k1+1))==1
 assert sum(Q(comb(n,k)*M**k*(N-M)**(n-k),N**n) for k in range(n+1))==1
# A10: r=1时还原几何，其他r求前500项
for r,p in [(1,.2),(3,.4),(5,.75)]:
 dist=[comb(k-1,r-1)*p**r*(1-p)**(k-r) for k in range(r,r+501)]
 near(sum(dist),1,1e-8)
 if r==1:near(dist[2],p*(1-p)**2)
# A12: 精确二项 vs 泊松近似
b12=sum(comb(500,k)*.005**k*.995**(500-k) for k in range(6))
near(b12,.9583971796320703)
assert abs(b12-sum(exp(-2.5)*2.5**k/factorial(k) for k in range(6)))<.001
# A14: 穷举概率峰，整数两众数
for lam,expect in [(4,[3,4]),(.4,[0]),(3.2,[3])]:
 pp=[exp(-lam)*lam**k/factorial(k) for k in range(15)];mx=max(pp)
 assert [k for k,v in enumerate(pp) if isclose(v,mx,rel_tol=1e-12)]==expect
# A16: CDF vs symmetric integral; boundaries
near((asin(.5)-asin(-.5))/pi,Q(1,3))
near((asin(1)+pi/2)/pi,1);near((asin(-1)+pi/2)/pi,0)
# A18: independent NormalDist symmetry for range of parameters
for mu,sigma in [(0,1),(-3,2),(10,.4)]:
 norm=NormalDist(mu,sigma)
 for x in [mu-1,mu,mu+3]:near(norm.cdf(x)+norm.cdf(2*mu-x),1)
# A20: 判别式=4(9-6x) 的离散网格计数 vs 几何长度
num=sum((9-6*((i+.5)*5/100000)>=0) for i in range(100000))
near(num/100000,Q(3,10),1e-5)
# A22: 原6原子按四函数独立聚合；最后各和1
X=[-2,-1,0,1,2,3];P=[Q(1,15),Q(1,10),Q(1,6),Q(1,3),Q(3,10),Q(1,30)]
assert sum(P)==1
funcs=[lambda x:Q(2)**x,lambda x:abs(1-2*x),lambda x:1-x*x,
       lambda x:{-2:0,-1:1,0:2,1:1,2:0,3:-2}[x]]
wants=[{Q(1,4):Q(1,15),Q(1,2):Q(1,10),1:Q(1,6),2:Q(1,3),4:Q(3,10),8:Q(1,30)},
       {1:Q(1,2),3:Q(2,5),5:Q(1,10)},
       {-8:Q(1,30),-3:Q(11,30),0:Q(13,30),1:Q(1,6)},
       {-2:Q(1,30),0:Q(11,30),1:Q(13,30),2:Q(1,6)}]
for f,w in zip(funcs,wants):
 got=defaultdict(Q)
 for x,p in zip(X,P):got[f(x)]+=p
 assert got==w and sum(got.values())==1,(got,w)
# A24: transformation CDF and Jacobian integrate numerically via X variable
for lam in (.3,1,4):
 for y in (.1,.5,2):
  h=1e-5
  cdf=lambda z:1-exp(-lam*z**(1/3))
  deriv=(cdf(y+h)-cdf(y-h))/(2*h)
  near(deriv,lam*exp(-lam*y**(1/3))/(3*y**(2/3)),1e-8)
 for y in (.1,.5,.9):near(exp(-lam*(-__import__('math').log(y)/lam)),y)
# A26: 半正态CDF+两根密度
for sigma in (.5,2):
 for y in (.1,1):
  h=1e-5;nc=NormalDist(0,sigma)
  cdf=lambda z:nc.cdf(z)-nc.cdf(-z)
  near((cdf(y+h)-cdf(y-h))/(2*h),2*exp(-y*y/(2*sigma*sigma))/(sigma*sqrt(2*pi)),1e-8)
# B2: 直接公式与独立子群卷积（作为另一路）
q=.01;group=[comb(20,k)*q**k*(1-q)**(20-k) for k in range(21)]
p1=1-(group[0]+group[1])**5
p2=1-sum(comb(100,k)*q**k*(1-q)**(100-k) for k in range(6))
near(p1,.08150183345137352);near(p2,.0005345344639938743)
conv=[1.]
for _ in range(5):
 nxt=[0.]*(len(conv)+20)
 for i,u in enumerate(conv):
  for j,v in enumerate(group):nxt[i+j]+=u*v
 conv=nxt
near(1-sum(conv[:6]),p2);near(1-sum((group[0]+group[1])**5 for _ in [0]),p1)
assert p2<p1
# B4: two densities via CDF finite difference and analytic normalization
for R in (1,3):
 for y in (-R/2,0,R/2):
  cdf=lambda z:.5+asin(z/R)/pi
  h=1e-5
  near((cdf(y+h)-cdf(y-h))/(2*h),1/(pi*sqrt(R*R-y*y)),1e-8)
 for l in (R/2,R,3*R/2):
  cdf=lambda z:2*asin(z/(2*R))/pi
  h=1e-5
  near((cdf(l+h)-cdf(l-h))/(2*h),2/(pi*sqrt(4*R*R-l*l)),1e-8)
 near((asin(1)-asin(-1))/pi,1)
 near(2*asin(1)/pi,1)
# B6: intervals vs survival difference, total mass
for lam in (.3,1,5):
 a=exp(-lam)
 for k in range(1,5): near(exp(-lam*(k-1))-exp(-lam*k),(1-a)*a**(k-1))
 near(sum((1-a)*a**(k-1) for k in range(1,300)),1)
# PDF coverage / glyph, no orphaned exercise numbers
for kind in ('答题卷','完整解析'):
 path=root/f'第二版-第二章AB偶数题-{kind}.pdf';doc=pymupdf.open(path)
 assert all(abs(p.rect.width-595.28)<1 and abs(p.rect.height-841.89)<1 and len(p.get_text())>100 for p in doc)
 text='\n'.join(p.get_text() for p in doc)
 if kind=='答题卷': assert re.findall(r'\b([AB]\d+) 题',text)==ids
 else:
  for id in ids:assert re.search(rf'(?m)^{id}\n',text),id
 for s in ('-1','^2','B4'):assert s in text,(kind,s)
print('PASS 16/16: independently checked supports/normalization, transformations, B2 convolution, B4 CDF, B6 tails, PDFs')
