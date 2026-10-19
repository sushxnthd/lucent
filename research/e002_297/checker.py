"""Exact rational counterexamples, independent of simulator."""
from fractions import Fraction as F
def ol(a,b,c,d):return max(F(0),min(b,d)-max(a,c))
def stat(x):
    w=F(2,3);return ol(-F(2),F(2),x-w/2,x+w/2)/w
def roll(x):
    q=F(3,4)*x;return 2*ol(F(0),F(1,2),q-F(5,4),q+F(7,4))
def contrast(x,A,w,C):
    return C*ol(-A/2,A/2,x-w/2,x+w/2)/w
if __name__=="__main__":
    for i in range(-300,301):
        x=F(i,100)
        assert stat(x)==roll(x)
        assert contrast(x,F(2),F(4),F(2))==contrast(x,F(4),F(2),F(1))
    assert F(3)/(1-F(1,4))==F(4)
    print("PASS: 601 exact rolling and contrast collisions")
