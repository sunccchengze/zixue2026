#!/usr/bin/env python3
"""Read-only numerical/structural checks of the three new AI diagnostic papers.

Standard library only. This checks selected numerical results and printed result
markers; it does not prove the entire exposition or certify official exam scope.
"""
from fractions import Fraction as F
import math
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def integrate(f, a, b, n=4000):
    h = (b-a)/n
    return (f(a)+f(b)+sum((4 if i%2 else 2)*f(a+i*h) for i in range(1,n)))*h/3


def verify():
    errors = []
    count = 0
    def check(name, actual, expected, tol=1e-8):
        nonlocal count
        count += 1
        if abs(float(actual)-float(expected)) > tol:
            errors.append(f'{name}: {actual} != {expected}')
    for course in ['大学物理', '大学化学', '概率论与数理统计']:
        base = ROOT / course / '考试复习/期中/AI模拟/卷01'
        q = (base/'题目.md').read_text()
        a = (base/'参考答案.md').read_text()
        check(course+' question count', len(re.findall(r'^\*\*[1-8]\. ', q, re.M)), 8)
        check(course+' answer count', len(re.findall(r'^### [1-8]（', a, re.M)), 8)
        check(course+' total points', 4*10+4*15, 100)
        for value in ['100分', '90分钟', '不是真题', '孙承泽', '2253710052', '能动强基2501']:
            check(course+' paper marker '+value, value in q, True)
    a = (ROOT/'大学物理/考试复习/期中/AI模拟/卷01/参考答案.md').read_text()
    for marker in ['−0.040√3π', '3.00 mm', '200 nm', '10.0 mm', '共5条', '7.50', '60°']:
        check('physics printed '+marker, marker in a, True)
    check('wave speed', 4*math.pi/(2*math.pi), 2)
    check('point displacement', .020*math.cos(math.pi/3), .010)
    check('point velocity', -.020*4*math.pi*math.sin(math.pi/3), -.040*math.sqrt(3)*math.pi)
    check('Young spacing m', 600e-9*1.5/.300e-3, .003)
    check('film fringe shift', (.50*1.20e-6)/600e-9, 1)
    check('film minimum m', 600e-9/(2*1.5), 200e-9)
    check('single slit width m', 2*500e-9*2/.200e-3, .010)
    d = 1/(600e3)
    check('geometrical orders', math.floor(d/500e-9), 3)
    visible = [k for k in range(-3,4) if k == 0 or k % 3]
    check('visible orders', len(visible), 5)
    check('three polarizers', 80/2*math.cos(math.pi/6)**2*math.cos(math.pi/3)**2, 7.5)
    check('Brewster degrees', math.degrees(math.atan(math.sqrt(3))), 60)
    check('refraction degrees', math.degrees(math.asin(math.sin(math.pi/3)/math.sqrt(3))), 30)
    a = (ROOT/'大学化学/考试复习/期中/AI模拟/卷01/参考答案.md').read_text()
    for marker in ['10电子', '101.390', '1.86', '500/509', '−70 J', '−120 J', '−890.3', '400 K']:
        check('chemistry printed '+marker, marker in a, True)
    check('d electrons capacity', 2*(2*2+1), 10)
    check('ideal gas kPa', .5*8.314*300/12.3, 101.39024390243902)
    check('molality', (6/60)/.1, 1)
    check('freezing decrease', 1.86*(6/60)/.1, 1.86)
    check('water mole fraction', F(100,18)/(F(100,18)+F(1,10)), F(500,509))
    check('first law', -120+50, -70)
    check('enthalpy', -70-50, -120)
    check('combustion enthalpy', -393.5+2*(-285.8)-(-74.8), -890.3)
    check('quarter mol heat', .25*(-890.3), -222.575)
    check('Gibbs 298', 40-298*.1, 10.2)
    check('Gibbs 500', 40-500*.1, -10)
    check('zero standard Gibbs T', 40/.1, 400)
    a = (ROOT/'概率论与数理统计/考试复习/期中/AI模拟/卷01/参考答案.md').read_text()
    for marker in ['3/7', '18/67', '0.61', '7/8', '(5/2)y^(3/2)', '5/7', '1/6', '−1/9', '−1/2', '9.4']:
        check('probability printed '+marker, marker in a, True)
    check('combinations', F(math.comb(4,2)*math.comb(6,2),math.comb(10,4)), F(3,7))
    check('Bayes', F(2,100)*F(9,10)/(F(2,100)*F(9,10)+F(98,100)*F(5,100)), F(18,67))
    check('discrete variance', F(23,10)-F(13,10)**2, F(61,100))
    check('density normalization', integrate(lambda x:3*x*x,0,1), 1)
    check('tail', integrate(lambda x:3*x*x,.5,1), F(7,8))
    check('transformed normalization', integrate(lambda y:2.5*y**1.5,0,1), 1)
    check('EY via X', integrate(lambda x:x*x*2.5*x**4,-1,1), F(5,7))
    check('EY via Y', integrate(lambda y:y*2.5*y**1.5,0,1), F(5,7))
    for y in [.04,.25,.64]:
        check('transform CDF '+str(y), integrate(lambda x:2.5*x**4,-math.sqrt(y),math.sqrt(y)), y**2.5)
    check('joint normalization', integrate(lambda y:4*y**3,0,1), 1)
    check('joint X+Y<1', integrate(lambda y:4*y**3,0,.5)+integrate(lambda y:4*y*(1-y)**2,.5,1), F(1,6))
    check('triangle EX', integrate(lambda x:x*(2-x)/2,0,2), F(2,3))
    check('triangle EX2', integrate(lambda x:x*x*(2-x)/2,0,2), F(2,3))
    check('triangle EXY', integrate(lambda x:x*(2-x)**2/4,0,2), F(1,3))
    check('triangle covariance', F(1,3)-F(2,3)**2, -F(1,9))
    check('triangle correlation', (-F(1,9))/F(2,9), -F(1,2))
    check('linear mean', 2*(10*.2)-3+4, 5)
    check('linear variance', 4*(10*.2*.8)+3, 9.4)
    return errors, count


if __name__ == '__main__':
    errors, count = verify()
    for error in errors:
        print('FAIL:', error)
    if not errors:
        print(f'PASS: {count} selected numeric/structure/printed-result checks; not official exam certification.')
    raise SystemExit(bool(errors))
