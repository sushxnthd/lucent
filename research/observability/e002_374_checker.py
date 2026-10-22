"""E002-374 exact nonlinear shutter-moment and photometric-gauge checker; stdlib only."""
from fractions import Fraction as Q
from math import factorial
S=[(Q(15,2),Q(0)),(Q(5,2),-Q(1,50)),(Q(5,2),-Q(1,50)),
   (Q(25,6),Q(0)),(Q(5),Q(1,50)),(Q(5),Q(1,50)),
   (Q(25,6),Q(0)),(Q(5,2),-Q(1,50)),(Q(5,2),-Q(1,50)),(Q(15,2),Q(0))]
def rows():
    t,a,v=Q(-10),Q(1),Q(0);out=[]
    for dt,u in S:
        out.append((t,dt,a,v,u))
        t,a,v=t+dt,a+v*dt+u*dt*dt/2,v+u*dt
    assert (t,a,v)==(Q(100,3),Q(1),Q(0))
    return out
def poly_integral(row,p):
    _,dt,a,v,u=row;co=[Q(1)]
    for _ in range(p):
        nxt=[Q(0)]*(len(co)+2)
        for j,c in enumerate(co):
            nxt[j]+=c*a;nxt[j+1]+=c*v;nxt[j+2]+=c*u/2
        co=nxt
    return sum(c*dt**(j+1)/(j+1) for j,c in enumerate(co))
def weights(n):
    a=[[Q(j,n)**k for j in range(n+1)]+[Q(1,k+1)] for k in range(n+1)]
    for c in range(n+1):
        pivot=next(i for i in range(c,n+1) if a[i][c])
        a[c],a[pivot]=a[pivot],a[c]
        z=a[c][c];a[c]=[x/z for x in a[c]]
        for i in range(n+1):
            if i!=c:
                z=a[i][c];a[i]=[a[i][j]-z*a[c][j] for j in range(n+2)]
    return [r[-1] for r in a]
def quad_integral(row,p):
    _,dt,a,v,u=row;n=2*p
    return dt*sum(w*(a+v*dt*Q(j,n)+u*(dt*Q(j,n))**2/2)**p for j,w in enumerate(weights(n)))
def check():
    rr=rows();M=[]
    for p in (1,2,3):
        ms=[]
        for ex in (rr[:2],rr[-2:]):
            x=sum(poly_integral(r,p) for r in ex)/10
            y=sum(quad_integral(r,p) for r in ex)/10
            assert x==y
            ms.append(x)
        assert ms[0]==ms[1]
        M.append(ms[0])
    m=M[0];C=[m**k for k in (1,2,3)]
    assert m==Q(191,192) and M[1]-C[1]==Q(31,184320)
    g2=(M[1]-M[0])/(C[1]-C[0]);b2=M[0]-g2*C[0]
    assert (g2,b2)==(Q(924,955),Q(31,960))
    assert all(M[i]==g2*C[i]+b2 for i in (0,1))
    w=[C[1]-C[2],C[2]-C[0],C[0]-C[1]]
    assert sum(w)==0 and sum(w[i]*C[i] for i in range(3))==0
    d=abs(sum(w[i]*M[i] for i in range(3)))/sum(abs(x) for x in w)
    assert d==Q(3313,82360320)
    g=((M[0]-d)-(M[1]+d))/(C[0]-C[1]);b=M[0]-d-g*C[0]
    assert (g,b)==(Q(2437488,2560355),Q(3419,71680))
    assert [M[i]-g*C[i]-b for i in range(3)]==[d,-d,d]
    def quant(x,bits):
        z=2**bits-1
        return (2*x.numerator*z+x.denominator)//(2*x.denominator)
    for bits in (8,10,12,16):
        lhs=[quant(x,bits) for x in M]
        rhs=[quant(g*x+b,bits) for x in C]
        assert (lhs==rhs)==(bits<16)
        print(bits,'bit codes',lhs,rhs)
    assert d>2*Q(19,1000000) and d<2*Q(21,1000000)
    print('PASS exact polynomial/quadrature, 2-channel collision, 3-channel dual certificate, quantization')
    print('minimax delta=',d,'symmetric error threshold=',d/2)
if __name__=='__main__':check()
