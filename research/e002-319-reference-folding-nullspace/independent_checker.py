"""Independent tests of the published rowwise three-block average."""
from fractions import Fraction
import numpy as np
N=90
a=[Fraction(j%11,100) for j in range(N)]
x=[3+v for v in a]+[3-v for v in a]+[Fraction(3)]*N
z=[3-v for v in a]+[3+v for v in a]+[Fraction(3)]*N
fold=lambda q:[(q[j]+q[j+N]+q[j+2*N])/3 for j in range(N)]
assert x!=z and fold(x)==fold(z)==[3]*N
rng=np.random.default_rng(91218)
for _ in range(1000):
    v=rng.normal(size=270)
    y=(v[:90]+v[90:180]+v[180:])/3
    assert abs(y.mean()-v.mean())<1e-12
for phase in np.linspace(-3,3,101):
    t=np.arange(270)/90
    v=3+.2*np.sin(2*np.pi*t/3+phase)
    assert np.max(abs((v[:90]+v[90:180]+v[180:])/3-3))<1e-12
for j in (0,45,89):
    t=j/30
    v=3+.2*abs(np.arange(270)/90-t)
    y=(v[j]+v[j+90]+v[j+180])/3
    b=sum(abs(k+j/90-t) for k in range(3))/3
    assert abs(abs(y-v[3*j])-.2*b)<1e-12
print("PASS: exact rational collision, 1000 mean trials, 101 phase trials, sharp Lipschitz witnesses")
