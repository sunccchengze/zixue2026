"""用穷举/精确分数独立复核可计算题；运行后所有断言通过即验证成功。"""
from fractions import Fraction as F
from itertools import product, combinations
from math import comb
# 5：真值表验证化简结果 Ω 与 ∅
for A,B in product([False,True], repeat=2):
    e1=(A and B) or (A and not B) or not A
    D=(A and not B) or (B and not A)
    e2=((A or B) and not D) and not B
    assert e1 and not e2
# 7：10^3小块中恰有两个坐标位于边界（即两涂色面）
n2=sum(sum(c in (0,9) for c in xyz)==2 for xyz in product(range(10), repeat=3))
assert n2==96
# 9：面积法（乘2避免半数）
assert F(24*24*2-(23*23+22*22),24*24*2)==F(139,1152)
# 15
assert (F(comb(4,2),comb(10,3)),F(comb(5,2),comb(10,3)),F(comb(4,3),comb(10,3)),1-F(comb(5,3),comb(10,3)))==(F(1,20),F(1,12),F(1,30),F(11,12))
# 19：用花色四元组穷举牌的组合，核对四个计数公式
cards=list(product(range(4),range(13))); hands=list(combinations(cards,4)); den=len(hands)
c1=sum(len({c[0] for c in h})==1 for h in hands)
c2=sum(len({c[0] for c in h})==4 for h in hands)
c4=sum(any(c[1]==0 for c in h) for h in hands)
assert (c1,c2,den-c2,c4)==(4*comb(13,4),13**4,den-13**4,den-comb(48,4))
# 21：直接枚举4^3投放结果
mx=[max(s.count(i) for i in range(4)) for s in product(range(4),repeat=3)]
assert tuple(F(mx.count(k),64) for k in (1,2,3))==(F(3,8),F(9,16),F(1,16))
# 25,27,29,31,37
assert F(1,4)+F(1,6)-F(1,12)==F(1,3)
assert F(7,100)*F(6,99)*F(93,98)==F(217,53900)
assert sum((F(4,20)*F(9,10),F(8,20)*F(7,10),F(7,20)*F(5,10),F(1,20)*F(2,10)))==F(129,200)
good=F(4,9)*F(4,5)+F(3,9)*F(3,5)+F(2,9)*F(7,10)
assert good==F(32,45) and (F(3,9)*F(3,5))/good==F(9,32)
assert 1-F(1,5)*F(1,3)*F(1,4)==F(59,60)
print('PASS：题5、7、9、15、19、21、25、27、29、31、37的独立穷举/精确分数复核全部通过。')
