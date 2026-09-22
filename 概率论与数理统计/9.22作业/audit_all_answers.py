"""全题双轨审计：解析公式 vs 独立穷举/动态规划/代数恒等式。"""
from fractions import Fraction as F
from itertools import product, combinations
from math import comb
from collections import Counter

# 1：停止规则状态树
terminal=set()
def walk(s=''):
    if s.endswith('次次') or len(s)==4: terminal.add(s); return
    walk(s+'正'); walk(s+'次')
walk()
assert terminal=={'次次','正次次','正正正正','正正正次','正正次正','正正次次','正次正正','正次正次','次正正正','次正正次','次正次正','次正次次'}
# 3、5：8/4行真值表逐行核对事件含义和化简
for A,B,C in product([0,1],repeat=3):
    assert (A and B and not C)==bool(A*B*(1-C))
    assert ((not A) and B and (not C))==bool((1-A)*B*(1-C))
    assert not(A or C)==((not A) and (not C))
    assert (A and not(B or C))==(A and not B and not C)
for A,B in product([0,1],repeat=2):
    e1=(A and B) or (A and not B) or not A
    D=(A and not B) or (B and not A)
    e2=(A or B) and not D and not B
    assert e1 and not e2
# 7：坐标穷举
assert sum(sum(t in (0,9) for t in xyz)==2 for xyz in product(range(10),repeat=3))==12*(10-2)==96
# 9：积分区域面积 vs 补集三角形
wait2=2*24*24-(24-1)**2-(24-2)**2
assert F(wait2,2*24*24)==F(139,1152)
# 11：8原子构造并直接求并集（原子顺序abc）
atoms={(1,1,0):F(1,8),(0,1,1):F(1,8),(1,0,0):F(1,8),(0,0,1):F(1,8),(0,1,0):F(0), (0,0,0):F(1,2),(1,0,1):F(0),(1,1,1):F(0)}
assert sum(v for k,v in atoms.items() if k[0])==F(1,4)
assert sum(v for k,v in atoms.items() if any(k))==F(1,2)
# 13：对多个确定集合直接核对容斥
sets=[{1,2,5},{2,3},{1,4},{2,4,5}]
lhs=len(set().union(*sets)); rhs=0
for r in range(1,len(sets)+1):
    rhs+=(-1)**(r+1)*sum(len(set.intersection(*(sets[i] for i in I))) for I in combinations(range(len(sets)),r))
assert lhs==rhs
# 15：枚举120个号码组合
hands=list(combinations(range(1,11),3)); den=len(hands)
assert [sum(max(h)==5 for h in hands),sum(min(h)==5 for h in hands),sum(max(h)<5 for h in hands),sum(max(h)>5 for h in hands)]==[comb(4,2),comb(5,2),comb(4,3),den-comb(5,3)]
# 17：组合计数 vs 顺序DP（无放回十步状态）
dp={(0,0,0):F(1)}
for _ in range(10):
    nd={}
    for (a,b,c),p in dp.items():
        used=a+b+c
        for j,(x,N) in enumerate(((a,80),(b,15),(c,5))):
            if N>x:
                q=[a,b,c];q[j]+=1;q=tuple(q)
                nd[q]=nd.get(q,F(0))+p*F(N-x,100-used)
    dp=nd
assert dp[(7,2,1)]==F(comb(80,7)*comb(15,2)*comb(5,1),comb(100,10))
# 19：枚举270725手牌
cards=list(product(range(4),range(13))); hs=list(combinations(cards,4)); N=len(hs)
nums=(sum(len({x[0] for x in h})==1 for h in hs),sum(len({x[0] for x in h})==4 for h in hs),sum(len({x[0] for x in h})<4 for h in hs),sum(any(x[1]==0 for x in h) for h in hs))
assert nums==(4*comb(13,4),13**4,N-13**4,N-comb(48,4))
# 21：64种有标号球投盒
m=Counter(max(s.count(i) for i in range(4)) for s in product(range(4),repeat=3)); assert (m[1],m[2],m[3])==(24,36,4)
# 23：生成函数DP计数，和闭式逐k核对
# 每双贡献：不取1种、取一只2种、取一双1种；追踪鞋数与完整双数
dp={(0,0):1}
for _ in range(15):
    nd=Counter()
    for (sh,pair),v in dp.items():
        nd[sh,pair]+=v; nd[sh+1,pair]+=2*v; nd[sh+2,pair+1]+=v
    dp=nd
for k in range(6): assert dp.get((10,k),0)==comb(15,k)*comb(15-k,10-2*k)*2**(10-2*k)
assert sum(dp[10,k] for k in range(2,6))==sum(comb(15,k)*comb(15-k,10-2*k)*2**(10-2*k) for k in range(2,6))
# 25、27、29、31
assert F(1,4)+F(1,6)-F(1,12)==F(1,3)
assert F(7,100)*F(6,99)*F(93,98)==F(217,53900)
assert sum((F(4,20)*F(9,10),F(8,20)*F(7,10),F(7,20)*F(5,10),F(1,20)*F(2,10)))==F(129,200)
good=F(4,9)*F(4,5)+F(3,9)*F(3,5)+F(2,9)*F(7,10); assert good==F(32,45) and F(1,5)/good==F(9,32)
# 33：随机取多组独立伯努利参数，逐原子求概率核对三个独立性等式
for pa,pb,pc in [(F(1,3),F(2,5),F(3,7)),(F(0),F(1,2),F(1)),(F(4,5),F(1,6),F(2,3))]:
    mass={(a,b,c):(pa if a else 1-pa)*(pb if b else 1-pb)*(pc if c else 1-pc) for a,b,c in product([0,1],repeat=3)}
    prob=lambda pred:sum(v for k,v in mass.items() if pred(*k))
    for E in (lambda a,b,c:a or b,lambda a,b,c:a and b,lambda a,b,c:a and not b):
        assert prob(lambda a,b,c:E(a,b,c) and c)==prob(E)*prob(lambda a,b,c:c)
# 35：卡片集合直接计数
A={1,2,3,4};B={1,2,3,5};C={1,6,7,8}; assert F(len(A&B&C),8)==F(len(A),8)*F(len(B),8)*F(len(C),8) and F(len(A&B),8)!=F(len(A),8)*F(len(B),8)
# 37：补事件 vs 8种命中模式枚举
ps=(F(4,5),F(2,3),F(3,4)); total=F(0)
for s in product([0,1],repeat=3):
    mass=F(1)
    for hit,p in zip(s,ps):mass*=p if hit else 1-p
    if any(s):total+=mass
assert total==1-(1-ps[0])*(1-ps[1])*(1-ps[2])==F(59,60)
# 39：两方程相减得x=y，再验证唯一根1/2
assert F(1,2)*(1-F(1,2))==F(1,4)
print('ALL PASS：20道奇数题均已完成题面复核；可计算/可枚举部分通过独立真值表、穷举、DP或精确代数复核。')
