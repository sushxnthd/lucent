"""E002-378 exact-rational nuisance-quotient checker. Synthetic only."""
from fractions import Fraction as Q
from random import Random
V=(Q(0),Q(1),Q(1),Q(0))
X=(Q(-3),Q(-1),Q(1),Q(3))
W=(Q(-1,4),Q(1,4),Q(1,4),Q(-1,4))
def dot(a,b): return sum((u*v for u,v in zip(a,b)),Q(0))
assert dot(W,V)==Q(1,2) and dot(W,X)==0 and sum(W)==0
def overlap(a,b,c,d):return max(Q(0),min(b,d)-max(a,c))
def rho(k,phase=Q(41),D=Q(42),F=Q(50),w=Q(10)):
    t=phase+k*F
    return overlap(t,t+w,Q(0),D)/w
def distance(r,A,b):return max(Q(0),r*A-2*b)/2
def collision(A,b,eps):
    """Exact common RGB stack for 4 frames x 3 channels x 4 pixels."""
    worst=Q(0);channels=0
    for k in (-1,0,1,2):
        r=rho(k)
        for scale in (Q(1),Q(2,3),Q(1,3)):
            z=r*A*scale;t=min(b,z/2);alpha=-(z-2*t)/2
            h0=[Q(1,5)+t*v for v in V]
            h1=[Q(1,5)+(z-t)*v+alpha for v in V]
            midpoint=[(a+c)/2 for a,c in zip(h0,h1)]
            e0=max(abs(y-a) for y,a in zip(midpoint,h0))
            e1=max(abs(y-a) for y,a in zip(midpoint,h1))
            assert e0==e1
            assert all(Q(0)<=x<=Q(1) for x in h0+h1+midpoint)
            worst=max(worst,e0);channels+=4
    return worst<=eps,worst,channels
def run():
    assert max(rho(k) for k in (-1,0,1,2))==Q(1,10)
    eps=Q(1,100);A=Q(3,5)
    for b,expected in [(Q(9,1000),False),(Q(1,100),True),(Q(11,1000),True)]:
        coll,worst,n=collision(A,b,eps)
        assert coll==expected and n==48
        assert coll==(distance(Q(1,10),A,b)<=2*eps)
        print('b=',float(b),'distance=',float(distance(Q(1,10),A,b)),
              'collision=',coll,'max_noise=',float(worst))
    assert all(v==(Q(9)-x*x)/8 for v,x in zip(V,X))
    rng=Random(378)
    for _ in range(400):
        r=Q(rng.randint(1,20),100);a=Q(rng.randint(1,60),100)
        b=Q(rng.randint(0,15),1000);t=min(b,r*a/2)
        alpha=-(r*a-2*t)/2
        h0=[t*v for v in V];h1=[(r*a-t)*v+alpha for v in V]
        assert max(abs(x-y) for x,y in zip(h0,h1))==distance(r,a,b)
    print('PASS: 3 boundary cases, 48 RGB components per case, 400 rational checks')
if __name__=='__main__':run()
