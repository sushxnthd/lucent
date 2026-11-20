"""E002-694: conservative exposure-mean to endpoint conversion; synthetic falsification."""
from fractions import Fraction as F
from itertools import product

def mean_piecewise(nodes, a, b):
    knots=sorted(set([a,b]+[t for t,_ in nodes if a<t<b]))
    def value(t):
        for (t0,x0),(t1,x1) in zip(nodes,nodes[1:]):
            if t0<=t<=t1:return x0+(x1-x0)*(t-t0)/(t1-t0)
        raise ValueError(t)
    return sum((value(p)+value(q))*(q-p)/2 for p,q in zip(knots,knots[1:]))/(b-a)

def certified_lower(m0,m1,T,h,V):
    # |x'|<=V implies aperture at exposure boundary >= exposure mean - V*T/2.
    a=m0-V*T/2; b=m1-V*T/2
    return (a+b-V*h)/2

def main():
    T=F(1,4); h=F(1,2); threshold=F(1,4)
    checked=0; false_robust=0; false_naive=0; robust=0; naive=0; witness=None
    # Five nodes: -T, 0, h/2, h, h+T; all adjacent slopes bounded by V=1.
    for heights in product([F(i,8) for i in range(9)],repeat=5):
        nodes=list(zip([-T,F(0),h/2,h,h+T],heights))
        V=F(1)
        if any(abs(y-x)>V*(b-a) for (a,x),(b,y) in zip(nodes,nodes[1:])):continue
        m0=mean_piecewise(nodes,-T,F(0));m1=mean_piecewise(nodes,h,h+T)
        truth=min(heights[1:4])
        r=certified_lower(m0,m1,T,h,V)>threshold
        n=(m0+m1-V*h)/2>threshold
        checked+=1;robust+=int(r);naive+=int(n)
        false_robust+=int(r and truth<=threshold)
        false_naive+=int(n and truth<=threshold)
        if n and truth<=threshold and witness is None:witness=(heights,m0,m1,truth)
    assert false_robust==0
    assert false_naive>0
    print(dict(feasible=checked,robust_certificates=robust,robust_false_exclusions=false_robust,naive_certificates=naive,naive_false_exclusions=false_naive,witness=str(witness)))
if __name__=='__main__':main()
