from fractions import Fraction as Q

def bounds(H,V,a,b,t):
    assert H>0 and V>0 and 0<t<1 and 0<=a<=1 and 0<=b<=1 and abs(a-b)<=V*H
    return min(H,(max(0,t-a)+max(0,t-b))/V),max(0,H-(max(0,a-t)+max(0,b-t))/V)

F,w=Q(1,30),Q(1,100)
H=F-w
t=Q(1,5)
assert H==Q(7,300)
assert bounds(H,Q(100),Q(1),Q(1),t)==(0,Q(11,1500))
assert bounds(H,Q(50),Q(1),Q(1),t)==(0,0)
assert 2*(1-t)/H==Q(480,7)
# Always-open vs hidden closure: both aperture signals equal 1 in all exposures.
for k in range(8):
    s,e=k*F,k*F+w
    assert e<=w or s>=F
# 500 Hz eye-reference resolves closure while ordinary RGB exposures cannot.
samples=[max(0,Q(1)-Q(100)*min(Q(j,500)-w,F-Q(j,500))) for j in range(6,17)]
assert sum(x<=t for x in samples)>0
print('PASS: exact rational collision and threshold transition')
