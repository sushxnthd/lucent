"""E002-753: exact exposure-kernel adversarial detector test. No human evidence."""
from fractions import Fraction as F

def overlap(a,b,c,d): return max(F(0), min(b,d)-max(a,c))

def response(event_start, duration, weights):
    # Piecewise constant density, each segment [start,end,density].
    return sum((overlap(event_start,event_start+duration,a,b)*w for a,b,w in weights),F(0))

def main():
    uniform=[(F(0),F(1),F(1))]
    front=[(F(0),F(1,4),F(4)),(F(1,4),F(1),F(0))]
    rear=[(F(0),F(3,4),F(0)),(F(3,4),F(1),F(4))]
    threshold=F(3,4); duration=F(1,4)
    for name,k in [('uniform',uniform),('front',front),('rear',rear)]:
        assert sum(((b-a)*w for a,b,w in k),F(0))==1
        counts=sum(response(F(i,10000),duration,k)>=threshold for i in range(7501))
        print(name,counts,'of 7501 admissible phases')
    assert response(F(0),duration,uniform)==F(1,4)
    assert response(F(0),duration,front)==1
    assert response(F(0),duration,rear)==0
    assert response(F(3,4),duration,rear)==1
    assert duration/(threshold*F(1))==F(1,3)
    print('PASS: kernel counterexamples and exact phase enumeration')
if __name__=='__main__': main()
