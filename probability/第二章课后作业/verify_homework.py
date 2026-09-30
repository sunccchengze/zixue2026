"""对本作业的题号、离散分布、概率和 PDF 完整性做独立数值复核。"""
from collections import defaultdict
from fractions import Fraction as F
from math import comb, exp, factorial, isclose
from pathlib import Path
from statistics import NormalDist
import re
import pymupdf

root = Path(__file__).resolve().parent
q = (root/'作业02-第二章习题偶数题-已核实部分.md').read_text()
a = (root/'作业02-第二章习题偶数题-已核实部分-参考答案.md').read_text()
nums = list(range(2,31,2))
assert [int(n) for n in re.findall(r'^### (\d+)',q,re.M)] == nums
assert [int(n) for n in re.findall(r'^## (\d+)｜',a,re.M)] == nums
assert sum([F(1,15),F(1,10),F(1,6),F(1,3),F(3,10),F(1,30)])==1
xvals=[-2,-1,0,1,2,3]
probs=[F(1,15),F(1,10),F(1,6),F(1,3),F(3,10),F(1,30)]
expected=[{F(1,4):F(1,15),F(1,2):F(1,10),F(1):F(1,6),F(2):F(1,3),F(4):F(3,10),F(8):F(1,30)},
          {1:F(1,2),3:F(2,5),5:F(1,10)},
          {-8:F(1,30),-3:F(11,30),0:F(13,30),1:F(1,6)},
          {-1:F(1,30),0:F(11,30),1:F(13,30),2:F(1,6)}]
# 用整数编码 cos(pi*x/4)：-1↔-√2/2, 1↔√2/2, 2↔1
functions=[lambda x:F(2)**x, lambda x:abs(1-2*x),lambda x:1-x*x,
           lambda x:{-2:0,-1:1,0:2,1:1,2:0,3:-1}[x]]
for fn,want in zip(functions,expected):
 got=defaultdict(F)
 for x,p in zip(xvals,probs): got[fn(x)]+=p
 assert got==want,(got,want)
 assert sum(got.values())==1
assert sum(F(comb(3,k)*comb(12,5-k),comb(15,5)) for k in range(4))==1
assert sum(F(comb(5,k)*4**(5-k),5**5) for k in range(6))==1
p12=sum(comb(500,k)*.005**k*.995**(500-k) for k in range(6))
assert isclose(p12,.9583971796320703,abs_tol=1e-12)
assert isclose(exp(-3)-exp(-4.5), .03867807182962164,abs_tol=1e-12)
N=NormalDist(); a20=(3*N.inv_cdf(N.cdf(2/3)+.01)-2)/2
assert isclose(a20,.04746085364633479,abs_tol=1e-12)
assert isclose(N.cdf((2*a20+2)/3)-N.cdf(2/3),.01,abs_tol=1e-12)
assert isclose(exp(-4)*4**3/factorial(3),exp(-4)*4**4/factorial(4))
for kind in ['答题卷','完整解析']:
 pdf=list(root.glob(f'*{kind}.pdf'))
 assert len(pdf)==1
 d=pymupdf.open(pdf[0]);assert len(d)>0
 assert all(abs(p.rect.width-595.28)<1 and abs(p.rect.height-841.89)<1 and len(p.get_text())>100 for p in d)
 t='\n'.join(p.get_text() for p in d)
 if kind=='答题卷':
  assert [int(n) for n in re.findall(r'第 (\d+) 题\n',t)]==nums
 else:
  for n in nums: assert re.search(rf'(?m)^\s*{n} *[｜|]',t),n
 assert 'A/B' in t
print('PASS: 15道题题号，离散分布、二项/正态/指数数值，A4 PDF文字及页码')
