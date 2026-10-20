"""Full-RGB 11-frame collision: opposite true pupil trends, same pixels.
Ideal pinhole with unknown effective entrance-pupil depth; not human proof."""
from fractions import Fraction
from hashlib import sha256
import numpy as np
N=11;H=W=128;F=500
X,Y=np.meshgrid(np.arange(W)-W//2,np.arange(H)-H//2)
Ri=Fraction(3,5);Zi=Fraction(10);r0=Fraction(2,5)
def render(r,z):
    ir=float(F*Ri/Zi);pr=float(F*r/z)
    d=X*X+Y*Y
    out=np.empty((H,W,3),dtype=np.uint8)
    out[:]=(220,216,208)
    out[d<=ir*ir]=(102,123,80)
    out[d<=pr*pr]=(19,18,21)
    return out
for i in range(N):
    t=Fraction(i,10)
    ra=r0*(1+Fraction(1,100)*t)
    rb=r0*(1-Fraction(1,100)*t)
    za=Fraction(10);zb=za*rb/ra
    A=render(ra,za);B=render(rb,zb)
    assert np.array_equal(A,B)
    print(i,str(ra),str(rb),str(zb),sha256(A.tobytes()).hexdigest())
assert ra>r0 and rb<r0
assert 1-zb/za==Fraction(2,101)
print("PASS: 11 identical RGB frames, opposite slopes, depth change 2/101")
