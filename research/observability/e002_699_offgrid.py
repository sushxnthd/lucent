"""E002-699 exact-rational off-grid closure falsifier. Python 3 stdlib."""
from fractions import Fraction as F

def tent(t, d, level, speed):
    return level-speed*min(t, d-t)

def test():
    n=0
    for d in (F(1,10), F(1,5), F(1,2), F(1)):
        for speed in (F(1,2),F(1),F(2)):
            threshold=F(1,2)
            level=threshold+speed*d/4
            assert tent(F(0),d,level,speed)>threshold
            assert tent(d,d,level,speed)>threshold
            assert tent(d/2,d,level,speed)<threshold
            assert tent(d/2,d,level,speed)==level-speed*d/2
            assert (level-tent(d/2,d,level,speed))/(d/2)==speed
            n+=1
    print('E002-699 PASS',n,'exact-rational hidden-closure witnesses')
    print('Example: d=1/5, L=1, threshold=1/2, samples=11/20, true min=9/20')
if __name__=='__main__':test()
