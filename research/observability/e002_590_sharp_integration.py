#!/usr/bin/env python3
"""E002-590: exact-rational full-duty alias threshold. Synthetic operator only."""
from fractions import Fraction as F
from itertools import pairwise
import json

def critical(c):
    assert 0 < c < 1
    return 4*c if c <= F(1,2) else 1/(1-c)

def maximum_mean(L):
    assert L>0
    return L/4 if L<=2 else 1-1/L

def extremizer(c,L):
    assert L>=2*c
    t=c/L
    if L<=2:
        return [(F(0),c),(t,F(0)),(t+F(1,2),L/2),(F(1),c)]
    return [(F(0),c),(t,F(0)),((c+1)/L,F(1)),(1-(1-c)/L,F(1)),(F(1),c)]

def integrate(knots,L):
    area=F(0); speeds=[]
    for (x,y),(xx,yy) in pairwise(knots):
        assert xx>x and 0<=y<=1 and 0<=yy<=1
        speeds.append(abs((yy-y)/(xx-x)))
        area+=(xx-x)*(y+yy)/2
    assert knots[0]==(F(0),knots[-1][1]) and knots[-1][0]==1
    assert min(y for _,y in knots)==0 and max(speeds)<=L
    return area,max(speeds)

def run():
    grid=[]
    for n in range(1,20):
        c=F(n,20); L=critical(c)
        area,speed=integrate(extremizer(c,L),L)
        assert area==c and speed==L
        lower=L*F(99,100)
        assert lower>=2*c and maximum_mean(lower)<c
        grid.append({'c':str(c),'Lcrit':str(L),'subthreshold_max_mean':str(maximum_mean(lower))})
    examples=[]
    for c in (F(1,5),F(1,2),F(4,5)):
        L=critical(c); knots=extremizer(c,L); area,_=integrate(knots,L)
        examples.append({'c':str(c),'Lcrit':str(L),'mean':str(area),
            'knots':[[str(t),str(a)] for t,a in knots]})
    assert [critical(c)*30 for c in (F(1,5),F(1,2),F(4,5))]==[24,60,150]
    print(json.dumps({'evidence':'exact idealized synthetic operator; no human/physical evidence',
        'critical_cases_verified':19,'subthreshold_rejections':19,
        'examples':examples,'grid':grid,
        'illustrative_Vcrit_per_second_at_30fps':['24','60','150']},
        sort_keys=True,indent=2))

if __name__=='__main__':
    run()
